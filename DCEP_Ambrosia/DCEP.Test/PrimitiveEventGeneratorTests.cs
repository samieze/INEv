using System.Globalization;
using System;
using System.Diagnostics;
using DCEP.Core;
using DCEP.Core.Utils.PoissonEvaluator;
using DCEP.Node;
using Xunit;
using System.Collections.Generic;
using System.Linq;

namespace DCEP.Test
{
    public class PrimitiveEventGeneratorTests : DCEPTestClass
    {
        [Fact]
        public void test_actual_rate_in_range()
        {
            var seconds = 2;
            var eventsPerInterval = 100000;
            var g = new PrimitiveEventGenerator(eventsPerInterval, TimeUnit.Second, new EventType("T"), null);
            var sw = new Stopwatch();
            long count = 0;
            sw.Start();
            while (sw.ElapsedMilliseconds < seconds * 1000)
            {
                count += g.generate().Length;
            }

            Assert.InRange(count / (float)(seconds * eventsPerInterval), 0.999, 1.001);
        }

        [Fact]
        public void test_low_rate_in_range()
        {
            var seconds = 2;
            var eventsPerInterval = 1;
            var g = new PrimitiveEventGenerator(eventsPerInterval, TimeUnit.Second, new EventType("T"), null);
            var sw = new Stopwatch();
            long count = 0;
            sw.Start();
            while (sw.ElapsedMilliseconds < seconds * 1000)
            {
                count += g.generate().Length;
            }

            Assert.InRange(count / (float)(seconds * eventsPerInterval), 0.999, 1.001);
        }

        [Fact]
        public void test_longer_duration_more_events()
        {
            var seconds = 2;
            var eventsPerInterval = 100000;
            var g = new PrimitiveEventGenerator(eventsPerInterval, TimeUnit.Second, new EventType("T"), null);
            var sw = new Stopwatch();
            long count = 0;
            sw.Start();
            while (sw.ElapsedMilliseconds < (seconds + 1) * 1000)
            {
                count += g.generate().Length;
            }


            var actualratio = count / (float)((seconds) * eventsPerInterval);
            Assert.NotInRange(actualratio, 0.999, 1.001);
            Assert.True(actualratio > 1.0);
        }


        [Fact]
        public void test_shorter_duration_fewer_events()
        {
            var seconds = 2;
            var eventsPerInterval = 100000;
            var g = new PrimitiveEventGenerator(eventsPerInterval, TimeUnit.Second, new EventType("T"), null);
            var sw = new Stopwatch();
            long count = 0;
            sw.Start();
            while (sw.ElapsedMilliseconds < (seconds - 1) * 1000)
            {
                count += g.generate().Length;
            }

            var actualratio = count / (float)(seconds * eventsPerInterval);
            Assert.NotInRange(actualratio, 0.999, 1.001);
            Assert.True(actualratio < 1.0);
        }

        [Fact]
        public void parallel_generation(){
            var duration = 10.0; 
            var rates = new int[] {100, 200, 500, 30};
            var x = getPrimitiveCounts(rates, duration);

            for (int i = 0; i < rates.Length; i++)
            {
                var ratio = x[i] / (rates[i] * duration);
                Assert.InRange(ratio, 0.99, 1.01);   
            }

        }

        [Fact]

        public void parallel_generation_saveddata()
        {
            var duration = 10.0;
            var rates = new int[] { 100, 100, 100 };
            var x = getPrimitiveCounts(rates, duration);

            var data = getGeneratedPrimitiveInputList(rates, duration);

            var actual = new int[] {0, 0, 0};

            foreach (var e in data)
            {
                switch (e.type.ToString())
                {
                    case "A":
                        actual[0]++;
                    break;
                    case "B":
                    actual[1]++;
                    break;
                    case "C":
                    actual[2]++;
                    break;
                }
            }


            for (int i = 0; i < rates.Length; i++)
            {
                var ratio = actual[i] / (rates[i] * duration);
                Assert.InRange(ratio, 0.99, 1.01);
            }


        }
    }
}
