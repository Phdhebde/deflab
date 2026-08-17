# Defensive Lab

Un laboratoire de sécurité défensive **modulaire** : chaque module tient sur une
machine ordinaire, se lance en une commande, contient un scénario d'attaque
reproductible et la détection qui le couvre.

Chaque module suit la même boucle, sans sauter d'étape : **télémétrie → attaque
→ détection → mesure**, et se termine par les deux sections qui comptent le
plus — les faux positifs réellement observés, et les angles morts assumés.

[Parcourir les modules](modules/index.md){ .md-button .md-button--primary }

## Comment lire un module

Les dix sections sont identiques d'un module à l'autre : on apprend la structure
une fois. Les sections 9 et 10 (*faux positifs observés*, *angles morts*) sont
le cœur du travail — une détection non calibrée est une détection inutile, et
savoir dire ce qu'on ne voit pas vaut mieux que prétendre tout couvrir.

## Interface uniforme

Tout module s'utilise avec les mêmes commandes :

```bash
make up       # monter l'environnement
make attack   # rejouer le scénario d'attaque
make verify   # vérifier que la détection se déclenche
make down     # arrêter
make clean    # tout supprimer
```
