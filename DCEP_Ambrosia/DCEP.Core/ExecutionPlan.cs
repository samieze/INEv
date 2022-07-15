using System.Diagnostics;
using System.Data;
using System;
using System.Collections.Generic;
using DCEP.Core.Utils;
using System.Linq;
using System.Runtime.Serialization;
using System.IO;

namespace DCEP.Core
{

    [DataContract]
    public class ExecutionPlan
    {
        [DataMember] public PrimitiveInputMode primitiveInputMode;
        
        [DataMember]
        public Dictionary<NodeName, NodeParams> networkPlan { get; set; }

        [DataMember]
        public Dictionary<NodeName, HashSet<Query>> queriesByNodeName { get; set; }

        [DataMember]
        public Dictionary<NodeName, Dictionary<EventType, List<ForwardRule>>> forwardRulesByNodeName { get; set; }

        [DataMember]
        internal Dictionary<EventType, HashSet<NodeName>> sourceNodesByEventName { get; set; }

        [DataMember]
        public Dictionary<string, double> singleSelectivities { get; set; }

        [DataMember]
        private HashSet<EventType> primitiveEventNames = null;

        [DataMember]
        private int numberOfNodes = -1;

        [DataMember] public string datasetFileNameTemplate { get; set; }

        public DictionaryWithDefault<Query, bool> wasQueryProcessed;


        [DataMember]
        private string EventNameSequence = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";

        private void parseSingleSelectivities(string line)
        {
            line = line.Trim('}');
            string[] selectivities = line.Split('{')[1].Split(',');
            
            foreach(string selectivity in selectivities)
            {
                string formattedString = selectivity.TrimAllWhitespace();
                string eventTypes = formattedString.Split(':')[0];
                string outputRate = formattedString.Split(':')[1];
                string eventProjectionKey = eventTypes.Substring(1, eventTypes.Length-2);

                double convertedOutputRate = 0.0;

                double.TryParse(outputRate, out convertedOutputRate);
                
                singleSelectivities[eventProjectionKey] = convertedOutputRate;
                
            }
        }


        public ExecutionPlan(string[] inputlines)
        {
            if (inputlines == null)
            {
                throw new ArgumentException("inputlines must not be null.");
            }

            this.wasQueryProcessed = new DictionaryWithDefault<Query, bool>(false);
            this.networkPlan = new Dictionary<NodeName, NodeParams>();

            this.sourceNodesByEventName = new Dictionary<EventType, HashSet<NodeName>>();
            this.forwardRulesByNodeName = new Dictionary<NodeName, Dictionary<EventType, List<ForwardRule>>>();
            this.queriesByNodeName = new Dictionary<NodeName, HashSet<Query>>();
            
            this.singleSelectivities = new Dictionary<string, double>();

            // parsing the which nodes there are and what primitive events they generate at what rates
            parseNetworkPlan(inputlines);
            
            // initialize members now that the nodeCount is known
            foreach (var nodeName in networkPlan.Keys)
            {
                forwardRulesByNodeName[nodeName] = new Dictionary<EventType, List<ForwardRule>>();
                queriesByNodeName[nodeName] = new HashSet<Query>();
            }

            var remaining = inputlines.Skip(numberOfNodes + 1).ToArray();

            var primitiveInputModeLine = remaining[0];

            if (primitiveInputModeLine.Trim().ToLower().Contains("randomized rate-based"))
            {
                primitiveInputMode = PrimitiveInputMode.RANDOM_WITH_RATES;

                if (!remaining[1].Trim().StartsWith("-"))
                {
                    throw new ArgumentException("dash separation line expected after randomized rate-based primitive event generation statement ");
                }
                
                remaining = remaining.Skip(2).ToArray();
            }
            else
            {
                primitiveInputMode = PrimitiveInputMode.DATASET;
                datasetFileNameTemplate = remaining[1].Trim();

                if (!remaining[2].Trim().StartsWith("-"))
                {
                    throw new ArgumentException("dash separation line expected after Dataset-Based Primitive Event Generation statement and a single next line with the dataset configuration");
                }
                
                remaining = remaining.Skip(3).ToArray();
            }
            
            if(remaining[0].StartsWith("Single Selectivities"))
            {
                parseSingleSelectivities(remaining[0]);
                if (!remaining[1].Trim().StartsWith("-"))
                {
                    throw new ArgumentException("dash separation line expected after Single Selectivities statement");
                }
                remaining = remaining.Skip(2).ToArray();
            }
            
            //new forward rules parse code 
            while(remaining.Count() > 0 && remaining[0].StartsWith("~~"))
            {
                remaining = remaining.Skip(1).ToArray();
                string[] nodeNames = remaining[0].Split(',');

                for(int i=0; i<nodeNames.Count(); ++i)
                {
                
                    nodeNames[i] = nodeNames[i].Trim().Substring(4);

                }

                remaining = remaining.Skip(2).ToArray();
                if (!remaining[0].Trim().StartsWith("Forward rules:"))
                {
                    throw new ArgumentException("forward rules expected after node assignment");
                }
                
                remaining = remaining.Skip(1).ToArray();
                
                List<ForwardRule> forwardRules = new List<ForwardRule>();
                
                while(remaining.Count() > 0 && !remaining[0].StartsWith("--"))
                {
                    if(remaining[0].Trim().Equals(""))
                    {
                        remaining = remaining.Skip(1).ToArray();
                        continue;
                    }
                    ForwardRule forwardRule = new ForwardRule();
                    
                    string typeString = remaining[0].Split("-")[0];
                    
                    bool isFiltering = typeString.Contains("|");
                    //A,B|SEQ(A,B,C)
                    string toSendEventTypes = isFiltering?typeString.Split("|")[0]:typeString;
                    string receivedEventType = isFiltering?typeString.Split("|")[1]:typeString;
                    List<string> toSendEventTypeList = new List<string>();
                    if(isFiltering)
                        toSendEventTypeList = toSendEventTypes.Trim().Split(',').ToList();
                    else
                    {
                        toSendEventTypeList.Add(toSendEventTypes);
                    }
                    foreach(var toSendEventType in toSendEventTypeList)
                    {
                        forwardRule.componentsToSend.Add(new EventType(toSendEventType));
                    }
                    EventType eventType = new EventType(receivedEventType);
                    
                    remaining[0] = remaining[0].Split("-")[1];
                    
                    
                    //parse all relevant ETB nodes
                    string eventTypeBindingsString = remaining[0].Split("ETB:")[1].Split("FROM:")[0];
                    
                    string[] eventTypeBindingList = eventTypeBindingsString.Split(";");

                    foreach(var eventTypeBinding in eventTypeBindingList)
                    {
                        if(eventTypeBinding.Trim().Equals(""))
                            continue;
                        
                        string cleanedEventTypeBinding = eventTypeBinding.Trim().Substring(1);
                        cleanedEventTypeBinding = cleanedEventTypeBinding.Substring(0,cleanedEventTypeBinding.Count()-1);
                        EventType type = new EventType(cleanedEventTypeBinding.Split(":")[0]);
                        string cleanedNodeName = cleanedEventTypeBinding.Split(":")[1].Trim();
                        
                        //ANY means, that an event type is not constrained
                        if(cleanedNodeName.Equals("ANY"))
                            continue;
                        NodeName node = new NodeName(cleanedNodeName.Substring(4));

                        //Add a ETB rule als constraint
                        forwardRule.constraints.Add(type,node);
                    }
                    
                    //parse possible sources
                    string possibleSourcesString = remaining[0].Split("FROM:")[1].Split("TO:")[0];
                    string cleanedPossibleSourcesString = possibleSourcesString.Replace("[","").Replace("]","");
                    string[] possibleSourcesList = cleanedPossibleSourcesString.Split(";");
                    
                    //parse possible destinations
                    remaining[0] = remaining[0].Split("TO:")[1];
                    string cleanedDestinations = remaining[0].Replace("[","").Replace("]","");
                    string[] destinationsList = cleanedDestinations.Split(";");
                    
                    foreach(var destination in destinationsList)
                    {
                        //add destinations to forward rule
                        forwardRule.destinations.Add(new NodeName(destination.Trim().Substring(4)));
                    }
                    
                    
                    
                    foreach(var source in possibleSourcesList)
                    {
                        ForwardRule copy = forwardRule.DeepCopy();                        
                        copy.lastSenderNodeName = new NodeName(source.ToString().Trim().Substring(4));
                        foreach(var node in nodeNames)
                        {
                            if(!forwardRulesByNodeName[new NodeName(node)].ContainsKey(eventType))
                                forwardRulesByNodeName[new NodeName(node)].Add(eventType, new List<ForwardRule>());
                            forwardRulesByNodeName[new NodeName(node)][eventType].Add(copy);
                        }
                    }
                    remaining = remaining.Skip(1).ToArray();
                }
                
                remaining = remaining.Skip(1).ToArray();
                if(!remaining[0].Trim().StartsWith("Projections to process:"))
                {
                    remaining = remaining.Skip(1).ToArray();
                    continue;
                }
                remaining = remaining.Skip(1).ToArray();
                
                // parsing what queries and compex events there are
                while(remaining.Count() > 0 && !remaining[0].Trim().StartsWith("~~"))
                {
                    if(remaining[0].Trim().Equals(""))
                    {
                        remaining = remaining.Skip(1).ToArray();
                        continue;
                    }
                    
                    Query q = Query.createFromString(remaining[0]);
                    
                    //register respective query for each defined node
                    foreach(var node in nodeNames)
                    {
                        RegisterQueryPlacementOnNode(q, new NodeName(node));
                    }
                    remaining = remaining.Skip(1).ToArray();
                }
            }
        }

        /// Parse network plan (which nodes generate which primitive events at what rate)
        private void parseNetworkPlan(string[] inputlines)
        {
            int nodeID = -1;
            numberOfNodes = -1;

            foreach (string line in inputlines)
            {
                if (line.StartsWith("-"))
                {
                    numberOfNodes = nodeID + 1;
                    // finished with parsing the network plan
                    return;
                }

                nodeID++;
                var currentNodeName = new NodeName(nodeID.ToString());

                //int[] rates = Array.ConvertAll(line.Trim().Split(' '), Int32.Parse);
                float[] rates = Array.ConvertAll(line.Trim().Split(' '), float.Parse);
                EventType[] eventNames = EventNameSequence.Substring(0, rates.Length).Select(c => new EventType(c.ToString())).ToArray();


                if (primitiveEventNames == null)
                {
                    primitiveEventNames = new HashSet<EventType>(eventNames);
                }

                NodeParams nodeParams = new NodeParams(currentNodeName, eventNames, rates);
                networkPlan[currentNodeName] = nodeParams;

                foreach (var e in eventNames.Zip(rates, (e, r) => new { Name = e, Rate = r }))
                {
                    if (e.Rate > 0)
                    {
                        if (!sourceNodesByEventName.ContainsKey(e.Name))
                        {
                            sourceNodesByEventName[e.Name] = new HashSet<NodeName>() { currentNodeName };
                        }
                        else
                        {
                            sourceNodesByEventName[e.Name].Add(currentNodeName);
                        }
                    }
                }
            }

            throw new ArgumentException("Expected ---- separation line after the network plan information was not found.");
        }


        private void RegisterQueryPlacementOnNode(Query q, NodeName n)
        {
            if (!sourceNodesByEventName.ContainsKey(q.name))
            {
                sourceNodesByEventName[q.name] = new HashSet<NodeName>() { n };
            }
            else
            {
                sourceNodesByEventName[q.name].Add(n);
            }

            if (!queriesByNodeName.ContainsKey(n))
            {
                queriesByNodeName[n] = new HashSet<Query>() { q }; ;
            }
            else
            {
                queriesByNodeName[n].Add(q);
            }
        }



        public string generateHumanReadableString()
        {
            StringWriter writer = new StringWriter();


            foreach (var nodeName in networkPlan.Keys)
            {
                writer.WriteLine("");
                writer.WriteLine("***** Node " + nodeName + ": *****");

                writer.Write("Source of events:");

                foreach (var item in sourceNodesByEventName)
                {
                    if (item.Value.Contains(nodeName))
                    {
                        writer.Write(" " + item.Key);
                    }
                }

                writer.WriteLine("");

                // foreach (var e in networkPlan[nodeName].primitiveEventNames.Zip(networkPlan[nodeName].primitiveEventRates, (e, r) => new { Name = e, Rate = r }))
                // {
                //     if (e.Rate > 0)
                //     {
                //         writer.Write(" " + e.Name);
                //     }
                // }

                writer.WriteLine("Processing Queries:");


                foreach (var query in queriesByNodeName[nodeName])
                {
                    writer.Write("- [");

                    foreach (var item in query.inputEvents)
                    {
                        writer.Write(" " + item);
                    }

                    writer.Write(" ] => ");
                    writer.WriteLine(query.name);
                }
                
                writer.WriteLine("Print for all forwarding rules is missing! Add it.");
                /*
                writer.WriteLine("Forwarding Local Events to:");

                foreach (var ruleDict in forwardRulesByNodeName[nodeName])
                {
                    writer.Write("- " + ruleDict.Key + " =>");

                    foreach (var destinationNode in ruleDict.Value.destinations)
                    {
                        writer.Write(" " + destinationNode);
                    }

                    writer.WriteLine("");
                }*/
            }

            return writer.ToString();
        }
    }

}
