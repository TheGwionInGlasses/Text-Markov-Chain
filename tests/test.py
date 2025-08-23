from src.models import Filereader

@pytest.fixture
def text():
    file_path = "/tests/test.py"
    filereader = Filereader(file_path)
    return filereader.Sequence()

def test_filereader_loading_correct_length(text):
    assert text.get_length() == 58

def test_filereader_character_counting(text):
    assert text.get_num_consonants() == 35
    assert text.get_num_vowels() == 23

def test_filereader_counting_transitions(text):
    assert text.get_num_concon_transition() == 18
    assert text.get_num_convow_transition() == 17
    assert text.get_num_vowvow_transition() == 5
    assert text.get_num_vowcon_transition() == 17
