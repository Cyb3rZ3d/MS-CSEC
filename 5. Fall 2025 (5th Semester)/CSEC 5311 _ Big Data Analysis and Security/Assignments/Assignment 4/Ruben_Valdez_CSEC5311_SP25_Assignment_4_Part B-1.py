#Ruben_Valdez_CSEC5311_SP25_Assignment_4_Part B-1.py
from mrjob.job import MRJob
from mrjob.step import MRStep
import re
import sys

# Regular expression pattern to extract HTTP status codes from log lines
LOG_PATTERN = re.compile(r'"\s*\w+\s+[^"]+"\s+(\d+)\s+\d+')


class MRTopStatusCodes(MRJob):
    """
    A MapReduce job to identify the Top 10 most frequent HTTP status codes
    from a web server log file in Common Log Format (CLF).
    """

    def mapper(self, _, line):
        """
        Extracts HTTP status codes from each line of the log file.
        Ignored key (since input is a text file)
        line (str): A line from the log file.
        tuple: (HTTP status code, 1) for counting occurrences.
        """
        match = LOG_PATTERN.search(line)
        if match:
            yield match.group(1), 1

    def combiner(self, status_code, counts):
        """
        Locally aggregates counts for each status code before sending data to reducers.
        status_code (str): The HTTP status code.
        counts (iterable): A list of counts (all 1s).
        tuple: (HTTP status code, sum of occurrences).
        """
        yield status_code, sum(counts)

    def reducer(self, status_code, counts):
        """
        Aggregates counts globally to compute total occurrences per status code.
        status_code (str): The HTTP status code.
        counts (iterable): A list of aggregated counts.
        tuple: (None, (total count, HTTP status code)), for sorting in the next step.
        """
        yield None, (sum(counts), status_code)

    def reducer_top_10(self, _, status_counts):
        """
        Sorts status codes by frequency in descending order and selects the top 10.
        status_counts (iterable): A list of tuples (count, HTTP status code).
        tuple: (HTTP status code, total count) for the top 10 most frequent codes.
        """
        sorted_counts = sorted(status_counts, reverse=True, key=lambda x: x[0])
        for count, status_code in sorted_counts[:10]:
            yield status_code, count

    def steps(self):
        """
        Defines the sequence of MapReduce steps.

        Returns: A sequence of MRSteps for processing the log file.
        """
        return [
            MRStep(mapper=self.mapper,
                   combiner=self.combiner,
                   reducer=self.reducer),
            MRStep(reducer=self.reducer_top_10)
        ]


def main():
    """
    Main function to execute the MapReduce job.
    - Ensures the correct number of command-line arguments.
    - Runs the MapReduce job using `mrjob`.
    - Outputs the top 10 HTTP status codes with their counts.
    """
    if len(sys.argv) != 2:
        print("Usage: python top_status_codes.py <logfile>")
        sys.exit(1)

    logfile = sys.argv[1]
    mr_job = MRTopStatusCodes(args=[logfile])

    with mr_job.make_runner() as runner:
        runner.run()
        print("\nPart-B | Q-1")
        print("Top 10 Most Frequent HTTP Status Codes\n")
        for key, value in mr_job.parse_output(runner.cat_output()):
            print(f"Status Code: {key}, Count: {value}")
        print("\n")

if __name__ == '__main__':
    main()
