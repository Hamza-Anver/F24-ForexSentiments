from textblob import TextBlob
import json, os

json_dir = "cleaned_data"
output_dir = "data/sentiments.csv"

def analyze_articles():
    files = os.listdir(json_dir)
    output_file = open(output_dir, "w", encoding="utf-8")
    output_file.write("date,sentiment\n")

    for file in files:
        with open(f"{json_dir}/{file}", "r", encoding="utf-8") as f:
            articles = json.load(f)
            day_sentiment_average = 0
            for article in articles:
                text = article["summary"]
                blob = TextBlob(text)
                article["sentiment"] = blob.sentiment.polarity
                day_sentiment_average += blob.sentiment.polarity
            
            day_sentiment_average /= len(articles)
            print(f"{file} - Average Sentiment: {day_sentiment_average}")
            date = file.split(".")[0]
            output_file.write(f"{date},{day_sentiment_average}\n")

                

if __name__ == "__main__":
    analyze_articles()