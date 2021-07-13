#!/usr/bin/python3
import sys
import enchant
import csv
import codecs

# The English library to validate words
d = enchant.Dict("en_US")

# The minimum length of the crib word
MIN_CRIB_LEN = 3

# The minimun length of the internal partial matching word
# This should be less or equal to MIN_CRIB_LEN
MIN_INTERNAL_LEN = 3


# Load the 5,000 common English vocabulary library as crib word candidates
with open('FrequentEnglishWordList.csv', 'r') as f:
	reader = csv.reader(f)
	crib_list = list(reader)
# Remove the header of the list file
crib_list = crib_list[1:]

# This function is credit to https://github.com/SpiderLabs/cribdrag
# @param: 	ctext	- 	The cipher text to be crib dragged
# @param: 	crib 	- 	The crib word to drag on the cipher text
# @return: 	results - 	A list of result that generated from a or partial match
#						of the crib word on the cipher text. Each result is
#						ensured to be an English word and contain letters only
def sxor(ctext, crib):
	results = []
	single_result = ''
	crib_len = len(crib)
	positions = len(ctext)-crib_len+1
	for index in range(positions):
		single_result = ''
		for a,b in zip(ctext[index:index+crib_len],crib):
			single_result += chr(ord(a) ^ ord(b))

		# Check the word partially, to see whether it conatins an English word
		result_length = len(single_result)
		if (result_length >= MIN_INTERNAL_LEN):
			for i in range(0, result_length - MIN_INTERNAL_LEN):
				for j in range(i + MIN_INTERNAL_LEN, result_length):
					result_partial = single_result[i:j]
					if (result_partial.isalpha()):
						if (d.check(result_partial)):
							results.append(result_partial + "(" + str(index) + ")")

		# Check the whole word, to see whether it is an English word
		if (single_result.isalpha()):
			if(d.check(single_result)):
				results.append(single_result + "(" + str(index) + ")")
		
	return results

# This function executes the crib dragging of a single word on the cipher text
# And write/append the result to the target output file
def writeResultGivenCrib(ctext, crib):
	results = sxor(ctext, crib)
	results_len = len(results)
	# Write to the output (Append)
	with open(FILE_NAME, "a") as text_file:
		text_file.write(crib + "(" + str(results_len) + "): [ " + ', '.join(results) + " ]\n")

# Provide the Hexidecimal version of cipher_text here
CIPHER_HEX = b"0x1b0xe0x90x4d0x150x1b0x450x630xc0x10x1b0x170x60x550x00x3d0x00x1e0x450x110x4f0x1a0xf0x530x410x150x430x170x1d0x80x550x3e0xe0xd0x40x80x00x200xe0x60x00x520x190xc"
# Decode the hexidecimal cipher text
cipher_text = codecs.decode(CIPHER_HEX)
# File Name
FILE_NAME = "auto_output.txt"

# Clear the content of the output file before starting to append
open(FILE_NAME, 'w').close()

# Iterate through the crib word list
for ind, crib in enumerate(crib_list):
	# Get the column of the word
	crib_word = crib[1]
	print(str(ind) + ": " + crib_word)
	# Write the result to the file
	if (len(crib_word) >= MIN_CRIB_LEN):
		writeResultGivenCrib(cipher_text, crib_word)
