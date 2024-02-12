import re
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import pandas as pd
import lyricsgenius as lg



api_key = '8wCh_XDvpgDsH1PZhstKFSSjS7DfJtXYl6gGfu_3iQb7cQr5OM0LzmdAIDYo8U0H'
genius = lg.Genius(api_key, skip_non_songs=True, excluded_terms=["(Remix)", "(Live)"], remove_section_headers=True)

def lyrics_from_title(song_title, artist):
    song = genius.search_song("505", "Arctic Monkeys")
    lyrics = song.lyrics
    return lyrics



page_url = "https://kworb.net/spotify/"

uClient = uReq(page_url) # downloads the html page from page_url

page_soup = soup(uClient.read(), "html.parser") # parses html into a readable alphabet soup

country_soup = page_soup.find("table") # narrows html down to the country

country_soup_list = country_soup.find_all("tr") # get each row of the country soup

country_dict_links = {}

for entry in country_soup_list:
    
    country_name = entry.contents[0].string # country name
    country_links = []
    for link in entry.contents[2].find_all("a"):
        
        country_links.append(link.get('href'))
    country_dict_links[country_name] = country_links

country_top_info = {country:{"links":country_dict_links[country]} for country in country_dict_links.keys()}
country_top_info_df = pd.DataFrame(country_dict_links.items(), columns=['Country', 'Links'])
country_abbv = {}
for country in country_dict_links.keys():
    daily_link = country_dict_links[country][0]
    match = re.search(r'country/(\w+)_daily.html', daily_link)
    abbv = match.group(1)
    country_abbv[country] = abbv
abbv_df = pd.DataFrame(list(country_abbv.items()), columns=['Country', 'Abbreviation'])
country_top_info_df.columns
country_top_info_df.merge(abbv_df)

# Iterate through each row and each item in the list column
daily_paths = {}
for index, row in country_top_info_df.iterrows():
    country = row['Country']
    paths = row['Links']
    daily_paths[country] = paths

def generate_dataset(path, country):
    page_url = f"https://kworb.net/spotify/{path}"
    
    uClient = uReq(page_url) # downloads the html page from page_url

    page_soup = soup(uClient.read(), "html.parser") # parses html into a readable alphabet soup

    spotify_entry_soup = page_soup.find("table") # narrows html down to the country
    
    headings = [th.get_text() for th in spotify_entry_soup.find("tr").find_all("th")]

    datasets = []
    for row in spotify_entry_soup.find_all("tr")[1:]:
        dataset = zip(headings, (td.get_text() for td in row.find_all("td")))
        datasets.append(dataset)
        
    dataset_tuples = [list(zip(dataset)) for dataset in datasets]
    
    # Convert the data into a dictionary to handle repeated attributes
    dict_data = {}
    for sublist in dataset_tuples:
        for tup in sublist:
            attribute, value = tup[0]
            if attribute in dict_data:
                dict_data[attribute].append(value)
            else:
                dict_data[attribute] = [value]

    # Create a DataFrame from the dictionary
    df = pd.DataFrame(dict_data)
    df = df.set_index("Pos")
    
    df[['Artist', 'Title']] = df["Artist and Title"].str.split("-", 1, expand=True)
    
    df_obj = df.select_dtypes('object')
    df[df_obj.columns] = df_obj.apply(lambda x: x.str.strip())
    
    df = df.reset_index()
    
    df["Country"] = country
    
    return df

dfs = []
for country in daily_paths:
    try:
        dfs.append(generate_dataset(daily_paths[country][0], country))
    except:
        continue


# def export(df):
#     df.to_csv

# top_200_songs_by_country = pd.concat(dfs, ignore_index=True)
# top_200_songs_by_country.to_csv("top_200_songs_by_country.csv", index=False)

# new_df = pd.DataFrame(columns=['Country', 'Artist', 'Title', 'Lyrics'])

# df = []

# for index, row in df.iterrows():
#     country = row['Country']
#     artist = row['Artist']
#     title = row['Title']
        
#     lyrics = lyrics_from_title(title, artist)
        
#     new_df = new_df.append({'Country': country, 'Artist': artist, 'Title': title, 'Lyrics': lyrics}, ignore_index=True)

