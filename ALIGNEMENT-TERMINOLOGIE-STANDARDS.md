# Alignement terminologique avec les standards internationaux

Ce document compare les 5 dimensions de qualité des données d'activité utilisées dans la méthode Bilan Carbone® avec la terminologie employée par les principaux standards internationaux : ISO 14064-1, GHG Protocol et EcoInvent.

L'objectif est de choisir des traductions EN cohérentes avec l'usage international, et d'identifier les termes qui n'ont pas d'équivalent direct dans ces standards.

---

## Tableau comparatif

| Terme Bilan Carbone® (FR) | Terme Bilan Carbone® (EN proposé) | ISO 14064-1:2018 | GHG Protocol (Corporate Standard) | EcoInvent (matrice Pedigree) |
|---|---|---|---|---|
| Représentativité technique | Technical representativeness | ⚠️ Non nommé explicitement — couvert implicitement par le critère de *relevance* (pertinence) des facteurs d'émission | ⚠️ Non nommé explicitement — abordé dans les guides pratiques sur la sélection des FE | ✅ **"Further technological correlation"** — critère explicite de la matrice Pedigree (Weidema & Wesnæs, 1996) |
| Représentativité géographique | Geographical representativeness | ⚠️ Non nommé explicitement — mentionné dans ISO 14069 (guide d'application) comme critère de sélection des FE | ⚠️ Mentionné dans les guides de sélection des FE, pas dans le standard core | ✅ **"Geographical correlation"** — critère explicite de la matrice Pedigree |
| Représentativité temporelle | Temporal representativeness | ⚠️ Non nommé explicitement — ISO 14064-1 utilise *"temporal coverage"* dans le contexte des FE | ⚠️ Mentionné comme *"temporal representativeness"* dans les guides, pas dans le standard core | ✅ **"Temporal correlation"** — critère explicite de la matrice Pedigree |
| Complétude | Completeness | ✅ **"Completeness"** — critère explicite de qualité des données (§ 5.6) | ✅ **"Completeness"** — principe fondamental du standard | ✅ **"Completeness"** — critère explicite de la matrice Pedigree |
| Fiabilité | Reliability | ⚠️ Couvert par *"accuracy"* et *"uncertainty"* — pas nommé "reliability" en tant que tel | ⚠️ Couvert par *"accuracy"* — pas nommé "reliability" en tant que tel | ✅ **"Reliability"** — critère explicite de la matrice Pedigree |

---

## Analyse et recommandations

### Ce que ça révèle

Les 3 dimensions de représentativité (technique, géographique, temporelle) et la fiabilité sont des concepts issus principalement de la **matrice Pedigree d'EcoInvent** (Weidema & Wesnæs, 1996), adaptés à la comptabilité carbone. Elles ne font **pas partie du vocabulaire normé d'ISO 14064-1 ou du GHG Protocol Corporate Standard** en tant que critères nommés explicitement.

Seule la **complétude** est un terme partagé par les trois standards.

### Recommandations de traduction EN

| Terme FR | Traduction recommandée | Justification |
|---|---|---|
| Représentativité technique | **Technological representativeness** | Aligné avec EcoInvent ("further technological correlation") et la littérature ACV. Préférer "technological" à "technical" pour cohérence avec les bases de données d'émission. |
| Représentativité géographique | **Geographical representativeness** | Terme cohérent avec EcoInvent et la littérature académique. |
| Représentativité temporelle | **Temporal representativeness** | Terme cohérent avec EcoInvent. Éviter "temporal coverage" (ISO) qui a un sens légèrement différent. |
| Complétude | **Completeness** | Terme universel, cohérent avec les 3 standards. |
| Fiabilité | **Reliability** | Aligné avec EcoInvent. À distinguer de *"accuracy"* (précision) utilisé par ISO et GHG Protocol. |

### Questions pour la validation technique

1. La méthode Bilan Carbone® s'appuie-t-elle explicitement sur la matrice Pedigree d'EcoInvent pour définir ces 5 critères, ou s'en est-elle inspirée librement ?
2. Est-ce que "technological representativeness" (vs "technical representativeness") correspond mieux à l'usage interne ABC ?
3. Pour ISO 14064 et GHG Protocol, confirmer que ces 3 dimensions de représentativité ne sont effectivement pas des termes normés — ou indiquer la section exacte si elles y figurent.

---

## Référence : matrice Pedigree EcoInvent

La matrice Pedigree (Weidema & Wesnæs, 1996 ; reprise dans ecoinvent v3) évalue la qualité d'une donnée selon 5 critères notés de 1 (très bon) à 5 (très mauvais) :

| Critère EcoInvent | Correspondance Bilan Carbone® FR | Score 1 (meilleur) | Score 5 (moins bon) |
|---|---|---|---|
| Reliability | Fiabilité | Données mesurées vérifiées | Estimation non vérifiée |
| Completeness | Complétude | Représentatif de > 50% des sites sur > 3 ans | Représentatif d'un seul site sur < 1 an |
| Temporal correlation | Représentativité temporelle | < 3 ans d'écart | > 15 ans d'écart |
| Geographical correlation | Représentativité géographique | Même zone géographique | Données mondiales non différenciées |
| Further technological correlation | Représentativité technique | Même procédé, même technologie | Procédé différent ou technologie obsolète |

---

*Document créé le 2026-06-23 — à soumettre à validation technique avant d'intégrer les termes EN dans le glossaire et les infographies.*
