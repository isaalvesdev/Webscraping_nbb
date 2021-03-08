import requests
from bs4 import BeautifulSoup
import pandas as pd
import sqlalchemy

engine = sqlalchemy.create_engine('sqlite:///C:\\Users\\Isabe\\Documents\\Programação\\Python Avançado\\Modulos\\Selenium\\nbb.db',echo = True)



url = 'https://lnb.com.br/nbb/equipes'
r = requests.get(url).text
soup = BeautifulSoup(r,'html.parser')
teams = soup.find("section",{"class":"archive_team_screen_one"})
links_teams = [i.get("href") for i in teams.find_all("a")]



df = []
for links in links_teams:
    
    r_links = requests.get(links).text
    soup_teams = BeautifulSoup(r_links,'html.parser')
    table = soup_teams.find("div",{"class":"tabs-panel is-active table-wrapper"})
    tables = pd.read_html(str(table))[0]
    df.append(tables)
    
data = pd.concat(df,axis=0,ignore_index=False)
data.to_sql("nbb_tb",engine,if_exists = "append",index = False)




