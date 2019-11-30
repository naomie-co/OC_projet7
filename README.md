# OC projet7 - GrandPy Bot


Si vous souhaitez installer GrandPy Bot en local, voici la marche à suivre:

## 1 - Création de l’environnement virtuel
Ce programme est exécuté en Python et utilse le Framework Flask.

Pour l'exécuter, il faut au préalable créer un environnement virtuel. 

Une fois l'environnement virtuel créé, lancez l'installation de dépendances avec la commande:

    pip install -r requirements.txt 

## 2 - Connexion à l'API Google Geocoding
Pour une utilisation en local, il est nécessaire de posséder une clé d'API Google maps geocoding. Elle doit être insérée dans la fichier api_classes.py dans la variable **API_KEY**

## 3 - Lancer le fichier run.py
Pour accéder au site en local, il faut lancer le fichier run.py, puis se rendre à l'adresse indiquée dans la console.
Le site s'affiche. 

Vous avez alors la possibilité de rechercher une lieu, le bot vous donne l'adresse de ce lieu et raconte une anecdote.

## 4 - Lien vers le site
Si vous souhaitez tester GrandPy Bot, cliquez sur ce lien:

	https://obscure-hamlet-87573.herokuapp.com/ 