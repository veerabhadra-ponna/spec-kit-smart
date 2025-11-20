# Use Case 2: Healthcare Patient Portal

## The Requirement

### Overview
Build a patient portal for a healthcare network that allows patients to view medical records, schedule appointments, communicate with providers, and manage prescriptions while maintaining strict HIPAA compliance.

### Functional Requirements

#### Core Features
1. **Patient Authentication**
   - Multi-factor authentication
   - Biometric login support
   - Session management with automatic timeout
   - Delegated access (caregivers, family members)

2. **Medical Records Access**
   - View lab results with historical trends
   - Download/share records with other providers
   - Imaging viewer for X-rays, MRIs
   - Medication history and interactions

3. **Appointment Management**
   - Online scheduling with provider availability
   - Telehealth video appointments
   - Appointment reminders (SMS, email)
   - Waitlist management

4. **Secure Messaging**
   - Provider-patient communication
   - Message threading with attachments
   - Read receipts and response time tracking
   - Emergency escalation protocols

5. **Prescription Management**
   - Request refills
   - Pharmacy selection/transfer
   - Drug interaction warnings
   - Prior authorization status

### Compliance Requirements (HIPAA)
- **Access Controls**: Role-based access with minimum necessary principle
- **Audit Trails**: All PHI access must be logged with timestamp, user, and purpose
- **Encryption**: AES-256 for data at rest, TLS 1.3 for transit
- **Data Retention**: 7-year retention with secure deletion
- **Breach Notification**: Automated detection and 72-hour notification capability
- **Business Associate Agreements**: Third-party integrations must be compliant

### Technical Requirements
- React frontend with accessibility (WCAG 2.1 AA)
- Node.js backend with Express
- MongoDB with field-level encryption
- FHIR R4 API compatibility
- SOC 2 Type II infrastructure

---

## Why Vibe Coding Fails

### The Scenario
A developer starts with: *"Build a patient portal where users can see their medical records and message their doctors"*

### What Actually Happens

#### The "Move Fast" Approach
```
Developer: "Create a patient dashboard showing medical records"
AI: Creates dashboard component fetching from /api/records
    - No access control check
    - No audit logging
    - Records cached in localStorage (violation!)
```

```
Developer: "Add messaging between patients and doctors"
AI: Creates messaging feature
    - Stores messages in plain text
    - No encryption at rest
    - Attachments saved with predictable URLs (violation!)
```

```
Developer: "Make it look nice and add appointment booking"
AI: Focuses on UI polish
    - Still no audit trails
    - No session timeout
    - Patient IDs in URLs (violation!)
```

#### Week 4: Security Review Disaster

**Compliance Officer:** "We need to audit this before launch"

**Findings:**
1. ❌ PHI stored in browser localStorage
2. ❌ No audit logs for record access
3. ❌ Messages not encrypted at rest
4. ❌ Session doesn't timeout after 15 minutes
5. ❌ Patient IDs exposed in URLs
6. ❌ No access control on API endpoints
7. ❌ Attachments accessible without authentication
8. ❌ No breach detection capability
9. ❌ Missing BAA validation for SMS provider
10. ❌ Deletion doesn't meet secure deletion standards

**Compliance Officer:** "This cannot launch. Every finding is a potential $50,000 fine."

#### The Expensive Rework

```
Developer: "Add HIPAA compliance to the patient portal"
AI: "I'll add encryption and audit logging..."

But:
- Changing data model requires migration
- Audit logging wasn't designed in; it's bolted on
- Session management conflicts with existing auth
- Can't just "add" access controls to existing endpoints
- Third-party integrations need complete review
```

### The Result
- **Timeline**: 6 weeks development → 8 weeks rework
- **Cost**: $150,000 development → $400,000 total (with compliance fixes)
- **Risk**: 3 months delayed launch, reputation damage
- **Pattern**: Compliance as afterthought = complete redesign

---

## Why Spec Kit Wins

### Phase 1: Guidelines Generation (Day 1)

```bash
npx spec-kit guidelines
```

**Input**: Project context + HIPAA compliance requirements

**Output: CORPORATE-GUIDELINES.md**

```markdown
## Healthcare Compliance Standards

### 1. Data Handling (HIPAA)
- NEVER store PHI in localStorage, sessionStorage, or cookies
- ALL database fields containing PHI must use field-level encryption
- ALL API responses with PHI must be logged with: timestamp, user_id,
  patient_id, data_accessed, purpose

### 2. Authentication & Session
- Sessions MUST timeout after 15 minutes of inactivity
- Failed login attempts: lock after 5 attempts for 30 minutes
- MFA required for all PHI access

### 3. API Security
- All endpoints MUST check user authorization before data access
- Patient IDs MUST NOT appear in URLs; use opaque tokens
- All responses MUST include audit correlation ID

### 4. Third-Party Integrations
- ALL external services MUST have BAA on file before integration
- SMS/Email providers MUST be HIPAA-compliant (Twilio, SendGrid Healthcare)

### 5. Code Patterns
- Use `AuditLogger.logPHIAccess()` for all PHI operations
- Use `EncryptedField` decorator for PHI database fields
- Use `@RequiresMFA` decorator for sensitive operations
```

### Phase 2: Specification with Compliance Built-In (Day 1-2)

```bash
npx spec-kit specify
```

**Output: PRD with compliance integrated**

```markdown
## Medical Records Feature

### API: GET /api/patient/records
Authorization: Bearer token + MFA verification
Audit: Log access with purpose "patient_self_access"

Response:
- Records returned with opaque IDs (not database PKs)
- Audit correlation ID in response header
- Access logged before response sent

### Data Model: MedicalRecord
- patient_id: EncryptedField(String)
- diagnosis: EncryptedField(String)
- provider_notes: EncryptedField(String)
- access_log: Embedded audit trail

### Frontend: Dashboard Component
- No PHI in component state after unmount
- No caching of medical data
- Display audit notice: "Access logged for your protection"
```

### Phase 3: Compliant Development (Days 2-6)

Every feature is developed with compliance built-in from the start:

#### Example: Messaging Feature

**Specification says:**
```markdown
## Secure Messaging
- Messages encrypted with patient-specific key
- Attachments stored in compliant storage (S3 with SSE-KMS)
- Attachment URLs are signed, expire in 5 minutes
- All message access logged with thread context
```

**AI develops WITH these constraints:**
```typescript
// Generated code follows guidelines automatically
@RequiresMFA()
async getMessages(patientId: string, userId: string) {
  // Audit BEFORE access (guideline enforcement)
  await AuditLogger.logPHIAccess({
    userId,
    patientId,
    action: 'VIEW_MESSAGES',
    purpose: 'patient_communication'
  });

  // Encrypted at rest (guideline enforcement)
  const messages = await MessageModel.find({
    patientId: encrypt(patientId)
  });

  // Signed URLs for attachments (guideline enforcement)
  return messages.map(m => ({
    ...m,
    attachments: m.attachments.map(a =>
      generateSignedUrl(a, { expiresIn: 300 })
    )
  }));
}
```

### Phase 4: Compliance Validation (Day 7)

```bash
npx spec-kit validate
```

**Automated checks:**
- ✅ All PHI fields use EncryptedField
- ✅ All API endpoints have audit logging
- ✅ Session timeout configured (15 min)
- ✅ No localStorage usage for PHI
- ✅ All third-party services have BAA

---

## Measurable Outcomes

| Metric | Vibe Coding | Spec Kit | Improvement |
|--------|-------------|----------|-------------|
| Development Time | 14 weeks | 5 weeks | **64% faster** |
| Compliance Violations | 10 findings | 0 findings | **100% compliant** |
| Rework Cost | $250,000 | $0 | **100% savings** |
| Launch Delay | 3 months | 0 | **On schedule** |
| Audit Prep Time | 2 weeks | 2 hours | **98% reduction** |
| Potential Fines Avoided | $500,000 | $0 | **Risk eliminated** |

---

## Key Differentiator

### The Compliance Drift Problem
In vibe coding, compliance is an afterthought:
1. Developer focuses on features
2. AI builds what's asked (not what's required)
3. Compliance review finds violations
4. Architectural changes needed
5. Expensive rework or risky launch

### The Spec Kit Solution
**Guidelines enforce compliance from line 1:**

```
CORPORATE-GUIDELINES.md
        ↓
   Every AI prompt
        ↓
   Every generated code
        ↓
   Compliant by design
```

The AI **cannot generate non-compliant code** because:
- Guidelines are injected into every prompt
- Patterns are predefined (EncryptedField, AuditLogger)
- Violations are caught in specification review
- Validation runs before merge

**Compliance is not a phase. It's the foundation.**

---

## Demo Script

### Setup (2 min)
"Healthcare has strict HIPAA requirements. A single violation can be a $50,000 fine. Let's see how vibe coding handles this..."

### Problem Demo (3 min)
Show a typical chat session:
1. "Build a patient messaging feature"
2. AI creates feature with messages in plain text
3. No audit logging
4. Point out: "This is 3 HIPAA violations in 50 lines of code"

### Solution Demo (5 min)
1. Show CORPORATE-GUIDELINES.md with HIPAA patterns
2. Show specification with compliance requirements embedded
3. Show generated code using EncryptedField, AuditLogger
4. Show validation output: "0 compliance violations"

### Close (2 min)
"With vibe coding, compliance is a $250,000 rework. With Spec Kit, it's built into every line of code. That's the difference between a launch and a lawsuit."
