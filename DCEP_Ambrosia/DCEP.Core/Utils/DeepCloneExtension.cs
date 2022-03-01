using System.Runtime.Serialization.Formatters.Binary;
using System.IO;
using System.Xml;
using System.Runtime.Serialization;

namespace DCEP.Core.Utils.DeepCloneExtension
{
    public static class DeepCloneExtension
    {
        // Deep clone
        public static T DeepClone<T>(this T a)
        {
            using (MemoryStream stream = new MemoryStream())
            {
                return dataContractDeserializeObject<T>(dataContractSerializeObject<T>(a));
            }
        }

        public static string dataContractSerializeObject<T>(T objectToSerialize)
        {
            using (var output = new StringWriter())
            using (var writer = new XmlTextWriter(output) { Formatting = Formatting.Indented })
            {
                new DataContractSerializer(typeof(T)).WriteObject(writer, objectToSerialize);
                return output.GetStringBuilder().ToString();
            }
        }

        public static T dataContractDeserializeObject<T>(string stringToDeserialize)
        {
            using (var input = new StringReader(stringToDeserialize))
            using (var reader = new XmlTextReader(input))
            {
                T node = (T)new DataContractSerializer(typeof(T)).ReadObject(reader);
                return node;
            }
        }
    }
}