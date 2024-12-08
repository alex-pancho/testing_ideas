
"""
Write words and char counter
Input (stdin)

    Most of the lists and dicts and stuff were fine for me…but when it got to Classes section
    5

Expected Output

    Top 5 letters:
    t: 10
    s: 9
    e: 8
    o: 6
    f: 5

    Top 5 words:
    and: 2
    but: 1
    classes: 1
    dicts: 1
    fine: 1

Input (stdin)

    The sun sets behind the mountains, painting the sky in hues of orange and pink, casting a serene glow over the tranquil landscape below.
    3

Expected Output

    Top 3 letters:
    e: 14
    n: 14
    a: 9

    Top 3 words:
    the: 4
    a: 1
    and: 1
"""

import os
from collections import Counter
import re
def get_top_letters_and_words(text, num):
    text = re.sub(r'[^a-zA-Z\s]', '', text).lower()
    letters = [ch for ch in text if ch != ' ']
    letters_cnt = Counter(letters)
    top_letters = letters_cnt.most_common(num)
    
    words = text.split()
    words_cnt = Counter(words)
    top_alptha = sorted(words_cnt.items(), key=lambda x: (-x[1], x[0]))
    top_words = top_alptha[:num]
    print(top_alptha)
    letters_out = f"Top {num} letters:\n"
    letters_str = "\n".join([f"{letter}: {freq}" for letter, freq in top_letters])
    words_out = f"Top {num} words:\n"
    words_str = "\n".join([f"{word}: {freq}" for word, freq in top_words])
    return letters_out+letters_str+"\n", words_out+words_str

if __name__ == "__main__":
    # fptr = open("tt.txt", 'w')
    text = input("t:")
    num = int(input("c:"))
    letters,words = get_top_letters_and_words(text,num)
    print(letters)
    # fptr.write(letters)
    # fptr.write("\n")
    print(words)
    # fptr.write(words)
    # fptr.close()
