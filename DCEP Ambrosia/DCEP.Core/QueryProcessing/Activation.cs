using System;
using System.Collections.Generic;
using System.Runtime.InteropServices;
using System.Data.SqlTypes;
using System.Linq;
using System.Runtime.Serialization;

namespace DCEP.Core
{
    [DataContract]
    internal class Activation
    {
        [DataMember]
        AbstractEvent[] eventBuffer { get; set; }

        [DataMember]
        public State currentState { get; set; }


        public Activation(State startState)
        {
            currentState = startState;
            eventBuffer = new AbstractEvent[0];
        }

        public Activation(State startState, AbstractEvent firstEvent)
        {
            currentState = startState;
            eventBuffer = new AbstractEvent[] { firstEvent };
        }

        public Activation(State startState, AbstractEvent[] oldEventBuffer, AbstractEvent newBufferEvent)
        {
            currentState = startState;
            eventBuffer = new AbstractEvent[oldEventBuffer.Count() + 1];
            eventBuffer[0] = newBufferEvent;
            oldEventBuffer.CopyTo(eventBuffer, 1);
        }

        /// returns potentially new activations or a complete event buffer to generate the output event from
        public (IEnumerable<Activation>, IEnumerable<AbstractEvent>, bool) consumeEvent(AbstractEvent e, DateTime t, TimeSpan timeWindow)
        {
           /* if (testInvalid(t, timeWindow)){  
                return (null, null, true);
            }*/ 
           
            if (currentState.testGuardConditions(e, eventBuffer))
            {

                if (currentState.nextStates == null)
                {
                    // no next states exist, returning the complete buffer to then create the output event
                    var bufferlistoutput = new List<AbstractEvent>(eventBuffer);
                    bufferlistoutput.Add(e);
                    return (null, bufferlistoutput, false);
                }
               
                var outputActivations = currentState.nextStates.Select((state) => new Activation(state, eventBuffer, e));
                return (outputActivations, null,  false);
            
            }
           
            return (null, null, false);
           


        }

        public bool testInvalid(DateTime t, TimeSpan timeWindow)
        {
            if (eventBuffer.Length > 0)
            {
                var x = eventBuffer.Select(even => even.timeCreated).ToList().Min(); //x = oldest Event in eventBuffer
                //return false;
                return ((t - x).Duration() >= timeWindow);
            }
            return false;
        }
    }
}
