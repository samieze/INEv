using System.Collections.Generic;
using DCEP.AmbrosiaNodeAPI;
using DCEP.Core;

namespace DCEP.Node
{
    public interface ICommunicationRelay
    {
        void sendEvent(AbstractEvent e, NodeName target);

    }
}