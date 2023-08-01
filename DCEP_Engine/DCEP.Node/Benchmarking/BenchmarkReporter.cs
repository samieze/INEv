using System.Collections.Immutable;
using System.Linq;
using System;
using System.Collections.Generic;
using System.Runtime.Serialization;
using DCEP.Core;

namespace DCEP.Node.Benchmarking
{
    [DataContract]
    public abstract class BenchmarkReporter
    {
        public abstract void report(BenchmarkRecord record);

        internal static IEnumerable<BenchmarkReporter> createInstances(IEnumerable<BenchmarkReporterName> reporterNames, DCEPSettings settings, NodeName nodeName)
        {
            if (reporterNames == null)
            {
                return Enumerable.Empty<BenchmarkReporter>();
            }

            var uniquereporters = reporterNames.ToImmutableHashSet();

            var result = new List<BenchmarkReporter>();

            foreach (var name in uniquereporters)
            {
                switch (name)
                {
                    case BenchmarkReporterName.CSV:
                        result.Add(new CSVBenchmarkReporter(settings, nodeName));
                        break;
                    default:
                        continue;
                }
            }

            return result;

        }
    }
}