# Backend Testing Skill

## Purpose
Provides comprehensive backend testing strategies for API endpoints, database interactions, authentication, and server-side logic. Combines QA best practices with backend development expertise.

## Auto-Activation Keywords
- "api test"
- "backend test"
- "test api endpoint"
- "integration test"
- "server test"
- "database test"
- "auth test"

## Core Principles

### 1. API Testing Pyramid
```
     /\
    /  \ E2E Tests (10%)
   /____\
  /      \ Integration Tests (30%)
 /________\
/__________\ Unit Tests (60%)
```

**Unit Tests**: Individual functions, utilities, business logic
**Integration Tests**: API endpoints, database queries, external services
**E2E Tests**: Complete user workflows, multi-endpoint scenarios

### 2. Test-Driven Development (TDD) for APIs

**Red-Green-Refactor Cycle**:
1. Write failing test for new endpoint
2. Implement minimum code to pass
3. Refactor for clarity and performance
4. Repeat

**Example**: Testing POST /api/users endpoint

```typescript
// 1. RED: Write test first (fails - endpoint doesn't exist)
describe('POST /api/users', () => {
  it('should create new user with valid data', async () => {
    const response = await request(app)
      .post('/api/users')
      .send({
        email: 'test@example.com',
        password: 'SecurePass123!',
        name: 'Test User'
      });

    expect(response.status).toBe(201);
    expect(response.body).toHaveProperty('id');
    expect(response.body.email).toBe('test@example.com');
  });
});

// 2. GREEN: Implement endpoint to pass test
app.post('/api/users', async (req, res) => {
  const user = await db.users.create(req.body);
  res.status(201).json(user);
});

// 3. REFACTOR: Add validation, error handling
app.post('/api/users', validateUser, async (req, res) => {
  try {
    const user = await userService.create(req.body);
    res.status(201).json(user);
  } catch (error) {
    handleError(error, res);
  }
});
```

### 3. Essential Test Cases for Every API Endpoint

**Success Cases** (2xx):
- ✅ Valid input → 200 OK (GET, PUT, DELETE)
- ✅ Valid creation → 201 Created (POST)
- ✅ Idempotent operations (PUT, DELETE can be called multiple times)

**Client Error Cases** (4xx):
- ✅ Missing required fields → 400 Bad Request
- ✅ Invalid format (email, phone) → 400 Bad Request
- ✅ Missing auth token → 401 Unauthorized
- ✅ Insufficient permissions → 403 Forbidden
- ✅ Resource not found → 404 Not Found
- ✅ Duplicate resource → 409 Conflict
- ✅ Validation failures → 422 Unprocessable Entity

**Server Error Cases** (5xx):
- ✅ Database connection failure → 500 Internal Server Error
- ✅ External API timeout → 503 Service Unavailable

### 4. Integration Testing Patterns

**Pattern 1: Database Integration Test**

```typescript
describe('UserService', () => {
  beforeEach(async () => {
    // Setup: Clean test database
    await db.users.deleteMany({});
  });

  afterEach(async () => {
    // Teardown: Clean up test data
    await db.users.deleteMany({});
  });

  it('should persist user to database', async () => {
    const userData = {
      email: 'test@example.com',
      password: 'hashedpass',
      name: 'Test User'
    };

    const user = await userService.create(userData);

    // Verify in database
    const dbUser = await db.users.findById(user.id);
    expect(dbUser).toBeDefined();
    expect(dbUser.email).toBe(userData.email);
  });
});
```

**Pattern 2: External API Integration Test**

```typescript
describe('Stripe Payment Integration', () => {
  it('should create charge via Stripe API', async () => {
    // Mock external API (don't hit real Stripe in tests)
    const stripeMock = jest.spyOn(stripe.charges, 'create').mockResolvedValue({
      id: 'ch_test123',
      status: 'succeeded',
      amount: 1000
    });

    const charge = await paymentService.createCharge({
      amount: 1000,
      currency: 'usd',
      source: 'tok_visa'
    });

    expect(stripeMock).toHaveBeenCalledWith({
      amount: 1000,
      currency: 'usd',
      source: 'tok_visa'
    });
    expect(charge.status).toBe('succeeded');
  });
});
```

**Pattern 3: Authentication Flow Test**

```typescript
describe('Authentication Flow', () => {
  let authToken;

  it('should login with valid credentials', async () => {
    const response = await request(app)
      .post('/api/auth/login')
      .send({
        email: 'test@example.com',
        password: 'password123'
      });

    expect(response.status).toBe(200);
    expect(response.body).toHaveProperty('token');
    authToken = response.body.token;
  });

  it('should access protected route with token', async () => {
    const response = await request(app)
      .get('/api/users/profile')
      .set('Authorization', `Bearer ${authToken}`);

    expect(response.status).toBe(200);
    expect(response.body).toHaveProperty('email');
  });

  it('should reject access without token', async () => {
    const response = await request(app)
      .get('/api/users/profile');

    expect(response.status).toBe(401);
  });
});
```

### 5. Performance Testing

**Load Testing** (using k6 or Artillery):

```javascript
import http from 'k6/http';
import { check, sleep } from 'k6';

export let options = {
  stages: [
    { duration: '30s', target: 50 },  // Ramp up to 50 users
    { duration: '1m', target: 50 },   // Stay at 50 users
    { duration: '30s', target: 0 },   // Ramp down to 0
  ],
  thresholds: {
    http_req_duration: ['p(95)<500'], // 95% of requests < 500ms
    http_req_failed: ['rate<0.01'],   // <1% request failures
  },
};

export default function () {
  let response = http.get('http://localhost:3000/api/products');

  check(response, {
    'status is 200': (r) => r.status === 200,
    'response time < 500ms': (r) => r.timings.duration < 500,
  });

  sleep(1);
}
```

**Expected Metrics**:
- Response Time: p95 < 500ms, p99 < 1000ms
- Throughput: 100+ requests/second
- Error Rate: <1% under normal load
- Database Connections: Pool not exhausted

### 6. Security Testing

**SQL Injection Test**:

```typescript
it('should prevent SQL injection attacks', async () => {
  const maliciousInput = "'; DROP TABLE users; --";

  const response = await request(app)
    .get('/api/search')
    .query({ q: maliciousInput });

  // Should return safe results, not error
  expect(response.status).toBe(200);

  // Verify database tables still exist
  const usersExist = await db.users.count();
  expect(usersExist).toBeGreaterThan(0);
});
```

**XSS Prevention Test**:

```typescript
it('should sanitize HTML in user input', async () => {
  const xssPayload = '<script>alert("XSS")</script>';

  const response = await request(app)
    .post('/api/comments')
    .send({ text: xssPayload });

  expect(response.status).toBe(201);
  // Script tags should be escaped or removed
  expect(response.body.text).not.toContain('<script>');
});
```

**Rate Limiting Test**:

```typescript
it('should enforce rate limiting', async () => {
  // Send 101 requests rapidly
  const requests = Array(101).fill(0).map(() =>
    request(app).get('/api/data')
  );

  const responses = await Promise.all(requests);

  // First 100 should succeed
  const successfulReqs = responses.filter(r => r.status === 200);
  expect(successfulReqs.length).toBe(100);

  // 101st should be rate limited
  const rateLimitedReqs = responses.filter(r => r.status === 429);
  expect(rateLimitedReqs.length).toBeGreaterThan(0);
});
```

## Testing Frameworks & Tools

### Node.js/TypeScript
- **Jest**: Unit and integration testing
- **Supertest**: HTTP assertion library for APIs
- **MockDB/TestContainers**: Isolated database testing
- **nock**: HTTP mocking for external APIs

### Python
- **pytest**: Testing framework
- **pytest-mock**: Mocking utilities
- **requests-mock**: HTTP mocking
- **faker**: Test data generation

### Database Testing
- **In-memory databases**: SQLite (for SQL), MongoDB Memory Server
- **Test containers**: Docker containers for real databases
- **Database rollback**: Transaction-based test isolation

## Best Practices

### 1. Test Data Management

**Use Factories** (not hardcoded data):

```typescript
// Bad: Hardcoded test data
const testUser = {
  email: 'test@example.com',
  password: 'password123'
};

// Good: Factory pattern
const createTestUser = (overrides = {}) => ({
  email: faker.internet.email(),
  password: 'SecurePass123!',
  name: faker.person.fullName(),
  ...overrides
});

// Use in tests
const user1 = createTestUser();
const user2 = createTestUser({ email: 'specific@example.com' });
```

### 2. Test Isolation

**Each test should be independent**:

```typescript
describe('User API', () => {
  beforeEach(async () => {
    await db.users.deleteMany({});  // Clean slate
  });

  it('test 1', async () => {
    // Create user for this test only
    const user = await createTestUser();
    // Test logic...
  });

  it('test 2', async () => {
    // This test doesn't depend on test 1
    const user = await createTestUser();
    // Test logic...
  });
});
```

### 3. Descriptive Test Names

**Use "should" statements**:

```typescript
// Bad
it('user creation', async () => { ... });

// Good
it('should create user with valid email and password', async () => { ... });
it('should return 400 when email is missing', async () => { ... });
it('should hash password before storing in database', async () => { ... });
```

### 4. Mock External Dependencies

**Mock, don't hit real services**:

```typescript
// Mock email service (don't send real emails in tests)
jest.mock('../services/email', () => ({
  sendWelcomeEmail: jest.fn().mockResolvedValue(true)
}));

// Mock payment gateway (don't charge real cards)
jest.mock('stripe', () => ({
  charges: {
    create: jest.fn().mockResolvedValue({ id: 'ch_test', status: 'succeeded' })
  }
}));
```

### 5. Test Coverage Goals

**Aim for 80%+ coverage**:

```bash
# Generate coverage report
npm run test:coverage

# View coverage
open coverage/lcov-report/index.html
```

**Focus on critical paths**:
- ✅ Authentication and authorization (100% coverage)
- ✅ Payment processing (100% coverage)
- ✅ Data validation (90%+ coverage)
- ✅ Business logic (80%+ coverage)
- ⚠️ Utility functions (70%+ acceptable)

## Anti-Patterns to Avoid

### ❌ Testing Implementation Details

```typescript
// Bad: Testing internal function (implementation detail)
expect(userService._hashPassword).toHaveBeenCalled();

// Good: Testing behavior (public contract)
expect(user.password).not.toBe('plaintext');
```

### ❌ Flaky Tests

```typescript
// Bad: Time-dependent test (flaky)
it('should expire session after 30 minutes', async () => {
  createSession();
  await sleep(1801000);  // Wait 30 minutes + 1 second
  expect(isSessionValid()).toBe(false);
});

// Good: Control time with mocks
it('should expire session after 30 minutes', async () => {
  const now = Date.now();
  jest.spyOn(Date, 'now').mockReturnValue(now);

  createSession();

  // Fast-forward time
  jest.spyOn(Date, 'now').mockReturnValue(now + 1801000);

  expect(isSessionValid()).toBe(false);
});
```

### ❌ Over-Mocking

```typescript
// Bad: Mocking everything (not testing real integration)
jest.mock('../db');
jest.mock('../services/user');
jest.mock('../utils/validator');
// What are you even testing?

// Good: Only mock external dependencies
jest.mock('stripe');  // External service
// Test real database integration with test DB
// Test real validation logic
```

## MCP Integration for Visual API Testing

When APIs have UI components, use Chrome DevTools MCP for verification:

```typescript
// Navigate to API testing dashboard
await mcp__chrome-devtools__navigate_page({
  url: "http://localhost:3000/api-test-dashboard",
  type: "url"
});

// Verify API responses displayed correctly
await mcp__chrome-devtools__list_network_requests({
  resourceTypes: ["fetch", "xhr"]
});

// Take screenshot of test results
await mcp__chrome-devtools__take_screenshot({
  filePath: "api-test-results.png"
});
```

## Quick Reference

### Common Test Commands

```bash
# Run all tests
npm test

# Run specific test file
npm test user.test.ts

# Run tests in watch mode
npm test -- --watch

# Run with coverage
npm test -- --coverage

# Run integration tests only
npm test -- --testPathPattern=integration

# Run E2E tests
npm run test:e2e
```

### Useful Matchers (Jest)

```typescript
expect(value).toBe(expected)          // Strict equality (===)
expect(value).toEqual(expected)       // Deep equality
expect(value).toBeDefined()           // Not undefined
expect(value).toBeNull()              // Is null
expect(value).toBeTruthy()            // Truthy value
expect(value).toBeFalsy()             // Falsy value
expect(array).toContain(item)         // Array includes item
expect(object).toHaveProperty('key')  // Object has key
expect(fn).toThrow(error)             // Function throws
expect(promise).resolves.toBe(value)  // Promise resolves to value
expect(promise).rejects.toThrow()     // Promise rejects
```

## Summary

**Backend testing ensures**:
- ✅ APIs work as expected under all conditions
- ✅ Data integrity is maintained
- ✅ Security vulnerabilities are caught early
- ✅ Performance meets requirements
- ✅ Regressions are detected immediately

**Test early, test often, automate everything.**
