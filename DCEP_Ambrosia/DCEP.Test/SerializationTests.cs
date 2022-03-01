using System.Threading;
using System;
using System.IO;
using System.Runtime.Serialization;
using System.Xml;
using DCEP.Core;
using DCEP.Node;
using Xunit;

namespace DCEP.Test
{
    public class SerializationTests
    {

        [Fact]
        public void test_DCEPNodeInstantiation_SampleA()
        {
            ExecutionPlan executionPlan = new ExecutionPlan(new InputSamples().sampleA);

            foreach (var item in executionPlan.networkPlan)
            {
                var node = new DCEPNode(item.Key, new InputSamples().sampleA, new DCEPSettings());
            }
        }


        [Fact]
        public void test_isNodeSerializable()
        {
            var testenv = new TestEnvorioment(new InputSamples().sampleA, new DCEPSettings() );
            foreach (var item in testenv.nodedict)
            {
               item.Value.onFirstStart(testenv); 
            }

            Thread.Sleep(500);

            foreach (var item in testenv.nodedict)
            {
                string serialized = dataContractSerializeObject(item.Value);
            }

            testenv.terminateAll();

        }

        public static string dataContractSerializeObject<T>(T objectToSerialize)
        {
            using (var output = new StringWriter())
            using (var writer = new XmlTextWriter(output) { Formatting = Formatting.Indented })
            {
                new DataContractSerializer(typeof(T)).WriteObject(writer, objectToSerialize);
                return output.GetStringBuilder().ToString();
            }
        }

        public static T dataContractDeserializeObject<T>(string stringToDeserialize)
        {
            using (var input = new StringReader(stringToDeserialize))
            using (var reader = new XmlTextReader(input))
            {
                T node = (T)new DataContractSerializer(typeof(T)).ReadObject(reader);
                return node;
            }
        }

        [Fact]
        public void test_isNodeDeserializable()
        {

            var testenv = new TestEnvorioment(new InputSamples().sampleA, new DCEPSettings());
            foreach (var item in testenv.nodedict)
            {
                item.Value.onFirstStart(testenv);
            }

            Thread.Sleep(500);

            foreach (var item in testenv.nodedict)
            {
                string serialized = dataContractSerializeObject(item.Value);
                Console.WriteLine(serialized);
                var node2 = dataContractDeserializeObject<DCEPNode>(serialized);
                Assert.NotNull(node2);
            }

            testenv.terminateAll();
        }
    }


}