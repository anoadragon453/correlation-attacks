# Performs a correlation attack
import matplotlib as plt

# Progress bar
from sys import stdout

z_sequence = ([
    0, 1, 1, 0, 0, 1, 1, 0, 1, 0, 0, 1, 1, 0, 1, 0, 0, 1, 0, 1, 0, 1, 1, 1, 1,
    1, 0, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1,
    1, 0, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1,
    0, 1, 0, 0, 1, 0, 0, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 0, 1, 1, 0, 1, 1,
    1, 1, 1, 0, 0, 1, 1, 0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 1, 1,
    1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0,
    1, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1,
    1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 0, 
])

polynomial = [1, 2, 4, 6, 7, 10, 11, 13]
length = 13

def hamming(x, y):
    """Computes the hamming distance for two binary arrays"""

    distance = 0
    for i in range(len(x)):
        if x[i] != y[i]:
            distance += 1
    return distance

def shift_state(s, new_num):
    """Shifts state s to the left and returns outputted number"""
    num = s[0]
    for i in range(len(s) - 1):
        s[i] = s[i+1]
    return s, num

def compute_keystream(s, p, pL, sL):
    """Simulates an LFSR and produces a keystream of length sL given an initial
    state s and a polynomial p of length pL encoded as a list.
    """

    # Our resulting keystream sequence
    keystream = []

    for _ in range(sL):
        # Simulate one round of LFSR
        sum = 0
        
        # Run xor operations given taps
        for exponent in p:
            tap = pL - exponent
            sum += s[tap]

        # Shift state with new value, get popped value
        (s, popped) = shift_state(s, sum % 2)

        # Append popped value to the overall keystream sequence
        keystream.append(popped)

    return keystream

def increment_state(s):
    """Increment a state by 1. Ex: [0,0,0,1] -> [0,0,1,0]"""
    state_int = int(''.join(str(c) for c in s), 2) + 1
    state_binary_str = str(bin(state_int))[2:]
    new_s = [int(bit) for bit in state_binary_str]
    return [0] * (len(s) - len(state_binary_str)) + new_s

def calc_p_star(u, z):
    """Calculates the p* value for given u, z sequences"""
    n = len(z)
    return 1 - (hamming(u, z)/n)

# Attempt to guess the initial state of the smallest LFSR, L1, with L = 13
state = [0] * (length - 1)
state += [1]
print(state)

p_map = {}
highest_p_star = 0
count = 1
possible_states = 2**(length)
total_bars = 30
while count < possible_states:
    # Compute the generated keystream from this polynomial and initial state
    u_sequence = compute_keystream(state[:], polynomial, length, len(z_sequence))

    # Calculate p* of this initial state
    p_star = calc_p_star(u_sequence, z_sequence)

    # Note down this p_star value
    p_map[', '.join(str(c) for c in state)] = p_star

    # Note down highest value
    refresh_progress_bar = False
    if p_star > highest_p_star:
        highest_p_star = p_star
        refresh_progress_bar = True

    if count % (possible_states // total_bars) == 0:
        refresh_progress_bar = True

    if refresh_progress_bar:
        progress = int(count / possible_states * total_bars)
        bar = "[" + '#' * progress + '.' * (total_bars - progress - 1) + "]"
        text = "\rHighest: %f Progress: %s" % (highest_p_star, bar)
        stdout.write(text)

    if p_star > 0.9:
        break

    state = increment_state(state)
    count += 1

# Print out the results
print("\nFound p*: ", highest_p_star, "for initial state:", state)

# Show progress bar

# Show graph of results
