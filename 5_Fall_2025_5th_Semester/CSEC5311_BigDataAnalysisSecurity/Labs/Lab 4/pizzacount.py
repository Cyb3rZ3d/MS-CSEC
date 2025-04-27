from mrjob.job import MRJob

class PizzaOrderCount(MRJob):

    def mapper(self, _, line):
        """Map function: Read each line and emit (PizzaType, 1)"""
        yield line.strip(), 1  # Each line is a pizza order

    def reducer(self, pizza_type, counts):
        """Reduce function: Sum all counts for each pizza type"""
        yield pizza_type, sum(counts)

if __name__ == '__main__':
    PizzaOrderCount.run()
