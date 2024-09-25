# Sentiment and Forex Analysis
These scripts were made as part of a class project. The goal was to analyze the sentiment of news articles and compare them to forex rates. 
The DailyMirror (Sri Lanka) news articles were webscraped and the sentiment was analyzed using the TextBlob library. The forex rates were obtained an API from the Central Bank of Sri Lanka.

Project is accessible through the following link: [https://hamza-anver.github.io/F24-ForexSentiments/](https://hamza-anver.github.io/F24-ForexSentiments/)

## Structure
This project is divided into 4 scripts. 
1. `scraper.py` - This script takes in an argument to define its mode of operation (scrape or clean). The scrape mode scrapes the news articles and saves them to a file. The DailyMirror site requires a button press to view a few articles at a time, each page is saved seperately into the `dailymirror_archive_pages` directory (not included in the repo). The clean mode cleans the scraped data and saves it as JSON files named by day of publishing of the article into the `cleaned_data` directory.
2. `sentiment.py` - This script takes in the JSON file created by the scraper and calculates the sentiment of each article. The sentiment is saved to a new CSV file in `data\sentiments.csv`.
3. `forexrates.py` - This script uses the Central Bank of Sri Lanka API to get the forex rates for the USD to LKR exchange rate. The rates are saved to a CSV file in `data\forex.csv`.
4. `main.py` - This script does the final combining of the sentiment and forex rates data. It creates a new CSV file with the sentiment and forex rates data combined in `data\combined_data.csv`. It also creates a plot of the data using plotly which is saved to an HTML file (`index.html`) for easier viewing.

### Ethics
The news articles were scraped from the DailyMirror website. The articles are the property of the DailyMirror and are used for educational purposes only. There are no restrictions on webscraping specified by the DailyMirror. The forex rates were obtained from the Central Bank of Sri Lanka API. The API is free to use and there are no restrictions on its use.