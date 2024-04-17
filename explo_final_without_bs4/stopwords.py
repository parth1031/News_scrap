import sys
import re


def stop_word_lis():
    f= open(r"stop_words_en.txt")
    fh = f.read()
    stop_words = []
    for word in fh:
      stop_words.append(word)
    
    return stop_words

def read_text_file():
    lines = []
    with open(r"class_names.txt") as file:
        for line in file:
            lines.append(line.strip())
    return lines