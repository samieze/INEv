using DCEP;
using DCEP.Core;
using DCEP.Core.Utils.DeepCloneExtension;
using System;
using System.Collections.Generic;
using System.Globalization;
using System.Runtime.Serialization;


namespace DCEP.Core
{
    [DataContract]
    [KnownType(typeof(PrimitiveEvent))]
    [KnownType(typeof(ComplexEvent))]
    public abstract class AbstractEvent
    {
        [DataMember]
        public DateTime timeCreated;
        
        [DataMember]
        public DateTime actualTime; // Samira

        [DataMember]
        public string ID { get; set; }

        [DataMember]
        public EventType type { get; set; }

        [DataMember]
        public Dictionary<string, string> attributes { get; set; }

        [DataMember]
        public List<NodeName> knownToNodes { get; set; }

        [DataMember]
        public NodeName lastSenderNodeName { get; set; }

        [DataMember]
        public NodeName nodeName;

        [DataMember]
        public string filteredBy { get; set; }

        protected AbstractEvent(EventType name, NodeName nodeName)
        {
            timeCreated = DateTime.Now; // Samira
            actualTime = timeCreated; // Samira
            ID = Guid.NewGuid().ToString();
            attributes = new Dictionary<string, string>();
            knownToNodes = new List<NodeName>();
            this.type = name;
            this.nodeName = nodeName;
            lastSenderNodeName = nodeName; //Steven
            this.filteredBy = "";
        }
        
        /*new*/
        protected AbstractEvent(EventType name, DateTime t)
        {
            actualTime = DateTime.Now; // Samira
            timeCreated = t; // Samira [generate event with creation time from input file]
            ID = Guid.NewGuid().ToString();
            attributes = new Dictionary<string, string>();
            knownToNodes = new List<NodeName>();
            this.type = name;
            this.nodeName = nodeName;
            this.filteredBy = "";
        }
        /*new*/

        public string getCreatedTimestamp()
        {
            return timeCreated.ToString("yyyy-MM-dd HH:mm:ss.fff",
                                            CultureInfo.InvariantCulture);
        }
        
        public void setFilter(string filter)
        {
            this.filteredBy = filter;
        }
        
        public override string ToString()
        {
            return String.Format("{{{0}, {1}, {2}}}", type, getCreatedTimestamp(), ID.Substring(0, 8));
        }

        public abstract DateTime getOldest(); // Samira
        public abstract DateTime getNewestAlt(); // Samira
       
        
        public override bool Equals(object obj)
        {
            return base.Equals(obj);
        }

        public override int GetHashCode()
        {
            return base.GetHashCode();
        }

        public string getAllPrimitiveEventTypesAsString()
        {
            var allPrimitiveEventTypesString = this.type.ToString().Replace("SEQ", "");
            allPrimitiveEventTypesString = allPrimitiveEventTypesString.Replace("AND", "");
            allPrimitiveEventTypesString = allPrimitiveEventTypesString.Replace("(", "");
            allPrimitiveEventTypesString = allPrimitiveEventTypesString.Replace(")", "");
            var allPrimitiveEventTypes = allPrimitiveEventTypesString.Split(',');
            string result = "";
            foreach(var primitiveEventType in allPrimitiveEventTypes)
                result += primitiveEventType.ToString();
                
            return result;
        }

        public IEnumerable<AbstractEvent> getAllPrimitiveEventComponents()
        {
            List<AbstractEvent> output = new List<AbstractEvent>();
            var s = new Stack<AbstractEvent>();
            s.Push(this);

            while (s.Count != 0)
            {
                var current = s.Pop();
                
                if (current is ComplexEvent)
                {
                    
                    foreach (var child in (current as ComplexEvent).children)
                    {
                        s.Push(child);
                    }
                }
                else if (current is PrimitiveEvent)
                {
                    output.Add(current);
                }

            }

            return output;
        }
        
        
        public AbstractEvent getSubProjection(EventType eventTypeToSend) //Steven 
        {
            //if there is nothing to filter
            if(eventTypeToSend.Equals(type))
                return this.DeepClone();
            
            var requiredEventTypes = eventTypeToSend.getAllPrimitiveEventTypes();
            
            List<AbstractEvent> output = new List<AbstractEvent>();

            foreach(var primitiveEvent in getAllPrimitiveEventComponents())
            {
                if(requiredEventTypes.Contains(primitiveEvent.type))
                {
                     output.Add(primitiveEvent);
                }
            }
            if(output.Count == 1)
                return output[0].DeepClone();
            else
                return new ComplexEvent(eventTypeToSend, output, nodeName);
        }
        
        
        public IEnumerable<AbstractEvent> getAllEventComponents() //Steven
        {
            List<AbstractEvent> output = new List<AbstractEvent>();
            var s = new Stack<AbstractEvent>();
            s.Push(this);
            
            while (s.Count != 0)
            {
                var current = s.Pop();
                
                output.Add(current);
                if (current is ComplexEvent)
                {
                    foreach (var child in (current as ComplexEvent).children)
                    {
                        s.Push(child);
                    }
                }
            }

            return output;
        }
        
        
    }

}
