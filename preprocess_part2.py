# Big Data Management and Analytics project (CS6350 - Spring 2019)
# Project: Detecting Opinion Spamming in Amazon Movie Reviews
import csv
from collections import defaultdict

columns = defaultdict(list)

with open('movies_output_pp1.csv', 'r') as inputFile:
    # Creating the reader object and ignoring the whitespaces immediately after the delimiter ':'
    reader = csv.reader(inputFile, skipinitialspace=True)
    # Creating the writer object and instructing it to never quote fields and setting escapechar
    writer = csv.writer(open('movies_output_pp2.csv', 'w'), quoting=csv.QUOTE_NONE, escapechar=' ')
    # Creating a set
    conversion = set('"[]\' ')
    for row in reader:
        intermediate = [''.join(' ' if c in conversion else c for c in entry) for entry in row]
        writer.writerow(intermediate)