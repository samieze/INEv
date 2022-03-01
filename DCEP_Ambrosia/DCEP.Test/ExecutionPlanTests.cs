using System;
using Xunit;
using DCEP;
using System.IO;
using DCEP.Core;
using System.Collections.Generic;
using System.Linq;

namespace DCEP.Test
{
    public class ExecutionPlanTests
    {

        [Fact]
        public void test_sampleA_nodecount()
        {
            ExecutionPlan executionPlan = new ExecutionPlan(new InputSamples().sampleA);
            Assert.Equal(5, executionPlan.networkPlan.Count);
        }

        [Fact]
        public void test_sampleA_processedAllQueries()
        {
            ExecutionPlan executionPlan = new ExecutionPlan(new InputSamples().sampleA);

            foreach (var item in executionPlan.wasQueryProcessed)
            {
                Assert.True(item.Value, "Query " + item.Key.ToString() + " was not processed.");
            }
        }

        [Fact]
        public void test_sampleA_HasForwardRules()
        {
            ExecutionPlan executionPlan = new ExecutionPlan(new InputSamples().sampleA);
            int count = 0;
            foreach (var item in executionPlan.forwardRulesByNodeName)
            {
                count += item.Value.Count;
            }
            Assert.True(count > 0);
        }

        [Fact]
        void test_sampleA_NoSelfForwarding()
        {
            ExecutionPlan executionPlan = new ExecutionPlan(new InputSamples().sampleA);

            foreach (var nodeDict in executionPlan.forwardRulesByNodeName)
            {
                foreach (var ruleItem in nodeDict.Value)
                {
                    foreach(var forwardRule in ruleItem.Value)
                    {
                        Assert.DoesNotContain(nodeDict.Key, forwardRule.destinations);
                    }
                }
            }
        }

        [Fact]
        void test_sampleA_SourceByNodeID()
        {
            ExecutionPlan executionPlan = new ExecutionPlan(new InputSamples().sampleA);

            var e0 = "B C D SEQ(A,B) SEQ(A,C) SEQ(B,D) SEQ(AND(B,C),D) SEQ(A,AND(B,C),D)".Split(' ');
            var e1 = "B C A SEQ(A,B) SEQ(A,C) SEQ(B,D) SEQ(AND(B,C),D) SEQ(A,AND(B,C),D)".Split(' ');
            var e2 = "B D A SEQ(A,B) SEQ(B,D)".Split(' ');
            var e3 = "C D SEQ(A,C) SEQ(AND(B,C),D)".Split(' ');
            var e4 = "D A".Split(' ');

            var expectedlist = new List<IEnumerable<string>>() { e0, e1, e2, e3, e4 };

            for (int i = 0; i < 5; i++)
            {
                List<string> actual = new List<string>();
                foreach (var item in executionPlan.sourceNodesByEventName)
                {
                    if (item.Value.Contains(new NodeName(i.ToString())))
                    {
                        actual.Add(item.Key.ToString());
                    }
                }
                Assert.Equal(expectedlist[i], actual);
            }
        }
        /*
        [Fact]
        void test_sampleA_ForwardRules()
        {
            ExecutionPlan executionPlan = new ExecutionPlan(new InputSamples().sampleA);

            var expectations = new List<(string, string, string)>(){
                ("0", "D", "1 2"),
                ("0", "SEQ(B,D)", "1 3"),
                ("0", "SEQ(A,B)", "1"),
                ("0", "SEQ(A,C)", "1"),
                ("1", "A", "0 2 3"),
                ("1", "SEQ(B,D)", "0 3"),
                ("1", "SEQ(A,B)", "0"),
                ("1", "SEQ(A,C)", "0"),
                ("2", "A", "0 1 3"),
                ("2", "D", "0 1"),
                ("2", "SEQ(B,D)", "0 1 3"),
                ("2", "SEQ(A,B)", "0 1"),
                ("3", "D", "0 1 2"),
                ("3", "SEQ(A,C)", "0 1"),
                ("3", "SEQ(AND(B,C),D)", "0"),
                ("4", "A","0 1 2 3"),
                ("4", "D","0 1 2")
            };

            var fr = executionPlan.forwardRulesByNodeName;

            foreach (var item in expectations)
            {

                Assert.Equal(item.Item3.Split(' ').Select(x => new NodeName(x)),
                fr[new NodeName(item.Item1)][new EventType(item.Item2)].destinations);
            }
        }*/


    }
}
