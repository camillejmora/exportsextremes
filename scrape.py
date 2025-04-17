import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

# Load the Excel file
excel_file = '/Users/cmor7802/repos/exports/data/raw/interventions-2.xlsx' 
df = pd.read_excel(excel_file)

# Access column with URLs
url_column = 'State Act URL'

word_to_find = ['drought', 'heat', 'rain', 'flood', 'fire', 'monsoon', 'storm']
pattern = r'\b(' + '|'.join(map(re.escape, word_to_find)) + r')\b'

results = []

# Iterate through the URLs in the specified column
for url in df[url_column]:
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        content = response.text.lower()
        found = 'Y' if re.search(pattern, content, re.IGNORECASE) else 'N'
        results.append({'URL': url, 'Found': found})
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        results.append({'URL': url, 'Found': 'Error'})  # Mark as error if URL can't be fetched

# Create a new DataFrame from the results
results_df = pd.DataFrame(results)

df = pd.DataFrame(results)
df.to_excel('results.xlsx', index=False)