using System;
using System.Collections.Generic;
using System.Runtime.Serialization;
using DCEP.Core;

namespace DCEP.Core.QueryProcessing
{
    [DataContract]
    [KnownType(typeof(QueryProcessorUniqueComponents))]
    public abstract class QueryProcessor
    {
        [DataMember]
        public readonly Query query;

        [DataMember]
        protected readonly TimeSpan timeWindow;
        
        [DataMember]
        public int removedActivations { get; set; }
        
        [DataMember]
        public static HashSet<EventType> transitionEventTypes = new HashSet<EventType>();

        public abstract IEnumerable<ComplexEvent> processInputEvent(AbstractEvent e, DateTime t);
        public abstract void removeActivations(DateTime t);
        protected QueryProcessor(Query query, TimeSpan timeWindow)
        {
            this.query = query;
            this.timeWindow = timeWindow;
            foreach(var transitionEventType in query.inputEvents)
            {
                transitionEventTypes.Add(transitionEventType);
            }
        }

        public bool inputEventIsTransitionEventType(AbstractEvent e)
        {
            return transitionEventTypes.Contains(e.type);
        }

        public static QueryProcessor getQueryProcessorForQuery(Query q, TimeSpan timeWindow, ExecutionPlan executionPlan, NodeName name)
        {
            // check if any primitive events occure more than once in the query
            var primitiveEventTypesInQuery = q.rootOperator.getListOfPrimitiveEventTypes();
            var numberOfUniquePrimitiveEventTypesInQuery = new HashSet<EventType>(primitiveEventTypesInQuery).Count;

            foreach(var transitionEventType in q.inputEvents)
            {
                transitionEventTypes.Add(transitionEventType);
            }

            if (primitiveEventTypesInQuery.Count == numberOfUniquePrimitiveEventTypesInQuery)
            {
                // no duplicate primitive events in query
                return new QueryProcessorUniqueComponents(q, timeWindow, executionPlan, name);

            }
			else
            {
                return null;
            }
        }
    }

}
