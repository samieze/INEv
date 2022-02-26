using System.Runtime.Serialization;
using DCEP.Core;

namespace DCEP.Core.QueryProcessing.Constraints
{
    [DataContract]
    [KnownType(typeof(EventTypeConstraint))]
    public abstract class SingleEventConstraint : AbstractConstraint
    {
        public abstract bool check(AbstractEvent e);
    }
}