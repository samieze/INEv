using System.Reflection;
using DCEP.Core;
using Xunit;

namespace DCEP.Test
{
    public class PlacementInfoTests
    {
        [Fact]
        public void test_placementparsing_selectednodes()
        {
            PlacementInfo p = new PlacementInfo("{0,1}/n(SEQ(AND(B,C),D))");
            Assert.Equal(new EventType("SEQ(AND(B,C),D)"), p.allSourcesOfEvent);
            Assert.Equal(2, p.selectedNodes.Count);
            Assert.Contains(new NodeName("0"), p.selectedNodes);
            Assert.Contains(new NodeName("1"), p.selectedNodes);
            Assert.Null(p.singleNode);
        }

        [Fact]
        public void test_placementparsing_singlenode()
        {
            PlacementInfo p = new PlacementInfo("{0}");
            Assert.Empty(p.selectedNodes);
            Assert.Equal(new NodeName("0"), p.singleNode);
            Assert.Null(p.allSourcesOfEvent);
        }


        [Fact]
        public void test_placementparsing_allEventSourceNodes()
        {
            PlacementInfo p = new PlacementInfo("n(XYZn)");
            Assert.Empty(p.selectedNodes);
            Assert.Equal(new EventType("XYZn"), p.allSourcesOfEvent);
            Assert.Null(p.singleNode);
        }
    }
}