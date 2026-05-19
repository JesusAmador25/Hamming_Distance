"""
Unit tests for the hammindist package.
Covers: hamming_distance, bounds, max_set, graph construction,
        Bron-Kerbosch variants, edge cases, and known A(n,d) values.
"""

from hammindist.solvers import (
    hamming_distance,
    sphere_packing_bound,
    plotkin_bound,
    upper_bound,
    is_valid_set,
    max_set,
    max_set_bounded,
    HammingTupla,
    build_adjacency_mask,
    bron_kerbosch_max_clique2,
)
from hammindist.graphwithpruning import (
    hamming_distance as hd_graph,
    build_hamming_graph,
    bron_kerbosch_max_cliques,
)

class TestHammingDistance:
    """Tests for hamming_distance in solvers.py."""

    def test_identical_words(self):
        """Distance from a word to itself must be 0."""
        assert hamming_distance((0, 0, 0), (0, 0, 0)) == 0

    def test_opposite_words(self):
        """Distance between (0,0,0) and (1,1,1) must be 3."""
        assert hamming_distance((0, 0, 0), (1, 1, 1)) == 3

    def test_one_difference(self):
        """Words differing in exactly one position."""
        assert hamming_distance((1, 0, 1), (1, 1, 1)) == 1

    def test_two_differences(self):
        assert hamming_distance((0, 1, 0, 1), (1, 1, 1, 1)) == 2

    def test_string_input(self):
        """Function must also accept strings."""
        assert hamming_distance("0101", "1100") == 2

    def test_different_lengths_returns_warning(self):
        """Inputs of different lengths must return a WARNING string."""
        result = hamming_distance((0, 1), (0, 1, 0))
        assert "WARNING" in str(result)

    def test_symmetry(self):
        """d(x, y) == d(y, x) for all x, y."""
        x = (1, 0, 1, 1, 0)
        y = (0, 0, 1, 0, 1)
        assert hamming_distance(x, y) == hamming_distance(y, x)

    def test_triangle_inequality(self):
        """d(x, z) <= d(x, y) + d(y, z)."""
        x = (1, 0, 0, 0)
        y = (1, 1, 0, 0)
        z = (1, 1, 1, 0)
        assert hamming_distance(x, z) <= hamming_distance(x, y) + hamming_distance(y, z)