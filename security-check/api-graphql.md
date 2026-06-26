# API & GraphQL Security Reference

> Read this file when analyzing REST APIs, OpenAPI/Swagger specs, GraphQL schemas,
> resolvers, WebSocket handlers, or gRPC services.

---

## REST API Security — OWASP API Security Top 10

### API1 — Broken Object Level Authorization (BOLA / IDOR)

The most common API vulnerability. The API exposes endpoints that accept object IDs without verifying the requesting user is authorized for that specific object.

**Vulnerable patterns:**
```
GET  /api/v1/invoices/4892        ← Can any authenticated user read invoice #4892?
PUT  /api/v1/users/123/profile    ← Can user 456 modify user 123's profile?
GET  /api/v1/files/download?id=99 ← Is file 99 owned by the requesting user?
```

**Testing:** Replace your own resource ID with another user's ID. Also try:
- Sequential integers (1, 2, 3...)
- UUIDs from other responses
- IDs from error messages
- IDs seen in other users' shared content

**Fix:** Every data access must verify ownership at the data layer:
```python
# ❌ Missing authorization
def get_invoice(invoice_id):
    return db.query(Invoice).filter(Invoice.id == invoice_id).first()

# ✅ Scoped to current user
def get_invoice(invoice_id, current_user_id):
    invoice = db.query(Invoice).filter(
        Invoice.id == invoice_id,
        Invoice.owner_id == current_user_id
    ).first()
    if not invoice:
        raise HTTPException(403)  # Not 404 — avoid object existence oracle
    return invoice
```

---

### API3 — Broken Object Property Level Authorization (Mass Assignment + Over-Exposure)

**Mass Assignment:** API auto-binds all request properties to the model, including privileged ones.

```json
// Normal request
{"name": "Alice", "email": "alice@example.com"}

// Attacker adds privileged fields
{"name": "Alice", "email": "alice@example.com", "role": "admin", "subscription": "enterprise"}
```

**Over-Exposure:** API returns more data than the client needs, leaking sensitive fields.

```json
// Response exposes internal/sensitive fields
{
  "id": 42,
  "name": "Alice",
  "email": "alice@example.com",
  "password_hash": "$2b$12$...",  // ❌ Never return this
  "internal_notes": "VIP customer",
  "ssn": "123-45-6789",
  "stripe_customer_id": "cus_..."
}
```

**Fix:** Use explicit response schemas (DTOs/Serializers) — never return `*` or the full model:
```python
# ❌ Exposes everything
return user.__dict__

# ✅ Explicit fields only
return UserPublicSchema.from_orm(user)  # Only id, name, email
```

---

### API4 — Unrestricted Resource Consumption

APIs without rate limiting enable DoS and financial attacks on pay-per-use resources.

**Attack scenarios:**
- Sending 10,000 requests/second to exhaust CPU
- Uploading huge files to exhaust storage
- Triggering expensive operations (PDF generation, email sending, ML inference)
- Using the API to exhaust third-party service quotas (SMS, payment processing)

**Required controls:**
```
Rate limiting:     Max requests per second/minute per user/IP
Throttling:        Slow down after threshold before hard block
Quota:             Daily/monthly limits per account tier
Body size limit:   Reject payloads above threshold
Timeout:           Maximum request processing time
Pagination limits: Max `limit` parameter (e.g., ≤100 items)
```

**Implementation pattern (Express/Node.js):**
```javascript
const rateLimit = require('express-rate-limit')

app.use('/api/', rateLimit({
  windowMs: 15 * 60 * 1000,  // 15 minutes
  max: 100,                    // Max 100 requests per window per IP
  standardHeaders: true,
  legacyHeaders: false,
  message: { error: 'Too many requests, please try again later' }
}))
```

---

### API5 — Broken Function Level Authorization

Admin/internal functions are accessible by regular users because access control only restricts the UI.

**Attack:** Attacker discovers admin endpoints through:
- Documentation/Swagger UI accessible without auth
- Consistent URL patterns (`/api/v1/users` → try `/api/v1/admin/users`)
- Error messages that reveal endpoint structure
- JavaScript bundles that reference admin routes

**Testing checklist:**
- [ ] Access admin endpoints with a regular user token
- [ ] Try HTTP method escalation: GET works but also try POST/PUT/DELETE
- [ ] Check if `/api/internal/...` or `/api/admin/...` requires authentication
- [ ] Verify Swagger/OpenAPI docs are not publicly accessible in production

---

### API9 — Improper Inventory Management

**Red flags:**
- Multiple API versions active simultaneously without lifecycle plan
- Beta/test endpoints in production (`/api/v1/debug`, `/api/test/...`)
- Undocumented endpoints that still process requests
- Different security standards between versions (v1 less secure than v2)

**Fix:**
- Maintain an API inventory; retire old versions with sunset dates
- Remove debug/test endpoints before production deployment
- Version-based security parity — don't relax security for older versions

---

## REST API Security Checklist

### Authentication
- [ ] All endpoints except explicitly public ones require authentication
- [ ] Token expiry enforced; expired tokens rejected with 401
- [ ] API keys not passed in URL query strings (exposed in logs)
- [ ] No HTTP Basic Auth over plain HTTP
- [ ] `Authorization` header, not custom `X-API-Key` in body

### Authorization
- [ ] BOLA checked: every object access validates ownership
- [ ] Function-level: admin endpoints inaccessible to regular users
- [ ] HTTP methods: authorization checked for PUT/PATCH/DELETE separately from GET
- [ ] Service-to-service: mutual TLS or signed requests

### Input Validation
- [ ] Request body schema validated (types, required fields, formats)
- [ ] URL parameters validated (integer IDs, UUID format, enum values)
- [ ] Pagination: `limit` has a maximum (e.g., 100); `offset`/`cursor` validated
- [ ] File uploads: content type, size, and extension validated

### Rate Limiting & DoS
- [ ] Rate limiting on all public and authenticated endpoints
- [ ] Stricter limits on auth endpoints (login, register, password reset)
- [ ] Request body size limit configured at web server level
- [ ] Query timeout set; long-running queries terminated

### Information Exposure
- [ ] Error responses use generic messages; no stack traces, file paths, DB errors
- [ ] API version/framework not revealed in headers (`X-Powered-By`, `Server`)
- [ ] 404 vs 403 decision: don't reveal object existence to unauthorized users
- [ ] CORS: `Access-Control-Allow-Origin` not `*` for credentialed endpoints

### Security Headers for APIs
```http
Content-Type: application/json  (not text/html — prevents HTML injection)
X-Content-Type-Options: nosniff
Strict-Transport-Security: max-age=63072000
Cache-Control: no-store        (for responses containing sensitive data)
```

---

## GraphQL Security

### Attack Patterns

#### 1. Introspection — Information Disclosure

By default, GraphQL exposes the full schema via introspection queries. Attackers use this to discover every type, field, query, mutation, and argument — a complete map of your API.

```graphql
# Attacker runs this to get full schema
query IntrospectionQuery {
  __schema {
    queryType { name }
    types { name fields { name type { name } } }
  }
}
```

**Fix:** Disable introspection in production:
```javascript
// Apollo Server
const server = new ApolloServer({
  schema,
  introspection: process.env.NODE_ENV !== 'production'
})
```

Keep introspection available in development only, behind authentication.

---

#### 2. Query Depth Attack (DoS)

GraphQL's recursive nature allows arbitrarily deep queries that can exhaust server resources:

```graphql
query {
  user {
    friends {
      friends {
        friends {
          friends {  # 100 levels deep → exponential DB queries
            name
          }
        }
      }
    }
  }
}
```

**Fix:** Enforce maximum query depth:
```javascript
const depthLimit = require('graphql-depth-limit')

const server = new ApolloServer({
  schema,
  validationRules: [depthLimit(10)]  // Max 10 levels deep
})
```

---

#### 3. Query Complexity / Batch DoS

Each field has a computational cost. Attackers request thousands of fields in one query:

```graphql
query {
  user1: user(id: 1) { posts { comments { author { posts { ... } } } } }
  user2: user(id: 2) { posts { comments { author { posts { ... } } } } }
  # ... 100 aliases
}
```

**Fix:** Calculate and enforce query cost before execution:
```javascript
const { createComplexityLimitRule } = require('graphql-validation-complexity')

validationRules: [
  createComplexityLimitRule(1000, {  // Max complexity score of 1000
    scalarCost: 1,
    objectCost: 10,
    listFactor: 10
  })
]
```

---

#### 4. Field-Level Authorization Missing

REST APIs have per-endpoint authorization; GraphQL has a single endpoint. Authorization must be implemented at the **field/resolver level**.

```graphql
# The same `user` query might return different fields for different roles
type User {
  id: ID!
  name: String!
  email: String!      # Only the user themselves
  role: String!       # Only admins
  salary: Float       # Only HR
  internalNotes: String  # Only admins
}
```

**Vulnerable pattern:**
```javascript
// ❌ No field-level authorization
const resolvers = {
  User: {
    salary: (parent) => parent.salary  // Anyone can request this
  }
}

// ✅ Check authorization per sensitive field
const resolvers = {
  User: {
    salary: (parent, args, context) => {
      if (context.user.role !== 'hr' && context.user.id !== parent.id) {
        throw new ForbiddenError('Not authorized to view salary')
      }
      return parent.salary
    }
  }
}
```

---

#### 5. Batched Query / N+1 via Field Abuse

**Attack:** Attacker uses field batching to enumerate data without triggering rate limits:

```graphql
query {
  # All in one request — bypasses per-request rate limiting
  u1: user(id: 1) { email }
  u2: user(id: 2) { email }
  u3: user(id: 3) { email }
  # ... u1000: user(id: 1000) { email }
}
```

**Fix:** Limit the number of aliases/batch operations per request.

---

#### 6. Injection via GraphQL Arguments

GraphQL arguments can carry injection payloads just like REST parameters:

```graphql
# SQL Injection attempt
query {
  users(filter: "1=1 UNION SELECT username, password FROM admins--") {
    name
  }
}

# NoSQL Injection
query {
  login(username: "admin", password: {$gt: ""}) {
    token
  }
}
```

**Fix:** Same as REST — parameterized queries; input validation on all resolver arguments.

---

### GraphQL Security Checklist

- [ ] Introspection disabled in production
- [ ] Query depth limit enforced (≤10 levels)
- [ ] Query complexity scoring implemented
- [ ] Alias/batch operation count limited per request
- [ ] Authorization checked at field/resolver level, not just query level
- [ ] All arguments validated (type, format, range)
- [ ] Rate limiting applied to the `/graphql` endpoint
- [ ] Mutations require authentication (not just queries)
- [ ] Error messages sanitized — no schema info, stack traces, or DB errors in responses
- [ ] Query timeout set (long queries terminated)
- [ ] Persisted queries for production (allowlist of known-good queries)

---

## WebSocket Security

### Attack Patterns

| Attack | Description | Fix |
|---|---|---|
| **Missing origin check** | Any site can open a WebSocket to your server | Validate `Origin` header on handshake |
| **No authentication** | WS connection established without proving identity | Authenticate during HTTP upgrade handshake |
| **Token in URL** | `wss://api.example.com/ws?token=...` — token in server logs | Send token in first message after connection |
| **Injection** | WS message content not sanitized before processing | Same input validation as HTTP requests |
| **DoS** | No rate limiting on WS messages | Limit message rate and size per connection |
| **No timeout** | Idle connections held open indefinitely | Implement ping/pong + idle timeout |

**Secure WebSocket handshake:**
```javascript
// Express + ws
wss.on('connection', (ws, req) => {
  // 1. Validate origin
  const origin = req.headers.origin
  if (!ALLOWED_ORIGINS.includes(origin)) {
    ws.close(1008, 'Invalid origin')
    return
  }

  // 2. Validate token from query param or cookie (established before WS upgrade)
  const token = parseCookies(req.headers.cookie).session
  const user = verifyToken(token)
  if (!user) {
    ws.close(1008, 'Unauthorized')
    return
  }

  ws.user = user
})
```

---

## gRPC Security

| Check | Red Flag | Fix |
|---|---|---|
| TLS | `grpc.Dial(addr, grpc.WithInsecure())` | Use `grpc.WithTransportCredentials(...)` |
| Authentication | No interceptor for auth | Add UnaryInterceptor to validate tokens |
| Authorization | No per-RPC authorization | Implement per-method access checks in interceptor |
| Reflection | gRPC reflection enabled in prod | Disable: allows full schema enumeration |
| Input validation | Proto fields without validation | Use `protoc-gen-validate` plugin |

---

## References

- [OWASP API Security Top 10](https://owasp.org/www-project-api-security/)
- [OWASP API Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/REST_Security_Cheat_Sheet.html)
- [GraphQL Security — HackTricks](https://book.hacktricks.xyz/network-services-pentesting/pentesting-web/graphql)
- [PortSwigger GraphQL Attacks](https://portswigger.net/web-security/graphql)
- [Apollo Server Security](https://www.apollographql.com/docs/apollo-server/security/authentication/)
