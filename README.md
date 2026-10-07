# DevSecOps CI/CD Security & Monitoring Platform

**École Hassania des Travaux Publics (EHTP)** — Computer Engineering  
*Prepared by: Amhidi Hamza*  
*Academic Year: 2026–2027*

---

## 1. Project Overview

Modern software development demands rapid deployment through CI/CD pipelines without compromising application security. This project demonstrates a complete end-to-end DevSecOps lifecycle connecting:
1. **Shift-Left Security**: Static Application Security Testing (SAST) and automated Quality & Security Gates preventing vulnerable code from reaching production.
2. **Containerized Orchestration**: Automated container build (Docker) and cluster deployment (Kubernetes).
3. **Shift-Right Security Operations (SOC)**: Continuous runtime monitoring (Wazuh HIDS/SIEM), centralized log analytics and dashboarding (Elastic Stack / ELK), and structured Incident Response and Case Management (TheHive).

```
[Developer] 
    │
    ▼ (git push)
[CI/CD Pipeline]
    ├── Stage 1: SAST (Semgrep) ─────────────► [Blocks Vulnerable Code]
    ├── Stage 2: Quality Gate (SonarQube) ───► [Enforces Code & Security Standards]
    ├── Stage 3: Container Build (Docker) ───► [Builds Minimal, Non-Root Image]
    └── Stage 4: Orchestration (Kubernetes) ─► [Deploys to Cluster]
                                                       │
                                                       ▼
                                            [Runtime Environment]
                                                       │
                                                       ▼ (File changes, Brute-force attacks)
                                            [Wazuh Agent & Manager]
                                                       │
                                                       ▼ (Alert forwarding)
                                            [Elasticsearch & Kibana]
                                                       │
                                                       ▼ (Qualified Alerts / Connector)
                                            [TheHive Incident Response]
```

---

## 2. Technology Stack

| Layer | Technology | Purpose |
|---|---|---|
| **Target Application** | Python (Flask) / Node.js | Microservice with intentional, documented vulnerabilities |
| **Containerization** | Docker | Minimal, pinned base images, non-root user execution |
| **Orchestration** | Kubernetes (Docker Desktop / kind) | Declarative deployment manifests, cluster isolation |
| **Version Control & CI** | Git & CI Runner | Pipeline automation on push/merge requests |
| **SAST** | Semgrep | Pattern-matched vulnerability scanning (OWASP Top 10) |
| **Quality & Security Gate** | SonarQube | Code smells, security hotspots, quality gate enforcement |
| **Runtime HIDS / SIEM** | Wazuh | Log analysis, File Integrity Monitoring (FIM), anomaly detection |
| **Log Analytics** | Elastic Stack (ELK) | Centralized log indexing, search, and Kibana dashboards |
| **Incident Response** | TheHive | Case management, observable enrichment, task tracking |

---

## 3. Repository Structure

```text
devsecops-platform/
├── app/                  # Target application source code
├── docker/               # Dockerfiles and container configurations
├── k8s/                  # Kubernetes manifests (Deployment, Service, ConfigMap/Secret)
├── ci/                   # CI/CD pipeline definition files
├── security/
│   ├── semgrep/          # Custom Semgrep rules and scan policies
│   └── sonar/            # sonar-project.properties and quality gate configs
├── monitoring/
│   ├── wazuh/            # Wazuh manager and agent configurations (ossec.conf, rules)
│   └── elk/              # Elasticsearch, Logstash/Filebeat, and exported Kibana dashboards
├── ir/
│   └── thehive/          # TheHive configuration, case templates, and automation connector
├── docs/                 # Architectural diagrams, vulnerability inventory, IR runbook
└── Documentation/        # Official academic specification and detailed implementation plan
```

---

## 4. Implementation Roadmap (11 Phases)

- [x] **Phase 0 — Environment and Repository Setup**: Scaffolding, container networks, toolchain verification.
- [x] **Phase 1 — Target Application and Dockerization**: Web application with documented vulnerabilities and secure Dockerfile.
- [ ] **Phase 2 — CI/CD Pipeline Skeleton**: Multi-stage automated pipeline runner.
- [ ] **Phase 3 — SAST Integration with Semgrep**: Pipeline gate failing on high-severity vulnerabilities.
- [ ] **Phase 4 — Code Quality Gate with SonarQube**: Complementary quality & security hotspot checks.
- [ ] **Phase 5 — Containerized Build and Kubernetes Deployment**: Automated image build and Kubernetes deployment.
- [ ] **Phase 6 — Wazuh Runtime Monitoring**: Wazuh agent/manager deployment, FIM, and brute-force detection.
- [ ] **Phase 7 — Elastic Stack Integration**: Log centralization, indexing, and SOC Kibana dashboards.
- [ ] **Phase 8 — Incident Response with TheHive**: Case management workflow from qualified alerts.
- [ ] **Phase 9 — Alert-to-Case Automation (Optional)**: Connector script bridging alerts into TheHive cases.
- [ ] **Phase 10 — End-to-End Demonstration and Documentation**: Full before/after rehearsal, walkthrough, and demo recording.

> 📋 **Suivi d'avancement détaillé** : Consultez le fichier [AVANCEMENT.md](file:///c:/Users/Hamza/Downloads/projet%20s5/AVANCEMENT.md) pour le journal chronologique complet de chaque phase, les commandes exécutées et les résultats de validation.

---

## 5. Phase 0 Validation Checkpoint

To verify the setup:
1. Docker daemon active: `docker ps`
2. Dedicated network available: `docker network ls` (includes `devsecops-net`)
3. Kubernetes cluster available: `kubectl get nodes`
4. Repository committed: `git log`
