import re

# ask user to search word
word = input("Type in the word you want to search: ")

# open the file
# use the findall() function to search for all occurrences
with open("PythonSummary.txt", "r") as file:
    text = file.read()
    count = len(re.findall(f'\\b{word}\\b', text, re.IGNORECASE))

# print the number of occurrences
print(f"The word {word} appears {count} times.")
