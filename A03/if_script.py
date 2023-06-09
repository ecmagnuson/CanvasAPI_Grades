#!/usr/bin/env python3

import sys

try:
    user_number = int(input('"Enter a value"\n'))
except ValueError:
    print("integer expression expected")
    sys.exit(1)

if user_number < 10:
    print("It is a one digit number")
else:
    print("It is a two digit number")