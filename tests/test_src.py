"""
Tests
"""

import pytest
from src.models import FileReader

@pytest.fixture(name="text")
def ficture_text():
    """
    Load the test text file.
    """
    file_path = FileReader("test_file.txt")
    file_path.process_file()
    return file_path.sequence()

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
