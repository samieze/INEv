using System.Runtime.Serialization;

namespace DCEP.Core.DCEPControlMessage
{
    [DataContract]
    public class ExperimentRunNodeDataMessage : NodeInfoForCoordinatorMessage
    {
        [DataMember] public ExperimentRunData nodeData;

        public ExperimentRunNodeDataMessage(NodeName sendingNode, ExperimentRunData nodeData) : base(sendingNode)
        {
            this.nodeData = nodeData;
        }
    }
}