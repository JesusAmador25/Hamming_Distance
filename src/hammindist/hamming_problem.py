import itertools


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


def hamming_set_c(d, *X):
    """
    Build the set C wich contains all the strings that are a distance d between them
    Args:
        d: the distance that must have the elements of C
        *X: the strings, arrays or tuples that we want to know if are in the set C
    Returns:
        C: the set of strings with distance d between them
    """
    X_list = list(X)
    n = len(X_list)
    C = set()

    if n == 0 or n == 1:
        print(
            "WARNING: You must give at least two string, arrays or tuples, otherwise C is the same X"
        )
        return X_list[:]

    for i in range(n):
        for j in range(i + 1, n):
            distance = hamming_distance(X_list[i], X_list[j])
            if distance >= d and X_list[j] not in C:
                C.add(X_list[i])
                C.add(X_list[j])
    C = list(C)
    m = len(C)
    max_set = []
    max_value = 0
    for k in range(m):
        distances = []
        for l in range(m):
            distances.append(hamming_distance(C[k], C[l]))
        C1 = [C[i] for i in range(m) if distances[i] >= d]
        if len(C1) > max_value:
            max_set, max_value = C1, len(C1)
    return max_set


def hamming_instances_generator(n):
    """
    Create a instance for the hamming problem
    Args:
        n: is the lenght of each tuple
    Return:
        instance: a tuple with all the posibles tuples of 0's and 1's with lenght n
    """
    return itertools.product(range(2), repeat=n)


class HammingTupla:
    def __init__(self, length, distance):
        self.length = length
        self.distance = distance

    def __repr__(self):
        return f"HammingTupla(lenght = {self.length}, distance = {self.distance})"

    def get_instances(self):
        for one in range(0, self.distance + 1):
            for indices in itertools.combinations(range(self.length), one):
                tupla = [0] * self.length
                for index in indices:
                    tupla[index] = 1
