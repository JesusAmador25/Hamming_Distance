"""
Unit tests for functions.py (all functions)

This module tests all classes and functions defined in functions.py.
"""

import unittest
import random
from hammindist.functions import*
class TestHammingTupla(unittest.TestCase):
    """Test cases for the HammingTupla class."""

    def test_initialization(self):
        ht = HammingTupla(3, 2)
        self.assertEqual(ht.lenght, 3)
        self.assertEqual(ht.distance, 2)

    def test_repr(self):
        ht = HammingTupla(4, 1)
        self.assertEqual(repr(ht), "HammingTupla(lenght = 4, distance = 1)")

    def test_get_instances_complete(self):
        ht = HammingTupla(2, 1)
        instances = list(ht.get_instances_complete())
        expected = [(0, 0), (0, 1), (1, 0), (1, 1)]
        self.assertEqual(instances, expected)

    def test_get_instances_restricted(self):
        ht = HammingTupla(3, 1)
        instances = list(ht.get_instances_restricted())
        expected = [(0,0,0), (1,0,0), (0,1,0), (0,0,1)]
        self.assertEqual(instances, expected)

    def test_as_list(self):
        ht = HammingTupla(2, 1)
        self.assertEqual(ht.as_list(), [(0,0), (1,0), (0,1)])

    def test_hamming_distance(self):
        self.assertEqual(HammingTupla.hamming_distance((0,1,0), (1,1,0)), 1)
        self.assertEqual(HammingTupla.hamming_distance((0,0), (1,1)), 2)
        self.assertEqual(HammingTupla.hamming_distance((1,0,1), (1,0,1)), 0)
        # different lengths --> returns warning string
        res = HammingTupla.hamming_distance((0,1), (0,1,0))
        self.assertTrue(isinstance(res, str))

    def test_build_graph(self):
        ht = HammingTupla(2, 1)
        ht._build_graph()
        self.assertEqual(ht.graph.number_of_nodes(), 3)
        self.assertEqual(ht.graph.number_of_edges(), 2)


class TestBacktrackingFunctions(unittest.TestCase):
    """Test functions used in backtracking algorithms."""

    def test_is_valid_set(self):
        # Test a valid addition
        candidate_set = [(0,0,0), (1,1,0)]  # distance between them is 2
        # (1,0,1) has distance 2 to (0,0,0) and distance 2 to (1,1,0) -> valid
        self.assertTrue(is_valid_set(candidate_set, (1,0,1), 2))
        # Test an invalid addition (distance 1 to first element)
        self.assertFalse(is_valid_set(candidate_set, (0,0,1), 2))

    def test_sphere_packing_bound(self):
        self.assertEqual(sphere_packing_bound(3, 3), 2)
        self.assertEqual(sphere_packing_bound(5, 3), 5)

    def test_plotkin_bound(self):
        self.assertEqual(plotkin_bound(5, 3), 2*(3//(6-5)))  # 6
        self.assertEqual(plotkin_bound(6, 3), float('inf'))

    def test_upper_bound(self):
        self.assertEqual(upper_bound(3, 3), 2)
        self.assertEqual(upper_bound(5, 3), 5)

    def test_max_set(self):
        codes = [(0,0), (0,1), (1,0), (1,1)]
        best = max_set(codes, 2)
        self.assertEqual(len(best), 2)
        for i in range(len(best)):
            for j in range(i+1, len(best)):
                self.assertGreaterEqual(
                    HammingTupla.hamming_distance(best[i], best[j]), 2)

    def test_max_set_bounded(self):
        best = max_set_bounded(3, 2)
        self.assertGreaterEqual(len(best), 4)


class TestGraphFunctions(unittest.TestCase):
    """Test functions for graph construction and clique finding."""

    def test_binary_hamming_distance(self):
        self.assertEqual(binary_hamming_distance(1, 2), 2)
        self.assertEqual(binary_hamming_distance(5, 1), 1)
        self.assertEqual(binary_hamming_distance(3, 3), 0)

    def test_build_adjacency_bitsets(self):
        adj, N, vertices = build_adjacency_bitsets(2, 1, even_only=False)
        self.assertEqual(N, 4)
        for a in adj:
            self.assertEqual(a.bit_count(), 3)

    def test_greedy_color(self):
        adj, N, _ = build_adjacency_bitsets(2, 1, even_only=False)
        P_bits = (1 << N) - 1
        sorted_verts, num_colors = greedy_color(P_bits, adj)
        self.assertEqual(num_colors, N)
        self.assertEqual(len(sorted_verts), N)

    def test_greedy_initial_clique(self):
        adj, N, vertices = build_adjacency_bitsets(3, 2, even_only=False)
        size, clique_bits = greedy_initial_clique(adj, N, vertices)
        self.assertGreaterEqual(size, 2)

    def test_max_clique_tomita(self):
        adj, N, vertices = build_adjacency_bitsets(3, 2, even_only=False)
        size, clique_bits = max_clique_tomita(adj, N, vertices, use_translation=True)
        self.assertEqual(size, 4)

    def test_A_function(self):
        size, code = A(3, 2, verbose=False)
        self.assertEqual(size, 4)
        for i in range(len(code)):
            for j in range(i+1, len(code)):
                self.assertGreaterEqual(binary_hamming_distance(code[i], code[j]), 2)


class TestHeuristicFunctions(unittest.TestCase):
    """Test heuristic functions for approximating A(n,d)."""

    def setUp(self):
        random.seed(42)

    def test_greedy_start(self):
        """Test that greedy_start returns a valid code (no size requirement)."""
        n, d = 3, 2
        all_words = list(HammingTupla(n, d).get_instances_complete())
        code = greedy_start(all_words, d)
        # Check validity using HammingTupla.hamming_distance
        for i in range(len(code)):
            for j in range(i+1, len(code)):
                self.assertGreaterEqual(
                    HammingTupla.hamming_distance(code[i], code[j]), d
                )
        # No minimum size assertion because the greedy algorithm is random
        # and may produce a small code (size 2) with some seeds.

    def test_heuristic(self):
        n, d = 3, 2
        best_code = heuristic(n, d, iterations=10, seed=42)
        self.assertGreaterEqual(len(best_code), 4)
        # Check validity
        for i in range(len(best_code)):
            for j in range(i+1, len(best_code)):
                self.assertGreaterEqual(
                    HammingTupla.hamming_distance(best_code[i], best_code[j]), d
                )

    def test_select_words_to_remove(self):
        current = [1, 2, 3, 4]
        tabu_expiry = {2: 10, 3: 5}
        step = 6
        k = 2
        removed = select_words_to_remove(current, tabu_expiry, step, k)
        self.assertEqual(len(removed), 2)
        non_tabu = [1, 4]
        self.assertTrue(any(r in non_tabu for r in removed))

    def test_build_outside_pool(self):
        all_words_set = {1, 2, 3, 4, 5}
        candidate = [1, 3]
        tabu_expiry = {2: 10, 4: 5}
        step = 6
        pool = build_outside_pool(all_words_set, candidate, tabu_expiry, step)
        # Eligible: 4 (expiry 5 <= 6) and 5 (never tabu)
        self.assertCountEqual(pool, [4, 5])  # order may vary due to shuffle

    def test_try_add_codewords(self):
        candidate = [(0,0,0)]
        # Use words that are pairwise compatible for d=2:
        # (0,1,1) and (1,0,1) are both distance 2 from (0,0,0) and distance 2 from each other
        pool = [(0,1,1), (1,0,1)]
        d = 2
        k = 1   # we can add up to k+1 = 2 words
        result = try_add_codewords(candidate, pool, d, k)
        self.assertEqual(len(result), 3)  # original + 2 new ones
        # Check validity
        for i in range(len(result)):
            for j in range(i+1, len(result)):
                self.assertGreaterEqual(
                    HammingTupla.hamming_distance(result[i], result[j]), d
                )

    def test_accept(self):
        current = [1,2]
        candidate_better = [1,2,3]
        candidate_worse = [1]
        T = 0.5
        self.assertEqual(accept(current, candidate_better, T), candidate_better)
        random.seed(123)
        res = accept(current, candidate_worse, 0.1)
        self.assertTrue(res in (current, candidate_worse))

    def test_simulated_annealing(self):
        n, d = 3, 2
        # Increased iterations for reliability
        best_code = simulated_annealing(n, d, iterations=500, tabu_tenure=5,
                                         max_perturbation=2, seed=123)
        self.assertGreaterEqual(len(best_code), 4)
        # Check validity
        for i in range(len(best_code)):
            for j in range(i+1, len(best_code)):
                self.assertGreaterEqual(
                    HammingTupla.hamming_distance(best_code[i], best_code[j]), d
                )


if __name__ == '__main__':
    unittest.main()
