using System.Runtime.Serialization;

namespace DCEP.Core.QueryProcessing.Constraints
{
    [DataContract]
    public class EventTypeConstraint : SingleEventConstraint
    {
        [DataMember]
        EventType requiredType;

        public EventTypeConstraint(EventType requiredType)
        {
            this.requiredType = requiredType;
        }

        public override bool check(AbstractEvent e)
        {
            return e.type.Equals(requiredType);
        }
    }
}