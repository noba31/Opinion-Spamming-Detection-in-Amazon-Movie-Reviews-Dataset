# Big Data Management and Analytics project (CS6350 - Spring 2019)
# Project: Detecting Opinion Spamming in Amazon Movie Reviews
# Data Pre-processing Steps - Part 1
import re
import csv
with open('movies.txt', 'r') as moviesData:
    # Step 1: Removing leading and trailing characters from every line
    lineStrip = (line.strip() for line in moviesData)
    # Step 2: Replacing all commas with blanks and splitting text using ':' as the delimiter
    lineSplit = (((re.sub(r"[,]", "", line)).split(':')[-1:]) for line in lineStrip if line)
    # Step 3: Grouping reviews for each movie and representing the 8 lines of each movie review in 8 columns
    lineGroup = zip(*[lineSplit] * 8)
    # Step 4: Writing all cleaned movie data reviews as rows to an output file - movies_output_pp1.csv'
    with open('movies_output_pp1.csv', 'w') as moviesDataPP1:
        # Step 5: Creating the writer object
        csvWriterObject = csv.writer(moviesDataPP1)
        # Step 6: Column names to store the 8 rows of information for each movie review
        csvWriterObject.writerow(('productId', 'userId', 'profileName', 'helpfulness', 'score', 'time', 'summary', 'text'))
        # Step 7: Writing all rows to the output file
        csvWriterObject.writerows(lineGroup)