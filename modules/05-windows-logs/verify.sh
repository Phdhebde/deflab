#!/usr/bin/env bash
# Validation en deux temps :
#   1. la détection se déclenche sur le scénario   (sinon la règle ne sert à rien)
#   2. elle ne se déclenche pas sur le corpus légitime (sinon elle est trop large)
#
# Le second contrôle est celui qui compte. Une détection bruyante est une
# détection inutile — cf. section 9 du write-up.
set -euo pipefail

CHAINSAW="${1:?chemin de chainsaw attendu}"
WORK="${2:?répertoire de travail attendu}"
SIGMA="${3:?dépôt sigma attendu}"

MAPPING="$(dirname "$CHAINSAW")/mappings/sigma-event-logs-all.yml"
RULES="detections"
NEGATIVE="corpus-negatif"

if [ ! -d "$WORK" ] || [ -z "$(find "$WORK" -name '*.evtx' -print -quit)" ]; then
    echo "Aucun journal dans ${WORK}/ — lancer 'make attack' d'abord." >&2
    exit 1
fi

hunt() {  # hunt <cible> <fichier-sortie>
    "$CHAINSAW" hunt "$1" \
        --sigma "$RULES" \
        --mapping "$MAPPING" \
        --json > "$2" 2>/dev/null || true
}

echo "=== 1/2 — La détection se déclenche-t-elle sur le scénario ? ==="
hunt "$WORK" "$WORK/hits.json"
hits=$(python3 -c "import json,sys; print(len(json.load(open(sys.argv[1]))))" "$WORK/hits.json")
echo "    ${hits} détection(s)"

if [ "$hits" -eq 0 ]; then
    echo "✘ ÉCHEC : aucune détection. La règle ne couvre pas ce scénario." >&2
    exit 1
fi
echo "✔ La détection se déclenche."

echo
echo "=== 2/2 — Se déclenche-t-elle à tort sur l'activité légitime ? ==="
if [ ! -d "$NEGATIVE" ] || [ -z "$(find "$NEGATIVE" -name '*.evtx' -print -quit 2>/dev/null)" ]; then
    echo "⚠ Corpus négatif absent — contrôle sauté."
    echo "  Ce contrôle est le plus instructif du module : sans lui, on ne sait"
    echo "  rien du bruit de la règle. Constituer le corpus depuis une machine"
    echo "  Windows au repos, puis le placer dans ${NEGATIVE}/ :"
    echo "    wevtutil epl Microsoft-Windows-Sysmon/Operational benign.evtx"
    exit 0
fi

hunt "$NEGATIVE" "$WORK/noise.json"
noise=$(python3 -c "import json,sys; print(len(json.load(open(sys.argv[1]))))" "$WORK/noise.json")
echo "    ${noise} déclenchement(s) sur activité légitime"

if [ "$noise" -gt 0 ]; then
    echo "✘ ÉCHEC : la règle est trop large. Documenter le bruit en section 9." >&2
    exit 1
fi
echo "✔ Aucun faux positif sur le corpus négatif."
