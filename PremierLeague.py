import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
import numpy as np


def espn_table(url):

    """Get League Table after ESPN changed their website."""

    ESPN = requests.get(url).content
    ESPNsoup = BeautifulSoup(ESPN, 'lxml')
    TableHTML = ESPNsoup.find_all("table")

    Table = pd.read_html(str(TableHTML[2]))[0]
    Table = Table.drop(index=[0, 1], axis=0)[["GP", "W", "D", "L", "F", "A", "GD", "P"]]
    Table.columns = ['Played', 'Won', 'Drawn', 'Lost', 'GF', 'GA', 'GD', 'Points']
    Table = Table.reset_index().drop(columns="index").iloc[0:20]

    Teams = pd.read_html(str(TableHTML[1]))[0]
    team_array = np.array(Teams)
    team_list = list()
    for team in team_array:
        nums = (re.findall("\d", team[0]))
        if len(nums) > 1:
            nums = nums[0] + (nums[1])
        else:
            nums = nums[0]
        tm = team[0].replace(nums, "")
        team_list.append(tm[3:])

    Table["Club"] = team_list

    Table = Table[["Club", "Played", "Won", "Drawn", "Lost", "GF", "GD", "Points"]]

    # Table = Table.drop(columns="Unnamed: 0")

    """Before ESPN changed their website"""

    #     for name in Table['Club']:
    #         Table = Table.replace(name, name[:-3])
    #     nums = list()
    #     for name in Table['Club']:
    #         num = re.findall('\d', name)
    #         nums.append(num)
    #     positions = list()
    #     for n in nums[0:9]:
    #         for pos in n:
    #             positions.append(pos)
    #     for pairs in nums[9:]:
    #         positions.append(''.join(pairs))
    #     clubs = list()
    #     for name in Table['Club']:
    #         for char in name:
    #             if char in str(list(range(10))):
    #                 name = name.replace(char, '')
    #         clubs.append(name)
    #     Table['Club'] = clubs
    #     Table['Position'] = positions

    #     Table = Table[['Position', 'Club', 'Played', 'Won', 'Drawn', 'Lost', 'GF', 'GA', 'GD', 'Points']]

    return Table

def stats_table(table):
    club_table = pd.DataFrame(table['Club'])
    total_games = table['Played'].values[0]
    win_pct = list()
    wins = table['Won'].values
    for team in wins:
        win_pct.append(round(team/total_games*100, 2))
    club_table['WinPCT'] = win_pct
    return club_table


def league(url):
    table = espn_table(url)
    stats = stats_table(table)
    champions_league = table[:4]
    return table, stats, champions_league


def player_stats(url):
    player_page = requests.get(url)
    player_content = player_page.content
    player_soup = BeautifulSoup(player_content, 'lxml')
    gk_html = player_soup.find_all('table')[2]
    outfield_html = player_soup.find_all('table')[5]
    gk_table = pd.read_html(str(gk_html))[0]
    gk_table = gk_table.drop('Unnamed: 13', axis=1)
    gk_table.columns = ['POS', 'NO', 'Name', 'Age', 'Apps', 'SubIn', 'S', 'GC', 'A', 'FC', 'FA', 'YC', 'RC']
    outfield_table = pd.read_html(str(outfield_html))[0]
    outfield_table.columns = ['POS', 'NO', 'Name', 'Age', 'Apps', 'SubIn', 'G', 'A', 'SH', 'ST', 'FC', 'FA', 'YC', 'RC']
    return gk_table, outfield_table


league_table = espn_table("http://www.espn.com/soccer/standings/_/league/eng.1")

utd_gk, utd_field = player_stats("http://www.espn.com/soccer/team/squad/_/id/360/manchester-united")

# league_table = pd.read_csv("Data/Week18Table.csv")
# league_table = league_table.drop(columns="Unnamed: 0")

# stat_table.to_csv('Data/Week18Stats.csv')
# league_table.to_csv('Data/Week21Table.csv')
# utd_gk.to_csv('Data/Week21GK.csv')
# utd_field.to_csv('Data/Week21Field.csv')
