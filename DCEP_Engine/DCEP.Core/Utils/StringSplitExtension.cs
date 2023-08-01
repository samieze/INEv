using System;

namespace DCEP.Core.Utils
{
    public static class StringSplitExtension
    {
        public static string[] Split(this string str, string splitter)
        {
            return str.Split(new[] { splitter }, StringSplitOptions.None);
        }

        public static string TrimAllWhitespace(this string input)
        {
            return

             string.Join("", input.Split(new char[] { ' ', '\t' }));
        }
    }
}