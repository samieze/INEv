using System;

namespace DCEP.Test
{
    public class InputSamples
    {

        public string[] sampleA { get; set; }
        public string[] sampleWithDataset { get; set; }
        public InputSamples()
        {
            string theText = @"0 10 50 5
1 10 50 0
1 10 0 5
0 0 50 5
1 0 0 5
-----------
Randomized Rate-Based Primitive Event Generation
-----------
SELECT SEQ(A,AND(B,C),D)    FROM SEQ(A,B),SEQ(A,C),SEQ(AND(B,C),D)  ON {0,1}/n(SEQ(AND(B,C),D)) WITH selectionRate=0.123
SELECT SEQ(A,B)             FROM A,B                                ON n(B) 
SELECT SEQ(A,C)             FROM A,C                                ON n(C)
SELECT SEQ(AND(B,C),D)      FROM SEQ(B,D),C                         ON n(C)
SELECT SEQ(B,D)             FROM B,D                                ON n(B)";
            sampleA = theText.Split(
                new[] { "\r\n", "\r", "\n" },
                StringSplitOptions.None
            );
            
            string sampleWithDatasetText = @"0 10 50 5
1 10 50 0
1 10 0 5
0 0 50 5
1 0 0 5
-----------
Dataset-Based Primitive Event Generation 
devdataA-%NodeName%.txt
-----------
SELECT SEQ(A,AND(B,C),D)    FROM SEQ(A,B),SEQ(A,C),SEQ(AND(B,C),D)  ON {0,1}/n(SEQ(AND(B,C),D)) WITH selectionRate=0.123
SELECT SEQ(A,B)             FROM A,B                                ON n(B) 
SELECT SEQ(A,C)             FROM A,C                                ON n(C)
SELECT SEQ(AND(B,C),D)      FROM SEQ(B,D),C                         ON n(C)
SELECT SEQ(B,D)             FROM B,D                                ON n(B)";
            sampleWithDataset = theText.Split(
                new[] { "\r\n", "\r", "\n" },
                StringSplitOptions.None
            );
        }
    }
}