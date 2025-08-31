import requests
from ..db import crud,database
from datetime import datetime

# --- Rainfall ---
def get_rainfall(db, district_id=1):
    url = f"hhttps://indiawris.gov.in/swagger-ui/index.html#/Data%20API%20Based%20On%20Admin%20Hierarchy/getRainF"
    response = requests.get(url)
    data = response.json()

    for entry in data.get("rainfall", []):   # Check API JSON format
        crud.save_rainfall(
            db,
            district=entry.get("district"),
            rainfall=float(entry.get("rainfall", 0)),
            date=datetime.now()
        )
    return {"status": "success", "records": len(data.get("rainfall", []))}

