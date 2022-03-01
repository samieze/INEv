using System.Collections.Generic;
using System.Diagnostics;

namespace DCEP.Core
{
    public class PlacementInfo
    {
        public NodeName singleNode = null;

        public HashSet<NodeName> selectedNodes = new HashSet<NodeName>();

        public NodeName selectedNodesForwardDestination = null;

        public EventType allSourcesOfEvent = null;



        public PlacementInfo()
        {

        }


        public PlacementInfo(string placementstring)
        {
            string remaining = placementstring;
            if (placementstring[0] == '{')
            {
                string specificNodesString = placementstring.Split('/')[0];

                var nodenamestrings = specificNodesString.TrimStart('{').TrimEnd('}').Split(',');

                if (nodenamestrings.Length == 1)
                {
                    singleNode = new NodeName(nodenamestrings[0]);
                }
                else
                {
                    foreach (var nodenamestring in nodenamestrings)
                    {
                        selectedNodes.Add(new NodeName(nodenamestring));

                        // set the first node added to the subset as the forward destination nodes not in the subset
                        if (selectedNodesForwardDestination == null)
                        {
                            selectedNodesForwardDestination = new NodeName(nodenamestring);
                        }
                    }
                }

                remaining = remaining.Substring(remaining.IndexOf("}") + 1);
            }



            if (remaining.StartsWith("/"))
            {
                remaining = TrimStart(remaining, "/");
                Debug.Assert(remaining.StartsWith("n("));
            }

            if (remaining.StartsWith("n("))
            {
                Debug.Assert(remaining.EndsWith(")"));

                remaining = TrimStart(remaining, "n(");
                // remove last ')' character of n()
                var eventNameString = remaining.Remove(remaining.Length - 1);
                allSourcesOfEvent = new EventType(eventNameString);
            }
        }

        public static string TrimStart(string target, string trimString)
        {
            if (string.IsNullOrEmpty(trimString)) return target;

            string result = target;
            while (result.StartsWith(trimString))
            {
                result = result.Substring(trimString.Length);
            }

            return result;
        }

        public static string TrimEnd(string target, string trimString)
        {
            if (string.IsNullOrEmpty(trimString)) return target;

            string result = target;
            while (result.EndsWith(trimString))
            {
                result = result.Substring(0, result.Length - trimString.Length);
            }

            return result;
        }


    }



}
