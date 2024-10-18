import networkx as nx 
import numpy as np 
import matplotlib.pyplot as plt 
from collections import Counter


def add_nums(a,b):
    return a+b


def degree_distribution(G, number_of_bins=15, log_binning=True, density=True, directed=False):
   
    # Step 0: Do we want the directed or undirected degree distribution?
    if directed:
        if directed=='in':
            k = list(dict(G.in_degree()).values()) # get the in degree of each node
        elif directed=='out':
            k = list(dict(G.out_degree()).values()) # get the out degree of each node
        else:
            out_error = "Help! if directed!=False, the input needs to be either 'in' or 'out'"
            print(out_error)
            # Question: Is this the correct way to raise an error message in Python?
            #           See "raise" function...
            return out_error
    else:
        k = list(dict(G.degree()).values()) # get the degree of each node


    # Step 1: We will first need to define the support of our distribution
    kmax = np.max(k)    # get the maximum degree
    kmin = 0            # let's assume kmin must be 0


    # Step 2: Then we'll need to construct bins
    if log_binning:
        # array of bin edges including rightmost and leftmost
        bins = np.logspace(0, np.log10(kmax+1), number_of_bins+1)
    else:
        bins = np.linspace(0, kmax+1, num=number_of_bins+1)


    # Step 3: Then we can compute the histogram using numpy
    probs, _ = np.histogram(k, bins, density=density)


    # Step 4: Return not the "bins" but the midpoint between adjacent bin
    #         values. This is a better way to plot the distribution.
    bins_out = bins[1:] - np.diff(bins)/2.0
    
    return bins_out, probs


def plot_degree_distribution(G):
    x, y = degree_distribution(G)
    fig, ax = plt.subplots(1,1,figsize=(4.5,4),dpi=125)
    ax.loglog(x, y,'o', color='teal', label='degree', alpha=0.8, mec='.1')
    ax.set_xlabel(r"$k$",fontsize='large')
    ax.set_ylabel(r"$P(k)$",fontsize='large')
    ax.legend(fontsize='small')
    ax.grid(linewidth=1.5, color='#999999', alpha=0.2, linestyle='-')
    ax.set_title('CS PhD Collabs Degree Distribution')

    plt.savefig('CS PhD Collabs Degree Distribution.png', dpi=425, bbox_inches='tight')
    plt.savefig('CS PhD Collabs Degree Distribution.pdf', bbox_inches='tight')
    plt.show()


def configuration_model_from_degree_sequence(G, return_simple=True):

    degree_sequence = list(dict(G.degree()).values())

    # Check if the degree sequence is valid (sum of degrees must be even)
    if sum(degree_sequence) % 2 != 0:
        raise ValueError("The sum of the degree sequence must be even.")

    # Create stubs list: node i appears degree_sequence[i] times
    stubs = []
    for node, degree in enumerate(degree_sequence):
        stubs.extend([node] * degree)

    # Shuffle stubs to randomize the pairing process
    np.random.shuffle(stubs)

    # Initialize an empty multigraph
    G = nx.MultiGraph()

    # Add nodes to the graph
    G.add_nodes_from(range(len(degree_sequence)))

    # Pair stubs to create edges
    while stubs:
        u = stubs.pop()
        v = stubs.pop()

        # Add the edge to the graph
        G.add_edge(u, v)

    if return_simple:
        # Convert the multigraph to a simple graph (remove parallel edges and self-loops)
        G_simple = nx.Graph(G)  # This removes parallel edges and self-loops by default

        return G_simple

    else:
        return G
    

