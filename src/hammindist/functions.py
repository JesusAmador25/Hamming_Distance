# Libraries

import itertools
import networkx as nx
import matplotlib.pyplot as plt
import random
import math
import sys
import time
from math import comb 

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

# Bactracking functions

def hamming_distance(X, Y):
    """
    Calculate the distance between two elements with the same length
    Arg:
        X: a string, an array or a tuple of 0's and 1's with length n
        Y: a string, an array or a tuple of 0's and 1's with length n
    Returns:
        d: a integer value non negative
    """
    if len(X) != len(Y):
        return "WARNING: the strings or arrays must have the same length"
    X_unpacked = [str(x) for x in [*X]]
    Y_unpacked = [str(y) for y in [*Y]]
    d = 0  # lets count the amount of characters that are different beetwen X and Y
    for x, y in zip(X_unpacked, Y_unpacked):
        if x != y:
            d += 1
    return d

def is_valid_set(candidate_set, new_code, min_distance):
    """
    Valid if a candidate_set is a valid set, it means that the elements of the set
    are at least the required distance apart
    Args:
        candidate_set: a set of codes with min_distance between them
        new_code: a code that will be added to the set if it has min_distance with all
            the elements of th candidate_set
        min_distance: the minimum distance that must havee the all elements of the set
            with the new code
    Returns:

    """
    for existing in candidate_set:
        distance = hamming_distance(new_code, existing)
        if distance < min_distance:
            return False
    return True

def sphere_packing_bound(length, distance):
    """
    Compute the sphere-packing (Hamming) upper bound for A(n, d).

    Treats each codeword as the center of a Hamming ball of radius
    t = (d-1)//2. Because balls around distinct codewords are
    disjoint, their total volume cannot exceed the full space 2^n,
    giving A(n, d) <= 2^n / sum_{i=0}^{t} C(n, i).

    Args:
        length   (int): n, the length of the codes.
        distance (int): d, the minimum Hamming distance required.

    Returns:
        int: the sphere-packing upper bound on A(n, d).
    """
    t = (distance - 1)//2
    return 2**length//sum(comb(length, i) for i in range(t+1))

def plotkin_bound(length, distance):
    """
    Compute the Plotkin upper bound for A(n, d).

    Counts the total pairwise distance of a code in two ways:
      - from below: each of the C(M,2) pairs contributes at least d,
        so S >= M(M-1)/2 * d.
      - from above: each of the n bit positions contributes at most
        M^2/4 differing pairs, so S <= n * M^2 / 4.
    Combining both inequalities and solving for M yields
    A(n, d) <= 2 * floor(d / (2d - n)), but only when 2d > n.
    When 2d <= n the bound does not apply and infinity is returned.

    Args:
        length   (int): n, the length of the codes.
        distance (int): d, the minimum Hamming distance required.

    Returns:
        int | float: the Plotkin upper bound on A(n, d),
                     or float('inf') if the bound does not apply.
    """
    if 2*distance > length:
        return 2*(distance//(2*distance - length))
    else:
        return float('inf')

def upper_bound(length, distance):
    """
    Compute the tightest available upper bound for A(n, d).

    Takes the minimum of the sphere-packing (Hamming) bound and the
    Plotkin bound. When Plotkin does not apply (2d <= n) its value is
    infinity, so the sphere-packing bound is returned automatically.

    Args:
        length   (int): n, the word length in bits.
        distance (int): d, the minimum Hamming distance required.

    Returns:
        int: the tightest upper bound on A(n, d) from the two methods.
    """
    return min(sphere_packing_bound(length, distance), plotkin_bound(length, distance))

def max_set(codes_list, min_distance):
    """
    Build the set C wich contains all the strings that are a distance d between them
    Args:
        codes_list: the strings, arrays or tuples that we want to know if are in the "best_set"
        min_distance: the distance that must have the elements of the "best_set"
    Returns:
        best_set: the set of strings with min_distance between them
    """
    codes_list = sorted(set(codes_list))
    n = len(codes_list)
    best_set = []

    def backtrack(start, current_set):
        nonlocal best_set  # nonlocal helps us to work with thee set that is out of bactrack
        if len(current_set) + (n - start) <= len(best_set):
            return

        if len(current_set) > len(best_set):
            best_set = current_set.copy()

        for i in range(start, n):
            if is_valid_set(current_set, codes_list[i], min_distance):
                current_set.append(codes_list[i])
                backtrack(i + 1, current_set)
                current_set.pop()

    backtrack(0, [])
    return best_set

def max_set_bounded(length, min_distance):
    """
    Build the set C wich contains all the strings that are a distance d between
    them using a upper bound
    Args:
        codes_list: the strings, arrays or tuples that we want to know if are in the "best_set"
        min_distance: the distance that must have the elements of the "best_set"
    Returns:
        best_set: the set of strings with min_distance between them
    """
    code = HammingTupla(length, min_distance)
    codes_list = code.as_list()
    best_set = []

    u_bound = upper_bound(length, min_distance)

    def backtrack(start, current_set):
        nonlocal best_set  # nonlocal helps us to work with thee set that is out of bactrack

        if len(current_set) + (len(codes_list) - start) <= len(best_set):
            return

        if len(current_set) >= u_bound:
            if len(current_set) > len(best_set):
                best_set = current_set.copy()
            return
            

        if len(current_set) > len(best_set):
            best_set = current_set.copy()

        for i in range(start, len(codes_list)):
            if is_valid_set(current_set, codes_list[i], min_distance):
                current_set.append(codes_list[i])
                backtrack(i + 1, current_set)
                current_set.pop()

    backtrack(0, [])
    return best_set

# Graphs Functions

#En esta seccion se implementa el algoritmo de Tomita para encontrar el tamaño 
#del clan maximal de la grafica de Hamming, con algunas optimizaciones como la 
#reducción por paridad y poda por coloración greedy
#1.La función que calcula el tamaño del clan maximal de la grafica de hamming
#sin embargo no es eficiente calculando grafos densos como A(8,3) en adelante

sys.setrecursionlimit(1000000)

def binary_hamming_distance(x: int, y: int) -> int:
    return (x ^ y).bit_count()

def build_adjacency_bitsets(n: int, d: int, even_only: bool = False):
    """Grafo de adyacencia: arista si distancia >= d.
    Si even_only=True, solo vértices de peso par."""
    total = 1 << n
    vertices = [v for v in range(total) if (not even_only) or (v.bit_count() % 2 == 0)]
    N = len(vertices)
    idx = {v: i for i, v in enumerate(vertices)}
    adj = [0] * N
    for a in range(N):
        for b in range(a + 1, N):
            if binary_hamming_distance(vertices[a], vertices[b]) >= d:
                adj[a] |= (1 << b)
                adj[b] |= (1 << a)
    return adj, N, vertices

def greedy_color(P_bits, adj):
    """Coloreo greedy del subgrafo inducido por P_bits.
    Devuelve (lista_vertices_ordenados, número_de_colores)."""
    verts = []
    bits = P_bits
    while bits:
        v = (bits & -bits).bit_length() - 1
        verts.append(v)
        bits &= bits - 1
    if not verts:
        return [], 0
    verts.sort(key=lambda v: (P_bits & adj[v]).bit_count(), reverse=True)
    color = {}
    max_c = -1
    for v in verts:
        used = set()
        neigh = adj[v] & P_bits
        nbits = neigh
        while nbits:
            u = (nbits & -nbits).bit_length() - 1
            if u in color:
                used.add(color[u])
            nbits &= nbits - 1
        c = 0
        while c in used:
            c += 1
        color[v] = c
        if c > max_c:
            max_c = c
    num_colors = max_c + 1
    sorted_verts = sorted(verts, key=lambda v: color[v], reverse=True)
    return sorted_verts, num_colors

def greedy_initial_clique(adj, N, vertices):
    """Cota inferior rápida: clique greedy. Devuelve (tamaño, bitset de la clique)."""
    order = list(range(N))
    order.sort(key=lambda v: -adj[v].bit_count())
    current = 0
    for v in order:
        if (current & adj[v]) == current:
            current |= (1 << v)
    return current.bit_count(), current

def max_clique_tomita(adj, N, vertices, use_translation=True):
    """Algoritmo de Tomita para el tamaño de la clique máxima.
    Devuelve (tamaño, bitset de la clique encontrada)."""
    # Clique inicial greedy
    max_size, best_clique_bits = greedy_initial_clique(adj, N, vertices)

    if use_translation:
        # Fijamos el vértice 0 (índice 0) en la clique
        R0 = 1 << 0
        P0 = (1 << N) - 1
        P0 &= adj[0]          # solo vecinos de 0
        X0 = 0
    else:
        R0 = 0
        P0 = (1 << N) - 1
        X0 = 0

    # Variable para almacenar la mejor clique encontrada (como bitset)
    # Inicialmente la mejor es la greedy
    best_clique = best_clique_bits

    def expand(R_bits, P_bits, X_bits):
        nonlocal max_size, best_clique
        cur_sz = R_bits.bit_count()
        # Poda simple
        if cur_sz + P_bits.bit_count() <= max_size:
            return
        if P_bits == 0 and X_bits == 0:
            if cur_sz > max_size:
                max_size = cur_sz
                best_clique = R_bits
            return
        # Poda por coloración
        sorted_cand, colors = greedy_color(P_bits, adj)
        if cur_sz + colors <= max_size:
            return
        # Pivote: vértice en P∪X con mayor vecindario en P
        union = P_bits | X_bits
        best_u = -1
        best_deg = -1
        temp = union
        while temp:
            u_bit = temp & -temp
            u = u_bit.bit_length() - 1
            deg = (P_bits & adj[u]).bit_count()
            if deg > best_deg:
                best_deg = deg
                best_u = u
            temp ^= u_bit
        # Candidatos = P \ N(best_u)
        candidates = P_bits & ~adj[best_u]
        for v in sorted_cand:
            v_bit = 1 << v
            if not (candidates & v_bit):
                continue
            expand(R_bits | v_bit,
                   P_bits & adj[v],
                   X_bits & adj[v])
            P_bits &= ~v_bit
            X_bits |= v_bit
            if cur_sz + P_bits.bit_count() <= max_size:
                break

    expand(R0, P0, X0)
    return max_size, best_clique

def A(n, d, verbose=True):
    """Calcula A(n,d) y devuelve (valor, código) donde código es una lista de enteros (palabras)."""
    even_only = (d % 2 == 0)   # reducción por paridad
    if verbose:
        print(f"Construyendo grafo de adyacencia (distancia ≥ {d}) para n={n}...")
    adj, N, vertices = build_adjacency_bitsets(n, d, even_only)
    if verbose:
        print(f"Vértices: {N} (reducción por paridad: {even_only})")
    start = time.time()
    size, clique_bits = max_clique_tomita(adj, N, vertices, use_translation=True)
    elapsed = time.time() - start
    
    # Convertir el bitset de la clique a una lista de palabras originales
    code = []
    bits = clique_bits
    while bits:
        v = (bits & -bits).bit_length() - 1
        code.append(vertices[v])
        bits &= bits - 1
    
    # Si usamos reducción por paridad, el código obtenido es de peso par. No es necesario volver a trasladar.
    if verbose:
        print(f"A({n},{d}) = {size}  (tiempo: {elapsed:.2f} segundos)")
        print("Código encontrado (palabras en decimal):")
        print(code)
        # Opcional: mostrar también en binario
        # print([format(w, f'0{n}b') for w in code])
    return size, code

# Heuristic Functions 

def greedy_start(all_words, d):
    """
    Build an initial valid code using a greedy random approach.

    Shuffles all candidate codewords and adds each one to the code
    if it satisfies the minimum distance constraint with all
    already-selected codewords.

    This is used as a warm start for more sophisticated heuristics
    such as simulated annealing.

    Parameters
    ----------
    all_words : list of tuple of int
        All candidate binary codewords of length n.
    d : int
        Minimum Hamming distance required between any two codewords.

    Returns
    -------
    code : list of tuple of int
        A valid code built greedily. Not guaranteed to be optimal.
    """
    candidates = all_words.copy()  # copy to avoid modifying the original list
    random.shuffle(candidates)     # shuffle to get a different start each call
    code = []                      # initialize empty code

    for word in candidates:                  # iterate over shuffled candidates
        if is_valid_set(code, word, d):      # check minimum distance constraint
            code.append(word)                # add word if it is compatible

    return code


def heuristic(n, d, iterations=1000, seed=None):
    """
    Estimate A(n, d) — the maximum size of a binary code of length n
    and minimum Hamming distance d — using a greedy heuristic with
    random restarts.

    The algorithm builds a valid code greedily: at each step it tries
    to add a random codeword that satisfies the minimum distance
    constraint with all already-selected codewords. When no more
    codewords can be added, it records the size and restarts.

    This is a heuristic, so the result is a lower bound on A(n, d).
    It is not guaranteed to find the true optimum.

    Parameters
    ----------
    n : int
        Length of the binary codewords.
    d : int
        Minimum Hamming distance required between any two codewords.
    iterations : int, optional
        Number of random restarts (default is 1000).
    seed : int or None, optional
        Random seed for reproducibility (default is None).

    Returns:

    best_code : list of tuple of int
        The largest valid code found.
    """
    if seed is not None:
        random.seed(seed)

    all_words = list(HammingTupla(n, d).get_instances())
    best_code = []

    bound = upper_bound(n, d)  # compute the upper bound once before the loop

    for _ in range(iterations):
        current_code = greedy_start(all_words, d)

        if len(current_code) > len(best_code):
            best_code = current_code

        if len(best_code) >= bound:  # stop early if the upper bound is reached
            break

    return best_code


def select_words_to_remove(current_code, tabu_expiry, step, k):
    """
    Select k codewords to remove.

    Priority is given to codewords that are not currently tabu.
    If there are not enough non-tabu codewords, the remaining
    selections are completed with tabu codewords.
    """
    # Codewords whose tabu period has already expired.
    non_tabu = [
        w for w in current_code
        if tabu_expiry.get(w, -1) <= step
    ]

    # Codewords that are still tabu.
    tabu_in_code = [
        w for w in current_code
        if tabu_expiry.get(w, -1) > step
    ]

    # If enough non-tabu codewords exist, select only from them.
    if len(non_tabu) >= k:
        return random.sample(non_tabu, k)

    # Complete the selection using tabu codewords.
    return non_tabu + random.sample(
        tabu_in_code,
        k - len(non_tabu)
    )


def build_outside_pool(all_words_set, candidate, tabu_expiry, step):
    """
    Build a pool of candidate codewords for insertion.

    Only codewords that:
    - Are not part of the current candidate solution.
    - Are not tabu.

    The resulting pool is shuffled to encourage exploration
    of the search space.
    """
    pool = [
        w for w in all_words_set - set(candidate)
        if tabu_expiry.get(w, -1) <= step
    ]

    random.shuffle(pool)

    return pool


def try_add_codewords(candidate, pool, d, k):
    """
    Attempt to add up to k + 1 compatible codewords.

    A codeword is added only if it preserves the required
    minimum distance from all codewords already in the solution.
    """
    added = 0

    for word in pool:
        # Limit the number of insertions to control perturbation size.
        if added > k:
            break

        # Check whether the codeword is compatible with the current solution.
        if is_valid_set(candidate, word, d):
            candidate.append(word)
            added += 1

    return candidate


def accept(current_code, candidate, T):
    """
    Simulated annealing acceptance criterion.

    - Improvements are always accepted.
    - Worse solutions may be accepted with probability
      exp(Δ/T), where Δ is the size difference between solutions.
    """
    delta = len(candidate) - len(current_code)

    if delta > 0 or random.random() < math.exp(delta / T):
        return candidate

    return current_code


def simulated_annealing(
    n,
    d,
    iterations=5000,
    T_start=1.0,
    T_end=0.01,
    tabu_tenure=20,
    max_perturbation=3,
    seed=None
):
    """
    Estimate A(n, d) using simulated annealing with tabu memory.

    At each iteration:
    1. Remove between 1 and max_perturbation codewords.
    2. Mark removed codewords as tabu for a fixed tenure.
    3. Attempt to add up to max_perturbation + 1 new codewords.
    4. Accept or reject the candidate solution according to
       the simulated annealing criterion.

    A reheating mechanism is also applied whenever no improvement
    is observed for an extended number of iterations.
    """
    # Set random seed for reproducibility.
    if seed is not None:
        random.seed(seed)

    # Generate all possible codewords.
    all_words = list(HammingTupla(n, d).get_instances_complete())
    all_words_set = set(all_words)

    # Theoretical upper bound for A(n, d).
    bound = upper_bound(n, d)

    # Generate an initial solution using a greedy heuristic.
    current_code = greedy_start(all_words, d)
    best_code = current_code.copy()

    # Stop immediately if the upper bound is reached.
    if len(best_code) >= bound:
        return best_code

    # Stores the iteration at which each tabu codeword becomes available.
    tabu_expiry = {}

    # Geometric cooling factor.
    alpha = (T_end / T_start) ** (1 / iterations)

    T = T_start

    # Counter for consecutive iterations without improvement.
    no_improve_count = 0
    no_improve_limit = iterations // 10

    for step in range(iterations):

        # Randomly choose the perturbation size.
        k = random.randint(
            1,
            min(max_perturbation, len(current_code))
        )

        # Select codewords to remove from the current solution.
        words_to_remove = select_words_to_remove(
            current_code,
            tabu_expiry,
            step,
            k
        )

        # Build a candidate solution without the removed codewords.
        candidate = [
            w for w in current_code
            if w not in set(words_to_remove)
        ]

        # Mark removed codewords as tabu.
        for word in words_to_remove:
            tabu_expiry[word] = step + tabu_tenure

        # Build a pool of eligible codewords for insertion.
        pool = build_outside_pool(
            all_words_set,
            candidate,
            tabu_expiry,
            step
        )

        # Attempt to expand the candidate solution.
        candidate = try_add_codewords(
            candidate,
            pool,
            d,
            k
        )

        # Apply the acceptance criterion.
        current_code = accept(
            current_code,
            candidate,
            T
        )

        # Update the best solution found so far.
        if len(current_code) > len(best_code):
            best_code = current_code.copy()
            no_improve_count = 0
        else:
            no_improve_count += 1

        # Reheat the temperature if the search stagnates.
        if no_improve_count >= no_improve_limit:
            T = T_start * 0.5
            no_improve_count = 0

        # Stop if the theoretical bound is reached.
        if len(best_code) >= bound:
            break

        # Apply geometric cooling.
        T = max(T * alpha, T_end)

    return best_code