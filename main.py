import requests
from bs4 import BeautifulSoup
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt
from wordcloud import WordCloud

class StockAnalyzer:
    def __init__(self):
        self.sid = SentimentIntensityAnalyzer()

    def scrape_news(self, stock):
        url = f"https://www.example.com/news/{stock}"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        news_articles = soup.find_all('div', class_='article')

        headlines = []
        for article in news_articles:
            headline = article.find('h2').text
            headlines.append(headline)

        return headlines

    def scrape_tweets(self, stock):
        url = f"https://www.example.com/tweets/{stock}"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        tweets = soup.find_all('div', class_='tweet')

        tweet_text = []
        for tweet in tweets:
            text = tweet.find('p').text
            tweet_text.append(text)

        return tweet_text

    def perform_sentiment_analysis(self, text):
        sentiment_scores = []
        for item in text:
            sentiment_scores.append(self.sid.polarity_scores(item)['compound'])

        return sentiment_scores

    def visualize_sentiment_distribution(self, scores):
        plt.hist(scores, bins=[-1, -0.5, 0, 0.5, 1], edgecolor='black')
        plt.xlabel('Sentiment Score')
        plt.ylabel('Frequency')
        plt.title('Sentiment Distribution')
        plt.show()

    def generate_word_cloud(self, text):
        if len(text) == 0:
            print("No text available to generate word cloud.")
            return

        word_cloud_text = ' '.join(text)
        wordcloud = WordCloud().generate(word_cloud_text)

        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.show()

    def analyze_stock(self, stock):
        news_headlines = self.scrape_news(stock)
        tweet_text = self.scrape_tweets(stock)

        all_text = news_headlines + tweet_text

        sentiment_scores = self.perform_sentiment_analysis(all_text)

        self.visualize_sentiment_distribution(sentiment_scores)

        self.generate_word_cloud(all_text)

if __name__ == "__main__":
    stocks = ['AAPL', 'GOOGL', 'AMZN']  # Example list of stocks to analyze

    analyzer = StockAnalyzer()
    for stock in stocks:
        analyzer.analyze_stock(stock)