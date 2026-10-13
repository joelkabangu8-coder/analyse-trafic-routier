"""Analyse de comptages de trafic routier : profils horaires, hebdomadaires et mensuels.

Usage :
    python analyse_trafic.py donnees.csv --col-date date_heure --col-debit debit
"""
import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


def charger(chemin, col_date, col_debit):
    """Lit le CSV, convertit les dates, retire les valeurs manquantes ou négatives."""
    df = pd.read_csv(chemin)
    df[col_date] = pd.to_datetime(df[col_date], errors="coerce")
    df[col_debit] = pd.to_numeric(df[col_debit], errors="coerce")
    avant = len(df)
    df = df.dropna(subset=[col_date, col_debit])
    df = df[df[col_debit] >= 0]
    print(f"{avant - len(df)} lignes invalides retirées sur {avant}.")
    df["heure"] = df[col_date].dt.hour
    df["jour"] = df[col_date].dt.dayofweek  # 0 = lundi
    df["mois"] = df[col_date].dt.month
    return df


def tracer(df, col_debit, sortie):
    """Trace trois profils moyens et les enregistre en PNG."""
    sortie.mkdir(exist_ok=True)
    profils = [
        ("heure", "Heure de la journée", "profil_horaire.png"),
        ("jour", "Jour de la semaine (0 = lundi)", "profil_hebdomadaire.png"),
        ("mois", "Mois", "profil_mensuel.png"),
    ]
    for col, etiquette, fichier in profils:
        moyenne = df.groupby(col)[col_debit].mean()
        fig, ax = plt.subplots(figsize=(7, 4))
        moyenne.plot(ax=ax, marker="o")
        ax.set_xlabel(etiquette)
        ax.set_ylabel("Débit moyen (véhicules)")
        ax.grid(alpha=0.3)
        fig.tight_layout()
        fig.savefig(sortie / fichier, dpi=150)
        plt.close(fig)
        print(f"Graphique enregistré : {sortie / fichier}")


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("csv", help="fichier CSV de comptages")
    p.add_argument("--col-date", default="date_heure")
    p.add_argument("--col-debit", default="debit")
    p.add_argument("--sortie", default="resultats")
    a = p.parse_args()

    df = charger(a.csv, a.col_date, a.col_debit)
    print(df[a.col_debit].describe())
    tracer(df, a.col_debit, Path(a.sortie))


if __name__ == "__main__":
    main()
