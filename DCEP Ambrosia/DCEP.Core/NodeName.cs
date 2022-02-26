using System;
using System.Runtime.Serialization;
using DCEP;

namespace DCEP.Core
{
    [DataContract]
    public class NodeName
    {
        [DataMember]
        string name { get; set; }

        public NodeName(string name)
        {
            this.name = name;
        }

        public override bool Equals(object obj)
        {
            return obj is NodeName name &&
                   this.name.Equals(name.name);
        }

        public override string ToString()
        {
            return this.name.ToString();
        }

        public override int GetHashCode()
        {
            return this.name.GetHashCode();
        }
    }
}