using System;
using System.Collections.Generic;
using System.Runtime.Serialization;
using DCEP;
using DCEP.Core.Utils.DeepCloneExtension;


namespace DCEP.Core
{
    [DataContract]
    public class ForwardRule
    {
        [DataMember]
        public HashSet<NodeName> destinations { get; set; }
        
        [DataMember]
        public Dictionary<EventType, NodeName> constraints { get; set; }

        [DataMember]
        public double dropProbability = 0.0; 
        
        [DataMember]
        public List<EventType> componentsToSend = new List<EventType>();

        [DataMember] 
        private Random randomNumberGenerator = new Random();
        
        [DataMember]
        public NodeName lastSenderNodeName;

        public ForwardRule()
        {
            this.constraints = new Dictionary<EventType, NodeName>();
            this.destinations = new HashSet<NodeName>();
        }

        public void addTarget(NodeName n)
        {
            destinations.Add(n);
        }
        
        public bool isSatisfiedBy(AbstractEvent e)
        {
            HashSet<EventType> seenEventTypes = new HashSet<EventType>();

            if (!e.lastSenderNodeName.Equals(lastSenderNodeName))
                return false;
            
            foreach(var component in e.getAllEventComponents())
            {
                if(constraints.ContainsKey(component.type))
                {
                    seenEventTypes.Add(component.type);
                    
                    if(!component.nodeName.Equals(constraints[component.type]))
                        return false;
                }

            }
            
            //every constraint is satisfied (or not)
            return seenEventTypes.Count == constraints.Count && !shouldDropEvent();
            
        }
        
        public ForwardRule DeepCopy()
        {
            ForwardRule copy = new ForwardRule();
            
            copy.destinations = new HashSet<NodeName>(this.destinations);
            copy.constraints = new Dictionary<EventType, NodeName>(this.constraints);
            copy.dropProbability = this.dropProbability;
            foreach(var componentToSend in this.componentsToSend)
            {
                copy.componentsToSend.Add(new EventType(componentToSend.ToString()));
            }
            return copy;
        }
        
        //if an event does not match selecitvity-wise, then drop it
        private bool shouldDropEvent()
        {
            var doDropIt = randomNumberGenerator.NextDouble() < dropProbability;
            if (doDropIt)
            {
                Console.WriteLine("Event is dropped due to selectivity.");
                return true;
            }
            return false;
        }
    }
}
