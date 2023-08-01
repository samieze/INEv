using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;
using System.Runtime.Serialization;
using DCEP.Core;

namespace DCEP.Node.Benchmarking
{

    [DataContract]
    public class BenchmarkMeter
    {
        public BenchmarkMeter(DCEPSettings settings, NodeName nodeName)
        {
            this.reportIntervalInMilliseconds = settings.benchmarkIntervalInSeconds * 1000;
            this.reporters = BenchmarkReporter.createInstances(settings.benchmarkReporterNames, settings, nodeName);
        }

        [DataMember]
        private bool isRunning = false;

        [DataMember]
        private readonly long reportIntervalInMilliseconds;

        [DataMember]
        private long lastBenchmarkReport = 0;

        [DataMember]
        BenchmarkRecord currentRecord = new BenchmarkRecord(); 

        IEnumerable<BenchmarkReporter> reporters;

        public void registerProcessedEvent(AbstractEvent e, long processingStart, long elapsedMilliseconds)
        {
            currentRecord.eventTimeLatency += (DateTime.UtcNow - e.timeCreated).TotalSeconds;
            currentRecord.processingTimeLatency += (elapsedMilliseconds - processingStart) * 0.001;
            currentRecord.processedInputEvents += 1;
            
        }

        public void tick(long elapsedMilliseconds)
        {
            // make sure the first benchmark record is not created immediately but after the reportInterval
            if (lastBenchmarkReport == 0)
            {
                lastBenchmarkReport = elapsedMilliseconds;
                return;
            }

            if (elapsedMilliseconds - lastBenchmarkReport > reportIntervalInMilliseconds)
            {
                var outputRecord = currentRecord;
                currentRecord = new BenchmarkRecord(); 

                lastBenchmarkReport = elapsedMilliseconds;

                foreach (var reporter in reporters)
                {
                    reporter.report(outputRecord);
                }

            }
        }

        public void registerComplexMatchBeforeDropout(ComplexEvent complexEvent)
        {
            currentRecord.complexMatchesBeforeDropout++;
            /*DateTime t = DateTime.Now;
            double latency = (t - complexEvent.getOldest()).TotalSeconds;
            // make tuple out of e and latency
            var complexTup =  Tuple.Create(complexEvent.type.name, latency);
            currentRecord.complexTuples.Add(complexTup); //?*/
        }

        public void registerComplexMatchAfterDropout(ComplexEvent complexEvent)
        {
            currentRecord.complexMatchesAfterDropout++;
            /*DateTime t = DateTime.Now;
            double latency = (t - complexEvent.getOldest()).TotalSeconds;
            // make tuple out of e and latency
            var complexTup =  Tuple.Create(complexEvent.type.name, latency);
            currentRecord.complexTuples.Add(complexTup); //?*/
        }
    }
}