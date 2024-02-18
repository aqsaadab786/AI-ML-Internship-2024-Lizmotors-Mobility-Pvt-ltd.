# AI-ML-Internship-2024-Lizmotors-Mobility-Pvt-ltd.

The following diagram illustrates the retrieval-augmented generation pattern. Although the diagram shows a question-answering example, the same workflow supports other use cases.
![image](https://github.com/aqsaadab786/AI-ML-Internship-2024-Lizmotors-Mobility-Pvt-ltd./assets/118045039/a7de2441-f949-49c4-ba9a-1cdb41cb7a73)

## The retrieval-augmented generation pattern involves the following steps:

* Search in your knowledge base for content that is related to the user's input.
* Pull the most relevant search results into your prompt as context and add an instruction, such as “Answer the following question by using only information from the following passages.”
* Only if the foundation model that you're using is not instruction-tuned: Add a few examples that demonstrate the expected input and output format.
* Send the combined prompt text to the model to generate output.
## Here step-by-step how i approach this assighnment:
### step1: Importing Libraries
*Web Scraping Libraries:Import the necessary libraries for web scraping, such as requests for making HTTP requests and BeautifulSoup for parsing HTML.
### Data Manipulation Libraries:
* Import libraries like pandas for data manipulation and storage and csv for handling CSV files.
### Step 2: Function for Web Scraping
* Web Scraping Function:Define a function (extraction) that takes a URL as input, fetches the HTML content, and extracts relevant information using BeautifulSoup. The function might return a Pandas Series with data like URL, title, and history.
### step 3: URL to Extract Data
* Specify URL:Set the URL of the webpage from which you want to extract data. For example, 'https://en.wikipedia.org/wiki/Lordstown_Motors'.
### step 4: DataFrame Initialization
* Initialize DataFrame:Create a Pandas DataFrame with a single row containing the specified URL. This DataFrame will be used to store the extracted data.
### step 5: Applying Extraction Function
* Apply Extraction Function:Apply the extraction function to the DataFrame to extract data from the specified URL. This might involve creating new columns like 'Title' and 'History' in the DataFrame.
### step 6: List of URLs:
* Create a list of URLs from which you want to extract data. These URLs can be from different sources or pages.
### step 7: Creating Empty List for Data
* List for Data Storage:Create an empty list to store the extracted data. This list will be populated by dictionaries, where each dictionary represents data from a specific URL.
### step 8: Iterate Over URLs:
*Iterate over the list of URLs.:For each URL, perform web scraping, extract relevant information, and store it as a dictionary in the list.
### step 9: Saving Data to CSV and Text Files
*Save to CSV and Text Files: After extracting data from all URLs, save the collected data to a single CSV file (extracted_data.csv) and a single text file (extracted_data.txt).
## These steps outline the process of web scraping, data extraction, and storage in a structured format.
## Chalenges:
* In the process of completing the task, I encountered challenges while attempting to extract data from HTML content on various websites. To address this, I delved into researching and exploring different methods, eventually finding a solution that involved utilizing Python libraries such as requests for fetching HTML content and BeautifulSoup for parsing and extracting the relevant information. By leveraging these libraries, along with Pandas for data manipulation, I streamlined the web scraping process. Despite facing difficulties in the past, the experience contributed to continuous learning and a better understanding of effective strategies for extracting and organizing data from diverse online sources.






## Conclusion:
* In conclusion, the provided steps detail the process of web scraping and extracting information from various URLs related to Lordstown Motors. By utilizing Python libraries like requests and BeautifulSoup, along with Pandas for data handling, the code demonstrates how to collect and organize data systematically. The final output includes a Pandas DataFrame showcasing the extracted information, which is then saved in both CSV and text file formats for further analysis or reference.
