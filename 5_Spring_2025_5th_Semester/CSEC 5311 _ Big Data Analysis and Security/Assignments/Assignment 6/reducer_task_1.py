#!/usr/bin/env python3
import sys

current_hour = None
trip_count = 0

for line in sys.stdin:
    hour, count = line.strip().split('\t')
    count = int(count)
    if current_hour == hour:
        trip_count += count
    else:
        if current_hour:
            print(f"{current_hour}\t{trip_count} trips")
        current_hour = hour
        trip_count = count

if current_hour:
    print(f"{current_hour}\t{trip_count} trips")
