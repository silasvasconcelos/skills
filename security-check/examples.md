# Security Analysis — Example Outputs

> Use these examples as reference for formatting and depth of analysis. Adapt the
> level of detail to the audience (developer, security team, or management).

---

## Example 1 — Python Flask API (Code Review)

**Input provided by user:**
```python
@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')
    query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
    user = db.execute(query).fetchone()
    if user:
        token = jwt.encode({'user_id': user['id']}, 'secret', algorithm='HS256')
        return jsonify({'token': token})
    return jsonify({'error': 'Invalid credentials'}), 401

@app.route('/users/<user_id>/profile')
def get_profile(user_id):
    user = db.execute(f"SELECT * FROM users WHERE id={user_id}").fetchone()
    return jsonify(dict(user))
```

---

**Security Analysis Output:**

---

### 🔴 SQL Injection — Login & Profile Endpoints

**CWE:** CWE-89 | **OWASP Category:** Injection
**DREAD Score:** 9.4 (Critical)

| D | R | E | A | D | Total |
|---|---|---|---|---|---|
| 10 | 10 | 9 | 10 | 8 | **9.4** |

**Vulnerability:** Both endpoints construct SQL queries via f-string interpolation with user-controlled input, enabling SQL injection.

**Evidence:**
```python
query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
# line ~5 — direct string interpolation
db.execute(f"SELECT * FROM users WHERE id={user_id}")
# line ~14 — integer injection possible
```

**Attack Scenario:**
```
# Authentication bypass — username: ' OR '1'='1' --
SELECT * FROM users WHERE username='' OR '1'='1' --' AND password='...'
→ Returns first user in table (likely admin)

# Data extraction via UNION injection — username: ' UNION SELECT username,password,null FROM users--
→ Dumps entire users table credentials
```

**Remediation:**
```python
# Use parameterized queries for all DB interactions
@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')
    user = db.execute(
        "SELECT * FROM users WHERE username = ? AND password_hash = ?",
        (username, hash_password(password))  # Also fix plaintext password comparison
    ).fetchone()
    ...

@app.route('/users/<int:user_id>/profile')  # int: type enforces integer
def get_profile(user_id):
    user = db.execute(
        "SELECT id, name, email FROM users WHERE id = ?",  # Explicit columns
        (user_id,)
    ).fetchone()
    ...
```

**Prevention:** Adopt an ORM (SQLAlchemy); enable SAST scanning in CI/CD to catch string-concatenated SQL.

---

### 🔴 Broken Authentication — Weak JWT Secret & Plaintext Password Comparison

**CWE:** CWE-287, CWE-916 | **OWASP Category:** Identification & Authentication Failures
**DREAD Score:** 8.6 (Critical)

| D | R | E | A | D | Total |
|---|---|---|---|---|---|
| 9 | 9 | 9 | 9 | 7 | **8.6** |

**Vulnerability:** (1) JWT signed with hardcoded weak secret `'secret'`. (2) Password compared in plaintext (implying passwords stored in plain text or with reversible encoding).

**Evidence:**
```python
token = jwt.encode({'user_id': user['id']}, 'secret', algorithm='HS256')
#                                             ^^^^^^^^ hardcoded weak secret
query = f"... AND password='{password}'"
#                            ^^^^^^^^^ plaintext comparison → plaintext storage
```

**Attack Scenario:**
1. Attacker brute-forces the HS256 secret `'secret'` in minutes using `hashcat` or `jwt_tool`
2. Forges a token for any `user_id`, including admin accounts
3. Plaintext password storage means any DB read (via SQLi or breach) exposes all user passwords

**Remediation:**
```python
import os
import secrets
import bcrypt

# Passwords: hash on registration, verify on login
def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt(rounds=12)).decode()

def verify_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode(), hashed.encode())

# JWT: load secret from environment; use strong random value
JWT_SECRET = os.environ['JWT_SECRET']  # Set to: openssl rand -base64 32
JWT_EXPIRY = 900  # 15 minutes

token = jwt.encode(
    {'user_id': user['id'], 'exp': time.time() + JWT_EXPIRY},
    JWT_SECRET,
    algorithm='HS256'
)
```

**Prevention:** Secrets management (never hardcode); Argon2id or bcrypt mandatory for passwords; SAST rules for hardcoded credentials.

---

### 🟠 Broken Access Control — IDOR in Profile Endpoint

**CWE:** CWE-639 | **OWASP Category:** Broken Access Control
**DREAD Score:** 7.0 (High)

| D | R | E | A | D | Total |
|---|---|---|---|---|---|
| 7 | 8 | 8 | 8 | 4 | **7.0** |

**Vulnerability:** The profile endpoint accepts any `user_id` without verifying the requesting user is authorized to access that profile.

**Evidence:**
```python
@app.route('/users/<user_id>/profile')
def get_profile(user_id):
    # No authentication check
    # No ownership verification
    user = db.execute(f"SELECT * FROM users WHERE id={user_id}").fetchone()
    return jsonify(dict(user))  # Returns ALL columns including sensitive data
```

**Attack Scenario:**
1. Authenticated user calls `GET /users/42/profile` (their own)
2. Changes to `GET /users/1/profile` — gets admin user's profile
3. Iterates 1..10000 to extract all user profiles including emails, password hashes, PII

**Remediation:**
```python
from functools import wraps
from flask_jwt_extended import jwt_required, get_jwt_identity

@app.route('/users/<int:user_id>/profile')
@jwt_required()  # Require authentication
def get_profile(user_id):
    current_user_id = get_jwt_identity()
    # Only allow users to access their own profile (or admins)
    if current_user_id != user_id and not is_admin(current_user_id):
        abort(403)
    user = db.execute(
        "SELECT id, name, email, created_at FROM users WHERE id = ?",  # No password_hash
        (user_id,)
    ).fetchone()
    if not user:
        abort(404)
    return jsonify(dict(user))
```

---

### 🟠 Sensitive Data Exposure — Full Model Returned

**CWE:** CWE-200 | **OWASP Category:** Cryptographic Failures / Sensitive Data Exposure
**DREAD Score:** 6.0 (High)

**Vulnerability:** `jsonify(dict(user))` returns all columns from the `users` table, potentially including `password_hash`, `internal_notes`, `admin_flag`, etc.

**Remediation:** Define an explicit response schema with only public-safe fields.

---

## Security Review Summary — Flask API

| # | Severity | Finding | CWE | DREAD | Effort |
|---|---|---|---|---|---|
| 1 | 🔴 Critical | SQL Injection (login + profile) | CWE-89 | 9.4 | Low |
| 2 | 🔴 Critical | Weak JWT secret + plaintext passwords | CWE-287/916 | 8.6 | Medium |
| 3 | 🟠 High | IDOR — missing access control on profile | CWE-639 | 7.0 | Low |
| 4 | 🟠 High | Sensitive data exposure — full model | CWE-200 | 6.0 | Low |

### Immediate Actions Required
1. **Replace all f-string SQL with parameterized queries** — this is the highest risk; exploitable in minutes
2. **Rotate JWT secret** (invalidates all existing tokens) and **rehash all passwords** with bcrypt
3. **Add `@jwt_required()` decorator** to all non-public endpoints and enforce ownership checks

### Recommended Security Controls
- Add Bandit (SAST) to CI/CD: `bandit -r app/`
- Adopt SQLAlchemy ORM to eliminate raw SQL
- Use `flask-limiter` for rate limiting on auth endpoints
- Add integration tests that verify 403 is returned when accessing other users' resources

### Positive Findings
- Flask framework itself is well-maintained
- JSON API (not HTML-rendering) reduces XSS surface

---

## Example 2 — Dockerfile Review

**Input:**
```dockerfile
FROM ubuntu:latest
RUN apt-get update && apt-get install -y python3 pip
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
ENV DATABASE_URL=postgresql://admin:SuperSecret123@db:5432/prod
ENV SECRET_KEY=my-secret-key
EXPOSE 8080
CMD ["python3", "app.py"]
```

**Security Analysis Output:**

---

### 🔴 Secrets in Dockerfile — Credentials Exposed

**CWE:** CWE-798 | **OWASP Category:** Security Misconfiguration
**DREAD Score:** 9.0 (Critical)

**Vulnerability:** Database password and application secret hardcoded in `ENV` directives. These are embedded in the image layers, visible in `docker inspect`, image registries, CI/CD logs, and anyone with read access to the Dockerfile or image.

**Evidence:**
```dockerfile
ENV DATABASE_URL=postgresql://admin:SuperSecret123@db:5432/prod
ENV SECRET_KEY=my-secret-key
```

**Attack Scenario:** Any developer with `docker pull` access or access to the git repository can extract these credentials.

**Remediation:**
```dockerfile
# Remove secrets from Dockerfile entirely
# Inject at runtime via orchestrator secrets or environment
```
```yaml
# docker-compose.yml
services:
  app:
    environment:
      DATABASE_URL_FILE: /run/secrets/database_url
    secrets:
      - database_url
secrets:
  database_url:
    external: true  # Managed by Docker Swarm or K8s secrets
```

---

### 🟠 Running as Root — Container Escape Risk

**CWE:** CWE-250
**DREAD Score:** 6.6 (High)

**Vulnerability:** No `USER` directive — container runs as root. If the application is compromised, the attacker has root within the container and may be able to escape to the host.

**Remediation:**
```dockerfile
RUN useradd -r -u 1001 appuser
USER 1001
```

---

### 🟡 Unpinned Base Image

**DREAD Score:** 4.0 (Medium)

**Vulnerability:** `FROM ubuntu:latest` resolves to a different image on each build — unpredictable and may pull in vulnerable packages without knowing.

**Remediation:** Pin to a specific version and digest:
```dockerfile
FROM ubuntu:24.04@sha256:72297848456d5d33d600...
```

Or use a minimal base:
```dockerfile
FROM python:3.12-slim@sha256:...
```

---

## Example 3 — Management Summary (Same Flask API Findings)

> Use this format when the audience is non-technical (management, CTO, compliance).

---

**Security Review: Payment API — Executive Summary**
**Date:** [date of review] | **Reviewer:** Security Team | **Risk Level: 🔴 Critical**

**Overview:** The payment API contains critical vulnerabilities that would allow an attacker to:
1. **Bypass authentication** and log in as any user, including administrators, without a password
2. **Extract all customer data** (names, emails, password hashes) from the database
3. **Forge identity tokens** to impersonate any user

**Business Impact:**
- **LGPD/GDPR compliance violation** — customer PII would be exposed in a breach
- **Financial loss** — compromised admin accounts could access payment processing
- **Reputational damage** — customer data breach requires public notification (LGPD Art. 48)

**Required Actions:**

| Priority | Action | Estimated Effort | Owner |
|---|---|---|---|
| 🔴 Immediate | Fix SQL injection vulnerabilities | 4 hours | Backend Dev |
| 🔴 Immediate | Rotate database password and JWT secret | 1 hour | DevOps |
| 🔴 This week | Implement password hashing (bcrypt) | 8 hours | Backend Dev |
| 🟠 This week | Add authentication to all API endpoints | 4 hours | Backend Dev |
| 🟡 Next sprint | Add automated security scanning to CI/CD pipeline | 8 hours | DevOps |

**Recommendation:** Halt new feature development until Critical findings are resolved. Schedule a follow-up security review after fixes are deployed.

---

## Formatting Notes for LLMs

When generating security analysis output:

1. **Always include Evidence** — quote the specific line/pattern, not a general description
2. **Make Attack Scenarios concrete** — show the actual payload or steps, not just "an attacker could..."
3. **Make Remediation actionable** — include a code fix when possible, not just "use parameterized queries"
4. **Scale depth to context** — snippet → focus on the 2-3 most critical issues; full codebase → comprehensive analysis
5. **Positive findings matter** — always note what security controls ARE in place
6. **Don't overwhelm** — group related findings; a developer needs ≤7 actionable items to act on
7. **Be specific about effort** — Low (hours), Medium (days), High (weeks) helps with prioritization
