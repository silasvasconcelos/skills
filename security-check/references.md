# Security Reference Tables

> Read this file for: canonical security resource URLs, OWASP/CWE classification tables,
> security tools, Secure SDLC phases, and the complete code review checklist.
>
> Version numbers in tables reflect editions current at the time of authoring.
> CWE IDs are permanent identifiers. Always verify rankings at official sources.

---

## 1. Security Standards & Frameworks

| Resource | URL | Purpose |
|---|---|---|
| OWASP Top 10 (Web) | https://owasp.org/www-project-top-ten/ | Top web application risks |
| OWASP API Security Top 10 | https://owasp.org/www-project-api-security/ | Top API-specific risks |
| OWASP Mobile Top 10 | https://owasp.org/www-project-mobile-top-10/ | Top mobile risks |
| OWASP ASVS | https://owasp.org/www-project-application-security-verification-standard/ | Application security verification standard |
| OWASP Cheat Sheet Series | https://cheatsheetseries.owasp.org/ | Implementation guidance per vulnerability type |
| OWASP Testing Guide (WSTG) | https://owasp.org/www-project-web-security-testing-guide/ | Comprehensive testing methodology |
| OWASP SAMM | https://owaspsamm.org/ | Software Assurance Maturity Model |
| CWE Top 25 | https://cwe.mitre.org/top25/ | Most dangerous software weaknesses (MITRE) |
| NVD / CVE Database | https://nvd.nist.gov/ | NIST vulnerability database with CVSS scores |
| CVE.org | https://www.cve.org | Official CVE records |
| NIST SP 800-53 | https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final | Security and privacy controls catalog |
| NIST CSF | https://www.nist.gov/cyberframework | Cybersecurity risk management framework |
| NIST SSDF (SP 800-218) | https://csrc.nist.gov/Projects/ssdf | Secure Software Development Framework |
| NIST 800-63B | https://pages.nist.gov/800-63-4/sp800-63b.html | Digital identity / authentication guidelines |
| CISA KEV Catalog | https://www.cisa.gov/known-exploited-vulnerabilities-catalog | Actively exploited CVEs — must-patch list |
| CVSS Calculator | https://www.first.org/cvss/calculator/4.0 | Vulnerability scoring (0.0–10.0) |
| Microsoft SDL | https://learn.microsoft.com/en-us/azure/security/develop/threat-modeling-tool | Threat modeling tool |

## 2. Learning & Practice Platforms

| Resource | URL | Purpose |
|---|---|---|
| PortSwigger Web Security Academy | https://portswigger.net/web-security | Free interactive labs — 100+ vulnerability types |
| OWASP WebGoat | https://owasp.org/www-project-webgoat/ | Intentionally vulnerable Java app for training |
| OWASP Juice Shop | https://owasp-juice.shop | Intentionally vulnerable Node.js/Angular app |
| HackerOne Hacktivity | https://hackerone.com/hacktivity/overview | Real-world disclosed vulnerability reports |
| Bugcrowd University | https://www.bugcrowd.com/bugcrowd-university/ | Free bug bounty & web security training |
| PentesterLab | https://pentesterlab.com/ | Advanced web app security & code review labs |
| Snyk Learn | https://snyk.io/learn/ | Developer-focused security knowledge base |
| Have I Been Pwned API | https://haveibeenpwned.com/API/v3 | Check credentials against known breaches |

---

## 3. OWASP Top 10 — Web Application Security Risks

> Check https://owasp.org/www-project-top-ten/ for the current edition.

| ID | Risk | Key CWEs | Primary Prevention |
|----|------|----------|--------------------|
| A01 | Broken Access Control | CWE-200, CWE-352, CWE-639 | Deny by default; server-side RBAC on every request |
| A02 | Cryptographic Failures | CWE-259, CWE-327, CWE-331 | TLS; Argon2/bcrypt for passwords; AES-256 at rest |
| A03 | Injection | CWE-79, CWE-89, CWE-77 | Parameterized queries; input validation; output encoding |
| A04 | Insecure Design | CWE-209, CWE-522, CWE-840 | Threat modeling; SDL; secure design patterns |
| A05 | Security Misconfiguration | CWE-16, CWE-611 | Hardening; minimal platform; security headers |
| A06 | Vulnerable & Outdated Components | CWE-1104 | SCA tools; SBOM; CVE monitoring; patch management |
| A07 | Identification & Authentication Failures | CWE-287, CWE-307, CWE-613 | MFA; rate limiting; NIST 800-63B password policy |
| A08 | Software & Data Integrity Failures | CWE-494, CWE-502, CWE-829 | Digital signatures; SCA; secure CI/CD; safe deserialization |
| A09 | Security Logging & Monitoring Failures | CWE-117, CWE-223, CWE-532 | Centralized logging; SIEM; alerting; incident response plan |
| A10 | Server-Side Request Forgery (SSRF) | CWE-918 | URL allowlists; network segmentation; IMDSv2 |

---

## 4. OWASP API Security Top 10

> Check https://owasp.org/www-project-api-security/ for the current edition.
> See [api-graphql.md](api-graphql.md) for detailed patterns per item.

| ID | Name | Core Prevention |
|----|------|-----------------|
| API1 | Broken Object Level Authorization | Verify ownership on every object access (BOLA/IDOR) |
| API2 | Broken Authentication | Strong auth, MFA, token expiry |
| API3 | Broken Object Property Level Authorization | Expose only required fields; explicit output serialization |
| API4 | Unrestricted Resource Consumption | Rate limiting on all endpoints |
| API5 | Broken Function Level Authorization | Explicit role checks on admin/privileged endpoints |
| API6 | Unrestricted Access to Sensitive Business Flows | Anti-automation; CAPTCHA; velocity checks |
| API7 | Server Side Request Forgery | URL allowlist validation before fetching remote resources |
| API8 | Security Misconfiguration | Hardening; disable debug; restrict CORS |
| API9 | Improper Inventory Management | API gateway; versioning; retire deprecated endpoints |
| API10 | Unsafe Consumption of APIs | Apply same input validation to third-party API responses |

---

## 5. OWASP Mobile Top 10

> Check https://owasp.org/www-project-mobile-top-10/ for the current edition.

| ID | Name | Core Prevention |
|----|------|-----------------|
| M1 | Improper Credential Usage | No hardcoded creds; use platform keychain/keystore |
| M2 | Inadequate Supply Chain Security | Audit third-party SDKs; verify checksums |
| M3 | Insecure Authentication/Authorization | Biometrics + MFA; server-side auth verification |
| M4 | Insufficient Input/Output Validation | Validate all inputs including deep links, IPC data |
| M5 | Insecure Communication | TLS pinning; certificate validation; no cleartext |
| M6 | Inadequate Privacy Controls | Data minimization; GDPR/LGPD compliance; consent |
| M7 | Insufficient Binary Protections | Obfuscation; anti-tampering; root/jailbreak detection |
| M8 | Security Misconfiguration | Disable debug builds; remove test endpoints |
| M9 | Insecure Data Storage | No PII in SharedPreferences/NSUserDefaults unencrypted |
| M10 | Insufficient Cryptography | Use platform crypto APIs; no custom crypto; AES-256 |

---

## 6. CWE Top 25 — Most Dangerous Software Weaknesses

> CWE IDs are permanent identifiers — they don't change between editions.
> Check https://cwe.mitre.org/top25/ for current rankings.

| Rank | CWE ID | Name | Brief |
|---:|---|---|---|
| 1 | CWE-79 | Cross-Site Scripting (XSS) | Injects scripts executed in users' browsers |
| 2 | CWE-89 | SQL Injection | Unsanitized input alters SQL query logic |
| 3 | CWE-352 | CSRF | Forces authenticated users to execute unwanted actions |
| 4 | CWE-862 | Missing Authorization | Actions performed without permission verification |
| 5 | CWE-787 | Out-of-Bounds Write | Writes outside allocated memory — code execution |
| 6 | CWE-22 | Path Traversal | `../` sequences access files outside allowed directory |
| 7 | CWE-416 | Use-After-Free | Accessing freed memory — arbitrary code execution |
| 8 | CWE-125 | Out-of-Bounds Read | Reading beyond buffer — data leak |
| 9 | CWE-78 | OS Command Injection | Unsanitized input passed to OS shell |
| 10 | CWE-94 | Code Injection | Attacker-injected code interpreted and executed |
| 11 | CWE-120 | Classic Buffer Overflow | Overwrites adjacent memory |
| 12 | CWE-434 | Unrestricted File Upload | Allows upload of executable file types |
| 13 | CWE-476 | NULL Pointer Dereference | Crash / DoS |
| 14 | CWE-121 | Stack-Based Buffer Overflow | Common code execution exploit vector |
| 15 | CWE-502 | Unsafe Deserialization | Executing code via malicious serialized objects |
| 16 | CWE-122 | Heap-Based Buffer Overflow | Heap corruption |
| 17 | CWE-863 | Incorrect Authorization | Auth checks exist but implemented incorrectly |
| 18 | CWE-20 | Improper Input Validation | Enables wide class of attacks |
| 19 | CWE-284 | Improper Access Control | Inadequate restrictions on resources |
| 20 | CWE-200 | Information Exposure | Sensitive data leaked to unauthorized parties |
| 21 | CWE-306 | Missing Authentication for Critical Function | Critical ops with no auth |
| 22 | CWE-918 | SSRF | Server makes requests to attacker-controlled URLs |
| 23 | CWE-77 | Command Injection | Commands constructed from user input |
| 24 | CWE-639 | Authorization Bypass via User-Controlled Key | IDOR — changing IDs to access others' data |
| 25 | CWE-770 | Allocation Without Limits | No throttling — enables DoS |

---

## 7. Security Tools Reference

### SAST — Static Analysis

| Tool | Language Focus | Free? | URL |
|---|---|---|---|
| Semgrep | Multi-language | Freemium | https://semgrep.dev/ |
| CodeQL | Multi-language | Free for OSS | https://codeql.github.com/ |
| SonarQube | Multi-language | Community edition free | https://www.sonarqube.org/ |
| Checkmarx | Multi-language | Commercial | https://checkmarx.com/ |
| Bandit | Python | Free | https://bandit.readthedocs.io/ |
| ESLint (security plugins) | JavaScript | Free | https://eslint.org/ |
| Brakeman | Ruby on Rails | Free | https://brakemanscanner.org/ |
| Gosec | Go | Free | https://github.com/securego/gosec |

### DAST — Dynamic Analysis

| Tool | Type | Free? | URL |
|---|---|---|---|
| OWASP ZAP | Web app scanner | Free | https://www.zaproxy.org/ |
| Burp Suite | Web app scanner + manual | Community free | https://portswigger.net/burp |
| Nuclei | Template-based scanner | Free | https://nuclei.projectdiscovery.io/ |
| Nikto | Web server scanner | Free | https://cirt.net/Nikto2 |
| sqlmap | SQL injection automation | Free | https://sqlmap.org/ |
| ffuf | Fuzzing / discovery | Free | https://github.com/ffuf/ffuf |

### SCA — Software Composition Analysis

| Tool | Free? | URL |
|---|---|---|
| Snyk | Freemium | https://snyk.io/ |
| OWASP Dependency-Check | Free | https://owasp.org/www-project-dependency-check/ |
| Dependabot | Free (GitHub) | https://github.com/features/security |
| npm audit | Free (Node.js) | Built-in to npm |
| pip-audit | Free (Python) | https://pypi.org/project/pip-audit/ |
| Trivy | Free | https://trivy.dev/ |
| Grype | Free | https://github.com/anchore/grype |
| OSV-Scanner | Free | https://google.github.io/osv-scanner/ |

### Container & Infrastructure Scanning

| Tool | Purpose | Free? | URL |
|---|---|---|---|
| Trivy | Container, IaC, SBOM, code | Free | https://trivy.dev/ |
| tfsec | Terraform | Free | https://aquasecurity.github.io/tfsec/ |
| Checkov | IaC multi-cloud | Free | https://www.checkov.io/ |
| kube-bench | Kubernetes CIS Benchmark | Free | https://github.com/aquasecurity/kube-bench |
| Grype | Container image CVE scan | Free | https://github.com/anchore/grype |
| Clair | Container image analysis | Free | https://github.com/quay/clair |
| Terrascan | Multi-cloud IaC | Free | https://runterrascan.io/ |

### Secrets Scanning

| Tool | Free? | URL |
|---|---|---|
| Gitleaks | Free | https://github.com/gitleaks/gitleaks |
| truffleHog | Free | https://trufflesecurity.com/trufflehog |
| detect-secrets | Free | https://github.com/Yelp/detect-secrets |
| GitHub Secret Scanning | Free (GitHub) | https://docs.github.com/en/code-security/secret-scanning |

### CVSS Score Severity Reference

| Score | Severity | Recommended Action |
|---|---|---|
| 9.0–10.0 | Critical | Patch within 24 hours |
| 7.0–8.9 | High | Patch within 7 days |
| 4.0–6.9 | Medium | Patch within 30 days |
| 0.1–3.9 | Low | Patch at next scheduled cycle |
| 0.0 | None | No action required |

---

## 8. Secure SDLC — Security Activities by Phase

| Phase | Key Security Activities |
|---|---|
| **Requirements** | Security requirements; abuse cases; compliance mapping (GDPR, PCI DSS, HIPAA, LGPD); data classification |
| **Design** | Threat modeling (STRIDE/DREAD); security architecture review; attack surface analysis; crypto selection |
| **Development** | Secure coding standards; pre-commit hooks (SAST, secrets detection); SCA in CI/CD; IDE security plugins |
| **Testing** | SAST (SonarQube, CodeQL, Semgrep); DAST (ZAP, Burp); SCA; penetration testing; fuzz testing; security regression tests |
| **Deployment** | Security sign-off; CIS Benchmark hardening; IaC scanning (tfsec, Checkov); container scanning (Trivy) |
| **Operations** | SIEM; WAF; vulnerability management; incident response plan; periodic pen tests; bug bounty program |

### CI/CD Security Pipeline

```
Commit → Pre-commit hooks (secrets detection, linting)
       → SAST (Semgrep, CodeQL)
       → SCA (Snyk, OWASP Dependency-Check)
       → Unit tests + security regression tests
       → Container build → Container scan (Trivy)
       → Deploy staging → DAST (OWASP ZAP)
       → Security gate review (block on Critical/High)
       → Deploy production → Runtime monitoring (SIEM, WAF, RASP)
```

### Patch SLA (Risk-Based)

| Severity | SLA |
|---|---|
| Critical (CVSS 9.0+) | 24 hours |
| High (CVSS 7.0–8.9) | 7 days |
| Medium (CVSS 4.0–6.9) | 30 days |
| Low (CVSS < 4.0) | Next release cycle |
| CISA KEV listed | 72 hours regardless of CVSS |

---

## 9. Complete Security Code Review Checklist

### Input Validation & Output Encoding
- [ ] All inputs validated server-side against allowlist (type, length, format, range)
- [ ] Client-side validation present for UX but not relied on for security
- [ ] Data from all sources treated as untrusted: query params, headers, cookies, body, files, IPC
- [ ] Output context-specifically encoded before rendering (HTML, JS, CSS, URL, SQL, LDAP, OS)
- [ ] File uploads: MIME type checked by magic bytes (not `Content-Type` header); stored outside web root
- [ ] No user input placed in HTTP response headers without CRLF stripping
- [ ] Archive extraction guarded against Zip Slip (path traversal in archives)

### Authentication
- [ ] Passwords hashed with Argon2id / bcrypt / scrypt (NOT MD5 / SHA-1 / SHA-256 alone)
- [ ] No hardcoded credentials in source code, config, or environment files in VCS
- [ ] Rate limiting + lockout on login, registration, and password reset endpoints
- [ ] MFA available; enforced for privileged accounts
- [ ] Session ID rotated after successful login (prevent session fixation)
- [ ] Generic error messages — no username enumeration via different responses or timing
- [ ] Constant-time comparisons for token/hash validation (prevent timing attacks)
- [ ] Password recovery uses time-limited, single-use, unguessable tokens
- [ ] Known-breached passwords blocked (Have I Been Pwned API integration)

### Authorization & Access Control
- [ ] Every request verifies both authentication AND authorization server-side
- [ ] IDOR: queries scoped to current user: `WHERE id = :id AND user_id = :current_user`
- [ ] No client-supplied role/admin/privilege flags trusted
- [ ] Vertical privilege: regular users cannot access admin functions
- [ ] Horizontal privilege: users cannot access other users' data
- [ ] HTTP method privilege: PUT/PATCH/DELETE authorized separately from GET
- [ ] Service accounts have minimal permissions (principle of least privilege)

### Session Management
- [ ] Session tokens ≥ 128 bits entropy; server-generated
- [ ] Cookies: `Secure`, `HttpOnly`, `SameSite=Strict` (or `Lax` with justification)
- [ ] Session invalidated server-side on logout (not just client-side cookie deletion)
- [ ] Idle timeout (e.g., 15–30 min) and absolute timeout (e.g., 8 hours) enforced
- [ ] Concurrent session policy defined and enforced
- [ ] Session token not logged, not reflected in URLs

### Cryptography
- [ ] TLS 1.2+ everywhere; TLS 1.0 / 1.1 / SSLv3 disabled; HSTS enabled
- [ ] Strong cipher suites only; no RC4, DES, 3DES, export ciphers
- [ ] AES-256-GCM or ChaCha20-Poly1305 for data at rest
- [ ] Keys stored in secrets manager (Vault, AWS KMS, HSM); never in source code
- [ ] Key rotation implemented and tested
- [ ] CSPRNG for all security-sensitive random values (not `Math.random()`, `rand()`)
- [ ] No deprecated algorithms: MD5, SHA-1, RC4, DES, ECB mode, PKCS#1 v1.5

### SQL / Database
- [ ] All SQL uses parameterized queries / prepared statements (no string concatenation)
- [ ] Database account has minimal privileges (no DROP, CREATE unless required)
- [ ] Database errors caught and logged internally; generic message returned to user
- [ ] Sensitive fields encrypted at rest (PII, financial data)

### Injection Prevention
- [ ] OS commands use argument arrays (`shell=False`); native APIs preferred
- [ ] LDAP queries escape special characters or use parameterized APIs
- [ ] XPath/XQuery expressions not built from user input
- [ ] Template engines render user data as variables, never as template source
- [ ] Expression language injection prevented (Spring EL, OGNL, Freemarker)

### File Handling
- [ ] Path traversal: user-supplied filenames validated with `realpath()` against allowed base
- [ ] File uploads: validated by magic bytes; stored outside web root; renamed on storage
- [ ] File downloads: user cannot specify arbitrary server paths
- [ ] Temporary files use secure creation (`mkstemp()`); cleaned up after use

### HTTP Security Headers
- [ ] `Strict-Transport-Security: max-age=63072000; includeSubDomains; preload`
- [ ] `Content-Security-Policy: default-src 'self'; script-src 'self'; object-src 'none'; frame-ancestors 'none'`
- [ ] `X-Content-Type-Options: nosniff`
- [ ] `Referrer-Policy: strict-origin-when-cross-origin`
- [ ] `Permissions-Policy: camera=(), microphone=(), geolocation=()`
- [ ] `X-Frame-Options: DENY` (or CSP `frame-ancestors`)
- [ ] Server / X-Powered-By headers suppressed or generalized (no version disclosure)

### CSRF Protection
- [ ] CSRF tokens on all state-changing forms and AJAX requests
- [ ] `SameSite=Strict` or `Lax` cookie attribute set on session cookies
- [ ] CORS policy configured; `Access-Control-Allow-Origin: *` not used with credentials

### Sensitive Data
- [ ] No secrets, API keys, or passwords in source code, config files, or VCS
- [ ] No sensitive data in URLs (query params, path segments)
- [ ] No sensitive data logged (passwords, credit cards, SSNs, session tokens)
- [ ] PII stored only when necessary; data minimization applied
- [ ] Data retention limits enforced; purge mechanisms in place

### Error Handling & Logging
- [ ] Exceptions caught and handled; generic user message; detailed internal log
- [ ] No stack traces, internal paths, or version info in error responses
- [ ] Security events logged: auth attempts, authz failures, admin actions, validation rejections
- [ ] Logs do not contain credentials or tokens (prevent log injection risk)
- [ ] Log integrity protected; logs shipped to external SIEM
- [ ] Minimum retention: 90 days hot; 1 year cold

### Third-Party Dependencies
- [ ] All dependencies scanned with SCA; no known Critical/High CVEs
- [ ] Lock files committed for reproducible builds
- [ ] Subresource Integrity (SRI) hashes for CDN-loaded assets
- [ ] Unused dependencies removed
- [ ] SBOM generated (CycloneDX/SPDX format)

### Business Logic
- [ ] Monetary values, quantities, and prices enforced server-side; not trusted from client
- [ ] Multi-step workflows enforce order; steps cannot be skipped
- [ ] Boundary conditions tested: negative values, zero, maximum limits
- [ ] Race conditions: critical sections use atomic DB operations or distributed locks
- [ ] Coupon/discount systems enforce single-use; checked atomically

### Deserialization
- [ ] Native deserialization not used with untrusted data (`pickle`, `unserialize`, `ObjectInputStream`)
- [ ] If unavoidable: class allowlist; signed payloads; isolated process
- [ ] JSON parsing uses schema validation; `TypeNameHandling != All` in .NET JSON

### Infrastructure & Configuration
- [ ] Debug mode disabled in production
- [ ] Directory listing disabled
- [ ] Admin interfaces not publicly accessible; protected by additional auth
- [ ] No default credentials on any service or device
- [ ] Environment configs are independent (dev ≠ staging ≠ prod)
- [ ] Container images run as non-root user
- [ ] Secrets injected at runtime via vault; not baked into Docker images

### API-Specific
- [ ] All API endpoints require authentication (except explicitly public ones)
- [ ] Rate limiting on all endpoints; stricter limits on auth endpoints
- [ ] Pagination limits enforced (`limit` ≤ max configured value)
- [ ] Deprecated API versions retired; no security regressions between versions
- [ ] GraphQL: introspection disabled in production; depth/complexity limits set
- [ ] CORS: `Access-Control-Allow-Origin` is not `*` for credentialed requests
