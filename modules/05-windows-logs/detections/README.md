# Détections du module 05

Règles Sigma évaluées par Chainsaw contre les journaux de `work/`.

## Cycle de vie d'une règle ici

1. **Hypothèse** — la règle est écrite à partir de la compréhension de la
   technique, avant d'avoir vu la moindre donnée. Statut `experimental`.
2. **Confrontation au scénario** — `make verify` (contrôle 1/2). Si elle ne se
   déclenche pas, l'hypothèse sur le champ discriminant était fausse.
3. **Calibration** — `make verify` (contrôle 2/2) contre `corpus-negatif/`.
   Chaque déclenchement à tort part en section 9 du write-up.
4. **Stabilisation** — statut `stable` seulement une fois les deux contrôles
   passés et le bruit documenté.

Une règle qui n'a pas franchi l'étape 3 n'est pas une détection : c'est une
intention. Le champ `falsepositives` doit refléter ce qui a été **observé**,
pas ce qui est plausible.

## Le corpus négatif

`corpus-negatif/` n'est pas versionné (il contient des journaux d'une vraie
machine). Le constituer depuis une session Windows au repos :

```powershell
wevtutil epl Microsoft-Windows-Sysmon/Operational corpus-negatif/benign.evtx
```

Une heure d'activité normale suffit à disqualifier la plupart des règles trop
larges.
