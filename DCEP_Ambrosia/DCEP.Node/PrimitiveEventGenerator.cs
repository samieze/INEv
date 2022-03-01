using System.Linq;
using System.Reflection.Metadata.Ecma335;
using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Runtime.Serialization;
using DCEP;
using DCEP.Core;
using DCEP.Core.Utils.PoissonEvaluator;

namespace DCEP.Node
{
    [DataContract]
    public class PrimitiveEventGenerator
    {
        [DataMember]
        private readonly int eventCount;

        [DataMember]
        EventType eventName;

        [DataMember]
        Stopwatch stopwatch = new Stopwatch();

        [DataMember]
        Random random = new Random();

        [DataMember]
        int timeArrayIndex;

        [DataMember]
        double[] timeArray;

        [DataMember]
        double elapsedTimeOffset = 0.0;

        [DataMember]
        long intervalMS;

        [DataMember]
        double lastIntervalReset = 0.0;

        [DataMember]
        private readonly NodeName nodeName;

        public PrimitiveEventGenerator(int eventCount, TimeUnit timeUnit, EventType eventName, NodeName nodeName)
        {
            this.eventCount = eventCount;
            this.eventName = eventName;
            this.nodeName = nodeName;

            //this.rate = timeUnit.GetIntervalFromCountPerUnit(eventCount);
            timeArray = new double[eventCount];
            intervalMS = (long)timeUnit.GetTimeSpanFromDuration(1).TotalMilliseconds;
        }

        private void repopulateTimeArray()
        {
            stopwatch.Restart();
            timeArrayIndex = 0;

            for (int i = 0; i < eventCount; i++)
            {
                timeArray[i] = random.NextDouble() * intervalMS;
            }
            Array.Sort(timeArray);

        }

        public PrimitiveEvent[] generate()
        {
            // start timer, initialize and return empty list if the timer was not running
            if (!stopwatch.IsRunning)
            {
                repopulateTimeArray();
                return new PrimitiveEvent[0];
            }

            // count the random timestamps in the array that have passed and not yet been registered
            var outputCount = 0;
            double passedTime = stopwatch.Elapsed.TotalMilliseconds + elapsedTimeOffset;
            while (timeArrayIndex < eventCount && timeArray[timeArrayIndex] <= passedTime)
            {
                outputCount++;
                timeArrayIndex++;
            }

            // repopulate the array once the interval is over
            if (passedTime - lastIntervalReset > intervalMS)
            {
                // count potentially remaining array timestamps before the array is reset
                outputCount += eventCount - timeArrayIndex;

                // calculate offset between upcoming actual interval change and theoretical interval change
                // add this offset to the elapsed time afterwards, since the time between theoretical interval change
                // and actual interval change would be lost otherwise
                elapsedTimeOffset = passedTime - lastIntervalReset - intervalMS;

                repopulateTimeArray();
            }

            // actually generate the output events
            var outputs = new PrimitiveEvent[outputCount];
            for (int i = 0; i < outputCount; i++)
            {
                outputs[i] = new PrimitiveEvent(eventName, nodeName);
            }

            return outputs;
        }
    }
}

