using System.Reflection;
using DCEP.Core;
using DCEP.Node;
using Xunit;

namespace DCEP.Test
{
    public class SettingsTest
    {
        [Fact]
        public void test_defaultambrosiavalues(){
            var s = new AmbrosiaDCEPSettings();
            Assert.Equal(new NodeName("0"), s.directorNodeName);
        }
    }
}