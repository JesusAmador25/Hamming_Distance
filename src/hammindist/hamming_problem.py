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
        Generate all binary tuples of the given lenght (2^lenght tuples).
        This method is independent of the distance attribute.

        Yields
        ------
        tuple of int
            A binary tuple (containing 0s and 1s).
        """
        for tupla in itertools.product([0, 1], repeat = self.lenght):
                yield tupla
 
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

import random

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


import math
import random

def simulated_annealing(
    n, d,
    iterations=5000,
    T_start=1.0,
    T_end=0.01,
    tabu_tenure=20,
    max_perturbation=3,
    seed=None
):
    """
    Estimate A(n, d) using simulated annealing with tabu memory and
    aggressive perturbation.

    At each step, removes between 1 and max_perturbation codewords and
    attempts to add max_perturbation + 1 new ones. Tabu memory penalizes
    recently removed codewords, discouraging the search from revisiting
    the same regions. Accepts worsening moves with probability e^(delta/T)
    (Boltzmann distribution)to escape local optima.

    Parameters:
    n : int
        Length of the binary codewords.
    d : int
        Minimum Hamming distance required between any two codewords.
    iterations : int, optional
        Number of annealing steps (default 5000).
    T_start : float, optional
        Initial temperature, controls early acceptance of worse solutions
        (default 1.0).
    T_end : float, optional
        Final temperature, controls strictness at the end (default 0.01).
    tabu_tenure : int, optional
        Number of steps a removed codeword remains tabu (default 20).
    max_perturbation : int, optional
        Maximum number of codewords removed per perturbation (default 3).
    seed : int or None, optional
        Random seed for reproducibility (default None).

    Returns:
    best_code : list of tuple of int
        The largest valid code found.
    """
    if seed is not None:                   # fix the random seed if provided
        random.seed(seed)

    all_words = list(HammingTupla(n, d).get_instances())  # generate all 2^n binary codewords
    all_words_set = set(all_words)                        # set for fast membership checks

    bound = upper_bound(n, d)             # compute the upper bound once before the loop

    current_code = greedy_start(all_words, d)  # build a warm-start solution with greedy
    best_code = current_code.copy()            # initialize the global best

    if len(best_code) >= bound:           # if greedy already hits the bound, return immediately
        return best_code

    # --- tabu memory ---
    # maps each codeword to the step at which its tabu tenure expires
    # words not yet in the dict are treated as non-tabu (default expiry -1)
    tabu_expiry = {}

    # --- cooling schedule ---
    # geometric decay: T_k = T_start * alpha^k
    alpha = (T_end / T_start) ** (1 / iterations)
    T = T_start

    for step in range(iterations):

        # choose how many codewords to remove this step (between 1 and max_perturbation)
        k = random.randint(1, min(max_perturbation, len(current_code)))

        # prefer removing non-tabu words; fall back to tabu ones if necessary
        non_tabu = [w for w in current_code if tabu_expiry.get(w, -1) <= step]
        tabu_in_code = [w for w in current_code if tabu_expiry.get(w, -1) > step]

        if len(non_tabu) >= k:
            words_to_remove = random.sample(non_tabu, k)   # remove from non-tabu words first
        else:
            words_to_remove = non_tabu + random.sample(    # fill the rest from tabu words
                tabu_in_code, k - len(non_tabu)
            )

        removed_set = set(words_to_remove)
        candidate = [w for w in current_code if w not in removed_set]  # build candidate without removed words

        # mark removed words as tabu for the next tabu_tenure steps
        for word in words_to_remove:
            tabu_expiry[word] = step + tabu_tenure

        # --- attempt to add k+1 new codewords ---
        # exclude tabu words and words already in the candidate from the pool
        outside = [
            w for w in all_words_set - set(candidate)
            if tabu_expiry.get(w, -1) <= step          # skip tabu words when adding
        ]
        random.shuffle(outside)                        # shuffle to avoid deterministic order

        added = 0
        for word in outside:
            if added > k:                              # try to add one more than we removed
                break
            if is_valid_set(candidate, word, d):       # check minimum distance constraint
                candidate.append(word)                 # add word if compatible
                added += 1

        # --- acceptance criterion ---
        delta = len(candidate) - len(current_code)    # size difference after perturbation

        if delta > 0:
            current_code = candidate                   # always accept improvements
        elif random.random() < math.exp(delta / T):
            current_code = candidate                   # accept worsening with probability e^(delta/T)

        # --- update global best ---
        if len(current_code) > len(best_code):
            best_code = current_code.copy()            # save a copy so further changes don't affect it

        # --- early stopping ---
        if len(best_code) >= bound:                    # stop if the upper bound is reached
            break

        if delta > 0:
            T *= 0.999   # cold
        else:
            T *= alpha   # normal

        T = max(T, T_end)  # never less than T_end

    return best_code
