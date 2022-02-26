using System.Collections.Generic;
using System.Runtime.Serialization;

namespace DCEP.Core.QueryProcessing.Constraints
{
    [DataContract]
    [KnownType(typeof(WithinTimeWindowConstraint))]
    public abstract class BufferConstraint : AbstractConstraint
    {
        public abstract bool check(AbstractEvent candidate, IEnumerable<AbstractEvent> eventBuffer);
    }
}