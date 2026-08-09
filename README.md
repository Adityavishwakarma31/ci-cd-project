# Ledger — CI/CD Pipeline for Django Todo App

A fully automated CI/CD pipeline that takes a Django Todo App from a `git push` to a live deployment on Kubernetes — no manual steps in between.

**Live pipeline flow:**
`GitHub Push → Jenkins → Docker Build & Test → Docker Hub → K8s Manifest Update → kubectl Deploy`

📦 **K8s Manifest Repo:** [github.com/Adityavishwakarma31/k8s-manifest](https://github.com/Adityavishwakarma31/k8s-manifest)

---

## 🔗 Related Repositories

| Repo | Description |
|---|---|
| [`ci-cd-project`](https://github.com/Adityavishwakarma31/ci-cd-project) | Django Todo App source code + Jenkinsfile |
| [`k8s-manifest`](https://github.com/Adityavishwakarma31/k8s-manifest) | Kubernetes deployment & service manifests (GitOps-lite) |

---

## 🏗️ Architecture

```
Developer                Jenkins (EC2 Agent)              Docker Hub          k8s-manifest repo         Kubernetes Cluster
    │                          │                                │                     │                        │
    ├─ git push ──────────────▶│                                │                     │                        │
    │                          ├─ Fetch (Checkout SCM)          │                     │                        │
    │                          ├─ Build (docker build)          │                     │                        │
    │                          ├─ Test (run + curl + teardown)  │                     │                        │
    │                          ├─ Push ────────────────────────▶│                     │                        │
    │                          ├─ Update Manifests ─────────────┼────────────────────▶│                        │
    │                          └─ Deploy (kubectl apply) ────────┼─────────────────────┼───────────────────────▶│
```

---

## ⚙️ Pipeline Stages

The pipeline is defined in [`jenkins/jenkinsfile`](https://github.com/Adityavishwakarma31/ci-cd-project/blob/main/jenkins/jenkinsfile) and runs on a dedicated Jenkins EC2 agent (`ec2-agent`).

1. **Fetching** — Clones the app source from `ci-cd-project` (GitHub credentials via Jenkins `github-id`).
2. **Building** — Builds the Docker image, tagged with the Jenkins `BUILD_NUMBER`.
   ```bash
   docker build -t django-todo-app:${BUILD_NUMBER} .
   ```
3. **Testing** — Spins up a temporary container, hits it with `curl`, then tears it down.
   ```bash
   docker run -d --name testapp -p 8000:8000 django-todo-app:${BUILD_NUMBER}
   curl http://localhost:8000
   docker stop testapp && docker rm testapp
   ```
4. **Push** — Tags and pushes the image to Docker Hub (`adityavishwakarma31/django-todo-app`) using Jenkins `docker-cred`.
5. **Update Manifests** — Clones the `k8s-manifest` repo, updates the image tag in `deployment.yaml` with `sed`, commits, and pushes back (using `github-pat` credentials).
6. **Deployment** — Applies the updated manifests directly to the cluster.
   ```bash
   kubectl apply -f deployment.yaml
   kubectl apply -f service.yaml
   ```

---

## ☸️ Kubernetes Resources

**`deployment.yaml`**
- 2 replicas of the Django Todo App
- Resource requests/limits set (CPU: 100m–300m, Memory: 128Mi–256Mi)
- Container port `8000`

**`service.yaml`**
- Type: `NodePort`
- Maps port `80` → container port `8000`, exposed on `nodePort 30080`

---

## 🔐 Jenkins Credentials Used

| Credential ID | Purpose |
|---|---|
| `github-id` | Clone `ci-cd-project` repo |
| `docker-cred` | Docker Hub login for push |
| `github-pat` | Push updated manifests to `k8s-manifest` repo |
| `kubeconfig-cred` | kubectl access to the Kubernetes cluster |

---

## ✅ Verified Deployment

```bash
$ kubectl get pods
NAME                        READY   STATUS    RESTARTS   AGE
todo-app-6fdc7c847-wjnw8    1/1     Running   0          4m59s
todo-app-6fdc7c847-zg9ct    1/1     Running   0          4m52s
```

---

## 🧭 Roadmap / Improvements

- [ ] Replace the static EC2 Jenkins agent with **ephemeral Docker container agents** — spin up for build/push, tear down automatically after.
- [ ] Adopt **ArgoCD** for delivery/deployment instead of Jenkins directly running `kubectl apply` — move to a proper pull-based GitOps model.
- [ ] Revisit the separate `k8s-manifest` repo pattern — the CI job's commit-back can retrigger its own webhook and create a pipeline loop if not filtered/guarded properly.
- [ ] Test orchestration on AWS EKS (currently validated locally on minikube/kind for cost efficiency).

---

## 🛠️ Tech Stack

`Django` · `Docker` · `Jenkins` · `Kubernetes` · `kubectl` · `AWS EC2` · `GitHub`

---

## Notes for deployment
- Uses `gunicorn` as the production WSGI server (not Django's dev server) inside Docker.
- Uses `whitenoise` to serve static files directly from the container — no need for nginx for a simple deployment.
- SQLite is used by default (fine for a portfolio/demo project). For production, swap in Postgres via `DATABASES` in `settings.py`.
- `ALLOWED_HOSTS = ['*']` is set for demo convenience — restrict this to your actual domain in real production.
