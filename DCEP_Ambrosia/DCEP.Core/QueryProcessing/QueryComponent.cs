using System.Linq;
using System.ComponentModel.DataAnnotations;
using System.Collections;
using System.Collections.Generic;
using System.Runtime.Serialization;
using DCEP.Core.Utils;
using DCEP.Core.QueryProcessing.Operators;

namespace DCEP.Core
{
    [DataContract(IsReference = true)]
    [KnownType(typeof(AbstractQueryOperator))]
    [KnownType(typeof(EventType))]
    public abstract class QueryComponent : ITreeNode<QueryComponent>
    {
        public QueryComponent Value => this;

        public IEnumerable<ITreeNode<QueryComponent>> Children => this.getChildren();

        // public QueryComponent parent { get; set; } = null;
        // public abstract QueryComponent getParent();
        public abstract IEnumerable<QueryComponent> getChildren();
        public abstract IEnumerable<EventType> getComponentsAsEventTypes();
        public abstract EventType asEventType();


        /// traverse the  tree downwards and return the first occurrence of a or b, or null if both never occur
        public QueryComponent getFirstOccuringChildOf(QueryComponent a, QueryComponent b)
        {
            Stack<QueryComponent> toCheck = new Stack<QueryComponent>();
            toCheck.Push(this);

            while (toCheck.Count > 0)
            {
                var comp = toCheck.Pop();

                if (comp.Equals(a))
                {
                    return a;
                }
                else if (comp.Equals(b))
                {
                    return b;
                }

                foreach (var child in comp.getChildren().Reverse())
                {
                    toCheck.Push(child);
                }
            }

            return null;
        }

        public List<EventType> getListOfPrimitiveEventTypes()
        {
            var output = new List<EventType>();
            if (this is EventType)
            {
                output.Add((EventType)this);

            }
            else
            {
                Stack<QueryComponent> toCheck = new Stack<QueryComponent>();
                toCheck.Push(this);

                while (toCheck.Count > 0)
                {
                    var comp = toCheck.Pop();

                    if (comp is EventType)
                    {
                        output.Add((EventType)comp);
                    }

                    foreach (var child in comp.getChildren())
                    {
                        toCheck.Push(child);
                    }
                }
            }
            return output;
        }
    }
}
