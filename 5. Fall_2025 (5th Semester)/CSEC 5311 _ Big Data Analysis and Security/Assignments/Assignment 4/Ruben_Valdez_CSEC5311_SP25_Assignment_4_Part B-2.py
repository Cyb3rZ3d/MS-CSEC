#Ruben_Valdez_CSEC5311_SP25_Assignment_4_Part B-2.py
from mrjob.job import MRJob
from mrjob.step import MRStep
import re
from collections import defaultdict

# Regular expression to parse log file lines (Common Log Format)
LOG_PATTERN = re.compile(
    r'(?P<ip>\d+\.\d+\.\d+\.\d+) - - \[.*\] ".*" (?P<status>\d+) .*'
)

class MRErrorIPs(MRJob):

    def mapper(self, _, line):
        """Extracts IP and status code, emits (IP, (1, status_code, category)) for 4xx and 5xx errors"""
        match = LOG_PATTERN.match(line)
        if match:
            ip = match.group("ip")
            status = int(match.group("status"))
            if 400 <= status < 600:  # Only client (4xx) and server (5xx) errors
                category = "client" if 400 <= status < 500 else "server"
                yield ip, (1, status, category)
                yield "TOTAL_ERRORS", (1, status, category)  # Track global total errors

    def combiner(self, key, values):
        """Aggregates counts and status codes at the mapper level"""
        error_count = 0
        error_codes = defaultdict(int)
        client_errors = 0
        server_errors = 0

        for count, status, category in values:
            error_count += count
            error_codes[status] += count
            if category == "client":
                client_errors += count
            else:
                server_errors += count

        yield key, (error_count, client_errors, server_errors, dict(error_codes))

    def reducer(self, key, values):
        """Aggregates error counts and status codes at the reducer level"""
        total_errors = 0
        client_errors = 0
        server_errors = 0
        error_codes = defaultdict(int)

        for count, c_errors, s_errors, codes in values:
            total_errors += count
            client_errors += c_errors
            server_errors += s_errors
            for code, code_count in codes.items():
                error_codes[code] += code_count

        # Ensure TOTAL_ERRORS outputs the same structure
        if key == "TOTAL_ERRORS":
            yield key, (total_errors, client_errors, server_errors, dict(error_codes))
        else:
            yield None, (total_errors, key, client_errors, server_errors, dict(error_codes))

    def reducer_sort(self, key, ip_data):
        """Sorts IPs by total errors and outputs the top 5"""
        sorted_ips = []
        total_error_entry = None

        for data in ip_data:
            if key == "TOTAL_ERRORS":
                total_error_entry = data  # Store the TOTAL_ERRORS entry separately
            else:
                sorted_ips.append(data)

        sorted_ips = sorted(sorted_ips, reverse=True, key=lambda x: x[0])[:5]  # Sort by total errors

        for total_errors, ip, client_errors, server_errors, error_codes in sorted_ips:
            formatted_codes = ", ".join([f"{code}: {count}" for code, count in sorted(error_codes.items())])
            yield ip, (total_errors, client_errors, server_errors, formatted_codes)

        if total_error_entry:
            total_errors, client_errors, server_errors, error_codes = total_error_entry
            formatted_codes = ", ".join([f"{code}: {count}" for code, count in sorted(error_codes.items())])
            yield "TOTAL_ERRORS", (total_errors, client_errors, server_errors, formatted_codes)

    def steps(self):
        return [
            MRStep(mapper=self.mapper,
                   combiner=self.combiner,
                   reducer=self.reducer),
            MRStep(reducer=self.reducer_sort)
        ]

def main():
    """Runs the MapReduce job and displays results"""
    import sys
    if len(sys.argv) != 2:
        print("Usage: python ex_1.py <input_log_file>")
        sys.exit(1)

    job = MRErrorIPs(args=[sys.argv[1]])
    with job.make_runner() as runner:
        runner.run()

        results = list(job.parse_output(runner.cat_output()))

        if not results:
            print("\nNo errors found in the log file.")
            sys.exit(0)

        print("\nPart-B | Q-2")
        print("Top 5 IPs Generating the Most Errors (4xx & 5xx)\n")
        print(f"{'IP Address':<18}{'Total Errors':<15}{'Client Errors':<15}{'Server Errors':<15}{'Error Codes'}")
        print("=" * 100)

        total_errors_entry = None
        for key, (total_errors, client_errors, server_errors, error_details) in results:
            if key == "TOTAL_ERRORS":
                total_errors_entry = (total_errors, client_errors, server_errors, error_details)
            else:
                print(f"{key:<18}{total_errors:<15}{client_errors:<15}{server_errors:<15}{error_details}")

        if total_errors_entry:
            print("=" * 100)
            print(f"{'TOTAL ERRORS':<18}{total_errors_entry[0]:<15}{total_errors_entry[1]:<15}{total_errors_entry[2]:<15}{total_errors_entry[3]}\n")

if __name__ == '__main__':
    main()
