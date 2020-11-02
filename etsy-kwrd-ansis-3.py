import requests
from bs4 import BeautifulSoup
import pandas as pd

# the search term
query = input("Enter the search terms: ") #"harry+potter+bookmark"
#query = query.replace(" ", "+")

# this is getting/calling the page in python
etsy_page_search = requests.get("https://www.etsy.com/search/?q=" + query)
soup_search = BeautifulSoup(etsy_page_search.content, "html.parser") #html5lib after upgrading bs4

# # this is the listing id list
listing_id = soup_search.find_all("a")

# # this holds the listing url
list_id_records = []
keywords_records = []

# # this gather listing url by listing id and adding to website address
for listing in listing_id:
    list_id = (listing.get("data-listing-id"))
    if list_id != None:
        url_product = "http://www.etsy.com/listing/" + str(list_id) + "/"
        list_id_records.append(url_product)
print(list_id_records)
# # getting product page information
for list_id in list_id_records:
    etsy_page_product = requests.get(list_id)
    soup_product = BeautifulSoup(etsy_page_product.content, "html.parser")
    #keywords_list = soup_product.find_all("a", {"class":"btn btn-secondary"})
    keywords_list = soup_product.find_all("a", {"class":"wt-btn"})

    for keywords in keywords_list:
        keyword = keywords.text
        # title = soup_product.find("h1", attrs={"class":"mb-xs-2"}).text
        # seller = soup_product.find("a", attrs={"class":"text-link-no-underline text-gray-lightest"}).text
        # price = soup_product.find("span", attrs={"class":"text-largest strong override-listing-price"}).text
        keywords_records.append(keyword)

df = pd.DataFrame(keywords_records)
df.to_csv(query + ".csv", index=True, encoding="utf-8")
len(keywords_records)


import csv
from collections import Counter
from collections import defaultdict

words= []
with open(query+'.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
         csv_words = row[1].split(" ")
         for i in csv_words:
              words.append(i)

words_counted = []
for i in words:
    x = words.count(i)
    words_counted.append((i,x))

#write this to csv file
with open('output.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerows(words_counted)
        set(words_counted)
        print(words_counted)

df2 = pd.read_csv('output.csv')
df2.drop_duplicates(inplace=True)
df2.to_csv('output.csv', index=False)

import csv
from wordcloud import WordCloud


#read first column of csv file to string of words seperated
#by tab

your_list = []
with open('output.csv', 'r') as f:
    reader = csv.reader(f)
    your_list = '\t'.join([i[0] for i in reader])


# Generate a word cloud image
wordcloud = WordCloud().generate(your_list)

# Display the generated image:
# the matplotlib way:
import matplotlib.pyplot as plt
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")

# lower max_font_size
wordcloud = WordCloud(max_font_size=40).generate(your_list)
plt.figure()
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.show()

input()