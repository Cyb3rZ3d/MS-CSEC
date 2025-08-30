#!/usr/bin/env python3
import sys
import csv

for row in csv.reader(sys.stdin):
    try:
        if row[4] == "pickup_longitude":
            continue  # Skip header

        lon = row[4].strip()
        lat = row[5].strip()

        if lon and lat and lon != "0" and lat != "0":
            print(f"{lon},{lat}\t1")
    except:
        continue
