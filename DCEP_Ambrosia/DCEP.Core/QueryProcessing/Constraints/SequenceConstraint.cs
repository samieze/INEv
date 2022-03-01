using System.Collections.Generic;
using System.Runtime.Serialization;

namespace DCEP.Core.QueryProcessing.Constraints
{
    public enum SequenceType { IsPredecessor, IsSuccessor }

    [DataContract]
    public class SequenceConstraint : PrimitiveBufferComponentAnyMatchConstraint
    {
        [DataMember]
        internal readonly EventType candidateType;
        [DataMember]
        internal readonly EventType bufferType;
        [DataMember]
        internal readonly SequenceType sequenceType;

        public SequenceConstraint(EventType candidateType, EventType bufferType, SequenceType sequenceType)
        {
            this.candidateType = candidateType;
            this.bufferType = bufferType;
            this.sequenceType = sequenceType;
        }

        public override bool check(AbstractEvent primitiveCandidateComponent, AbstractEvent primitiveBufferedComponent)
        {
            if (primitiveCandidateComponent.type.Equals(candidateType) && primitiveBufferedComponent.type.Equals(bufferType))
            {
                // types match, check required sequence Type
                switch (sequenceType)
                {
                    case SequenceType.IsPredecessor:
                        return primitiveCandidateComponent.timeCreated < primitiveBufferedComponent.timeCreated;

                    case SequenceType.IsSuccessor:
                        return primitiveCandidateComponent.timeCreated > primitiveBufferedComponent.timeCreated;
                }

            }
            return false;
        }
    }
}