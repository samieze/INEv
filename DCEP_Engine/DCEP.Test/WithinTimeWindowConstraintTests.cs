using System.Threading;
using System;
using System.Collections.Generic;
using System.ComponentModel;
using DCEP.Core;
using DCEP.Core.QueryProcessing;
using Xunit;

namespace DCEP.Test
{

    public class WithinTimeWindowConstraintTests : DCEPTestClass
    {

        [Fact]
        public void tosmalltimewindow_EmptyResult()
        {
            var inputs = createPrimitiveEvents("AA");
            Thread.Sleep(21);
            inputs.AddRange(createPrimitiveEvents("BB"));

            var outputs = getOutputWithTimeWindow("[AND(A,B),[A,B],n(B)]", inputs, TimeSpan.FromMilliseconds(20));
            Assert.Empty(outputs);
        }

        [Fact]
        public void timewindow_WithResult()
        {
            var inputs = createPrimitiveEvents("AA");
            inputs.AddRange(createPrimitiveEvents("BB"));

            var outputs = getOutputWithTimeWindow("[AND(A,B),[A,B],n(B)]", inputs, TimeSpan.FromMilliseconds(20));
            Assert.NotEmpty(outputs);
        }


    }
}