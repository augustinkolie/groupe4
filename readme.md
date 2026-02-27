# CAHIER DES CHARGES : PROJET ECOWATCH

## Système de Surveillance Locale de la Qualité de l'Air

---

## 1. PRÉSENTATION DU PROJET

### 1.1 Contexte

Dans les zones urbaines d'Afrique de l'Ouest, notamment en Guinée, la pollution atmosphérique représente un enjeu de santé publique majeur. L'absence de données précises et localisées empêche les autorités et les citoyens de prendre des mesures adaptées pour protéger la population.

### 1.2 Objectif général

Développer un système de surveillance environnementale complet permettant la collecte, l'analyse et la visualisation en temps réel des données de qualité de l'air, afin de fournir des outils d'aide à la décision pour les institutions et les citoyens.

### 1.3 Portée du projet

EcoWatch déploie un réseau de capteurs connectés capables de mesurer divers polluants atmosphériques et de transmettre ces données vers une plateforme web centralisée et interactive.

---

## 2. DESCRIPTION DE LA SOLUTION

### 2.1 Vue d'ensemble

La solution repose sur un écosystème IoT structuré autour de quatre piliers :

- Des stations de mesure (physiques ou virtuelles via API).
- Un protocole de transmission de données sécurisé.
- Une plateforme web d'administration et de visualisation.
- Un module d'intelligence artificielle pour l'interprétation des données.

### 2.2 Architecture technique

#### 2.2.1 Composante Hardware

Les stations de mesure utilisent des microcontrôleurs de type ESP32 ou Raspberry Pi Pico W, équipés de capteurs de particules fines (PM2.5, PM10), de monoxyde de carbone (CO) et de paramètres environnementaux (température, humidité). L'alimentation est prévue pour être autonome via des panneaux solaires.

#### 2.2.2 Composante Software

Le backend est développé en Python avec le framework Django, utilisant une base de données SQLite (extensible vers PostgreSQL). Le frontend utilise JavaScript avec des bibliothèques telles que Leaflet.js pour la cartographie et Chart.js pour les graphiques. L'intelligence artificielle intégrée traite les tendances pour fournir des recommandations automatiques.

---

## 3. SPÉCIFICATIONS FONCTIONNELLES

### 3.1 Collecte et ingestion des données

Le système permet la récupération automatique des données toutes les 10 à 15 minutes. L'ingestion est actuellement opérationnelle via l'API OpenWeather, permettant une couverture immédiate des zones urbaines ciblées.

### 3.2 Traitement et analyse

Le moteur de calcul transforme les mesures brutes en Indices de Qualité de l'Air (AQI) selon les standards internationaux. Un module d'intelligence artificielle nommé "EcoWatch Intelligence" analyse les tendances pour générer des extraits textuels explicatifs et des conseils de santé.

### 3.3 Visualisation et reporting

La plateforme propose :

- Une carte interactive affichant l'état des stations.
- Un tableau de bord détaillé par station avec graphiques historiques.
- Un générateur de rapports professionnels au format PDF.
- Un outil d'exportation des données brutes en format Excel (XLSX).

### 3.4 Système d'alertes

Le système surveille les dépassements de seuils critiques. Des notifications sont générées sur le tableau de bord et envoyées par email aux administrateurs.

---

## 4. ÉTAT D'AVANCEMENT ET ROADMAP

### 4.1 Fonctionnalités implémentées

- Plateforme web complète (Dashboard, Cartographie).
- Ingestion des données via API OpenWeather.
- Module d'IA pour les insights automatiques.
- Génération de rapports PDF et exports Excel.
- Gestion des utilisateurs et des stations.

### 4.2 Fonctionnalités en cours de développement

- Automatisation de l'envoi périodique des rapports par email.
- Affinage des algorithmes de détection d'anomalies.

### 4.3 Évolutions prévues (Roadmap)

- Intégration de l'API Twilio pour les alertes par SMS réelles.
- Développement d'une application mobile native.
- Ajout de modèles de prédiction à 24 et 48 heures via Machine Learning.
- Superposition de couches cartographiques (trafic, densité de population).

---

## 5. SPÉCIFICATIONS TECHNIQUES

### 5.1 Performance

- Temps de réponse de l'interface inférieur à 2 secondes.
- Mise à jour des données toutes les 10 minutes.
- Disponibilité du système visée à 99,9%.

### 5.2 Sécurité

- Chiffrement des communications via HTTPS.
- Protection contre les injections SQL et les failles XSS (sécurité native Django).
- Gestion des accès par rôles (Public, Administrateur).

---

## 6. DÉPLOIEMENT ET INFRASTRUCTURE

Le déploiement initial est prévu sur des serveurs cloud avec une architecture permettant une scalabilité horizontale pour supporter l'ajout de centaines de stations sans dégradation des performances.

---

## 7. MODÈLE ÉCONOMIQUE

EcoWatch propose un modèle basé sur la valorisation de la donnée :

- Accès public gratuit pour la consultation temps réel.
- Abonnements premium pour les ONG, entreprises et municipalités (accès aux rapports détaillés, API, alertes avancées).

---

## 8. PLANNING PRÉVISIONNEL

Le projet suit un cycle de développement agile :

- Phase 1 : Prototypage et socle technique (Terminé).
- Phase 2 : Tests pilotes et IA (En cours).
- Phase 3 : Commercialisation et extension régionale (Prévu 2026-2027).

---

## 9. RESSOURCES NÉCESSAIRES

- Développement technique : Développeurs Python/Django, experts IoT.
- Infrastructure : Serveurs de base de données, services d'IA générative.
- Opérations : Techniciens pour le déploiement des stations physiques.

---

## 10. RISQUES ET MITIGATION

Les principaux risques identifiés incluent la fiabilité du réseau de communication et la calibration des capteurs. Ces risques sont mitigés par l'utilisation de données satellites de référence et le stockage tampon local des données en cas de coupure réseau.

---

## 11. CRITÈRES DE SUCCÈS

- Précision des mesures comparée aux standards de référence.
- Taux d'utilisation de la plateforme par les partenaires institutionnels.
- Nombre de rapports générés et exploités pour des politiques publiques.

---

## 12. LIVRABLES ATTENDUS

- Code source complet de la plateforme.
- Documentation technique et manuels d'utilisation.
- Prototypes fonctionnels de stations de mesure.
- Cahier des charges et rapports de tests.

---

## 13. SUPPORT ET MAINTENANCE

Le support inclut la maintenance corrective du logiciel ainsi que le suivi régulier du bon fonctionnement des scripts de synchronisation des données.

---

## 14. ANNEXES

Des documents complémentaires tels que le guide d'installation, les schémas d'architecture et les pitchs commerciaux sont disponibles dans les fichiers joints au projet.

---

## 15. CONTACTS ET VALIDATION

Préparé par : Équipe Group4  
Date : 27 février 2026  
Version : 1.3

---
