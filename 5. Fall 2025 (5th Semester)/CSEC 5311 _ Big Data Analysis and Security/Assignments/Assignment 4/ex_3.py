from mrjob.job import MRJob
from mrjob.step import MRStep


class TopErrorIPs(MRJob):
    def mapper(self, _, line):
        parts = line.split()
        if len(parts) > 8:
            ip = parts[0]
            status_code = parts[-2]
            if status_code.startswith("4") or status_code.startswith("5"):
                yield ip, 1

    def reducer(self, key, values):
        yield None, (sum(values), key)

    def sorter(self, _, ip_counts):
        sorted_counts = sorted(ip_counts, reverse=True, key=lambda x: x[0])[:5]
        for count, ip in sorted_counts:
            yield ip, count

    def steps(self):
        return [
            MRStep(mapper=self.mapper, reducer=self.reducer),
            MRStep(reducer=self.sorter)
        ]
    
def main():
    print(f"\n***Q-2:  Top 5 IP Addresses Generating the Most Errors (4xx and 5xx Status Codes)***\n")
    TopErrorIPs.run()
    print(f"\n")


if __name__ == "__main__":
    main()
