using System.Collections.Generic;
using System.Linq;
using System.Runtime.Serialization;
using System.Threading;
using DCEP.AmbrosiaNodeAPI;
using DCEP.Core;

namespace DCEP.Node
{
    [DataContract]
    public class RandomPrimitiveEventGenerationService : PrimitiveEventSourceService
    {
        [DataMember]
        private readonly List<PrimitiveEventGenerator> eventGenerators;
        [DataMember]
        private readonly NodeName nodeName;
        [DataMember]
        bool continueRunning;

        public RandomPrimitiveEventGenerationService(NodeName nodeName, NodeParams nodeparams, INodeProxyProvider proxyProvider, DCEPSettings settings) : base(proxyProvider, nodeName)
        {
            this.nodeName = nodeName;
            eventGenerators = new List<PrimitiveEventGenerator>();


            foreach (var e in nodeparams.primitiveEventNames.Zip(nodeparams.primitiveEventRates, (e, r) => new { Name = e, Rate = r }))
            {
                if (e.Rate > 0)
                {
                    eventGenerators.Add(new PrimitiveEventGenerator(e.Rate, settings.timeUnit, e.Name, nodeName));
                }
            }
        }

        private void separateThreadMethod()
        {
            while(continueRunning){
                foreach (PrimitiveEventGenerator generator in this.eventGenerators)
                {
                    var events = generator.generate();
                    foreach (var e in events)
                    {
                        registerPrimitiveEvent((e));
                    }
                }
            }
        }


        public override void start()
        {
            continueRunning = true;
            Thread t = new Thread(new ThreadStart(separateThreadMethod));
            t.Start();
        }

        public override void stop()
        {
            continueRunning = false;
        }

        public override void setFull(bool b)
        {
            
        }
    }


}
