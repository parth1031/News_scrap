import requests

# import pandas as pd
from urllib.parse import urlencode
from lxmlparser1 import HTMLParser
from extractor1 import CustomExtractor


from cleaner1 import cleaning_function

url="https://www.gadgetsnow.com/gn-advertorial/enter-the-new-era-of-mobile-technology-as-samsung-is-all-set-to-introduce-the-revolutionary-galaxy-ai/articleshow/106867089.cms?upcache=2&_gl=1*1ncy8wg*_ga*MzI4MzUwNDA5LjE2OTI1NTY4MTQ.*_ga_FCN624MN68*MTcwNTkxOTU1Ny4xMS4xLjE3MDU5MTk4MTIuNjAuMC4w"
url = input("Please Enter the url :")

proxies = {
"http": "http://scraperapi:ed327761c0dc69ab3455d9af6142525e@proxy-server.scraperapi.com:8001"
}
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

response = requests.get(url,headers=headers,proxies=proxies,verify=False)
API_KEY = "ed327761c0dc69ab3455d9af6142525e"
params = {'api_key': API_KEY, 'url': url}
response = requests.get('http://api.scraperapi.com/', params=urlencode(params))
response.raise_for_status()


# print(html_content)
# Create an instance of CustomExtractor
extractor = CustomExtractor(response.text)
html_content= response.text
parser=HTMLParser(html_content)




authors_list=extractor.findauthors(html_content)
print("*************************************************************************************************************")
print("authors/sources  are")

if authors_list:
    
    for author in authors_list:
        print(author)
       
else:
    print("No authors found.")

date=extractor.finddate(html_content,url)

print("date of publication:",date)



title_list=extractor.fetch_title(parser)
print("title  is/are")

print(extractor.fetch_title(parser))


# Calculate best node based on custom gravity scores
best_node = extractor.most_imp_node(html_content)

print("\n\n")
# Now, you ca
# n access the best node and its gravity score
if best_node is not None:
    try:
        print(f"Best Node: {best_node.get('class')}")
    except:
        pass
    cleaning_function(best_node,parser)
    
else:
    print("No best node found.")

print("*************************************************************************************************************")