using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Globalization;
using System.IO;
using System.Linq;
using System.Runtime.Serialization;
using System.Threading;
using DCEP.Core;
using DCEP.Core.Utils;

namespace DCEP.Node
{
    [DataContract]
    public class DatasetPrimitiveEventInputService : PrimitiveEventSourceService
    {
        [DataMember] private string TAG { get; set; }
        [DataMember] private readonly string _filePath;
        [DataMember] private readonly DCEPSettings _settings;
        
        [DataMember] private bool _continueRunning;
        
        [DataMember] private Stopwatch _stopwatch;
        [DataMember] private TimeSpan _offset;
        [DataMember] private DateTime timestamp; //new
        [DataMember] private string _eventtype;
        [DataMember] private bool _candidateInQueue;
        [DataMember] public IEnumerable<EventType> _primitiveEventNames;
        [DataMember] private NodeName _nodeName;
        [DataMember] private bool _queueFull; 
        
        public DatasetPrimitiveEventInputService(INodeProxyProvider proxyProvider, string tag, string filePath,
            NodeName nodeName, DCEPSettings settings, NodeParams nodeparams) : base(proxyProvider, nodeName)
        {
            TAG = tag + "[DatasetPrimitiveEventInputService] ";
            var inputfilepath = new FileInfo(settings.InputFilePath).Directory.FullName;
            filePath = filePath.Replace("%NodeName%", nodeName.ToString());
            _filePath = Path.Combine(inputfilepath, Path.GetFileName(filePath));
            _settings = settings;
            var tuples = nodeparams.primitiveEventNames.Zip(nodeparams.primitiveEventRates, (e, r) => new {Name = e, Rate = r});
            _primitiveEventNames = tuples.Where(arg => arg.Rate > 0).Select(arg => arg.Name);
            _nodeName = nodeName;
        }

        public override void start()
        {
            _continueRunning = true;
            Thread t = new Thread(new ThreadStart(SeparateThreadMethod));
            t.Start();
        }


        private void SeparateThreadMethod()
        {
            _stopwatch = new Stopwatch();
            _stopwatch.Start();

            Console.WriteLine(TAG + "Starting to read dataset file "+_filePath);
            System.IO.StreamReader file =
                new System.IO.StreamReader(_filePath);

            _candidateInQueue = false;


            while (_continueRunning)
            {
                if (!_candidateInQueue)
                {
                    var line = file.ReadLine();

                    if (line == null)
                    {
                        Console.WriteLine(TAG + " Reached end of input file. Terminating primitive input service.");
                        return;
                    }
                    var timestampstring = line.Split(',')[0].Replace("\"", "");
                    
                    //_offset = TimeSpan.ParseExact(timestampstring, _settings.datasetDateFormatString,
                    //    CultureInfo.InvariantCulture, TimeSpanStyles.None);
                    _offset = new TimeSpan(int.Parse(timestampstring.Split(':')[0]),    // hours
                                           int.Parse(timestampstring.Split(':')[1]),    // minutes
                                           0);                                          // seconds
                    
                    //_offset = TimeSpan.Parse(timestampstring, CultureInfo.InvariantCulture);
                    timestamp = DateTime.MinValue.Add(_offset); //new
                    //Console.WriteLine("timestampstring"+timestampstring);
                    //_offset = _offset.Multiply(1.0/_settings.datasetSpeedup); 
                    _eventtype = line.Split(',')[1].Replace("\"", "");
                    _candidateInQueue = true;
                }

                if (!_queueFull)//(_offset < _stopwatch.Elapsed) // Samira [if not queue full]
                {
                    if (_primitiveEventNames.Select(type => type.name).Contains(_eventtype)) 
                    {
                        var primEvent = new PrimitiveEvent(new EventType(_eventtype),  timestamp);

                        primEvent.lastSenderNodeName = _nodeName;
                        primEvent.nodeName = _nodeName;
                        registerPrimitiveEvent(primEvent);
                    }
                    _candidateInQueue = false;
                }
                
            }
        }

        public override void stop()
        {
            _continueRunning = false;
        }
        public override void setFull(Boolean b)
        {
            _queueFull = b;
        }
    }
}
