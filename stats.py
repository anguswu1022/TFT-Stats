from __future__ import annotations
from riotwatcher import TftWatcher
import pandas as pd
import plotly.graph_objects as go
import numpy as np
import json


def get_placement_trend(matches: list | np.ndarray) -> np.ndarray:
    placement_trend = []
    for match in matches:
        my_match_data = match["info"]["participants"][
            match["metadata"]["participants"].index(me["puuid"])
        ]
        placement_trend.append(int(my_match_data["placement"]))

    return np.array(placement_trend, dtype=np.int32)


with open("api_key.txt", "r") as file:
    API_KEY = file.read().strip()

watcher = TftWatcher(API_KEY)
my_region = "na1"
summoner_name = "Darkserious"

me = watcher.summoner.by_name(my_region, summoner_name=summoner_name)

for key in me:
    print(key, ":", me[key])

matches_ids = watcher.match.by_puuid(my_region, me["puuid"], count=20)
matches = [watcher.match.by_id(my_region, item) for item in matches_ids]

matches[0].keys()
matches[0]["metadata"]
matches[0]["info"].keys()

my_match_data = matches[0]["info"]["participants"][
    matches[0]["metadata"]["participants"].index(me["puuid"])
]
my_match_data.keys()

my_match_data["augments"]
my_match_data["placement"]
my_match_data["units"][:2]

with open("units.json", "w") as file:
    json.dump(my_match_data["units"], file, indent=4)

placements = get_placement_trend(matches=matches)
x = np.arange(len(placements))

fig = go.Figure()

fig.add_trace(
    go.Scatter(x=x, y=placements, name="sin", mode="markers", marker_color=placements)
)

fig.update_traces(mode="markers", marker_line_width=2, marker_size=10)
fig.update_layout(title="Positioning trend", width=800)
fig.show()
