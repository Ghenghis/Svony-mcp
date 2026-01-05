# Evony Encryption Keys Reference

Complete encryption keys extracted from EvonyClient1921.swf and AutoEvony2.swf.

## Primary Keys

### ACTION_KEY (Command Signatures)
```
TAO_{313-894*&*($*#-FDIU(430}-{facebook_dioe(&*%$l}
```
**Purpose**: Signs all game commands to prevent tampering.

**Usage**:
```python
def action_signature(data: str) -> str:
    return md5(data + ACTION_KEY)
```

### ACTION_KEY_SL (Secondary)
```
TAO_{313-894*&*($*#-FDIU(430}_SL
```
**Purpose**: Alternate action key for specific commands.

### USER_INFO_KEY (Player Lookup)
```
IUGI_md5_key_{djfiji3*4930}-{fjdi3284$9dlld}
```
**Purpose**: Double MD5 hash for user info lookup.

**Usage**:
```python
def user_info_signature(server: str, fbid: str) -> str:
    return md5(server + fbid + USER_INFO_KEY)
```

### API_KEY (API Signatures)
```
9f758e2deccbe6244f734371b9642eda
```
**Purpose**: Signs API requests.

**Usage**:
```python
def api_signature(data: str) -> str:
    return md5(data + API_KEY)
```

### XOR_KEY (Data Obfuscation)
```
0xAA (170 decimal)
```
**Purpose**: XOR encryption for certain data fields.

**Usage**:
```python
def xor_encrypt(data: bytes) -> bytes:
    return bytes([b ^ 0xAA for b in data])
```

### LOGIN_SALT
```
evony
```
**Purpose**: Salt for password hashing.

## Signature Functions

### Command Signature
```python
import hashlib

def md5(data: str) -> str:
    return hashlib.md5(data.encode()).hexdigest()

def generate_signature(command: str, params: dict, key: str = ACTION_KEY) -> str:
    """Generate command signature"""
    data = command + str(sorted(params.items()))
    return md5(data + key)
```

### Extended Action Signature
```python
def extended_action_signature(
    action: str, 
    sex: str, 
    datetime: str,
    username: str, 
    server_id: str, 
    speed_type: str
) -> str:
    """Extended signature for complex actions"""
    combined = f"{action}{sex}{datetime}{username}{server_id}{speed_type}"
    return md5(combined + ACTION_KEY_SL)
```

## Key Sources

| Key | Source File | Location |
|-----|-------------|----------|
| ACTION_KEY | EvonyClient1921.swf | com.evony.Encryption |
| USER_INFO_KEY | AutoEvony2.swf | Protocol handler |
| API_KEY | Server config | API endpoints |
| XOR_KEY | Both SWFs | Data obfuscation |

## Security Notes

1. **MD5 Weakness**: All signatures use MD5 which is cryptographically broken
2. **Static Keys**: Keys are hardcoded and never rotate
3. **No HMAC**: Simple concatenation, vulnerable to length extension
4. **Client-Side**: All keys extractable from SWF decompilation
