import requests
from bs4 import BeautifulSoup
import pandas as pd
from urllib.parse import urlencode
from lxmlparser1 import HTMLParser
from extractor1 import CustomExtractor


from cleaner1 import cleaning_function

url="https://www.gadgetsnow.com/gn-advertorial/enter-the-new-era-of-mobile-technology-as-samsung-is-all-set-to-introduce-the-revolutionary-galaxy-ai/articleshow/106867089.cms?upcache=2&_gl=1*1ncy8wg*_ga*MzI4MzUwNDA5LjE2OTI1NTY4MTQ.*_ga_FCN624MN68*MTcwNTkxOTU1Ny4xMS4xLjE3MDU5MTk4MTIuNjAuMC4w"
url = input("Please Enter the url :")

proxies = {
"http": "http://scraperapi:8355bf750256f87924cb321115d06996@proxy-server.scraperapi.com:8001"
}
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

response = requests.get(url,headers=headers,proxies=proxies,verify=False)
API_KEY = "8355bf750256f87924cb321115d06996"
params = {'api_key': API_KEY, 'url': url}
response = requests.get('http://api.scraperapi.com/', params=urlencode(params))
response.raise_for_status()

soup = BeautifulSoup(response.text, 'html.parser')

# print(soup)
# Create an instance of CustomExtractor
extractor = CustomExtractor(response.text)
html_content= response.text
parser=HTMLParser(html_content)




authors_list=extractor.findauthors(html_content)
print("authors/sources  are")

if authors_list:
    
    for author in authors_list:
        print(author)
       
else:
    print("No authors found.")

date=extractor.finddate(html_content,url)

print("date of publication:",date)



title_list=extractor.get_title(soup)
print("title  is/are")

print(extractor.get_title(soup))


# Calculate best node based on custom gravity scores
best_node = extractor.most_imp_node(soup)

print("\n\n")
# Now, you ca
# n access the best node and its gravity score
if best_node:
    print(best_node.tag)
    try:
        print(f"Best Node: {best_node['class']}, Gravity Score: {best_node.get('score', 0)}")
    except:
        pass
    # print(best_node.get_text(strip=True))
    print(best_node.text_content().strip())
    cleaning_function(best_node,parser)
    
else:
    print("No best node found.")