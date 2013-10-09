import networkx
import numpy

from ..util import log

__all__ = ["rooted_pagerank", "simrank"]


def rooted_pagerank(G, root, alpha=0.85, beta=0, weight='weight'):
    """Return the rooted PageRank of all nodes with respect to node `root`.

    Parameters
    ----------

    G : a networkx.(Di)Graph
        network to compute PR on

    root : a node from the network
        the node that will be the starting point of all random walks

    alpha : float
        PageRank probability that we will advance to a neighbour of the
        current node in a random walk

    beta : float or int
        Normally, we return to the root node with probability 1 - alpha.
        With this parameter, we can also advance to a random other node in the
        network with probability beta. Thus, we get back to the root node with
        probability 1 - alpha - beta. This is off (0) by default.

    weight : string or None
        The edge attribute that holds the numerical value used for
        the edge weight.  If None then treat as unweighted.

    """
    personalization = dict.fromkeys(G, beta)
    personalization[root] = 1 - beta

    return networkx.pagerank_scipy(G, alpha, personalization, weight=weight)


def simrank(G, nodelist=None, c=0.8, num_iterations=10, weight='weight'):
    r"""Calculate SimRank matrix for nodes in nodelist

    SimRank is defined as

        sim(u, v) = \frac{c}{|\Gamma(u)| |\Gamma(v)|} \sum_{p \in \Gamma(u)}
        \sum_{q \in \Gamma(v)} sim(p, q)

    """
    n = len(G)
    M = raw_google_matrix(G, nodelist=nodelist, weight=weight)
    sim = numpy.identity(n, dtype=numpy.float32)
    for i in range(num_iterations):
        log.logger.debug("Starting SimRank iteration %d" % i)
        temp = c * M.T * sim * M
        sim = temp + numpy.identity(n) - numpy.diag(numpy.diag(temp))
    return sim


def raw_google_matrix(G, nodelist=None, weight='weight'):
    """Calculate the raw Google matrix (stochastic without teleportation)"""
    M = networkx.to_numpy_matrix(G, nodelist=nodelist, dtype=numpy.float32,
                                 weight=weight)
    n, m = M.shape  # should be square
    assert n == m and n > 0
    # Find 'dangling' nodes, i.e. nodes whose row's sum = 0
    dangling = numpy.where(M.sum(axis=1) == 0)
    # add constant to dangling nodes' row
    for d in dangling[0]:
        M[d] = 1.0 / n
    # Normalize. We now have the 'raw' Google matrix (cf. example on p. 11 of
    # Langville & Meyer (2006)).
    M = M / M.sum(axis=1)
    return M
