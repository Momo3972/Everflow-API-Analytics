import os
import logging
from typing import Dict, List, Any, Optional
import requests
from dotenv import load_dotenv

load_dotenv()

EFLOW_API_KEY = os.getenv("EFLOW_API_KEY", "")
EFLOW_BASE_URL = os.getenv("EFLOW_BASE_URL", "https://api.eflow.team").rstrip("/")
EFLOW_TIMEZONE_ID = int(os.getenv("EFLOW_TIMEZONE_ID", "67"))
EFLOW_CURRENCY_ID = os.getenv("EFLOW_CURRENCY_ID", "USD")

HEADERS = {
    "X-Eflow-API-Key": EFLOW_API_KEY,
    "Content-Type": "application/json",
}

logger = logging.getLogger("everflow")
logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")

class EverflowError(Exception):
    pass

def _check_api_key():
    if not EFLOW_API_KEY:
        raise EverflowError("EFLOW_API_KEY manquante. Renseignez-la dans .env ou variables d'env.")

def aggregated_table(from_date: str, to_date: str, columns: List[str],
                     filters: Optional[List[Dict[str, Any]]] = None,
                     exclusions: Optional[List[Dict[str, Any]]] = None,
                     settings: Optional[Dict[str, Any]] = None,
                     timezone_id: Optional[int] = None,
                     currency_id: Optional[str] = None) -> Dict[str, Any]:
    _check_api_key()
    tz = timezone_id if timezone_id is not None else EFLOW_TIMEZONE_ID
    cur = currency_id if currency_id is not None else EFLOW_CURRENCY_ID

    url = f"{EFLOW_BASE_URL}/v1/networks/reporting/entity/table"
    payload = {
        "from": from_date,
        "to": to_date,
        "timezone_id": tz,
        "currency_id": cur,
        "columns": [{"column": c} for c in columns],
        "query": {}
    }
    if filters:
        payload["query"]["filters"] = filters
    if exclusions:
        payload["query"]["exclusions"] = exclusions
    if settings:
        payload["query"]["settings"] = settings

    resp = requests.post(url, headers=HEADERS, json=payload, timeout=60)
    if resp.status_code != 200:
        raise EverflowError(f"HTTP {resp.status_code}: {resp.text}")
    return resp.json()
