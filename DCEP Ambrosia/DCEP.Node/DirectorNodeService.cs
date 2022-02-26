using System.Runtime.CompilerServices;
using System.Linq;
using System.Collections.Generic;
using System.Diagnostics;
using System.Runtime.Serialization;
using System.Threading;
using DCEP.Core;
using DCEP.AmbrosiaNodeAPI;
using System;
using System.Threading.Tasks;
using DCEP.Core.DCEPControlMessage;
using DCEP.Core.Utils;

namespace DCEP.Node
{

    [DataContract]
    public class DirectorNodeService
    {
        [DataMember] private bool keepRunning = true;
        [DataMember] Stopwatch stopwatch = new Stopwatch();
        [DataMember] NodeExecutionState systemState;
        [DataMember] HashSet<NodeName> nodesToWaitWithStartingFor;
        [DataMember] private readonly IEnumerable<NodeName> allNodeNames;
        [DataMember] private readonly DCEPSettings settings;
        //Dictionary<NodeName, IAmbrosiaNodeProxy> nodedict;
        [DataMember] private double durationMS;

        [DataMember] Dictionary<NodeName, double> lastReadyToTerminateSignalTime;

        [DataMember] private string TAG { get; set; }

        [DataMember] private Dictionary<NodeName, ExperimentRunData> experimentRunDataByNodeName;
        private INodeProxyProvider proxyProvider;

        [DataMember] private SerializableQueue<ExperimentRunNodeDataMessage> experimentRunMessageQueue;
        [DataMember] public  bool localNodeCanTerminate;

        public DirectorNodeService(string TAG, IEnumerable<NodeName> allNodeNames, INodeProxyProvider proxyProvider, DCEPSettings settings){
            this.TAG = TAG + "[DirectorNodeService] ";
            this.allNodeNames = allNodeNames;
            this.settings = settings;
            this.localNodeCanTerminate = false;
            if (settings.duration != 0){
                this.durationMS = settings.timeUnit.GetTimeSpanFromDuration(settings.duration).TotalMilliseconds;
            }

            experimentRunMessageQueue = new SerializableQueue<ExperimentRunNodeDataMessage>();
            
            nodesToWaitWithStartingFor = new HashSet<NodeName>(allNodeNames);
            systemState = NodeExecutionState.WaitForStart;

            lastReadyToTerminateSignalTime = new Dictionary<NodeName, double>();
            experimentRunDataByNodeName = new Dictionary<NodeName, ExperimentRunData>();

            foreach (var nodeName in allNodeNames)
            {
                lastReadyToTerminateSignalTime[nodeName] = -1;
                experimentRunDataByNodeName[nodeName] = null;
            }

            this.proxyProvider = proxyProvider;
            
            Thread t = new Thread(new ThreadStart(threadStartMethod));
            t.Start();
        }

        public void threadStartMethod()
        {
            while (keepRunning)
            {
                switch (systemState)
                {
                    case NodeExecutionState.WaitForStart:
                        // check if nodes are ready to start and start them when everyone is ready
                        if(nodesToWaitWithStartingFor.Count() == 0){
                            Console.WriteLine(TAG+" All nodes ready. Transitioning into run phase.");
                            broadcastUpdatedExecutionState(NodeExecutionState.DoStartInputGeneration);

                            if (settings.duration == 0){
                                Console.WriteLine(TAG + "running indefinitely from now on, DirectorNodeService is terminating.");
                                return;
                            }

                            systemState = NodeExecutionState.Running;
                            stopwatch.Start();
                        } else {
                            Console.WriteLine(TAG + "Waiting for node(s) " + string.Join(",", nodesToWaitWithStartingFor.Select(x => x.ToString())) + " to signal they are ready to start.");
                            Thread.Sleep(1000);

                        }
                        break;

                    case NodeExecutionState.Running:
                        // check the timer and send "stop input generation" requests once the timer is over 
                        if ((stopwatch.ElapsedMilliseconds - this.durationMS) > 0){
                            broadcastUpdatedExecutionState(NodeExecutionState.DoStopInputGeneration);
                            systemState = NodeExecutionState.ProcessingRemainder;
                            Console.WriteLine(TAG + "Requested to stop input event generation on all nodes. Now waiting for all nodes to finish processing their event queues.");

                        }
                        
                        break;

                    case NodeExecutionState.ProcessingRemainder:
                        // wait until all message queues are empty, then possibly count messages and send "terminate" requests
                        var nowMS = stopwatch.ElapsedMilliseconds;
                        
                        if (lastReadyToTerminateSignalTime.Values.ToList().All(timestamp => timestamp != -1 && nowMS - timestamp < 1000))
                        {
                            Console.WriteLine(TAG + "Done. All nodes signaled their queues are empty within the last second. Requesting to terminate query processing on all nodes.");
                            broadcastUpdatedExecutionState(NodeExecutionState.DoSendExperimentDataAndTerminate);
                            

                            // gathering experiment run data
                            Console.WriteLine(TAG + "Waiting for all nodes to send their ExperimentRunData");

                            while(experimentRunDataByNodeName.Values.ToList().Contains(null)){

                                while (!experimentRunMessageQueue.Data.IsEmpty)
                                {
                                    ExperimentRunNodeDataMessage m = null;
                                    if (experimentRunMessageQueue.Data.TryDequeue(out m))
                                    {
                                        experimentRunDataByNodeName[m.sendingNode] = m.nodeData;
                                        Console.WriteLine(TAG + "Received experiment data from node "+m.sendingNode);
                                    }
                                }

                                Thread.Sleep(100);


                            }

                            // all experiment data was received
                            Console.WriteLine(TAG + "ExperimentRunData was received from all nodes. Printing the result and terminating.");

                            long totalSentEvents = 0;
                            long totalGeneratedComplexEvents = 0;
                            long totalGeneratedPrimtiveEvents = 0;
                            long totalDroppedComplexEvents = 0;
                            long totalDroppedPartialMatches = 0;

                            foreach (var item in experimentRunDataByNodeName)
                            {
                                totalSentEvents += item.Value.receivedEventCount;
                                totalGeneratedComplexEvents += item.Value.locallyGeneratedComplexEventCount;
                                totalGeneratedPrimtiveEvents += item.Value.locallyGeneratedPrimitiveEventCount;
                                totalDroppedComplexEvents += item.Value.locallyDroppedComplexEvents;
                                totalDroppedPartialMatches += item.Value.locallyDroppedPartialMatches;
                            }

                            Console.WriteLine("");
                            Console.WriteLine("Total number of generated complex events:  " + totalGeneratedComplexEvents);
                            Console.WriteLine("Total number of generated primitive events:  " + totalGeneratedPrimtiveEvents);
                            Console.WriteLine("Total number of events sent over network:  " + totalSentEvents);
                            Console.WriteLine("Total number of dropped complex events: " + totalDroppedComplexEvents);
                            Console.WriteLine("Total number of dropped partial matches: " + totalDroppedPartialMatches);
                            localNodeCanTerminate = true;
                            return;

                        } else {
                            Thread.Sleep(100);
                        }
                        
                        break;
                }
            }
        }

        public void terminateAllNodesImmediately()
        {
            broadcastUpdatedExecutionState(NodeExecutionState.DoSendExperimentDataAndTerminate);
        }

        private void broadcastUpdatedExecutionState(NodeExecutionState newstate){
            var m = new UpdatedExecutionStateMessage(settings.directorNodeName, newstate);
            foreach (var item in allNodeNames)
            {
                (proxyProvider.getProxy(item) as IAmbrosiaNodeProxy).ReceiveDCEPControlMessageFork(m);
            }
        }


        void ReceiveReadyToLaunchNotification(NodeIsReadyToStartMessage message)
        {
            if (systemState.Equals(NodeExecutionState.WaitForStart)){
                Console.WriteLine(TAG + "received ready to start message from " +message.sendingNode.ToString());
                nodesToWaitWithStartingFor.Remove(message.sendingNode);
            } {
               Console.WriteLine(TAG + "received ready to start message from " + message.sendingNode.ToString() +" but ignoring it due to being in systemState=."+systemState);
            }
        }

        void ReceiveNodeIsReadyToTerminateNotification(NodeIsReadyToTerminateMessage message)
        {
            if (systemState.Equals(NodeExecutionState.ProcessingRemainder))
            {
                lastReadyToTerminateSignalTime[message.sendingNode] = stopwatch.ElapsedMilliseconds;
            }
        }

        void ReceiveExperimentRunData(ExperimentRunNodeDataMessage message){
            experimentRunMessageQueue.Data.Enqueue(message);
        }

        internal void ProcessNodeInfoForCoordinatorMessage(NodeInfoForCoordinatorMessage m)
        {
            if (m is NodeIsReadyToTerminateMessage){
                ReceiveNodeIsReadyToTerminateNotification(m as NodeIsReadyToTerminateMessage);
            } else if (m is ExperimentRunNodeDataMessage) {
                ReceiveExperimentRunData(m as ExperimentRunNodeDataMessage);
            } else if (m is NodeIsReadyToStartMessage){
                ReceiveReadyToLaunchNotification(m as NodeIsReadyToStartMessage);
            }
        }
    }
}