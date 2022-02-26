using System.Collections.Generic;
using System.Runtime.Serialization;
using DCEP.Core;

namespace DCEP.Core.QueryProcessing.Constraints
{
    [DataContract]
    public class EqualIDWhenEqualEventTypeConstraint : PrimitiveBufferComponentAnyMatchConstraint
    {
        [DataMember]
        private readonly EventType typeToCheck;

        public EqualIDWhenEqualEventTypeConstraint(EventType typeToCheck)
        {
            this.typeToCheck = typeToCheck;
        }

        public override bool check(AbstractEvent primitiveCandidateComponent, AbstractEvent primitiveBufferedComponent)
        {
            if (primitiveBufferedComponent.type.Equals(typeToCheck) && primitiveCandidateComponent.type.Equals(typeToCheck))
            {
                return primitiveCandidateComponent.ID.Equals(primitiveBufferedComponent.ID);
            }
            return false;
        }
    }
}