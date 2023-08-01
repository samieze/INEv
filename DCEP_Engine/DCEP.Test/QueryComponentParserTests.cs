using System.Linq;
using System;
using System.Reflection;

using DCEP.Core.QueryProcessing.Operators;
using Xunit;
using DCEP.Core.QueryProcessing;
using DCEP.Core;

namespace DCEP.Test
{
    public class QueryComponentParserTests
    {
        [Fact]
        public void test_illegalinput1()
        {
            QueryComponentParser parser = new QueryComponentParser();
            Assert.Throws<ArgumentException>(() =>
                parser.parse("SEEEQ(A,AND(B,C),D)")
            );

        }

        [Fact]
        public void test_illegalinput_emptybraces()
        {
            QueryComponentParser parser = new QueryComponentParser();
            Assert.ThrowsAny<TargetInvocationException>(() =>
                parser.parse("SEQ(A,AND(),D)")
            );

        }

        [Fact]
        public void test_primitiveAND()
        {
            QueryComponentParser parser = new QueryComponentParser();
            ANDOperator op = (ANDOperator)parser.parse("AND(B,C)");

            Assert.Equal(2, op.getChildren().Count());
            Assert.Equal(new EventType("B"), op.getChildren().ToList()[0]);
            Assert.Equal(new EventType("C"), op.getChildren().ToList()[1]);
        }

        [Fact]
        public void test_ANDWithoutBraces()
        {
            QueryComponentParser parser = new QueryComponentParser();

            Assert.Throws<TargetInvocationException>(() =>
                parser.parse("AND")
            );
        }


        [Fact]
        public void test_nestedAND()
        {
            QueryComponentParser parser = new QueryComponentParser();
            ANDOperator op = (ANDOperator)parser.parse("AND(AND(ABBA, D),C)");

            //var nestedExpected = new ANDOperator("AND(ABBA, D)");
            var nestedActualComponents = op.getChildren().ToList()[0].getChildren().ToList();


            Assert.Equal(2, op.getChildren().Count());

            Assert.IsType<ANDOperator>(op.getChildren().ToList()[0]);

            Assert.Equal(new EventType("C"), op.getChildren().ToList()[1]);

            Assert.Equal(new EventType("AND(ABBA, D)"), op.getChildren().ToList()[0].asEventType());

            Assert.Equal(new EventType("ABBA"), nestedActualComponents[0]);
            Assert.Equal(new EventType("D"), nestedActualComponents[1]);
        }

        [Fact]
        public void test_primitiveSEQ()
        {
            QueryComponentParser parser = new QueryComponentParser();
            SEQOperator op = (SEQOperator)parser.parse("SEQ(ABBA,ACDC)");

            Assert.Equal(2, op.getChildren().Count());
            Assert.Equal(new EventType("ABBA"), op.getChildren().ToList()[0]);
            Assert.Equal(new EventType("ACDC"), op.getChildren().ToList()[1]);
        }

    }
}