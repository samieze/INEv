using System;
using System.Linq;
using System.Collections.Generic;
using System.Text.RegularExpressions;
using DCEP.Core.QueryProcessing;
using Xunit;
using DCEP.Core;

namespace DCEP.Test
{
    public class QueryProcessorTests : DCEPTestClass
    {


        [Fact]
        public void testPrimitiveSEQExample()
        {
            var outputs = getOutputListFromPrimitiveInputs("[SEQ(A,B),[A,B],n(B)]", "AABBAB");
            Assert.Equal(7, outputs.Count);
        }

        [Fact]
        public void testPrimitiveANDExample()
        {
            var outputs = getOutputListFromPrimitiveInputs("[AND(A,B),[A,B],n(B)]", "AABBAB");
            Assert.Equal(9, outputs.Count);
        }

        [Fact]
        public void testPrimitiveANDExample_ComplexEventChildrenComplete()
        {
            var outputs = getOutputListFromPrimitiveInputs("[AND(A,B),[A,B],n(B)]", "AB");

            Assert.Equal(1, outputs.Count);
            Assert.Equal(2, outputs[0].children.ToList().Count);
        }

        [Fact]
        public void testPrimitiveSEQExample_ComplexEventChildrenComplete()
        {
            var outputs = getOutputListFromPrimitiveInputs("[SEQ(A,B),[A,B],n(B)]", "AB");

            Assert.Equal(1, outputs.Count);
            Assert.Equal(2, outputs[0].children.ToList().Count);
        }

        [Fact]
        public void testQueryB_EventCount_ShortSequence()
        {
            var inputs = new List<AbstractEvent>(){
                new PrimitiveEvent("C",null)
            };

            var seqbds = getOutputListFromPrimitiveInputs("[SEQ(B,D),[B,D],n(B)]", "BD");
            Assert.Equal(1, seqbds.Count);
            inputs.AddRange(seqbds);

            inputs.AddRange(createPrimitiveEvents("CCC"));

            var outputs = getOutputListFromInputList("[SEQ(AND(B,C), D),[SEQ(B,D),C],n(X)]", inputs);

            Assert.Equal(1, outputs.Count);
        }

        [Fact]
        public void testQueryB_EventCount_LongerSequence()
        {
            var inputs = new List<AbstractEvent>(){
                new PrimitiveEvent("C", null)
            };

            var seqbds = getOutputListFromPrimitiveInputs("[SEQ(B,D),[B,D],n(B)]", "BDD");
            Assert.Equal(2, seqbds.Count);
            inputs.AddRange(seqbds);

            inputs.AddRange(createPrimitiveEvents("CCC"));

            var outputs = getOutputListFromInputList("[SEQ(AND(B,C), D),[SEQ(B,D),C],n(X)]", inputs);

            Assert.Equal(2, outputs.Count);
        }

        [Fact]
        public void test_complexquery_duplicateimputprimitives_unequalIDs_NoMatches()
        {
            var inputs = new List<AbstractEvent>();
            var seqabs = getOutputListFromPrimitiveInputs("[SEQ(A,B),[A,B],n(B)]", "AAB");
            Assert.Equal(2, seqabs.Count);
            inputs.AddRange(seqabs);

            var seqacs = getOutputListFromPrimitiveInputs("[SEQ(A,C),[A,C],n(B)]", "AAC");
            Assert.Equal(2, seqacs.Count);
            inputs.AddRange(seqacs);

            var seqandbcdsinputs = new List<AbstractEvent>();
            seqandbcdsinputs.AddRange(createPrimitiveEvents("CC"));
            var seqbds = getOutputListFromPrimitiveInputs("[SEQ(B,D),[B,D],n(B)]", "BDD");
            Assert.Equal(2, seqbds.Count);
            seqandbcdsinputs.AddRange(seqbds);
            var seqandbcds = getOutputListFromInputList("[SEQ(AND(B,C), D),[SEQ(B,D),C],n(X)]", seqandbcdsinputs);
            Assert.Equal(4, seqandbcds.Count);
            inputs.AddRange(seqandbcds);

            var outputs = getOutputListFromInputList("[SEQ(A,AND(B,C),D),[SEQ(A,B),SEQ(A,C),SEQ(AND(B,C),D)],n(X))]", inputs);

            Assert.Equal(0, outputs.Count);
        }

        [Fact]
        public void test_complexquery_duplicateimputprimitives_unequalIDs_NoMatchesDespiteSameAs()
        {
            var inputs = new List<AbstractEvent>();

            var sameAs = createPrimitiveEvents("AA");

            var seqabinputs = new List<AbstractEvent>(sameAs);
            seqabinputs.AddRange(createPrimitiveEvents("AB"));
            var seqabs = getOutputListFromInputList("[SEQ(A,B),[A,B],n(B)]", seqabinputs);
            Assert.Equal(3, seqabs.Count);
            inputs.AddRange(seqabs);

            var seqacinputs = new List<AbstractEvent>(sameAs);
            seqacinputs.AddRange(createPrimitiveEvents("AC"));
            var seqacs = getOutputListFromInputList("[SEQ(A,C),[A,C],n(B)]", seqacinputs);
            Assert.Equal(3, seqacs.Count);
            inputs.AddRange(seqacs);

            var seqandbcdsinputs = new List<AbstractEvent>();
            seqandbcdsinputs.AddRange(createPrimitiveEvents("CC"));
            var seqbds = getOutputListFromPrimitiveInputs("[SEQ(B,D),[B,D],n(B)]", "BDD");
            Assert.Equal(2, seqbds.Count);
            seqandbcdsinputs.AddRange(seqbds);
            var seqandbcds = getOutputListFromInputList("[SEQ(AND(B,C), D),[SEQ(B,D),C],n(X)]", seqandbcdsinputs);
            Assert.Equal(4, seqandbcds.Count);
            inputs.AddRange(seqandbcds);

            var outputs = getOutputListFromInputList("[SEQ(A,AND(B,C),D),[SEQ(A,B),SEQ(A,C),SEQ(AND(B,C),D)],n(X))]", inputs);

            Assert.Equal(0, outputs.Count);
        }

        [Fact]
        public void test_complexquery_duplicateimputprimitives_unequalIDs_Matches()
        {
            var inputs = new List<AbstractEvent>();

            var sameAs = createPrimitiveEvents("AA");
            var sameB = new PrimitiveEvent("B",null);
            var sameC = new PrimitiveEvent("C",null);

            var seqabinputs = new List<AbstractEvent>(sameAs);
            seqabinputs.AddRange(createPrimitiveEvents("AB"));
            seqabinputs.Add(sameB);
            var seqabs = getOutputListFromInputList("[SEQ(A,B),[A,B],n(B)]", seqabinputs);
            Assert.Equal(5, seqabs.Count); // 5x SEQ(A,B), only 2x with sameA and sameB should match later
            inputs.AddRange(seqabs);

            var seqacinputs = new List<AbstractEvent>(sameAs);
            seqacinputs.AddRange(createPrimitiveEvents("AC"));
            seqacinputs.Add(sameC);
            var seqacs = getOutputListFromInputList("[SEQ(A,C),[A,C],n(B)]", seqacinputs);
            Assert.Equal(5, seqacs.Count); // 5x SEQ(A,C), only 2x with sameA and sameC should match later
            inputs.AddRange(seqacs);

            var seqandbcdsinputs = new List<AbstractEvent>();
            seqandbcdsinputs.AddRange(createPrimitiveEvents("C"));
            seqandbcdsinputs.Add(sameC);

            var seqbdinputs = new List<AbstractEvent>() { sameB };
            seqbdinputs.AddRange(createPrimitiveEvents("BDD"));
            var seqbds = getOutputListFromInputList("[SEQ(B,D),[B,D],n(B)]", seqbdinputs);
            Assert.Equal(4, seqbds.Count); // 4x SEQ(B,D), only 2x with sameB should match later
            seqandbcdsinputs.AddRange(seqbds);
            var seqandbcds = getOutputListFromInputList("[SEQ(AND(B,C), D),[SEQ(B,D),C],n(X)]", seqandbcdsinputs);
            Assert.Equal(8, seqandbcds.Count); // 8x SEQ(AND(B,C), D), only 2x with sameC and sameB should match later
            inputs.AddRange(seqandbcds);

            var outputs = getOutputListFromInputList("[SEQ(A,AND(B,C),D),[SEQ(A,B),SEQ(A,C),SEQ(AND(B,C),D)],n(X))]", inputs);

            Assert.Equal(4, outputs.Count);
        }

        [Fact]
        public void test_complexquery_duplicateimputprimitives_onlyequalIDs_Matches()
        {
            var inputs = new List<AbstractEvent>();

            var sameAs = createPrimitiveEvents("A");
            var sameB = new PrimitiveEvent("B",null);
            var sameC = new PrimitiveEvent("C",null);

            var seqabinputs = new List<AbstractEvent>(sameAs);
            seqabinputs.Add(sameB);
            var seqabs = getOutputListFromInputList("[SEQ(A,B),[A,B],n(B)]", seqabinputs);
            Assert.Equal(1, seqabs.Count);
            inputs.AddRange(seqabs);

            var seqacinputs = new List<AbstractEvent>(sameAs);
            seqacinputs.Add(sameC);
            var seqacs = getOutputListFromInputList("[SEQ(A,C),[A,C],n(B)]", seqacinputs);
            Assert.Equal(1, seqacs.Count);
            inputs.AddRange(seqacs);

            var seqandbcdsinputs = new List<AbstractEvent>();
            seqandbcdsinputs.Add(sameC);

            var seqbdinputs = new List<AbstractEvent>() { sameB };
            seqbdinputs.AddRange(createPrimitiveEvents("D"));
            var seqbds = getOutputListFromInputList("[SEQ(B,D),[B,D],n(B)]", seqbdinputs);
            Assert.Equal(1, seqbds.Count); // 4x SEQ(B,D), only 2x with sameB should match later
            seqandbcdsinputs.AddRange(seqbds);
            var seqandbcds = getOutputListFromInputList("[SEQ(AND(B,C), D),[SEQ(B,D),C],n(X)]", seqandbcdsinputs);
            Assert.Equal(1, seqandbcds.Count);
            inputs.AddRange(seqandbcds);

            var outputs = getOutputListFromInputList("[SEQ(A,AND(B,C),D),[SEQ(A,B),SEQ(A,C),SEQ(AND(B,C),D)],n(X))]", inputs);

            Assert.Equal(1, outputs.Count);
        }
    }
}
