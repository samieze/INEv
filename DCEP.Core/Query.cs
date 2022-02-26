using System;
using System.Collections.Generic;
using System.Globalization;
using System.Runtime.Serialization;
using DCEP.Core.QueryProcessing;
using DCEP.Core.QueryProcessing.Operators;
using DCEP.Core.Utils;

namespace DCEP.Core
{

    [DataContract]
    public class Query
    {
        [DataMember]
        public EventType name { get; set; }

        [DataMember]
        public List<EventType> inputEvents { get; set; }

        [DataMember]
        public PlacementInfo placement { get; set; }

        [DataMember]
        public double selectionRate { get; set; }
        public double selectionRateTransition { get; set; }


        [DataMember]
        public AbstractQueryOperator rootOperator { get; set; }

        [DataMember]
        public string eventSelectionStrategy { get; set; }
        
        [DataMember]
        public string filteredBy { get; set; }

        public Query(EventType name, PlacementInfo placementInfo, IEnumerable<EventType> inputEventNames, double selectionRate, string eventSelectionStrategy, string filteredBy)
        {
            this.name = name;
            this.inputEvents = new List<EventType>();
            this.placement = placementInfo;
            this.selectionRate = selectionRate;
            this.rootOperator = (AbstractQueryOperator)new QueryComponentParser().parse(name.ToString());

			this.eventSelectionStrategy = eventSelectionStrategy;
            
            foreach (EventType item in inputEventNames)
            {
                inputEvents.Add(item);
            }
            this.selectionRateTransition = Math.Pow(selectionRate, 1.0/inputEvents.Count);
            this.filteredBy = filteredBy;
        }

        /// parsing legacy format and set default value for selection rate
        public static Query parseLegacyFormat(string input)
        {
            // remove whitespace
            input = string.Join("", input.Split(' '));

            string selectionStrategy = input.Substring(0,4);
            if(!selectionStrategy.Equals("STAM") && !selectionStrategy.Equals("STNM"))
                selectionStrategy = "STAM";

            string eventName = input.Split('[')[1].TrimEnd(',');
            string inputEventsString = input.Split('[')[2].Split(']')[0];
            string placementString = input.Split('[')[2].Split(']')[1].TrimStart(',');

            IEnumerable<EventType> inputEventNames = EventType.splitSemicolonSeparatedEventNames(inputEventsString);
            PlacementInfo placementInfo = new PlacementInfo(placementString);

            return new Query(new EventType(eventName), placementInfo, inputEventNames, 1.0d, selectionStrategy, "");
        }

        public static Query createFromString(string input)
        {
            // support legacy format
            if (input.TrimAllWhitespace().StartsWith("["))
            {
                return parseLegacyFormat(input);
            }

            if (!input.Contains("SELECT")){
                throw new ArgumentException("Query string is missing the SELECT statement.");
            }


            // parsing required components
            // determine event selection strategy (ANY/NEXT)
            string selectionStrategy = input.Substring(0,4);
            if(!selectionStrategy.Equals("STAM") && !selectionStrategy.Equals("STNM"))
                selectionStrategy = "STAM";

            string eventName = input.Split("SELECT")[1].Split("FROM")[0].TrimAllWhitespace();
            string inputEventsString = input.Split("FROM")[1].Split("WITH")[0].TrimAllWhitespace();
            
            string filterEventType = "";
            if (eventName.Contains("|"))
            {
                filterEventType = eventName.Split("|")[1];
                eventName = eventName.Split("|")[0];
            }
            
            IEnumerable<EventType> inputEventNames = EventType.splitSemicolonSeparatedEventNames(inputEventsString);
            
            // parsing optional components
            string withString = (input.Contains("WITH")) ? input.Split("WITH")[1].TrimAllWhitespace() : "";

            double selectionRate = 1.0;
            if (withString.Contains("selectionRate="))
            {
                selectionRate = Double.Parse(withString.Split("selectionRate=")[1].Split(",")[0], CultureInfo.InvariantCulture);
            }

            // constructing query instance
            return new Query(new EventType(eventName), new PlacementInfo(), inputEventNames, selectionRate, selectionStrategy, filterEventType);
        }

        public override string ToString()
        {
            return String.Format("SELECT {0} FROM {1}", name, string.Join(",", inputEvents));
        }
    }
}
