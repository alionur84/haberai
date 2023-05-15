from bs4 import BeautifulSoup
import urllib3
import random

sections = {'ekonomi': 'cg726y2k82dt',
			'saglik': 'cnq68n6wgzdt',
			'teknoloji':'c2dwqnwkvnqt',
			'spor': 'c340qx04vwwt',
			'siyaset': 'c8y94d98rqzt',
			'kultur': 'cwr9jq9rpp2t',
			'ortadogu': 'cg726y2qxg1t',
			'avrupa_birligi': 'cqywj1w7y73t',
			'rusya_ukrayna': 'cy0ryl4pvx6t'
			}

url = "https://www.bbc.com/turkce/topics/"

def get_news(section):

	req = urllib3.PoolManager()
	res = req.request('GET', url + sections[section])

	soup = BeautifulSoup(res.data, 'html.parser')

	container = soup.find_all('h2')

	links_to_articles = []

	articles = []

	for i in container:
		link = i.find_next()
		links_to_articles.append(link['href'])

	random_integers = random.sample(range(len(links_to_articles)), 5)

	random_links_to_articles = [links_to_articles[i] for i in random_integers]

	if len(random_links_to_articles) != 0:

		for link in random_links_to_articles:
			try:
				res2 = req.request('GET', link)
				soup2 = BeautifulSoup(res2.data, 'html.parser')
				article_container = soup2.find('main', class_='bbc-fa0wmp')
				articles.append([article_container.text, link])
			except:
				continue
		return articles
	else:
		return ['sorry no news']

