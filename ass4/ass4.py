import pandas as pd
import numpy as np
import re
from lxml import etree
import scipy.stats as stats

mlb = pd.read_csv('mlb.csv')
nba = pd.read_csv('nba.csv')
nfl = pd.read_csv('nfl.csv')
nhl = pd.read_csv('nhl.csv')

def parse_wiki(page: str) -> pd.DataFrame:
    with open(page, 'r', encoding='iso-8859-1') as f:
        html = f.read()

    tree = etree.HTML(html)

    table  = tree.xpath('//table[@class="wikitable sortable jquery-tablesorter"]')[0]

    data = []

    for row in table.xpath('.//tr'):

        cells = row.xpath('.//td | .//th')
        
        row = []
        for cell in cells:
            text = cell.xpath("descendant-or-self::*/text()")

            pat1 = r'\[.*\]'
            pat2 = r'[^\x00-\x7F]+'

            res = ''.join([re.sub(pat1 + '|' + pat2, '', str.strip()) for str in text])

            row.append(res)
        data.append(row)

    PopTeam = pd.DataFrame(data[1:], columns=data[0])

    PopTeam.rename(columns={'Population(2016 est.)' : 'Population'}, inplace=True)
    PopTeam = PopTeam[['Metropolitan area', 'Population', 'NFL', 'MLB', 'NBA', 'NHL']]
    # print(PopTeam)
    return PopTeam

def filter_mlb_data(mlb: pd.DataFrame) -> pd.DataFrame:
    
    mlb = mlb[mlb['year'] == 2018]
    print(mlb)
    sel_mlb = mlb[['W-L%', 'team']]
    filtered_mlb = sel_mlb[~sel_mlb['team'].isin(['Atlantic Division', 'Metropolitan Division', 'Central Division', 'Pacific Division'])]
    filtered_mlb.rename(columns={"W-L%": "W/L"}, inplace=True)
    return filtered_mlb

def filter_nba_data(nba: pd.DataFrame) -> pd.DataFrame:
    
    nba = nba[nba['year'] == 2018]
    sel_nba = nba[['W/L%', 'team']]
    sel_nba['team'] = sel_nba['team'].str.replace( '(\*\s\((\d+)\))|(\s\((\d+)\))', '', regex=True)
    sel_nba.rename(columns={"W/L%": "W/L"}, inplace=True)
    sel_nba['W/L'] = sel_nba['W/L'].astype(float)
    
    return sel_nba

def filter_nfl_data(nfl: pd.DataFrame) -> pd.DataFrame:
    
    nfl = nfl[nfl['year'] == 2018]
    sel_nfl = nfl[['W-L%', 'team']]
    filtered_nfl = sel_nfl[~sel_nfl['team'].isin(['AFC North', 'AFC South', 'AFC West', 'NFC East','NFC North','NFC South', 'NFC West','AFC East'])]
    filtered_nfl.rename(columns={"W-L%": "W/L"}, inplace=True)
    filtered_nfl['team'] = filtered_nfl['team'].str.rstrip('*+')
    filtered_nfl['W/L'] = filtered_nfl['W/L'].astype(float) 
    
    return filtered_nfl

def filter_nhl_data(nhl: pd.DataFrame) -> pd.DataFrame:

    nhl = nhl[nhl['year'] == 2018]
    sel_nhl = nhl[['W','L', 'team']]
    
    filtered_nhl = sel_nhl[~sel_nhl['team'].isin(['Atlantic Division', 'Metropolitan Division', 'Central Division', 'Pacific Division'])]
    
    filtered_nhl['team'] = filtered_nhl['team'].str.rstrip('*')

    filtered_nhl['W/L'] = filtered_nhl['W'].astype(float)/(filtered_nhl['W'].astype(float) + filtered_nhl['L'].astype(float))
    filtered_nhl.drop(['W', 'L'], axis=1,inplace=True)
    len()
    return filtered_nhl

PopTeam = parse_wiki('wikipedia_data.html')


#########-NHL-#########

# nhl = filter_nhl_data(nhl)

# Pop4nhl = PopTeam[PopTeam['NHL'] != ''][['Metropolitan area', 'Population', 'NHL']].sort_values(by=['NHL'])

# Pop4nhl = PopTeam[['Population', 'NHL', 'Metropolitan area']]
# Pop4nhl.rename(columns={'NHL':'team'}, inplace=True)
# Pop4nhl = Pop4nhl[Pop4nhl['team'] != '']
# Pop4nhl.drop(index=Pop4nhl.index[-1], inplace=True)
# Pop4nhl['Population'] = Pop4nhl['Population'].str.replace(',', '').astype(int)

# nhl['team'] = nhl['team'].apply(lambda x: x.split()[-1])

# Pop4nhl['team'] = Pop4nhl['team'].apply(lambda x: x.split()[-1])
# Pop4nhl['team'] = Pop4nhl['team'].str.findall(r'[A-Z][a-z]*')
# Pop4nhl = Pop4nhl.explode('team')

# merge = pd.merge(Pop4nhl, nhl, on='team', how='right')

# metropolitan_winrate = merge.groupby('Metropolitan area')['W/L'].mean()

# popWinrateNHL = pd.merge(metropolitan_winrate, Pop4nhl.drop('team', axis=1), on='Metropolitan area', how='right').drop_duplicates()
# popWinrateNHL.set_index('Metropolitan area')

# corr = stats.pearsonr(popWinrateNHL['W/L'],popWinrateNHL['Population'])[0]
# print(corr)

#########-NBA-#########

# Pop4nba = PopTeam[PopTeam['NBA'] != ''][['Metropolitan area', 'Population', 'NBA']].sort_values(by=['NBA'])

# Pop4nba = PopTeam[['Population', 'NBA', 'Metropolitan area']]
# Pop4nba.rename(columns={'NBA':'team'}, inplace=True)
# Pop4nba = Pop4nba[Pop4nba['team'] != '']

# Pop4nba.drop(index=Pop4nba.index[-1], inplace=True)
# Pop4nba['Population'] = Pop4nba['Population'].str.replace(',','').astype(int)

# nba = filter_nba_data(nba)

# nba['team'] = nba['team'].apply(lambda x: x.split()[-1])

# Pop4nba['team'] = Pop4nba['team'].apply(lambda x: x.split()[-1])
# Pop4nba['team'] = Pop4nba['team'].str.findall(r'[A-Z][a-z]*|\d.*')
# Pop4nba = Pop4nba.explode('team')

# merge = pd.merge(Pop4nba, nba, on='team', how='right')

# metropolitan_winrate = merge.groupby('Metropolitan area')['W/L'].mean()

# popWinrateNBA = pd.merge(metropolitan_winrate, Pop4nba.drop('team', axis=1), on='Metropolitan area', how='right').drop_duplicates()

# popWinrateNBA.set_index('Metropolitan area')
# # print(popWinrateNBA)
# corr = stats.pearsonr(popWinrateNBA['W/L'], popWinrateNBA['Population'])[0]

# print(corr)

#########-MLB-#########

# PopTeam = parse_wiki('wikipedia_data.html')
# Pop4MLB = PopTeam[PopTeam['MLB'] != ''][['Metropolitan area', 'Population', 'MLB']].sort_values(by=['MLB'])

# Pop4MLB = PopTeam[['Population', 'MLB', 'Metropolitan area']]
# Pop4MLB.rename(columns={'MLB':'team'}, inplace=True)
# Pop4MLB = Pop4MLB[Pop4MLB['team'] != '']

# Pop4MLB.drop(index=Pop4MLB.index[-1], inplace=True)
# Pop4MLB['Population'] = Pop4MLB['Population'].str.replace(',','').astype(int)


# mlb = filter_mlb_data(mlb)


# mlb['team'] = mlb['team'].apply(lambda x: x.split()[-1])

# mlb.loc[mlb['W/L'] == 0.667, 'team'] = 'White'
# mlb.loc[mlb['team'] == 'Sox', 'team'] = 'Red' 

# Pop4MLB['team'] = Pop4MLB['team'].str.findall(r'[A-Z][a-z]*|\d.*')

# Pop4MLB = Pop4MLB.explode('team')

# merge = pd.merge(Pop4MLB, mlb, on='team', how='right')
# # print(mlb)

# print(merge[merge['Metropolitan area'] == 'Chicago'])
# print(merge[merge['Metropolitan area'] == 'Boston'])
# print(merge[merge['Metropolitan area'] == 'San Francisco Bay Area'])

# metropolitan_winrate = merge.groupby('Metropolitan area')['W/L'].mean()

# popWinrateMLB = pd.merge(metropolitan_winrate, Pop4MLB.drop('team', axis=1), on='Metropolitan area', how='right').drop_duplicates()

# popWinrateMLB.set_index('Metropolitan area')


# mask = popWinrateMLB['Metropolitan area'].isin(['Chicago', 'Boston'])
# # print(mask)
# popWinrateMLB.loc[mask, 'W/L'] = [0.482769,0.666667]
# print(popWinrateMLB)

# corr = stats.pearsonr(popWinrateMLB['Population'], popWinrateMLB['W/L'])[0]

# print(corr)


#########-NFL-#########

PopTeam = parse_wiki('wikipedia_data.html')
Pop4NFL = PopTeam[PopTeam['NFL'] != ''][['Metropolitan area', 'Population', 'NFL']].sort_values(by=['NFL'])

Pop4NFL = PopTeam[['Population', 'NFL', 'Metropolitan area']]
Pop4NFL.rename(columns={'NFL':'team'}, inplace=True)
Pop4NFL = Pop4NFL[Pop4NFL['team'] != '']

Pop4NFL.drop(index=Pop4NFL.index[-1], inplace=True)
Pop4NFL['Population'] = Pop4NFL['Population'].str.replace(',','').astype(int)

nfl = filter_nfl_data(nfl)

nfl['team'] = nfl['team'].apply(lambda x: x.split()[-1])

nfl.loc[nfl['W/L'] == 0.667, 'team'] = 'White'
nfl.loc[nfl['team'] == 'Sox', 'team'] = 'Red' 

Pop4NFL['team'] = Pop4NFL['team'].str.findall(r'[A-Z][a-z]*|\d.*')

Pop4NFL = Pop4NFL.explode('team')

merge = pd.merge(Pop4NFL, nfl, on='team', how='right')


metropolitan_winrate = merge.groupby('Metropolitan area')['W/L'].mean()

popWinrateNFL = pd.merge(metropolitan_winrate, Pop4NFL.drop('team', axis=1), on='Metropolitan area', how='left').drop_duplicates()

popWinrateNFL.set_index('Metropolitan area')

print(popWinrateNFL[popWinrateNFL['Metropolitan area'] == 'New York City'])

corr = stats.pearsonr( popWinrateNFL['Population'],popWinrateNFL['W/L'])[0]

print(corr - 0.027884914405012548)
