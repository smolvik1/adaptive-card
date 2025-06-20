import json
import pandas as pd
from typing import List

field_data = [
    {
        "field": "Yggdrasil",
        "webhook_url": "https://example.com/webhook",
        "card_timestamp": "",
    }
]

event_data = [
    {
        "name": "Workflow 1",
        "type": "workflow",
        "status": "good",
        "text": "Yolo!",
        "source": "Workflow 1",
        "url": "",
    },
    {
        "name": "Field A",
        "type": "field",
        "status": "warning",
        "text": "This is not good!",
        "url": "http://www.vg.no",
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
    {
        "name": "A-03",
        "type": "pipe",
        "status": "good",
        "text": "This is good!",
        "source": "SQC",
        "url": "",
    },
]

field_df = pd.DataFrame(field_data)
event_df = pd.DataFrame(event_data)


criticality_map = {
    "Info": "good",
    "Warning": "warning",
    "Critical": "bad",
}


def fill_missing_values(
    df: pd.DataFrame, columns_to_fill: List, default_value: str = "Missing Data"
) -> pd.DataFrame:
    """Fill missing values in specified columns of a DataFrame with a default value."""
    df[columns_to_fill] = df[columns_to_fill].fillna(default_value)


# Heading Section
def generate_heading(
    field: str, card_timestamp: str, col_width: List[int] = [20, 80]
) -> List[dict]:
    return [
        {
            "type": "ColumnSet",
            "columns": [
                {
                    "type": "Column",
                    "width": col_width[0],
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
                    "width": col_width[1],
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
def generate_section_wo_url(
    event_df: pd.DataFrame, type: str, title: str, col_width: List[int] = [20, 80]
):
    items = event_df[event_df["type"].str.lower() == type.lower()]
    if items.empty:
        return []

    rows = []
    for _, row in items.iterrows():
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
            "text": title,
            "wrap": True,
            "style": "heading",
            "weight": "Bolder",
            "size": "Large",
        },
        {
            "type": "Table",
            "columns": [{"width": col_width[0]}, {"width": col_width[1]}],
            "rows": rows,
            "roundedCorners": True,
            "separator": True,
        },
    ]


# Wells Section
def generate_section_w_url(
    event_df: pd.DataFrame, type: str, title: str, col_width: List[int] = [20, 60, 20]
):
    items = event_df[event_df["type"].str.lower() == type.lower()]
    if items.empty:
        return []

    rows = []
    for _, row in items.iterrows():
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
                # "style": row["status"],
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
                                "isEnabled": (
                                    True
                                    if pd.notna(row["url"])
                                    and str(row["url"]).strip() not in ["", "0"]
                                    else False
                                ),
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
            "text": title,
            "wrap": True,
            "style": "heading",
            "weight": "Bolder",
            "size": "Large",
        },
        {
            "type": "Table",
            "columns": [
                {"width": col_width[0]},
                {"width": col_width[1]},
                {"width": col_width[2]},
            ],
            "rows": rows,
            "separator": True,
            "gridStyle": "default",
            "roundedCorners": True,
            "verticalCellContentAlignment": "Center",
            "horizontalCellContentAlignment": "Left",
        },
    ]


# Combine all parts
def generate_card(event_df: pd.DataFrame, field_df: pd.DataFrame) -> dict:
    fill_missing_values(event_df, ["name", "type", "status", "text"])
    fill_missing_values(field_df, ["field", "webhook_url"])

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
    card["body"].extend(generate_heading(field, card_timestamp, col_width=[20, 80]))
    card["body"].extend(
        generate_section_wo_url(
            event_df, type="field", title="Field", col_width=[20, 80]
        )
    )
    card["body"].extend(
        generate_section_wo_url(
            event_df, type="workflow", title="Workflow", col_width=[20, 80]
        )
    )
    card["body"].extend(
        generate_section_w_url(
            event_df, type="well", title="Well", col_width=[20, 65, 15]
        )
    )
    card["body"].extend(
        generate_section_wo_url(event_df, type="pipe", title="Pipe", col_width=[20, 80])
    )
    return card


def generate_card_str(event_df: pd.DataFrame, field_df: pd.DataFrame) -> str:
    card = generate_card(event_df=event_df, field_df=field_df)

    return json.dumps(card)


# Export to JSON
if __name__ == "__main__":
    card = generate_card(event_df=event_df, field_df=field_df)
    card_str = generate_card_str(event_df=event_df, field_df=field_df)

    with open("adaptive_card.json", "w") as f:
        f.write(json.dumps(card, indent=4))
