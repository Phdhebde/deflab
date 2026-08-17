# Defensive Lab

[![docs](https://github.com/Phdhebde/deflab/actions/workflows/docs.yml/badge.svg)](https://github.com/Phdhebde/deflab/actions/workflows/docs.yml)
[![validate](https://github.com/Phdhebde/deflab/actions/workflows/validate.yml/badge.svg)](https://github.com/Phdhebde/deflab/actions/workflows/validate.yml)
[![site](https://img.shields.io/badge/site-phdhebde.github.io%2Fdeflab-indigo)](https://phdhebde.github.io/deflab/)

**Un laboratoire de sécurité défensive modulaire.** Chaque module tient sur une
machine ordinaire, se lance en une commande, contient un scénario d'attaque
reproductible et la détection qui le couvre — le tout documenté publiquement.

**[Lire les write-ups →](https://phdhebde.github.io/deflab/)**

---

## Le principe

Un module = un dossier = un fichier compose isolé = un write-up. Aucun module ne
dépend du démarrage d'un autre. On lance celui sur lequel on travaille, on
l'arrête, on passe au suivant.

Chaque module suit la boucle complète du métier, sans sauter d'étape :

```
télémétrie → attaque rejouable → observation → détection → calibration → angles morts
```

## Les modules

| # | Module | Stack | Coût | Statut |
| --- | --- | --- | --- | --- |
| 01 | Socle de télémétrie | Loki + Grafana | Moyen | à venir |
| 02 | Runtime conteneur | Falco | Léger | à venir |
| 03 | Supply chain | Syft, Grype, cosign | Nul | à venir |
| 04 | Analyse réseau | Zeek sur pcap public | Léger | à venir |
| 05 | Logs Windows | Chainsaw + EVTX-ATTACK-SAMPLES | Nul | **en cours** |
| 06 | Détection AppSec | Semgrep + règles custom | Nul | à venir |
| 07 | Deception | Canarytokens, T-Pot | Léger | à venir |
| 08 | Detection-as-Code | CI de validation | Nul | à venir |

## Interface uniforme

Tous les modules exposent les mêmes cibles. On apprend l'interface une fois :

```bash
cd modules/05-windows-logs
make up       # monter l'environnement
make attack   # rejouer le scénario d'attaque
make verify   # vérifier que la détection se déclenche
make down     # arrêter
make clean    # tout supprimer
```

## Le gabarit de write-up

Chaque `modules/*/README.md` suit exactement les [dix sections
imposées](shared/template/MODULE.md), vérifiées en CI :

1. Objectif · 2. Prérequis · 3. Architecture · 4. Montage · 5. Scénario d'attaque ·
6. Ce que je vois · 7. La détection · 8. Validation ·
**9. Faux positifs observés** · **10. Angles morts**

Les sections 9 et 10 sont le cœur du projet. Une détection non calibrée est une
détection inutile ; documenter ce qu'on ne voit pas vaut mieux que prétendre
tout couvrir.

## Organisation du dépôt

```
modules/<nn>-<slug>/     un module autonome (write-up, compose, détections, attaque, preuves)
shared/template/         le gabarit imposé
tools/                   vérification de structure, synchronisation du site
docs/                    source du site (les write-ups y sont recopiés au build)
.github/workflows/       publication du site, validation
```

Le write-up vit dans `modules/*/README.md` — **source unique de vérité**. Le
site le réutilise, il n'est jamais dupliqué.

## Contribuer / rejouer un module

Prérequis : Docker, GNU Make, Python 3.12+.
Sous Windows, lancer les modules depuis WSL (Make et les scripts sont POSIX).

```bash
pip install -r requirements-docs.txt
python tools/check_structure.py   # les dix sections sont-elles là ?
python tools/sync_docs.py && mkdocs serve
```

## Licence

[MIT](LICENSE)
