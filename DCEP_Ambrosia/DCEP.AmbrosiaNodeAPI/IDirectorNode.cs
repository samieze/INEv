using DCEP.Core;

namespace DCEP.AmbrosiaNodeAPI
{
    public interface IDirectorNode
    {
        int ReceiveReadyToLaunchNotification(NodeName sendingNode);

        int ReceiveNodeIsReadyToTerminateNotification(NodeName sendingNode);

        int ReceiveExperimentRunData(ExperimentRunData data, NodeName sendingNode);
    }
}