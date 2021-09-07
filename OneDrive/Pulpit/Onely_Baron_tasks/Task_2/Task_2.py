from Web import Web_scraping, Save
import sys

links = []
content = []
end=0
try:

    keywords = open("keywords.txt","r")#opening and reading .txt file
except FileNotFoundError:
    
    sys.exit()

for keyword in keywords:#iteration over all records in .txt file
    word = keyword.split('\n')#spliting by enter
    buffor = Web_scraping(word[0])#creating object
    content.append(buffor)#adding to list which contains all objects
  

for cnt in content:
    links, qty = Web_scraping.get_links(cnt.URL)#webscraping list and quantity of pages
    Save.save_to_csv(links, cnt.kwd)#saving links to to .csv file -> one object to one .csv file
    Save.save_results(cnt.kwd, qty)#saving keywords and quantity to .csv file -> all objects to one .csv file