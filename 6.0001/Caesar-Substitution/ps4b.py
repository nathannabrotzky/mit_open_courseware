import io
import string

### HELPER CODE ###
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

def get_story_string() -> str:
    f:io.TextIOWrapper = open("story.txt", "r")
    story:str = str(f.read())
    f.close()
    return story

WORDLIST_FILENAME = 'words.txt'

class Message(object):
    def __init__(self, text:str):
        self.message_text:str = text
        self.valid_words:list[str] = load_words(WORDLIST_FILENAME)

    def get_message_text(self:Message) -> str:
        return self.message_text

    def get_valid_words(self:Message) -> list[str]:
        return self.valid_words.copy()

    def build_shift_dict(self:Message, shift:int) -> dict[str, str]:
        lowercase_letters:str = string.ascii_lowercase
        uppercase_letters:str = string.ascii_uppercase
        result_dict:dict[str, str] = {}
        for i, c in enumerate(lowercase_letters):
            if i + shift < 26:
                result_dict[c] = lowercase_letters[i + shift]
            else:
                result_dict[c] = lowercase_letters[(i + shift) - 26]
        for i, c in enumerate(uppercase_letters):
            if i + shift < 26:
                result_dict[c] = uppercase_letters[i + shift]
            else:
                result_dict[c] = uppercase_letters[(i + shift) - 26]
        return result_dict
    
    def apply_shift(self:Message, shift:int) -> str:
        shift_dict:dict[str, str] = self.build_shift_dict(shift)
        shifted_message:str = ''
        for c in self.message_text: 
            if c in shift_dict.keys():
                shifted_message += shift_dict[c]
            else:
                shifted_message += c
        return shifted_message

class PlaintextMessage(Message):
    def __init__(self:PlaintextMessage, text:str, shift:int):
        super().__init__(text)
        self.shift:int = shift
        self.encryption_dict:dict[str, str] = self.build_shift_dict(shift)
        self.message_text_encrypted:str = self.apply_shift(shift)

    def get_shift(self:PlaintextMessage) -> int:
        return self.shift

    def get_encryption_dict(self:PlaintextMessage) -> dict[str, str]:
        return self.encryption_dict.copy()

    def get_message_text_encrypted(self:PlaintextMessage) -> str:
        return self.message_text_encrypted

    def change_shift(self:PlaintextMessage, shift:int):
        self.shift:int = shift
        self.encryption_dict:dict[str, str] = self.build_shift_dict(shift)
        self.message_text_encrypted:str = self.apply_shift(shift)

class CiphertextMessage(Message):
    def __init__(self:CiphertextMessage, text:str):
        super().__init__(text)

    def decrypt_message(self:CiphertextMessage) -> tuple[int, str]:
        current_valid_word_count:int = 0
        correct_shift:int = 0
        decrypted_text:str = ''
        for i in range(25):
            decrypted_message:str = self.apply_shift(26 - i - 1)
            words:list[str] = decrypted_message.split(' ')
            valid_word_count:int = 0
            for word in words:
                if is_word(self.valid_words, word):
                    valid_word_count += 1
            if valid_word_count > current_valid_word_count:
                correct_shift = valid_word_count
                decrypted_text = decrypted_message
        return (26 - correct_shift - 1, decrypted_text)

if __name__ == '__main__':

   #Example test case (PlaintextMessage)
   plaintext = PlaintextMessage('hello', 2)
   print('Expected Output: jgnnq')
   print('Actual Output:', plaintext.get_message_text_encrypted())

   #Example test case (CiphertextMessage)
   ciphertext = CiphertextMessage('jgnnq')
   print('Expected Output:', (24, 'hello'))
   print('Actual Output:', ciphertext.decrypt_message())
