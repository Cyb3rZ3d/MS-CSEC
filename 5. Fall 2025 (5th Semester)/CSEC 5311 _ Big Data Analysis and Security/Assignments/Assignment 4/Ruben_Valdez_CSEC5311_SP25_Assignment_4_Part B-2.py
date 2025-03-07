from mrjob.job import MRJob
from mrjob.step import MRStep
import re

# Regular expression to parse the log file
LOG_PATTERN = re.compile(r'(?P<ip>\S+) \S+ \S+ \[.*?\] "(?:GET|POST|PUT|DELETE|HEAD) .*?" (?P<status>\d{3}) .*?')

class TopErrorIPs(MRJob):
    
    def mapper(self, _, line):
        match = LOG_PATTERN.match(line)
        if match:
            ip = match.group('ip')
            status_code = int(match.group('status'))
            
            # Check if the status code is 4xx or 5xx
            if 400 <= status_code < 600:
                yield ip, 1
    
    def combiner(self, ip, counts):
        yield ip, sum(counts)
    
    def reducer(self, ip, counts):
        yield None, (sum(counts), ip)
    
    def sort_and_output(self, _, ip_counts):
        # Sort by count in descending order and take top 5
        top_5 = sorted(ip_counts, reverse=True, key=lambda x: x[0])[:5]
        for count, ip in top_5:
            yield ip, count
    
    def steps(self):
        return [
            MRStep(mapper=self.mapper, 
                   combiner=self.combiner,
                   reducer=self.reducer),
            MRStep(reducer=self.sort_and_output)
        ]

def main():
    print(f"\n")
    TopErrorIPs.run()
    print(f"\nEnd of Program\n")

if __name__ == "__main__":
    main()