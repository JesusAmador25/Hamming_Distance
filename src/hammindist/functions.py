# Libraries

import itertools
import networkx as nx
import matplotlib.pyplot as plt
import random
import math
import itertools
import sys
import time

# Classes
class HammingTupla:
    """
    A class to generate binary tuples of a given length with Hamming weight
    less than or equal to a specified distance.

    Attributes
    ----------
    lenght : int
        The lenght of the binary tuples.
    distance : int
        The maximum number of 1s (Hamming weight) allowed in each tuple.
    graph : networkx.Graph
        The graph representation of the Hamming tuples, where nodes are tuples
        and edges connect tuples with Hamming distance 1.
    """
    def __init__(self, lenght, distance):
        """
        Initialize a HammingTupla instance.

        Parameters
        ----------
        lenght : int
            The lenght of the binary tuples.
        distance : int
            The maximum number of 1s allowed in each tuple.
        """
        self.lenght = lenght
        self.distance = distance
        self.graph = nx.Graph() # Initialize the graph

    def __repr__(self):
        """
        Return a string representation of the object.

        Returns
        -------
        str
            A string describing the instance.
        """
        return f"HammingTupla(lenght = {self.lenght}, distance = {self.distance})"

    def get_instances_complete(self):
        """
        Generate all binary tuples of the given lenght (2^lenght tuples).
        This method is independent of the distance attribute.

        Yields
        ------
        tuple of int
            A binary tuple (containing 0s and 1s).
        """
        for tupla in itertools.product([0, 1], repeat = self.lenght):
                yield tupla

    def get_instances_restricted(self):
        for one in range(0, self.distance + 1):
            for indices in itertools.combinations(range(self.lenght), one):
                tupla = [0] * self.lenght
                for index in indices:
                    tupla[index] = 1
                yield tuple(tupla)

    def as_list(self):
        """
        Return all generated tuples as a list.

        Returns
        -------
        list of tuple of int
            A list containing all generated binary tuples.
        """
        return list(self.get_instances_restricted())

    @staticmethod
    def hamming_distance(X, Y):
        """
        Calculate the distance between two elements with the same lenght
        Arg:
            X: a string, an array or a tuple of 0's and 1's with lenght n
            Y: a string, an array or a tuple of 0's and 1's with lenght n
        Returns:
            d: a integer value non negative
        """
        if len(X) != len(Y):
            return "WARNING: the strings or arrays must have the same lenght"
        X_unpacked = [str(x) for x in [*X]]
        Y_unpacked = [str(y) for y in [*Y]]
        d = 0  # lets count the amount of characters that are different beetwen X and Y
        for x, y in zip(X_unpacked, Y_unpacked):
            if x != y:
                d += 1
        return d

    def _build_graph(self):
        """
        Builds the graph with nodes as Hamming tuples and edges between
        tuples with Hamming distance 1.
        """
        # Clear existing graph data before rebuilding to ensure fresh state
        self.graph.clear()
        nodes = self.as_list()
        self.graph.add_nodes_from(nodes)

        # Add edges based on Hamming distance 1
        for i in range(len(nodes)):
            for j in range(i + 1, len(nodes)):
                hamming_dist = HammingTupla.hamming_distance(nodes[i], nodes[j])
                if hamming_dist == 1:
                    self.graph.add_edge(nodes[i], nodes[j])

    def draw(self):
        """
        Render the Hamming graph using Matplotlib without node labels.

        Useful for larger graphs where text labels would clutter the
        visualization. Nodes are drawn as small 'orchid' colored circles.
        """
        self._build_graph() # Ensure the graph is built
        plt.figure(figsize = (10, 10))
        nx.draw(self.graph, with_labels = False, node_color = 'orchid',
                node_size = 60)
        plt.title(f"Hamming Graph (for length={self.lenght})")
        plt.show()

