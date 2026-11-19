# Compte Rendu d'Avancement — Projet DevSecOps CI/CD Platform

**École Hassania des Travaux Publics (EHTP)** — Casablanca  
**Cycle Ingénieur** : Génie Informatique (Promotion 2026–2027)  
**Étudiant** : AMHIDI Hamza  
**Projet** : Plateforme DevSecOps de Sécurité CI/CD, Déploiement Kubernetes et Supervision SOC  
**Dépôt GitHub** : [echoenvoy/SecOps-Pipeline](https://github.com/echoenvoy/SecOps-Pipeline)  
**Date du rapport** : 07 Octobre 2026  

---

## 1. Travaux Réalisés la Semaine Dernière : Phase 0 (Environnement & Dépôt)

*L'objectif de cette phase initiale était de poser le socle technique, de valider les outils conteneurs et Kubernetes, et d'établir la structure de gouvernance du projet.*

### Tâches accomplies :
1. **Activation et Vérification de l'Environnement Docker** :
   - Démarrage du démon Docker via Docker Desktop sous Windows/WSL2.
   - Validation de la disponibilité du moteur Docker (`v29.5.3`) et de Docker Compose (`v5.1.4`).
2. **Création du Réseau de Sécurité Dédié** :
   - Mise en place du réseau bridge isolé `devsecops-net` (`172.20.0.0/16`).
   - But : Permettre aux futurs services de supervision (Wazuh, ELK, TheHive) et aux applications de dialoguer de manière sécurisée sans exposition publique superflue.
3. **Provisionnement du Cluster Kubernetes Local (`kind`)** :
   - Installation de la CLI `kind v0.33.0` via le gestionnaire de paquets Windows (`winget`).
   - Déploiement d'un cluster Kubernetes local nommé `devsecops-lab` (version `v1.37.0`, nœud `kindest/node`).
   - Raccordement du conteneur du cluster au réseau `devsecops-net` (`IP: 172.20.0.2`).
   - Vérification du bon fonctionnement via `kubectl get nodes` (statut **Ready**).
4. **Initialisation de l'Arborescence Modulaire du Dépôt** :
   - Création des dossiers du cycle complet : `app/`, `docker/`, `k8s/`, `ci/`, `security/`, `monitoring/`, `ir/`, `docs/`.
   - Ajout des fichiers `.gitkeep` pour figer l'arborescence sous Git.
5. **Gouvernance Git & Documentation Initiale** :
   - Configuration du fichier [`.gitignore`](.gitignore) pour exclure caches, identifiants, tokens et artefacts temporaires.
   - Rédaction du [`README.md`](README.md) général (architecture globale Shift-Left / Shift-Right, pile technologique, feuille de route des 11 phases).
   - Création du journal chronologique de suivi [`AVANCEMENT.md`](AVANCEMENT.md).
   - Intégration du guide de contribution [`CONTRIBUTING.md`](CONTRIBUTING.md) et des templates de Pull Request et d'Issues dans [`.github/`](.github/).
6. **Publication Git** :
   - Rebase sur `origin/main` et synchronisation du commit initial sur GitHub.

---

## 2. Travaux Réalisés Aujourd'hui : Phase 1 (Application Cible & Dockerisation)

*L'objectif d'aujourd'hui était de développer l'application web cible avec un jeu de vulnérabilités intentionnelles documentées, de la packager dans une image Docker sécurisée (non-root) et de valider son fonctionnement par une suite de tests automatisée.*

### Tâches accomplies :
1. **Création de la Branche de Fonctionnalité** :
   - Création et basculement vers la branche `feat/phase-1-target-app` selon le workflow GitHub Flow.
2. **Développement de l'Application Cible (`app/`)** :
   - Microservice web développé en Python avec **Flask** (`app/app.py`).
   - Base de données locale SQLite initialisée (`app/database.py`) avec tables `users`, `notes` et `audit_logs`.
   - Comptes de test pré-alimentés (`admin`, `alice`, `bob`) et notes confidentielles.
   - Interface utilisateur web légère (`app/templates/`) pour tester visuellement les fonctionnalités.
3. **Implémentation des 5 Vulnérabilités Intentionnelles** :
   - **VULN-01 (Injection SQL)** : Requêtes construites par concaténation de chaînes brutes dans l'authentification et la recherche (`/api/search`). Permet le contournement d'authentification avec `' OR 1=1 --` et l'exfiltration de la table des utilisateurs.
   - **VULN-02 (XSS Réfléchi)** : Rendu de template dynamique non échappé sur `/api/greet` via `render_template_string` et filtre Jinja2 `| safe`.
   - **VULN-03 (Secrets en clair)** : Présence de clés secrètes et de jetons codés en dur dans `app/config.py`.
   - **VULN-04 (IDOR)** : Absence de contrôle de propriété sur `/api/notes/<id>` permettant à un utilisateur d'accéder aux données privées d'un autre sans autorisation.
   - **VULN-05 (Cryptographie Faible)** : Recours à l'algorithme obsolète MD5 pour le hachage des mots de passe (`/api/hash`).
4. **Télémétrie et Journalisation Structurée pour Wazuh** :
   - Ajout d'un formateur de log émettant des événements d'authentification structurés en JSON : `[AUTH_SUCCESS]` et `[AUTH_FAILURE]`.
   - Ces logs constituent la matière première requise pour déclencher les alertes Wazuh de détection d'attaques brute-force (Phase 6).
5. **Rédaction du Registre Documentaire des Failles (`docs/vulnerabilities.md`)** :
   - Fiche d'identité complète pour chaque vulnérabilité : identifiant (VULN-01 à 05), référence CWE, catégorie OWASP Top 10, lignes de code concernées, commande de démonstration cURL (PoC) et méthode de remédiation recommandée.
6. **Conteneurisation Docker Durcie (`docker/Dockerfile`)** :
   - Image de base minimale et épinglée : `python:3.12-slim`.
   - Création et attribution des privilèges à un utilisateur système non-root : `appuser` (UID 1000).
   - Optimisation du cache des calques avec `--no-cache-dir`.
   - Intégration d'une directive `HEALTHCHECK` périodique vérifiant l'endpoint `/health`.
   - Configuration du fichier [`.dockerignore`](.dockerignore) pour exclure les fichiers inutiles du build.
7. **Campagne de Tests & Validation Technique** :
   - Création de la suite de tests automatisée [`tests/test_endpoints.py`](tests/test_endpoints.py).
   - Exécution des tests directement à l'intérieur du conteneur Docker en cours d'exécution sur le réseau `devsecops-net` :
     - Sonde de santé `/health` : **100% PASS** (HTTP 200 `status: UP`).
     - Non-root user (`whoami`) : **100% PASS** (`appuser`).
     - Bypass Injection SQL : **100% PASS**.
     - Extraction Injection SQL : **100% PASS** (3 comptes extraits).
     - Déclenchement XSS : **100% PASS** (balise script reflétée).
     - Déclenchement IDOR : **100% PASS** (note financière privée de Bob récupérée sans droits).
     - Hachage MD5 : **100% PASS**.
     - Télémétrie brute-force : **100% PASS** (code 401 et log `[AUTH_FAILURE]` émis).
8. **Mise à Jour du Journal & Push GitHub** :
   - Mise à jour de [`AVANCEMENT.md`](AVANCEMENT.md) attestant de l'achèvement de la Phase 1.
   - Commit et push de la branche `feat/phase-1-target-app` sur GitHub (`origin/feat/phase-1-target-app`).

---

## 3. Synthèse des Livrables Disponibles

| Composant | Fichiers associés | État |
|---|---|:---:|
| **Application web** | `app/app.py`, `app/database.py`, `app/config.py`, `app/requirements.txt` | Opérationnelle |
| **Interfaces web** | `app/templates/base.html`, `login.html`, `index.html` | Opérationnelles |
| **Conteneurisation** | `docker/Dockerfile`, `.dockerignore` | Build & Test validés |
| **Tests de validation**| `tests/test_endpoints.py` | 7/7 tests réussis |
| **Documentation failles** | `docs/vulnerabilities.md` | Exhaustive |
| **Suivi d'avancement** | `AVANCEMENT.md` | À jour (Phases 0 et 1 validées) |
| **Branche GitHub** | `feat/phase-1-target-app` | Pushée sur GitHub (prête pour PR) |

---

## 4. Prochaine Étape

- **Phase 2 — Squelette du Pipeline CI/CD** : Mettre en place la chaîne d'intégration continue automatisée (avec les 4 étapes : SAST $\rightarrow$ Quality Gate $\rightarrow$ Build conteneur $\rightarrow$ Déploiement Kubernetes).
