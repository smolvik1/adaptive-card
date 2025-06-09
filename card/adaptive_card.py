import json
import pandas as pd
import requests
import os
from dotenv import load_dotenv

load_dotenv()
POST_TO_TEAMS = True

field_data = [
    {
        "field": "Yggdrasil",
        "webhook_url": os.getenv("WEBHOOK_URL"),
        "card_timestamp": "",
    }
]

event_data = [
    {
        "name": "Workflow 123",
        "type": "workflow",
        "status": "good",
        "text": "This is good!",
        "source": "Workflow 1",
        "url": "",
    },
    {
        "name": "A-02",
        "type": "well",
        "status": "warning",
        "text": "This is not good!",
        "url": "http://www.vg.no",
    },
    {
        "name": "A-03",
        "type": "well",
        "status": "good",
        "text": "This is good!",
        "source": "SQC",
        "url": "",
    },
]

field_df = pd.DataFrame(field_data)
event_df = pd.DataFrame(event_data)


# Heading Section
def generate_heading(field: str, card_timestamp: str):
    return [
        {
            "type": "ColumnSet",
            "columns": [
                {
                    "type": "Column",
                    "width": 15,
                    "items": [
                        {
                            "type": "Image",
                            "altText": "Aker BP",
                            "size": "Small",
                            "url": "https://companieslogo.com/img/orig/AKRBP.OL-c65af99e.png?t=1603469381",
                            "style": "RoundedCorners",
                            "width": "50px",
                            "horizontalAlignment": "Left",
                        }
                    ],
                },
                {
                    "type": "Column",
                    "width": 50,
                    "items": [
                        {
                            "type": "TextBlock",
                            "wrap": True,
                            "size": "Large",
                            "weight": "Bolder",
                            "color": "Default",
                            "style": "heading",
                            "text": "Digital Oil Friend Status",
                        },
                        {"type": "TextBlock", "text": f"Field: {field}", "wrap": True},
                    ],
                },
            ],
        },
        {
            "type": "TextBlock",
            "text": f"{card_timestamp}",
            "wrap": True,
            "spacing": "None",
            "fontType": "Default",
            "size": "Small",
            "weight": "Default",
            "isSubtle": True,
            "color": "Default",
        },
    ]


# Workflows Section
def generate_workflows(event_df: pd.DataFrame):
    workflows = event_df[event_df["type"] == "workflow"]
    if workflows.empty:
        return []

    rows = []
    for _, row in workflows.iterrows():
        rows.append(
            {
                "type": "TableRow",
                "cells": [
                    {
                        "type": "TableCell",
                        "items": [
                            {"type": "TextBlock", "text": row["name"], "wrap": True}
                        ],
                    },
                    {
                        "type": "TableCell",
                        "style": row["status"],
                        "items": [
                            {"type": "TextBlock", "text": row["text"], "wrap": True}
                        ],
                    },
                ],
            }
        )

    return [
        {
            "type": "TextBlock",
            "text": "Workflows",
            "wrap": True,
            "style": "heading",
            "weight": "Bolder",
            "size": "Large",
        },
        {
            "type": "Table",
            "columns": [{"width": 1}, {"width": 7}],
            "rows": rows,
            "roundedCorners": True,
            "separator": True,
        },
    ]


# Wells Section
def generate_wells(event_df: pd.DataFrame):
    wells = event_df[event_df["type"] == "well"]
    if wells.empty:
        return []

    rows = []
    for _, row in wells.iterrows():
        row_cells = [
            {
                "type": "TableCell",
                "items": [{"type": "TextBlock", "text": row["name"], "wrap": True}],
            },
            {
                "type": "TableCell",
                "style": row["status"],
                "items": [{"type": "TextBlock", "text": row["text"], "wrap": True}],
            },
            {
                "type": "TableCell",
                "items": [
                    {
                        "type": "ActionSet",
                        "actions": [
                            {
                                "type": "Action.OpenUrl",
                                "iconUrl": "icon:DataTrending",
                                "title": "Plot",
                                "style": "positive",
                                "tooltip": "Plot the event in SeeQ",
                                "isEnabled": True
                                if pd.notna(row["url"])
                                and str(row["url"]).strip() != ""
                                else False,
                                "url": row["url"] or "http://",
                            }
                        ],
                        "horizontalAlignment": "Center",
                    }
                ],
            },
        ]
        rows.append({"type": "TableRow", "cells": row_cells})

    return [
        {
            "type": "TextBlock",
            "text": "Wells",
            "wrap": True,
            "style": "heading",
            "weight": "Bolder",
            "size": "Large",
        },
        {
            "type": "Table",
            "columns": [{"width": 1}, {"width": 6}, {"width": 1}],
            "rows": rows,
            "separator": True,
            "gridStyle": "default",
            "roundedCorners": True,
            "verticalCellContentAlignment": "Center",
            "horizontalCellContentAlignment": "Left",
        },
    ]


# Combine all parts
def generate_card(event_df: pd.DataFrame, field_df: pd.DataFrame) -> str:
    field = field_df.iloc[0]["field"]
    card_timestamp = field_df.iloc[0]["card_timestamp"]
    card = {
        "type": "AdaptiveCard",
        "speak": "Digital Oilfield Alerts",
        "$schema": "https://adaptivecards.io/schemas/adaptive-card.json",
        "version": "1.5",
        "msteams": {"width": "full"},
        "body": [],
    }
    card["body"].extend(generate_heading(field, card_timestamp))
    card["body"].extend(generate_workflows(event_df))
    card["body"].extend(generate_wells(event_df))

    return card

def post_card (card: dict, webhook_url: str):
    response = requests.post(url=webhook_url, json=card)
    print("Status Code:", response.status_code)
    try:
        print("Response JSON:", response.json())
    except ValueError:
        print("Response Text:", response.text)
    return response

def do_all(event_df: pd.DataFrame, field_df: pd.DataFrame):
    webhook_url = field_df.iloc[0]["webhook_url"]
    card = generate_card(event_df=event_df, field_df=field_df)
    return post_card(card=card, webhook_url=webhook_url)

# Export to JSON
if __name__ == "__main__":
    card = generate_card(event_df=event_df, field_df=field_df)
    webhook_url = field_df.iloc[0]["webhook_url"]

    if POST_TO_TEAMS and webhook_url != "":
        post_card(card=card, webhook_url=webhook_url)
    with open("adaptive_card.json", "w") as f:
        f.write(json.dumps(card, indent=4))
