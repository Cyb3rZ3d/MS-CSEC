#!/usr/bin/env python3
import sys
import csv

for row in csv.reader(sys.stdin):
    try:
        location_id = row[7]  # Adjust if index is different
        if location_id == "PULocationID":
            continue  # Skip header
        print(f"{location_id}\t1")
    except:
        continue
