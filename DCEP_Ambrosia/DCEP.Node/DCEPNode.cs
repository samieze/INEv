using System.Diagnostics;
using System;
using System.Globalization;
using DCEP.Core.QueryProcessing;
using System.Runtime.Serialization;
using System.Threading;
using System.Threading.Tasks;
using System.Collections.Generic;
using System.Linq;
using System.Collections.Concurrent;
using System.Linq.Expressions;
using DCEP.Core;
using DCEP.AmbrosiaNodeAPI;
using DCEP.Core.Utils;
using DCEP.Node.Benchmarking;
using DCEP.Core.DCEPControlMessage;

namespace DCEP.Node
{
    [DataContract]
    public class DCEPNode : IAmbrosiaNode
    {
        [DataMember] NodeExecutionState state;
        [DataMember] private readonly SerializableQueue<AbstractEvent> externalEventQueue;
        [DataMember] private readonly SerializableQueue<AbstractEvent> internalEventQueue;
        [DataMember] private readonly SerializableQueue<DCEPControlMessage> controlMessageQueue;
        [DataMember] public Dictionary<EventType, ForwardRule> forwardRules { get; set; }
        [DataMember] private readonly DCEPSettings settings;
        [DataMember] private readonly string TAG;
        [DataMember] private bool dataSetMode; //new
        [DataMember] public long receivedEventCount { get; set; }
        [DataMember] public long locallyGeneratedComplexEventCount { get; set; }
        [DataMember] public long locallyGeneratedPrimitiveEventCount { get; set; }
        
        [DataMember] public long locallyDroppedComplexEvents { get; set; }
        [DataMember] public long locallyDroppedPartialMatches { get; set; }
        [DataMember] public NodeName nodeName { get; set; }
        [DataMember] private List<QueryProcessor> queryProcessors;
        [DataMember] private ForwardRuleProcessor forwardRuleProcessor;
        [DataMember] private Random randomNumberGenerator = new Random(); // for the implementation of selection rates
        [DataMember] Stopwatch stopwatch = new Stopwatch(); // for performance benchmarking
        [DataMember] ExecutionPlan executionPlan;
        [DataMember] private readonly BenchmarkMeter benchmarkMeter;
        [DataMember] PrimitiveEventSourceService primitiveEventSourceService;
        [DataMember] private DirectorNodeService directorNodeService = null;
        //private Dictionary<NodeName, IAmbrosiaNodeProxy> proxyDict;
        //private IAmbrosiaNodeProxy directorNodeProxy { get; set; }
        //private IAmbrosiaNodeProxy thisProxy { get; set; }

        private INodeProxyProvider proxyProvider;
        [DataMember] long lastStatusMessageToCoordinator = -1;
        [DataMember] private bool sentReadyToStartMessage;
        [DataMember] private long _remainingTimeLastPrintTime = 0;
        [DataMember] private long _remainingTimeLastProcessedCount = 0;
        
        [DataMember] private ConcurrentDictionary<NodeName, DateTime> TimestampsDict = new ConcurrentDictionary<NodeName, DateTime>(); // Samira
        [DataMember] private DateTime oldestTimestamp = DateTime.MinValue; // Samira
        public DCEPNode(NodeName name, string[] inputlines, DCEPSettings settings)
        {
            TAG = "[" + name + "] ";
            Console.WriteLine(TAG + "DCEPNode Constructor called.");
            state = NodeExecutionState.WaitForStart;
            receivedEventCount = 0;
            sentReadyToStartMessage = false;
            nodeName = name;
            externalEventQueue = new SerializableQueue<AbstractEvent>();
            internalEventQueue = new SerializableQueue<AbstractEvent>();
            controlMessageQueue = new SerializableQueue<DCEPControlMessage>();
            queryProcessors = new List<QueryProcessor>();
            this.settings = settings;
            executionPlan = new ExecutionPlan(inputlines);
            benchmarkMeter = new BenchmarkMeter(settings, nodeName);
            createQueryProcessors(executionPlan.queriesByNodeName[nodeName]);
            dataSetMode = false; // new
        }

        private void initPrimitiveEventSourceService()
        {
            switch (executionPlan.primitiveInputMode)
            {
                case PrimitiveInputMode.RANDOM_WITH_RATES:
                    primitiveEventSourceService =  new RandomPrimitiveEventGenerationService(nodeName,
                        executionPlan.networkPlan[nodeName],
                        proxyProvider,
                        settings);
                    break;
            
                case PrimitiveInputMode.DATASET:
                    dataSetMode = true; //new
                    primitiveEventSourceService = new DatasetPrimitiveEventInputService(proxyProvider,
                        TAG,
                        executionPlan.datasetFileNameTemplate,
                        nodeName,
                        settings,
                        executionPlan.networkPlan[nodeName]);
                    break;
            
                default:
                    throw new ArgumentException("Unknown primitiveInputMode in executionPlan.");
            }
        }

        public void onFirstStart(INodeProxyProvider proxyProvider){
            this.proxyProvider = proxyProvider;

            /*proxyDict = new Dictionary<NodeName, IAmbrosiaNodeProxy>();
            
            foreach (var nName in executionPlan.networkPlan.Keys)
            {
                proxyDict[nName] = proxyProvider.getProxy(nName);
            }
            */
            if (settings.directorNodeName == null){
                throw new ArgumentException(TAG + "DirectorNodeName must not be null.");
            }

            /*if (proxyDict.Keys.Contains(settings.directorNodeName)){
                throw new ArgumentException(TAG + "DirectorNodeName " + settings.directorNodeName.ToString() + " could not be found in proxydict.");
            }*/

            //directorNodeProxy = proxyDict[settings.directorNodeName];
            //thisProxy = proxyDict[nodeName];
            
            var forwardRules = executionPlan.forwardRulesByNodeName[nodeName];
            this.forwardRuleProcessor = new ForwardRuleProcessor(TAG, forwardRules, proxyProvider);

            initPrimitiveEventSourceService();

            if (this.nodeName.Equals(settings.directorNodeName))
            {
                directorNodeService = new DirectorNodeService(TAG,
                                                              executionPlan.networkPlan.Keys.ToList(),
                                                              proxyProvider,
                                                              settings);
            }
      
            
        }

        public void threadStartMethod()
        {
            stopwatch.Start();

            while (true)
            {
                processControlMessages();

                switch (state)
                {
                    case NodeExecutionState.WaitForStart:
 /*                        // broadcast isready signal to directorNode every second
                        if (stopwatch.ElapsedMilliseconds - lastStatusMessageToCoordinator > 1000){
                            proxyProvider.getProxy(settings.directorNodeName).ReceiveDCEPControlMessageFork(new NodeIsReadyToStartMessage(nodeName));
                            //Console.WriteLine(TAG + "sending ready to start message to director node "+settings.directorNodeName.ToString());
                            lastStatusMessageToCoordinator = stopwatch.ElapsedMilliseconds;
                        } */

                        if (!sentReadyToStartMessage){
                            proxyProvider.getProxy(settings.directorNodeName).ReceiveDCEPControlMessageFork(new NodeIsReadyToStartMessage(nodeName));
                            sentReadyToStartMessage = true;
                        }

                    break;

                    case NodeExecutionState.DoStartInputGeneration:
                        // TODO: check if this is not already running and throw an error if it is
                        primitiveEventSourceService.start();
                        state = NodeExecutionState.Running;
                        processingStep();
                    break;

                    case NodeExecutionState.Running:
                        processingStep();
                    break;

                    case NodeExecutionState.DoStopInputGeneration:
                        primitiveEventSourceService.stop();
                        state = NodeExecutionState.ProcessingRemainder;

                    break;

                    case NodeExecutionState.ProcessingRemainder:
                        processingStep();
                        
                        // when queues are empty, send isReadyToTerminate message every second 
                        if (getQueuedEventCount() == 0)
                        {
                            if (stopwatch.ElapsedMilliseconds - lastStatusMessageToCoordinator > 1000)
                            {
                                proxyProvider.getProxy(settings.directorNodeName)
                                    .ReceiveDCEPControlMessageFork(new NodeIsReadyToTerminateMessage(nodeName));
                                lastStatusMessageToCoordinator = stopwatch.ElapsedMilliseconds;
                            }
                        }

                        break;

                    case NodeExecutionState.DoSendExperimentDataAndTerminate:

                       
                        var data = new ExperimentRunData(
                            locallyGeneratedComplexEventCount,
                            receivedEventCount,
                            locallyGeneratedPrimitiveEventCount,
                            locallyDroppedComplexEvents,
                            locallyDroppedPartialMatches);
                        
                        proxyProvider.getProxy(settings.directorNodeName).ReceiveDCEPControlMessageFork(new ExperimentRunNodeDataMessage(nodeName, data));
                        Console.WriteLine(TAG + "Sent experiment data. Update loop is terminating.");
                        Thread.Sleep(500);
                        if (getQueuedEventCount() > 0)
                        {
                            Console.WriteLine(TAG + String.Format("WARNING: requested to terminate with {0} events left in queue.", getQueuedEventCount()));
                        }

                        if (directorNodeService != null){
                            while(!directorNodeService.localNodeCanTerminate){
                                processControlMessages();
                            }
                        }
                        return;



                    case NodeExecutionState.DoTerminate:
                        if (getQueuedEventCount() > 0){
                            Console.WriteLine(TAG + String.Format("WARNING: requested to terminate with {0} events left in queue.", getQueuedEventCount()));
                        }
                        return;
                }

            }
        }

        public long getQueuedEventCount()
        {
            return internalEventQueue.Data.LongCount() + externalEventQueue.Data.LongCount();
        }

        private void createQueryProcessors(IEnumerable<Query> queries)
        {
            var timeWindow = settings.timeUnit.GetTimeSpanFromDuration(settings.timeWindow);
            timeWindow = timeWindow.Multiply(1.0 / settings.datasetSpeedup);
            
            foreach (var q in queries)
            {
                var processor = QueryProcessor.getQueryProcessorForQuery(q, timeWindow, executionPlan, nodeName);
                if (processor != null)
                {
                    queryProcessors.Add(processor);
                }
                else
                {
                    Console.WriteLine(TAG + String.Format("!WARNING! - Inactive Query '{0}' due not no matching QueryProcessor implementation.", q.ToString()));
                }
            }
        }

        public void processControlMessages(){
            while(!controlMessageQueue.Data.IsEmpty){
                DCEPControlMessage controlMessage = null;
                if (controlMessageQueue.Data.TryDequeue(out controlMessage)){

                    if (controlMessage is NodeInfoForCoordinatorMessage){
                        directorNodeService.ProcessNodeInfoForCoordinatorMessage(controlMessage as NodeInfoForCoordinatorMessage);

                    } else if (controlMessage is UpdatedExecutionStateMessage){
                        var newState = (controlMessage as UpdatedExecutionStateMessage).newState;
                        Console.WriteLine(TAG + "updated execution state from " + state.ToString() + " to "+newState.ToString());
                        state = newState;
                    }
                }
            }
        }

        public async Task<int> ReceiveDCEPControlMessageAsync(DCEPControlMessage controlMessage)
        {
            controlMessageQueue.Data.Enqueue(controlMessage);
            return 0;
        }

        public async Task<int> ReceiveExternalEventAsync(AbstractEvent e)
        {
            receivedEventCount++;
            externalEventQueue.Data.Enqueue(e);

            return 0;
        }

        public void processingStep(){
            
            
            if (getQueuedEventCount()>10000 & dataSetMode) // Samira [ "artificial" input buffer of size 10000 - only works for reading input from file]
            {
               //Console.WriteLine(TAG + $"Buffer capacity full!!!!");
               primitiveEventSourceService.setFull(true);
               // terminateImmediately();
            }
            else if (getQueuedEventCount()<10000) {
                primitiveEventSourceService.setFull(false);
                //Console.WriteLine(TAG + $"Events in Queue: "  + getQueuedEventCount());
            }
          

            AbstractEvent externalEvent = null;
            if (externalEventQueue.Data.TryDequeue(out externalEvent))
            {
                externalEvent.knownToNodes.Add(this.nodeName);
                var processingStart = stopwatch.ElapsedMilliseconds;
                processQueries(externalEvent);
                
                foreach (var queryProcessor in queryProcessors)
                {
                    if (queryProcessor.inputEventIsTransitionEventType(externalEvent))
                    {
                        benchmarkMeter.registerProcessedEvent(externalEvent, processingStart, stopwatch.ElapsedMilliseconds);
                        break;
                    }
                }
                forwardRuleProcessor.processEvent(externalEvent, this.nodeName); // steven
            }

            AbstractEvent internalEvent = null;
            if (internalEventQueue.Data.TryDequeue(out internalEvent))
            {
                if(internalEvent.knownToNodes.Count==0) internalEvent.knownToNodes.Add(this.nodeName); // Samira : now internal primtive events have two identical entries, however complex events did not get a first entry before   
               
                var processingStart = stopwatch.ElapsedMilliseconds;
                if (queryProcessors.Count != 0) 
                {
                    processQueries(internalEvent);
                    
                    foreach (var queryProcessor in queryProcessors)
                    {
                        if (queryProcessor.inputEventIsTransitionEventType(internalEvent))
                        {
                            benchmarkMeter.registerProcessedEvent(internalEvent, processingStart, stopwatch.ElapsedMilliseconds);
                            break;
                        }
                    }
                }
         
                forwardRuleProcessor.processEvent(internalEvent, this.nodeName);
            }

            benchmarkMeter.tick(stopwatch.ElapsedMilliseconds);
            updateRemainingTimePrinter(stopwatch.ElapsedMilliseconds);
        }

        private void processQueries(AbstractEvent inputEvent)
        {
	     	 
            DateTime t = inputEvent.getOldest(); // Samira  [getOldest is defined as generation time for prim, oldest timestamp of contained prim for complex events]
            var processingStart = stopwatch.ElapsedMilliseconds; // new
            int stupidCount = 0;

            if (TimestampsDict.TryGetValue(inputEvent.knownToNodes[0], out DateTime value)) // Samira [if t is older than the oldest timestamp received from the same node (inputEvent.knownToNodes[0])
            {if (t > value) TimestampsDict.AddOrUpdate(inputEvent.knownToNodes[0], t, (key, oldValue) => t); }
            else // Samira: If not initialized, set to t
            {
                TimestampsDict.AddOrUpdate(inputEvent.knownToNodes[0], t, (key, oldValue) => t);
            }

            
            t = TimestampsDict.Values.Min(); // Samira [get current oldest value and use it for removing activations in between]
            if (t > oldestTimestamp) {oldestTimestamp = t; // Samira [oldest timestamp updated -> trigger activation deletion]

            foreach (var queryProcessor in queryProcessors) 
            {
                queryProcessor.removeActivations(oldestTimestamp);
            }}


            foreach (var queryProcessor in queryProcessors)
            {
                foreach (var outputEvent in queryProcessor.processInputEvent(inputEvent, oldestTimestamp))
                {   
                    proxyProvider.getProxy(nodeName).RegisterComplexEventMatchFork(outputEvent, false); // Samira [isDropped is always false, as dropping events now happens during processing]
                }
            }
        }

        public async Task RegisterPrimitiveEventInputAsync(PrimitiveEvent e) {
            
            locallyGeneratedPrimitiveEventCount++;
            internalEventQueue.Data.Enqueue(e);
        }

        public async Task RegisterComplexEventMatchAsync(ComplexEvent e, bool isDropped)
        {
            TimeSpan delay = DateTime.Now - e.getNewestAlt(); // Samira [getNewestAlt reflects actual time event was created as opposed to artificial time stamp caused by dataset based input generation]
            
            Console.WriteLine(TAG + "Complex;" + e.type + ";" +  delay);

            benchmarkMeter.registerComplexMatchBeforeDropout(e);
            if (!isDropped)
            {
                locallyGeneratedComplexEventCount++;
                internalEventQueue.Data.Enqueue(e);
                benchmarkMeter.registerComplexMatchAfterDropout(e);
            }
            else
            {
                locallyDroppedComplexEvents++;
            }
        }

        public void  terminateImmediately(){
            
            // ProcessingRemainder
            state = NodeExecutionState.DoSendExperimentDataAndTerminate;
            if (directorNodeService != null){
                directorNodeService.terminateAllNodesImmediately();
            }
        }
        public void updateRemainingTimePrinter(long passedMilliseconds)
        {
            if (_remainingTimeLastPrintTime == 0)
            {
                _remainingTimeLastPrintTime = passedMilliseconds;
                return;
            }
            
            // after 60 seconds, every 60 seconds: 
            if (passedMilliseconds - _remainingTimeLastPrintTime > 60000)
            {
                var totalEvents = locallyGeneratedComplexEventCount +
                                  receivedEventCount +
                                  locallyGeneratedPrimitiveEventCount;

                var throughput = totalEvents - _remainingTimeLastProcessedCount;
                if (throughput == 0) return;
                
                double interval = (passedMilliseconds - _remainingTimeLastPrintTime);
                double queueCount = getQueuedEventCount();
                double estimatedMs  = interval * (queueCount / throughput);
                long estimatedMinutes = (long) (estimatedMs / 60000);
       
                 
                
                _remainingTimeLastPrintTime = passedMilliseconds;
                _remainingTimeLastProcessedCount = totalEvents;
                Console.WriteLine(TAG + $"Estimated time for processing queued events: {estimatedMinutes} minutes ({queueCount} events in queue) ");
                
            }
        }
    }
}
