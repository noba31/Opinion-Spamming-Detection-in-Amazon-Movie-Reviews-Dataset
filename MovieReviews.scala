package  com.utd.scala

import org.apache.spark.{SparkConf, SparkContext}
import org.apache.spark.sql.{SparkSession}
import edu.stanford.nlp.ling.CoreAnnotations
import edu.stanford.nlp.neural.rnn.RNNCoreAnnotations
import edu.stanford.nlp.pipeline.{Annotation, StanfordCoreNLP}
import edu.stanford.nlp.sentiment.SentimentCoreAnnotations


object MovieReviews {
  def main(args: Array[String]):Unit = {

    if (args.length != 2) {
      println("Usage InputFile OutputFile")
      throw new Exception("too few args")
    }

    val sc = new SparkContext(new SparkConf().setAppName("MovieReview"))
    val spark = SparkSession.builder().getOrCreate()
    import spark.implicits._

    val PATH = args(0)
    val movieDF = spark.read.option("header", "true").option("delimiter", ",").option("inferSchema", "true").csv(PATH).toDF("ProductId", "UserId", "ProfileName", "Helpfulness", "Score", "Time", "Summary", "Text")

    val movieDF2 = movieDF.select("Score", "Text", "Helpfulness")

    // COMMAND ----------

    import org.apache.spark.sql.functions._
    val movieDF3 = movieDF2.withColumn("Helpfulness score", split($"Helpfulness", "/").getItem(0) / split($"Helpfulness", "/").getItem(1)).
      drop("Helpfulness")

    val movieDF4 = movieDF3.na.fill(0, Seq("Helpfulness score"))

    import java.util.Properties
    import scala.collection.JavaConversions._
    val props = new Properties()
    props.setProperty("annotators", "tokenize, ssplit, parse, sentiment")
    val pipeline: StanfordCoreNLP = new StanfordCoreNLP(props)

    def extractSentiment(text: String): Int =
    {
      val (_, sentiment) = extractSentiments(text)
        .maxBy { case (sentence, _) => sentence.length }
      sentiment
    }

    def extractSentiments(text: String): List[(String, Int)] = {
      val annotation: Annotation = pipeline.process(text)
      val sentences = annotation.get(classOf[CoreAnnotations.SentencesAnnotation])
      sentences.map(sentence => (sentence, sentence.get(classOf[SentimentCoreAnnotations.SentimentAnnotatedTree]))).map { case (sentence, tree) => (sentence.toString, RNNCoreAnnotations.getPredictedClass(tree)) }
        .toList
    }

    val mainSentiment =  udf((input: String) => Option(input) match {
      case Some(text) if !text.isEmpty => extractSentiment(text)
      case _ => throw new IllegalArgumentException("input can't be null or empty")
    })

    val finalDF = movieDF4.withColumn("Sentiment Score", mainSentiment(movieDF4("Text")))

    finalDF.limit(10).write.format("csv").option("header", "true").csv(args(1))
  }

}
