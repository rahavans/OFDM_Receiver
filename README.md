# OFDM_Receiver

Greetings! Over my 4A academic term at the University of Waterloo, I was taking a course on Wireless Communications (ECE 414) where the final project was to build a complete OFDM Receiver, that would be able to demodulate a signal using a digital communication pipeline. 

My design follows the traditional OFDM receiver design which incorporates parallelizing bitstreams for OFDM subcarriers, removing the pilot signal which later is used for channel equalization, and removing a cyclic prefix that is used to assist in combatting inter-symbol interference (ISI).

A DFT module is used to convert the received digital baseband time domain signal into a frequency domain representation. This conversion happens to the pilot signal and the message from the received signal.

Zero-Forcing channel equalization is performed to equalize the Additive White Gaussian Noise (AWGN) introduced by the channel. The equalization factor is a ratio of the received pilot signal to the expected pilot signal. The original message is then divided by this equalization to remove all channel effects.

Once the channel effects are removed, we perform symbol detection using the Maximum Likelihood Estimate (MLE) in 16-QAM, to determine the nearest constellation symbol to the received symbol. Using a 16-QAM constellation map, we have assigned 4-bit representations to each constellation symbol, which we are then able to map and recover. From there, we can form 8-bit representations, by concatenating every two 4-bit representation, which can then be used to retrieve the corresponding ASCII characters.

The OFDM_demodulator.py module depicts these steps in detail, as it is mirrored off the design discussed above.

To run the program, you will need Python 3. After downloading Python 3, simply git clone this repository and from inside the directory, while in your terminal, run:

python3 OFDM_demodulator.py

Make sure signal.csv is in the same directory as OFDM_demodulator.py since the program assumes that, if moved, then the file location in the program has to be updated as well.