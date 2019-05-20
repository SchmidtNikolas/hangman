import requests
from bs4 import BeautifulSoup

# get a random word
r = requests.get("https://wordunscrambler.me/random-word-generator")
soup = BeautifulSoup(r.text, features='lxml')

# clean the request to get just the word
word = soup.find('div', {'id': 'random-word-wrapper'}).findChildren('a')[0].text.strip()

print(word)
