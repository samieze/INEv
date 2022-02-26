// "LeastCommonAncestor.zip" from the article Solving LCA by Reducing to RMQ in C#. Governed by the The Code Project Open License (CPOL). 
// https://www.codeproject.com/Articles/141999/Solving-LCA-by-Reducing-to-RMQ-in-C

using System;
using System.Collections.Generic;
using System.Text;
using System.Diagnostics;
using System.Runtime.Serialization;

namespace DCEP.Core.Utils.LeastCommonAncestor
{
    [DataContract]
    /// <summary>
    /// Helps find the least common ancestor in a graph 
    /// </summary>
    /// <typeparam name="T"></typeparam>
    public class LeastCommonAncestorFinder<T>
    {
        [DataMember]
        private ITreeNode<T> _rootNode;
        [DataMember]
        private Dictionary<ITreeNode<T>, NodeIndex> _indexLookup = new Dictionary<ITreeNode<T>, NodeIndex>(); // n or so
        [DataMember]
        private List<ITreeNode<T>> _nodes = new List<ITreeNode<T>>();  // n
        [DataMember]
        private List<int> _values = new List<int>(); // n * 2

        /// <summary>
        /// Initializes a new instance of the <see cref="LeastCommonAncestorFinder&lt;T&gt;"/> class.
        /// </summary>
        /// <param name="rootNode">The root node.</param>
        public LeastCommonAncestorFinder(ITreeNode<T> rootNode)
        {
            if (rootNode == null)
            {
                throw new NotImplementedException("rootNode");
            }
            _rootNode = rootNode;
            PreProcess();
        }

        /// <summary>
        /// Finds the common parent between two nodes.
        /// </summary>
        /// <param name="x">The x.</param>
        /// <param name="y">The y.</param>
        /// <returns></returns>
        public ITreeNode<T> FindCommonParent(ITreeNode<T> x, ITreeNode<T> y)
        {
            // Find the first time the nodes were visited during preprocessing.
            NodeIndex nodeIndex;
            int indexX, indexY;
            if (!_indexLookup.TryGetValue(x, out nodeIndex))
            {
                throw new ArgumentException("The x node was not found in the graph.");
            }
            indexX = nodeIndex.FirstVisit;
            if (!_indexLookup.TryGetValue(y, out nodeIndex))
            {
                throw new ArgumentException("The y node was not found in the graph.");
            }
            indexY = nodeIndex.FirstVisit;

            // Adjust so X is less than Y
            int temp;
            if (indexY < indexX)
            {
                temp = indexX;
                indexX = indexY;
                indexY = temp;

            }

            // Find the lowest value.
            temp = int.MaxValue;
            for (int i = indexX; i < indexY; i++)
            {
                if (_values[i] < temp)
                {
                    temp = _values[i];
                }
            }
            return _nodes[temp];
        }

        private void PreProcess()
        {
            // Eulerian path visit of graph 
            Stack<ProcessingState> lastNodeStack = new Stack<ProcessingState>();
            ProcessingState current = new ProcessingState(_rootNode);
            ITreeNode<T> next;
            lastNodeStack.Push(current);

            NodeIndex nodeIndex;
            int valueIndex;
            while (lastNodeStack.Count != 0)
            {
                current = lastNodeStack.Pop();
                if (!_indexLookup.TryGetValue(current.Value, out nodeIndex))
                {
                    valueIndex = _nodes.Count;
                    _nodes.Add(current.Value);
                    _indexLookup[current.Value] = new NodeIndex(_values.Count, valueIndex);
                }
                else
                {
                    valueIndex = nodeIndex.LookupIndex;
                }
                _values.Add(valueIndex);

                // If there is a next then push the current value on to the stack along with 
                // the current value.
                if (current.Next(out next))
                {
                    lastNodeStack.Push(current);
                    lastNodeStack.Push(new ProcessingState(next));
                }
            }
            _nodes.TrimExcess();
            _values.TrimExcess();
        }
        [DataContract]
        private class ProcessingState
        {
            [DataMember]
            private IEnumerator<ITreeNode<T>> _enumerator;

            /// <summary>
            /// Initializes a new instance of the <see cref="LeastCommonAncestorFinder&lt;T&gt;.ProcessingState"/> class.
            /// </summary>
            /// <param name="value">The value.</param>
            public ProcessingState(ITreeNode<T> value)
            {
                Value = value;
                _enumerator = value.Children.GetEnumerator();
            }

            /// <summary>
            /// Gets the node.
            /// </summary>
            /// <value>The value.</value>
            [DataMember]
            public ITreeNode<T> Value { get; private set; }

            /// <summary>
            /// Gets the next child.
            /// </summary>
            /// <param name="value">The value.</param>
            /// <returns></returns>
            public bool Next(out ITreeNode<T> value)
            {
                if (_enumerator.MoveNext())
                {
                    value = _enumerator.Current;
                    return true;
                }
                value = null;
                return false;
            }
        }
        [DataContract]
        private struct NodeIndex
        {
            [DataMember]
            public readonly int FirstVisit;
            [DataMember]
            public readonly int LookupIndex;

            public NodeIndex(int firstVisit, int lookupIndex)
            {
                FirstVisit = firstVisit;
                LookupIndex = lookupIndex;
            }
        }
    }
}
