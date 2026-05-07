import networkx as nx
import itertools
from math import comb

def hamming_distance(a: int, b: int) -> int:
    """Distancia de Hamming entre dos enteros (popcount del XOR)."""
    return (a ^ b).bit_count()

def build_hamming_graph(n: int, d: int) -> nx.Graph:
    """
    Construye el grafo de Hamming H(n, d):
    - Vértices: números enteros de 0 a 2^n - 1 (representan palabras binarias)
    - Arista entre u y v si hamming_distance(u, v) >= d
    """
    num_vertices = 1 << n
    G = nx.Graph()
    G.add_nodes_from(range(num_vertices))
    for u in range(num_vertices):
        for v in range(u + 1, num_vertices):
            if hamming_distance(u, v) >= d:
                G.add_edge(u, v)
    return G

def bron_kerbosch_max_cliques(G: nx.Graph):
    """
    Implementación del algoritmo de Bron–Kerbosch (versión con pivote)
    que encuentra todos los cliques maximales en un grafo no dirigido.
    Adaptado del artículo original "Algorithm 457: Finding All Cliques of an Undirected Graph".
    Retorna una lista de cliques (cada clique es un conjunto de vértices).
    """
    # Convertir los vértices a enteros 0..N-1 (ya lo son)
    vertices = list(G.nodes())
    # Precalcular vecinos como lista de conjuntos para acceso rápido
    neighbors = {v: set(G.neighbors(v)) for v in vertices}
    N = len(vertices)
    # Orden inicial: todos los vértices en "candidates", "not" vacío
    all_vertices = vertices[:]  # lista de todos los vértices en orden
    compsub = []  # R, clique en construcción
    cliques = []  # almacenará los cliques maximales encontrados

    def extend(old, ne, ce):
        """
        old: lista de vértices (primero 'not' (0..ne-1), luego 'candidates' (ne..ce-1))
        ne: número de vértices en not (0 <= ne <= ce)
        ce: número total de elementos en old (len(old))
        """
        nonlocal cliques
        # Paso 1: elegir punto fijo (fixp) con mínimo número de disconexiones
        minnod = ce
        fixp = None
        s = -1
        nod = 0  # indicador si el punto fijo se tomó de candidates (1) o not (0)

        i = 0
        while i < ce and minnod != 0:
            p = old[i]
            count = 0
            # Contar disconexiones con el resto de candidatos (desde ne hasta ce-1)
            j = ne
            pos = -1
            while j < ce and count <= minnod:
                if p not in neighbors[old[j]]:  # disconexión
                    count += 1
                    pos = j
                j += 1
            if count < minnod:
                fixp = p
                minnod = count
                if i < ne:
                    s = pos
                else:
                    s = i
                    nod = 1
            i += 1

        # Bucle principal de backtracking
        # nod iterará desde minnod + nod hasta 1
        for _ in range(minnod + nod, 0, -1):
            # Intercambiar el candidato seleccionado (old[s]) con old[ne]
            p = old[s]
            old[s] = old[ne]
            sel = old[ne]
            old[ne] = p

            # Construir nuevo conjunto 'not' (new) y 'candidates' (newcand)
            new = [0] * ce  # preasignamos tamaño máximo
            newne = 0
            # Copiar vértices de 'not' que son vecinos de sel
            for i in range(ne):
                if sel in neighbors[old[i]]:
                    new[newne] = old[i]
                    newne += 1
            newce = newne
            # Copiar vértices de 'candidates' (desde ne+1 hasta ce-1) que son vecinos de sel
            # Nota: el índice ne ya contiene sel, que fue movido; lo saltamos
            for i in range(ne + 1, ce):
                if sel in neighbors[old[i]]:
                    new[newce] = old[i]
                    newce += 1

            compsub.append(sel)

            if newce == 0:
                # Se encontró un clique maximal
                cliques.append(compsub.copy())
            else:
                if newne < newce:
                    # Llamada recursiva con el nuevo conjunto
                    # new[:newce] contiene (not + candidates)
                    extend(new, newne, newce)

            compsub.pop()
            # Mover sel al conjunto 'not' para futuras iteraciones
            ne += 1

            # Si aún quedan candidatos por procesar (nod > 1), seleccionar el siguiente
            # candidato desconectado del punto fijo
            if nod > 1:
                # Buscar siguiente candidato (pos > s) que esté desconectado de fixp
                s = ne
                while s < ce and fixp in neighbors[old[s]]:
                    s += 1
                if s >= ce:
                    break
                # El siguiente candidato ya está en old[s], listo para el siguiente ciclo
            else:
                # Solo un candidato, terminar
                break

    # Iniciar llamada con todos los vértices en candidates, not vacío
    extend(all_vertices, 0, N)
    return cliques

def main():
    # Parámetros de prueba
    n = 3      # longitud de las palabras
    d = 2      # distancia mínima requerida
    print(f"Construyendo grafo de Hamming H({n},{d})...")
    G = build_hamming_graph(n, d)
    print(f"Vértices: {G.number_of_nodes()}, Aristas: {G.number_of_edges()}")

    print("\n=== Cliques maximales encontrados por nuestra implementación ===")
    our_cliques = bron_kerbosch_max_cliques(G)
    print(f"Número de cliques maximales: {len(our_cliques)}")
    max_size = max(len(c) for c in our_cliques) if our_cliques else 0
    print(f"Tamaño del clique máximo (A({n},{d})): {max_size}")
    # Mostrar primeros 5 cliques como ejemplo
    print("Ejemplo de cliques (primeros 5):")
    for i, clique in enumerate(our_cliques[:5]):
        # Convertir enteros a representación binaria para mejor visualización
        bin_repr = [format(v, f'0{n}b') for v in clique]
        print(f"  {i+1}: {bin_repr}")

    # Comparación con networkx.find_cliques (Bron–Kerbosch implementado en C)
    print("\n=== Comparación con networkx.find_cliques ===")
    nx_cliques = list(nx.find_cliques(G))
    print(f"networkx encontró {len(nx_cliques)} cliques maximales.")
    nx_max_size = max(len(c) for c in nx_cliques) if nx_cliques else 0
    print(f"Tamaño del clique máximo según networkx: {nx_max_size}")

    # Verificar que nuestros cliques coinciden (como conjuntos)
    our_sets = [set(c) for c in our_cliques]
    nx_sets = [set(c) for c in nx_cliques]
    if set(frozenset(s) for s in our_sets) == set(frozenset(s) for s in nx_sets):
        print("¡Los conjuntos de cliques maximales coinciden perfectamente!")
    else:
        print("Advertencia: los conjuntos difieren. Revisar implementación.")

if __name__ == "__main__":
    main()