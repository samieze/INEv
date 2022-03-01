using System.Collections.Generic;
using DCEP.Core;
using DCEP.Core.QueryProcessing.Constraints;
using Xunit;

namespace DCEP.Test
{
    public class EqualIDWhenEqualEventTypeConstraintTests : DCEPTestClass
    {
        [Fact]
        public void test_constraint_satisfied()
        {
            var sameAs = createPrimitiveEvents("A");

            var seqabinputs = new List<AbstractEvent>(sameAs);
            seqabinputs.Add(new PrimitiveEvent("B", null));
            var seqabs = getOutputListFromInputList("[SEQ(A,B),[A,B],n(B)]", seqabinputs);
            Assert.Equal(1, seqabs.Count);

            var seqacinputs = new List<AbstractEvent>(sameAs);
            seqacinputs.Add(new PrimitiveEvent("C", null));
            var seqacs = getOutputListFromInputList("[SEQ(A,C),[A,C],n(B)]", seqacinputs);
            Assert.Equal(1, seqacs.Count);

            var c = new EqualIDWhenEqualEventTypeConstraint(new EventType("A"));
            Assert.True(PrimitiveBufferComponentAnyMatchConstraint.checkAll(new List<PrimitiveBufferComponentAnyMatchConstraint>() { c }, seqacs[0], seqabs));
            Assert.True(PrimitiveBufferComponentAnyMatchConstraint.checkAll(new List<PrimitiveBufferComponentAnyMatchConstraint>() { c }, seqabs[0], seqacs));
        }

        [Fact]
        public void test_constraint_unsatisfied()
        {
            var seqabinputs = new List<AbstractEvent>(createPrimitiveEvents("A"));
            seqabinputs.Add(new PrimitiveEvent("B", null));
            var seqabs = getOutputListFromInputList("[SEQ(A,B),[A,B],n(B)]", seqabinputs);
            Assert.Equal(1, seqabs.Count);

            var seqacinputs = new List<AbstractEvent>(createPrimitiveEvents("A"));
            seqacinputs.Add(new PrimitiveEvent("C", null));
            var seqacs = getOutputListFromInputList("[SEQ(A,C),[A,C],n(B)]", seqacinputs);
            Assert.Equal(1, seqacs.Count);

            var c = new EqualIDWhenEqualEventTypeConstraint(new EventType("A"));
            Assert.False(PrimitiveBufferComponentAnyMatchConstraint.checkAll(new List<PrimitiveBufferComponentAnyMatchConstraint>() { c }, seqacs[0], seqabs));
            Assert.False(PrimitiveBufferComponentAnyMatchConstraint.checkAll(new List<PrimitiveBufferComponentAnyMatchConstraint>() { c }, seqabs[0], seqacs));
        }
    }
}
