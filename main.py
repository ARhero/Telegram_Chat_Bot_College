import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
requests.get("https://api.telegram.org/bot6853528823:AAE4p-zFzNLdJoREhhRAbYmA_7mgjKqhWQs/sendMessage?chat_id=-4103221629&text='bot is on now'")
url = 'https://www.soa.ac.in/iter'
hrefs_file = 'hrefs.csv'
texts_file = 'texts.csv'
if not os.path.isfile(hrefs_file):
    pd.DataFrame(columns=['links']).to_csv(hrefs_file, index=False)
if not os.path.isfile(texts_file):
    pd.DataFrame(columns=['titles']).to_csv(texts_file, index=False)
base_url = "https://api.telegram.org/bot6853528823:AAE4p-zFzNLdJoREhhRAbYmA_7mgjKqhWQs/sendMessage?chat_id=-1001719304073&text={}"
base_url2 = "https://api.telegram.org/bot6853528823:AAE4p-zFzNLdJoREhhRAbYmA_7mgjKqhWQs/sendMessage?chat_id=-1001609971210&text={}"
def send_to_telegram(text, href):
    text = text.replace('&', 'and')
    href = href.replace('&', 'and')
    message = f"🔔 | {text} | 🔔\n\n🔗 Tap on the link below 🔗:\n\nhttps://www.soa.ac.in{href}"
    requests.get(base_url.format(message))
    requests.get(base_url2.format(message))
def scrape_website(url):
    hrefs_df = pd.read_csv(hrefs_file)
    texts_df = pd.read_csv(texts_file)
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        summary_title_links = soup.find_all('a', class_='summary-title-link')
        new_hrefs = []
        new_texts = []
        for link in summary_title_links:
            href = link['href']
            text = link.get_text()
            if href not in hrefs_df['links'].values:
                new_hrefs.append(href)
                new_texts.append(text)
        if new_hrefs:
            new_hrefs_df = pd.DataFrame({'links': new_hrefs})
            hrefs_df = pd.concat([hrefs_df, new_hrefs_df], ignore_index=True)
            hrefs_df.to_csv(hrefs_file, index=False)
        if new_texts:
            new_texts_df = pd.DataFrame({'titles': new_texts})
            texts_df = pd.concat([texts_df, new_texts_df], ignore_index=True)
            texts_df.to_csv(texts_file, index=False)
        for text, href in zip(new_texts, new_hrefs):
            send_to_telegram(text, href)
    else:
        print("Failed to retrieve the webpage. Status code:", response.status_code)
scrape_website(url)
