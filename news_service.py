import openai
import requests
from bs4 import BeautifulSoup
from portal.services import app_constants
from flask import request
#from gtts import gTTS

"""
def generate_sum_delete(inputs):
    # todo: add your code here
    article_info = articles(inputs)
    generated_summary = summary(article_info[1])
    results_list = [article_info[0],article_info[1],article_info[2],generated_summary]
    return results_list
"""

def summary(url):
    # Fetch the article content from the URL
    lang_dict = app_constants.LANG_DICT
    language_code = request.form["language"]
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    article_text = soup.get_text()

    # Create the TL;DR prompt
    prompt = f"TL;DR\n{url}. Generate the response in {lang_dict[language_code][0]}"

    response = openai.Completion.create(
        engine="text-davinci-003",  # You can use "davinci" or "curie" as well
        prompt=prompt,
        max_tokens=200  # Adjust the max_tokens as needed
    )

    summary = response.choices[0].text.strip()

    # Ensure the summary ends at a sentence boundary
    sentences = summary.split(".")
    if len(sentences) > 1:
        summary = ".".join(sentences[:-1]) + "."

    return summary


def generate_sum(inputs):
    results = []
    openai.api_key = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
    API_KEY = 'yyyyyyyyyyyyyyyyyyyyyy'
    BASE_URL = 'https://gnews.io/api/v4/top-headlines'

    categories = inputs['interests']

    for category in categories:
        params = {
            'country': inputs['country'],
            'category': category,
            'token': API_KEY,
            'lang': inputs['language'],
            'max': 1
        }

        response = requests.get(BASE_URL, params=params)
        data = response.json()

        if 'articles' in data:
            print("***2 got raw data from gnews", data["articles"])
            for article in data['articles']:
                title = article['title']
                url = article['url']
                source = article['source']['name']
                image = article['image']
                keysList = list(article.keys())
                # get summary for current article
                one_summary = summary(url)
                one_article = [title,url,one_summary, image, source]
                results.append(one_article)

        else:
            print("Error fetching top headlines")
    return results
