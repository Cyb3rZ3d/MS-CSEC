from mrjob.job import MRJob
from mrjob.step import MRStep
import re

# Regular expression pattern to extract HTTP status codes
LOG_PATTERN = re.compile(r'"\s*\w+\s+[^"]+"\s+(\d+)\s+\d+')

class MRTopStatusCodes(MRJob):

    def mapper(self, _, line):
        """Extracts HTTP status codes from each log line."""
        match = LOG_PATTERN.search(line)
        if match:
            yield match.group(1), 1

    def combiner(self, status_code, counts):
        """Aggregates counts locally before shuffling."""
        yield status_code, sum(counts)

    def reducer(self, status_code, counts):
        """Aggregates counts globally."""
        yield None, (sum(counts), status_code)

    def reducer_top_10(self, _, status_counts):
        """Sorts and selects the top 10 most frequent status codes."""
        sorted_counts = sorted(status_counts, reverse=True, key=lambda x: x[0])
        for count, status_code in sorted_counts[:10]:
            yield status_code, count

    def steps(self):
        return [
            MRStep(mapper=self.mapper,
                   combiner=self.combiner,
                   reducer=self.reducer),
            MRStep(reducer=self.reducer_top_10)
        ]

if __name__ == '__main__':
    MRTopStatusCodes.run()
