# CAHIER DES CHARGES
## Projet EcoWatch – Suivi Local de la Qualité de l'Air

---

## 1. PRÉSENTATION DU PROJET

### 1.1 Contexte
Dans les zones urbaines, notamment en Guinée et en Afrique de l'Ouest, la pollution atmosphérique constitue un enjeu majeur de santé publique. L'absence de mesures précises et localisées de la qualité de l'air empêche les autorités, ONG et citoyens de prendre des décisions éclairées pour protéger la santé des populations.

### 1.2 Objectif général
Développer un système de surveillance environnementale permettant la collecte, l'analyse et la visualisation en temps réel des données de qualité de l'air dans les zones urbaines, avec un modèle économique basé sur la vente de rapports de données.

### 1.3 Portée du projet
Le projet EcoWatch vise à déployer un réseau de capteurs autonomes connectés, capables de mesurer plusieurs paramètres de qualité de l'air et de transmettre ces données vers une plateforme centralisée accessible via une interface web interactive.

---

## 2. DESCRIPTION DE LA SOLUTION

### 2.1 Vue d'ensemble
EcoWatch est un système IoT complet comprenant :
- Des stations de mesure autonomes équipées de capteurs
- Un système de transmission de données (cellulaire/WiFi)
- Une base de données centralisée
- Une plateforme web de visualisation interactive
- Un module de génération de rapports

### 2.2 Architecture technique

#### 2.2.1 Composante Hardware (Stations de mesure)
- **Microcontrôleur** : ESP32 ou Raspberry Pi Pico W
- **Capteurs requis** :
  - Capteur CO (monoxyde de carbone) : MQ-7 ou équivalent
  - Capteur de particules fines (PM2.5/PM10) : SDS011, PMS5003 ou similaire
  - Capteur d'humidité et température : DHT22 ou BME280
  - Capteur de CO₂ : MH-Z19B (optionnel mais recommandé)
  - Capteur de NO₂ et O₃ (optionnel pour version avancée)
- **Alimentation** : Panneau solaire + batterie lithium pour autonomie énergétique
- **Connectivité** : Module GSM/4G (SIM800L/SIM7600) ou WiFi selon disponibilité réseau
- **Boîtier** : Protection IP65 contre intempéries

#### 2.2.2 Composante Software

**Backend (Serveur)**
- **Langage** : Python 3.9+
- **Framework** : Django Framework
- **Base de données** : PostgreSQL avec extension PostGIS pour données géospatiales
- **API REST** : Pour communication stations ↔ serveur
- **Traitement des données** :
  - Validation et nettoyage des données
  - Calcul d'indices de qualité de l'air (IQA)
  - Agrégation temporelle (horaire, journalière, hebdomadaire)
  - Détection d'anomalies et alertes

**Frontend (Interface web)**
- **Technologies** : Django
- **Cartographie** : Leaflet.js ou Mapbox GL JS
- **Visualisations** : Chart.js ou Plotly pour graphiques temporels
- **Fonctionnalités** :
  - Carte interactive avec positionnement des stations
  - Affichage en temps réel des mesures
  - Graphiques d'évolution temporelle
  - Comparaison entre zones
  - Système d'alertes personnalisables
  - Export de données

**Code embarqué (Microcontrôleurs)**
- **Langage** : MicroPython ou C/C++ (Arduino)
- **Fonctions** :
  - Lecture périodique des capteurs
  - Transmission sécurisée des données (HTTPS/MQTT)
  - Gestion de l'énergie (mode veille)
  - Auto-diagnostic et reporting d'erreurs

---

## 3. SPÉCIFICATIONS FONCTIONNELLES

### 3.1 Fonctionnalités principales

#### F1 : Collecte de données
- Mesure automatique toutes les 5 à 15 minutes
- Horodatage précis (GPS ou NTP)
- Géolocalisation de chaque station
- Transmission automatique vers serveur central

#### F2 : Stockage et traitement
- Sauvegarde sécurisée dans base de données
- Calcul automatique de l'indice de qualité de l'air
- Archivage historique sur minimum 2 ans
- Détection d'anomalies et valeurs aberrantes

#### F3 : Visualisation interactive
- Carte affichant toutes les stations avec code couleur selon IQA
- Clic sur station → affichage détails et graphiques
- Filtrage par polluant, date, zone géographique
- Comparaison multi-stations
- Superposition de couches (densité population, trafic, industries)

#### F4 : Système d'alertes
- Alertes automatiques si seuils dépassés
- Notification par email/SMS aux abonnés
- Historique des alertes
- Configuration personnalisable des seuils

#### F5 : Génération de rapports
- Rapports automatisés (quotidien, hebdomadaire, mensuel, annuel)
- Rapports personnalisés sur demande
- Format PDF et Excel
- Analyses statistiques et tendances
- Comparaisons temporelles et spatiales
- Recommandations basées sur données

### 3.2 Utilisateurs et droits d'accès

#### Niveau 1 : Public (gratuit)
- Visualisation carte en temps réel
- Données des dernières 24h
- Indices globaux par zone

#### Niveau 2 : Standard (abonnement basique)
- Accès historique 3 mois
- Export données format CSV
- Rapports mensuels automatiques
- Alertes email basiques

#### Niveau 3 : Premium (ONG, municipalités, entreprises)
- Accès historique complet
- API pour intégration externe
- Rapports personnalisés illimités
- Alertes SMS
- Support prioritaire
- Analyse prédictive (IA)

---

## 4. SPÉCIFICATIONS TECHNIQUES

### 4.1 Performance
- Latence transmission données : < 5 minutes
- Disponibilité système : 99% minimum
- Temps de réponse interface web : < 2 secondes
- Autonomie stations sur batterie : 7 jours minimum sans soleil

### 4.2 Sécurité
- Chiffrement des communications (TLS 1.3)
- Authentification stations (certificats)
- Protection API (tokens JWT)
- Sauvegarde quotidienne base de données
- Protection contre injections SQL
- Conformité RGPD si applicable

### 4.3 Scalabilité
- Architecture supportant 100+ stations simultanées
- Possibilité d'extension à 1000+ stations
- Base de données optimisée pour gros volumes
- Infrastructure cloud élastique (AWS, Azure ou GCP)

### 4.4 Précision des mesures
- CO : ±5% ou ±5 ppm
- PM2.5/PM10 : ±10%
- Humidité : ±2%
- Température : ±0.5°C
- Calibration trimestrielle recommandée

---

## 5. DÉPLOIEMENT ET INFRASTRUCTURE

### 5.1 Phase pilote
- **Zone** : Conakry (quartiers prioritaires à définir)
- **Nombre de stations** : 10-15 stations
- **Durée** : 3 mois
- **Objectifs** :
  - Validation technique du système
  - Tests en conditions réelles
  - Ajustements capteurs et algorithmes
  - Collecte premiers datasets pour démo clients

### 5.2 Déploiement progressif
- Expansion à 50 stations sur Conakry (6 mois)
- Extension autres villes guinéennes (12 mois)
- Déploiement régional Afrique de l'Ouest (18-24 mois)

### 5.3 Infrastructure IT
- **Hébergement** : Cloud (recommandé AWS ou Azure)
- **Serveurs** : 
  - 1 serveur API/Backend
  - 1 serveur base de données
  - 1 serveur frontend/web
  - CDN pour distribution contenu statique
- **Monitoring** : Système surveillance 24/7 (Prometheus, Grafana)
- **Backup** : Sauvegardes quotidiennes avec rétention 30 jours

---

## 6. MODÈLE ÉCONOMIQUE

### 6.1 Sources de revenus

#### 6.1.1 Abonnements
- **Grand public** : 5-10 USD/mois (accès données détaillées)
- **ONG/Associations** : 100-300 USD/mois (rapports + API)
- **Municipalités** : 500-2000 USD/mois selon taille ville
- **Entreprises** : 300-1000 USD/mois (conformité environnementale)

#### 6.1.2 Rapports personnalisés
- Rapport ponctuel basique : 200-500 USD
- Étude approfondie : 1000-5000 USD
- Étude d'impact environnemental : 5000-20000 USD

#### 6.1.3 Services additionnels
- Installation et maintenance stations
- Consulting en qualité de l'air
- Formation personnel (ONG, administrations)
- API premium pour intégration tierce

### 6.2 Clients cibles

**Primaires**
- Ministères de l'Environnement et de la Santé
- Municipalités et collectivités locales
- ONG environnementales internationales (WWF, Greenpeace, etc.)
- Organisations de santé publique (OMS, CDC)

**Secondaires**
- Entreprises soumises à réglementations environnementales
- Promoteurs immobiliers
- Médias et journalistes
- Chercheurs et universités
- Citoyens sensibilisés

### 6.3 Projections financières (à affiner)
- **Revenus année 1** : 50 000 - 100 000 USD
- **Revenus année 2** : 200 000 - 400 000 USD
- **Revenus année 3** : 500 000 - 1 000 000 USD

---

## 7. PLANNING PRÉVISIONNEL

### Phase 1 : Développement et prototypage (Mois 1-3)
- Sélection et commande composants
- Développement code embarqué stations
- Développement backend et API
- Développement interface web version 1
- Tests en laboratoire

### Phase 2 : Tests et validation (Mois 4)
- Installation stations pilotes
- Tests terrain
- Corrections bugs
- Optimisations

### Phase 3 : Déploiement pilote (Mois 5-7)
- Déploiement 10-15 stations à Conakry
- Monitoring intensif
- Formation équipe maintenance
- Démonstrations clients potentiels

### Phase 4 : Commercialisation (Mois 8+)
- Prospection clients
- Signature premiers contrats
- Extension réseau selon demande
- Améliorations continues

---

## 8. RESSOURCES NÉCESSAIRES

### 8.1 Ressources humaines

**Équipe technique (core)**
- 1 Chef de projet / Product Owner
- 1-2 Développeurs backend Python
- 1 Développeur frontend (React/Vue)
- 1 Ingénieur électronique/IoT
- 1 Data scientist (temps partiel)

**Support et opérations**
- 1-2 Techniciens terrain (installation/maintenance)
- 1 Chargé de clientèle / Commercial
- Support externe : Expert qualité de l'air (consultant)

### 8.2 Budget estimatif

**Développement initial**
- Matériel prototype (10 stations) : 5 000 - 8 000 USD
- Développement logiciel : 15 000 - 30 000 USD
- Infrastructure cloud (1 an) : 2 000 - 5 000 USD
- Tests et certifications : 2 000 - 5 000 USD
- **Total phase développement** : 24 000 - 48 000 USD

**Déploiement et opérations (année 1)**
- Stations supplémentaires (40 unités) : 20 000 - 35 000 USD
- Salaires équipe : 50 000 - 100 000 USD
- Marketing et commercialisation : 10 000 - 20 000 USD
- Frais généraux : 10 000 - 20 000 USD
- **Total année 1** : 90 000 - 175 000 USD

---

## 9. RISQUES ET MITIGATION

### 9.1 Risques techniques
| Risque | Impact | Probabilité | Mitigation |
|--------|--------|-------------|------------|
| Défaillance capteurs | Élevé | Moyen | Redondance capteurs, monitoring actif |
| Problèmes connectivité | Élevé | Élevé | Stockage local tampon, multi-opérateurs |
| Vandalisme stations | Moyen | Moyen | Boîtiers robustes, installations sécurisées, assurance |
| Cyberattaques | Élevé | Faible | Sécurité multicouche, audits réguliers |

### 9.2 Risques commerciaux
| Risque | Impact | Probabilité | Mitigation |
|--------|--------|-------------|------------|
| Manque de clients payants | Élevé | Moyen | Partenariats ONG, subventions, freemium |
| Concurrence | Moyen | Faible | Innovation continue, ancrage local |
| Réglementation défavorable | Moyen | Faible | Veille juridique, conformité proactive |

### 9.3 Risques opérationnels
| Risque | Impact | Probabilité | Mitigation |
|--------|--------|-------------|------------|
| Manque de compétences locales | Moyen | Moyen | Formation, documentation, support externe |
| Coûts maintenance élevés | Moyen | Moyen | Conception modulaire, pièces standard |

---

## 10. CRITÈRES DE SUCCÈS

### 10.1 Indicateurs techniques
- 90%+ de disponibilité des stations
- Moins de 5% de données manquantes/erronées
- Temps de réponse système < 2 secondes

### 10.2 Indicateurs commerciaux
- Minimum 5 clients payants après 12 mois
- Revenus récurrents > 50 000 USD/an fin année 1
- Taux de rétention clients > 80%

### 10.3 Indicateurs d'impact
- Couverture d'au moins 80% de la zone urbaine ciblée
- Utilisation des données par autorités locales pour décisions
- Sensibilisation de 10 000+ citoyens via plateforme
- Publication d'au moins 1 étude académique basée sur données

---

## 11. LIVRABLES ATTENDUS

### 11.1 Matériel
- 10 stations de mesure fonctionnelles (prototype)
- Documentation technique hardware
- Schémas électroniques et PCB designs

### 11.2 Logiciel
- Code source complet (GitHub privé)
- API REST documentée (Swagger/OpenAPI)
- Interface web responsive
- Application mobile (optionnelle phase 2)
- Scripts de déploiement et maintenance

### 11.3 Documentation
- Guide d'installation stations
- Manuel d'utilisation plateforme web
- Documentation API pour développeurs
- Guide de maintenance et troubleshooting
- Rapports de tests et validation

### 11.4 Formation
- Sessions de formation équipe technique
- Matériel de formation utilisateurs finaux
- Vidéos tutoriels

---

## 12. SUPPORT ET MAINTENANCE

### 12.1 Support technique
- Hotline/Email support 5j/7
- Temps de réponse : < 4h pour clients premium
- Intervention terrain : < 48h zone urbaine

### 12.2 Maintenance préventive
- Inspection visuelle stations : trimestrielle
- Calibration capteurs : semestrielle
- Mise à jour logicielle : mensuelle
- Backup et tests restauration : hebdomadaire

### 12.3 Garantie
- Stations : 1 an pièces et main d'œuvre
- Logiciel : Corrections bugs illimitées
- Support : Selon niveau abonnement

---

## 13. ÉVOLUTIONS FUTURES

### Phase 2 (12-18 mois)
- Application mobile iOS/Android
- Prévisions qualité de l'air (Machine Learning)
- Intégration données météo externes
- Alertes géolocalisées push

### Phase 3 (18-24 mois)
- Analyse prédictive avancée (Deep Learning)
- Corrélation avec données santé publique
- Expansion autres pays africains
- Capteurs additionnels (bruit, UV, pollens)

### Phase 4 (24+ mois)
- Plateforme white-label pour autres villes
- Marketplace de données environnementales
- Intégration smart city
- Programme citoyens scientifiques (capteurs personnels)

---

## 14. ANNEXES

### 14.1 Standards et normes de référence
- Indices de qualité de l'air : WHO Air Quality Guidelines
- Protocoles de mesure : EPA Quality Assurance Handbook
- Sécurité IoT : OWASP IoT Top 10
- Protection données : RGPD (si applicable)

### 14.2 Technologies alternatives envisagées
- **Microcontrôleurs** : Arduino Mega, STM32
- **Protocoles communication** : LoRaWAN, Sigfox (zones rurales)
- **Base de données** : InfluxDB (time-series), MongoDB
- **Carto** : Google Maps API, OpenStreetMap

### 14.3 Partenaires potentiels
- Universités locales (recherche, validation scientifique)
- Fournisseurs télécoms (connectivité, partenariats)
- ONG environnementales (financement, déploiement)
- Gouvernements (subventions, cadre réglementaire)

---

## 15. CONTACTS ET VALIDATION

**Préparé par** : Group4  
**Date** : Janvier 2026  
**Version** : 1.0  

**Destinataire** : Antigravity

**Signatures**

Chef de projet : _____________________ Date : _____

Client/Partenaire : _____________________ Date : _____

---

*Ce cahier des charges est un document de travail susceptible d'évoluer selon les retours d'Antigravity et les résultats des phases de faisabilité technique et commerciale.*