# Libraries
import itertools
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