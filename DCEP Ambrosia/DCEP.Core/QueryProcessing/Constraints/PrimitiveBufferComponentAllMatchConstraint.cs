using System.Runtime.CompilerServices;
using System.Linq;
using System.Collections.Immutable;
using System.Collections.Generic;
using System.Runtime.Serialization;

namespace DCEP.Core.QueryProcessing.Constraints
{
    [DataContract]
    [KnownType(typeof(WithinTimeWindowConstraint))]
    public abstract class PrimitiveBufferComponentAllMatchConstraint : AbstractConstraint
    {
        public abstract bool check(AbstractEvent primitiveCandidateComponent, AbstractEvent primitiveBufferedComponent);

        /// marks a PrimitiveBufferComponentAllMatchConstraint as satisfied when the constraint returns true for all component pairs
        public static bool checkAll(IEnumerable<PrimitiveBufferComponentAllMatchConstraint> constraints, AbstractEvent candidate, IEnumerable<AbstractEvent> activationBuffer)
        {
            foreach (var bufferedEvent in activationBuffer)
            {
                foreach (var primitiveBufferComponent in bufferedEvent.getAllPrimitiveEventComponents())
                {
                    foreach (var primitiveCandidateComponent in candidate.getAllPrimitiveEventComponents())
                    {
                        foreach (var constraint in constraints)
                        {
                            if (!constraint.check(primitiveCandidateComponent, primitiveBufferComponent))
                            {
                                return false;
                            }
                        }
                    }
                }
            }
            return true;
        }
    }
}