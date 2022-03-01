using System.Collections;
using System;
using System.Diagnostics;
using System.Reflection;
using System.Reflection.Metadata;
using System.Linq;
using System.Collections.Generic;
using System.Runtime.Serialization;

namespace DCEP.Core.QueryProcessing.Operators
{
    [DataContract]
    [KnownType(typeof(ANDOperator))]
    [KnownType(typeof(SEQOperator))]
    public abstract class MultiArgOperator : AbstractQueryOperator
    {
        [DataMember]
        List<QueryComponent> components;

        [DataMember]
        EventType eventType;

        public MultiArgOperator(string input)
        {
            eventType = new EventType(input);

            int openBraces = 1;
            int lastComponentStart = input.IndexOf('(') + 1;
            components = new List<QueryComponent>();

            for (int pivot = lastComponentStart; pivot < input.Length; pivot++)
            {
                if (input[pivot] == '(')
                {
                    openBraces++;
                }
                else if (input[pivot] == ')')
                {
                    openBraces--;
                    if (openBraces == 0)
                    {
                        if (pivot != input.Length - 1)
                        {
                            throw new ArgumentException("A closing brace at root level has to be the last character. Input: " + input);
                        }
                        components.Add(parseComponentString(input.Substring(lastComponentStart, pivot - lastComponentStart)));
                    }
                }
                else if (input[pivot] == ',')
                {
                    if (openBraces == 1)
                    {
                        // comma at root level separates components, adding component
                        components.Add(parseComponentString(input.Substring(lastComponentStart, pivot - lastComponentStart)));
                        lastComponentStart = pivot + 1;
                    }
                }
            }

            if (components.Count() < 2)
            {
                throw new ArgumentException("At least two components are required for MultiArgOperator. Input: " + input);
            }
        }

        public override EventType asEventType()
        {
            return eventType;
        }

        public override IEnumerable<QueryComponent> getChildren()
        {
            return components;
        }

        public override IEnumerable<EventType> getComponentsAsEventTypes()
        {
            return components.Select((comp) => comp.asEventType());
        }
    }
}