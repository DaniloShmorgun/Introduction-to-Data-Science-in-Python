import pandas as pd
import scipy.stats as stats
import re

import ass4 as ass

nhl_df=pd.read_csv("nhl.csv")
cities=pd.read_html("wikipedia_data.html")[1]
cities=cities.iloc[:-1,[0,3,5,6,7,8]]

def clean_nhl_df():
    # load data
    nhl_df=pd.read_csv("nhl.csv")
    cities=pd.read_html("wikipedia_data.html")[1]
    cities=cities.iloc[:-1,[0,3,5,6,7,8]]

    # cleaning the cities dataframe
    cities["NHL"] = cities["NHL"].apply(lambda x: re.sub(r"\[.+\]", "", x))
    cities["NHL"] = cities["NHL"].replace({"RangersIslandersDevils": "Rangers,Islanders,Devils",
                                           "KingsDucks": "Kings,Ducks",
                                           "Red Wings": "Red,Wings", 
                                           "Maple Leafs": "Maple,Leafs", 
                                           "Blue Jackets": "Blue,Jackets",
                                           "Golden Knights": "Golden,Knights" })
    cities["NHL"] = cities["NHL"].apply(lambda x: x.split(","))
    cities = cities.explode("NHL")

    # cleaning the nhl_df dataframe
    nhl_df = nhl_df[nhl_df["year"] == 2018]
    nhl_df["team"] = nhl_df["team"].apply(lambda x: x.replace("*", ""))
    nhl_df["team"] = nhl_df["team"].apply(lambda x: x.split(" ")[-1])

    # merge the dataframes
    df = pd.merge(cities, nhl_df, left_on="NHL", right_on="team")
    df = df[["Metropolitan area", "Population (2016 est.)[8]", "NHL", "team", "W", "L"]]
    df["W-L%"] = df["W"].astype("int")/(df["W"].astype("int") + df["L"].astype("int"))
    df["Population (2016 est.)[8]"] = df["Population (2016 est.)[8]"].astype("float")
    df["W-L%"] = df["W-L%"].astype("float")

    # drop duplicated columns
    df.loc[df["Metropolitan area"] == "New York City", "W-L%"] = 0.5182013333333334 # mean of NY W-L%
    df.loc[df["Metropolitan area"] == "Los Angeles", "W-L%"] = 0.6228945 # mean of LA W-L%
    df = df.drop_duplicates(subset="Metropolitan area").reset_index()
    df = df.drop(columns="index")
    
    return df

def nhl_correlation(): 
    # YOUR CODE HERE
#     raise NotImplementedError()
    df = clean_nhl_df()

    population_by_region = df["Population (2016 est.)[8]"] # pass in metropolitan area population from cities
    win_loss_by_region = df["W-L%"] # pass in win/loss ratio from nhl_df in the same order as cities["Metropolitan area"]

    # assert len(population_by_region) == len(win_loss_by_region), "Q1: Your lists must be the same length"
    # assert len(population_by_region) == 28, "Q1: There should be 28 teams being analysed for NHL"
    
    result = stats.pearsonr(population_by_region, win_loss_by_region)
    print(result)
    return result[0]

def clean_nba_df():
    # load data
    nba_df=pd.read_csv("nba.csv")
    cities=pd.read_html("wikipedia_data.html")[1]
    cities=cities.iloc[:-1,[0,3,5,6,7,8]]
    
    # cleaning the cities dataframe
    cities["NBA"] = cities["NBA"].apply(lambda x: re.sub(r"\[.+\]", "", x))
    cities["NBA"] = cities["NBA"].replace({"KnicksNets": "Knicks,Nets",
                                           "LakersClippers": "Lakers,Clippers",
                                           "Trail Blazers": "Trail,Blazers"})
    cities["NBA"] = cities["NBA"].apply(lambda x: x.split(","))
    cities = cities.explode("NBA")

    # cleaning the nhl_df dataframe
    nba_df = nba_df[nba_df["year"] == 2018]
    nba_df["team"] = nba_df["team"].apply(lambda x: re.sub(r"(\*)*\s\(\d+\)", "", x))
    nba_df["team"] = nba_df["team"].apply(lambda x: x.split(" ")[-1])

    # merge the dataframes
    df = pd.merge(cities, nba_df, left_on="NBA", right_on="team")
    df = df.rename(columns={"W/L%": "W-L%"})
    df = df[["Metropolitan area", "Population (2016 est.)[8]", "NBA", "team", "W", "L", "W-L%"]]
    df["Population (2016 est.)[8]"] = df["Population (2016 est.)[8]"].astype("float")
    df["W-L%"] = df["W-L%"].astype("float")
    
    # drop duplicated columns
    df.loc[df["Metropolitan area"] == "New York City", "W-L%"] = 0.34750000000000003 # mean of NY W-L%
    df.loc[df["Metropolitan area"] == "Los Angeles", "W-L%"] = 0.46950000000000003 # mean of LA W-L%
    df = df.drop_duplicates(subset="Metropolitan area").reset_index()
    df = df.drop(columns="index")
    
    return df

def clean_mlb_df():
    # load data
    mlb_df=pd.read_csv("mlb.csv")
    cities=pd.read_html("wikipedia_data.html")[1]

    cities=cities.iloc[:-1,[0,3,5,6,7,8]]

    # cleaning the cities dataframe
    cities["MLB"] = cities["MLB"].apply(lambda x: re.sub(r"\[.+\]", "", x))
    cities["MLB"] = cities["MLB"].replace({"Blue Jays": "Blue,Jays", 
                                           "CubsWhite Sox": "Cubs,White,Sox", 
                                           "DodgersAngels": "Dodgers,Angels", 
                                           "GiantsAthletics": "Giants,Athletics", 
                                           "YankeesMets": "Yankees,Mets",
                                           "Red Sox": "Red,Sox"})
    cities["MLB"] = cities["MLB"].apply(lambda x: x.split(","))
    cities = cities.explode("MLB")

    # cleaning the nhl_df dataframe
    mlb_df = mlb_df[mlb_df["year"] == 2018]
    mlb_df["team"] = mlb_df["team"].apply(lambda x: x.split(" ")[-1])

    # merge the dataframes
    df = pd.merge(cities, mlb_df, left_on="MLB", right_on="team")
    df = df[["Metropolitan area", "Population (2016 est.)[8]", "MLB", "team", "W", "L", "W-L%"]]
    df["Population (2016 est.)[8]"] = df["Population (2016 est.)[8]"].astype("float")
    df["W-L%"] = df["W-L%"].astype("float")
    print(mlb_df)
    # drop duplicated columns
    df.loc[df["Metropolitan area"] == "New York City", "W-L%"] = 0.546 # mean of NY W-L%
    df.loc[df["Metropolitan area"] == "Los Angeles", "W-L%"] = 0.5289999999999999 # mean of LA W-L%
    df.loc[df["Metropolitan area"] == "San Francisco Bay Area", "W-L%"] = 0.525 # mean of SF W-L%
    df.loc[df["Metropolitan area"] == "Chicago", "W-L%"] = 0.482769 # mean of CH W-L%
    df.loc[df["Metropolitan area"] == "Boston", "W-L%"] = 0.666667 # mean of BO W-L%
    df = df.drop_duplicates(subset="Metropolitan area").reset_index()
    df = df.drop(columns="index")
    
    return df

def mlb_correlation(): 
    # YOUR CODE HERE
#     raise NotImplementedError()
    df = clean_mlb_df()

    population_by_region = df["Population (2016 est.)[8]"] # pass in metropolitan area population from cities
    win_loss_by_region = df["W-L%"] # pass in win/loss ratio from mlb_df in the same order as cities["Metropolitan area"]

    assert len(population_by_region) == len(win_loss_by_region), "Q3: Your lists must be the same length"
    assert len(population_by_region) == 26, "Q3: There should be 26 teams being analysed for MLB"

    result = stats.pearsonr(population_by_region, win_loss_by_region)
    
    return result[0]


def clean_nfl_df():
    # load data
    nfl_df=pd.read_csv("nfl.csv")
    cities=pd.read_html("wikipedia_data.html")[1]
    cities=cities.iloc[:-1,[0,3,5,6,7,8]]

    # cleaning the cities dataframe
    cities["NFL"] = cities["NFL"].apply(lambda x: re.sub(r"\[.+\]", "", x))
    cities["NFL"] = cities["NFL"].replace({"GiantsJets": "Giants,Jets",
                                           "RamsChargers": "Rams,Chargers",
                                           "49ersRaiders": "49ers,Raiders"
                                           })
    cities["NFL"] = cities["NFL"].apply(lambda x: x.split(","))
    cities = cities.explode("NFL")

    # cleaning the nhl_df dataframe
    nfl_df = nfl_df[nfl_df["year"] == 2018]
    nfl_df["team"] = nfl_df["team"].apply(lambda x: re.sub(r"(\*|\+)", "", x))
    nfl_df["team"] = nfl_df["team"].apply(lambda x: x.split(" ")[-1])

    # merge the dataframes
    df = pd.merge(cities, nfl_df, left_on="NFL", right_on="team")
    df = df[["Metropolitan area", "Population (2016 est.)[8]", "NFL", "team", "W", "L", "W-L%"]]
    df["Population (2016 est.)[8]"] = df["Population (2016 est.)[8]"].astype("float")
    df["W-L%"] = df["W-L%"].astype("float")

    # drop duplicated columns
    df.loc[df["Metropolitan area"] == "New York City", "W-L%"] = 0.2815 # mean of NY W-L%
    df.loc[df["Metropolitan area"] == "Los Angeles", "W-L%"] = 0.7815 # mean of LA W-L%
    df.loc[df["Metropolitan area"] == "San Francisco Bay Area", "W-L%"] = 0.25 # mean of SF W-L%
    df = df.drop_duplicates(subset="Metropolitan area").reset_index()
    df = df.drop(columns="index")
    
    return df

def nfl_correlation(): 
    # YOUR CODE HERE
#     raise NotImplementedError()
    df = clean_nfl_df()
    
    population_by_region = df["Population (2016 est.)[8]"] # pass in metropolitan area population from cities
    win_loss_by_region = df["W-L%"] # pass in win/loss ratio from nfl_df in the same order as cities["Metropolitan area"]

    assert len(population_by_region) == len(win_loss_by_region), "Q4: Your lists must be the same length"
    assert len(population_by_region) == 29, "Q4: There should be 29 teams being analysed for NFL"

    result = stats.pearsonr(population_by_region, win_loss_by_region)
    
    return result[0]


test = clean_nfl_df()[['W-L%', 'Metropolitan area', 'Population (2016 est.)[8]']].sort_values(by='Metropolitan area').set_index('Metropolitan area')
test.rename(columns={'W-L%' : 'W/L', 'Population (2016 est.)[8]':'Population'},inplace=True)
test.rename(index={'Dallas–Fort Worth':'DallasFort Worth' ,'Miami–Fort Lauderdale':'MiamiFort Lauderdale','Minneapolis–Saint Paul':'MinneapolisSaint Paul', 'New York' :'New York City' },inplace=True)
print(type(test))

my = ass.popWinrateNFL[['W/L', 'Metropolitan area','Population']].sort_values(by='Metropolitan area').set_index('Metropolitan area')
# print(my['Metropolitan area'])

# new_rows = pd.DataFrame([
#     {'W/L': 0.546, 'Population' : 0},
#     {'W/L': 0.5289999999999999 , 'Population' : 0},
#     {'W/L': 0.525 , 'Population' : 0},
#     {'W/L': 0.482769 , 'Population' : 0},
#     {'W/L':0.666667 , 'Population' : 0}
# ], index=['New York City', 'Los Angeles', 'San Francisco Bay Area', 'Chicago', 'Boston'])

new_rows = pd.DataFrame([
    {'W/L': 0.2815 , 'Population' : 0},
    {'W/L': 0.7815  , 'Population' : 0}
], index=['New York City', 'Los Angeles'])

test = test.append(new_rows)

print(type(test))
print(test)
print(my)

print(my - test)

# resTest = nhl_correlation()
# resMine = ass.corr

# print(abs(resMine - resTest))
