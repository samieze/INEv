using System;
using System.Collections.Generic;
using System.Runtime.Serialization;

namespace DCEP.Core.QueryProcessing.Constraints
{
    [DataContract]
    public class WithinTimeWindowConstraint : PrimitiveBufferComponentAllMatchConstraint
    {

        TimeSpan maxDiff;

        public WithinTimeWindowConstraint(TimeSpan maxDiff)
        {
            this.maxDiff = maxDiff;
        }

        public override bool check(AbstractEvent primitiveCandidateComponent, AbstractEvent primitiveBufferedComponent)
        {
            return (primitiveBufferedComponent.timeCreated - primitiveCandidateComponent.timeCreated).Duration() <= maxDiff;
        }
    }
}