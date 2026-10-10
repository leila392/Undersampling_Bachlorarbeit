"""Plot previously calculated model metrics; no training or generated data."""

import argparse
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd


METRICS = {
    "precision": "Precision",
    "recall": "Recall",
    "f1_score": "F1-Score",
    "brier_score": "Brier Score",
}


def load_results(path: Path) -> pd.DataFrame:
    results = pd.read_csv(path)
    required = ["model", *METRICS]
    missing = set(required) - set(results.columns)
    if missing:
        raise ValueError(f"Fehlende CSV-Spalten: {', '.join(sorted(missing))}")
    results = results[required].copy()
    if len(results) != 2:
        raise ValueError("Die CSV muss genau zwei Modellzeilen enthalten.")
    if results["model"].isna().any():
        raise ValueError("Modellnamen dürfen nicht fehlen.")
    results["model"] = results["model"].astype(str).str.strip()
    if results["model"].eq("").any() or results["model"].duplicated().any():
        raise ValueError("Es werden zwei unterschiedliche, nicht leere Modellnamen benötigt.")
    for metric in METRICS:
        results[metric] = pd.to_numeric(results[metric], errors="raise")
        if not results[metric].between(0, 1).all():
            raise ValueError(f"{metric}: Alle Werte müssen als Dezimalzahlen zwischen 0 und 1 vorliegen.")
    return results


def plot_results(results: pd.DataFrame, output_dir: Path) -> list[Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    paths = []
    for metric, label in METRICS.items():
        fig, ax = plt.subplots(figsize=(8, 5))
        bars = ax.bar(results["model"], results[metric], color=["#4477AA", "#EE7733"])
        if metric == "brier_score":
            ax.set_ylim(0, max(float(results[metric].max()) * 1.2, 0.001))
            ax.ticklabel_format(axis="y", style="plain", useOffset=False)
        else:
            ax.set_ylim(0, 1.1)
            ax.set_yticks([0, 0.2, 0.4, 0.6, 0.8, 1])
        ax.set_ylabel(label)
        direction = "niedriger ist besser" if metric == "brier_score" else "höher ist besser"
        ax.set_title(f"{label} – {direction}")
        ax.bar_label(bars, labels=[format(value, ".6g") for value in results[metric]], padding=5)
        ax.grid(axis="y", alpha=0.25)
        ax.set_axisbelow(True)
        fig.tight_layout()
        path = output_dir / f"{metric}.png"
        fig.savefig(path, dpi=200)
        plt.close(fig)
        paths.append(path)
    return paths


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("results", type=Path, help="CSV mit den bereits berechneten Kennzahlen")
    parser.add_argument("--output-dir", type=Path, default=Path("plots"))
    args = parser.parse_args()
    try:
        results = load_results(args.results)
    except (OSError, ValueError, pd.errors.ParserError) as error:
        parser.error(str(error))
    paths = plot_results(results, args.output_dir)
    print(results.to_string(index=False))
    for path in paths:
        print(f"Gespeichert: {path}")


if __name__ == "__main__":
    main()
