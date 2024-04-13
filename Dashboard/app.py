from pathlib import Path

import pandas as pd
import numpy as np

import plotly.graph_objects as go
from shiny import render, reactive, req
from shiny.express import input, ui
from shinywidgets import render_plotly
from shinyswatch import theme

# Load data
app_dir = Path(__file__).parent

matches_df = pd.read_csv(app_dir / "wta_proj_matches_2023.csv", dtype={"person_id": str})

@reactive.calc
def filtered_data():
    # The required function req() is used to ensure that
    # the input.selected_surface function is not empty.
    req(input.selected_surface())

    # If empty, req() will stop the execution and
    # we'll just wait until the associated input changes to not empty.
    # If not empty, we'll continue and filter the data.
    #isSurfaceMatch = df["surface"].isin(input.selected_surface())
    
    data_filter = (df['name'].isin(input.players())) & (df['surface'].isin(input.selected_surface()))
    filtered_data = df[data_filter]

    filtered_df = pd.DataFrame(filtered_data)

    return filtered_df

@reactive.calc
def player_calcs():
    # Ensure that inputs from user are not empty is not empty
    req(input.players())
    req(input.selected_surface()
       )
    # Initialize an empty list to store player names and win percentages
    player_data = []

    # Iterate over each selected player
    for player in input.players():
        # Filter the data based on the selected player and surface
        player_filter = (df['name'] == player) & (df['surface'].isin(input.selected_surface()))
        filtered_data = df[player_filter]

        # Calculate total wins and losses for the selected player
        total_wins = filtered_data['w/l'].eq('W').sum()
        total_losses = filtered_data['w/l'].eq('L').sum()

        # Compute win percentage
        if total_wins + total_losses > 0:
            win_percentage = round(total_wins / (total_wins + total_losses) * 100, 2)
        else:
            win_percentage = 0

        total_svpt = filtered_data['svpt'].sum()

        total_first_serve_in = filtered_data['1stIn'].sum()

        # Calculate % of first serves that went in
        if total_svpt != 0:
            first_serve_in = round(total_first_serve_in/total_svpt * 100, 2)
        else:
            first_serve_in = 0
            
        first_serve_won = filtered_data['1stWon'].sum()

        # Calculate % points won when first serve is in

        if total_first_serve_in != 0:
            first_serve_win_percent = round(first_serve_won/total_first_serve_in * 100, 2)
        else:
            first_serve_win_percent = 0 

        num_second_serves = total_svpt - total_first_serve_in

        second_serve_won = total_svpt = filtered_data['2ndWon'].sum()

        if num_second_serves != 0:
            second_serve_win_percent = round(second_serve_won/num_second_serves * 100, 2)
        else:
            second_serve_win_percent = 0 

        # Append player name and win percentage to the list
        player_data.append({'Player': player, 'Win Percentage': win_percentage, 'First Serve In %' : first_serve_in, 'First Serve Win %' : first_serve_win_percent, 'Second Serve Win %' : second_serve_win_percent})

    # Create a DataFrame from the list of player data
    player_df = pd.DataFrame(player_data)

    return player_df
    
# Create DataFrame
df = pd.DataFrame(matches_df)

ui.page_opts(title="SMiller's Reactive Analysis of 2023 WTA Statistics", fillable=True)

theme.cerulean()

unique_names = df['name'].drop_duplicates().tolist()

def radar_chart(df):
    
    stats = ['Win Percentage', 'First Serve In %', 'First Serve Win %', 'Second Serve Win %']
    fig = go.Figure()  

    for index, row in df.iterrows():
        r = row[stats].values.tolist() + [row[stats[0]]]  # Close the loop
        
        fig.add_trace(go.Scatterpolar(
            r=r,
            theta=stats + [stats[0]],  # Close the loop
            fill='none',
            name=row['Player']
        ))

    # Layout configuration
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]  # Adjust as needed
            )
        ),
        showlegend=True
    )

    return fig

with ui.sidebar():

    ui.h2("Select Filters")

    ui.input_selectize(
        "players",
        "Search for players",
        multiple=True,
        choices=unique_names,
        selected=["Cori Gauff"],
        width="100%",
    )
    
    ui.input_checkbox_group(
        "selected_surface",
        "Surface",
        ["Hard", "Clay", "Grass"],
        selected=["Hard", "Clay"],
        inline=True,
    )

with ui.layout_columns():
    with ui.accordion():   

        with ui.accordion_panel("Player Statistics"):
            @render.data_frame
            def win_perc_df(height = '100px'):
                return render.DataTable(player_calcs())
        
        with ui.accordion_panel("All Player Data - Displayed by Individual Matches"):
            @render.data_frame
            def tennis_df():
                return render.DataTable(filtered_data())

    @render_plotly
    def tennis_plot():
        return radar_chart(player_calcs())

            
  
