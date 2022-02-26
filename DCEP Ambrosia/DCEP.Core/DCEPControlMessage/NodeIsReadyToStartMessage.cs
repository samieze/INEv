using System.Runtime.Serialization;
namespace DCEP.Core.DCEPControlMessage
{
    [DataContract]
    public class NodeIsReadyToStartMessage : NodeInfoForCoordinatorMessage
    {
        public NodeIsReadyToStartMessage(NodeName sendingNode) : base(sendingNode)
        {
        }
    }
}