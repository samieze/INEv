using System.Runtime.Serialization;
using System.Threading.Tasks;
using DCEP.AmbrosiaNodeAPI;
using DCEP.Core;
using DCEP.Core.DCEPControlMessage;

namespace DCEP.Node
{
    public class SimulatedAmbrosiaSelfProxy : IAmbrosiaNodeProxy
    {
        private readonly DCEPNode node;

        public SimulatedAmbrosiaSelfProxy(DCEPNode node)
        {
            this.node = node;
        }

        public Task<int> ReceiveExternalEventAsync(AbstractEvent p_0) => node.ReceiveExternalEventAsync(p_0);

        public void ReceiveExternalEventFork(AbstractEvent p_0) => node.ReceiveExternalEventAsync(p_0).Wait();

        public Task RegisterComplexEventMatchAsync(ComplexEvent p_0, bool p_1) => node.RegisterComplexEventMatchAsync(p_0, p_1);
        public void RegisterComplexEventMatchFork(ComplexEvent p_0, bool p_1) => node.RegisterComplexEventMatchAsync(p_0, p_1).Wait();

        public Task RegisterPrimitiveEventInputAsync(PrimitiveEvent p_0) => node.RegisterPrimitiveEventInputAsync(p_0);
        public void RegisterPrimitiveEventInputFork(PrimitiveEvent p_0) => node.RegisterPrimitiveEventInputAsync(p_0).Wait();

        public Task<int> ReceiveDCEPControlMessageAsync(DCEPControlMessage p_0) => node.ReceiveDCEPControlMessageAsync(p_0);

        public void ReceiveDCEPControlMessageFork(DCEPControlMessage p_0) => node.ReceiveDCEPControlMessageAsync(p_0).Wait();
    }
}