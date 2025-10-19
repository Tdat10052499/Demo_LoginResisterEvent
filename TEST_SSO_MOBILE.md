# Hướng dẫn Test SSO Microsoft trên Android Emulator

## 🚀 Đã cấu hình

### Backend
- ✅ Chạy trên `http://0.0.0.0:8000` (cho phép emulator truy cập)
- ✅ CORS đã được cấu hình với `allow_origins=["*"]`
- ✅ Endpoint `/auth/sso-login` đã sẵn sàng

### Frontend (Flutter Mobile)
- ✅ `kBackendUrl = 'http://10.0.2.2:8000'` (Android emulator)
- ✅ Microsoft SSO config:
  - Client ID: `f0f9e0b2-d6ff-40c0-b0b5-9b6a9acf4abc`
  - Redirect URI: `msauth://com.example.login_register_event/qitkjCObmVXTpHslEaOpznysgEk`
  - Scopes: `openid`, `profile`, `email`, `User.Read`

## 📱 Test Flow trên Android Emulator

### 1. Đăng nhập với Microsoft SSO

1. Mở app trên emulator (SM S908E)
2. Tại màn hình Login, click nút **"Đăng nhập với Microsoft"**
3. Trình duyệt sẽ mở và hiển thị trang đăng nhập Microsoft
4. Nhập tài khoản Microsoft (ví dụ: your-email@outlook.com)
5. Sau khi xác thực thành công, app sẽ nhận được token
6. App sẽ gọi API `POST /auth/sso-login` với thông tin user
7. Backend sẽ:
   - Kiểm tra user đã tồn tại (theo email)
   - Nếu chưa → Tạo user mới với `provider='microsoft'`
   - Nếu rồi → Trả về thông tin user
8. App lưu thông tin user vào SharedPreferences
9. Navigate đến HomeScreen

### 2. Đăng ký với Username/Password (local)

1. Click **"Đăng ký ngay"**
2. Nhập thông tin:
   - Username: `testuser_mobile`
   - Email: `testuser_mobile@example.com`
   - Password: `123456`
   - Confirm Password: `123456`
3. Click **"Đăng ký"**
4. Sau khi thành công → Chuyển về Login screen
5. Đăng nhập với username/password vừa tạo

### 3. Đăng nhập với Username/Password

1. Nhập username: `testuser_mobile`
2. Nhập password: `123456`
3. Click **"Đăng nhập"**
4. App gọi API `POST /auth/login`
5. Backend xác thực với bcrypt
6. Trả về thông tin user
7. Navigate đến HomeScreen

## 🔍 Debug & Troubleshooting

### Kiểm tra kết nối Backend từ Emulator

Từ terminal trên máy host:

```powershell
# Test từ emulator (dùng adb shell)
adb shell

# Trong shell của emulator:
curl http://10.0.2.2:8000/
# Phải trả về: {"message":"Welcome to Login Register Event API"}
```

### Kiểm tra log Backend

Terminal chạy uvicorn sẽ hiển thị:
- Request từ emulator: `INFO: 10.0.2.2:xxxxx - "POST /auth/sso-login HTTP/1.1" 200`
- Request thành công: status code 200
- Lỗi: status code 400/401/500 với detail message

### Kiểm tra log Flutter

```bash
flutter logs
```

Hoặc xem log trong Android Studio / VS Code terminal khi chạy `flutter run`.

### Common Issues

#### 1. **Lỗi kết nối: "Failed to connect to /10.0.2.2:8000"**
- **Nguyên nhân:** Backend không chạy hoặc không listen trên `0.0.0.0`
- **Giải pháp:** 
  ```powershell
  cd backend
  python -m uvicorn app.main:app --reload --host 0.0.0.0
  ```

#### 2. **Microsoft SSO không mở trình duyệt**
- **Nguyên nhân:** `flutter_appauth` chưa được cấu hình đúng
- **Giải pháp:** Kiểm tra `android/app/src/main/AndroidManifest.xml`:
  ```xml
  <activity android:name="net.openid.appauth.RedirectUriReceiverActivity">
      <intent-filter>
          <action android:name="android.intent.action.VIEW"/>
          <category android:name="android.intent.category.DEFAULT"/>
          <category android:name="android.intent.category.BROWSABLE"/>
          <data android:scheme="msauth"
                android:host="com.example.login_register_event"
                android:path="/qitkjCObmVXTpHslEaOpznysgEk"/>
      </intent-filter>
  </activity>
  ```

#### 3. **CORS Error**
- **Nguyên nhân:** Backend không trả về header CORS
- **Giải pháp:** Đã fix trong `app/main.py` với `allow_origins=["*"]`

#### 4. **Internal Server Error 500**
- **Nguyên nhân:** Lỗi trong backend (thường là bcrypt hoặc database)
- **Giải pháp:** Xem log backend để biết chi tiết, đã fix bằng cách dùng bcrypt trực tiếp

## 📊 Test Checklist

- [ ] Backend chạy trên `http://0.0.0.0:8000`
- [ ] Emulator kết nối được backend (`curl http://10.0.2.2:8000/`)
- [ ] Flutter app build và cài đặt thành công trên emulator
- [ ] Đăng ký tài khoản mới với username/password
- [ ] Đăng nhập với username/password
- [ ] Click "Đăng nhập với Microsoft" → Mở trình duyệt
- [ ] Đăng nhập Microsoft thành công
- [ ] App nhận được token và user info
- [ ] Navigate đến HomeScreen sau khi đăng nhập
- [ ] SharedPreferences lưu thông tin user đúng

## 🎯 Expected Results

### Đăng ký thành công
```json
{
  "id": "uuid",
  "username": "testuser_mobile",
  "email": "testuser_mobile@example.com",
  "name": "testuser_mobile",
  "provider": "local",
  "created_at": "2025-10-19T..."
}
```

### Đăng nhập thành công (local)
```json
{
  "id": "uuid",
  "username": "testuser_mobile",
  "email": "testuser_mobile@example.com",
  "name": "testuser_mobile",
  "provider": "local",
  "created_at": "2025-10-19T..."
}
```

### SSO Login thành công
```json
{
  "id": "uuid",
  "username": null,
  "email": "your-email@outlook.com",
  "name": "Your Name",
  "provider": "microsoft",
  "created_at": "2025-10-19T..."
}
```

## 📝 Notes

- **Android Emulator IP:** `10.0.2.2` = `localhost` của máy host
- **Web/iOS Simulator:** Dùng `http://localhost:8000`
- **Device thật:** Dùng IP thực của máy (ví dụ: `http://192.168.1.100:8000`)
- **Bcrypt limit:** Mật khẩu tối đa 72 ký tự (đã xử lý tự động trong backend)
- **Database:** PostgreSQL với users table đã migration xong
