from mrjob.job import MRJob
from mrjob.step import MRStep
import re

class MRTopHTTPStatusCodes(MRJob):

    # Mapper function to extract HTTP status codes
    def mapper(self, _, line):
        # Define the pattern to capture the HTTP status code (typically the 9th field in CLF)
        match = re.search(r'"\s(\d{3})\s', line)
        if match:
            status_code = match.group(1)
            yield status_code, 1

    # Reducer function to count occurrences of each HTTP status code
    def reducer(self, key, values):
        # Sum all occurrences of the status code
        total = sum(values)
        yield key, total

    # Final reducer to sort and output the top 10 results
    def reducer_find_top_10(self, _, status_counts):
        status_counts_list = list(status_counts)
        
        # Sort by count (descending) and return the top 10
        top_10 = sorted(status_counts_list, key=lambda x: x[1], reverse=True)[:10]
        
        # Yield the top 10 status codes with counts
        for status_code, count in top_10:  # Fix here: unpack each tuple as (status_code, count)
            yield status_code, count

    def steps(self):
        return [
            MRStep(mapper=self.mapper,
                   reducer=self.reducer),
            MRStep(reducer=self.reducer_find_top_10)
        ]

if __name__ == '__main__':
    MRTopHTTPStatusCodes.run()
