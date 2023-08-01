using System.Linq;
using DCEP.Core;
using Xunit;

namespace DCEP.Test
{
    public class QueryParsingTests
    {
        [Fact]
        public void selectionRate_realvalue()
        {
            var q = Query.createFromString("SELECT SEQ(A,AND(B,C),D)    FROM SEQ(A,B),SEQ(A,C),SEQ(AND(B,C),D)  ON {0,1}/n(SEQ(AND(B,C),D)) WITH selectionRate=0.123");
            Assert.Equal(0.123d, q.selectionRate);
        }

        [Fact]
        public void selectionRate_realvalue_spacedout()
        {
            var q = Query.createFromString("SELECT SEQ(A,AND(B,C),D)    FROM SEQ(A,B),SEQ(A,C),SEQ(AND(B,C),D)  ON {0,1}/n(SEQ(AND(B,C),D)) WITH selectionRate = 0.123");
            Assert.Equal(0.123d, q.selectionRate);
        }

        [Fact]
        public void selectionRate_novalue()
        {
            var q = Query.createFromString("SELECT SEQ(A,AND(B,C),D)    FROM SEQ(A,B),SEQ(A,C),SEQ(AND(B,C),D)  ON {0,1}/n(SEQ(AND(B,C),D))");
            Assert.Equal(1.0d, q.selectionRate);
        }

        [Fact]
        public void selectionRate_novalue_emptywith()
        {
            var q = Query.createFromString("SELECT SEQ(A,AND(B,C),D)    FROM SEQ(A,B),SEQ(A,C),SEQ(AND(B,C),D)  ON {0,1}/n(SEQ(AND(B,C),D)) WITH");
            Assert.Equal(1.0d, q.selectionRate);
        }

        [Fact]
        public void selectionRate_novalue_WithSpam()
        {
            var q = Query.createFromString("SELECT SEQ(A,AND(B,C),D)    FROM SEQ(A,B),SEQ(A,C),SEQ(AND(B,C),D)  ON {0,1}/n(SEQ(AND(B,C),D)) WITH abc=xyz");
            Assert.Equal(1.0d, q.selectionRate);
        }


        [Fact]
        public void selectionRate_whitespacetesting()
        {
            var q = Query.createFromString("SELECT SEQ(E,AND(D,C,F))   FROM SEQ(E,AND(C,F)),D 		  ON n(D) WITH selectionRate=0.0000001 ");
            Assert.Equal(new EventType("D"), q.inputEvents.ToList()[1]);
        }



    }
}