import pandas as pd

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