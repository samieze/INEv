using System;
using System.Collections.Generic;
using System.Runtime.Serialization;

namespace DCEP.Node.Benchmarking
{
    [DataContract]
    public struct BenchmarkRecord
    {
        [DataMember]
        public double eventTimeLatency { get; set; }

        [DataMember]
        public double processingTimeLatency { get; set; }

        [DataMember]
        public double processedInputEvents { get; set; }
        
        [DataMember]
        public double complexMatchesBeforeDropout { get; set;  }

        [DataMember]
        public double complexMatchesAfterDropout { get; set; }

        //public IList<Tuple<string, double>> complexTuples { get; set; }

        
    }
}