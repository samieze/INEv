using System.Runtime.Serialization;

namespace DCEP.Core.DCEPControlMessage
{
    [DataContract]
    public class NodeIsReadyToTerminateMessage : NodeInfoForCoordinatorMessage
    {
        public NodeIsReadyToTerminateMessage(NodeName sendingNode) : base(sendingNode)
        {
        }
    }
}