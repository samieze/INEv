using System.Runtime.Serialization;

namespace DCEP.Core.QueryProcessing.Constraints
{
    [DataContract]
    [KnownType(typeof(SingleEventConstraint))]
    [KnownType(typeof(PrimitiveBufferComponentAnyMatchConstraint))]
    public abstract class AbstractConstraint
    {

    }
}