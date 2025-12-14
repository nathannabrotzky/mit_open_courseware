import io
import math
import random
import string

VOWELS:str = 'aeiou'
CONSONANTS:str = 'bcdfghjklmnpqrstvwxyz'
HAND_SIZE:int = 7

SCRABBLE_LETTER_VALUES:dict[str,int] = {
    'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1, 'f': 4, 'g': 2,
    'h': 4, 'i': 1, 'j': 8, 'k': 5, 'l': 1, 'm': 3, 'n': 1, 'o': 1, 'p': 3,
    'q': 10, 'r': 1, 's': 1, 't': 1, 'u': 1, 'v': 4, 'w': 4, 'x': 8, 'y': 4, 'z': 10
}

WORDLIST_FILENAME:str = "words.txt"

def load_words() -> list[str]:
    ret:None = print("Loading word list from file...")
    inFile:io.TextIOWrapper = open(WORDLIST_FILENAME, 'r')
    wordlist:list[str] = []
    for line in inFile:
        wordlist.append(line.strip().lower())
    ret:None = print("  ", len(wordlist), "words loaded.")
    return wordlist

def get_frequency_dict(sequence:str) -> dict[str,int]:
    freq:dict[str,int] = {}
    for x in sequence:
        freq[x] = freq.get(x,0) + 1
    return freq
	
def get_word_score(word:str, n:int) -> int:
    first_comp:int = 0
    for c in word.lower():
        first_comp += SCRABBLE_LETTER_VALUES.get(c,0)
    second_comp:int = max(1, (7 * len(word) - 3 * (n - len(word))))
    return first_comp * second_comp

def display_hand(hand):
    for letter in hand.keys():
        for j in range(hand[letter]):
             print(letter, end=' ')
    print()

def deal_hand(n):
    hand={"*":1}
    num_vowels:int = int(math.ceil(n / 3)) - 1
    for i in range(num_vowels):
        x = random.choice(VOWELS)
        hand[x] = hand.get(x, 0) + 1
    for i in range(num_vowels + 1, n):    
        x = random.choice(CONSONANTS)
        hand[x] = hand.get(x, 0) + 1
    return hand

def update_hand(hand:dict[str, int], word:str) -> dict[str,int]:
    new_hand:dict[str,int] = {}
    word_freq = get_frequency_dict(word.lower())
    for k in hand.keys():
        if hand[k] - word_freq.get(k,0) > 0:
            new_hand[k] = hand[k] - word_freq.get(k,0)
        elif k not in word_freq.keys():
            new_hand[k] = hand[k]
    return new_hand

def is_valid_word(word:str, hand:dict[str,int], word_list:list[str]) -> bool:
    wildcard = word.find("*")
    if wildcard == -1 and word.lower() not in word_list:
        return False
    if wildcard != -1:
        trigger = 0
        for c in "aeiou":
            if word.lower().replace("*",c) in word_list:
                trigger = 1
                break
        if trigger == 0:
            return False
    word_freq:dict[str,int] = get_frequency_dict(word.lower())
    for k in word_freq.keys():
        if k not in hand.keys():
            return False
        if word_freq[k] > hand.get(k,0):
            return False
    return True

def calculate_handlen(hand:dict[str,int]) -> int:
    return sum(list(hand.values()))

def play_hand(hand:dict[str,int], word_list:list[str]) -> int:
    total_score:int = 0
    while calculate_handlen(hand) > 0:
        print(f"Current Hand: {display_hand(hand)}")
        word:str = input('Enter word, or "!!" to indicate that you are finished: ')
        if word == "!!":
            break
        else:
            if is_valid_word(word, hand, word_list):
                score:int = get_word_score(word, calculate_handlen(hand))
                print(f'"{word}" earned {score} points.')
                total_score += score
            else:
                print("That is not a valid word. Please choose another word.")
            hand = update_hand(hand, word)
    print(f"Total score: {total_score} points.")
    return total_score

#
# Problem #6: Playing a game
# 
def substitute_hand(hand:dict[str,int], letter:str) -> dict[str,int]:
    new_hand:dict[str,int] = hand.copy()
    letters:str = VOWELS + CONSONANTS
    for l in letters:
        if l in hand.keys():
            letters = letters.replace(l, "")
    if letter in hand.keys():
        new_letter:str = random.choice(letters)
        new_hand[new_letter] = new_hand[letter]
        del new_hand[letter]
    return new_hand  
    
def play_game(word_list:list[str]):
    replay:str = "no"
    total_score:int = 0
    total_hands:int = int(input("Enter total number of hands: "))
    i:int = 0
    while i < total_hands:
        if replay.lower() == "yes":
            hand:dict[str,int] = hand
        else:
            hand:dict[str,int] = deal_hand(HAND_SIZE)
            print(f"Current hand: {display_hand(hand)}")
            replace:str = input("Would you like to substitute a letter? ")
            if replace.lower() == "yes":
                letter:str = input("Which letter would you like to replace: ")
                hand = substitute_hand(hand, letter)
        total_score += play_hand(hand, word_list)
        print("----------")
        if replay.lower() != "yes":
            replay:str = input("Would you like to replay the hand? ")
        if replay.lower() != "yes":
            i += 1
    print(f"Total score over all hands: {total_score}")
    
if __name__ == '__main__':
    word_list = load_words()
    play_game(word_list)
