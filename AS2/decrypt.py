import os
import sys
import subprocess
import random
from typing import final


def writeToFile(padding_check):
    # Write to file
    func = open("padding_check", "wb")
    func.write(padding_check)
    func.close()


def replaceR(index, padding_check):
    padding_check[index] = padding_check[random.randrange(
        index, len(padding_check), 4)]
    writeToFile(padding_check)
    return padding_check


def decryptByte(y_n, index, random_block):

    # Append ciphertext with random block
    padding_check = random_block + y_n[-index]

    writeToFile(padding_check)

    # Call oracle
    output = 0
    while output == 0:
        output = int(subprocess.check_output(
            ['python3', 'oracle.py', 'padding_check']))
        if output == 0:
            padding_check[15] += 1
            writeToFile(padding_check)

    # Replace R from random block
    k_indx = 0
    while k_indx < 15:
        padding_check = replaceR(k_indx, padding_check)
        output = int(subprocess.check_output(
            ['python3', 'oracle.py', 'padding_check']))
        if output == 1:
            k_indx += 1
        elif output == 0:
            break

    # Obtain last byte of X_n
    if k_indx == 15:
        # Oracle always yes
        Dy_n = padding_check[15] ^ 1
        final_byte = Dy_n ^ y_n[-index-1][15]
        return final_byte, Dy_n, k_indx
    elif k_indx < 15:
        # Oracle said no somewhere
        Dy_n = padding_check[15] ^ (17 - k_indx)
        final_byte = Dy_n ^ y_n[-index-1][15]
        return final_byte, Dy_n, k_indx


def main():

    f = open(sys.argv[1], "rb")
    ciphertext = f.read()
    f.close()

    # Set array with block of 16 bytes
    y_n = []
    for i in range(0, len(ciphertext), 16):
        y_n.append(ciphertext[i:i+16])

    number_of_blocks = len(y_n)

    # Obtain all the byte values for X_n
    x_n = []
    dy_n = []

    for i in range(len(y_n)):
        x_n.append(bytearray(16))
        dy_n.append(bytearray(16))

    start = 0
    index = -1

    while start < number_of_blocks - 1:
        # Generate random block with 15 bytes, followed by a byte i, initially i = 0
        size = 15
        random_block = bytearray(os.urandom(size))
        random_block.append(0)

        # This will be generalized inside the loop to go through all the loops
        x_n[index][-1], dy_n[index][-1], k = decryptByte(
            y_n, -index, random_block)

        ########### Decrypt Block ###########
        while k > 0:
            # Step 1
            new_r = bytearray(16)
            for i in range(k):
                new_r[i] = random_block[i]
            new_r[k - 1] = 0

            for i in range(k, 16):
                new_r[i] = dy_n[index][i] ^ (17 - k)

            padding_check = new_r + y_n[index]
            writeToFile(padding_check)

            # Step 2, 3, 4
            output = 0
            while output == 0:
                output = int(subprocess.check_output(
                    ['python3', 'oracle.py', 'padding_check']))
                if output == 0:
                    padding_check[k - 1] += 1
                    writeToFile(padding_check)

            dy_n[index][k - 1] = padding_check[k - 1] ^ (17 - k)
            x_n[index][k - 1] = dy_n[index][k - 1] ^ y_n[index - 1][k - 1]
            k -= 1
        index -= 1
        start += 1

    decoded_message = ""
    x_n.pop(0)
    for i in range(len(x_n)):
        decoded_message += x_n[i].decode()

    print(decoded_message, end='')


if __name__ == "__main__":
    main()
