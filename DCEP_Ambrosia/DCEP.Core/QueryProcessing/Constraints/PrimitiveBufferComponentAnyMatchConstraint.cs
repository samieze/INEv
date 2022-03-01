using System.Runtime.CompilerServices;
using System.Linq;
using System.Collections.Immutable;
using System.Collections.Generic;
using System.Runtime.Serialization;

namespace DCEP.Core.QueryProcessing.Constraints
{
    [DataContract]
    [KnownType(typeof(EqualIDWhenEqualEventTypeConstraint))]
    [KnownType(typeof(SequenceConstraint))]
    public abstract class PrimitiveBufferComponentAnyMatchConstraint : AbstractConstraint
    {
        public abstract bool check(AbstractEvent primitiveCandidateComponent, AbstractEvent primitiveBufferedComponent);

        /// marks a PrimitiveBufferComponentConstraint as satisfied as soon as the first component pair is found (reverse loop in buffer) where the constraint returns true
        public static bool checkAll(IEnumerable<PrimitiveBufferComponentAnyMatchConstraint> constraints, AbstractEvent candidate, IEnumerable<AbstractEvent> activationBuffer)
        {
            var unsatisfiedConstraints = new List<PrimitiveBufferComponentAnyMatchConstraint>(constraints);

            foreach (var bufferedEvent in activationBuffer)
            {
                foreach (var primitiveBufferComponent in bufferedEvent.getAllPrimitiveEventComponents())
                {
                    foreach (var primitiveCandidateComponent in candidate.getAllPrimitiveEventComponents())
                    {
                        // reverse loop through constraints to remove the ones that are satisfied in the loop
                        for (int constraintIndex = unsatisfiedConstraints.Count - 1; constraintIndex >= 0; constraintIndex--)
                        {
                            var constraint = unsatisfiedConstraints[constraintIndex];
                            var nowsatisfied = constraint.check(primitiveCandidateComponent, primitiveBufferComponent);

                            if (nowsatisfied)
                            {
                                unsatisfiedConstraints.RemoveAt(constraintIndex);
                                if (unsatisfiedConstraints.Count == 0)
                                {
                                    return true;
                                }
                            }
                        }
                    }
                }
            }

            return unsatisfiedConstraints.Count == 0;
        }
    }
}