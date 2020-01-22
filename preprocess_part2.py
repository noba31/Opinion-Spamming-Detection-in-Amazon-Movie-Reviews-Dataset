# Big Data Management and Analytics project (CS6350 - Spring 2019)
# Project: Detecting Opinion Spamming in Amazon Movie Reviews
# Data Pre-processing Steps - Part 2
from collections import defaultdict
import csv
columns = defaultdict(list)
with open('movies_output_pp1.csv', 'r') as inputFile:
    # Step 1: Creating the reader object and ignoring the whitespaces immediately after the delimiter ':'
    csvReaderObject = csv.reader(inputFile, skipinitialspace=True)
    # Step 2: Creating the writer object and instructing it to never quote fields and setting escapechar
    csvWriterObject = csv.writer(open('movies_output_pp2.csv', 'w'), quoting=csv.QUOTE_NONE, escapechar=' ')
    # Step 3: Creating a set
    setVar = set('"[]\' ')
    for row in csvReaderObject:
        intermediate = [''.join(' ' if c in setVar else c for c in entry) for entry in row]
        csvWriterObject.writerow(intermediate)