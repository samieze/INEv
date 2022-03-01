using System;
using System.Collections.Generic;
using System.Collections.Immutable;
using System.Diagnostics.CodeAnalysis;
using DCEP.Core;
using DCEP.Core.QueryProcessing.Constraints;
using Xunit;

namespace DCEP.Test
{
    public class QueryProcessorUniqueComponentsTests
    {
        TimeSpan irrelevantTimeWindow = TimeSpan.FromDays(1);

        [Fact]
        public void test_QueryA_NoConstraints_C_after_B()
        {
            var p = new QueryProcessorUniqueComponents(Query.createFromString("[SEQ(AND(B,C),D),[B,C,D],n(X)]"), irrelevantTimeWindow, null, null);

            Assert.Empty(p.createPBCAnyMatchConstraints(new EventType("C"), new List<EventType>() { new EventType("B") }));
        }

        [Fact]
        public void test_QueryA_NoConstraints_B_after_C()
        {
            var p = new QueryProcessorUniqueComponents(Query.createFromString("[SEQ(AND(B,C),D),[B,C,D],n(X)]"), irrelevantTimeWindow, null, null);

            Assert.Empty(p.createPBCAnyMatchConstraints(new EventType("B"), new List<EventType>() { new EventType("C") }));
        }

        [Fact]
        public void test_QueryA_IsSuccConstraint_D_after_C()
        {
            var p = new QueryProcessorUniqueComponents(Query.createFromString("[SEQ(AND(B,C),D),[B,C,D],n(X)]"), irrelevantTimeWindow, null, null);
            var actual = p.createPBCAnyMatchConstraints(new EventType("D"), new List<EventType>() { new EventType("C") });

            Assert.Equal(1, actual.Count);
            Assert.IsType(typeof(SequenceConstraint), actual[0]);
            Assert.Equal(new EventType("C"), (actual[0] as SequenceConstraint).bufferType);
            Assert.Equal(SequenceType.IsSuccessor, (actual[0] as SequenceConstraint).sequenceType);
            Assert.Equal(new EventType("D"), (actual[0] as SequenceConstraint).candidateType);

        }

        [Fact]
        public void test_QueryA_IsPredConstraint_C_after_D()
        {
            var p = new QueryProcessorUniqueComponents(Query.createFromString("[SEQ(AND(B,C),D),[B,C,D],n(X)]"), irrelevantTimeWindow, null, null);
            var actual = p.createPBCAnyMatchConstraints(new EventType("C"), new List<EventType>() { new EventType("D") });

            Assert.Equal(1, actual.Count);
            Assert.IsType(typeof(SequenceConstraint), actual[0]);
            Assert.Equal(new EventType("D"), (actual[0] as SequenceConstraint).bufferType);
            Assert.Equal(SequenceType.IsPredecessor, (actual[0] as SequenceConstraint).sequenceType);
            Assert.Equal(new EventType("C"), (actual[0] as SequenceConstraint).candidateType);
        }

        [Fact]
        public void test_QueryB_C_after_SEQBD()
        {
            var p = new QueryProcessorUniqueComponents(Query.createFromString("[SEQ(AND(B,C), D),[SEQ(B,D),C],n(X)]"), irrelevantTimeWindow, null, null);

            var actual = p.createPBCAnyMatchConstraints(new EventType("C"), new List<EventType>() { new EventType("SEQ(B,D)") });

            Assert.Equal(1, actual.Count);
            Assert.IsType(typeof(SequenceConstraint), actual[0]);
            Assert.Equal(new EventType("D"), (actual[0] as SequenceConstraint).bufferType);
            Assert.Equal(SequenceType.IsPredecessor, (actual[0] as SequenceConstraint).sequenceType);
            Assert.Equal(new EventType("C"), (actual[0] as SequenceConstraint).candidateType);
        }

        [Fact]
        public void test_QueryB_SEQBD_after_C()
        {
            var p = new QueryProcessorUniqueComponents(Query.createFromString("[SEQ(AND(B,C), D),[SEQ(B,D),C],n(X)]"), irrelevantTimeWindow, null, null);

            var actual = p.createPBCAnyMatchConstraints(new EventType("SEQ(B,D)"), new List<EventType>() { new EventType("C") });

            Assert.Equal(1, actual.Count);
            Assert.IsType(typeof(SequenceConstraint), actual[0]);
            Assert.Equal(new EventType("C"), (actual[0] as SequenceConstraint).bufferType);
            Assert.Equal(SequenceType.IsSuccessor, (actual[0] as SequenceConstraint).sequenceType);
            Assert.Equal(new EventType("D"), (actual[0] as SequenceConstraint).candidateType);
        }
    }
}
