using System;
using System.Collections.Generic;
using System.Threading;
using DCEP.AmbrosiaNodeAPI;
using DCEP.Core;
using DCEP.Node;

namespace DCEP.Test
{
    public class TestEnvorioment : INodeProxyProvider
    {
        public Dictionary<NodeName, DCEPNode> nodedict;
        private Dictionary<NodeName, IAmbrosiaNodeProxy> proxydict;

        public TestEnvorioment(string[] inputlines, DCEPSettings settings)
        {
            this.nodedict = new Dictionary<NodeName, DCEPNode>();
            this.proxydict = new Dictionary<NodeName, IAmbrosiaNodeProxy>();

            ExecutionPlan executionPlan = new ExecutionPlan(inputlines);

            Console.WriteLine(executionPlan.generateHumanReadableString());

            foreach (var item in executionPlan.networkPlan)
            {

                DCEPNode node = new DCEPNode(item.Key, inputlines, settings);
                nodedict.Add(item.Key, node);
                proxydict.Add(item.Key, new SimulatedAmbrosiaSelfProxy(node));                
            }

            foreach (var item in nodedict)
            {
                item.Value.onFirstStart((INodeProxyProvider)this);
                new Thread(item.Value.threadStartMethod).Start();
            }

            Console.WriteLine("[TestEnvironment] Running.");

        }

        public DCEPNode getNode(NodeName name){
            return nodedict[name];
        }

        public void terminateAll(){
            foreach (var item in nodedict)
            {
                (item.Value as DCEPNode).terminateImmediately();
            }
        }

        public IAmbrosiaNodeProxy getProxy(NodeName nodeName)
        {
            return proxydict[nodeName];
        }
    }
}