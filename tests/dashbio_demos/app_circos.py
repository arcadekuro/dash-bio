from textwrap import dedent
import base64
import io
import pandas as pd
import json
import os

import dash_bio
from dash_bio.utils import circos_parser as cp
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
import dash_html_components as html
import dash_table as dt

# running directly with Python
if __name__ == '__main__':
    from utils.app_standalone import run_standalone_app

# running with gunicorn (on servers)
elif 'DASH_PATH_ROUTING' in os.environ:
    from tests.dashbio_demos.utils.app_standalone import run_standalone_app


DATAPATH = os.path.join(".", "tests", "dashbio_demos", "sample_data", "circos_")
# Main dataset used for all graphs
with open("{}graph_data.json".format(DATAPATH), "r") \
        as circos_graph_data:
    circos_graph_data = json.load(circos_graph_data)

# Parsed data using circosParser for parsed_dataset graph
parsed_layout = cp.txt_to_layout(
    file_one_name="{}GRCh37.txt".format(DATAPATH),
    file_two_name="{}GRCh38.txt".format(DATAPATH),
    append_one="-GRCh37",
    append_two="-GRCh38",
    rel_path=True,
    create_local=False,
)

parsed_track_one = cp.txt_to_track(
    file_name="{}GRCh37.txt".format(DATAPATH),
    append_block_id="-GRCh37",
    rel_path=True,
    create_local=False,
)

parsed_track_two = cp.txt_to_track(
    file_name="{}GRCh38.txt".format(DATAPATH),
    append_block_id="-GRCh38",
    rel_path=True,
    create_local=False,
)


def get_circos_graph(
        key,
        size,
        data=[None, None, None]
):

    circos_graphs = {
        'upload-custom-dataset': dash_bio.Circos(
                    id="main-circos",
                    selectEvent={"0": "both", "1": "both"},
                    layout=data[0],
                    config={
                        "innerRadius": size / 2 - 80,
                        "outerRadius": size / 2 - 40,
                        "ticks": {"display": False, "labelDenominator": 1000000},
                        "labels": {
                            "position": "center",
                            "display": False,
                            "size": 12,
                            "color": "#fff",
                            "radialOffset": 70,
                        },
                    },
                    tracks=[
                        {
                            "type": "HIGHLIGHT",
                            "data": data[1],
                            "config": {
                                "innerRadius": size / 2 - 80,
                                "outerRadius": size / 2 - 40,
                                "opacity": 0.3,
                                "tooltipContent": {"name": "all"},
                                "color": {"name": "color"},
                            },
                        },
                        {
                            "type": "HIGHLIGHT",
                            "data": data[2],
                            "config": {
                                "innerRadius": size / 2 - 80,
                                "outerRadius": size / 2 - 40,
                                "opacity": 0.3,
                                "tooltipContent": {"name": "all"},
                                "color": {"name": "color"},
                            },
                        },
                    ],
                    size=800,
                ),

        'select-dataset-parser': dash_bio.Circos(
                id="main-circos",
                selectEvent={"0": "hover", "1": "click"},
                layout=parsed_layout,
                config={
                    "innerRadius": size / 2 - 80,
                    "outerRadius": size / 2 - 40,
                    "ticks": {"display": False, "labelDenominator": 1000000},
                    "labels": {
                        "position": "center",
                        "display": False,
                        "size": 8,
                        "color": "#fff",
                        "radialOffset": 90,
                    },
                },
                tracks=[
                    {
                        "type": "HIGHLIGHT",
                        "data": parsed_track_one,
                        "config": {
                            "innerRadius": size / 2 - 80,
                            "outerRadius": size / 2 - 40,
                            "opacity": 0.3,
                            "tooltipContent": {"name": "block_id"},
                            "color": {"name": "color"},
                        },
                    },
                    {
                        "type": "HIGHLIGHT",
                        "data": parsed_track_two,
                        "config": {
                            "innerRadius": size / 2 - 80,
                            "outerRadius": size / 2 - 40,
                            "opacity": 0.3,
                            "tooltipContent": {"name": "block_id"},
                            "color": {"name": "color"},
                        },
                    },
                ],
                size=800,
            ),

        'select-dataset-heatmap': dash_bio.Circos(
                id="main-circos",
                selectEvent={"0": "hover", "1": "hover"},
                layout=circos_graph_data["month_layout"],
                config={
                    "innerRadius": (size / 2 - 80),
                    "outerRadius": (size / 2 - 30),
                    "ticks": {"display": False},
                    "labels": {
                        "position": "center",
                        "display": True,
                        "size": 14,
                        "color": "#fff",
                        "radialOffset": 15,
                    },
                },
                tracks=[
                    {
                        "type": "HEATMAP",
                        "data": circos_graph_data["heatmap"],
                        "config": {
                            "innerRadius": 0.8,
                            "outerRadius": 0.98,
                            "logScale": False,
                            "color": "YlOrRd",
                            "tooltipContent": {"name": "value"},
                        },
                    },
                    {
                        "type": "HEATMAP",
                        "data": circos_graph_data["heatmap"],
                        "config": {
                            "innerRadius": 0.7,
                            "outerRadius": 0.79,
                            "logScale": False,
                            "color": "Blues",
                            "tooltipContent": {"name": "value"},
                        },
                    },
                ],
                size=800
            ),

        'select-dataset-chords': dash_bio.Circos(
                id="main-circos",
                selectEvent={"0": "both", "1": "both"},
                layout=circos_graph_data["GRCh37"],
                config={
                    "innerRadius": size / 2 - 80,
                    "outerRadius": size / 2 - 40,
                    "ticks": {"display": False, "labelDenominator": 1000000},
                    "labels": {
                        "position": "center",
                        "display": True,
                        "size": 11,
                        "color": "#fff",
                        "radialOffset": 75,
                    },
                },
                tracks=[
                    {
                        "type": "HIGHLIGHT",
                        "data": circos_graph_data["cytobands"],
                        "config": {
                            "innerRadius": size / 2 - 80,
                            "outerRadius": size / 2 - 40,
                            "opacity": 0.3,
                            "tooltipContent": {"name": "all"},
                            "color": {"name": "color"},
                        },
                    },
                    {
                        "type": "CHORDS",
                        "data": circos_graph_data["chords"],
                        "config": {
                            "logScale": False,
                            "opacity": 0.7,
                            "color": {"name": "color"},
                            "tooltipContent": {
                                "source": "source",
                                "sourceID": "id",
                                "target": "target",
                                "targetID": "id",
                                "targetEnd": "end",
                            },
                        },
                    },
                ],
                size=800,
            ),

        'select-dataset-highlight': dash_bio.Circos(
                id="main-circos",
                selectEvent={"0": "hover"},
                layout=circos_graph_data["GRCh37"],
                config={
                    "innerRadius": size / 2 - 100,
                    "outerRadius": size / 2 - 50,
                    "ticks": {"display": False},
                    "labels": {"display": False},
                },
                tracks=[
                    {
                        "type": "HIGHLIGHT",
                        "data": circos_graph_data["cytobands"],
                        "config": {
                            "innerRadius": size / 2 - 100,
                            "outerRadius": size / 2 - 50,
                            "opacity": 0.5,
                            "tooltipContent": {"name": "name"},
                            "color": {"name": "color"},
                        },
                    }
                ],
                size=800,
            ),

        'select-dataset-histogram': dash_bio.Circos(
                id="main-circos",
                layout=circos_graph_data["GRCh37"],
                selectEvent={"0": "hover", "1": "hover"},
                config={
                    "innerRadius": size / 2 - 150,
                    "outerRadius": size / 2 - 120,
                    "ticks": {"display": False, "labelDenominator": 1000000},
                    "labels": {"display": False},
                },
                tracks=[
                    {
                        "type": "HIGHLIGHT",
                        "data": circos_graph_data["cytobands"],
                        "config": {
                            "innerRadius": size / 2 - 150,
                            "outerRadius": size / 2 - 120,
                            "opacity": 0.6,
                            "tooltipContent": {"name": "name"},
                            "color": {"name": "color"},
                        },
                    },
                    {
                        "type": "HISTOGRAM",
                        "data": circos_graph_data["histogram"],
                        "config": {
                            "innerRadius": 1.01,
                            "outerRadius": 1.4,
                            "color": "OrRd",
                            "tooltipContent": {"name": "value"},
                        },
                    },
                ],
                size=800,
            ),

        'select-dataset-line': dash_bio.Circos(
                id="main-circos",
                selectEvent={
                    "0": "both",
                    "1": "both",
                    "2": "both",
                    "3": "both",
                    "4": "both",
                    "5": "both",
                    "6": "both",
                    "7": "both",
                },
                layout=list(
                    filter(
                        lambda d: d["id"] in ["chr1", "chr2", "chr3"],
                        circos_graph_data["GRCh37"],
                    )
                ),
                config={
                    "innerRadius": size / 2 - 150,
                    "outerRadius": size / 2 - 130,
                    "ticks": {"display": False, "spacing": 1000000, "labelSuffix": ""},
                    "labels": {
                        "position": "center",
                        "display": False,
                        "size": 14,
                        "color": "#fff",
                        "radialOffset": 30,
                    },
                },
                tracks=[
                    {
                        "type": "HIGHLIGHT",
                        "data": list(
                            filter(
                                lambda d: d["block_id"] in [
                                    "chr1", "chr2", "chr3"],
                                circos_graph_data["cytobands"],
                            )
                        ),
                        "config": {
                            "innerRadius": size / 2 - 150,
                            "outerRadius": size / 2 - 130,
                            "opacity": 0.3,
                            "tooltipContent": {"name": "name"},
                            "color": {"name": "color"},
                        },
                    },
                    {
                        "type": "LINE",
                        "data": circos_graph_data["snp250"],
                        "config": {
                            "innerRadius": 0.5,
                            "outerRadius": 0.8,
                            "color": "#222222",
                            "tooltipContent": {
                                "source": "block_id",
                                "target": "position",
                                "targetEnd": "value",
                            },
                            "axes": [
                                {
                                    "spacing": 0.001,
                                    "thickness": 1,
                                    "color": "#666666"
                                }
                            ],
                            "backgrounds": [
                                {
                                    "start": 0,
                                    "end": 0.002,
                                    "color": "#f44336",
                                    "opacity": 0.5,
                                },
                                {
                                    "start": 0.006,
                                    "end": 0.015,
                                    "color": "#4caf50",
                                    "opacity": 0.5,
                                },
                            ],
                            "maxGap": 1000000,
                            "min": 0,
                            "max": 0.015,
                        },
                    },
                    {
                        "type": "SCATTER",
                        "data": circos_graph_data["snp250"],
                        "config": {
                            "innerRadius": 0.5,
                            "outerRadius": 0.8,
                            "min": 0,
                            "max": 0.015,
                            "fill": False,
                            "strokeWidth": 0,
                            "tooltipContent": {
                                "source": "block_id",
                                "target": "position",
                                "targetEnd": "value",
                            },
                        },
                    },
                    {
                        "type": "LINE",
                        "data": circos_graph_data["snp"],
                        "config": {
                            "innerRadius": 1.01,
                            "outerRadius": 1.15,
                            "maxGap": 1000000,
                            "min": 0,
                            "max": 0.015,
                            "color": "#222222",
                            "tooltipContent": {"name": "value"},
                            "axes": [
                                {"position": 0.002, "color": "#f44336"},
                                {"position": 0.006, "color": "#4caf50"},
                            ],
                        },
                    },
                    {
                        "type": "LINE",
                        "data": circos_graph_data["snp1m"],
                        "config": {
                            "innerRadius": 1.01,
                            "outerRadius": 1.15,
                            "maxGap": 1000000,
                            "min": 0,
                            "max": 0.015,
                            "color": "#f44336",
                            "tooltipContent": {"name": "value"},
                        },
                    },
                    {
                        "type": "LINE",
                        "data": circos_graph_data["snp"],
                        "config": {
                            "innerRadius": 0.85,
                            "outerRadius": 0.95,
                            "maxGap": 1000000,
                            "direction": "in",
                            "min": 0,
                            "max": 0.015,
                            "color": "#222222",
                            "axes": [
                                {"position": 0.01, "color": "#4caf50"},
                                {"position": 0.008, "color": "#4caf50"},
                                {"position": 0.006, "color": "#4caf50"},
                                {"position": 0.002, "color": "#f44336"},
                            ],
                        },
                    },
                    {
                        "type": "LINE",
                        "data": circos_graph_data["snp1m"],
                        "config": {
                            "innerRadius": 0.85,
                            "outerRadius": 0.95,
                            "maxGap": 1000000,
                            "direction": "in",
                            "min": 0,
                            "max": 0.015,
                            "color": "#f44336",
                            "tooltipContent": {"name": "value"},
                        },
                    },
                ],
                size=800,
            ),

        'select-dataset-scatter': dash_bio.Circos(
                id="main-circos",
                selectEvent={
                    "0": "hover",
                    "1": "both",
                    "3": "both",
                    "4": "both",
                    "5": "both",
                },
                layout=list(
                    filter(
                        lambda d: d["id"] in ["chr1", "chr2", "chr3"],
                        circos_graph_data["GRCh37"],
                    )
                ),
                config={
                    "innerRadius": size / 2 - 150,
                    "outerRadius": size / 2 - 130,
                    "ticks": {"display": False, "spacing": 1000000, "labelSuffix": ""},
                    "labels": {"display": False},
                },
                tracks=[
                    {
                        "type": "HIGHLIGHT",
                        "data": list(
                            filter(
                                lambda d: d["block_id"] in [
                                    "chr1", "chr2", "chr3"],
                                circos_graph_data["cytobands"],
                            )
                        ),
                        "config": {
                            "innerRadius": size / 2 - 150,
                            "outerRadius": size / 2 - 130,
                            "opacity": 0.8,
                            "tooltipContent": {"name": "name"},
                            "color": {"name": "color"},
                        },
                    },
                    {
                        "type": "SCATTER",
                        "data": list(
                            filter(
                                lambda d: float(d["value"]) > 0.007,
                                circos_graph_data["snp250"],
                            )
                        ),
                        "config": {
                            "innerRadius": 0.65,
                            "outerRadius": 0.95,
                            "color": {"colorData": "name"},
                            "tooltipContent": {
                                "source": "block_id",
                                "target": "position",
                                "targetEnd": "value",
                            },
                            "strokeColor": "grey",
                            "strokeWidth": 1,
                            "shape": "circle",
                            "size": 14,
                            "min": 0,
                            "max": 0.013,
                            "axes": [
                                {
                                    "spacing": 0.001,
                                    "start": 0.006,
                                    "thickness": 1,
                                    "color": "#4caf50",
                                    "opacity": 0.3,
                                },
                                {
                                    "spacing": 0.002,
                                    "start": 0.006,
                                    "thickness": 1,
                                    "color": "#4caf50",
                                    "opacity": 0.5,
                                },
                                {
                                    "spacing": 0.002,
                                    "start": 0.002,
                                    "end": 0.006,
                                    "thickness": 1,
                                    "color": "#666",
                                    "opacity": 0.5,
                                },
                                {
                                    "spacing": 0.001,
                                    "end": 0.002,
                                    "thickness": 1,
                                    "color": "#f44336",
                                    "opacity": 0.5,
                                },
                            ],
                            "backgrounds": [
                                {"start": 0.006, "color": "#4caf50", "opacity": 0.1},
                                {
                                    "start": 0.002,
                                    "end": 0.006,
                                    "color": "#d3d3d3",
                                    "opacity": 0.1,
                                },
                                {"end": 0.002, "color": "#f44336", "opacity": 0.1},
                            ],
                        },
                    },
                    {
                        "type": "SCATTER",
                        "data": circos_graph_data["snp250"],
                        "config": {
                            "tooltipContent": {
                                "source": "block_id",
                                "target": "position",
                                "targetEnd": "value",
                            },
                            "color": "#4caf50",
                            "strokeColor": "green",
                            "strokeWidth": 1,
                            "shape": "rectangle",
                            "size": 10,
                            "min": 0.007,
                            "max": 0.013,
                            "innerRadius": 1.075,
                            "outerRadius": 1.175,
                            "axes": [
                                {
                                    "spacing": 0.001,
                                    "thickness": 1,
                                    "color": "#4caf50",
                                    "opacity": 0.3,
                                },
                                {
                                    "spacing": 0.002,
                                    "thickness": 1,
                                    "color": "#4caf50",
                                    "opacity": 0.5,
                                },
                            ],
                            "backgrounds": [
                                {"start": 0.007, "color": "#4caf50", "opacity": 0.1},
                                {"start": 0.009, "color": "#4caf50", "opacity": 0.1},
                                {"start": 0.011, "color": "#4caf50", "opacity": 0.1},
                                {"start": 0.013, "color": "#4caf50", "opacity": 0.1},
                            ],
                        },
                    },
                    {
                        "type": "SCATTER",
                        "data": list(
                            filter(
                                lambda d: float(d["value"]) < 0.002,
                                circos_graph_data["snp250"],
                            )
                        ),
                        "config": {
                            "tooltipContent": {
                                "source": "block_id",
                                "target": "position",
                                "targetEnd": "value",
                            },
                            "color": "#f44336",
                            "strokeColor": "red",
                            "strokeWidth": 1,
                            "shape": "triangle",
                            "size": 10,
                            "min": 0,
                            "max": 0.002,
                            "innerRadius": 0.35,
                            "outerRadius": 0.60,
                            "axes": [
                                {
                                    "spacing": 0.0001,
                                    "thickness": 1,
                                    "color": "#f44336",
                                    "opacity": 0.3,
                                },
                                {
                                    "spacing": 0.0005,
                                    "thickness": 1,
                                    "color": "#f44336",
                                    "opacity": 0.5,
                                },
                            ],
                            "backgrounds": [
                                {"end": 0.0004, "color": "#f44336", "opacity": 0.1},
                                {"end": 0.0008, "color": "#f44336", "opacity": 0.1},
                                {"end": 0.0012, "color": "#f44336", "opacity": 0.1},
                                {"end": 0.0016, "color": "#f44336", "opacity": 0.1},
                                {"end": 0.002, "color": "#f44336", "opacity": 0.1},
                            ],
                        },
                    },
                    {
                        "type": "SCATTER",
                        "data": circos_graph_data["snp250"],
                        "config": {
                            "tooltipContent": {
                                "source": "block_id",
                                "target": "position",
                                "targetEnd": "value",
                            },
                            "innerRadius": 0.65,
                            "outerRadius": 0.95,
                            "strokeColor": "grey",
                            "strokeWidth": 1,
                            "shape": "circle",
                            "size": 14,
                            "min": 0,
                            "max": 0.013,
                            "axes": [
                                {
                                    "spacing": 0.001,
                                    "start": 0.006,
                                    "thickness": 1,
                                    "color": "#4caf50",
                                    "opacity": 0.3,
                                },
                                {
                                    "spacing": 0.002,
                                    "start": 0.006,
                                    "thickness": 1,
                                    "color": "#4caf50",
                                    "opacity": 0.5,
                                },
                                {
                                    "spacing": 0.002,
                                    "start": 0.002,
                                    "end": 0.006,
                                    "thickness": 1,
                                    "color": "#666",
                                    "opacity": 0.5,
                                },
                                {
                                    "spacing": 0.001,
                                    "end": "0.002",
                                    "thickness": 1,
                                    "color": "#f44336",
                                    "opacity": 0.5,
                                },
                            ],
                            "backgrounds": [
                                {"start": 0.006, "color": "#4caf50", "opacity": 0.1},
                                {
                                    "start": 0.002,
                                    "end": 0.006,
                                    "color": "#d3d3d3",
                                    "opacity": 0.1,
                                },
                                {"end": 0.002, "color": "#f44336", "opacity": 0.1},
                            ],
                        },
                    },
                ],
                size=800,
            ),

        'select-dataset-stack': dash_bio.Circos(
                id="main-circos",
                selectEvent={"0": "hover"},
                layout=[
                    {
                        "id": "chr9",
                        "len": 8000000,
                        "label": "chr9",
                        "color": "#FFCC00"
                    }
                ],
                config={
                    "innerRadius": size / 2 - 50,
                    "outerRadius": size / 2 - 30,
                    "ticks": {"display": False, "labels": False, "spacing": 10000},
                    "labels": {"display": False, "labels": False, "spacing": 10000},
                },
                tracks=[
                    {
                        "type": "STACK",
                        "data": circos_graph_data["stack"],
                        "config": {
                            "innerRadius": 0.7,
                            "outerRadius": 1,
                            "thickness": 4,
                            "margin": 0.01 * 8000000,
                            "direction": "out",
                            "strokeWidth": 0,
                            "opacity": 0.5,
                            "tooltipContent": {"name": "chr"},
                            "color": {
                                "conditional": {
                                    "end": "end",
                                    "start": "start",
                                    "value": [150000, 120000, 90000, 60000, 30000],
                                    "color": [
                                        "red",
                                        "black",
                                        "#fff",
                                        "#999",
                                        "#BBB",
                                    ],
                                }
                            },
                        },
                    }
                ],
                size=800,
            ),

        'select-dataset-text': dash_bio.Circos(
                id="main-circos",
                selectEvent={"0": "hover", "1": "both"},
                layout=[circos_graph_data["GRCh37"][0]],
                config={
                    "innerRadius": size / 2 - 100,
                    "outerRadius": size / 2 - 80,
                    "labels": {"display": False},
                    "ticks": {"display": False},
                },
                tracks=[
                    {
                        "type": "HIGHLIGHT",
                        "data": list(
                            filter(
                                lambda d: d["block_id"] == circos_graph_data["GRCh37"][0]["id"],
                                circos_graph_data["cytobands"],
                            )
                        ),
                        "config": {
                            "innerRadius": size / 2 - 100,
                            "outerRadius": size / 2 - 80,
                            "opacity": 0.7,
                            "tooltipContent": {"name": "name"},
                            "color": {"name": "color"},
                        },
                    },
                    {
                        "type": "TEXT",
                        "data": list(
                            map(
                                lambda d: {
                                    "position": (d["start"] + d["end"]) / 2,
                                    "value": d["name"],
                                    "block_id": d["block_id"],
                                },
                                filter(
                                    lambda d: d["block_id"] ==
                                    circos_graph_data["GRCh37"][0]["id"],
                                    circos_graph_data["cytobands"],
                                ),
                            )
                        ),
                        "config": {
                            "innerRadius": 1.02,
                            "outerRadius": 1.3,
                            "style": {"font-size": 12},
                        },
                    },
                ],
                size=800,
            )
    }

    return circos_graphs[key]


# Description for gallery
def description():
    return "Vizualize and analyze similarities and differences between " \
           "genes in a single plot, using the powerful Circos graph."


# Dash table call back dat
def update_dash_table(data_selector, a_layout, tracks, orientation):
    answer = None
    try:
        if data_selector == "layout":
            df = pd.DataFrame(a_layout)
        elif tracks[data_selector]["type"] == "CHORDS":
            new_chords = [
                {
                    "{}_{}".format(k, a): b
                    for k, v in d.items()
                    for a, b in v.items()
                }
                for d in tracks[data_selector]["data"]
            ]
            df = pd.DataFrame(new_chords)
        else:
            df = pd.DataFrame(tracks[data_selector]["data"])
        if orientation == "column":
            answer = [{"id": i, "name": i} for i in df.columns]
        elif orientation == "row":
            answer = df.to_dict("records")
    except Exception:
        answer = pd.DataFrame()
    return answer


# Content parser used for dcc.Upload
def parse_contents(contents, filename, _):
    _, content_string = contents.split(",")

    decoded = base64.b64decode(content_string).decode("UTF-8")
    answer = None
    try:
        if "csv" in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(io.StringIO(decoded))
            df = df.to_dict(orient="records")
            answer = df
    except Exception as e:
        answer = html.Div(["There was an error processing this file."])
        print(e)
    return answer


# Header colors
def header_colors():
    return {"bg_color": "#262B3D", "font_color": "#FFF", "light_logo": True}


# Circos explanation blurb
def circos_explain():
    return dcc.Markdown(
        dedent(
            """
    A Circos graph consists of two main parts: the layout and the tracks.
    The layout sets the basic parameters of the
    graph such as radius, ticks, labels, etc. The tracks are graph layouts
    that take in a series of data points and can be one of:  heatmaps,
    chords, highlights, histograms, line, scatter, stack and text graphs.
    Tracks can be placed on and around the layout graph.

    Reference : [Seminal paper](
    http://www.doi.org/10.1101/gr.092759.109)

    For a look into Circos and the API please go here:
    [https://github.com/nicgirault/circosJS](
     https://github.com/nicgirault/circosJS)
    """
        )
    )


# Empty Circos needed for circos graph callback
empty = dash_bio.Circos(
    id="main-circos",
    selectEvent={},
    layout=[],
    size=800,
    config={},
    tracks=[],
    enableZoomPan=True,
    enableDownloadSVG=True
)

# Upload text blurb
upload_instructions = (
    "1. Select your dataset or (press download for sample data). \n"
    + "2. Drag and drop .CSV for each dataset dropdown (layout -> layout.csv, etc) \n"
    + "3. Press Render! \n"
    + "4. Go to 'View Dataset' tab to view data in table."
)


def layout():
    return html.Div(id='circos-body', children=[
        html.Div(
            id="circos-hold",
            children=[empty]
        ),

        html.Div(id='circos-control-tabs', children=[
            dcc.Tabs(id='circos-tabs', value='data', children=[
                dcc.Tab(
                    label='About',
                    value='what-is',
                    children=html.Div(className='circos-tab', children=[
                        html.H4("What is Circos?"),
                        circos_explain(),
                    ])
                ),
                dcc.Tab(
                    label='Data',
                    value='data',
                    children=html.Div(className='circos-tab', children=[
                        html.Div(className='circos-option-name', children='Data source'),
                        dcc.Dropdown(
                            id='circos-preloaded-uploaded',
                            options=[
                                {'label': 'Preloaded', 'value': 'preloaded'},
                                {'label': 'Upload', 'value': 'upload'}
                            ],
                            value='preloaded'
                        ),
                        html.Hr(),
                        html.Div(className='circos-option-name', children='View dataset'),
                        dcc.Dropdown(
                            id='circos-view-dataset',
                            options=[
                                {'label': 'Layout',
                                 'value': 'layout'}
                            ],
                            value='layout'
                        ),
                        html.A(
                            html.Button(
                                "Download",
                                className="circos-button-data "
                                "five columns",
                            ),
                            href="/assets/sample_data/"
                            "circos_sample_data.rar",
                            download="circos_sample_data.rar",
                        ),
                        html.Button(
                            "Render",
                            id="render-button",
                            className="circos-button-render "
                            "five columns",
                        ),

                        html.Div(id='circos-uploaded-data', children=[
                            dcc.Upload(
                                id="upload-data",
                                children=html.Div(
                                    [
                                        "Drag and Drop or "
                                        "click to import "
                                        ".CSV file here!"
                                    ]
                                ),
                                className="circos-upload-data",
                                multiple=True,
                            )

                        ])
                    ])
                ),
                dcc.Tab(
                    label='Table',
                    value='table',
                    children=html.Div(className='circos-tab', children=[
                        html.Div(id='circos-table-container', children=[dt.DataTable(
                            id="data-table",
                            row_selectable='multi',
                            sorting=True,
                            filtering=True,
                            css=[
                                {
                                    "selector":  ".dash-cell "
                                    "div.dash-cell-value",
                                    "rule":  "display: inline; "
                                    "white-space: inherit; "
                                    "overflow: auto; "
                                    "text-overflow: inherit;",
                                }
                            ],
                            style_cell={
                                "whiteSpace": "no-wrap",
                                "overflow": "hidden",
                                "textOverflow": "ellipsis",
                                "maxWidth": 100,
                                'fontWeight': 100,
                                'fontSize': '11pt',
                                'fontFamily': 'Courier New',
                                'backgroundColor': '#1F2132'
                            },
                            style_header={
                                'backgroundColor': '#1F2132',
                                'textAlign': 'center'
                            },
                            style_table={
                                "maxHeight": "400px",
                                'width': '340px',
                                'marginTop': '10px'
                            },
                            n_fixed_rows=1,
                            n_fixed_columns=1
                        )]),
                        html.Div(
                            id="expected-index"),
                    ])
                ),
                dcc.Tab(
                    label='View',
                    value='view',
                    children=html.Div(className='circos-tab', children=[
                        html.Div(className='circos-option-name', children='Graph type'),
                        dcc.Dropdown(
                            id='circos-graph-type',
                            options=[
                                {'label': graph_type.title(), 'value': graph_type}
                                for graph_type in [
                                        'heatmap',
                                        'chords',
                                        'highlight',
                                        'histogram',
                                        'line',
                                        'scatter',
                                        'stack',
                                        'text',
                                        'parser_data'
                                ]
                            ],
                            value='chords'
                        ),
                        html.Div(id='chords-text'),
                        html.Div(className='circos-option-name', children='Graph size'),
                        dcc.Slider(
                            id='circos-size',
                            min=500,
                            max=800,
                            step=10,
                            value=600
                        )

                    ]),
                )

            ])
        ]),

        html.Div(
            [
                html.Div(
                    [
                        dcc.Tabs(
                            id="circos-tabs-orig",
                            value="circos-tab-dataset",
                            children=[
                                dcc.Tab(
                                    label="Select",
                                    value="circos-tab-select",
                                    children=[
                                        html.Div(
                                            [
                                                html.Div(
                                                    [
                                                        html.H5(
                                                            "Hover/Click Data"),
                                                        dcc.Textarea(
                                                            id="event-data-select",
                                                            placeholder="Hover or click on "
                                                            "data to see it here.",
                                                            value="Hover or click on "
                                                            "data to see it here.",
                                                            className="circos-event-data",
                                                        ),
                                                    ],
                                                    className="twelve columns",
                                                )
                                            ],
                                            className="circos-row-two row",
                                        ),
                                        html.Div(
                                            [
                                                html.Div(
                                                    [
                                                    ],
                                                    className="twelve columns",
                                                )
                                            ],
                                            className="circos-row-two row",
                                        ),
                                    ],
                                ),
                                dcc.Tab(
                                    label="View Dataset",
                                    value="circos-tab-dataset",
                                    children=[

                                    ],
                                ),
                                dcc.Tab(
                                    label="Custom Graph",
                                    value="circos-tab-custom",
                                    children=[
                                        html.Div([
                                            html.Div([
                                                html.H5(
                                                    "Upload Data",
                                                    className="circos-select-data-set "
                                                    "five columns",
                                                ),
                                                html.Div([
                                                    html.Div([
                                                    ],
                                                             className="row")
                                                ],
                                                         className="six columns")
                                            ],
                                                     className="circos-row-three row"),
                                            html.Div([
                                                html.Div([
                                                    dcc.Textarea(
                                                        value=upload_instructions,
                                                        className="circos-text-area",
                                                    )
                                                ],
                                                         className="six columns"),
                                                html.Div([
                                                ],
                                                         className="six columns")
                                            ],
                                                     className="circos-row-four row"),
                                            html.Div([
                                                html.Div([
                                                    html.H5(
                                                        "Select Upload Data"
                                                    ),
                                                    dcc.Dropdown(
                                                        id="circos-view-dataset-custom",
                                                        options=[
                                                            {
                                                                "label": "Layout",
                                                                "value": 0,
                                                            },
                                                            {
                                                                "label": "Track 1",
                                                                "value": 1,
                                                            },
                                                            {
                                                                "label": "Track 2",
                                                                "value": 2,
                                                            },
                                                        ],
                                                        value=0,
                                                    ),
                                                ],
                                                         className="six columns"),
                                                html.Div([
                                                    html.H5(
                                                        "Size Slider"
                                                    ),
                                                    html.Div([
                                                        dcc.Slider(
                                                            id="size-slider-custom",
                                                            marks={
                                                                500: "Min",
                                                                800: "Max",
                                                            },
                                                            min=500,
                                                            max=800,
                                                            step=10,
                                                            value=600,
                                                        )
                                                    ],
                                                             className="circos-size-slider")
                                                ],
                                                         className="six columns")
                                            ],
                                                     className="circos-row-two row"),
                                            html.Div(
                                                [
                                                    html.H5(
                                                        "Hover/Click Data"),
                                                    dcc.Textarea(
                                                        id="event-data-custom",
                                                        placeholder="Hover or click on "
                                                        "data to see it here.",
                                                        value="",
                                                        className="circos-event-data",
                                                    ),
                                                ],
                                                className="circos-row-two twelve columns",
                                            ),
                                        ],
                                                 className="row")
                                    ],
                                ),
                            ],
                        )
                    ],
                    className="circos-column-one five columns",
                ),
            ],
            className="row",
        ),
        html.Div(
            [
                html.Div(id="output-data-upload"),
                html.Div(id="event-data-store"),
            ],
            className="circos-display-none",
        ),
    ])


def callbacks(app):  # pylint: disable=redefined-outer-name

    @app.callback(
        Output('circos-uploaded-data', 'style'),
        [Input('circos-preloaded-uploaded', 'value')]
    )
    def show_hide_uploaded(pre_up):
        return {'display': 'none' if pre_up == 'preloaded' else 'inline-block'}

    # Dynamically update circos-view-dataset drop down on graph change
    @app.callback(
        Output("circos-view-dataset", "options"),
        [Input("circos-hold", "children"),
         Input("circos-graph-type", "value"),
         Input('circos-preloaded-uploaded', 'value')],
        [State("main-circos", "tracks")]
    )
    def event_dropdown(dropdown, circos_select, pre_up, tracks):

        answer = ["blank"]

        if tracks is not None and pre_up == 'preloaded':
            array = []
            dropdown = []

            for k, v in [(k, v) for x in tracks for (k, v) in x.items()]:
                if k == "type":
                    array.append(v)

            for i in range(len(tracks)):
                dropdown.append({"label": "{}".format(array[i]), "value": i})

            dropdown.append({"label": "LAYOUT", "value": "layout"}.copy())
            answer = dropdown

        elif pre_up == 'upload':
            dropdown = [
                {"label": "LAYOUT", "value": "layout"},
                {"label": "HIGHLIGHT", "value": 0},
                {"label": "HIGHLIGHT", "value": 1},
            ]
            answer = dropdown

        return answer

    # Take in and return uploaded .CSV data
    @app.callback(
        Output("output-data-upload", "children"),
        [Input("upload-data", "contents")],
        [
            State("upload-data", "filename"),
            State("upload-data", "last_modified"),
            State("output-data-upload", "children"),
            State("circos-view-dataset-custom", "value"),
        ],
    )
    def update_output(
            list_of_contents,
            list_of_names,
            list_of_dates,
            data,
            upload_select
    ):

        answer = None

        if data is None:
            array = [None, None, None]
        else:
            array = json.loads(data)

        if list_of_contents is not None:
            children = list(
                (
                    parse_contents(c, n, d)
                    for c, n, d in zip(list_of_contents, list_of_names, list_of_dates)
                )
            )
            children = children[0]
            array[upload_select] = children
            answer = json.dumps(array)
        return answer

    # Return Circos Graph with specified layout & dataset
    @app.callback(
        Output("circos-hold", "children"),
        [Input('circos-preloaded-uploaded', 'value'),
         Input('circos-graph-type', 'value'),
         Input("circos-size", "value"),
         Input("size-slider-custom", "value"),
         Input("render-button", "n_clicks"),
         Input("data-table", "selected_rows")],
        [
            State("output-data-upload", "children"),
            State("data-table", "data"),
            State("circos-view-dataset", "value"),
        ],
    )
    def show_circos_graph(
            pre_up,
            circos_select,
            size,
            size_custom,
            render_button,
            selected_row,
            upload_data,
            table_data,
            data_selector,
    ):
        if pre_up == 'upload' and upload_data is not None:
            array = json.loads(upload_data)
            answer = get_circos_graph(
                'upload-custom-dataset',
                size_custom,
                array
            )
        elif pre_up == 'preloaded' and circos_select == 'parser_data':
            answer = get_circos_graph(
                'select-dataset-parser',
                size
            )
        elif pre_up == 'preloaded' and circos_select == 'heatmap':
            answer = get_circos_graph(
                'select-dataset-heatmap',
                size
            )
        elif pre_up == 'preloaded' and circos_select == 'chords':
            if selected_row is not None and data_selector == 1:
                for i in list(range(len(circos_graph_data["chords"]))):
                    circos_graph_data["chords"][i]["color"] = "#ff5722"
                for i in selected_row:
                    circos_graph_data["chords"][i]["color"] = "#00cc96"

            answer = get_circos_graph(
                'select-dataset-chords',
                size
            )
        elif pre_up == 'preloaded' and circos_select == 'highlight':
            answer = get_circos_graph(
                'select-dataset-highlight',
                size
            )

        elif pre_up == 'preloaded' and circos_select == 'histogram':
            answer = get_circos_graph(
                'select-dataset-histogram',
                size
            )
        elif pre_up == 'preloaded' and circos_select == 'line':
            answer = get_circos_graph(
                'select-dataset-line',
                size
            )
        elif pre_up == 'preloaded' and circos_select == 'scatter':
            answer = get_circos_graph(
                'select-dataset-scatter',
                size
            )
        elif pre_up == 'preloaded' and circos_select == 'stack':
            answer = get_circos_graph(
                'select-dataset-stack',
                size
            )
        elif pre_up == 'preloaded' and circos_select == 'text':
            answer = get_circos_graph(
                'select-dataset-text',
                size
            )
        else:
            answer = empty

        return answer

    # If chords graph selected, output text blurb to let user know of highlight feature
    @app.callback(
        Output("chords-text", "children"),
        [Input("circos-graph-type", "value")]
    )
    def update_chords_text(circos_select):
        if circos_select == "chords":
            return "Select chords and select row in dash-table to highlight chords."
        return ""

    # Return dataset to data table
    @app.callback(
        Output("data-table", "data"),
        [
            Input("circos-view-dataset", "value"),
            Input("render-button", "n_clicks"),
            Input("circos-view-dataset", "options"),
            Input("data-table", "selected_cells"),
        ],
        [
            State("main-circos", "layout"),
            State("main-circos", "tracks")
        ],
    )
    def update_table_rows(
            data_selector,
            render_button,
            circos_trigger,
            selected,
            a_layout,
            tracks
    ):
        return update_dash_table(data_selector, a_layout, tracks, "row")

    # Return dataset to columns of data table
    @app.callback(
        Output("data-table", "columns"),
        [
            Input("circos-view-dataset", "value"),
            Input("render-button", "n_clicks"),
            Input("circos-view-dataset", "options"),
            Input("data-table", "selected_cells"),
        ],
        [
            State("main-circos", "layout"),
            State("main-circos", "tracks")
        ],
    )
    def update_table_columns(
            data_selector,
            render_button,
            circos_trigger,
            selected,
            a_layout,
            tracks
    ):
        return update_dash_table(data_selector, a_layout, tracks, "column")

    # Hover/click event handler data for preset graph
    @app.callback(
        Output("event-data-select", "value"),
        [Input("main-circos", "eventDatum")]
    )
    def event_data_select(event_datum):
        return str(event_datum)

    # Hover click event handler data for custom graph
    @app.callback(
        Output("event-data-custom", "value"),
        [Input("render-button", "n_clicks"),
         Input("main-circos", "eventDatum")],
    )
    def event_data_custom(_, event_datum):
        return str(event_datum)


# only declare app/server if the file is being run directly
if 'DASH_PATH_ROUTING' in os.environ or __name__ == '__main__':
    app = run_standalone_app(layout, callbacks, header_colors, __file__)
    server = app.server

if __name__ == '__main__':
    app.run_server(debug=True, port=8050)
