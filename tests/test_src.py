"""
Tests
"""

import re
import pytest
from src.models import FileReader, MarkovChain

@pytest.fixture(name="text")
def fixture_text():
    """
    Load the test text file.
    """
    file_path = FileReader("test_file.txt")
    file_path.process_file()
    return file_path.sequence()

@pytest.fixture(name="markov")
def markov_text(text):
    """
    Turn test text file into a markov chain
    """
    markov_chain = MarkovChain()
    markov_chain.text_sequence_to_markov(text)
    return markov_chain

def test_sequence_collecting_all_cons_and_vowels(text):
    """
    Test that the sequence is the correct length
    """
    assert text.get_num_alphabet_chars() == 58

def test_sequence_character_counting(text):
    """
    Test that the sequence contains the correct number of consonants and vowels
    """
    assert text.get_num_consonants() == 35
    assert text.get_num_vowels() == 23

def test_sequence_counting_transitions(text):
    """
    Test that the sequence contains the correct number of transitions i.e V|V or V|C
    """
    assert text.get_num_concon_transition() == 17
    assert text.get_num_convow_transition() == 17
    assert text.get_num_vowvow_transition() == 5
    assert text.get_num_vowcon_transition() == 18

def test_markov_chain_initialse(markov):
    """
    Test that the sequence correctly loaded
    """
    test_transitions = [(5/57)/(5/57 + 18/57), (18/57)/(5/57 + 18/57)]
    assert markov.current_state() == 'V'
    assert markov.current_state_transitions() == test_transitions

def test_markov_chain_execution(markov):
    """
    Test one execution of the markov chain
    """
    markov_chain = markov
    markov_chain.execute_transition()
    str_chain = ''.join(markov_chain.get_chain())
    assert re.match(r"VC|VV", str_chain)
