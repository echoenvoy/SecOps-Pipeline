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
| **Phase 1** | Application cible vulnérable et conteneurisation Docker | À venir | — |
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
- **Phase 1** : Conception et développement de l'application cible avec vulnérabilités intentionnelles documentées (SQLi, XSS, Secret codé en dur, IDOR), rédaction du Dockerfile durci et création du fichier de référence `docs/vulnerabilities.md`.
