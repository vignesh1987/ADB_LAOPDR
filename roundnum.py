import re

# specify the path to your text file
file_path = '11111.txt'

# read the text file
with open(file_path, 'r') as file:
    text = file.read()

# define a function to round numbers
def round_number(match):
    number = float(match.group())
    return "{:.4f}".format(number)

# use a regular expression to find all numbers with a decimal point
text = re.sub(r'\d+\.\d+', round_number, text)

# write the modified text back to the text file
with open(file_path, 'w') as file:
    file.write(text)
