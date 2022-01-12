import sqlite3 as sql
from os.path import dirname, join
from bokeh.palettes import Plasma256 as palette
import numpy as np
import pandas as pd

from bokeh.io import curdoc
from bokeh.layouts import column, row
from bokeh.models import ColumnDataSource, Div, Select, Slider, TextInput
from bokeh.plotting import figure
from bokeh.sampledata.movies_data import movie_path
import os
from bokeh.transform import linear_cmap, jitter

nba_player = pd.read_csv('nbaplayerstats.csv')


teams = nba_player['Team'].drop_duplicates()
teams = teams.tolist()
colormap = {'SAS': 'grey',
            'SDC': 'pink',
            'UTA': 'mediumpurple',
            'PHI':'blue',
            'HOU':'tomato',
            'LAL':'yellow',
            'DEN':'deepskyblue',
            'WAS':'orangered',
            'KCK':'indigo',
            'CLE':'black',
            'SEA':'forestgreen',
            'PHX':'orange',
            'NYK':'darkblue',
            'MIL':'darkgreen',
            'BOS':'limegreen',
            'NJN':'black',
            'CHI':'red',
            'POR':'lightslategray',
            'ATL':'salmon',
            'IND': 'khaki',
            'GSW': 'gold',
            'DET': 'royalblue',
            'DAL':'cornflowerblue',
            'LAC':'pink',
            'SAC':'indigo',
            'CHA':'darkturquoise',
            'MIA':'darkred',
            'MIN':'steelblue',
            'ORL':'mediumblue',
            'TOR':'mediumvioletred',
            'VAN':'teal',
            'MEM':'teal',
            'NOP':'saddlebrown',
            'OKC':'coral',
            'BRK':'black'
            
           }
colors = [colormap[x] for x in nba_player['Team']]
teams.append('ALL')
nba_player['color']= colors

desc = Div(text=open(join(os.getcwd(), "description.html")).read(), sizing_mode="stretch_width")

axis_map = {
    "Offensive Rebounds": "ORB",
    "Defensive Rebounds": "DRB",
    "Rebound per game": "RPG",
    "Assist per game": "APG",
    "Steal per game": "SPG",
    "Blocks per game": "BPG",
    "Turnovers per game":"TOV",
    "Points per game":"PPG",
    "Minutes per game ":"MPG"
}

#Chart tools
games_played = Slider(title = "Lower number of games played", value = 50, start = 0, end = 82, step = 1)
x_axis = Select(title="X Axis", options=sorted(axis_map.keys()), value="Points per game")
y_axis = Select(title="Y Axis", options=sorted(axis_map.keys()), value="Turnovers per game")
min_year = Slider(title="Min Year", start=1980, end=2020, value=1990, step=1)
max_year=Slider(title="Max Year", start=1981, end=2021, value=2013, step=1)

player = TextInput(title="Nba Player")
team = Select(title="Team", value="ALL",
               options=teams)

#Pointer tooltips
TOOLTIPS=[
    ("Player Name", "@player"),
    ("Year", "@year"),
    ("Team", "@team")
]

source = ColumnDataSource(data=dict(x=[], y=[], team=[], player=[], year=[], color=[]))
p = figure(height=800, width=1200, title="", toolbar_location=None, tooltips=TOOLTIPS, sizing_mode="scale_both")

p.circle(x="x", y="y", source=source, size=7, color='color', line_color=None, fill_alpha="alpha")

controls = [min_year, max_year,games_played,player,team, x_axis, y_axis]


def select_player():
    team_value = team.value
    player_value = player.value
    selected = nba_player[
        (nba_player.Year >= min_year.value) &
        (nba_player.Year <= max_year.value) &
        (nba_player.GP >= games_played.value)]
    
    if team_value != "ALL":
        selected = selected[selected.Team.str.contains(team_value)==True]
    if player_value != "":
        selected = selected[selected.Player.str.contains(player_value)==True]

    return selected

def update():
    df = select_player()
    x_name = axis_map[x_axis.value]
    y_name = axis_map[y_axis.value]

    p.xaxis.axis_label = x_axis.value
    p.yaxis.axis_label = y_axis.value
    p.title.text = "%d Nba Player statistics" % len(df)
    source.data = dict(
        x=df[x_name],
        y=df[y_name],
        team=df["Team"],
        player=df["Player"],
        year=df["Year"],
        color = df['color']
    )

for control in controls:
    control.on_change('value', lambda attr, old, new: update())

inputs = column(*controls, width=320)

l = column(desc, row(inputs, p), sizing_mode="fixed")

update()  # initial load of the data

curdoc().add_root(l)
curdoc().title = "Nba Player"

