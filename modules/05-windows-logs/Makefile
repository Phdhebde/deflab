# Module 05 — Logs Windows (Chainsaw + EVTX-ATTACK-SAMPLES)
#
# Aucun service ne tourne : le module rejoue des journaux d'événements Windows
# pré-enregistrés contre des règles Sigma, hors ligne. Coût en ressources : nul.

SHELL := /bin/bash
.SHELLFLAGS := -eu -o pipefail -c
.DEFAULT_GOAL := help

CACHE   := .cache
WORK    := work
SAMPLES := $(CACHE)/EVTX-ATTACK-SAMPLES
SIGMA   := $(CACHE)/sigma
CHAINSAW := $(CACHE)/chainsaw/chainsaw

# Motif de sélection de l'échantillon rejoué. Surchargeable :
#   make attack PATTERN=mimikatz
PATTERN ?= certutil

.PHONY: help up down attack verify clean samples

help:
	@echo "Module 05 — Logs Windows"
	@echo "  make up      télécharger Chainsaw, les règles Sigma et les échantillons EVTX"
	@echo "  make samples lister les échantillons disponibles"
	@echo "  make attack  rejouer un échantillon (PATTERN=$(PATTERN))"
	@echo "  make verify  vérifier que la détection se déclenche"
	@echo "  make down    aucun service à arrêter (module hors ligne)"
	@echo "  make clean   supprimer $(CACHE)/ et $(WORK)/"

up: $(CHAINSAW) $(SAMPLES) $(SIGMA)
	@echo "✔ Environnement prêt. Voir 'make samples' puis 'make attack'."

$(CHAINSAW):
	@mkdir -p $(CACHE)/chainsaw
	@echo "→ Chainsaw (dernière release)"
	@url=$$(curl -fsSL https://api.github.com/repos/WithSecureLabs/chainsaw/releases/latest \
	  | grep -o 'https://[^"]*x86_64-unknown-linux-gnu\.tar\.gz' | head -1); \
	 test -n "$$url" || { echo "release Chainsaw introuvable"; exit 1; }; \
	 curl -fsSL "$$url" | tar xz -C $(CACHE)/chainsaw --strip-components=1
	@chmod +x $(CHAINSAW)

$(SAMPLES):
	@echo "→ EVTX-ATTACK-SAMPLES"
	@git clone --depth 1 -q https://github.com/sbousseaden/EVTX-ATTACK-SAMPLES.git $(SAMPLES)

$(SIGMA):
	@echo "→ Règles Sigma (SigmaHQ)"
	@git clone --depth 1 -q https://github.com/SigmaHQ/sigma.git $(SIGMA)

samples: $(SAMPLES)
	@find $(SAMPLES) -name '*.evtx' | sed 's|$(SAMPLES)/||' | sort

attack: up
	@./attack/replay.sh "$(PATTERN)" "$(SAMPLES)" "$(WORK)"

verify: up
	@./verify.sh "$(CHAINSAW)" "$(WORK)" "$(SIGMA)"

down:
	@echo "Aucun service à arrêter : ce module tourne hors ligne."

clean:
	@rm -rf $(CACHE) $(WORK)
	@echo "✔ $(CACHE)/ et $(WORK)/ supprimés."
