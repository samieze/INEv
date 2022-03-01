using System.Numerics;
using System.Linq;
using System.Collections.Generic;
using System;
using System.Diagnostics;
using DCEP.Core;
using DCEP.Core.QueryProcessing;
using DCEP.Node;
using Xunit;

namespace DCEP.Test
{
    public class ComplexEventOutputRateTests : DCEPTestClass
    {
        /*
        [Fact]
        public void test_rate_AND_A_B_C_instantPrimitiveGeneration(){

            var primitiveGenerators = new PrimitiveEventGenerator[3] {
                new PrimitiveEventGenerator(100, TimeUnit.Second, new EventType("A")),
                new PrimitiveEventGenerator(100, TimeUnit.Second, new EventType("B")),
                new PrimitiveEventGenerator(100, TimeUnit.Second, new EventType("C"))
            };

            var stopwatch = new Stopwatch();

            var measurementTimeInMS = 10000;
            var timeWindow = measurementTimeInMS;

            var query = Query.createFromString("SELECT AND(A,B,C) FROM A,B,C ON n(X)");
            var queryProcessor = QueryProcessor.getQueryProcessorForQuery(query, TimeSpan.FromMilliseconds(timeWindow));

            stopwatch.Start();

            var complexCount = 0;
            var actualPrimitiveEventCount = 0;

            var primitiveCounts = new Dictionary<EventType, long>(){
                {new EventType("A"), 0},
                {new EventType("B"), 0},
                {new EventType("C"), 0}
            };

            var inputList = new List<AbstractEvent>(1000000);

            for (int i = 0; i < 100; i++)
            {
                inputList.Add(new PrimitiveEvent(new EventType("A")));
            }
            for (int i = 0; i < 100; i++)
            {
                inputList.Add(new PrimitiveEvent(new EventType("B")));
            }
            for (int i = 0; i < 100; i++)
            {
                inputList.Add(new PrimitiveEvent(new EventType("C")));
            }

            foreach (var primitiveEvent in inputList)
            {
                actualPrimitiveEventCount++;
                primitiveCounts[primitiveEvent.type]++;
                foreach (var outputEvent in queryProcessor.processInputEvent(primitiveEvent))
                {
                    complexCount++;
                }
            }


            var expectedComplexCount = primitiveCounts[new EventType("A")] * primitiveCounts[new EventType("B")] * primitiveCounts[new EventType("C")];

            Assert.Equal(expectedComplexCount, complexCount);
        }

        [Fact]
        public void test_rate_AND_A_B_C_realPrimitiveGeneration()
        {
            var rates = new int[]{100, 100, 100};
            var inputList = getGeneratedPrimitiveInputList(rates, 10);


            var timeWindow = 1000;
            var query = Query.createFromString("SELECT AND(A,B,C) FROM A,B,C ON n(X)");
            var queryProcessor = QueryProcessor.getQueryProcessorForQuery(query, TimeSpan.FromMilliseconds(timeWindow));


            var primitiveCounts = new Dictionary<EventType, long>(){
                {new EventType("A"), 0},
                {new EventType("B"), 0},
                {new EventType("C"), 0}
            };
            var complexCount = 0;
            var actualPrimitiveEventCount = 0;

            foreach (var primitiveEvent in inputList)
            {
                actualPrimitiveEventCount++;
                primitiveCounts[primitiveEvent.type]++;
                foreach (var outputEvent in queryProcessor.processInputEvent(primitiveEvent))
                {
                    complexCount++;
                }
            }


            var expectedComplexCount = primitiveCounts[new EventType("A")] * primitiveCounts[new EventType("B")] * primitiveCounts[new EventType("C")];

            Assert.Equal(expectedComplexCount, complexCount);
        }





        [Fact]
        public void test_rates_of_primitives_generation()
        {
            var primitiveGenerators = getGeneratorsFromRateString("100 100 100");

            var stopwatch = new Stopwatch();

            var measurementTimeInMS = 10000;
            var timeWindow = measurementTimeInMS;

            var query = Query.createFromString("SELECT AND(A,B,C) FROM A,B,C ON n(X)");
            var queryProcessor = QueryProcessor.getQueryProcessorForQuery(query, TimeSpan.FromMilliseconds(timeWindow));

            stopwatch.Start();

            var complexCount = 0;
            var actualPrimitiveEventCount = 0;

            var primitiveCounts = new Dictionary<EventType, long>(){
                {new EventType("A"), 0},
                {new EventType("B"), 0},
                {new EventType("C"), 0}
            };

            var inputList = new List<AbstractEvent>(1000000);

            for (int i = 0; i < 100; i++)
            {
                inputList.Add(new PrimitiveEvent(new EventType("A")));
            }
            for (int i = 0; i < 100; i++)
            {
                inputList.Add(new PrimitiveEvent(new EventType("B")));
            }
            for (int i = 0; i < 100; i++)
            {
                inputList.Add(new PrimitiveEvent(new EventType("C")));
            }

            foreach (var primitiveEvent in inputList)
            {
                actualPrimitiveEventCount++;
                primitiveCounts[primitiveEvent.type]++;
                foreach (var outputEvent in queryProcessor.processInputEvent(primitiveEvent))
                {
                    complexCount++;
                }
            }


            var expectedComplexCount = primitiveCounts[new EventType("A")] * primitiveCounts[new EventType("B")] * primitiveCounts[new EventType("C")];

            Assert.Equal(expectedComplexCount, complexCount);
        }
        */
    }
}
