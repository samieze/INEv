using System;
using System.Collections.Generic;
using System.Linq;
using System.Runtime.Serialization;
using CommandLine;
using CommandLine.Text;
using DCEP.Core;
using DCEP.Node.Benchmarking;

namespace DCEP.Node
{
    [DataContract]
    [KnownType(typeof(AmbrosiaDCEPSettings))]
    public class DCEPSettings
    {
        [Value(0, HelpText = "The path to an execution plan text file.")]
        public string InputFilePath { get; set; }

        [Option('t', "timeunit", Required = true, HelpText = "The time unit events will be generated at rate (n events / time unit).")]
        public TimeUnit timeUnit { get; set; }

        [Option('w', "timeWindow", Required = true, HelpText = "The global time window in which event components must occur to trigger a match. The time unit is specified with -t.")]
        public double timeWindow { get; set; }

        [Option('d', "duration", Required = false, Default = 0, HelpText = "The execution duration of the simulation. Per default it wil run indefinitely. If set to a value, the number of exchanged events within the time period will be measured and eventually printed to stdout. The time unit is specified with -t.")]
        public double duration { get; set; }

        [Option("doBenchmarkTo", Required = false, HelpText = "Set to 'CSV' to write performance metrics into the /out/benchmarks directory.")]
        public IEnumerable<BenchmarkReporterName> benchmarkReporterNames { get; set; }

        [Option("benchmarkInterval", Default = 10, HelpText = "The time window of benchmark metrics in seconds. They are continuously written to a file in out/benchmark/.")]
        public long benchmarkIntervalInSeconds { get; set; }

        [Option(HelpText = "Can be used as a custom identifier for benchmark file names in  /out/benchmark/.")]
        public string experimentName
        {
            get
            {
                return _experimentName;
            }
            set
            {
                _experimentName = experimentName;
            }
        }
        private string _experimentName = System.Guid.NewGuid().ToString().Substring(0, 8);


        protected NodeName _directorNodeName = null;
        
        [Option("datasetSpeedup", Required = false, Default = 1.0, HelpText = "A scalar by which a dataset will be sped up with. (1/scalar) will be multiplied with every timestamp.")]
        public double datasetSpeedup { get; set; }


        [Option("directorNodeName", HelpText="The name of the node that is responsible for starting and stopping all nodes when a duration is specified." )]
        public NodeName directorNodeName
        {
            get
            {
                if (_directorNodeName == null){
                    _directorNodeName = new NodeName("0");
                }
                //Console.WriteLine("Returning settings directorNodeName " + _directorNodeName);
                return _directorNodeName;
            }
            set
            {
                _directorNodeName = directorNodeName;
            }
        }
        
        //[Option(Default = "h:mm:ss",HelpText = "The dateformat string used for parsing timestamps in datasets. See https://docs.microsoft.com/de-de/dotnet/standard/base-types/standard-date-and-time-format-strings for reference.")]
        //public string datasetDateFormatString { get; set; }

        // [Option('e', "eventnamesequence", Required = false, Default = "ABCDEFGHIJKLMNOPQRSTUVWXYZ", HelpText = "Event name characters will be used sequentially from this string.")]
        // public string EventNameSequence { get; set; }
    }

    public static class CommandLineExtensions{
        public static ParserResult<T> ThrowOnParseError<T>(this ParserResult<T> result)
        {
            if (!(result is NotParsed<T>))
            {
                // Case with no errors needs to be detected explicitly, otherwise the .Select line will throw an InvalidCastException
                return result;
            }

            var builder = SentenceBuilder.Create();
            var errorMessages = HelpText.RenderParsingErrorsTextAsLines(result, builder.FormatError, builder.FormatMutuallyExclusiveSetErrors, 1);

            var excList = errorMessages.Select(msg => new ArgumentException(msg)).ToList();

            if (excList.Any())
            {
                throw new AggregateException(excList);
            }

            return result;
        }
    }

}

