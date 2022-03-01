using System;
using System.Globalization;
using System.IO;
using System.Runtime.Serialization;
using CsvHelper;
using CsvHelper.Configuration;
using CsvHelper.TypeConversion;
using DCEP.Core;

namespace DCEP.Node.Benchmarking
{

    public class FixedPointTypeConverter : DefaultTypeConverter
    {
        public override string ConvertToString(object value, IWriterRow row, MemberMapData memberMapData)
        {
            return ((double)value).ToString("F2", CultureInfo.InvariantCulture);
        }
    }

    public sealed class CSVBenchmarkReportMap : ClassMap<BenchmarkRecord>
    {
        public CSVBenchmarkReportMap()
        {
            Map(m => m.processedInputEvents).Index(0);
            Map(m => m.eventTimeLatency).TypeConverter<FixedPointTypeConverter>().Index(1);
            Map(m => m.processingTimeLatency).TypeConverter<FixedPointTypeConverter>().Index(2);
            Map(m => m.complexMatchesBeforeDropout).TypeConverter<FixedPointTypeConverter>().Index(3);
            Map(m => m.complexMatchesAfterDropout).TypeConverter<FixedPointTypeConverter>().Index(4);
        }
    }

    [DataContract]
    internal class CSVBenchmarkReporter : BenchmarkReporter
    {
        [DataMember]
        private DCEPSettings settings;

        [DataMember]
        private NodeName nodeName;

        [DataMember]
        string filepath;

        [DataMember]
        bool file_initialized = false;

        [DataMember]
        string directory = "benchmark\\";

        public CSVBenchmarkReporter(DCEPSettings settings, NodeName nodeName)
        {
            this.settings = settings;
            filepath = Path.Combine(directory, Path.GetFileName(settings.experimentName + "-" + nodeName + ".csv"));

            this.nodeName = nodeName;
        }

        public override void report(BenchmarkRecord record)
        {
            try
            {            
                Directory.CreateDirectory(directory);
                
                if (!file_initialized)
                {
                    using (var writer = new StreamWriter(filepath))
                    using (var csv = new CsvWriter(writer, CultureInfo.InvariantCulture))
                    {
                        csv.Configuration.RegisterClassMap<CSVBenchmarkReportMap>();
                        csv.WriteHeader<BenchmarkRecord>();
                    }
                    file_initialized = true;
                }

                using (var writer = new StreamWriter(filepath, append: true))
                using (var csv = new CsvWriter(writer, CultureInfo.InvariantCulture))
                {
                    csv.Configuration.RegisterClassMap<CSVBenchmarkReportMap>();
                    csv.NextRecord();
                    csv.WriteRecord(record);
                }
            }
            catch (IOException ioEx)
            {
                HandleIOException(ioEx);
            }

        }

        private void HandleIOException(IOException ioEx)
        {
            System.Console.WriteLine("Error: Could not write to '" + filepath + "'. Discarded a benchmark record.");
        }
    }
}