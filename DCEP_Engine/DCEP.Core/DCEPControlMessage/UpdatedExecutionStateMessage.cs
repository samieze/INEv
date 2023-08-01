using System.Runtime.Serialization;

namespace DCEP.Core.DCEPControlMessage
{
    [DataContract]
    public class UpdatedExecutionStateMessage : DCEPControlMessage
    {
        [DataMember]
        public NodeExecutionState newState;

        public UpdatedExecutionStateMessage(NodeName sendingNode, NodeExecutionState newState) : base(sendingNode)
        {
            this.newState = newState;
        }
    }
}