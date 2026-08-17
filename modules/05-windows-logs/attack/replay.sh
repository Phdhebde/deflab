#!/usr/bin/env bash
# Sélectionne et « rejoue » un échantillon EVTX.
#
# Précision importante, à assumer dans le write-up : l'attaque n'est pas exécutée
# ici. Elle a été exécutée par quelqu'un d'autre, sur une vraie machine Windows,
# et ce qu'on rejoue est sa *télémétrie*. C'est ce qui rend le module gratuit —
# et c'est aussi son premier angle mort (section 10).
set -euo pipefail

PATTERN="${1:?motif de recherche attendu}"
SAMPLES="${2:?répertoire des échantillons attendu}"
WORK="${3:?répertoire de travail attendu}"

mapfile -t matches < <(find "$SAMPLES" -name '*.evtx' -ipath "*${PATTERN}*" | sort)

if [ "${#matches[@]}" -eq 0 ]; then
    echo "Aucun échantillon ne correspond à « ${PATTERN} »." >&2
    echo "Lister les échantillons disponibles : make samples" >&2
    exit 1
fi

echo "Échantillons correspondant à « ${PATTERN} » : ${#matches[@]}"
for m in "${matches[@]}"; do
    echo "  - ${m#"$SAMPLES"/}"
done

rm -rf "$WORK"
mkdir -p "$WORK"
for m in "${matches[@]}"; do
    cp "$m" "$WORK/"
done

echo
echo "✔ ${#matches[@]} journal(aux) copié(s) dans ${WORK}/ — prêt pour 'make verify'."
