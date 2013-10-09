import networkx as nx

#TODO Examine if we can use nx.single-source_shortest_path_length here


def neighbourhood_search(G, n, k=1):
    """Get k-neighbourhood of node n"""
    dist = {}
    dist[n] = 0
    queue = [n]
    while queue:
        v = queue.pop(0)
        if dist[v] == k:
            break
        for w in G[v]:
            if w not in dist:
                queue.append(w)
                dist[w] = dist[v] + 1
    return dist


def neighbourhood_graph(G, n, k=1):
    """Get k-neighbourhood subgraph of node n"""
    dist = neighbourhood_search(G, n, k)
    return G.subgraph(dist.keys())


def edge_weights(G, weight='weight'):
    """Iterator over edge weights in G"""
    for u, nbrdict in G.adjacency_iter():
        for edgedata in nbrdict.itervalues():
            yield edgedata[weight]


def from_biadjacency_matrix(A, row_items=None, col_items=None, weight='weight'):
    import numpy

    kind_to_python_type = {'f': float,
                           'i': int,
                           'u': int,
                           'b': bool,
                           'c': complex,
                           'S': str}

    dt = A.dtype
    nrows, ncols = A.shape
    try:
        python_type = kind_to_python_type[dt.kind]
    except:
        raise TypeError("Unknown numpy data type: %s" % dt)

    if row_items is None:
        row_items = range(nrows)
    elif len(row_items) != nrows:
        raise ValueError("Expected %d row items, but got %d instead" %
                         (nrows, len(row_items)))
    if col_items is None:
        col_items = range(nrows, nrows + ncols)
    elif len(col_items) != ncols:
        raise ValueError("Expected %d col items, but got %d instead" %
                         (ncols, len(col_items)))

    G = nx.Graph()
    G.add_nodes_from(row_items)
    G.add_nodes_from(col_items)
    # get a list of edges
    x, y = numpy.asarray(A).nonzero()

    # handle numpy constructed data type
    G.add_edges_from((row_items[u], col_items[v], {weight: python_type(A[u, v])})
                     for u, v in zip(x, y))

    return G
