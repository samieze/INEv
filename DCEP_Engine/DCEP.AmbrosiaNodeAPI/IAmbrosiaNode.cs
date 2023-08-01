using System.Runtime.Serialization;
using Ambrosia;
using DCEP;
using DCEP.Core;
using DCEP.Core.DCEPControlMessage;

namespace DCEP.AmbrosiaNodeAPI
{
    public interface IAmbrosiaNode
    {
        int ReceiveExternalEvent(AbstractEvent eventname);

        int ReceiveDCEPControlMessage(DCEPControlMessage controlMessage);

        [ImpulseHandler]
        void RegisterPrimitiveEventInput(PrimitiveEvent e);

        [ImpulseHandler]
        void RegisterComplexEventMatch(ComplexEvent e, bool isDropped);
    }
}
