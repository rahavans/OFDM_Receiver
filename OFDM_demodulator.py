import numpy as np
import math

QAM_16_map = {complex(3,-3): '0000', complex(3,-1): '0001', complex(3,1): '0011', complex(3,3): '0010',
            complex(1,-3): '0100', complex(1,-1): '0101', complex(1,1): '0111', complex(1,3): '0110',                                                                                        
            complex(-1,-3): '1100', complex(-1,-1): '1101', complex(-1,1): '1111', complex(-1,3): '1110',               
            complex(-3,-3): '1000', complex(-3,-1): '1001', complex(-3,1): '1011', complex(-3,3): '1010'}

pilot_4_symbols = [complex(1,1), complex(-1,1), complex(-1,-1), complex(1,-1)]

PILOT_REF = np.tile(pilot_4_symbols, 32)

def nearest_constellation_symbol(symbol):
    minimum = math.inf # set minimum to positive infinity as starting point
    point = None # track coordinate that is closest to the symbol
    for coordinate in QAM_16_map.keys():
        distance = math.sqrt((symbol.real - coordinate.real)**2 + (symbol.imag - coordinate.imag)**2) # calculate the distance from the coordinate on the 16-QAM map to the symbol
        if(distance < minimum): # check if distance calculated is less than current minimum
            minimum = distance # update minimum
            point = coordinate # update coordinate
    
    return point # return closest point on the constellation map to the symbol

# Signal Structure: Pilot (160 samples - 32 samples Pilot Cyclic Prefix + 128 samples Pilot, 32 samples OFDM Cyclic Prefix, 128 samples OFDM symbol)

received_signal = np.loadtxt('signal.csv', delimiter=',') # extract received signal data from CSV file

signal = received_signal[:, 0] + (1j * received_signal[:, 1]) # compose each sample using its real and imaginary parts

# Pilot Handling

pilot_cyclic_prefix = np.arange(0,32) # creating a list of the indices of the first 32 samples as they are the pilot's cyclic prefix (which we want to remove)

removed_pilot_cyclic_prefix_signal = np.delete(signal, pilot_cyclic_prefix) # remove the pilot's cyclic prefix

pilot = removed_pilot_cyclic_prefix_signal[0:128].copy() # extract a copy of the pilot from the original signal

pilot_samples = np.arange(0,128) # creating a list of the indices of the first 128 samples as they are the pilot samples (which we now want to remove from the original received signal)

removed_pilot_signal = np.delete(removed_pilot_cyclic_prefix_signal, pilot_samples) # remove the pilot samples from the originally received signal since we have a copy

dft_pilot = np.fft.fft(pilot) # apply the DFT on the received pilot

H_hat = dft_pilot/PILOT_REF # calculate equalization factor H_hat by dividing the DFT of the pilot by the reference pilot (already in frequency domain)

OFDM_signal_cyclic_prefix = np.arange(0,32) # creating a list of the indices of the first 32 elements as they are the OFDM signal's cyclic prefix (which we want to remove)

OFDM_signal = np.delete(removed_pilot_signal, OFDM_signal_cyclic_prefix) # remove the OFDM signal cyclic prefix

dft_OFDM_signal = np.fft.fft(OFDM_signal) # apply the DFT to the OFDM signal

equalized_OFDM_signal = dft_OFDM_signal/H_hat # apply Channel Equalization using H_hat calculated from pilot signal

# AWGN handling for constellation mapping

demodulated_OFDM_signal = [] # create a list for the demodulated OFDM signal after constellation mapping

for symbol in equalized_OFDM_signal: 
    constellation_symbol = nearest_constellation_symbol(symbol) # find the 16-QAM constellation symbol that is closest to the symbol in the OFDM signal
    demodulated_OFDM_signal.append(QAM_16_map[constellation_symbol]) # append the 4-bit code that corresponds to the constellation symbol

combined_results = [] # create a list that combines the demodulated results of every two subcarriers

for i in range(0, len(demodulated_OFDM_signal)-1, 2):
    ascii_binary = demodulated_OFDM_signal[i] + demodulated_OFDM_signal[i+1] # concatenate the string representation of the two subcarriers into an 8-bit representation (its ASCII code)
    combined_results.append(ascii_binary) # append the resulting combined string (now 8 bit) to the list

message = "" # initialize a message string for the decoded message

for ascii_binary in combined_results:
    ascii_decimal = int(ascii_binary, 2) # convert the bit representation of the ASCII character to its decimal form
    character = chr(ascii_decimal) # get the corresponding character to the ASCII character's decimal form
    message += character # concatenate the ASCII character to the message string

print(f"Demodulated Message: {message}\n")