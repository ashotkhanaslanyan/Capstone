import pandas as pd

def clean_stats_frame(df,teams,player_id,player_name, columns, drop_indexes, id_vars): 
    df.drop(df.tail(1).index,inplace=True)
    df.iloc[:,1] = teams
    df = df.drop(df.columns[drop_indexes], axis = 1)
    df.columns = columns
    df.insert(0,"Player_Id", player_id)
    df.insert(1,"Name", player_name)
    df_long = pd.melt(df, id_vars = id_vars, var_name = "Attribute")
    return df_long