"""
Model definitions
"""
from dataclasses import dataclass
import re
import random

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
@dataclass
class MarkovNode:
    """
    For representing a state in a Markov chain
    """
    state_name: str
    transitions: list
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
    def get_total_num_transitions(self):
        """
        Return the sum of all transitions in the text.
        """
        return (self.text_data.cc_transitions +
                self.text_data.cv_transitions +
                self.text_data.vv_transitions +
                self.text_data.vc_transitions)
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
        Return the number of vowel-consonant transitions found.
        """
        return self.text_data.vc_transitions
    def get_concon_transition_prob(self):
        """
        The probability of C|C
        """
        return ((self.text_data.cc_transitions/self.get_total_num_transitions()) /
                (self.text_data.cc_transitions/self.get_total_num_transitions() +
                 self.text_data.cv_transitions/self.get_total_num_transitions()))
    def get_convow_transition_prob(self):
        """
        The probability of C|V
        """
        return 1-self.get_concon_transition_prob()
    def get_vowvow_transition_prob(self):
        """
        The probability of V|V
        """
        return ((self.text_data.vv_transitions/self.get_total_num_transitions()) /
                (self.text_data.vv_transitions/self.get_total_num_transitions() +
                 self.text_data.vc_transitions/self.get_total_num_transitions()))
    def get_vowcon_transition_prob(self):
        """
        The probability of V|C
        """
        return 1-self.get_vowvow_transition_prob()
    def get_transition_matrix(self):
        """
        Create a transition matrix from the text data.
        """
        x, z = 2, 2
        matrix = [[0.0 for i in range(x)] for j in range(z)]
        matrix[0][0] = self.get_vowvow_transition_prob()
        matrix[0][1] = self.get_vowcon_transition_prob()
        matrix[1][1] = self.get_convow_transition_prob()
        matrix[1][0] = self.get_concon_transition_prob()
        return matrix
    def get_expected_distribution(self):
        """
        This function returns a list of the expected distribution of vowels and consonants
        """
        distributions = []
        distribution_of_vowels = self.get_num_vowels() / self.get_num_alphabet_chars()
        distribution_of_consonants = 1-distribution_of_vowels
        distributions.append(['V', distribution_of_vowels])
        distributions.append(['C', distribution_of_consonants])
        return distributions
class MarkovChain:
    """
    This class is the logical implementation of a Markov chain
    """
    def __init__(self):
        self.current_node = MarkovNode('Placeholder', [])
        self.chain = []
    def text_sequence_to_markov(self, sequence : Sequence):
        """
        Load a given sequence into the Markov chain
        """
        vowel_node = MarkovNode('V', [])
        consonant_node = MarkovNode('C', [])
        vowel_node.transitions.append([sequence.get_vowvow_transition_prob(), vowel_node])
        vowel_node.transitions.append([sequence.get_vowcon_transition_prob(), consonant_node])
        consonant_node.transitions.append([sequence.get_concon_transition_prob(), consonant_node])
        consonant_node.transitions.append([sequence.get_convow_transition_prob(), vowel_node])
        self.current_node = vowel_node
        self.chain.append(self.current_node.state_name)
    def current_state(self):
        """
        Return the current state of the Markov chain
        """
        return self.current_node.state_name
    def current_state_transitions(self):
        """
        Return a list of the transition probabilities from the current state
        """
        transitions = [x[0] for x in self.current_node.transitions]
        return transitions
    def execute_transition(self):
        """
        Execute one transition
        """
        roll = random.random()
        for transition in self.current_node.transitions:
            roll -= transition[0]
            if roll < 0:
                self.current_node = transition[1]
                self.chain.append(self.current_node.state_name)
                return
    def get_length(self):
        """
        Get the length of Markov chain. Should be equivelant to n-1 where n is the number of 
        executions
        """
        return len(self.chain)
    def get_chain(self):
        """
        Return the Markov chain, a timeseries of states over the course of the execution
        """
        return self.chain
    def get_distribution_text(self):
        """
        Return the current probability distribution
        """
        num_of_vowels = self.chain.count('V')
        num_of_chars = self.get_length()
        distributions = []
        distribution_of_vowels = num_of_vowels/num_of_chars
        distribution_of_consonants = 1-distribution_of_vowels
        distributions.append(['V', distribution_of_vowels])
        distributions.append(['C', distribution_of_consonants])
        return distributions
