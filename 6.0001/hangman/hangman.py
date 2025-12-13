import io
import random
import string

WORDLIST_FILENAME:str = "words.txt"

def load_words() -> list[str]:
    ret:None = print("Loading word list from file...")
    if ret is not None:
        raise Exception("Failed to execute print statement")
    del ret
    inFile:io.TextIOWrapper = open(WORDLIST_FILENAME, 'r')
    if not isinstance(inFile, io.TextIOWrapper):
        raise Exception("Failed to open word list file")
    line:str = inFile.readline()
    if len(line) == 0:
        raise Exception("Word list is empty")
    ret:None = inFile.close()
    if ret is not None:
        raise Exception("Failed to close the file")
    del ret
    del inFile
    if not isinstance(line, str):
        raise Exception("Failed to read word list")
    wordlist:list[str] = line.split()
    del line
    if not isinstance(wordlist, list):
        raise Exception("Failed to split word list")
    ret:None = print("  ", len(wordlist), "words loaded.")
    if ret is not None:
        raise Exception("Failed to execute print statement")
    del ret
    return wordlist

def choose_word(wordlist:list[str]) -> str:
    return random.choice(wordlist)

wordlist:list[str] = load_words()
if not isinstance(wordlist, list):
    raise Exception("Failed to get word list.")

def is_word_guessed(secret_word:str, letters_guessed:list[str]) -> bool:
    for key in set(secret_word):
        if key not in letters_guessed:
            return False
    return True

def get_guessed_word(secret_word:str, letters_guessed:list[str]) -> str:
    new_word:str = ""
    if not isinstance(new_word, str):
        raise Exception("Failed to copy secret word")
    for c in secret_word:
        if c not in letters_guessed:
            new_word = new_word + "_"
        else:
            new_word = new_word + c
    return new_word

def get_available_letters(letters_guessed:list[str]) -> str:
    result:str = string.ascii_lowercase
    if not isinstance(result,str):
        raise Exception("Failed to generate alphabet")
    for c in string.ascii_lowercase:
        if c in letters_guessed:
            result = result.replace(c,"")
    return result

def hangman(secret_word):
    print("Welcome to the game Hangman!")
    print(f"I am thinking of a word that is {len(secret_word)} letters long.")
    guesses:int = 6
    warnings:int = 3
    letters_guessed:list[str] = []
    current_word:str = get_guessed_word(secret_word, letters_guessed)
    game_run:int = 1
    while (game_run == 1 and guesses > 0):
      print("-------------")
      print(f"You have {guesses} guesses left.")
      print(f"Available letters: {get_available_letters(letters_guessed)}")
      letter:str = input("Please guess a letter: ")
      if letter in letters_guessed:
          warnings -= 1
          print(f"Oops! You already guessed that letter. You have {max(warnings,0)} warnings left: {current_word}")
          if warnings < 0:
              print(f"Ran out of warnings. Losing a guess.")
              guesses -= 1
          continue
      elif not letter.isalpha():
          warnings -= 1
          print(f"Oops! You need to guess a lowercase letter. You have {max(warnings,0)} warnings left: {current_word}")
          if warnings < 0:
              print(f"Ran out of warnings. Losing a guess.")
              guesses -= 1
          continue
      elif len(letter) != 1:
          warnings -= 1
          print(f"Oops! You can only enter one character at-a-time. You have {max(warnings,0)} warnings left: {current_word}")
          if warnings < 0:
              print(f"Ran out of warnings. Losing a guess.")
              guesses -= 1
          continue
      else:
        letters_guessed.append(letter.lower())
      new_word = get_guessed_word(secret_word, letters_guessed)
      if new_word == current_word:
          print(f"Oops! That letter is not in my word: {current_word}")
          if letter in "aeiou":
            guesses -= 2
          else:
            guesses -= 1
      else:
          print(f"Good guess: {new_word}")
          current_word = new_word
      game_run = 0 if is_word_guessed(secret_word,letters_guessed) else 1
    if game_run == 1:
        print("Ran out of guesses. Better luck next time.")
        print(f"The secret word was: {secret_word}")
    else:
        print("Congratulations! You guessed my secret word!")
        score:int = len(set(secret_word)) * guesses
        print(f"Your total score for this game is: {score}.")

def match_with_gaps(my_word:str, other_word:str) -> bool:
    if len(my_word.strip()) != len(other_word.strip()):
        return False
    distinct:str = set(my_word)
    for i, c in enumerate(my_word):
        if c != other_word[i] and c != "_":
            return False
        if c == "_" and other_word[i] in distinct:
            return False
    return True

def show_possible_matches(my_word:str) -> None:
    for word in wordlist:
        if match_with_gaps(my_word, word):
            print(word, end=" ")
    print("")

def hangman_with_hints(secret_word):
    print("Welcome to the game Hangman!")
    print(f"I am thinking of a word that is {len(secret_word)} letters long.")
    guesses:int = 6
    warnings:int = 3
    letters_guessed:list[str] = []
    current_word:str = get_guessed_word(secret_word, letters_guessed)
    game_run:int = 1
    while (game_run == 1 and guesses > 0):
      print("-------------")
      print(f"You have {guesses} guesses left.")
      print(f"Available letters: {get_available_letters(letters_guessed)}")
      letter:str = input("Please guess a letter: ")
      if letter in letters_guessed:
          warnings -= 1
          print(f"Oops! You already guessed that letter. You have {max(warnings,0)} warnings left: {current_word}")
          if warnings < 0:
              print(f"Ran out of warnings. Losing a guess.")
              guesses -= 1
          continue
      elif letter == "*":
          print("Possible words matches are: ")
          show_possible_matches(current_word)
          continue
      elif not letter.isalpha():
          warnings -= 1
          print(f"Oops! You need to guess a lowercase letter. You have {max(warnings,0)} warnings left: {current_word}")
          if warnings < 0:
              print(f"Ran out of warnings. Losing a guess.")
              guesses -= 1
          continue
      elif len(letter) != 1:
          warnings -= 1
          print(f"Oops! You can only enter one character at-a-time. You have {max(warnings,0)} warnings left: {current_word}")
          if warnings < 0:
              print(f"Ran out of warnings. Losing a guess.")
              guesses -= 1
          continue
      else:
        letters_guessed.append(letter.lower())
      new_word = get_guessed_word(secret_word, letters_guessed)
      if new_word == current_word:
          print(f"Oops! That letter is not in my word: {current_word}")
          if letter in "aeiou":
            guesses -= 2
          else:
            guesses -= 1
      else:
          print(f"Good guess: {new_word}")
          current_word = new_word
      game_run = 0 if is_word_guessed(secret_word,letters_guessed) else 1
    if game_run == 1:
        print("Ran out of guesses. Better luck next time.")
        print(f"The secret word was: {secret_word}")
    else:
        print("Congratulations! You guessed my secret word!")
        score:int = len(set(secret_word)) * guesses
        print(f"Your total score for this game is: {score}.")

# When you've completed your hangman_with_hint function, comment the two similar
# lines above that were used to run the hangman function, and then uncomment
# these two lines and run this file to test!
# Hint: You might want to pick your own secret_word while you're testing.


if __name__ == "__main__":
    # pass

    # To test part 2, comment out the pass line above and
    # uncomment the following two lines.
    
    # secret_word = choose_word(wordlist)
    # hangman(secret_word)

###############
    
    # To test part 3 re-comment out the above lines and 
    # uncomment the following two lines. 
    
    secret_word = choose_word(wordlist)
    hangman_with_hints(secret_word)
