import argparse
from src.models import FileReader, Sequence, MarkovChain

parser = argparse.ArgumentParser(prog="Text Markov Chain", description="A program which can be used to calculate the stationary distribution of vowels and consonants in a provided text")
parser.add_argument('filename')
parser.add_argument('-c', '--count', type=int, default=1000, help="The number of times to run the Markov Chain")
args = vars(parser.parse_args())
fileReader = FileReader(args['filename'])
fileReader.process_file()
sequence = fileReader.sequence()
expected_distribution = sequence.get_expected_distribution()
markovChain = MarkovChain()
markovChain.text_sequence_to_markov(sequence)
for i in range(args['count']):
    markovChain.execute_transition()
probability_distribution = markovChain.get_distribution()
output = f"The expected distribution of vowels to consonants are {expected_distribution[0][1]}/{expected_distribution[1][1]}.\nThe actual distribution was {probability_distribution[0][1]}/{probability_distribution[1][1]} after running the Markov Chain over {args['count']} itterations.\nBear in mind, if this is not close to the expected distribution, perhaps the number of itterations ran was too low."
print(output)