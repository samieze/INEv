using DCEP.Core;
using System;
using System.Runtime.Serialization;

namespace DCEP.Core
{
    [DataContract]
    public class PrimitiveEvent : AbstractEvent
    {
        public PrimitiveEvent(EventType name, NodeName nodeName) : base(name, nodeName)
        {
        }
        public PrimitiveEvent(EventType name, DateTime t) : base(name,t) // Samira
        {
        }

        public PrimitiveEvent(string name, NodeName nodeName) : base(new EventType(name),nodeName)
        {

        }

        public override DateTime getOldest() // Samira
        {
            return timeCreated;
        }
        public override DateTime getNewestAlt() // Samira [used to determine latency in case timestamps are taken from input file and do not reflect actual time]
        {
            return actualTime;
        }

    }
}
