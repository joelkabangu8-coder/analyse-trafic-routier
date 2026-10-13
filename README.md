# Analyse de comptages de trafic routier

Petit projet Python pour explorer des données de trafic routier : nettoyage d'un fichier de comptages et tracé des profils horaire, hebdomadaire et mensuel du débit moyen.

## Pourquoi ce projet
Le trafic est un facteur déterminant de la dégradation des chaussées et du dimensionnement de leur épaisseur. Ce projet est une première étape pour apprendre à traiter ce type de données avec Python.

## Utilisation
1. Installer les dépendances : `pip install -r requirements.txt`
2. Télécharger un jeu de données de comptages de trafic (par exemple sur Données Québec) et l'enregistrer en CSV.
3. Lancer : `python analyse_trafic.py donnees.csv --col-date NOM_COLONNE_DATE --col-debit NOM_COLONNE_DEBIT`

Les graphiques sont enregistrés dans le dossier `resultats/`.

## Carte des débits
`carte_trafic.py` affiche les stations de comptage sur une carte interactive (GeoPandas + Folium) : plus le débit moyen est élevé, plus le cercle est grand.

`python carte_trafic.py donnees.csv --col-lat LATITUDE --col-lon LONGITUDE --col-debit DEBIT`

Le résultat est un fichier `carte_trafic.html` à ouvrir dans un navigateur.

## Prochaines étapes
- Convertir les comptages en charge de dimensionnement de chaussée
- Prédire le débit avec scikit-learn

## Auteur
Joël Kabangu
