using System.Net.Sockets;
using System.Runtime.CompilerServices;
using System.Threading;
using System.Collections.Generic;
using System;
using CommandLine;
using System.IO;
using System.Text;
using System.Linq;
using DCEP.Core.Utils.DeepCloneExtension;
using System.Diagnostics;
using DCEP.Core;
using DCEP.AmbrosiaNodeAPI;
using System.Threading.Tasks;
using DCEP.Node;

namespace DCEP.Simulation
{
    public class SimulationEnvironment : INodeProxyProvider
    {
        Dictionary<NodeName, DCEPNode> nodedict;
        private Dictionary<NodeName, IAmbrosiaNodeProxy> proxydict;

        public SimulationEnvironment(string[] inputlines, DCEPSettings settings)
        {
            this.nodedict = new Dictionary<NodeName, DCEPNode>();
            this.proxydict = new Dictionary<NodeName, IAmbrosiaNodeProxy>();

            ExecutionPlan executionPlan = new ExecutionPlan(inputlines);

            Console.WriteLine(executionPlan.generateHumanReadableString());

            foreach (var item in executionPlan.networkPlan)
            {

                DCEPNode node = new DCEPNode(item.Key, inputlines, settings);
                nodedict.Add(item.Key, node);
                proxydict.Add(item.Key, new SimulatedAmbrosiaSelfProxy(node));
            }

            foreach (var item in nodedict)
            {
                item.Value.onFirstStart((INodeProxyProvider)this);
                new Thread(item.Value.threadStartMethod).Start();
            }


            if (settings.duration == 0)
            {
                Console.WriteLine("[SimulationEnvironment] Running indefinitly. Press enter to terminate all nodes immediately.");
                Console.ReadLine();
                (nodedict[settings.directorNodeName] as DCEPNode).terminateImmediately();

            }
        }

        public IAmbrosiaNodeProxy getProxy(NodeName nodeName)
        {
            return proxydict[nodeName];
        }

        static void Main(string[] args)
        {
            Parser.Default.ParseArguments<DCEPSettings>(args)
                    .WithParsed<DCEPSettings>(o =>
                    {
                        Console.WriteLine("Reading input from " + o.InputFilePath);
                        string[] lines = File.ReadAllLines(o.InputFilePath, Encoding.UTF8);
                        SimulationEnvironment env = new SimulationEnvironment(lines, o);
                    });
        }
    }



}
