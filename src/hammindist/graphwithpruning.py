import networkx as nx
import itertools
import matplotlib.pyplot as plt
import sys
import time
'''
funcion que calcula el tamaño del clan maximal de la grafica de hamming
sin embargo no es eficiente calculando grafos densos como A(8,3) en adelante
'''
sys.setrecursionlimit(1000000)

def hamming_distance(x: int, y: int) -> int:
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
            if hamming_distance(vertices[a], vertices[b]) >= d:
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