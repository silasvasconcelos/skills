---
name: security-check
description: >-
  Performs a comprehensive security review of code, APIs, infrastructure, or architecture
  against OWASP Top 10, CWE Top 25, and secure coding best practices. Identifies
  vulnerabilities, assigns risk severity (DREAD/CVSS), and provides actionable
  remediation guidance — language and framework agnostic. Use when the user asks for a
  security review, security audit, security analysis, vulnerability check, penetration
  test guidance, threat modeling, or mentions OWASP, CVE, injection, XSS, authentication,
  authorization, CSRF, SSRF, JWT, OAuth, cryptography, secrets, container security,
  cloud misconfiguration, GraphQL security, or secure coding.
---

# Security Check

Performs a structured security analysis based on OWASP, CWE, and secure coding
standards. Works for code snippets, full files, API definitions, infrastructure configs,
or architectural descriptions — any language, framework, or platform.

> **Timeless by design:** Vulnerability classes (injection, broken access control, crypto
> failures, etc.) and their CWE identifiers are stable, permanent references — they don't
> expire when a new OWASP edition is published. When year-specific version numbers appear
> in reference files, treat them as the snapshot used to build this knowledge base; the
> underlying principles remain valid. Always verify classification against current official
> sources (owasp.org, cwe.mitre.org) when precision matters.

**Reference files (read when needed):**
- Security resource URLs, OWASP/CWE tables, tools, SSDLC, full checklist → [references.md](references.md)
- JWT / OAuth / OIDC attack patterns → [jwt-oauth.md](jwt-oauth.md)
- Cloud, container & IaC security → [cloud-infra.md](cloud-infra.md)
- GraphQL & advanced API security → [api-graphql.md](api-graphql.md)
- Example security analysis outputs → [examples.md](examples.md)

---

## Workflow

### Step 1 — Understand Scope

| Input type | Focus areas | Read |
|---|---|---|
| **Code snippet / file** | Injection, auth, authz, crypto, session, input validation, output encoding | This file |
| **API / OpenAPI spec** | OWASP API Top 10 (BOLA, broken auth, mass assignment, rate limits) | [api-graphql.md](api-graphql.md) |
| **GraphQL schema / resolvers** | Introspection, depth limits, batch attacks, authorization per field | [api-graphql.md](api-graphql.md) |
| **JWT / OAuth flow** | alg:none, weak secrets, token theft, PKCE, scope creep | [jwt-oauth.md](jwt-oauth.md) |
| **Infrastructure / IaC** | Secrets, network exposure, IAM over-privilege, container hardening | [cloud-infra.md](cloud-infra.md) |
| **Dockerfile / K8s YAML** | Root user, privileged containers, exposed sockets, image provenance | [cloud-infra.md](cloud-infra.md) |
| **Architecture / DFD** | STRIDE threat modeling — trust boundaries, data flows, attack surface | This file |
| **Dependencies / lockfile** | Vulnerable components (SCA) — CWE-1104, CVE lookup | This file |

### Step 2 — Apply Security Lenses

Check in order of typical severity:

1. **Injection** — SQL, XSS, OS Command, LDAP, SSTI, XXE, path traversal (CWE-89, -79, -78, -22, -94)
2. **Broken Access Control** — IDOR, missing authz, privilege escalation (CWE-862, -639)
3. **Cryptographic Failures** — weak hashing, cleartext, weak keys, bad random (CWE-327, -331, -338)
4. **Authentication Failures** — no MFA, brute-force, session fixation, JWT flaws (CWE-287, -307, -613)
5. **Security Misconfiguration** — debug mode, defaults, verbose errors, missing headers (CWE-16)
6. **Insecure Deserialization** — `pickle`, `ObjectInputStream`, `unserialize()` (CWE-502)
7. **Vulnerable Components** — outdated deps with known CVEs (CWE-1104)
8. **SSRF** — user-controlled URLs fetched server-side (CWE-918)
9. **Secrets & Supply Chain** — hardcoded creds, dependency confusion, unsigned artifacts
10. **File Upload** — unrestricted upload, missing content validation, web-accessible storage
11. **JWT / Token Security** — alg:none, weak secrets, missing claims validation, token leakage
12. **Cloud / Container** — IAM over-privilege, public storage, metadata service, root containers
13. **Logging & Monitoring** — missing audit events, insufficient alerting (CWE-223, -778)
14. **Business Logic** — workflow bypass, negative values, race conditions, mass assignment

### Step 3 — Rate Each Finding (DREAD)

Score each dimension 0–10; **Total = average of 5 scores**

| Dimension | 0 | 5 | 10 |
|---|---|---|---|
| **D**amage | No impact | Data leak | Full compromise / RCE |
| **R**eproducibility | Rare conditions | Skilled attacker | Always reproducible |
| **E**xploitability | Expert only | Some skill needed | Point-and-click tool |
| **A**ffected Users | None | Some users | All users |
| **D**iscoverability | Source code only | Requires probing | Obvious in browser |

| Score | Severity | Action |
|---|---|---|
| 7.5–10 | 🔴 Critical | Fix immediately; block release |
| 5.0–7.4 | 🟠 High | Fix before next release |
| 2.5–4.9 | 🟡 Medium | Next sprint |
| 0–2.4 | 🟢 Low | Backlog; document acceptance |

### Step 4 — Report Each Finding

```
### [🔴/🟠/🟡/🟢] [Finding Title]

**CWE:** CWE-XXX | **OWASP Category:** [e.g., Injection / Broken Access Control / Cryptographic Failures]
**DREAD Score:** X.X (Critical/High/Medium/Low)

**Vulnerability:** [One sentence description]

**Evidence:** [Specific line, config, or pattern that demonstrates the issue]

**Attack Scenario:** [How an attacker would exploit this — concrete steps]

**Remediation:** [Specific fix with code snippet when possible]

**Prevention:** [Architectural/process controls to prevent recurrence]
```

### Step 5 — Prioritized Summary

```markdown
## Security Review Summary

| # | Severity | Finding | CWE | DREAD | Effort |
|---|---|---|---|---|---|
| 1 | 🔴 Critical | SQL Injection in login | CWE-89 | 9.0 | Low |
| 2 | 🟠 High | Missing CSRF token | CWE-352 | 6.4 | Low |

## Immediate Actions Required
1. [Most critical fix — specific and actionable]
2. [Second most critical]

## Recommended Security Controls
- [Tool or architectural improvement to add]

## Positive Findings
- [Security controls already in place worth noting]
```

> **Adapt output to audience:** Developers → include code fixes. Security team → include attack scenarios and CVE references. Management → skip code, emphasize business impact and compliance risk.

---

## Quick Vulnerability Reference

### Injection Family

| Vuln | Red Flag in Code | Fix |
|---|---|---|
| SQL Injection | String-concatenated SQL: `"SELECT ... " + input` | Parameterized queries / ORM |
| XSS | `innerHTML`, `document.write`, unescaped template vars | Context-aware encoding; CSP |
| OS Command Injection | `shell=True`, `system()`, `exec()` + user input | Argument list; native APIs |
| SSTI | `render_template_string(f"...{user_input}...")` | Pass as variable, not template source |
| Path Traversal | `open(base + user_input)` without canonicalization | `realpath()` + base path check |
| XXE | XML parser without DTD disabled | `setFeature("disallow-doctype-decl", true)` |
| LDAP Injection | LDAP filter built from user input | Escape `( ) * \ NUL`; allowlist |

### Authentication Red Flags

- Password hashed with `md5()`, `sha1()`, `sha256()` alone → use Argon2id/bcrypt
- No rate limiting on `/login`, `/register`, `/reset-password`
- Session ID in URL parameters
- Session not invalidated server-side on logout
- `if user == 'admin'` hardcoded privilege checks
- Generic MFA bypass: OTP codes not expiring, not invalidated after use

### Authorization Red Flags

- `SELECT * FROM orders WHERE id = :id` — missing `AND user_id = :current_user`
- `is_admin = request.body.is_admin` — trusting client-supplied privilege claims
- Access control only in UI (frontend hiding, not server-side enforcement)
- Missing authorization on `PUT`/`PATCH`/`DELETE` endpoints that exist on `GET`

### JWT / Token Red Flags

- `alg: "none"` accepted — signature verification bypass
- `alg: "HS256"` with public key as secret — RS256 → HS256 confusion attack
- Weak or default secret: `"secret"`, `"changeme"`, app name
- `exp` claim missing or not validated — tokens never expire
- Sensitive data in payload without encryption (JWT is encoded, not encrypted)
- JWT stored in `localStorage` (XSS-accessible) instead of `HttpOnly` cookie
- Full reference → [jwt-oauth.md](jwt-oauth.md)

### File Upload Red Flags

- Extension-only validation: `if filename.endswith('.jpg')` — trivially bypassed
- No MIME type check by content (magic bytes): `Content-Type` header is user-controlled
- Uploaded files stored in web-accessible directory (`/uploads/file.php` → RCE)
- No file size limit → DoS via large uploads
- Original filename used in storage path → path traversal
- Zip/tar extraction without path validation → Zip Slip (CWE-22)

### Cryptography Red Flags

- `MD5`, `SHA1`, `DES`, `RC4`, `ECB` mode anywhere in crypto context
- `random.random()`, `Math.random()`, `rand()` for tokens/keys (not CSPRNG)
- Hardcoded keys: `SECRET_KEY = "abc123"`, `AES_KEY = b"1234567890123456"`
- Plaintext HTTP for any endpoint handling credentials or PII
- IV reuse in CBC mode; missing authenticated encryption (use GCM, not CBC)

### Secrets Detection Patterns

Look for these patterns in any file (code, config, CI/CD, Docker, IaC):

```
# API Keys & Tokens
(api[_-]?key|apikey)\s*[:=]\s*["'][A-Za-z0-9+/]{20,}
(secret[_-]?key|secret)\s*[:=]\s*["'][A-Za-z0-9+/]{16,}
(access[_-]?token|auth[_-]?token)\s*[:=]\s*["'][A-Za-z0-9._-]{20,}

# AWS
AKIA[0-9A-Z]{16}                      # AWS Access Key ID
aws_secret_access_key\s*=\s*[^\s]{40} # AWS Secret Key

# Private Keys
-----BEGIN (RSA|EC|OPENSSH|PGP) PRIVATE KEY-----

# Passwords in config
password\s*[:=]\s*["'][^"']{6,}["']
db_pass(word)?\s*[:=]\s*["'][^"']+["']

# Connection strings with credentials
(mongodb|mysql|postgres|redis):\/\/[^:]+:[^@]+@
```

### Deserialization Red Flags

- `pickle.loads(user_data)` / `pickle.load(request_stream)` in Python
- `unserialize($_POST['data'])` / `unserialize($_COOKIE[...])` in PHP
- Java: `new ObjectInputStream(request.getInputStream())` without class filtering
- .NET: `BinaryFormatter.Deserialize(stream)` / `TypeNameHandling != None` in JSON.NET
- Node.js: `serialize-javascript` eval, `node-serialize` with user data

### Cloud & Container Red Flags

- S3 bucket with `"Principal": "*"` or `ACL: public-read` on sensitive data
- IAM role/user with `"Action": "*"` or `"Resource": "*"` (over-privilege)
- `http://169.254.169.254/` accessible from application (cloud metadata — SSRF risk)
- Container running as `root` (`USER root` or no `USER` directive in Dockerfile)
- `--privileged` flag or `privileged: true` in container config
- Docker socket mounted: `-v /var/run/docker.sock:/var/run/docker.sock`
- Secrets in environment variables in `docker-compose.yml` committed to VCS
- Full reference → [cloud-infra.md](cloud-infra.md)

### Language-Specific Patterns

| Language | High-Risk Patterns to Check |
|---|---|
| **Python** | `eval()`, `exec()`, `pickle.loads()`, `subprocess(shell=True)`, `yaml.load()` (not `safe_load`), `render_template_string()` |
| **JavaScript / Node** | `eval()`, `innerHTML`, `dangerouslySetInnerHTML`, `child_process.exec()`, `serialize()` + `eval`, `require()` with user input |
| **Java** | `Runtime.exec()`, `ObjectInputStream`, `ProcessBuilder` + user input, `ScriptEngine.eval()`, `XMLDecoder` |
| **PHP** | `eval()`, `system()`, `exec()`, `unserialize()`, `include`/`require` + user input, `preg_replace` with `/e` flag |
| **Go** | `os/exec.Command()` + user input, `html/template` vs `text/template` (no auto-escape), `fmt.Sprintf` SQL strings |
| **Ruby** | `` `backtick` ``, `system()`, `eval()`, `YAML.load()` (use `YAML.safe_load`), `send()` with user input |

---

## Threat Modeling Quick Guide (STRIDE)

When reviewing architecture or design, ask for each component:

| Question | STRIDE Category | Common Controls |
|---|---|---|
| Can an attacker impersonate users or systems? | Spoofing | MFA, certificates, TLS mutual auth |
| Can data be modified in transit or at rest? | Tampering | Signatures, HMAC, TLS, input validation |
| Can users deny having performed actions? | Repudiation | Audit logging, tamper-evident logs |
| Can sensitive data be read by unauthorized parties? | Information Disclosure | Encryption, access controls, data minimization |
| Can the service be made unavailable? | Denial of Service | Rate limiting, resource quotas, CDN |
| Can users gain more privileges than intended? | Elevation of Privilege | Least privilege, authz checks, sandboxing |

**Process:** Create DFD → Apply STRIDE to each element → Document mitigations per threat

---

## Security Headers Checklist

For web applications, verify these headers are present:

```http
Strict-Transport-Security: max-age=63072000; includeSubDomains; preload
Content-Security-Policy: default-src 'self'; script-src 'self'; object-src 'none'; frame-ancestors 'none'
X-Content-Type-Options: nosniff
Referrer-Policy: strict-origin-when-cross-origin
Permissions-Policy: camera=(), microphone=(), geolocation=()
Set-Cookie: session=...; Secure; HttpOnly; SameSite=Strict
```

**Missing headers that indicate risk:**
- No `HSTS` → downgrade attack possible
- No `CSP` → XSS impact maximized
- No `X-Frame-Options` or `frame-ancestors` → Clickjacking
- `Access-Control-Allow-Origin: *` with credentials → CORS bypass

Test with: https://observatory.mozilla.org/ | https://securityheaders.com/

---

## Additional Resources

- Security resource URLs, OWASP/CWE/Mobile tables, tools, SSDLC, full checklist → [references.md](references.md)
- JWT/OAuth/OIDC deep reference → [jwt-oauth.md](jwt-oauth.md)
- Cloud, container & IaC security → [cloud-infra.md](cloud-infra.md)
- GraphQL & advanced API security → [api-graphql.md](api-graphql.md)
- Example security analysis outputs → [examples.md](examples.md)
- OWASP Cheat Sheet Series → https://cheatsheetseries.owasp.org/
- CWE Top 25 → https://cwe.mitre.org/top25/
- CISA Known Exploited Vulnerabilities → https://www.cisa.gov/known-exploited-vulnerabilities-catalog
- PortSwigger Web Security Academy → https://portswigger.net/web-security
