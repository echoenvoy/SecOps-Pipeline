# Journal d'Avancement du Projet — DevSecOps CI/CD Platform

**École Hassania des Travaux Publics (EHTP)** — Casablanca  
**Cycle Ingénieur** : Génie Informatique  
**Auteur** : Amhidi Hamza  
**Projet** : Plateforme DevSecOps de Sécurité CI/CD, Orchestration et Supervision SOC (SAST, K8s, Wazuh, ELK, TheHive)  
**Dépôt GitHub** : [echoenvoy/SecOps-Pipeline](https://github.com/echoenvoy/SecOps-Pipeline)  
**Dernière mise à jour** : 30 Septembre 2026  

---

## Tableau de Bord Global des Phases

| Phase | Intitulé | Statut | Date de Réalisation |
| :---: | :--- | :---: | :---: |
| **Phase 0** | **Mise en place de l'environnement et du dépôt Git** | **TERMINÉ** | 30/09/2026 |
| **Phase 1** | **Application cible vulnérable et conteneurisation Docker** | **TERMINÉ** | 07/10/2026 |
| **Phase 2** | Squelette du pipeline CI/CD | À venir | — |
| **Phase 3** | Intégration SAST avec Semgrep | À venir | — |
| **Phase 4** | Gate de qualité et sécurité avec SonarQube | À venir | — |
| **Phase 5** | Build conteneurisé et déploiement Kubernetes | À venir | — |
| **Phase 6** | Surveillance Runtime et HIDS avec Wazuh | À venir | — |
| **Phase 7** | Centralisation des logs et tableaux de bord ELK | À venir | — |
| **Phase 8** | Gestion d'incidents avec TheHive | À venir | — |
| **Phase 9** | Automatisation Alert-to-Case (Optionnel) | À venir | — |
| **Phase 10**| Démonstration de bout en bout et rapport final | À venir | — |

---

## Détails des Réalisations par Phase

---

### Phase 0 — Environnement et Initialisation du Dépôt (30/09/2026)

#### 1. Objectif de la Phase
Préparer la machine hôte locale, vérifier la chaîne d'outils (Docker, Kubernetes, kubectl, Git), configurer le réseau conteneur dédié et établir l'arborescence complète du projet conformément aux spécifications techniques.

---

#### 2. Actions Réalisées en Détail

##### A. Diagnostic et Activation de l'Environnement Docker
- **Diagnostic initial** : Détection du client Docker (`v29.5.3`) et de Docker Compose (`v5.1.4`) sur l'hôte Windows avec sous-système WSL2 (`kali-linux` et `docker-desktop`). Le démon Docker était arrêté.
- **Démarrage du service** : Lancement de l'exécutable Docker Desktop (`C:\Program Files\Docker\Docker\Docker Desktop.exe`).
- **Validation** : Confirmation de la disponibilité du démon via `docker info` et `docker ps`.

##### B. Configuration du Réseau Conteneur Dédié
- **Création du réseau** : Création d'un réseau bridge Docker isolé nommé `devsecops-net` :
  ```powershell
  docker network create devsecops-net
  ```
- **Caractéristiques du réseau** :
  - Nom : `devsecops-net`
  - Driver : `bridge`
  - Sous-réseau alloué : `172.20.0.0/16`
  - Passerelle : `172.20.0.1`
- **Objectif** : Permettre aux futurs conteneurs (Registre local, Wazuh Manager, Elasticsearch/Logstash/Kibana, TheHive) de communiquer de façon isolée sans exposer inutilement leurs ports sur le réseau public.

##### C. Provisionnement du Cluster Kubernetes Local
- **Outil retenu** : `kind` (Kubernetes in Docker), aligné avec les recommandations du plan d'implémentation.
- **Installation** : Déploiement de `kind v0.33.0` via le gestionnaire de paquets Windows (`winget install --id Kubernetes.kind`).
- **Création du cluster** :
  ```powershell
  kind create cluster --name devsecops-lab
  ```
  - Téléchargement et extraction de l'image de nœud Kubernetes `kindest/node:v1.37.0`.
  - Démarrage et initialisation du plan de contrôle (`control-plane`).
  - Déploiement du CNI (Container Network Interface) et de la StorageClass locale.
  - Configuration automatique du contexte `kubectl` vers `kind-devsecops-lab`.
- **Raccordement réseau** : Connexion du conteneur de nœud Kubernetes au réseau `devsecops-net` :
  ```powershell
  docker network connect devsecops-net devsecops-lab-control-plane
  ```
  - Adresse IP assignée au cluster sur le réseau de sécurité : `172.20.0.2`.
- **Vérification du cluster** :
  - Commande : `kubectl get nodes -o wide`
  - Résultat : Nœud `devsecops-lab-control-plane` au statut **Ready**, version **v1.37.0**, runtime `containerd://2.3.4`.

##### D. Mise en Place de l'Arborescence du Projet
Création des répertoires modulaires avec conservation sous Git via `.gitkeep` :
- `app/` : Code source de la future application cible vulnérable.
- `docker/` : Recettes Dockerfile (images sécurisées, utilisateurs non-root).
- `k8s/` : Manifestes Kubernetes déclaratifs (Deployment, Service, ConfigMap/Secret).
- `ci/` : Définitions et configurations du pipeline CI/CD.
- `security/semgrep/` : Règles personnalisées et politiques de scan SAST Semgrep.
- `security/sonar/` : Configuration `sonar-project.properties` et Quality Gates.
- `monitoring/wazuh/` : Fichiers de configuration Wazuh (`ossec.conf`, règles FIM et détection d'intrusions).
- `monitoring/elk/` : Configurations Elasticsearch, Logstash/Filebeat et dashboards Kibana exportés.
- `ir/thehive/` : Modèles de cas d'incident (case templates), connecteurs et scripts d'intégration TheHive.
- `docs/` : Documentation d'architecture, inventaire des vulnérabilités et procédures SOC.
- `Documentation/` : Conservation des documents de spécification et du plan d'implémentation originaux (`specification document.pdf`, `implementation_plan.pdf`).

##### E. Fichiers de Configuration et Documentation du Dépôt
- **Fichier `.gitignore`** : Élaboration d'un ensemble complet de règles d'exclusion pour protéger le dépôt (secrets, tokens, fichiers `.env`, caches Python/Node, logs, rapports volumineux, `.scannerwork/`, etc.).
- **Fichier `README.md`** : Rédaction complète de la documentation générale du projet (présentation, schéma d'architecture du flux Shift-Left vers Shift-Right, tableau des technologies, arborescence et statut des jalons).

##### F. Gestion de Version Git et Synchronisation GitHub
- Synchronisation avec les derniers ajouts du dépôt distant `origin/main` via `git fetch` et `git rebase origin/main`.
- Validation du commit initial :
  ```text
  Commit : 2ea2cf1
  Message : feat: initialize phase 0 repository structure, environment and documentation
  ```
- Push réussi vers la branche `main` du dépôt GitHub : `https://github.com/echoenvoy/SecOps-Pipeline`.

---

#### 3. Points de Contrôle et Validation Technique (Checkpoints)

| Critère de validation | Commande de test | Résultat obtenu | Statut |
| :--- | :--- | :--- | :---: |
| **Disponibilité Docker** | `docker ps` | Démon actif, conteneurs opérationnels | **VALIDÉ** |
| **Isolation réseau** | `docker network ls` | Réseau `devsecops-net` présent (ID `0f95507f186d`) | **VALIDÉ** |
| **Santé du cluster K8s** | `kubectl get nodes` | `devsecops-lab-control-plane` en statut **Ready** | **VALIDÉ** |
| **API Kubernetes** | `kubectl cluster-info` | Control-plane joignable sur `https://127.0.0.1:65044` | **VALIDÉ** |
| **Statut du dépôt Git** | `git status` | Branche à jour avec `origin/main`, copie de travail propre | **VALIDÉ** |

---

#### 4. Prochaine Étape
- **Phase 1** : Conception et développement de l'application cible avec vulnérabilités intentionnelles documentées, conteneurisation et validation.

---

### Phase 1 — Application Cible et Conteneurisation Docker (07/10/2026)

#### 1. Objectif de la Phase
Concevoir, implémenter et conteneuriser une application web Python/Flask dotée d'un jeu de 5 vulnérabilités intentionnelles documentées (SQLi, XSS, Secret en dur, IDOR, Hash faible), émettant des logs d'authentification structurés pour la supervision Wazuh, et packagée dans un conteneur Docker durci avec utilisateur non-root.

---

#### 2. Actions Réalisées en Détail

##### A. Création de la Branche Git
- Création et basculement vers la branche de fonctionnalité dédiée conformément au workflow GitHub Flow :
  ```bash
  git checkout -b feat/phase-1-target-app
  ```

##### B. Implémentation de l'Application Cible (`app/`)
- **Dépendances (`app/requirements.txt`)** : `Flask==3.0.3`, `Werkzeug==3.0.3`, `requests==2.32.3`, `pytest==8.2.2`.
- **Configuration (`app/config.py`)** : Définition des clés secrètes et variables d'environnement (`SECRET_KEY`, `JWT_SECRET`, `API_KEY`).
- **Base de données (`app/database.py`)** :
  - Initialisation SQLite (`devsecops.db`) avec tables `users`, `notes`, et `audit_logs`.
  - Amorçage des comptes utilisateurs de test (`admin`, `alice`, `bob`) et de notes confidentielles.
  - Implémentation de la fonction de hachage vulnérable MD5 `hash_password_insecure()`.
- **Application Web & API REST (`app/app.py`)** :
  - Endpoints REST : `/health` (Healthcheck HTTP 200), `/api/login`, `/api/search`, `/api/greet`, `/api/notes/<id>`, `/api/hash`.
  - Interface utilisateur web (`app/templates/base.html`, `login.html`, `index.html`) pour les tests visuels.
  - Générateur d'événements de journalisation structurée `log_auth_event()` produisant des logs JSON (`[AUTH_SUCCESS]`, `[AUTH_FAILURE]`) indispensables pour les futures règles de détection d'attaques brute-force sous Wazuh (Phase 6).

##### C. Jeu de Vulnérabilités Intentionnelles (`docs/vulnerabilities.md`)
Documentation rigoureuse des 5 failles selon les standards OWASP Top 10 et CWE :
1. **VULN-01 (SQL Injection)** : Concaténation de chaîne brute dans les requêtes de recherche et d'authentification (`SELECT ... WHERE username = '{username}'`). Exploitable via `' OR 1=1 --`.
2. **VULN-02 (Reflected XSS)** : Utilisation de `render_template_string` dynamique et du filtre Jinja2 `| safe` sans neutralisation des balises HTML/JS.
3. **VULN-03 (Hard-coded Secret / Token)** : Présence de jetons secrets et d'API keys en clair dans `app/config.py`.
4. **VULN-04 (IDOR - Insecure Direct Object Reference)** : Récupération de notes privées sans vérification de session ou d'appartenance utilisateur sur `/api/notes/<id>`.
5. **VULN-05 (Weak Cryptographic Hash)** : Recours à l'algorithme MD5 pour le hachage des mots de passe.

##### D. Conteneurisation Docker Durcie (`docker/Dockerfile`)
- Image de base minimale et épinglée : `python:3.12-slim`.
- Sécurité en profondeur :
  - Création d'un utilisateur système non privilégié `appuser` (UID 1000).
  - Installation sans cache avec `--no-cache-dir`.
  - Attribution des droits de propriété sur `/app` à `appuser`.
  - Instruction `USER appuser` pour interdire l'exécution en tant que root.
  - Sonde de santé intégrée (`HEALTHCHECK` via `urllib.request` sur `/health`).
- Fichier `.dockerignore` configuré pour exclure dépôts, caches, et fichiers sensibles du contexte de build.

##### E. Validation Automatisée et Tests dans le Conteneur
- Build de l'image :
  ```bash
  docker build -t target-app:dev -f docker/Dockerfile .
  ```
- Démarrage sur le réseau sécurisé `devsecops-net` :
  ```bash
  docker run -d --name target-app -p 8080:8080 --network devsecops-net target-app:dev
  ```
- Exécution de la suite de tests automatisée `tests/test_endpoints.py` directement au sein du conteneur :
  - Test 1 (Healthcheck) : `status: UP` (HTTP 200) $\rightarrow$ **PASS**
  - Test 2 (SQLi Auth Bypass) : Bypass réussi avec `' --` $\rightarrow$ **PASS**
  - Test 3 (SQLi Search) : Extraction de 3 enregistrements via injection SQL $\rightarrow$ **PASS**
  - Test 4 (Reflected XSS) : Injection de payload script reflétée non échappée $\rightarrow$ **PASS**
  - Test 5 (IDOR) : Note confidentielle de Bob récupérée sans droits $\rightarrow$ **PASS**
  - Test 6 (Weak Crypto) : Hachage MD5 (32 caractères hex) vérifié $\rightarrow$ **PASS**
  - Test 7 (Télémétrie Wazuh) : Code 401 et émission du log `[AUTH_FAILURE]` $\rightarrow$ **PASS**
  - Vérification utilisateur : `docker exec target-app whoami` renvoie `appuser` $\rightarrow$ **PASS**

---

#### 3. Points de Contrôle et Validation Technique (Checkpoints)

| Critère de validation | Commande de test | Résultat obtenu | Statut |
| :--- | :--- | :--- | :---: |
| **Démarrage conteneur** | `docker ps --filter name=target-app` | Conteneur actif (`Up (healthy)`) | **VALIDÉ** |
| **Privilèges non-root** | `docker exec target-app whoami` | Utilisateur `appuser` (UID 1000) | **VALIDÉ** |
| **Sonde Healthcheck** | `GET /health` | HTTP 200 `{"status": "UP"}` | **VALIDÉ** |
| **Déclenchement SQLi** | `POST /api/login` & `GET /api/search` | Bypass d'auth et extraction de données | **VALIDÉ** |
| **Déclenchement XSS** | `GET /api/greet?name=<script>...` | Payload reflété sans échappement | **VALIDÉ** |
| **Déclenchement IDOR** | `GET /api/notes/2` | Note d'un tiers accessible sans contrôle | **VALIDÉ** |
| **Télémétrie brute-force** | `docker logs target-app` | Événements `[AUTH_FAILURE]` en JSON | **VALIDÉ** |
| **Documentation failles** | `docs/vulnerabilities.md` | Matrice complète avec PoCs | **VALIDÉ** |

---

#### 4. Prochaine Étape
- **Phase 2** : Mise en place du squelette de pipeline CI/CD multi-étapes (`sast`, `quality-gate`, `build`, `deploy`).

