from typing import List, Dict, Any
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

def _rows_to_df(rows: List[Dict[str, Any]]) -> pd.DataFrame:
    records = []
    for r in rows:
        cols = r.get("columns", {})
        metrics = r.get("metrics", {})
        offer = cols.get("offer", {})
        affiliate = cols.get("affiliate", {})
        advertiser = cols.get("advertiser", {})
        revenue = float(metrics.get("revenue", 0))
        payout = float(metrics.get("payout", 0))
        profit = revenue - payout
        records.append({
            "offer_id": offer.get("id"),
            "offer_name": offer.get("name"),
            "affiliate_id": affiliate.get("id"),
            "affiliate_name": affiliate.get("name"),
            "advertiser_id": advertiser.get("id"),
            "advertiser_name": advertiser.get("name"),
            "revenue": revenue,
            "payout": payout,
            "profit": profit,
            "cv": metrics.get("cv", 0),
            "total_click": metrics.get("total_click", 0),
        })
    return pd.DataFrame.from_records(records)

def topn_profit_by(df: pd.DataFrame, by: str, n: int = 15) -> pd.DataFrame:
    assert by in {"offer", "affiliate", "advertiser"}
    name_col = f"{by}_name"
    id_col = f"{by}_id"
    group = df.groupby([id_col, name_col], dropna=False)["profit"].sum().reset_index()
    group = group.sort_values("profit", ascending=False).head(n)
    return group

def save_barh(df: pd.DataFrame, value_col: str, label_col: str, title: str, path: Path):
    plt.figure(figsize=(10, 6))
    df = df.sort_values(value_col, ascending=True)
    plt.barh(df[label_col].astype(str), df[value_col])
    plt.title(title)
    plt.xlabel(value_col.capitalize())
    plt.tight_layout()
    path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(path)
    plt.close()

def make_all_charts(rows: List[Dict[str, Any]], outdir: str = "out"):
    Path(outdir).mkdir(parents=True, exist_ok=True)
    df = _rows_to_df(rows)
    offers = topn_profit_by(df, "offer", n=15)
    save_barh(offers, "profit", "offer_name", "Somme des profits par offre (Top 15)", Path(outdir) / "profit_by_offer.png")
    affiliates = topn_profit_by(df, "affiliate", n=15)
    save_barh(affiliates, "profit", "affiliate_name", "Somme des profits par affilié (Top 15)", Path(outdir) / "profit_by_affiliate.png")
    advertisers = topn_profit_by(df, "advertiser", n=15)
    save_barh(advertisers, "profit", "advertiser_name", "Somme des profits par advertiser (Top 15)", Path(outdir) / "profit_by_advertiser.png")
    return {"offers": offers, "affiliates": affiliates, "advertisers": advertisers}
