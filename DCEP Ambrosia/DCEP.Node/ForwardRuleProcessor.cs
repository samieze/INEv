using System;
using System.Collections.Generic;
using System.Runtime.Serialization;
using DCEP.AmbrosiaNodeAPI;
using DCEP.Core;
using DCEP.Core.Utils.DeepCloneExtension;

namespace DCEP.Node
{
    [DataContract]
    public class ForwardRuleProcessor
    {
        [DataMember] private readonly string TAG;
        [DataMember] private Dictionary<EventType, List<ForwardRule>> forwardRules;
        [DataMember] private HashSet<(string, NodeName)> alreadySent;

        private INodeProxyProvider proxyProvider;

        public ForwardRuleProcessor(string TAG, Dictionary<EventType, List<ForwardRule>> forwardRules, INodeProxyProvider proxyProvider)
        {
            this.TAG = TAG + "[ForwardRuleProcessor] ";
            this.forwardRules = forwardRules;
            this.proxyProvider = proxyProvider;
            this.alreadySent = new HashSet<(string, NodeName)>(); 
        }

        private bool isComplexEvent(AbstractEvent e)
        {
            return e.type.ToString().Length > 1;
        }

        private bool filterWasUsed(AbstractEvent e, AbstractEvent eventToSend)
        {
            return (!e.type.Equals(eventToSend.type));
        }

        private bool isFilteredComplexEvent(AbstractEvent e)
        {
            return isComplexEvent(e) && !e.filteredBy.Equals("");
        }

        public void processEvent(AbstractEvent e, NodeName processingNode)
        {
            List<ForwardRule> forwardRules;
            
            if (isFilteredComplexEvent(e))
                return;
            
            //Console.WriteLine(this.TAG + "processEvent - event: " + e + " - last sender node: " + e.lastSenderNodeName);
            
            if (this.forwardRules.TryGetValue(e.type, out forwardRules))
            {
                foreach(var rule in forwardRules)
                {
                    if(rule.isSatisfiedBy(e))
                    {
                        //Console.WriteLine("rule is satisfied! :) by " + e);
                        foreach(var componentToSend in rule.componentsToSend)
                        {
                            AbstractEvent eventToSend = e.getSubProjection(componentToSend);

                            if(filterWasUsed(e, eventToSend))
                            {                                
                                eventToSend.setFilter(e.getAllPrimitiveEventTypesAsString());
                            }
                            
                            eventToSend.lastSenderNodeName = processingNode;
                            
                            foreach (var nodeName in rule.destinations)
                            {
                                //prevents the multiple sending of matches produced by a subprojection (i.e., filter) of a projection
                                if(!alreadySent.Contains((eventToSend.ID,nodeName)))
                                {
                                    Console.WriteLine(String.Format(TAG + "Sending {0} to Node {1}", eventToSend, nodeName));
                                    proxyProvider.getProxy(nodeName).ReceiveExternalEventFork(eventToSend.DeepClone());
                                    alreadySent.Add((eventToSend.ID,nodeName));
                                }
                            }
                        }
                    }
                    //else
                        //Console.WriteLine("rule is not satisfied! :( by " + e);
                }
            }
        }
    }
}
