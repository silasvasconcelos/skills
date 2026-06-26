# JWT / OAuth 2.0 / OIDC Security Reference

> Read this file when analyzing JWT tokens, OAuth flows, API authentication, or OIDC implementations.

---

## JWT (JSON Web Token) — Attack Patterns

### 1. Algorithm None Attack

**Attack:** The `alg` header is changed to `"none"` — the server accepts the token without verifying the signature.

```
# Original header
{"alg":"HS256","typ":"JWT"}

# Attacker modifies to:
{"alg":"none","typ":"JWT"}
# Then removes the signature portion entirely
```

**Vulnerable code:**
```python
# WRONG — trusts the algorithm from the token itself
decoded = jwt.decode(token, key, algorithms=jwt.get_unverified_header(token)['alg'])

# RIGHT — enforce algorithm explicitly
decoded = jwt.decode(token, key, algorithms=["HS256"])
```

**Detection:** Check that algorithm is explicitly hardcoded server-side, not taken from the token header.

---

### 2. RS256 → HS256 Confusion Attack

**Attack:** When a server uses RS256 (asymmetric), the attacker changes `alg` to `HS256` and signs the token with the server's **public key** (which is often publicly available). The server then validates it as an HMAC using the public key as the HMAC secret.

**Fix:** Explicitly specify and enforce the expected algorithm; never accept both RS256 and HS256 for the same endpoint.

---

### 3. Weak or Default Secret (HS256/HS512)

**Attack:** Attacker brute-forces or guesses the HMAC secret used to sign tokens.

**Common weak secrets found in production:**
- `"secret"`, `"password"`, `"changeme"`, `"jwt_secret"`
- Application name or domain
- Hardcoded in `.env.example` committed to VCS

**Detection:** Check `SECRET_KEY`, `JWT_SECRET`, `JWT_SECRET_KEY` environment variables and config files.

**Fix:** Minimum 256-bit cryptographically random secret for HS256:
```bash
openssl rand -base64 32
```

**Fix for asymmetric:** Use RS256 or ES256 with proper key management (HSM/KMS).

---

### 4. Missing or Non-Validated Claims

Required claims to validate on **every** token verification:

| Claim | Type | Validation |
|---|---|---|
| `exp` | Expiration | Must be in the future; reject expired tokens |
| `nbf` | Not Before | If present, must be in the past |
| `iss` | Issuer | Must match expected issuer exactly |
| `aud` | Audience | Must include the current service's identifier |
| `sub` | Subject | Must correspond to an existing, active user |
| `jti` | JWT ID | For one-time tokens; check against revocation list |

**Vulnerable code:**
```python
# WRONG — only decodes, validates nothing
payload = jwt.decode(token, key, algorithms=["HS256"], options={"verify_exp": False})

# RIGHT — validate all critical claims
payload = jwt.decode(
    token, key,
    algorithms=["HS256"],
    issuer="https://auth.example.com",
    audience="https://api.example.com"
)
# exp is validated by default
```

---

### 5. Sensitive Data in JWT Payload

**Problem:** JWT payload is Base64-encoded, not encrypted. Anyone with the token can decode and read the payload.

**Never put in JWT payload:**
- Passwords or password hashes
- Full PII (SSN, credit card, address)
- Internal IDs that reveal business information
- Permission details that could assist privilege escalation

**Use JWE (JSON Web Encryption)** if sensitive claims must be in the token.

---

### 6. JWT Storage Location

| Storage | XSS Risk | CSRF Risk | Recommendation |
|---|---|---|---|
| `localStorage` | 🔴 High — JS readable | None | ❌ Avoid for session tokens |
| `sessionStorage` | 🔴 High — JS readable | None | ❌ Avoid for session tokens |
| `HttpOnly` cookie | None | Medium | ✅ Preferred — add `SameSite=Strict` |
| Memory (JS var) | Low | None | ✅ For SPAs — lost on page refresh |

---

### 7. JWT Revocation (Stateless Problem)

Stateless JWTs cannot be revoked before expiration. Mitigations:

- **Short expiry** — `exp` of 5–15 minutes for access tokens
- **Refresh token rotation** — new refresh token on every use; revoke on logout
- **`jti` blocklist** — store revoked JTI in Redis; check on each request
- **Token family tracking** — detect refresh token reuse (re-use = compromise detected)

---

### 8. kid (Key ID) Header Injection

**Attack:** The `kid` header is used to select which key to use for verification. Attackers inject:
- SQL: `"kid": "' UNION SELECT 'attacker_secret' --"` → key becomes `'attacker_secret'`
- Path traversal: `"kid": "../../dev/null"` → empty file → empty HMAC secret

**Fix:** Validate `kid` against a strict allowlist of known key IDs before using it.

---

## OAuth 2.0 — Attack Patterns

### 1. Authorization Code Interception (Missing PKCE)

**Attack:** On mobile/SPA apps, the authorization code is intercepted by a malicious app registered with the same redirect URI scheme.

**Fix:** Implement PKCE (RFC 7636):
```
1. Client generates code_verifier (random 43-128 char string)
2. Client computes code_challenge = BASE64URL(SHA256(code_verifier))
3. Client sends code_challenge in /authorize request
4. Client sends code_verifier in /token request
5. Server verifies: SHA256(code_verifier) == code_challenge
```

**PKCE is mandatory** for all public clients (SPAs, mobile apps).

---

### 2. Open Redirect in redirect_uri

**Attack:** `redirect_uri` validation uses prefix matching or `contains()`. Attacker registers `https://example.com.attacker.com` or uses `https://example.com/callback/../redirect?url=https://attacker.com`.

**Fix:** Pre-register exact `redirect_uri` values; reject any that don't match exactly (including trailing slashes).

---

### 3. State Parameter Missing (CSRF on OAuth)

**Attack:** Attacker initiates OAuth flow, captures their own authorization code, tricks victim into completing the flow with attacker's code — linking attacker's account to victim.

**Fix:** Generate cryptographically random `state` parameter; validate it on callback before using the code.

```python
# Generate and store state
state = secrets.token_urlsafe(32)
session['oauth_state'] = state

# On callback — validate before proceeding
if request.args.get('state') != session.pop('oauth_state', None):
    abort(403, "Invalid state parameter")
```

---

### 4. Token Leakage via Referer / Logs

**Attack:** If `access_token` is passed as a URL parameter (implicit flow), it appears in:
- Server access logs
- Browser history
- `Referer` header to third-party resources

**Fix:**
- Never use implicit flow — use Authorization Code + PKCE
- Tokens must only travel in HTTP `Authorization: Bearer` header or `HttpOnly` cookie
- If tokens appear in URLs, mark them as compromised and issue new ones

---

### 5. Scope Creep / Excessive Scope

**Attack:** Application requests overly broad scopes (`read:all`, `write:all`, `admin`). If the token is stolen, the attacker has maximum access.

**Fix:** Request minimum necessary scopes; validate received scopes server-side before performing actions.

---

### 6. Client Secret Exposure

**Attack:** `client_secret` committed to source control, embedded in mobile apps, or exposed in JavaScript bundles.

**Fix:**
- Public clients (SPA, mobile) must NOT have a `client_secret` — use PKCE instead
- Server-side clients store `client_secret` in secrets manager, never in code or `.env` in VCS
- Rotate immediately if exposed

---

## OIDC (OpenID Connect) — Attack Patterns

### 1. ID Token Validation Failures

**Required validations on ID token:**

```
1. iss (issuer) == expected authorization server
2. aud (audience) includes your client_id
3. exp > current time
4. iat is reasonable (not issued in the far past)
5. nonce == nonce sent in /authorize (prevents replay)
6. at_hash (if present) validates the access_token
```

---

### 2. Confused Deputy / Mix-Up Attack

**Attack:** In multi-IdP environments, the client receives a token from IdP-A but processes it as if it came from IdP-B, allowing an attacker on IdP-A to impersonate a user on IdP-B.

**Fix:** Always bind `iss` + `sub` together as the user's unique identity; never use `sub` alone.

---

### 3. Account Takeover via Email Claim

**Attack:** IdP allows unverified email addresses. Attacker creates IdP account with victim's email → gets token with `email: victim@example.com` → signs in as victim.

**Fix:**
- Check `email_verified: true` claim before using email as identifier
- Bind accounts to `sub` (stable, IdP-specific) not just `email`

---

## JWT Security Checklist

- [ ] Algorithm hardcoded server-side — not taken from token header
- [ ] `exp` claim validated on every request
- [ ] `iss` and `aud` claims validated
- [ ] Secret is ≥256 bits random; not committed to VCS
- [ ] Short expiry (≤15 min for access tokens)
- [ ] Refresh token rotation implemented
- [ ] Token stored in `HttpOnly` cookie, not `localStorage`
- [ ] `kid` parameter validated against allowlist
- [ ] No sensitive data in unencrypted JWT payload
- [ ] PKCE enforced for public clients
- [ ] `state` parameter validated on OAuth callback
- [ ] `redirect_uri` exact-match registered
- [ ] `email_verified` checked when using OIDC email claim

---

## References

- [JWT Best Practices — RFC 8725](https://www.rfc-editor.org/rfc/rfc8725)
- [OAuth 2.0 Security BCP — RFC 9700](https://www.rfc-editor.org/rfc/rfc9700)
- [PKCE — RFC 7636](https://www.rfc-editor.org/rfc/rfc7636)
- [OWASP JWT Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/JSON_Web_Token_for_Java_Cheat_Sheet.html)
- [PortSwigger JWT Attacks](https://portswigger.net/web-security/jwt)
