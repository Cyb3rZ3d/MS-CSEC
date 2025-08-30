from mrjob.job import MRJob
import re

WORD_RE = re.compile(r"\b\w+\b")  # Regular expression to extract words

class WordCount(MRJob):

    def mapper(self, _, line):
        for word in WORD_RE.findall(line.lower()):  # Convert to lowercase and extract words
            yield word, 1  # Emit each word with count 1

    def reducer(self, word, counts):
        yield word, sum(counts)  # Sum all occurrences of each word

if __name__ == '__main__':
    WordCount.run()

