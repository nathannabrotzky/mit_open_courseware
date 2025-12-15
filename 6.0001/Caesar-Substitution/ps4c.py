import io
import string
from ps4a import get_permutations

def load_words(file_name:str) -> list[str]:
    print("Loading word list from file...")
    inFile:io.TextIOWrapper = open(file_name, 'r')
    wordlist:list[str] = []
    for line in inFile:
        wordlist.extend([word.lower() for word in line.split(' ')])
    print("  ", len(wordlist), "words loaded.")
    return wordlist

def is_word(word_list:list[str], word:str) -> bool:
    word:str = word.lower()
    word:str = word.strip(" !@#$%^&*()-_+={}[]|\\:;'<>?,./\"")
    return word in word_list

WORDLIST_FILENAME = 'words.txt'

VOWELS_LOWER = 'aeiou'
VOWELS_UPPER = 'AEIOU'
CONSONANTS_LOWER = 'bcdfghjklmnpqrstvwxyz'
CONSONANTS_UPPER = 'BCDFGHJKLMNPQRSTVWXYZ'

class SubMessage(object):
    def __init__(self, text:str):
        self.message_text:str = text
        self.valid_words:list[str] = load_words(WORDLIST_FILENAME)
    
    def get_message_text(self:SubMessage) -> str:
        return self.message_text

    def get_valid_words(self:SubMessage) -> list[str]:
        return self.valid_words.copy()
                
    def build_transpose_dict(self:SubMessage, vowels_permutation:str) -> dict[str, str]:
        result_dict:dict[str, str] = {}
        for c in CONSONANTS_LOWER + CONSONANTS_UPPER:
            result_dict[c] = c
        for i, c in enumerate(VOWELS_LOWER):
            result_dict[c] = vowels_permutation[i].lower()
        for i, c in enumerate(VOWELS_UPPER):
            result_dict[c] = vowels_permutation[i].upper()
        return result_dict
    
    def apply_transpose(self:SubMessage, transpose_dict:dict[str,str]) -> str:
        transposed_text:str = ''
        for c in self.message_text: 
            if c in transpose_dict.keys():
                transposed_text += transpose_dict[c]
            else:
                transposed_text += c
        return transposed_text
        
class EncryptedSubMessage(SubMessage):
    def __init__(self:EncryptedSubMessage, text:str):
        super().__init__(text)

    def decrypt_message(self:EncryptedSubMessage) -> str:
        current_best_count:int = 0
        best_decrypted_message:str = self.message_text
        vowel_permutations:list[str] = get_permutations(VOWELS_LOWER)
        for permutation in vowel_permutations:
            transpose_dict:dict[str, str] = self.build_transpose_dict(permutation)
            decrypted_text:str = self.apply_transpose(transpose_dict)
            words:list[str] = decrypted_text.split(' ')
            valid_word_count:int = 0
            for word in words:
                if is_word(self.valid_words, word):
                    valid_word_count += 1
            if valid_word_count > current_best_count:
                current_best_count = valid_word_count
                best_decrypted_message = decrypted_text
        return best_decrypted_message

if __name__ == '__main__':

    # Example test case
    message = SubMessage("Hello World!")
    permutation = "eaiuo"
    enc_dict = message.build_transpose_dict(permutation)
    print("Original message:", message.get_message_text(), "Permutation:", permutation)
    print("Expected encryption:", "Hallu Wurld!")
    print("Actual encryption:", message.apply_transpose(enc_dict))
    enc_message = EncryptedSubMessage(message.apply_transpose(enc_dict))
    print("Decrypted message:", enc_message.decrypt_message())
     
    #TODO: WRITE YOUR TEST CASES HERE
