using System;
using System.Collections;
using System.Collections.Generic;
using System.Linq;
using System.Runtime.Serialization;

namespace DCEP.Core
{
    [DataContract]
    public class ComplexEvent : AbstractEvent
    {
        [DataMember]
        public IEnumerable<AbstractEvent> children { get; private set; }


        public ComplexEvent(EventType name, IEnumerable<AbstractEvent> outputeventcomponents, NodeName nodeName)  : base(name, nodeName)
        {
            children = outputeventcomponents;
        }

        public override DateTime getOldest() // Samira
        {
           return children.Select(even => even.getOldest()).ToList().Min();
        }
        
        public override DateTime getNewestAlt() // Samira
        {
            return children.Select(even => even.getNewestAlt()).ToList().Max();
        }
    }
}
