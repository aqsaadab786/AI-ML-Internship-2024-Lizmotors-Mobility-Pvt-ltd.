#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np 
import pandas as pd 
import requests
from bs4 import BeautifulSoup as bs
import re


# In[6]:


from duckduckgo_search import DDGS
import requests
from bs4 import BeautifulSoup
import pandas as pd
import spacy_universal_sentence_encoder


# In[7]:


def find_similarity(text_1:str,text_2:str):
    '''
    Function to remove filler words amd calculate similarity between two textual information

    Args:
        text_1(str): First Sentence/paragraph/textual-information
        text_2(str): Second Sentence/paragraph/textual-information

    Returns:
        similarity_score(float): Percentage Similarity between text_1 and text_2
    '''
    # Complete sentence encoding
    text_1 = nlp(text_1)
    text_2 = nlp(text_2)

    # Encoding without filler and stop words like I,is,am,are,...etc..
    text_1_encoding = nlp(" ".join([str(token) for token in text_1 if not token.is_stop]))
    text_2_encoding = nlp(" ".join([str(token) for token in text_2 if not token.is_stop]))

    similarity_score = text_1_encoding.similarity(text_2_encoding)
    
    return similarity_score


# In[8]:


def fetch_query_links(query:str):
    '''
    Fetch links of top results for the quesry from DuckDuckGo search engine

    Args:
        query(str): Query to be searched by DuckDuckGo search engine

    Returns:
        links(list[tuple[str,str]]): List of tuples containing headline/title of web page and link of that web page
    '''
    links = []
    # fetch results from DuckDuckGo search engine
    query_results = ddgs.text(region='us-en',keywords=query,max_results=10)
    # itterate over results to collect relevant information
    for result in query_results:
        title = result['title']
        link = result['href']
        links.append((title,link))

    return links


# In[9]:


def scrap_text_from_website(link:str):
    '''
    Collect HTML response from website and scrap it to extract relevant information

    Args:
        link(str): Web address of the target website.

    Returns:
        data(str): Scrapped data in string format
    '''
    website_response = requests.get(link,headers=AGENT)     # fetch reponse from website
    website_content = website_response.content              # extract HTML content
    soup = BeautifulSoup(website_content)                   # parse HTML with BS4
    data = soup.getText()                                   # extract text information

    return data


# In[11]:


QUERIES = [
    "Identify the industry in which Canoo operates, along with its size, growth rate, trends, and key players.",
    "Analyze Canoo's main competitors, including their market share, products or services offered, pricingstrategies, and marketing efforts.",
    "Identify key trends in the market, including changes in consumer behavior, technological advancements, and shifts in the competitive landscape."
    "Gather information on Canoo's financial performance, including its revenue, profit margins, return on investment, and expense structure."
    ]

# To bypass web-crawling restrictions
AGENT = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'}

ddgs = DDGS()
nlp = spacy_universal_sentence_encoder.load_model('en_use_lg')


# Initialize Structure data dictionary to support Pandas DataFrame
structured_data = {
    'Query':[],
    'Title':[],
    'Source':[],
    'Data':[]
}


# In[16]:


# Initialize Structure data dictionary to support Pandas DataFrame
structured_data = {
    'Query':[],
    'Title':[],
    'Source':[],
    'Data':[]
}

# Complete Pipeline to collect and store data
for e,query in enumerate(QUERIES):
    print(f'Executing Query : {e+1}')
    links = fetch_query_links(query=query)  # fetch first 10 webpage's links related to query
    
    for head,link in links:
        
        data = scrap_text_from_website(link) # scrap data from websites

        # Check whether similar data already exsist in database for that query
        add_in_database = True
        for checker,prev_data in enumerate(structured_data['Data']):
            if structured_data['Query'][e] == query:
                if find_similarity(prev_data,data) > 0.8:
                    add_in_database = False

        # Update Database with new information
        if add_in_database:
            structured_data['Query'].append(query)
            structured_data['Title'].append(head)
            structured_data['Source'].append(link)
            structured_data['Data'].append(data)


# converting Structured data to pandas DataFrame object which is optimized for python
dataframe = pd.DataFrame(structured_data)
print(dataframe.sample(frac=1))

# export structured tabular data to CSV
dataframe.to_csv('retrieved_data.csv',index=False)


# In[17]:


df=pd.read_csv("C:/Users/Aqsa/retrieved_data.csv")


# In[18]:


df.head()


# In[19]:


# Rename the 'Source' column to 'URL'
df.rename(columns={'Source': 'URL'}, inplace=True)


# In[21]:


df.head(5)


# In[26]:


import requests
from bs4 import BeautifulSoup
import pandas as pd

# Function to extract 'History' section text from a given URL using BeautifulSoup
def extraction(url):
    print(f"Processing URL: {url}")
    
    response = requests.get(url)
    print(f"HTTP Status Code: {response.status_code}")
    
    soup = BeautifulSoup(response.text, 'html.parser')

    # Extract title
    title = soup.find('title').text if soup.find('title') else ''
    print(f"Title: {title}")

    # Extract 'History' section
    history_section = soup.find('span', {'id': 'History'})

    # Extract text from the 'History' section
    history_text = ''
    if history_section:
        next_element = history_section.find_next()
        while next_element and not next_element.has_attr('id'):
            history_text += str(next_element)
            next_element = next_element.find_next()

    print(f"History: {history_text}")

    return pd.Series([url, title, history_text], index=['URL', 'Title', 'History'])

# URL to extract data from
url = 'https://en.wikipedia.org/wiki/Lordstown_Motors'

# Create a DataFrame with a single row containing the URL
df = pd.DataFrame({'URL': [url]})

# Apply the extraction function to the DataFrame
df[['URL', 'Title', 'History']] = df['URL'].apply(extraction)

# Display the output DataFrame
print(df)


# In[32]:


import requests
from bs4 import BeautifulSoup

url = "https://en.wikipedia.org/wiki/Lordstown_Motors"

# Fetch the HTML content from the URL
response = requests.get(url)
html_content = response.text

# Use BeautifulSoup to parse the HTML content
soup = BeautifulSoup(html_content, 'html.parser')

# Find the span with id "History" and extract all paragraphs within it
history_span = soup.find('span', {'id': 'History'})

# Check if the history span is found and extract all paragraphs
if history_span:
    history_paragraphs = history_span.find_all_next('p')
    history_text = '\n'.join([' '.join(paragraph.stripped_strings) for paragraph in history_paragraphs])

    print(f"Title: {soup.title.text}")
    print(f"History:\n{history_text}")


# In[50]:


import requests
from bs4 import BeautifulSoup

url = "https://www.prnewswire.com/news-releases/lordstown-motors-reports-fourth-quarter-and-fiscal-year-2021-financial-results-301491478.html"

# Fetch the HTML content from the URL
response = requests.get(url)
html_content = response.text

# Use BeautifulSoup to parse the HTML content
soup = BeautifulSoup(html_content, 'html.parser')

# Extract the title of the page
title = soup.title.text

# Extract all text from the webpage
webpage_text = ' '.join(soup.stripped_strings)

# Print or use the extracted information as needed
print(f"Title: {title}")
print(webpage_text)


# In[51]:


import requests
from bs4 import BeautifulSoup

url = "https://investor.lordstownmotors.com/news-releases/news-release-details/lordstown-motors-corp-announces-reverse-stock-split"
# Fetch the HTML content from the URL
response = requests.get(url)
html_content = response.text

# Use BeautifulSoup to parse the HTML content
soup = BeautifulSoup(html_content, 'html.parser')

# Extract the title of the page
title = soup.title.text

# Extract all text from the webpage
webpage_text = ' '.join(soup.stripped_strings)

# Print or use the extracted information as needed
print(f"Title: {title}")
print(webpage_text)


# In[52]:


import requests
from bs4 import BeautifulSoup

url = 'https://investor.lordstownmotors.com/news-releases/news-release-details/lordstown-motors-announces-production-and-delivery-pause-address'
response = requests.get(url)
html_content = response.text

# Use BeautifulSoup to parse the HTML content
soup = BeautifulSoup(html_content, 'html.parser')

# Extract the title of the page
title = soup.title.text

# Extract all text from the webpage
webpage_text = ' '.join(soup.stripped_strings)

# Print or use the extracted information as needed
print(f"Title: {title}")
print(webpage_text)


# In[53]:


import requests
from bs4 import BeautifulSoup

url = 'https://www.marketscreener.com/quote/stock/LORDSTOWN-MOTORS-CORP-57237498/news/Lordstown-Motors-Provides-Production-and-Financial-Update-36564804/'
html_content = response.text

# Use BeautifulSoup to parse the HTML content
soup = BeautifulSoup(html_content, 'html.parser')

# Extract the title of the page
title = soup.title.text

# Extract all text from the webpage
webpage_text = ' '.join(soup.stripped_strings)

# Print or use the extracted information as needed
print(f"Title: {title}")
print(webpage_text)


# In[62]:


import requests
from bs4 import BeautifulSoup
import csv

# List of URLs to extract data from
urls = [
    "https://en.wikipedia.org/wiki/Lordstown_Motors",
    "https://www.prnewswire.com/news-releases/lordstown-motors-reports-fourth-quarter-and-fiscal-year-2021-financial-results-301491478.html",
    "https://investor.lordstownmotors.com/news-releases/news-release-details/lordstown-motors-corp-announces-reverse-stock-split",
    'https://investor.lordstownmotors.com/news-releases/news-release-details/lordstown-motors-announces-production-and-delivery-pause-address',
    'https://www.marketscreener.com/quote/stock/LORDSTOWN-MOTORS-CORP-57237498/news/Lordstown-Motors-Provides-Production-and-Financial-Update-36564804/'
]

# Create an empty list to store extracted data
data_list = []

# Iterate through each URL
for url in urls:
    response = requests.get(url)
    html_content = response.text
    soup = BeautifulSoup(html_content, 'html.parser')

    # Extract the title and all text from the webpage
    title = soup.title.text
    webpage_text = ' '.join(soup.stripped_strings)

    # Append the extracted data to the list
    data_list.append({
        'Title': title,
        'Text': webpage_text
    })

# Save the data to a single CSV file
csv_file_path = 'extracted_data.csv'
with open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:
    fieldnames = ['Title', 'Text']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

    # Write the header
    writer.writeheader()

    # Write the data
    writer.writerows(data_list)

print(f"Data has been saved to {csv_file_path}")

# Save the data to a single text file
text_file_path = 'extracted_data.txt'
with open(text_file_path, 'w', encoding='utf-8') as text_file:
    for data in data_list:
        text_file.write(f"Title: {data['Title']}\n")
        text_file.write(f"Text: {data['Text']}\n\n")

print(f"Data has been saved to {text_file_path}")


# In[ ]:




