"""Carte interactive des débits de trafic par station de comptage.

Usage :
    python carte_trafic.py donnees.csv --col-lat latitude --col-lon longitude --col-debit debit
Le fichier CSV doit contenir une ligne par station (ou par comptage) avec ses coordonnées.
"""
import argparse

import folium
import geopandas as gpd
import pandas as pd


def charger_stations(chemin, col_lat, col_lon, col_debit):
    """Lit le CSV, agrège le débit moyen par station et crée un GeoDataFrame."""
    df = pd.read_csv(chemin)
    for col in (col_lat, col_lon, col_debit):
        df[col] = pd.to_numeric(df[col], errors="coerce")
    df = df.dropna(subset=[col_lat, col_lon, col_debit])
    df = df.groupby([col_lat, col_lon], as_index=False)[col_debit].mean()
    return gpd.GeoDataFrame(
        df,
        geometry=gpd.points_from_xy(df[col_lon], df[col_lat]),
        crs="EPSG:4326",
    )


def creer_carte(gdf, col_debit, sortie):
    """Dessine un cercle par station : plus le débit est élevé, plus il est grand."""
    centre = [gdf.geometry.y.mean(), gdf.geometry.x.mean()]
    carte = folium.Map(
        location=centre,
        zoom_start=11,
        tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Street_Map/MapServer/tile/{z}/{y}/{x}",
        attr="Tuiles : Esri, HERE, Garmin, OpenStreetMap contributors",
    )
    maximum = gdf[col_debit].max()
    for _, ligne in gdf.iterrows():
        folium.CircleMarker(
            location=[ligne.geometry.y, ligne.geometry.x],
            radius=3 + 12 * ligne[col_debit] / maximum,
            popup=f"Débit moyen : {ligne[col_debit]:.0f}",
            color="crimson",
            fill=True,
            fill_opacity=0.6,
        ).add_to(carte)
    carte.save(sortie)
    print(f"Carte enregistrée : {sortie}")


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("csv")
    p.add_argument("--col-lat", default="latitude")
    p.add_argument("--col-lon", default="longitude")
    p.add_argument("--col-debit", default="debit")
    p.add_argument("--sortie", default="carte_trafic.html")
    a = p.parse_args()

    gdf = charger_stations(a.csv, a.col_lat, a.col_lon, a.col_debit)
    print(f"{len(gdf)} stations chargées.")
    creer_carte(gdf, a.col_debit, a.sortie)


if __name__ == "__main__":
    main()
