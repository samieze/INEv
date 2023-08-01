using System.Collections.Generic;
using DCEP;

namespace DCEP.Core
{

    class Attribute
    {
        public string key, value;

        public Attribute(string key, string value)
        {
            this.key = key;
            this.value = value;
        }

        public override bool Equals(object obj)
        {
            return obj is Attribute attribute &&
                   key == attribute.key &&
                   value == attribute.value;
        }

        public override int GetHashCode()
        {
            int hashCode = 1363396886;
            hashCode = hashCode * -1521134295 + EqualityComparer<string>.Default.GetHashCode(key);
            hashCode = hashCode * -1521134295 + EqualityComparer<string>.Default.GetHashCode(value);
            return hashCode;
        }
    }

}