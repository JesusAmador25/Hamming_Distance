# Libraries
import itertools
import networkx as nx
import matplotlib.pyplot as plt
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

    def get_instances(self):
        """
        Generate all binary tuples of the given lenght whose number of 1s
        is less than or equal to the specified distance.

        Yields
        ------
        tuple of int
            A binary tuple (containing 0s and 1s).
        """
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
        return list(self.get_instances())

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
        Render the Hamming graph using Matplotlib with node labels.
        Uses a spring layout by default to visualize the connections. 
        The nodes are labeled with their corresponding binary tuple.
        """
        self._build_graph() # Ensure the graph is built
        plt.figure(figsize = (10, 10))
        nx.draw(self.graph, with_labels = True, node_color = 'orchid',
                node_size = 80, font_weight = 'bold', font_size = 9)
        plt.title(f"Hamming Graph (for length={self.lenght})")
        plt.show()

    def draw_withoutlabels(self):
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

# Functions
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

# Prueba 
def hamming_distance(x: int, y: int, n: int) -> int:
    """
    Calcula la distancia de Hamming entre dos enteros x e y,
    considerando solo los n bits menos significativos.
    """
    return (x ^ y).bit_count()  # Python 3.8+: bit_count() es más rápido que bin().count()

def build_adjacency_mask(n: int, d: int) -> list:
    """
    Construye una lista de máscaras de adyacencia para el grafo H(n,d).
    - Cada vértice se representa por un entero de 0 a 2^n - 1.
    - adj_mask[i] es un entero cuyo bit j está a 1 si el vértice i es adyacente a j (j ≠ i y d_H(i,j) ≥ d).
    - Usamos un solo entero por vértice (Python int de precisión arbitraria), capaz de manejar hasta 2^n bits.
    """
    N = 1 << n                     # N = 2^n, número de vértices
    adj_mask = [0] * N             # Inicializar lista de máscaras

    # Precalculamos todas las distancias? Podríamos, pero O(N^2) es inevitable para construir el grafo.
    # Sin embargo, podemos acelerar usando la propiedad de que la distancia de Hamming es el número de unos en XOR.
    for i in range(N):
        # Para cada i, recorremos j > i y llenamos simétricamente
        for j in range(i + 1, N):
            if hamming_distance(i, j, n) >= d:
                # Establecer el bit j en la máscara de i
                adj_mask[i] |= (1 << j)
                # Y el bit i en la máscara de j
                adj_mask[j] |= (1 << i)
    return adj_mask, N

def bron_kerbosch_max_clique2(adj_mask: list[int], N: int) -> int:
    """
    Algoritmo de Bron-Kerbosch con pivote y coloreo greedy para encontrar
    el tamaño de la clique máxima en el grafo representado por adj_mask.

    Parámetros
    ----------
    adj_mask : lista de N enteros.
               adj_mask[i] es un bitset donde el bit j está activo
               si existe arista entre el vértice i y el vértice j.
    N        : número de vértices del grafo (debe ser <= 63 para eficiencia,
               aunque Python soporta enteros arbitrariamente grandes).

    Retorna
    -------
    Tamaño (número de vértices) de la clique máxima encontrada.

    Estrategia
    ----------
    Los conjuntos se representan como enteros (bitsets):
      - P (candidatos)  : vértices que aún pueden extender la clique actual.
      - X (excluidos)   : vértices ya procesados (garantizan maximalidad).
      - r_size          : tamaño de la clique en construcción (reemplaza al
                          conjunto R, ya que solo necesitamos su cardinalidad).

    Podas aplicadas:
      1. Tamaño:   si r_size + |P| <= max_size, esta rama no puede mejorar.
      2. Coloreo:  si r_size + colores_greedy(P) <= max_size, ídem.
      3. Pivote:   se elige el vértice u en P∪X con mayor |P ∩ N(u)|,
                   reduciendo los candidatos a explorar a P \ N(u).
    """

    # Máscara de N bits para evitar bits "fantasma" al aplicar complemento (~)
    # En Python los enteros son de precisión arbitraria y con signo,
    # por lo que ~x activa infinitos bits superiores si no se enmascara.
    full_mask = (1 << N) - 1

    max_clique_size = 0   # mejor resultado encontrado hasta ahora

    # ── Coloreo greedy ──────────────────────────────────────────────────────────
    def greedy_color_bound(candidates_mask: int) -> int:
        """
        Devuelve una cota superior del tamaño de clique dentro de `candidates_mask`
        mediante coloreo greedy por clases de color independientes.
        Lógica: el tamaño de la clique máxima <= número cromático del grafo.
        Se construyen clases de color (conjuntos independientes) de forma greedy:
        cada vértice se asigna a la primera clase que no tenga ningún vecino suyo.
        El número de clases necesarias es la cota.
        """
        color_classes: list[int] = []   # cada elemento es un bitset (clase de color)
        remaining = candidates_mask

        while remaining:
            # Tomar el vértice de menor índice aún sin colorear
            vertex_bit = remaining & -remaining
            vertex = vertex_bit.bit_length() - 1

            # Buscar la primera clase existente sin vecinos de `vertex`
            placed = False
            for idx, color_class in enumerate(color_classes):
                if not (color_class & adj_mask[vertex]):
                    # Ningún nodo de esta clase es vecino de vertex → asignar aquí
                    color_classes[idx] |= vertex_bit
                    placed = True
                    break

            if not placed:
                # Ninguna clase sirve → abrir una nueva
                color_classes.append(vertex_bit)

            remaining &= ~vertex_bit

        return len(color_classes)

    # ── Expansión recursiva ─────────────────────────────────────────────────────
    def expand(r_size: int, P: int, X: int) -> None:
        """
        Extiende la clique actual (de tamaño r_size) probando cada candidato en P.

        Parámetros
        ----------
        r_size : número de vértices en la clique que se está construyendo.
        P      : bitset de candidatos que pueden ampliar la clique.
        X      : bitset de excluidos (ya procesados en ramas anteriores).
        """
        nonlocal max_clique_size

        # ── Caso base: clique maximal ───────────────────────────────────────────
        if P == 0 and X == 0:
            if r_size > max_clique_size:
                max_clique_size = r_size
            return

        # ── Poda 1: tamaño ─────────────────────────────────────────────────────
        # Si incluso añadiendo todos los candidatos no superamos el máximo, podar.
        if r_size + P.bit_count() <= max_clique_size:
            return

        # ── Poda 2: coloreo greedy ─────────────────────────────────────────────
        # Cota más ajustada: número cromático de P es cota del tamaño de clique en P.
        if r_size + greedy_color_bound(P) <= max_clique_size:
            return

        # ── Elegir pivote u en P ∪ X ───────────────────────────────────────────
        # Criterio: maximizar |P ∩ N(u)| para minimizar los candidatos a explorar.
        # Cuantos más candidatos cubre el pivote, menos ramas se abren.
        union_PX = P | X
        best_pivot = -1
        best_coverage = -1

        temp = union_PX
        while temp:
            u_bit = temp & -temp
            u = u_bit.bit_length() - 1
            coverage = (P & adj_mask[u]).bit_count()
            if coverage > best_coverage:
                best_coverage = coverage
                best_pivot = u
            temp ^= u_bit   # eliminar u_bit de temp

        # Candidatos a explorar: vértices de P que NO son vecinos del pivote.
        # El pivote ya "cubre" sus vecinos, así que no hay que expandirlos desde aquí.
        candidates = P & (~adj_mask[best_pivot] & full_mask)

        # ── Ciclo de backtracking ───────────────────────────────────────────────
        while candidates:
            # Tomar el candidato de menor índice
            v_bit = candidates & -candidates
            v = v_bit.bit_length() - 1

            # Llamada recursiva: añadir v a la clique,
            # restringir P y X a los vecinos de v.
            expand(
                r_size + 1,
                P & adj_mask[v],
                X & adj_mask[v],
            )

            # Mover v de P a X: ya fue procesado en esta rama.
            P &= ~v_bit
            X |= v_bit

            # Actualizar candidates eliminando directamente v.
            # Es equivalente a recalcular P & ~adj_mask[best_pivot] porque
            # v ya no está en P, y el pivote no cambia en este ciclo.
            candidates &= ~v_bit

    # ── Llamada inicial ─────────────────────────────────────────────────────────
    # Al inicio: r_size = 0, P = todos los vértices, X = vacío.
    all_vertices = full_mask
    expand(r_size=0, P=all_vertices, X=0)

    return max_clique_size
import random


def heuristic_without_upper_bound(n, d, iterations=1000, seed=None):
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

    Returns
    -------
    best_code : list of tuple of int
        The largest valid code found.
    best_size : int
        The number of codewords in best_code, i.e. the estimate of A(n, d).

    Examples
    --------
    >>> code, size = heuristic_A(9, 4)
    >>> print(size)
    20  # known value of A(9, 4)
    """
    if seed is not None:  # check if the user provided a seed for reproducibility
        random.seed(seed)  # fix the random seed so results can be reproduced

    # generate all 2^n binary tuples of length n (weight up to n covers everything)
    all_words = list(HammingTupla(n, n).get_instances())

    best_code = []  # stores the largest valid code found across all iterations

    for _ in range(iterations):  # repeat the greedy construction 'iterations' times
        candidates = all_words.copy()  # make a fresh copy so the original is not modified
        random.shuffle(candidates)     # shuffle to explore a different greedy path each restart
        current_code = []              # start building a new code from scratch

        for word in candidates:  # iterate over every candidate codeword in shuffled order
            if is_valid_set(current_code, word, d):  # check if word is at least distance d from all chosen words
                current_code.append(word)            # if valid, add it to the current code

        if len(current_code) > len(best_code):  # compare this iteration's result with the global best
            best_code = current_code            # update best if a larger valid code was found

    return best_code, len(best_code)  # return the best code found and its size as the estimate of A(n,d)
