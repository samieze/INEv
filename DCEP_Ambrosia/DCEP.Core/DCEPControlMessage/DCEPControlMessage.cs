using System.Runtime.Serialization;

namespace DCEP.Core.DCEPControlMessage
{
    [DataContract]
    [KnownType(typeof(NodeInfoForCoordinatorMessage))]
    [KnownType(typeof(UpdatedExecutionStateMessage))]
    public abstract class DCEPControlMessage
    {
        [DataMember]
        public NodeName sendingNode;

        protected DCEPControlMessage(NodeName sendingNode)
        {
            this.sendingNode = sendingNode;
        }
    }
}