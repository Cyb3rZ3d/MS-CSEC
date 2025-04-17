#!/usr/bin/env python3
import sys
import csv
from datetime import datetime

for row in csv.reader(sys.stdin):
    try:
        pickup_time = row[1]  # index 1 = tpep_pickup_datetime
        if pickup_time == "tpep_pickup_datetime":
            continue  # skip header
        hour = datetime.strptime(pickup_time, "%Y-%m-%d %H:%M:%S").strftime("%H:00")
        print(f"{hour}\t1")
    except Exception:
        continue
