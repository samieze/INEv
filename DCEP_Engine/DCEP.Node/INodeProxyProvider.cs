using System.Collections.Generic;
using DCEP.AmbrosiaNodeAPI;
using DCEP.Core;

namespace DCEP.Node
{
    public interface INodeProxyProvider
    {
        IAmbrosiaNodeProxy getProxy(NodeName nodeName);
    }
}