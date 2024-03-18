import sys
import re


def stop_word_lis():
    f= open(r"C:\Users\Prakhar\OneDrive\Desktop\stop_words_en.txt")
    fh = f.read()
    stop_words = []
    for word in fh:
      stop_words.append(word)
    
    return stop_words
