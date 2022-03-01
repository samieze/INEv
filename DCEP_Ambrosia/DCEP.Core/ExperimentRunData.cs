using System.Runtime.Serialization;

namespace DCEP.Core
{
    [DataContract]
    public class ExperimentRunData
    {
        [DataMember] public long locallyGeneratedComplexEventCount {get; set; }
        [DataMember] public long receivedEventCount { get; set; }
        [DataMember] public long locallyGeneratedPrimitiveEventCount { get; set; }
        
        [DataMember] public long locallyDroppedComplexEvents { get; set; }

        [DataMember] public long locallyDroppedPartialMatches { get; set; }

        public ExperimentRunData(long locallyGeneratedComplexEventCount, long receivedEventCount, long locallyGeneratedPrimitiveEventCount, long locallyDroppedComplexEvents, long locallyDroppedPartialMatches)
        {
            this.locallyGeneratedComplexEventCount = locallyGeneratedComplexEventCount;
            this.receivedEventCount = receivedEventCount;
            this.locallyGeneratedPrimitiveEventCount = locallyGeneratedPrimitiveEventCount;
            this.locallyDroppedComplexEvents = locallyDroppedComplexEvents;
            this.locallyDroppedPartialMatches = locallyDroppedPartialMatches;
        }


    }


}