using System.Collections.Generic;

namespace DCEP.Core.Utils
{
    public interface ITreeNode<T>
    {
        T Value { get; }

        /// <summary>
        /// Gets the children.
        /// </summary>
        /// <value>The children.</value>
        IEnumerable<ITreeNode<T>> Children { get; }
    }
}