using DCEP.Core;
using DCEP.Core.QueryProcessing.Operators;
using Xunit;

namespace DCEP.Test
{
    public class QueryComponentTests
    {
        [Fact]
        public void FindfirstChild_primitiveAND()
        {
            var qc = new ANDOperator("AND(A,B)");
            var fc = qc.getFirstOccuringChildOf(new EventType("A"), new EventType("B"));

            Assert.Equal(new EventType("A"), fc);
        }

        [Fact]
        public void FindfirstChild_primitiveAND_invertedargs()
        {
            var qc = new ANDOperator("AND(A,B)");
            var fc = qc.getFirstOccuringChildOf(new EventType("B"), new EventType("A"));

            Assert.Equal(new EventType("A"), fc);
        }

        [Fact]
        public void FindfirstChild_complex()
        {
            var qc = new ANDOperator("AND(B,SEQ(B,C), D)");
            var fc = qc.getFirstOccuringChildOf(new EventType("D"), new EventType("C"));

            Assert.Equal(new EventType("C"), fc);
        }
    }
}