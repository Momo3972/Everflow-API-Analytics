import argparse
import json
from pathlib import Path
from typing import List, Dict, Any

from dotenv import load_dotenv
load_dotenv()

from everflow_client import aggregated_table, EverflowError, EFLOW_TIMEZONE_ID, EFLOW_CURRENCY_ID
from plotting import make_all_charts

def load_mock_rows(path: str) -> List[Dict[str, Any]]:
    with open(path, "r") as f:
        return json.load(f)

def write_report(from_date: str, to_date: str, outdir: str, timezone_id: int, currency_id: str):
    template = Path("REPORT.md").read_text()
    content = (template
               .replace("{{FROM}}", from_date)
               .replace("{{TO}}", to_date)
               .replace("{{TIMEZONE_ID}}", str(timezone_id))
               .replace("{{CURRENCY_ID}}", currency_id))
    Path(outdir, "REPORT.md").write_text(content, encoding="utf-8")

def main():
    parser = argparse.ArgumentParser(description="Everflow API Analytics — Génération de graphiques")
    parser.add_argument("--from", dest="from_date", required=True, help="Date de début (YYYY-MM-DD)")
    parser.add_argument("--to", dest="to_date", required=True, help="Date de fin (YYYY-MM-DD)")
    parser.add_argument("--timezone-id", type=int, default=EFLOW_TIMEZONE_ID, help="Timezone Everflow ID (ex: 67 = Europe/Paris)")
    parser.add_argument("--currency", default=EFLOW_CURRENCY_ID, help="Devise (ex: USD)")
    parser.add_argument("--out", default="out", help="Dossier de sortie pour les images et le rapport")
    parser.add_argument("--mock", action="store_true", help="Utiliser des données factices (mock) au lieu de l'API")
    parser.add_argument("--charts", nargs="+", choices=["offers", "affiliates", "advertisers"], help="Limiter aux graphiques souhaités")
    args = parser.parse_args()

    rows: List[Dict[str, Any]] = []
    if args.mock:
        rows = load_mock_rows("mock_data/sample_table_rows.json")
    else:
        columns = ["offer", "affiliate"]
        data = aggregated_table(
            from_date=args.from_date,
            to_date=args.to_date,
            columns=columns,
            timezone_id=args.timezone_id,
            currency_id=args.currency
        )
        rows = data.get("rows") or data.get("data") or data.get("result") or []
        if data.get("incomplete_results"):
            print("[!] Attention : résultats incomplets (10k lignes max). Réduisez la plage ou le nombre de colonnes.")

    if not rows:
        raise SystemExit("Aucune donnée à tracer. Vérifiez la plage de dates / permissions / mock.")

    make_all_charts(rows, outdir=args.out)

    if args.charts:
        mapping = {"offers": "profit_by_offer.png", "affiliates": "profit_by_affiliate.png", "advertisers": "profit_by_advertiser.png"}
        keep = set(mapping[c] for c in args.charts)
        for fname in ["profit_by_offer.png", "profit_by_affiliate.png", "profit_by_advertiser.png"]:
            if fname not in keep:
                try:
                    Path(args.out, fname).unlink()
                except FileNotFoundError:
                    pass

    write_report(args.from_date, args.to_date, args.out, args.timezone_id, args.currency)
    print(f"✔ Graphiques générés dans: {args.out}/")
    print("   - profit_by_offer.png")
    print("   - profit_by_affiliate.png")
    print("   - profit_by_advertiser.png")
    print("✔ Rapport: REPORT.md")

if __name__ == "__main__":
    try:
        main()
    except EverflowError as e:
        raise SystemExit(f"Erreur Everflow: {e}")
