from urllib.parse import urlencode
from typing import List, Optional, NewType

ISO8601 = NewType("ISO8601", str)

data = {
    "trend_items": [
        "IAA_Miros_Weather_Data_Air_THP_Data_Air_Dewpoint_Temperature_(1_min._mean)	",
        "0EFB60A8-2C2D-66F0-8A57-9BF806030811",
    ],
    "investigate_start": ISO8601("2023-10-01T00:00:00Z"),
    "investigate_end": ISO8601("2023-10-04T23:59:59Z"),
    "display_start": ISO8601("2023-10-02T00:00:00Z"),
    "display_end": ISO8601("2023-10-03T23:59:59Z"),
}


def generate_seeq_url(
    trend_items: List[str],
    investigate_start: ISO8601,
    investigate_end: ISO8601,
    display_start: Optional[ISO8601] = None,
    display_end: Optional[ISO8601] = None,
    base_url: str = "https://akerbp.seeq.site",
    workbook_name: Optional[str] = "Digital Oilfield Events",
    worksheet_name: Optional[str] = "worksheet",
):
    """Generate a Seeq URL for a specific workbook and worksheet with given parameters."""

    if not display_end:
        display_end = investigate_end
    if not display_start:
        display_start = investigate_start

    query_params = {
        "workbookName": workbook_name,
        # "worksheetName": worksheet_name,
        "trendItems": trend_items,
        "displayStartTime": display_start,
        "displayEndTime": display_end,
        "investigateStartTime": investigate_start,
        "investigateEndTime": investigate_end,
    }

    encoded_params = urlencode(query_params, doseq=True)
    full_url = f"{base_url}/workbook/builder?{encoded_params}"
    return full_url


url = generate_seeq_url(**data)
print(url)
