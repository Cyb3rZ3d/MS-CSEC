#!/usr/bin/env python3
import sys

current_zone = None
current_count = 0
max_zone = None
max_count = 0

for line in sys.stdin:
    zone, count = line.strip().split('\t')
    count = int(count)
    
    if zone == current_zone:
        current_count += count
    else:
        if current_zone and current_count > max_count:
            max_count = current_count
            max_zone = current_zone
        current_zone = zone
        current_count = count

# Final zone check
if current_zone and current_count > max_count:
    max_count = current_count
    max_zone = current_zone

print(f"Most Popular Pickup Zone: {max_zone} with {max_count} trips")
