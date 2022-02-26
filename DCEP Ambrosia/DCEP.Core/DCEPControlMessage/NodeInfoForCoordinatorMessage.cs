using System.Runtime.Serialization;
namespace DCEP.Core.DCEPControlMessage
{
    [DataContract]
    [KnownType(typeof(NodeIsReadyToStartMessage))]
    [KnownType(typeof(NodeIsReadyToTerminateMessage))]
    [KnownType(typeof(ExperimentRunNodeDataMessage))]
    public abstract class NodeInfoForCoordinatorMessage : DCEPControlMessage
    {
        public NodeInfoForCoordinatorMessage(NodeName sendingNode) : base(sendingNode)
        {
        }
    }
}