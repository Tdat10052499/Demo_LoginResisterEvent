# Authentication & Registration Guide

## 🎯 Tổng quan

Ứng dụng hỗ trợ 2 phương thức đăng nhập:

1. **Đăng ký/Đăng nhập Local** - Username & Password
2. **Microsoft SSO** - Đăng nhập bằng tài khoản Microsoft

---

## 📋 Database Schema

### User Table

```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(100),                    -- Tên hiển thị
    email VARCHAR(100) UNIQUE NOT NULL,   -- Email (bắt buộc)
    username VARCHAR(100) UNIQUE,         -- Tên đăng nhập (local)
    hashed_password VARCHAR(255),         -- Mật khẩu đã hash (local)
    provider VARCHAR(50),                 -- 'local' hoặc 'microsoft'
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_users_username ON users(username);
CREATE INDEX idx_users_email ON users(email);
```

---

## 🔐 Authentication Flow

### 1. Đăng ký tài khoản mới (Local)

**Frontend: RegisterScreen**

```dart
// Gửi request đến backend
POST /auth/register
{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "securepass123"
}
```

**Backend: auth.py**

```python
@router.post("/register")
def register(user: UserRegister, db: Session):
    # 1. Kiểm tra username/email đã tồn tại
    # 2. Hash password với bcrypt
    # 3. Tạo user mới với provider="local"
    # 4. Return user info
```

**Validation:**
- Username: Tối thiểu 3 ký tự
- Email: Format hợp lệ
- Password: Tối thiểu 6 ký tự
- Confirm Password: Phải khớp với password

**Flow:**
```
User điền form → Validate → POST /auth/register → 
→ Backend kiểm tra duplicate → Hash password → 
→ Lưu vào database → Return success → 
→ Navigate to LoginScreen
```

---

### 2. Đăng nhập với username/password

**Frontend: LoginScreen**

```dart
// Gửi request đến backend
POST /auth/login
{
  "username": "john_doe",
  "password": "securepass123"
}
```

**Backend: auth.py**

```python
@router.post("/login")
def login(user: UserLogin, db: Session):
    # 1. Tìm user theo username
    # 2. Verify password với bcrypt
    # 3. Return user info nếu đúng
    # 4. Raise 401 nếu sai
```

**Flow:**
```
User nhập username/password → POST /auth/login → 
→ Backend tìm user → Verify password → 
→ Return user info → Save to SharedPreferences → 
→ Navigate to HomeScreen
```

---

### 3. Đăng nhập với Microsoft SSO

**Frontend: LoginScreen**

```dart
void _loginWithMicrosoft() async {
  // 1. Gọi flutter_appauth
  final result = await FlutterAppAuth().authorizeAndExchangeCode(...);
  
  // 2. Parse ID token để lấy user info
  // 3. Gửi user info lên backend
  await AuthService.sendUserToBackend(userName, userEmail, 'Microsoft');
  
  // 4. Lưu local và navigate
}
```

**Backend: auth.py**

```python
@router.post("/sso-login")
def sso_login(user: UserCreate, db: Session):
    # 1. Tìm user theo email
    # 2. Nếu chưa có, tạo user mới với provider="microsoft"
    # 3. Return user info
```

**Flow:**
```
Click "Đăng nhập bằng Microsoft" → 
→ OAuth2 flow → Browser redirect Microsoft → 
→ User login → Redirect back to app → 
→ Parse ID token → POST /auth/sso-login → 
→ Backend lưu/update user → Return user info → 
→ Navigate to HomeScreen
```

---

## 🔒 Password Security

### Hashing với Bcrypt

```python
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Hash password khi đăng ký
hashed = pwd_context.hash(plain_password)

# Verify password khi đăng nhập
is_valid = pwd_context.verify(plain_password, hashed)
```

**Bcrypt features:**
- Salt tự động
- Slow hashing (chống brute-force)
- Configurable cost factor

---

## 📱 Frontend Components

### 1. RegisterScreen (`register_screen.dart`)

**Fields:**
- Username (required, min 3 chars)
- Email (required, valid format)
- Password (required, min 6 chars)
- Confirm Password (required, must match)

**Actions:**
- Submit → POST /auth/register
- "Đã có tài khoản?" → Navigate to LoginScreen

---

### 2. LoginScreen (`login_screen.dart`)

**Fields:**
- Username (required)
- Password (required, with show/hide toggle)

**Actions:**
- Submit → POST /auth/login
- "Đăng nhập bằng Microsoft" → Microsoft SSO flow
- "Chưa có tài khoản?" → Navigate to RegisterScreen

---

### 3. AuthService (`auth_service.dart`)

**Methods:**

```dart
// Lưu user info vào SharedPreferences
static Future<void> saveUserInfo(String userName, String userEmail)

// Lấy user info từ SharedPreferences
static Future<Map<String, String?>> getUserInfo()

// Kiểm tra user đã đăng nhập
static Future<bool> isLoggedIn()

// Logout (clear data)
static Future<void> logout()

// Gửi user info lên backend (SSO)
static Future<void> sendUserToBackend(String name, String email, String provider)
```

---

## 🔄 Auto-login Flow

**main.dart - SplashScreen**

```dart
void _checkLoginStatus() async {
  final isLoggedIn = await AuthService.isLoggedIn();
  if (isLoggedIn) {
    final userInfo = await AuthService.getUserInfo();
    Navigator.pushReplacement(
      context,
      MaterialPageRoute(builder: (_) => HomeScreen(userName: userInfo['name'])),
    );
  } else {
    Navigator.pushReplacement(
      context,
      MaterialPageRoute(builder: (_) => LoginScreen()),
    );
  }
}
```

---

## 🧪 Testing

### Test Registration

1. **Mở RegisterScreen**
2. **Điền form:**
   - Username: `testuser`
   - Email: `test@example.com`
   - Password: `password123`
   - Confirm: `password123`
3. **Click "Đăng ký"**
4. **Verify:**
   - Success message hiển thị
   - Navigate to LoginScreen
   - User được tạo trong database

### Test Login

1. **Mở LoginScreen**
2. **Nhập credentials:**
   - Username: `testuser`
   - Password: `password123`
3. **Click "Đăng nhập"**
4. **Verify:**
   - Navigate to HomeScreen
   - User name hiển thị đúng

### Test Failed Login

1. **Nhập sai password**
2. **Click "Đăng nhập"**
3. **Verify:**
   - Error message: "Incorrect username or password"
   - Không navigate

### Test Duplicate Registration

1. **Đăng ký với username đã tồn tại**
2. **Verify:**
   - Error message: "Username already registered"

---

## 🐛 Troubleshooting

### "Username already registered"

**Nguyên nhân:** Username đã tồn tại trong database

**Giải pháp:** Chọn username khác

---

### "Email already registered"

**Nguyên nhân:** Email đã được dùng

**Giải pháp:** 
- Dùng email khác
- Hoặc login với tài khoản đó

---

### "Incorrect username or password"

**Nguyên nhân:** 
- Username không tồn tại
- Password không đúng

**Giải pháp:**
- Kiểm tra lại username/password
- Reset password (TODO: implement)

---

### "Lỗi kết nối"

**Nguyên nhân:** Backend không chạy hoặc sai URL

**Giải pháp:**
1. Check backend đang chạy: `http://localhost:8000/docs`
2. Check `kBackendUrl` in `msal_config.dart`:
   - Android Emulator: `http://10.0.2.2:8000`
   - iOS Simulator/Web: `http://localhost:8000`
   - Physical device: `http://192.168.x.x:8000`

---

## 🔑 Database Queries

### Tìm user theo username

```sql
SELECT * FROM users WHERE username = 'testuser';
```

### Tìm user theo email

```sql
SELECT * FROM users WHERE email = 'test@example.com';
```

### Liệt kê tất cả local users

```sql
SELECT id, username, email, provider, created_at 
FROM users 
WHERE provider = 'local';
```

### Liệt kê tất cả SSO users

```sql
SELECT id, name, email, provider, created_at 
FROM users 
WHERE provider = 'microsoft';
```

### Delete user (testing)

```sql
DELETE FROM users WHERE username = 'testuser';
```

---

## 📊 API Endpoints

### POST /auth/register

**Request:**
```json
{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "securepass123"
}
```

**Success Response (200):**
```json
{
  "id": "uuid-here",
  "username": "john_doe",
  "email": "john@example.com",
  "name": "john_doe",
  "provider": "local",
  "created_at": "2025-10-17T10:30:00"
}
```

**Error Response (400):**
```json
{
  "detail": "Username already registered"
}
```

---

### POST /auth/login

**Request:**
```json
{
  "username": "john_doe",
  "password": "securepass123"
}
```

**Success Response (200):**
```json
{
  "id": "uuid-here",
  "username": "john_doe",
  "email": "john@example.com",
  "name": "john_doe",
  "provider": "local",
  "created_at": "2025-10-17T10:30:00"
}
```

**Error Response (401):**
```json
{
  "detail": "Incorrect username or password"
}
```

---

## ✅ Checklist

Trước khi test, đảm bảo:

- [ ] Backend đang chạy (`python -m uvicorn app.main:app --reload`)
- [ ] PostgreSQL đang chạy
- [ ] Database migration đã chạy (tables có đủ columns)
- [ ] Flutter app đã compile (`flutter run`)
- [ ] `kBackendUrl` đúng trong `msal_config.dart`
- [ ] Internet connection (cho Microsoft SSO)

---

**Ready to test! 🚀**

Flow test đầy đủ:
1. Register account → Success
2. Login with registered account → Success → HomeScreen
3. Logout → LoginScreen
4. Login again → Auto-remember → HomeScreen
5. Close app and reopen → Auto-login → HomeScreen
