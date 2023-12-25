import requests
from bs4 import BeautifulSoup
import datetime
root_url="https://edition.cnn.com/"
response=requests.get(root_url)
doc = BeautifulSoup(response.text, 'html.parser')

def find_article_details(url):
  response_article=requests.get(url)
  #create a new soup for a new page
  soup = BeautifulSoup(response_article.text, 'html.parser')
  body=soup.find_all('div',{'class':'article__content'})
  description=['\n'.join(p.text) for p in body.find_all("p")]
  try:
    image_url=soup.find('div',{'class':'image__container'}).find('img').get('src')
  except:
    image_url=None
    #if video or image present

  try:
    author=soup.find('div',{'class':'headline__footer'}).find('span').text
  except:
    author=None
  try:
    temp=soup.find('div',{'class':'headline__footer'}).find('div',{'class':'timestamp'}).text
    words=temp.split()
    stripped_word=' '.join(words[1:])
    date_object = datetime.strptime(stripped_word, '%I:%M %p %Z, %a %B %d, %Y')
    timestamp= date_object.strftime('%Y-%m-%d %H:%M:%S')

  except:
    timestamp=None
  return description,author,image_url,timestamp

def ccn_scraper(category):
  
  newsAll=doc.find_all('div', { 'class': 'container__field-links container_lead-plus-headlines-with-images__field-links' })
  for idx,news in enumerate(newsAll):
    headline=news.find_all('a')[1].find('span').text
    path=news.find('a')['href']#first
    article_url=root_url+path
  try:
    description,author,img_url,time=find_article_details(article_url)
    article = {
                "id": path,
                "source": "BBC",
                "type": category,
                "Author":author,
                "title": headline,
                "description": description,
                "url": article_url,
                "image_url": img_url,
                "published_at": time,
                "updated_at": time
            }
  except:
    print("Wrong Url")

categories = ['US', 'World', 'Politics', 'Business', 'Opinion', 'Health', 'Entertainment', 'Style', 'Travel', 'Sports']
