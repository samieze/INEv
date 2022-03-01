using System;
using System.Collections.Generic;
using System.Runtime.Serialization;

namespace DCEP.Core.QueryProcessing.Operators
{
    [DataContract]
    public class SEQOperator : MultiArgOperator
    {
        public SEQOperator(string input) : base(input)
        {
            if (!input.StartsWith("SEQ("))
            {
                throw new ArgumentException("SEQOperator requires SEQ prefix in input string: " + input);
            }
        }

    }
}