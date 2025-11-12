# OFDM_Receiver

Hi! Over my 4A academic term at the University of Waterloo, I was taking a course on Wireless Communications (ECE414) where the final project was to build a OFDM receiver, that would be able to demodulate a signal in a communication pipeline. 

The design follows a traditional OFDM receiver design which incorporates parallelizing bitstreams for OFDM subcarriers, removing the pilot signal, later used for channel equalization, and removing a cyclic prefix used to assist in combatting inter-symbol interference (ISI).

A DFT module is used to convert the received digital baseband time domain signal into a frequency domain representation. This conversion happens to the pilot signal and the original message portion from the received signal.

Now, Zero-Forcing channel equalization is performed to equalize the AWGN noise introduced by the channel. The equalization factor is a ratio of the received pilot signal to the expected pilot signal. The original message is then divided by this equalization to remove all channel effects.

Now, with channel effects removed, we perform symbol detection using MLE in 16-QAM, to determine the nearest constellation symbol to the received symbol, to help recover the original message. From there, we are able to concatenate the 4-bit binaries of the two OFDM symbols to form 8-bit representations, that can then be casted into ASCII characters to assist in recovering the signal.

The OFDM_demodulator.py depicts these steps in detail, as it is mirrored off the design discussed.

To run the program, you will need Python 3. After downloading Python 3, simply git clone this repository and from inside the directory in your terminal, run:

python3 OFDM_demodulator.py signal.csv