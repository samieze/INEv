using System.Runtime.Serialization;
using DCEP;

namespace DCEP.Core
{
    [DataContract]
    public class NodeParams
    {

        [DataMember]
        NodeName name { get; set; }

        [DataMember]
        public EventType[] primitiveEventNames { get; set; }

        [DataMember]
        public int[] primitiveEventRates { get; set; }

        public NodeParams(NodeName name, EventType[] primitiveEventNames, int[] primitiveEventRates)
        {
            this.name = name;
            this.primitiveEventNames = primitiveEventNames;
            this.primitiveEventRates = primitiveEventRates;
        }
    }
}
