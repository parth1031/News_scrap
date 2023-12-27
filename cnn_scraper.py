import requests
from bs4 import BeautifulSoup
from datetime import datetime
import json
from urllib.parse import urljoin
root_url="https://edition.cnn.com/"
response=requests.get(root_url)
doc = BeautifulSoup(response.text, 'html.parser')
news_list=[]
def find_article_details(url):
  response_article=requests.get(url)
  #create a new soup for a new page
  soup = BeautifulSoup(response_article.text, 'html.parser')
  body=soup.find_all('div',{'class':'article__content'})
  paragraph=body[0].find_all("p")
  description=''.join([p.text for p in paragraph])
  # print(description)
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
    # Filter out empty strings and unnecessary elements
    temp=temp.split()
    filtered_list = [elem.strip() for elem in temp if elem.strip() and elem not in ['Published', 'EST,']]
    date_string=''
    for i in filtered_list:
      for j in i:
        if j!=',':
          date_string+=j
      date_string+=' '
    
    timestamp_dt = datetime.strptime(date_string.strip(), '%I:%M %p %a %B %d %Y')
  except:
    timestamp_dt=None
    date_string=None
  return description,author,image_url,timestamp_dt,date_string

def cnn_scraper(category):
  
  newsAll=doc.find_all('div', { 'class': 'container__field-links container_lead-plus-headlines-with-images__field-links' })
  for idx,news in enumerate(newsAll):
    headline=news.find_all('a')[1].find('span').text
    path=news.find('a')['href']#first
    article_url=urljoin(root_url,path)
    print(article_url)
    try:
      description,author,img_url,timestamp_dt,date_string=find_article_details(article_url)
      article = {
                  "id": path,
                  "source": "CCN",
                  "type": category,
                  "Author":author,
                  "title": headline,
                  "description": description,
                  "url": article_url,
                  "image_url": img_url,
                  "published_on":date_string
                  
              }
      news_list.append(article)
    except:
      print("Wrong Url")

categories = ['US', 'World', 'Politics', 'Business', 'Opinion', 'Health', 'Entertainment', 'Style', 'Travel', 'Sports']
for category in categories:
  response = requests.get(urljoin(root_url,category.lower()))
  doc = BeautifulSoup(response.text, 'html.parser')
  cnn_scraper(category)
print(len(news_list))

with open('ccnNews.json', 'w', encoding='utf-8') as file:
  json.dump(news_list , file, ensure_ascii=False, indent=4)

