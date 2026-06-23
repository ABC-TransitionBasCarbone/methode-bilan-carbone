# Proposition d'ajouts au glossaire

Ce document recense des termes identifiés lors de la traduction FR → EN qui ne figurent pas encore dans le glossaire (`annexes/glossaire.md`). Ils sont soumis à validation de l'équipe technique avant intégration.

---

## Termes issus de la traduction des infographies — incertitude des données d'activité

### Contexte
Ces termes ont été identifiés lors de la traduction de l'infographie *"Exemple de détermination de l'incertitude des données d'activité"*. Ils correspondent aux 5 dimensions de qualité utilisées pour évaluer l'incertitude des données d'activité dans la méthode Bilan Carbone®.

| Terme FR | Terme EN proposé | Sources comparatives | Justification du choix | Définition suggérée |
|---|---|---|---|---|
| Représentativité technique | **Technical representativeness** | EcoInvent Pedigree Matrix (Weidema & Wesnæs, 1996) : **"Further technical correlation"** — ISO 14064-1 : non nommé explicitement — GHG Protocol : non nommé explicitement | Le terme BC adapte "Further technical correlation" (EcoInvent) en "Technical representativeness". "Technical" retenu (et non "technological") car c'est le mot exact d'EcoInvent. | Degré auquel la donnée d'activité reflète fidèlement le processus ou l'équipement réellement utilisé par l'organisation. |
| Représentativité géographique | **Geographic representativeness** | EcoInvent Pedigree Matrix : **"Geographic correlation"** — ISO 14064-1 : non nommé explicitement (ISO 14069 mentionne un critère géographique) — GHG Protocol : non nommé dans le standard core | "Geographic" (et non "Geographical") pour rester cohérent avec le terme exact EcoInvent ("Geographic correlation", sans "al"). | Degré auquel la donnée d'activité reflète les conditions propres à la zone géographique concernée. |
| Représentativité temporelle | **Temporal representativeness** | EcoInvent Pedigree Matrix : **"Temporal correlation"** — ISO 14064-1 : utilise "temporal coverage" dans un sens légèrement différent — GHG Protocol : non nommé dans le standard core | "Temporal representativeness" adapté de "Temporal correlation" (EcoInvent). "Temporal coverage" (ISO) écarté car il désigne la période couverte par les données, pas leur représentativité. | Degré auquel la donnée d'activité correspond à la période de temps sur laquelle porte le Bilan Carbone®. |
| Complétude | **Completeness** | ISO 14064-1 §5.6 : **"Completeness"** ✅ — GHG Protocol : **"Completeness"** ✅ — EcoInvent Pedigree Matrix : **"Completeness"** ✅ | Seul terme partagé à l'identique par les trois standards. Choix sans ambiguïté. | Degré auquel la donnée d'activité couvre l'ensemble des sources d'émissions pertinentes pour le poste concerné. |
| Fiabilité | **Reliability** | EcoInvent Pedigree Matrix : **"Reliability"** ✅ — ISO 14064-1 : utilise "accuracy" et "uncertainty", pas "reliability" — GHG Protocol : utilise "accuracy", pas "reliability" | "Reliability" retenu car c'est le terme exact EcoInvent, seul standard à nommer explicitement ce critère. À distinguer de "accuracy" (précision de la mesure) utilisé par ISO et GHG Protocol. | Degré de confiance que l'on peut accorder à la source et à la méthode de collecte de la donnée d'activité (vérifiabilité, traçabilité). |

### Questions pour la validation technique
- Les définitions suggérées ci-dessus correspondent-elles à l'usage fait dans la méthode ?
- Ces 5 dimensions sont-elles appliquées de la même façon aux données d'activité et aux facteurs d'émission (voir infographie suivante) ?
- Ces 5 dimensions sont-elles toutes obligatoires ou certaines optionnelles selon le niveau de maturité ?

---

## Termes issus de la traduction des infographies — incertitude du facteur d'émission

### Contexte
Ces termes ont été identifiés lors de la traduction de l'infographie *"Exemple de détermination de l'incertitude du facteur d'émission"*.

| Terme FR | Terme EN proposé | Sources comparatives | Justification du choix | Définition suggérée |
|---|---|---|---|---|
| Base Empreinte® | **Base Empreinte®** (nom propre conservé) | ADEME : nom officiel de la base de données — ISO 14064-1 : référence générique à des "emission factor databases" sans nommer Base Empreinte® — GHG Protocol : idem | Nom propre commercial déposé par l'ADEME. Pas de traduction possible ni souhaitable. Dans les contextes EN, une description entre parenthèses peut être ajoutée : *"Base Empreinte® (ADEME emission factor database)"*. | Base de données de facteurs d'émission publiée et maintenue par l'ADEME. Référence principale pour les calculs du Bilan Carbone® en France. Actuellement mentionnée dans le glossaire sous "Base de données de facteurs d'émission" sans entrée propre. |

### Questions pour la validation technique
- Faut-il créer une entrée glossaire dédiée "Base Empreinte®" ou conserver la référence dans l'entrée "Base de données de facteurs d'émission" ?
- Dans les contextes EN, conserver le nom seul ou ajouter systématiquement *"(ADEME emission factor database)"* ?

---

## Termes issus de la traduction des infographies — parcours de transition bas carbone

### Contexte
Ces termes ont été identifiés lors de la traduction des infographies *"Parcours de transition bas carbone"* et *"Parcours 2 : Intégration"*. Ils désignent des étapes ou concepts structurants de la méthode Bilan Carbone® sans entrée propre dans le glossaire.

| Terme FR | Terme EN proposé | Sources comparatives | Justification du choix | Définition suggérée |
|---|---|---|---|---|
| Cadrage | **Scoping** | ISO 14064-1 §5.1-5.2 : utilise "scoping" implicitement pour la phase de définition des périmètres et objectifs — GHG Protocol : **"scoping"** utilisé couramment dans les guides pratiques — CSRD/ESRS : **"scoping"** pour la définition du périmètre de reporting | "Scoping" est le terme EN consacré dans les standards et la pratique pour désigner la phase initiale de définition du périmètre et des objectifs d'un inventaire GES. | Première étape de la démarche Bilan Carbone® : définition du contexte, des objectifs, du niveau de maturité visé et des ressources mobilisées. |
| Parcours (de transition bas carbone) | **Pathway** | SBTi : **"pathway"** pour désigner une trajectoire ou un niveau d'engagement — ACT Pas à Pas : utilise "parcours" pour les trois niveaux d'engagement (Initiation, Intégration, Pilotage) — GIEC : **"pathway"** pour les scénarios de transition | "Pathway" est le terme EN standard dans les cadres climatiques pour désigner un niveau ou une voie de transition. Les trois parcours BC deviennent : Pathway 1: Initiation, Pathway 2: Integration, Pathway 3: Steering. | Niveau d'engagement et de maturité dans la démarche Bilan Carbone®. Trois parcours existent : Initiation, Intégration, Pilotage. |
| Décarbonation | **Decarbonization** | GHG Protocol : **"decarbonization"** — SBTi : **"decarbonization pathway"**, **"decarbonization strategy"** — CSRD/ESRS E1 : **"decarbonization"** — GIEC AR6 : **"decarbonization"** | Terme universellement consacré dans les standards EN. Aucune ambiguïté. | Processus de réduction progressive des émissions de GES d'une organisation, d'un secteur ou d'une économie, visant à atteindre un niveau compatible avec les objectifs de l'Accord de Paris. |

### Questions pour la validation technique
- Le terme "Cadrage" désigne-t-il uniquement l'étape 1 du parcours BC ou couvre-t-il aussi la phase de recadrage entre deux bilans ?
- Les trois parcours (Initiation, Intégration, Pilotage) ont-ils des définitions officielles dans la méthode BC à intégrer au glossaire ?
- "Décarbonation" est-il à distinguer de "réduction des émissions" dans la méthode, ou les deux termes sont-ils interchangeables ?

---

*Document créé le 2026-06-23 — à compléter au fur et à mesure des traductions d'infographies.*
