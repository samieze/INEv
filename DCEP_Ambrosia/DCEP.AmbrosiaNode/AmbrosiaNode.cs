using Ambrosia;
using System;
using DCEP;
using System.Runtime.Serialization;
using DCEP.AmbrosiaNodeAPI;
using System.Threading.Tasks;
using System.Threading;
using DCEP.Core;
using DCEP.Node;
using System.Collections.Generic;
using DCEP.Core.DCEPControlMessage;

namespace DCEP.AmbrosiaNode
{

    [DataContract]
    public class AmbrosiaNode : Immortal<IAmbrosiaNodeProxy>, IAmbrosiaNode, INodeProxyProvider
    {
        [DataMember] DCEPNode node;
        [DataMember] private string TAG {get; set;}
        [DataMember] string[] inputlines {get; set;}
        [DataMember] private string name { get; set; }
        [DataMember] private  AmbrosiaDCEPSettings settings { get; set; }

        public AmbrosiaNode(string name, string[] inputlines, AmbrosiaDCEPSettings settings)
        {
            this.settings = settings;
            this.name = name;
            this.inputlines = inputlines;

            TAG = "[" + name + "] ";
        }

        protected override void BecomingPrimary()
        {
            Console.WriteLine(TAG + " [AmbrosiaNode] BecomingPrimary called -> doing nothing");
        }

        protected override async Task<bool> OnFirstStart()
        {
            Console.WriteLine(TAG + " [AmbrosiaNode] OnFirstStart called ->  creating DCEPNode and starting DCEPNode thread.");

            this.node = new DCEPNode(new NodeName(name), inputlines, settings);
            node.onFirstStart((INodeProxyProvider)this);
        
            new Thread(node.threadStartMethod).Start();
            
            return true;
        }


        public Task<int> ReceiveExternalEventAsync(AbstractEvent p_0) => node.ReceiveExternalEventAsync(p_0);

        public void ReceiveExternalEventFork(AbstractEvent p_0) => node.ReceiveExternalEventAsync(p_0).Wait();

        public Task RegisterComplexEventMatchAsync(ComplexEvent p_0, bool p_1) => node.RegisterComplexEventMatchAsync(p_0, p_1);
        public void RegisterComplexEventMatchFork(ComplexEvent p_0, bool p_1) => node.RegisterComplexEventMatchAsync(p_0, p_1).Wait();

        public Task RegisterPrimitiveEventInputAsync(PrimitiveEvent p_0) => node.RegisterPrimitiveEventInputAsync(p_0);
        public void RegisterPrimitiveEventInputFork(PrimitiveEvent p_0) => node.RegisterPrimitiveEventInputAsync(p_0).Wait();

        public Task<int> ReceiveDCEPControlMessageAsync(DCEPControlMessage p_0) => node.ReceiveDCEPControlMessageAsync(p_0);

        public void ReceiveDCEPControlMessageFork(DCEPControlMessage p_0) => node.ReceiveDCEPControlMessageAsync(p_0).Wait();


        public IAmbrosiaNodeProxy getProxy(NodeName nodeName)
        {
            if (nodeName.ToString().Equals(name)){
                //Console.WriteLine(TAG + "getting thisProxy");
                return thisProxy;
            } else {
                //Console.WriteLine(TAG + "getting proxy for nodename "+nodeName);
                return GetProxy<IAmbrosiaNodeProxy>("adcep" + nodeName.ToString());
            }
        }
    }
}
