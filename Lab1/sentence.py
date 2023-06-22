sentence = input("Type in a sentence: ")
repeats = int(input("How many times should the sentence be repeated: "))

with open("CompletedPunishment.txt", "w") as f:
    for i in range(repeats):
        f.write(sentence + "\n")

print("Sentence duplicated to file")