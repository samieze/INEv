using System.Collections;
using System;
using System.Collections.Generic;
using System.Runtime.Serialization;

namespace DCEP.Core.QueryProcessing.Operators
{
    [DataContract]
    [KnownType(typeof(MultiArgOperator))]
    public abstract class AbstractQueryOperator : QueryComponent
    {
        protected QueryComponentParser parser = new QueryComponentParser();

        protected QueryComponent parseComponentString(string input)
        {
            return parser.parse(input);
        }


    }
}