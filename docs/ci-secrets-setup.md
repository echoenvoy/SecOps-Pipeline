# CI/CD Pipeline Secrets & Environment Variables Contract

In alignment with **Phase 2 (Step 4)** of the Detailed Implementation Plan and secure DevSecOps best practices, sensitive parameters, tokens, and cluster credentials must **never be committed to Git**. Instead, they must be stored in the CI system's secret store (e.g., **GitHub Actions Secrets and Variables**).

---

## 1. Required Pipeline Secrets

| Secret Name | Purpose | Associated Stage | Production Source |
|---|---|---|---|
| `SONAR_TOKEN` | Authentication token for SonarQube Scanner CLI | `quality-gate` (Phase 4) | SonarQube Server (`Administration > Security > Users > Tokens`) |
| `SONAR_HOST_URL` | Base URL of the SonarQube server | `quality-gate` (Phase 4) | e.g. `http://sonarqube.internal:9000` or Cloud URL |
| `DOCKER_REGISTRY_USER` | Username for container registry authentication | `build` (Phase 5) | Docker Hub / Private Harbor / GitHub Container Registry |
| `DOCKER_REGISTRY_PASSWORD`| Token/Password for container registry authentication | `build` (Phase 5) | Personal Access Token (PAT) with write access |
| `KUBECONFIG` | Base64-encoded kubeconfig file for Kubernetes cluster access | `deploy` (Phase 5) | Generated via `kubectl config view --raw \| base64` |

---

## 2. Configuration in GitHub Repository Secrets

To configure these secrets on the GitHub repository:
1. Navigate to: `https://github.com/echoenvoy/SecOps-Pipeline/settings/secrets/actions`
2. Under **Repository secrets**, click **New repository secret**.
3. Add the key-value pairs matching the contract above.

---

## 3. Standard Non-Sensitive Pipeline Variables

These non-sensitive variables are declared directly within `.github/workflows/devsecops-pipeline.yml`:

```yaml
env:
  IMAGE_NAME: "target-app"
  APP_DIR: "app"
  DOCKERFILE_PATH: "docker/Dockerfile"
  K8S_DIR: "k8s"
```

---

## 4. Security Principles Enforced
- **Zero Credentials in Git**: Checked by `.gitignore` and enforced by GitHub Secret Scanning.
- **Least Privilege Access**: Dedicated service accounts for SonarQube and Kubernetes deployments.
- **Masked Logs**: GitHub Actions automatically masks values matching declared repository secrets in job execution logs.
