using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;
using System.Text.RegularExpressions;
using DCEP.AmbrosiaNodeAPI;
using DCEP.Core;
using DCEP.Core.QueryProcessing;
using DCEP.Node;

namespace DCEP.Test
{
    public abstract class DCEPTestClass
    {
        /// helper method for consise test cases
        /// creates two A and a B event from an "AAB" input
        /// (assuming single character event names)
        protected List<AbstractEvent> createPrimitiveEvents(string inputstring)
        {
            List<AbstractEvent> inputList = new List<AbstractEvent>();
            string[] inputs = Regex.Split(inputstring, string.Empty);
            foreach (var input in inputs)
            {
                // skipping first empty string
                if (input.Length > 0)
                {
                    inputList.Add(new PrimitiveEvent(input, null));
                }
            }
            return inputList;
        }

        /// helper method for concise test cases
        protected List<ComplexEvent> getOutputWithTimeWindow(string querystring, List<AbstractEvent> inputs, TimeSpan timeWindow)
        {
            Query q = Query.createFromString(querystring);

            QueryProcessor p = QueryProcessor.getQueryProcessorForQuery(q, timeWindow, null, null);
            List<ComplexEvent> outputs = new List<ComplexEvent>();

            foreach (var input in inputs)
            {
                foreach (var output in p.processInputEvent(input,new DateTime()))
                {
                    outputs.Add(output);
                }
            }
            return outputs;
        }

        /// helper method for concise test cases
        protected List<ComplexEvent> getOutputListFromInputList(string querystring, List<AbstractEvent> inputs)
        {
            var irrelevantTimeWindow = TimeSpan.FromDays(1);
            return getOutputWithTimeWindow(querystring, inputs, irrelevantTimeWindow);
        }

        /// helper method for concise test cases
        protected List<ComplexEvent> getOutputListFromPrimitiveInputs(string querystring, string inputstring)
        {
            var inputEvents = createPrimitiveEvents(inputstring);
            return getOutputListFromInputList(querystring, inputEvents);
        }

        public PrimitiveEventGenerator[] getGeneratorsFromRateString(string rateString)
        {
            string names = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";

            int i = 0;

            var data = new PrimitiveEventGenerator[rateString.Split(" ").Count()];

            foreach (var rate in rateString.Split(" "))
            {
                data[i] = new PrimitiveEventGenerator(Int16.Parse(rate), TimeUnit.Second, new EventType(names[i].ToString()), null);
                i++;
            }

            return data;
        }

        public List<AbstractEvent> getGeneratedPrimitiveInputList(int[] rates, double duration)
        {
            var generators = getGeneratorsFromRateString(string.Join(" ", rates));

            var result = new long[generators.Count()];
            var data = new List<AbstractEvent>();

            var durationMS = duration * 1000;
            var stopwatch = new Stopwatch();
            stopwatch.Start();

            while (stopwatch.ElapsedMilliseconds < durationMS)
            {
                for (int generatorIndex = 0; generatorIndex < generators.Length; generatorIndex++)
                {
                    foreach (var primitive in generators[generatorIndex].generate())
                    {
                        data.Add(primitive);
                    }
                }
            }
            return data;
        }


        public long[] getPrimitiveCounts(int[] rates, double duration)
        {

            var generators = getGeneratorsFromRateString(string.Join(" ", rates));
            var generatorIndex = 0;
            var result = new long[generators.Count()];

            var durationMS = duration * 1000;
            var stopwatch = new Stopwatch();
            stopwatch.Start();

            while (stopwatch.ElapsedMilliseconds < durationMS)
            {
                generatorIndex = 0;
                foreach (var generator in generators)
                {
                    foreach (var primitive in generator.generate())
                    {
                        result[generatorIndex]++;
                    }
                    generatorIndex++;
                }

            }
            return result;
        }
    }
}
