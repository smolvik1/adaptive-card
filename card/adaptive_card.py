import json
import pandas as pd

dummy_data = [
    {
        "name": "Workflow 1",
        "type": "workflow",
        "status": "good",
        "text": "This is good!",
        "url": ""
    },
    {
        "name": "A-02",
        "type": "well",
        "status": "warning",
        "text": "This is not good!",
        "url": "http://www.vg.no"
    },
    {
        "name": "A-03",
        "type": "well",
        "status": "good",
        "text": "This is good!",
        "url": ""
    },      
    ]

df = pd.DataFrame(dummy_data)

# Heading Section
def generate_heading():
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
                            "horizontalAlignment": "Left"
                        }
                    ]
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
                            "text": "Digital Oil Friend Status"
                        },
                        {
                            "type": "TextBlock",
                            "text": "Field: Valhall",
                            "wrap": True
                        }
                    ]
                }
            ]
        },
        {
            "type": "TextBlock",
            "text": "dd.mm.yyyy hh:mm",
            "wrap": True,
            "spacing": "None",
            "fontType": "Default",
            "size": "Small",
            "weight": "Default",
            "isSubtle": True,
            "color": "Default"
        }
    ]

# Workflows Section
def generate_workflows(df):
    workflows = df[df["type"] == "workflow"]
    if workflows.empty:
        return []

    rows = []
    for _, row in workflows.iterrows():
        rows.append({
            "type": "TableRow",
            "cells": [
                {
                    "type": "TableCell",
                    "items": [{"type": "TextBlock", "text": row["name"], "wrap": True}]
                },
                {
                    "type": "TableCell",
                    "style": row["status"],
                    "items": [{"type": "TextBlock", "text": row["text"], "wrap": True}]
                }
            ]
        })

    return [
        {"type": "TextBlock", "text": "Workflows", "wrap": True, "style": "heading"},
        {
            "type": "Table",
            "columns": [{"width": 2}, {"width": 5.5}],
            "rows": rows,
            "roundedCorners": True
        }
    ]


# Wells Section
def generate_wells(df):
    wells = df[df["type"] == "well"]
    if wells.empty:
        return []

    rows = []
    for _, row in wells.iterrows():
        row_cells = [
            {
                "type": "TableCell",
                "items": [{"type": "TextBlock", "text": row["name"], "wrap": True}]
            },
            {
                "type": "TableCell",
                "style": row["status"],
                "items": [{"type": "TextBlock", "text": row["text"], "wrap": True}]
            },
            {
                "type": "TableCell",
                "items": [{
                    "type": "ActionSet",
                    "actions": [{
                        "type": "Action.OpenUrl",
                        "iconUrl": "icon:DataTrending",
                        "title": "Plot",
                        "style": "positive",
                        "tooltip": f"Plot the event for well {row["name"]} in SeeQ",
                        "isEnabled": True if pd.notna(row["url"]) and str(row["url"]).strip() != "" else False,
                        "url": row["url"] or "http://"
                    }],
                    "horizontalAlignment": "Center"
                }]
            }
        ]
        rows.append({"type": "TableRow", "cells": row_cells})

    return [
        {"type": "TextBlock", "text": "Wells", "wrap": True, "style": "heading"},
        {
            "type": "Table",
            "columns": [{"width": 2}, {"width": 4}, {"width": 1.5}],
            "rows": rows,
            "separator": True,
            "gridStyle": "default",
            "roundedCorners": True,
            "verticalCellContentAlignment": "Center",
            "horizontalCellContentAlignment": "Left"
        }
    ]

# Combine all parts
def generate_card():
    card = {
        "type": "AdaptiveCard",
        "speak": "Digital Oilfield Alerts",
        "$schema": "https://adaptivecards.io/schemas/adaptive-card.json",
        "version": "1.5",
        "body": []
    }
    card["body"].extend(generate_heading())
    card["body"].extend(generate_workflows(df))
    card["body"].extend(generate_wells(df))
    return card

# Export to JSON
if __name__ == "__main__":
    final_card = generate_card()
    with open("adaptive_card.json", "w") as f:
        json.dump(final_card, f, indent=4)
