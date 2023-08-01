using Ambrosia;
using System;
using System.Threading;

using DCEP.AmbrosiaNodeAPI;
using System.IO;
using System.Text;
using DCEP.Node;
using CommandLine;
using CommandLine.Text;
using System.Linq;

namespace DCEP.AmbrosiaNode
{
    class Program
    {
        
        static void Main(string[] args)
        {
            Parser.Default.ParseArguments<AmbrosiaDCEPSettings>(args)
        .WithParsed<AmbrosiaDCEPSettings>(settings =>
        {

            if (settings.directorNodeName == null)
            {
                throw new ArgumentException("directorNodeName must not be null");
            }
            // removing the prefix from the service name to only have numbers as node names in DCEP
            string dcepnodename = settings.serviceName;
            if (dcepnodename.Contains("adcep")){
                dcepnodename = dcepnodename.Substring("adcep".Length);
            }

            if (!dcepnodename.All(char.IsDigit) || dcepnodename.Length == 0)
            {
                throw new ArgumentException("The -serviceName must be numeric and can be prefixed with 'adcep'.");
            }


            Console.WriteLine("Reading input from " + settings.InputFilePath);
            string[] lines = File.ReadAllLines(settings.InputFilePath, Encoding.UTF8);

            AmbrosiaNode ambrosiaNode = new AmbrosiaNode(dcepnodename, lines, settings);
            
            using (AmbrosiaFactory.Deploy<IAmbrosiaNode>(settings.serviceName, ambrosiaNode, settings.receivePort, settings.sendPort))
            {
                Thread.Sleep(14 * 24 * 3600 * 1000);
            }
        });            
        }
    }
}