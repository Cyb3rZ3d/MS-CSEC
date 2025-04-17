#!/usr/bin/env python3
import sys

current_group = None
total_fare = 0.0
trip_count = 0

for line in sys.stdin:
    group, fare = line.strip().split('\t')
    fare = float(fare)

    if current_group == group:
        total_fare += fare
        trip_count += 1
    else:
        if current_group:
            avg_fare = total_fare / trip_count
            print(f"{current_group} passenger(s) → Avg Fare: ${avg_fare:.2f}")
        current_group = group
        total_fare = fare
        trip_count = 1

# Final group
if current_group and trip_count > 0:
    avg_fare = total_fare / trip_count
    print(f"{current_group} passenger(s) → Avg Fare: ${avg_fare:.2f}")
