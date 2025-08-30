"""
Model definitions
"""
from dataclasses import dataclass
import re

vowel_or_consonant = {
    "a" : "V",
    "e" : "V",
    "i" : "V",
    "o" : "V",
    "u" : "V",
    "b" : "C",
    "c" : "C",
    "d" : "C",
    "f" : "C",
    "g" : "C",
    "h" : "C",
    "j" : "C",
    "k" : "C",
    "l" : "C",
    "m" : "C",
    "n" : "C",
    "p" : "C",
    "q" : "C",
    "r" : "C",
    "s" : "C",
    "t" : "C",
    "v" : "C",
    "w" : "C",
    "x" : "C",
    "y" : "C",
    "z" : "C",
}
@dataclass
class TextData:
    """
    For keeping track of text data
    """
    num_vowels: int
    num_consonants: int
    cc_transitions: int
    cv_transitions: int
    vv_transitions: int
    vc_transitions: int
class FileReader:
    """
    A FileReader. Contains the method for reading in a file.
    """
    def __init__(
        self, file_path
    ):
        self.file_path = file_path
        self.text = ""
    def process_file(self):
        """
        Read the contents of the file_path
        """
        with open(self.file_path, encoding="utf-8") as f:
            unprocessed_text = f.read()
            self.text = re.sub(r'[^a-zA-Z]', '', unprocessed_text)
    def sequence(self):
        """
        Return a sequence
        """
        if self.text:
            return Sequence(self.text)
        return ""
class Sequence:
    """
    The data processor for TextData Class.
    """
    def __init__(self, sequence : str):
        lower = sequence.lower()
        left = right = n_vow = n_con = n_cc_tran = n_cv_tran = n_vv_tran = n_vc_tran = 0
        while right < len(lower):
            right_char = vowel_or_consonant.get(lower[right])
            if right_char == "V":
                n_vow += 1
            if right_char == "C":
                n_con += 1
            if left != right:
                left_char = vowel_or_consonant.get(lower[left])
                if(left_char == "C" and right_char == "C"):
                    n_cc_tran += 1
                if(left_char == "C" and right_char == "V"):
                    n_cv_tran += 1
                if(left_char == "V" and right_char == "V"):
                    n_vv_tran += 1
                if(left_char == "V" and right_char == "C"):
                    n_vc_tran += 1
                left = right
            right += 1
        self.text_data = TextData(n_vow, n_con, n_cc_tran, n_cv_tran, n_vv_tran, n_vc_tran)
    def get_num_alphabet_chars(self):
        """
        Returns the total number of vowels and consonants found.
        """
        return self.text_data.num_vowels + self.text_data.num_consonants
    def get_num_consonants(self):
        """
        Return the number of consonants found
        """
        return self.text_data.num_consonants
    def get_num_vowels(self):
        """
        Return the number of vowels found
        """
        return self.text_data.num_vowels
    def get_num_concon_transition(self):
        """
        Return the number of consonant-consonant transitions found
        """
        return self.text_data.cc_transitions
    def get_num_convow_transition(self):
        """
        Return the number of consonant-vowel transitions found
        """
        return self.text_data.cv_transitions
    def get_num_vowvow_transition(self):
        """
        Return the number of vowel-vowel transitions found
        """
        return self.text_data.vv_transitions
    def get_num_vowcon_transition(self):
        """
        Return the number of vowel-consonant transitions found
        """
        return self.text_data.vc_transitions
class MarkovChain:
    """
    This class is the logical implementation of a Markov chain
    """
    def text_sequence_to_markov(self, sequence : Sequence):
        """
        Load a given sequence into the Markov chain
        """
        return NotImplementedError
    def current_state(self):
        """
        Return the current state of the Markov chain
        """
        return NotImplementedError
    def current_state_transitions(self):
        """
        Return a list of the transition probabilities from the current state
        """
        return NotImplementedError    
    def execute_transition(self):
        """
        Execute one transition
        """
        return NotImplementedError
