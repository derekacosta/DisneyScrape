import urllib
import urllib2
import json
import requests
from bs4 import BeautifulSoup
import os
import sys


html = requests.get("http://disney.wikia.com/wiki/Characters_from_Pixar_films")

soup = BeautifulSoup(html.content, "html.parser")

titles = []

def create_dir():
	for title in soup.findAll("span", { "class" : "mw-headline" }):
		titles.append(title.text)
		try:
			newpath = r'/Users/IM_working/Desktop/rachid/'+title.text.replace(" ", "")
			# if not os.path.exists(newpath):
			original_umask = os.umask(0)
			os.makedirs(newpath, 0755)
		except:
			pass
		finally:
		    os.umask(original_umask)

def scrape_title_and_url():
	for article in soup.findAll("div", { "id" : "WikiaArticle"}):
		temp = {}
		# interior = {}
		for details in article.findAll("div", { "class" : "wikia-gallery-item" }):
			key = str(details.find_previous('h3').text)
			temp.setdefault(key, [])
			for name in details.findAll("div", { "class" : "lightbox-caption" }):
				key2 = str(name.text)
				# interior.setdefault(key2, [])
				temp[key].append(key2)
			for image in details.findAll("img"):
				if image.get('src').startswith('http://vignette'):
					key3 = str(image.get('src'))
					# interior[key2].append(key3)
					temp[key].append(key3)
			download_img(temp)
			temp.clear()
		# interior.clear()

def download_img(temp):
	f = open("/Users/IM_working/Desktop/rachid/" + str(temp.keys()[0].replace(" ", "")) + "/" + str(temp.values()[0][0])+ ".jpg", 'wb')
	f.write(urllib.urlopen(str(temp.values()[0][1])).read())
	f.close()


def main():
	create_dir()
	scrape_title_and_url()

if __name__ == "__main__":
    main()















