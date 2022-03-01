using System;
using System.Runtime.Serialization;

namespace DCEP.Core.QueryProcessing.Operators
{
    [DataContract]
    public class ANDOperator : MultiArgOperator
    {

        public ANDOperator(string input) : base(input)
        {
            if (!input.StartsWith("AND("))
            {
                throw new ArgumentException("ANDOperator requires AND prefix in input string: " + input);
            }
        }
    }
}