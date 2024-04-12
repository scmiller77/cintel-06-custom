from pathlib import Path

import pandas as pd

# Load data
app_dir = Path(__file__).parent

matches_df = pd.read_csv(app_dir / "wta_proj_matches_2023.csv", dtype={"person_id": str})

#Make df of unique player names
unique_players_df = matches_df['name'].drop_duplicates().reset_index(drop=True)

print(len(unique_players_df))

def calculate_player_stats(df, player_name):
    # Filter rows for the specified player
    player_df = df[df['name'] == player_name]

    # Count total matches
    total_matches = len(player_df)

    # Count wins
    wins = len(player_df[player_df['w/l'] == 'W'])

    # Calculate win percentage
    if total_matches != 0:
        win_percentage = round((wins / total_matches) * 100, 2)
    else:
        win_percentage = 0

    total_svpt = player_df['svpt'].sum()

    total_first_serve_in = player_df['1stIn'].sum()

    print(total_first_serve_in)

    # Calculate % of first serves that went in
    if total_svpt != 0:
        first_serve_in = round(total_first_serve_in/total_svpt * 100, 2)
    else:
        first_serve_in = 0
        
    first_serve_won = player_df['1stWon'].sum()
    print(first_serve_won)
    # Calculate % points won when first serve is in

    if total_first_serve_in != 0:
        first_serve_win_percent = round(first_serve_won/total_first_serve_in * 100, 2)
    else:
        first_serve_win_percent = 0 

    num_second_serves = total_svpt - total_first_serve_in

    second_serve_won = total_svpt = player_df['2ndWon'].sum()

    if num_second_serves != 0:
        second_serve_win_percent = round(second_serve_won/num_second_serves * 100, 2)
    else:
        second_serve_win_percent = 0 

    

    # Create dictionary with individual stats
    player_stats = {
        'Player': player_name,
        'Matches Played': total_matches,
        'Win Percentage': win_percentage,
        'First Serve In Percentage' : first_serve_in,
        'First Serve Win Percentage' : first_serve_win_percent,
        'Second Serve Win Percentage' : second_serve_win_percent
    }

    # Convert dictionary into DataFrame
    player_stats_df = pd.DataFrame(player_stats, index=[0])

    return player_stats_df

print(calculate_player_stats(matches_df, 'Cori Gauff'))

