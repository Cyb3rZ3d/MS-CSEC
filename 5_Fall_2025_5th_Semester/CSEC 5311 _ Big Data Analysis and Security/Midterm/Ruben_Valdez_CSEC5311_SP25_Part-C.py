from mrjob.job import MRJob
from mrjob.step import MRStep

class OrderCountByCategory(MRJob):

    def steps(self):
        return [
            MRStep(mapper=self.mapper,
                   reducer=self.reducer),
            MRStep(reducer=self.sort_reducer)
        ]

    def mapper(self, _, line):
        # Assuming data is tab-separated. Adjust accordingly if different.
        fields = line.strip().split("\t")
        
        # Ensure we have the necessary fields (modify indexes based on dataset structure)
        if len(fields) >= 4:  
            segment = fields[0].strip()
            region = fields[1].strip()
            category = fields[2].strip()
            priority = fields[3].strip()
            
            # Emit key-value pair: (Segment, Region, Category, Priority) → 1
            yield (segment, region, category, priority), 1

    def reducer(self, key, values):
        # Sum up the total orders for each unique key
        yield None, (sum(values), key)  # Sending count first for sorting in the next step

    def sort_reducer(self, _, count_key_pairs):
        # Sort by order count in descending order
        sorted_results = sorted(count_key_pairs, reverse=True, key=lambda x: x[0])
        
        # Yield top 5 most frequent combinations
        for count, key in sorted_results[:5]:
            yield key, count

if __name__ == '__main__':
    OrderCountByCategory.run()
