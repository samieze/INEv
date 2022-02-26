using System.Diagnostics;
using System.Collections.Immutable;
using System.Collections;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Reflection.Metadata;
using System.Runtime.Serialization;
using DCEP.Core;
using DCEP.Core.QueryProcessing;
using DCEP.Core.Utils;
using DCEP.Core.QueryProcessing.Constraints;
using DCEP.Core.Utils.LeastCommonAncestor;
using DCEP.Core.QueryProcessing.Operators;

namespace DCEP.Core
{
    [DataContract]
    public class QueryProcessorUniqueComponents : QueryProcessor
    {
        [DataMember]
        List<State> startStates;

        [DataMember]
        Dictionary<Tuple<EventType, string>, List<Activation>> activationsByInputEventType;

        [DataMember]
        ImmutableList<EventType> queryComponentNames;

        [DataMember]
        private LeastCommonAncestorFinder<QueryComponent> leastCommonAncestorFinder;

        [DataMember]
        private readonly List<PrimitiveBufferComponentAllMatchConstraint> pBCAllMatchConstraints;

        [DataMember]
        private readonly ExecutionPlan executionPlan;

        [DataMember]
        private readonly NodeName nodeName;

        [DataMember]
        private Dictionary<NodeName, List<AbstractEvent>> sourceBuffers;

        [DataMember]
        private HashSet<EventType> initiatorEvents;

        [DataMember]
        private Dictionary<NodeName, List<EventType>> eventTypesProducedByNode;

        [DataMember] DateTime startTime; // for partial matches print
        
        [DataMember] TimeSpan printInterval;
        
        private Random randomNumberGenerator = new Random();
        
        public QueryProcessorUniqueComponents(Query query, TimeSpan timeWindow, ExecutionPlan executionPlan_, NodeName nodeName_) : base(query, timeWindow)
        {
            startStates = new List<State>();
            activationsByInputEventType = new Dictionary<Tuple<EventType, string>, List<Activation>>();
            executionPlan = executionPlan_;
            nodeName = nodeName_;
            leastCommonAncestorFinder = new LeastCommonAncestorFinder<QueryComponent>(query.rootOperator);

            eventTypesProducedByNode = new Dictionary<NodeName, List<EventType>>();


            sourceBuffers = new Dictionary<NodeName, List<AbstractEvent>>();
            initiatorEvents = new HashSet<EventType>();
            this.pBCAllMatchConstraints = new List<PrimitiveBufferComponentAllMatchConstraint>(){
                    new WithinTimeWindowConstraint(timeWindow)
                };

            //For partial matches print
            startTime = DateTime.UtcNow;
            //Determines the print interval of concurrent partial matches
            printInterval = TimeSpan.FromSeconds(15);
            
            initialize();
        }


        private void initialize()
        {
            queryComponentNames = query.rootOperator.getComponentsAsEventTypes().ToImmutableList();

            startStates = createAutomata(new HashSet<EventType>(query.inputEvents), Enumerable.Empty<EventType>());

            //STNM == Skip Till Next Match (Policy)
            if(query.eventSelectionStrategy.Equals("STNM"))
            {
                initializeSourceBuffers();
            }

            foreach (var startState in startStates)
            {
                initiatorEvents.Add(startState.requiredEventType);
                var key = new Tuple<EventType, string>(startState.requiredEventType, startState.requiredEventType.filteredBy);
                activationsByInputEventType[key] = new List<Activation>() { new Activation(startState) };
            }

        }

        //only relevant for skip-till next match global watermark
        //determine all sources for this node to generate one buffer per source
        //initialize hashmap from nodename to produced event types for optimization step
        private void initializeSourceBuffers()
        {
            /*(sourceBuffers[this.nodeName] = new List<AbstractEvent>();
            foreach (var forwardRules in executionPlan.forwardRulesByNodeName)
            {
                foreach (var forwardRule in forwardRules.Value)
                {
                    foreach (var nodeName in forwardRule.Value.destinations)
                    {
                        if (this.nodeName.Equals(nodeName))
                        {
                            sourceBuffers[forwardRules.Key] = new List<AbstractEvent>();

                            if (!eventTypesProducedByNode.ContainsKey(forwardRules.Key))
                                eventTypesProducedByNode[forwardRules.Key] = new List<EventType>();
                            eventTypesProducedByNode[forwardRules.Key].Add(forwardRule.Key);
                        }
                    }
                }
            }*/
            throw new ArgumentException("Source Buffers for skip-til next match are not initialized!");
        }


        private List<State> createAutomata(HashSet<EventType> remainingInputs, IEnumerable<EventType> preceedingEventTypes)
        {
            if (remainingInputs.Count == 0)
            {
                return null;
            }
            else
            {
                var result = new List<State>();

                foreach (var inputEvent in remainingInputs)
                {
                    // create state with constraints
                    var pBCAnyMatchConstraints = createPBCAnyMatchConstraints(inputEvent, preceedingEventTypes);

                    var bufferConstraints = new List<BufferConstraint>();
                    State s = new State(inputEvent, bufferConstraints, pBCAnyMatchConstraints, this.pBCAllMatchConstraints);

                    // create proceeding states
                    var newRemaining = new HashSet<EventType>(remainingInputs);
                    newRemaining.Remove(inputEvent);

                    var updatedPreceedingEventTypesList = preceedingEventTypes.ToList();
                    updatedPreceedingEventTypesList.Add(inputEvent);

                    s.nextStates = createAutomata(newRemaining, updatedPreceedingEventTypesList);

                    result.Add(s);
                }

                return result;
            }
        }

        internal List<PrimitiveBufferComponentAnyMatchConstraint> createPBCAnyMatchConstraints(EventType inputEvent, IEnumerable<EventType> preceedingEventTypes)
        {
            var output = new List<PrimitiveBufferComponentAnyMatchConstraint>();
            var equalIDGuaranteed = new HashSet<EventType>();

            foreach (var eventInBuffer in preceedingEventTypes)
            {
                // possibly deconstruct complex event types to primitive types for checking their respective constraints
                foreach (var primitiveInputEvent in inputEvent.parseToQueryComponent().getListOfPrimitiveEventTypes())
                {
                    foreach (var primitveEventInBuffer in eventInBuffer.parseToQueryComponent().getListOfPrimitiveEventTypes())
                    {
                        if (primitiveInputEvent.Equals(primitveEventInBuffer))
                        {
                            if (!equalIDGuaranteed.Contains(primitiveInputEvent))
                            {
                                output.Add(new EqualIDWhenEqualEventTypeConstraint(primitiveInputEvent));
                                equalIDGuaranteed.Add(primitiveInputEvent);
                            }

                            continue;
                        }

                        var op = (AbstractQueryOperator)leastCommonAncestorFinder.FindCommonParent(primitiveInputEvent, primitveEventInBuffer);

                        if (op is SEQOperator)
                        {
                            // derive predecessor or successor constraint
                            var first = op.getFirstOccuringChildOf(primitiveInputEvent, primitveEventInBuffer);

                            if (primitiveInputEvent.Equals(first))
                            {
                                output.Add(new SequenceConstraint(primitiveInputEvent, primitveEventInBuffer, SequenceType.IsPredecessor));
                            }
                            else if (primitveEventInBuffer.Equals(first))
                            {
                                output.Add(new SequenceConstraint(primitiveInputEvent, primitveEventInBuffer, SequenceType.IsSuccessor));
                            }
                        }

                    }
                }
            }

            return output;
        }

        public override IEnumerable<ComplexEvent> processInputEvent(AbstractEvent e, DateTime t)
        {
            getSizeOfPartialMatches();
            if (query.eventSelectionStrategy.Equals("STNM"))
                return skipTillNextMatch(e, t);
            else
                return skipTillAnyMatch(e, t);
        }


        private IEnumerable<ComplexEvent> skipTillNextMatch(AbstractEvent e, DateTime t)
        {
            List<ComplexEvent> outputEvents = new List<ComplexEvent>();
            /*
            bool singleSource = sourceBuffers.Count==1?true:false;
            
            if(!singleSource)
            {
                if (!sourceBuffers.ContainsKey(e.nodeName))
                {
                    sourceBuffers[e.nodeName] = new List<AbstractEvent>();
                }

                sourceBuffers[e.nodeName].Add(e);
            }
            
            
            bool bufferOptimizationWasRun = false;

            //check for the current best local watermark (output guarantee)
            while (true)
            {
                if(!singleSource)
                {
                    bool anyBufferEmpty = false;
                    List<AbstractEvent> minimumBuffer = null;
                    List<EventType> forbiddenEventTypes = new List<EventType>();
                    
                    int count = 0;
                    int numberOfBufferedEvents = 0;
                    foreach (var sourceBuffer in sourceBuffers)
                    {
                        numberOfBufferedEvents += sourceBuffer.Value.Count;

                        if (sourceBuffer.Value.Count == 0 && !sourceBuffer.Key.Equals(this.nodeName))
                        {
                            anyBufferEmpty = true;
                            // collect from every empty source buffer the correlating event types
                            forbiddenEventTypes.AddRange(eventTypesProducedByNode[sourceBuffer.Key]);
                        }
                        else
                        {
                            if (sourceBuffer.Value.Count != 0 && (minimumBuffer == null || sourceBuffer.Value[0].timeCreated < minimumBuffer[0].timeCreated))
                            {
                                minimumBuffer = sourceBuffer.Value;
                            }
                        }
                    }


                    if(anyBufferEmpty)
                    {
                        // only if current oldest event type is not forbidden and only run optimization once
                        if (minimumBuffer == null || forbiddenEventTypes.Contains(minimumBuffer[0].type) || bufferOptimizationWasRun)
                            break;

                        bufferOptimizationWasRun = true;
                    }


                    e = minimumBuffer[0];

                    // only remove elements, if optimization is not active
                    if(!bufferOptimizationWasRun)
                        minimumBuffer.RemoveAt(0);
                }


                if(activationsByInputEventType.ContainsKey(e.type))
                {
                    // reverse loop through activations to remove the ones that made a transition in the loop
                    for (int activationIndex = activationsByInputEventType[e.type].Count - 1; activationIndex >= 0; activationIndex--)
                    {
                        // if buffer optimization is activated, then no instance shall be created
                        if (bufferOptimizationWasRun && activationIndex < startStates.Count)
                            continue;

                        var (newactivations, outputeventcomponents, invalid) = activationsByInputEventType[e.type][activationIndex].consumeEvent(e,t,timeWindow);


                        if (newactivations != null)
                        {
                            foreach (var newactivation in newactivations)
                            {
                                activationsByInputEventType[newactivation.currentState.requiredEventType].Add(newactivation);
                            }
                        }

                        if (outputeventcomponents != null)
                        {
                            outputEvents.Add(new ComplexEvent(query.name, outputeventcomponents, nodeName));
                        }

                        if((newactivations != null || outputeventcomponents != null) && activationIndex >= startStates.Count)
                        {
                            activationsByInputEventType[e.type].RemoveAt(activationIndex);
                        }
                    }
                }
                if(singleSource)
                    break;
            }
            */
            return outputEvents;
        }

        private void getSizeOfPartialMatches()
        {   
            /*Console.WriteLine("getSizeOfPartialMatches");
            Console.WriteLine("DateTime.UtcNow:" + DateTime.UtcNow);
            Console.WriteLine("startTime:" + startTime);
            Console.WriteLine("DateTime.UtcNow - startTime > printInterval" + (DateTime.UtcNow - startTime > printInterval));*/
            if(DateTime.UtcNow - startTime > printInterval)
            {
                int size = 0;
                
                foreach(var key in activationsByInputEventType.Keys)
                {
                    size += activationsByInputEventType[key].Count();
                }
                Console.WriteLine("["+ nodeName +"] maintains " + size + " partial matches.");
                startTime = DateTime.UtcNow;
            }
        }

        private IEnumerable<ComplexEvent> skipTillAnyMatch(AbstractEvent e, DateTime t)
        {
            var activationsKey = new Tuple<EventType, string>(e.type, e.filteredBy);

            if (!activationsByInputEventType.ContainsKey(activationsKey)) return Enumerable.Empty<ComplexEvent>(); 
            
            List<ComplexEvent> outputEvents = new List<ComplexEvent>();
            
            List<Tuple<EventType,Activation>> invalidActivations = new List<Tuple<EventType,Activation>>(); //Samira [for removing partial matches due to expired timestamp]
            
            foreach (var activation in activationsByInputEventType[activationsKey])
            {
                var doDropIt = randomNumberGenerator.NextDouble() > query.selectionRateTransition;
                if (doDropIt)
                {
                    continue;
                }
                
                var (newactivations, outputeventcomponents, invalid) = activation.consumeEvent(e, t, timeWindow); // add return field to indicate that the activation should be removed
                

                if (newactivations != null)
                {
                    foreach (var newactivation in newactivations)
                    {
                        var newActivationsKey = new Tuple<EventType, string>(newactivation.currentState.requiredEventType, newactivation.currentState.requiredEventType.filteredBy);
                        activationsByInputEventType[newActivationsKey].Add(newactivation);
                    }
                }
                
                if (outputeventcomponents != null)
                {
                    var complexEvent = new ComplexEvent(query.name, outputeventcomponents, nodeName);
                    complexEvent.setFilter(query.filteredBy);
                    outputEvents.Add(complexEvent);
                }
                
                
            }
        
            return outputEvents;
        }
         
        public override void removeActivations(DateTime t)
        {
            List<Tuple<Tuple<EventType, string>,Activation>> invalidActivations = new List<Tuple<Tuple<EventType, string>,Activation>>();
            foreach (var key in activationsByInputEventType.Keys)
            {
                foreach (var act in activationsByInputEventType[key])
                {
                    if (act.testInvalid(t,timeWindow))
                    { 
                        invalidActivations.Add(new Tuple<Tuple<EventType, string>,Activation>(key,act));
                    }
                }
            }
            foreach (var tuple in invalidActivations)
            {   
                removedActivations++;
                activationsByInputEventType[tuple.Item1].Remove(tuple.Item2);
            }  
        }
    }
}
