using System.Runtime.CompilerServices;
using System;
using System.Collections.Generic;
using DCEP.Core.QueryProcessing.Operators;
using System.Runtime.Serialization;

namespace DCEP.Core.QueryProcessing
{
    [DataContract]
    public class QueryComponentParser
    {
        [DataMember]
        private readonly Dictionary<string, Type> operatorClassByName = new Dictionary<string, Type>(){
            {"AND", typeof(ANDOperator)},
            {"SEQ", typeof(SEQOperator)}
        };


        public QueryComponent parse(string input)
        {
            input = input.Replace(" ", "");


            foreach (var item in operatorClassByName)
            {
                if (input.StartsWith(item.Key))
                {
                    return (AbstractQueryOperator)Activator.CreateInstance(item.Value, input);
                }
            }

            // no operator detected, input must be an event type

            if (input.IndexOf('(') != -1)
            {
                throw new ArgumentException("Event names must not contain '(' characters.");
            }

            if (input.IndexOf(')') != -1)
            {
                throw new ArgumentException("Event names must not contain '(' characters.");
            }

            return new EventType(input);

            //throw new ArgumentException("Could not find an operator type for input: " + input);
        }

    }

    public static class EventTypeParsingExtension
    {
        public static QueryComponent parseToQueryComponent(this EventType eventType)
        {
            return new QueryComponentParser().parse(eventType.name);
        }
    }
}