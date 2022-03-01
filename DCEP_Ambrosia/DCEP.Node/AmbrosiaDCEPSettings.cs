using System.Runtime.Serialization;
using CommandLine;
using DCEP.Node;

namespace DCEP.Node
{
    [DataContract]
    public class AmbrosiaDCEPSettings : DCEPSettings
    {
        [Option("receivePort",Required=true)]
        public int receivePort {get; set;}

        [Option("sendPort", Required = true)]
        public int sendPort { get; set; }

        [Option("serviceName", Required = true)]
        public string serviceName {get; set;}

    }
}