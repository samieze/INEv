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
        private double eventCount;
        
        [DataMember]
        private readonly int eventPercentageVariance;
        
        [DataMember]
        private int eventCountForCurrInterval;
    
        [DataMember]
        private int intervalCount;
        
        [DataMember]
        private double duration;

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
        
        [DataMember]
        private int[] outputratesAdjustedByVariance;
        
        [DataMember]
        private int varianceSeed;
        
        [DataMember]
        private int[] outputRateFactor;

        public PrimitiveEventGenerator(double eventCount, double outputRateFactor, int eventPercentageVariance, int varianceSeed, double duration, TimeUnit timeUnit, EventType eventName, NodeName nodeName)
        {
            this.eventCount = eventCount * outputRateFactor;
            this.eventPercentageVariance = eventPercentageVariance;
            this.varianceSeed = varianceSeed;
            this.eventName = eventName;
            this.nodeName = nodeName;
            this.intervalCount = 1;
            this.duration = duration;
            
            this.outputratesAdjustedByVariance = new int[(int)duration];
            if (varianceSeed != 0)
                this.random = new Random(varianceSeed);
            //this.rate = timeUnit.GetIntervalFromCountPerUnit(eventCount);
            //timeArray = new double[eventCount];
            
            //duration is the number of time intervals
            double actualVariance = eventPercentageVariance * duration * eventCount/100.0;
            int budget = (int) (eventCount * duration + (random.NextDouble() * 2 * actualVariance - actualVariance));
            int usedBudget = budget;
            
            for(int i = 0; i < duration; ++i)
            {
                if (eventPercentageVariance == 0)
                {
                    this.outputratesAdjustedByVariance[i] = 0;
                    continue;
                }

                if (i == 0)
                {
                    this.outputratesAdjustedByVariance[i] = random.Next(0,budget+1);
                    usedBudget -= this.outputratesAdjustedByVariance[i];
                }
                else if (i == duration-1)
                {
                    this.outputratesAdjustedByVariance[i] = usedBudget;
                } 
                else
                {
                    this.outputratesAdjustedByVariance[i] = random.Next(0,usedBudget+1);
                    usedBudget -= this.outputratesAdjustedByVariance[i];
                }
            }
            
            outputratesAdjustedByVariance = outputratesAdjustedByVariance.OrderBy(x => random.Next()).ToArray();    

            intervalMS = (long)timeUnit.GetTimeSpanFromDuration(1).TotalMilliseconds;
            
        }

        private void repopulateTimeArray()
        {
            if (intervalCount < duration)
            {
                if (eventCount < 1 && eventCount > 0)
                {
                    if (random.NextDouble() <= eventCount)
                    {
                        eventCount = 1;
                    }
                    else
                    {
                        eventCount = 0;
                    }
                }
                
                //Console.WriteLine("intervalCount-1:"+(intervalCount-1));
                if (random.Next() % 2 == 0)
                {                        
                    eventCountForCurrInterval = (int)eventCount + outputratesAdjustedByVariance[intervalCount-1]; //also negative values should be allowed here
                }
                else
                {
                    //Console.WriteLine("REDUCED OUTRATE" + eventCount);
                    eventCountForCurrInterval = Math.Max((int)eventCount - outputratesAdjustedByVariance[intervalCount-1],0); //also negative values should be allowed here
                }
                eventCountForCurrInterval = (int)eventCountForCurrInterval;
                //Console.WriteLine("[" + nodeName + "] "+" interval "+ intervalCount +" ~ " + "for eventtype " + eventName + " - variance output rate " + eventCountForCurrInterval + " - actual output rate: " + eventCount);
                timeArray = new double[eventCountForCurrInterval];
                
                stopwatch.Restart();
                ++intervalCount;
                timeArrayIndex = 0;
                
                for (int i = 0; i < eventCountForCurrInterval; i++)
                {
                    timeArray[i] = random.NextDouble() * intervalMS;
                }
                Array.Sort(timeArray);
            }

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
            while (timeArrayIndex < eventCountForCurrInterval && timeArray[timeArrayIndex] <= passedTime)
            {
                outputCount++;
                timeArrayIndex++;
            }

            // repopulate the array once the interval is over
            if (passedTime - lastIntervalReset > intervalMS)
            {
                // count potentially remaining array timestamps before the array is reset
                outputCount += eventCountForCurrInterval - timeArrayIndex;

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

