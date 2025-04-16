#!/usr/bin/env python3
import sys
from datetime import datetime

for line in sys.stdin:
    try:
        fields = line.strip().split(',')
        if fields[0] == 'tpep_pickup_datetime':  # Skip header
            continue
        pickup_time = fields[0]
        hour = datetime.strptime(pickup_time, '%Y-%m-%d %H:%M:%S').hour
        print(f"{hour:02d}\t1")
    except Exception as e:
        continue
