# Proposition d'ajouts au glossaire

Ce document recense des termes identifiés lors de la traduction FR → EN qui ne figurent pas encore dans le glossaire officiel (`glossaire.csv`). Ils sont soumis à validation de l'équipe technique avant intégration.

> **Note de mise à jour (2026-06-24)** : Après vérification contre `glossaire.csv` (version complète reçue le 02.02), deux termes initialement proposés ont été retirés car déjà présents dans le glossaire officiel :
> - **Base Empreinte®** → déjà dans le CSV : `Base Empreinte®,Base Empreinte®`
> - **Cadrage** → déjà dans le CSV : `Framework,Cadrage`

---

## Termes issus de la traduction des infographies — incertitude des données d'activité

### Contexte
Ces termes ont été identifiés lors de la traduction de l'infographie *"Exemple de détermination de l'incertitude des données d'activité"*. Ils correspondent aux 5 dimensions de qualité de la matrice Pedigree (Weidema & Wesnæs, 1996) utilisées pour évaluer l'incertitude dans la méthode Bilan Carbone®.

**Décision validée : s'inspirer des termes EcoInvent, avec adaptation** (confirmé par Gabriel C., 2026-06-24). "Further technical correlation" simplifié en "Technical correlation" pour éviter les confusions. Les 4 autres termes sont identiques à EcoInvent.

| Terme FR (BC) | Terme EN retenu | Sources comparatives | Justification du choix | Définition suggérée |
|---|---|---|---|---|
| Représentativité technique | **Technical correlation** | EcoInvent Pedigree Matrix (Weidema & Wesnæs, 1996) : **"Further technical correlation"** — ISO 14064-1 : non nommé explicitement — GHG Protocol : non nommé explicitement | Adapté d'EcoInvent : "Further" retiré pour éviter les confusions (décision Gabriel C., 2026-06-24). "Technical correlation" retenu. | Degré auquel la donnée d'activité reflète fidèlement le processus ou l'équipement réellement utilisé par l'organisation. |
| Représentativité géographique | **Geographic correlation** | EcoInvent Pedigree Matrix : **"Geographic correlation"** ✅ — ISO 14064-1 : non nommé explicitement (ISO 14069 mentionne un critère géographique) — GHG Protocol : non nommé dans le standard core | Terme exact EcoInvent. "Geographic" (non "Geographical") : mot exact EcoInvent, sans le suffixe "-al". | Degré auquel la donnée d'activité reflète les conditions propres à la zone géographique concernée. |
| Représentativité temporelle | **Temporal correlation** | EcoInvent Pedigree Matrix : **"Temporal correlation"** ✅ — ISO 14064-1 : utilise "temporal coverage" dans un sens légèrement différent — GHG Protocol : non nommé dans le standard core | Terme exact EcoInvent. "Temporal coverage" (ISO) écarté car il désigne la période couverte par les données, pas leur représentativité. | Degré auquel la donnée d'activité correspond à la période de temps sur laquelle porte le Bilan Carbone®. |
| Complétude | **Completeness** | ISO 14064-1 §5.6 : **"Completeness"** ✅ — GHG Protocol : **"Completeness"** ✅ — EcoInvent Pedigree Matrix : **"Completeness"** ✅ | Seul terme partagé à l'identique par les trois standards. Choix sans ambiguïté. | Degré auquel la donnée d'activité couvre l'ensemble des sources d'émissions pertinentes pour le poste concerné. |
| Fiabilité | **Reliability** | EcoInvent Pedigree Matrix : **"Reliability"** ✅ — ISO 14064-1 : utilise "accuracy" et "uncertainty", pas "reliability" — GHG Protocol : utilise "accuracy", pas "reliability" | Terme exact EcoInvent, seule source à nommer explicitement ce critère. À distinguer de "accuracy" (précision de la mesure) utilisé par ISO et GHG Protocol. | Degré de confiance que l'on peut accorder à la source et à la méthode de collecte de la donnée d'activité (vérifiabilité, traçabilité). |

### Questions pour la validation technique
- Les définitions suggérées ci-dessus correspondent-elles à l'usage fait dans la méthode ?
- Ces 5 dimensions sont-elles appliquées de la même façon aux données d'activité et aux facteurs d'émission ?
- Ces 5 dimensions sont-elles toutes obligatoires ou certaines optionnelles selon le niveau de maturité ?

---

## Termes issus de la traduction des infographies — parcours de transition bas carbone

### Contexte
Ces termes ont été identifiés lors de la traduction des infographies *"Parcours de transition bas carbone"* et *"Parcours 2 : Intégration"*. Ils désignent des étapes ou concepts structurants de la méthode Bilan Carbone® sans entrée propre dans `glossaire.csv`.

| Terme FR | Terme EN proposé | Sources comparatives | Justification du choix | Définition suggérée |
|---|---|---|---|---|
| Parcours (de transition bas carbone) | **Pathway** | SBTi : **"pathway"** pour désigner une voie de transition — ACT Pas à Pas : utilise "parcours" pour les trois options d'intégration d'ACT dans la démarche BC — GIEC : **"pathway"** pour les scénarios de transition | "Pathway" est le terme EN standard dans les cadres climatiques pour désigner une voie ou option de transition. Les trois parcours BC deviennent : Pathway 1: Initiation, Pathway 2: Integration, Pathway 3: Steering. | L'une des trois options possibles pour intégrer ACT (Accelerate Climate Transition) dans la démarche Bilan Carbone®. Chaque parcours définit un niveau d'articulation entre les deux méthodes : Parcours 1 Initiation, Parcours 2 Intégration, Parcours 3 Pilotage. |
| Décarbonation | **Decarbonization** | GHG Protocol : **"decarbonization"** — SBTi : **"decarbonization pathway"**, **"decarbonization strategy"** — CSRD/ESRS E1 : **"decarbonization"** — GIEC AR6 : **"decarbonization"** | Terme universellement consacré dans les standards EN. Aucune ambiguïté. | Processus de réduction progressive des émissions de GES d'une organisation, d'un secteur ou d'une économie, visant à atteindre un niveau compatible avec les objectifs de l'Accord de Paris. |

### Questions pour la validation technique
- Les trois parcours (Initiation, Intégration, Pilotage) ont-ils des définitions officielles décrivant précisément ce que couvre chaque option d'intégration ACT × BC ?
- "Décarbonation" est-il à distinguer de "réduction des émissions" dans la méthode, ou les deux termes sont-ils interchangeables ?

---

*Document mis à jour le 2026-06-24 — retiré : Base Empreinte® et Cadrage (déjà dans glossaire.csv officiel). Termes EcoInvent retenus pour les dimensions d'incertitude, avec adaptation : "Further technical correlation" → "Technical correlation" (décision Gabriel C.).*
