from typing import List
import copy
import math


def main():
    bin_list = ["10110010000", "10110111111", "00110001100", "10100001001", "10011000000", "10110010101",
                "01100100101",
                "01110010110", "11100001000", "10110011111"]

    for encoded in bin_list:
        decode(encoded)
        print()


def binary_to_char(binary_str: str) -> str:
    ascii_value = int(binary_str, 2)  # Convert binary to integer
    char = chr(ascii_value)  # Convert integer (ASCII) to character
    return char


def decode(message: str) -> str:
    message_len = len(message)
    parity_no = find_encoded_parity_bits(message_len)
    parity_indexes = get_parity_indexes(parity_no)
    original = extract_original(message, parity_indexes)
    parity_bits = extract_parity_bits(message, parity_indexes)
    encoded, parity_values = encode(original)

    if parity_bits == parity_values:
        print("No errors detected: ", original)

        char = binary_to_char(original)
        print(char)

        return original

    errors = ""
    for i in range(len(parity_bits)):
        if parity_bits[i] != parity_values[i]:
            errors += '1'
        else:
            errors += '0'

    error_index = int(errors, 2)
    if error_index > len(encoded):
        print("Error in parity bits: ", original)
    else:
        char_array = list(message)
        if char_array[error_index] == '0':
            char_array[error_index] = '1'
        else:
            char_array[error_index] = '0'

        corrected = ''.join(char_array)
        print("Corrected: ", corrected)

        og = extract_original(corrected, parity_indexes)
        print("ascii bit: ", og)

        char = binary_to_char(og)
        print("char: ", char)

        return corrected


def encode(message: str):
    hamming_encoded_str = position_bits(message)
    parity_bit_no = find_parity_bits(len(hamming_encoded_str))
    parity_indexes = get_parity_indexes(parity_bit_no)
    parity_values = get_parities(parity_indexes, hamming_encoded_str)
    hamming_encoded_str = insert_parity_bits(hamming_encoded_str, parity_values.copy(), parity_indexes)

    return hamming_encoded_str, parity_values


def extract_original(encoded_msg: str, parity_indexes: List[int]):
    parity_indexes = set(parity_indexes)
    original = ""

    for i in range(len(encoded_msg)):
        if i not in parity_indexes:
            original += encoded_msg[i]

    return original


def extract_parity_bits(encoded_msg: str, parity_indexes: List[int]):
    parity_indexes = set(parity_indexes)
    parity_bits = ""

    for i in range(len(encoded_msg)):
        if i in parity_indexes:
            parity_bits += encoded_msg[i]

    return parity_bits


def insert_parity_bits(hamming_encoded_str: List[str], parity_values: List[str], parity_indexes: List[int]):
    for parity_index in parity_indexes:
        hamming_encoded_str[parity_index] = parity_values.pop(0)

    return hamming_encoded_str


def string_to_bit(string: str):
    """
    This function takes any string with ascii characters and turns it into its binary representation
    :param string:
    :return:
    """
    binary_list = ""
    for char in string:
        ascii_value = ord(char)
        binary_representation = bin(ascii_value)[2:]  # Remove the '0b' prefix
        binary_padded = binary_representation.zfill(8)  # Pad with zeros to ensure 8 bits
        binary_list += binary_padded
    return binary_list


def position_bits(bit_string: str):
    """
    This function positions the bits of the original bit string onto a new bit string, leaving
    spaces for the parity bits filled with 0s
    :param bit_string: the string of bits we wish to encode
    :return: a list of bits with the parity bits filled with 0s
    """
    parity_no = find_parity_bits(len(bit_string))
    hamming_code_len = len(bit_string) + parity_no
    hamming_code = ["0"] * hamming_code_len

    # we save the indexes of the parity bits
    parity_indexes = get_parity_indexes(parity_no)

    # we iterate over the hamming code
    og_index = 0
    new_index = 0
    while og_index < len(bit_string):
        if new_index in parity_indexes:
            new_index += 1
            continue
        else:
            hamming_code[new_index] = bit_string[og_index]

        og_index += 1
        new_index += 1

    return hamming_code


def get_parities(parity_indexes: List[int], hamming_encoding: List[str]):
    """
    This function takes as a parameter a hamming encoded bit string and the indexes of the parity
    bits and returns the calculated value of the parity bits
    :param parity_indexes: the indexes where the parity bits go (this should be powers of 2)
    :param hamming_encoding: a hamming encoded bit string
    :return:
    """
    parity_indexes = set(parity_indexes)
    parities = []

    for parity_index in parity_indexes:
        bits = []
        to_check = False

        hamming_index = parity_index
        counter = 0
        while hamming_index < len(hamming_encoding):
            # a = (hamming_index - parity_index + 1)
            # b = (parity_index + 1)
            # res = a % b

            if counter % (parity_index + 1) == 0:
                to_check = not to_check

            if to_check:
                bits.append(hamming_encoding[hamming_index])

            hamming_index += 1
            counter += 1

        is_even = bits.count("1") % 2 == 0

        if is_even:
            parities.append('0')
        else:
            parities.append('1')

    return parities


def get_parity_indexes(parity_bit_no: int):
    """
    This function takes as a parameter the number of parity bits that are needed
    and returns the indexes for the corresponding quantity of parity bits
    :param parity_bit_no:
    :return:
    """
    return [2 ** i - 1 for i in range(parity_bit_no)]


def find_encoded_parity_bits(encoded_length):
    r = 0
    while (2 ** r) < (encoded_length + 1):
        r += 1
    return r


def find_parity_bits(d):
    """
    This function returns how many parity bits do we need for a message of length m
    :param d:
    :return:
    """
    p = 0
    while True:
        if (2 ** p) >= (d + p + 1):
            break
        p += 1
    return p


if __name__ == "__main__":
    main()
