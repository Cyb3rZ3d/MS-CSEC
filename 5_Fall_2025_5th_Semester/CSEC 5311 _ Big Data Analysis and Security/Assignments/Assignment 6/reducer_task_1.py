#!/usr/bin/env python3
import sys

current_hour = None
count = 0

for line in sys.stdin:
    hour, trip = line.strip().split('\t')
    if current_hour == hour:
        count += int(trip)
    else:
        if current_hour is not None:
            print(f"{current_hour}:00\t{count} trips")
        current_hour = hour
        count = int(trip)

if current_hour is not None:
    print(f"{current_hour}:00\t{count} trips")
