#!/usr/bin/env python3
import sys
import csv

for row in csv.reader(sys.stdin):
    try:
        # Skip header
        if row[3] == "passenger_count" or row[12] == "fare_amount":
            continue

        passenger_count = row[3].strip()
        fare_amount = float(row[12].strip())

        # Only include valid values
        if passenger_count and passenger_count != "0" and fare_amount >= 0:
            print(f"{passenger_count}\t{fare_amount}")
    except:
        continue
