#!/usr/bin/env python3
import sys

current_coord = None
current_count = 0
max_coord = None
max_count = 0

for line in sys.stdin:
    coord, count = line.strip().split('\t')
    count = int(count)

    if coord == current_coord:
        current_count += count
    else:
        if current_coord and current_count > max_count:
            max_count = current_count
            max_coord = current_coord
        current_coord = coord
        current_count = count

# Final check
if current_coord and current_count > max_count:
    max_count = current_count
    max_coord = current_coord

print(f"Most Popular Pickup Location: {max_coord} with {max_count} trips")
