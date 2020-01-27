library("RColorBrewer")
library("NLP")
library("SnowballC")
library("wordcloud")
library("tm")

dataSource <- readLines(file.choose())

# Load the data as a corpus
dataFile <- Corpus(VectorSource(dataSource))

inspect(dataFile)

contentPattern <- content_transformer(function (x , pattern ) gsub(pattern, " ", x))
dataFile <- tm_map(dataFile, contentPattern, "/")
dataFile <- tm_map(dataFile, contentPattern, "@")
dataFile <- tm_map(dataFile, contentPattern, "\\|")

# Convert the text to lower case
dataFile <- tm_map(dataFile, content_transformer(tolower))
# Remove numbers
dataFile <- tm_map(dataFile, removeNumbers)
# Remove english common stopwords
dataFile <- tm_map(dataFile, removeWords, stopwords("english"))
# Remove your own stop word
# specify your stopwords as a character vector
dataFile <- tm_map(dataFile, removeWords, c("random1", "random2")) 
# Remove punctuations
dataFile <- tm_map(dataFile, removePunctuation)
# Eliminate extra white spaces
dataFile <- tm_map(dataFile, stripWhitespace)
# Text stemming
# docs <- tm_map(docs, stemDocument)

termDocMatrix <- TermDocumentMatrix(dataFile)
matrixVar <- as.matrix(termDocMatrix)
sortMatrixVar <- sort(rowSums(matrixVar),decreasing=TRUE)
dataFrame <- data.frame(word = names(sortMatrixVar),freq=sortMatrixVar)
head(dataFrame, 10)

set.seed(1234)
wordcloud(words = dataFrame$word, freq = dataFrame$freq, min.freq = 1,
          max.words=200, random.order=FALSE, rot.per=0.35, 
          colors=brewer.pal(8, "Dark2"))
