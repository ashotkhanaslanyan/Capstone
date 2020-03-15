import pandas as pd

def clean_trophies(df, sofifa_id, name):
    df.fillna(method='ffill', inplace=True)
    df.columns = ["Competition", "Trophy", "Quantity", "Season"]
    df.insert(0, "sofifa_id", sofifa_id)
    df.insert(1, "Name", name)
    df = df[(df["Competition"] != "Club International") & (df["Competition"] != "Club Domestic") & (
            df["Competition"] != "National")]
    get_quantity = lambda x: int(x.replace("x", ""))
    df.loc[:,"Quantity"] = list(map(get_quantity, df.loc[:,"Quantity"]))
    once = df[df.Quantity == 1]
    multiple = df[df.Quantity > 1]
    for row in range(0, multiple.shape[0]):
        seasons = multiple.iloc[row, 5].split(",")
        competiton = multiple.iloc[row, 2]
        trophy = multiple.iloc[row, 3]
        # sofifa_id = multiple.iloc[row, 0]
        # name = multiple.iloc[row, 1]
        for season in seasons:
            multiple = multiple.append({"sofifa_id": sofifa_id, "Name": name,
                                        "Competition": competiton, "Trophy": trophy, "Quantity": 1, "Season": season},
                                       ignore_index=True)
    multiple = multiple[multiple.Quantity == 1]
    final = once.append(multiple, ignore_index=True)
    final = final.drop(["Quantity"], axis=1)
    return final

def clean_injuries(df, sofifa_id, name):
    df.columns = ["Name", "Reason", "Start Date", "End Date"]
    df["Name"] = name
    df.insert(0, "sofifa_id", sofifa_id)
    return df

def clean_stats_frame(df,teams,player_id, team_ind ,player_name, columns, drop_indexes, drop_cols, id_vars, tm_id): 
    df.drop(df.tail(1).index,inplace=True)
    df.iloc[:,team_ind] = teams
    df = df.drop(df.columns[drop_indexes], axis = 1)
    df.columns = columns
    if not(drop_cols == []):
        df = df.drop(drop_cols, axis = 1)
    df.insert(0,"tm_Id", tm_id)
    df.insert(1,"Player_Id", player_id)
    df.insert(2,"Name", player_name)
    df_long = pd.melt(df, id_vars = id_vars, var_name = "Attribute")
    return df_long

def create_or_open(file_dest, columns):
    data_frame = None
    try:
        data_frame = pd.read_csv(file_dest, index_col = 0)
    except:
        data_frame = pd.DataFrame(columns=columns)
    return data_frame

def create_empty_df(file_dest, columns):
    data_frame = pd.DataFrame(columns=columns)
    data_frame.to_csv(file_dest)


def create_csv_dfs():
    create_empty_df("./Scrapped_Data/injuries.csv", columns = ["sofifa_id","Name","Reason","Start Date","End Date"])
    create_empty_df("./Scrapped_Data/trophies.csv", columns = ["sofifa_id","Name","Competition","Trophy","Season"])
    create_empty_df("./Scrapped_Data/markval.csv", columns = ['Name', 'Club', 'League', 'Season', 'Market Value', "tm_Id"])

def check_if_exists(dest):
    result = True
    try:
        open(dest)
    except IOError:
        result = False
    return result