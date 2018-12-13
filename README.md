# Correlation Attacks

Given the layout of a 3-LFSR (Linear Feedback Shift Register) key sequence
generator, and the combination function being that which picks the majority
output bit from the 3 LFSRs, and finally a output stream, compute the
keystream.

This can be done using a correlation attack given some number of plaintext and
ciphertext outputs, and finding a correlation between output and one (or more)
of the LFSRs.
