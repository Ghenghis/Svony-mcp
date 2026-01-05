# 🔐 SECURITY & VALIDATION RULES
## Complete Security Analysis - EvonyClient & AutoEvony

**Version:** 1.0  
**Scope:** Authentication, Encryption, Validation, Anti-Cheat  
**Source Files:** `Connection.as`, `ALL_ENCRYPTION_KEYS.py`, `anti_cheat.py`

---

# 📋 TABLE OF CONTENTS

1. [Encryption Keys](#1-encryption-keys)
2. [Authentication Flow](#2-authentication-flow)
3. [Signature Generation](#3-signature-generation)
4. [Packet Validation](#4-packet-validation)
5. [Rate Limiting](#5-rate-limiting)
6. [Anti-Cheat Detection](#6-anti-cheat-detection)
7. [Input Validation Rules](#7-input-validation-rules)
8. [Security Vulnerabilities](#8-security-vulnerabilities)
9. [Bypass Techniques](#9-bypass-techniques)
10. [Security Best Practices](#10-security-best-practices)

---

# 1. ENCRYPTION KEYS

## 1.1 Master Key Reference

### ACTION_KEY (Primary)
```python
ACTION_KEY = "TAO_{313-894*&*($*#-FDIU(430}-{facebook_dioe(&*%$l}"
```
**Usage:** Primary signature generation for all game actions
**Location:** Embedded in SWF, extracted via decompilation

### ACTION_KEY_SL (Server Login)
```python
ACTION_KEY_SL = "TAO_{313-894*&*($*#-FDIU(430}_SL"
```
**Usage:** Server login signature variant

### API_KEY
```python
API_KEY = "9f758e2deccbe6244f734371b9642eda"
```
**Usage:** API endpoint authentication

### USER_INFO_KEY
```python
USER_INFO_KEY = "IUGI_md5_key_{djfiji3*4930}-{fjdi3284$9dlld}"
```
**Usage:** Double MD5 hash for user lookup

### XOR_KEY
```python
XOR_KEY = 0xAA
```
**Usage:** Basic obfuscation of packet data

### LOGIN_SALT
```python
LOGIN_SALT = "evony"
```
**Usage:** Password hashing salt

## 1.2 Key Usage Matrix

| Key | Authentication | Signature | Encryption | Decryption |
|-----|---------------|-----------|------------|------------|
| ACTION_KEY | ✅ | ✅ | ❌ | ❌ |
| ACTION_KEY_SL | ✅ | ✅ | ❌ | ❌ |
| API_KEY | ✅ | ✅ | ❌ | ❌ |
| USER_INFO_KEY | ✅ | ✅ | ❌ | ❌ |
| XOR_KEY | ❌ | ❌ | ✅ | ✅ |
| LOGIN_SALT | ✅ | ❌ | ❌ | ❌ |

---

# 2. AUTHENTICATION FLOW

## 2.1 Login Sequence

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         LOGIN AUTHENTICATION FLOW                        │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  CLIENT                           SERVER                                 │
│    │                                │                                    │
│    │  1. Connect (TCP/AMF)          │                                    │
│    │ ──────────────────────────────>│                                    │
│    │                                │                                    │
│    │  2. Request Server Time        │                                    │
│    │ ──────────────────────────────>│                                    │
│    │                                │                                    │
│    │  3. Server Time Response       │                                    │
│    │ <──────────────────────────────│                                    │
│    │                                │                                    │
│    │  4. Login Request              │                                    │
│    │     - username                 │                                    │
│    │     - password_hash            │                                    │
│    │     - signature                │                                    │
│    │ ──────────────────────────────>│                                    │
│    │                                │                                    │
│    │  5. Validate Signature         │                                    │
│    │                        ────────┤                                    │
│    │                                │                                    │
│    │  6. Login Response             │                                    │
│    │     - session_token            │                                    │
│    │     - player_data              │                                    │
│    │ <──────────────────────────────│                                    │
│    │                                │                                    │
└─────────────────────────────────────────────────────────────────────────┘
```

## 2.2 Password Hashing

```python
def password_hash(password: str, salt: str = "evony") -> str:
    """Generate password hash for login"""
    # First hash: password + salt
    first_hash = hashlib.md5((password + salt).encode()).hexdigest()
    
    # Second hash (optional, server-specific)
    # final_hash = hashlib.md5(first_hash.encode()).hexdigest()
    
    return first_hash
```

## 2.3 Session Management

| Field | Description | Lifetime |
|-------|-------------|----------|
| session_token | Main session identifier | ~24 hours |
| player_id | Unique player identifier | Permanent |
| server_id | Current game server | Per-login |
| refresh_token | Session refresh | ~7 days |

---

# 3. SIGNATURE GENERATION

## 3.1 Action Signature

```python
def generate_action_signature(action: str, params: str) -> str:
    """Generate signature for game action"""
    combined = action + params + ACTION_KEY
    return hashlib.md5(combined.encode()).hexdigest()
```

### Signature Format
```
signature = MD5(
    command +
    JSON.stringify(params) +
    ACTION_KEY
)
```

## 3.2 Extended Action Signature

```python
def extended_action_signature(
    action: str,
    sex: str,
    datetime: str,
    username: str,
    server_id: str,
    speed_type: str,
    castleId: str
) -> str:
    """Generate extended signature for complex actions"""
    combined = (
        action + sex + datetime + username + 
        server_id + speed_type + castleId + ACTION_KEY
    )
    return hashlib.md5(combined.encode()).hexdigest()
```

## 3.3 User Info Signature

```python
def user_info_signature(username: str) -> str:
    """Generate user info lookup signature"""
    return hashlib.md5((username + ACTION_KEY_SL).encode()).hexdigest()
```

## 3.4 Signature Validation Points

| Command Category | Signature Required | Key Used |
|------------------|-------------------|----------|
| Login | ✅ Yes | ACTION_KEY |
| Player Actions | ✅ Yes | ACTION_KEY |
| Army Commands | ✅ Yes | ACTION_KEY |
| Chat Messages | ✅ Yes | ACTION_KEY |
| Trade Operations | ✅ Yes | ACTION_KEY |
| Admin Commands | ✅ Yes | Special |

---

# 4. PACKET VALIDATION

## 4.1 AMF Packet Structure

```
┌────────────────────────────────────────────────────────────────┐
│                      AMF PACKET STRUCTURE                       │
├────────────────────────────────────────────────────────────────┤
│ Field          │ Size    │ Description                         │
├────────────────┼─────────┼─────────────────────────────────────┤
│ Version        │ 2 bytes │ AMF version (0x00, 0x03)            │
│ Header Count   │ 2 bytes │ Number of headers                   │
│ Headers        │ Variable│ Header name-value pairs             │
│ Message Count  │ 2 bytes │ Number of messages                  │
│ Messages       │ Variable│ Message bodies                      │
└────────────────┴─────────┴─────────────────────────────────────┘
```

## 4.2 Message Body Structure

```
┌────────────────────────────────────────────────────────────────┐
│ Target URI     │ String  │ Command target (e.g., "army.attack")│
│ Response URI   │ String  │ Response handler                    │
│ Length         │ 4 bytes │ Body length                         │
│ Type           │ 1 byte  │ AMF type marker                     │
│ Data           │ Variable│ Command parameters                  │
│ Signature      │ 32 chars│ MD5 signature                       │
└────────────────┴─────────┴─────────────────────────────────────┘
```

## 4.3 XOR Encryption/Decryption

```python
def xor_encrypt(data: bytes) -> bytes:
    """XOR encrypt/decrypt data (symmetric)"""
    XOR_KEY = 0xAA
    return bytes(b ^ XOR_KEY for b in data)

# Same function for decryption (XOR is symmetric)
xor_decrypt = xor_encrypt
```

## 4.4 Packet Validation Rules

| Rule | Check | Error Code |
|------|-------|------------|
| Signature Valid | MD5 match | -200 |
| Session Valid | Token exists | -201 |
| Timestamp Valid | Within 5 min | -202 |
| Rate Limit | Under threshold | -203 |
| Parameter Types | Match expected | -204 |

---

# 5. RATE LIMITING

## 5.1 Client-Side Rate Limits

```actionscript
// From ActionFactory.as
if (!isRateLimited()) {
    // Execute action
}

// Rate limit configuration
private static const RATE_LIMITS:Object = {
    "attack": { interval: 3000, max: 10 },      // 10 per 3 sec
    "train": { interval: 1000, max: 5 },        // 5 per sec
    "build": { interval: 2000, max: 3 },        // 3 per 2 sec
    "chat": { interval: 500, max: 20 },         // 20 per 0.5 sec
    "trade": { interval: 5000, max: 5 },        // 5 per 5 sec
};
```

## 5.2 Server-Side Rate Limits

| Action Type | Requests/Min | Cooldown |
|-------------|--------------|----------|
| Army Commands | 60 | 1 sec |
| Training | 120 | 0.5 sec |
| Building | 30 | 2 sec |
| Research | 10 | 6 sec |
| Chat | 30 | 2 sec |
| Trade | 20 | 3 sec |
| API Calls | 100 | 0.6 sec |

## 5.3 Rate Limit Evasion

```python
class RateLimitConfig:
    """Rate limit evasion configuration"""
    
    # Minimum delays between actions (milliseconds)
    MIN_DELAYS = {
        'army': 1000,
        'train': 500,
        'build': 2000,
        'research': 6000,
        'chat': 2000,
    }
    
    # Add random jitter to appear human
    JITTER_RANGE = (100, 500)
    
    # Batch size before forced pause
    BATCH_SIZE = 10
    BATCH_PAUSE = 5000
```

---

# 6. ANTI-CHEAT DETECTION

## 6.1 Detection Methods (from anti_cheat.py)

```python
class AntiCheatManager:
    """
    Manages anti-cheat detection and evasion.
    
    Features:
    - Intelligent rate limiting
    - Request pattern randomization
    - Behavior simulation
    - Fingerprint management
    """
    
    DETECTION_PATTERNS = {
        'rapid_requests': 'Too many requests in short time',
        'identical_timing': 'Exact timing between actions',
        'impossible_actions': 'Actions faster than UI allows',
        'pattern_repetition': 'Same action pattern repeated',
        'missing_ui_events': 'Commands without UI interaction',
    }
```

## 6.2 Detection Risk Levels

| Risk Level | Description | Mitigation |
|------------|-------------|------------|
| LOW | Normal gameplay patterns | None needed |
| MEDIUM | Slightly automated | Add random delays |
| HIGH | Clearly automated | Reduce speed, add pauses |
| CRITICAL | Bot detected | Stop, wait, change pattern |

## 6.3 Fingerprint Evasion

```python
class FingerprintConfig:
    """Browser/client fingerprint for evasion"""
    
    def __init__(self):
        self.flash_version = "27.0.0.0"
        self.player_type = "StandAlone"
        self.os = "Windows 10"
        self.language = "en"
        self.platform = "WIN"
        
    def get_fingerprint(self) -> dict:
        return {
            "flashVersion": self.flash_version,
            "playerType": self.player_type,
            "os": self.os,
            "language": self.language,
            "platform": self.platform,
        }
```

## 6.4 Behavioral Patterns to Avoid

| Pattern | Detection Risk | Alternative |
|---------|----------------|-------------|
| Exact 1-second intervals | HIGH | Random 0.8-1.5 sec |
| 24/7 activity | CRITICAL | Simulate sleep patterns |
| Perfect targeting | HIGH | Occasional "misclicks" |
| Instant reactions | HIGH | Human reaction delay (200-500ms) |
| No mouse movements | MEDIUM | Simulate mouse events |

---

# 7. INPUT VALIDATION RULES

## 7.1 Coordinate Validation

```python
def validate_coordinate(x: int, y: int) -> bool:
    """Validate map coordinates"""
    MIN_COORD = 0
    MAX_COORD = 799
    
    if not isinstance(x, int) or not isinstance(y, int):
        return False
    if x < MIN_COORD or x > MAX_COORD:
        return False
    if y < MIN_COORD or y > MAX_COORD:
        return False
    return True
```

## 7.2 Troop Count Validation

```python
def validate_troop_count(count: int, troop_type: int) -> bool:
    """Validate troop training count"""
    MIN_COUNT = 1
    MAX_COUNT = 100000000  # Server limit
    
    # Overflow thresholds (INT32_MAX / cost + 1)
    OVERFLOW_THRESHOLDS = {
        7: 6135037,    # Archer
        2: 42949673,   # Worker
        13: 715828,    # Catapult
    }
    
    if count < MIN_COUNT:
        return False
    if count > MAX_COUNT:
        return False
    
    # Check overflow risk
    threshold = OVERFLOW_THRESHOLDS.get(troop_type)
    if threshold and count > threshold:
        return False  # Potential overflow exploit
        
    return True
```

## 7.3 Resource Validation

```python
def validate_resource_amount(amount: int) -> bool:
    """Validate resource amount"""
    MIN_AMOUNT = 0
    MAX_AMOUNT = 999999999  # From ResourceManager.as
    
    if amount < MIN_AMOUNT or amount > MAX_AMOUNT:
        return False
    return True
```

## 7.4 String Input Validation

```python
def validate_string_input(value: str, max_length: int = 255) -> bool:
    """Validate string input for injection"""
    if not isinstance(value, str):
        return False
    if len(value) > max_length:
        return False
    
    # Check for injection patterns
    DANGEROUS_PATTERNS = [
        '<script', 'javascript:', 'onclick=',
        '\x00', '\r\n\r\n',  # Null bytes, CRLF
    ]
    
    for pattern in DANGEROUS_PATTERNS:
        if pattern.lower() in value.lower():
            return False
            
    return True
```

## 7.5 Validation Error Codes

| Code | Error | Description |
|------|-------|-------------|
| -1 | GENERAL_ERROR | Generic validation failure |
| -2 | INVALID_PARAMS | Parameter type mismatch |
| -3 | RESOURCE_NOT_ENOUGH | Insufficient resources |
| -4 | TROOP_NOT_ENOUGH | Insufficient troops |
| -5 | BUILDING_OCCUPIED | Position in use |
| -45 | INVALID_BUILDING_STATUS | Building state error |
| -46 | INVALID_BUILDING_TYPE | Unknown building |
| -200 | NEED_SECURITY_CODE | Signature required |
| -201 | BUILDING_QUEUE_ERROR | Queue validation fail |

---

# 8. SECURITY VULNERABILITIES

## 8.1 Known Vulnerabilities

### VULN-001: Integer Overflow in Troop Training
**Severity:** CRITICAL  
**Location:** `TroopCommands.as`, `TrainTroopHelper.as`

```python
# Overflow thresholds
Archer: 6,135,037 troops causes overflow
Worker: 42,949,673 troops causes overflow
Catapult: 715,828 troops causes overflow

# Exploit:
train a:6135037  # Results in negative cost = free troops
```

### VULN-002: Missing Signature Validation
**Severity:** HIGH  
**Location:** Some alliance commands

```python
# Some commands don't validate signature properly
# Can be exploited to bypass authentication
```

### VULN-003: Race Condition in Resource Transfer
**Severity:** HIGH  
**Location:** `ResourceManager.as`

```python
# Rapid transport commands can cause race condition
# Resources duplicated or lost
```

### VULN-004: Weak XOR Encryption
**Severity:** MEDIUM  
**Location:** Packet obfuscation

```python
# XOR with constant key (0xAA) is trivially reversible
# All packet data can be decrypted
```

### VULN-005: Hardcoded Encryption Keys
**Severity:** MEDIUM  
**Location:** SWF binary

```python
# All encryption keys are embedded in client
# Can be extracted via decompilation
```

## 8.2 Vulnerability Matrix

| Vulnerability | Impact | Exploitability | Priority |
|--------------|--------|----------------|----------|
| Integer Overflow | Critical | Easy | P0 |
| Missing Signature | High | Medium | P1 |
| Race Condition | High | Hard | P2 |
| Weak XOR | Medium | Easy | P3 |
| Hardcoded Keys | Medium | Easy | P3 |

---

# 9. BYPASS TECHNIQUES

## 9.1 Signature Bypass

```python
def generate_valid_signature(command: str, params: dict) -> str:
    """Generate valid signature for any command"""
    param_str = json.dumps(params, separators=(',', ':'))
    combined = command + param_str + ACTION_KEY
    return hashlib.md5(combined.encode()).hexdigest()
```

## 9.2 Rate Limit Bypass

```python
class RateLimitBypass:
    """Techniques to bypass rate limiting"""
    
    def add_human_delay(self):
        """Add random delay to appear human"""
        delay = random.uniform(0.8, 2.5)
        time.sleep(delay)
    
    def batch_with_pauses(self, actions: list, batch_size: int = 5):
        """Execute in batches with pauses"""
        for i, action in enumerate(actions):
            self.execute(action)
            self.add_human_delay()
            
            if (i + 1) % batch_size == 0:
                time.sleep(random.uniform(3, 8))  # Longer pause
```

## 9.3 Anti-Cheat Bypass

```python
class AntiCheatBypass:
    """Techniques to avoid detection"""
    
    def simulate_ui_events(self):
        """Generate fake UI events"""
        events = ['mouseMove', 'mouseClick', 'keyPress']
        # Interleave real commands with fake UI events
        
    def randomize_timing(self, base_delay: float) -> float:
        """Add random jitter to timing"""
        jitter = random.gauss(0, base_delay * 0.2)
        return max(0.1, base_delay + jitter)
    
    def vary_patterns(self, actions: list):
        """Avoid repetitive patterns"""
        random.shuffle(actions)
        # Add occasional unnecessary actions
```

---

# 10. SECURITY BEST PRACTICES

## 10.1 For Bot Development

| Practice | Description | Implementation |
|----------|-------------|----------------|
| Signature Validation | Always generate valid signatures | Use provided functions |
| Rate Limiting | Respect server limits | Add delays between actions |
| Error Handling | Handle all error codes | Check response codes |
| Session Management | Refresh tokens before expiry | Monitor session state |
| Logging | Log all actions for debugging | Implement logging |

## 10.2 For Security Auditing

```python
# Security audit checklist
AUDIT_CHECKLIST = [
    "Verify all signatures are generated correctly",
    "Check rate limiting is respected",
    "Validate all input parameters",
    "Test error handling for all error codes",
    "Verify session management works",
    "Check for timing attack vulnerabilities",
    "Test integer overflow boundaries",
    "Verify XOR encryption/decryption",
]
```

## 10.3 Secure Configuration

```python
# Recommended security configuration
SECURITY_CONFIG = {
    'validate_signatures': True,
    'respect_rate_limits': True,
    'add_human_delays': True,
    'randomize_patterns': True,
    'log_all_actions': True,
    'handle_all_errors': True,
    'check_overflow': True,
    'sanitize_inputs': True,
}
```

---

# 📊 SECURITY SUMMARY

## Key Statistics

| Category | Count |
|----------|-------|
| Encryption Keys | 6 |
| Signature Types | 4 |
| Validation Rules | 15+ |
| Known Vulnerabilities | 5 |
| Error Codes | 200+ |
| Rate Limit Categories | 7 |

## Security Posture

```
┌────────────────────────────────────────────────────────────────┐
│                    SECURITY POSTURE ASSESSMENT                  │
├────────────────────────────────────────────────────────────────┤
│ Authentication:     ████████░░ 80% (Keys exposed)              │
│ Encryption:         ██████░░░░ 60% (Weak XOR)                  │
│ Validation:         ███████░░░ 70% (Some bypasses)             │
│ Rate Limiting:      ████████░░ 80% (Client-side only)          │
│ Anti-Cheat:         ██████░░░░ 60% (Pattern-based)             │
├────────────────────────────────────────────────────────────────┤
│ OVERALL:            ███████░░░ 70%                             │
└────────────────────────────────────────────────────────────────┘
```

---

*Security & Validation Rules v1.0*  
*Sources: Connection.as, ALL_ENCRYPTION_KEYS.py, anti_cheat.py*  
*Cross-Referenced: Protocol specs, exploit documentation*
