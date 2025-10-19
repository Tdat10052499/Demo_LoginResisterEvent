# Quick Start - Test SSO Mobile

## ✅ Hệ thống đã sẵn sàng

### Backend
```
✓ Chạy trên http://0.0.0.0:8000
✓ Database connected
✓ CORS configured
```

### Frontend
```
✓ Building trên Android Emulator (SM S908E)
✓ kBackendUrl = 'http://10.0.2.2:8000'
```

## 🚀 Test Steps

### 1. Đợi Flutter app build xong (2-3 phút)

Khi terminal hiển thị:
```
✓ Built build\app\outputs\flutter-apk\app-debug.apk
Syncing files to device SM S908E...
Flutter run key commands.
```

App sẽ tự động mở trên emulator.

### 2. Test Local Registration

Trên app emulator:
1. Click **"Đăng ký ngay"**
2. Nhập:
   - Username: `mobile_test`
   - Email: `mobile_test@example.com`
   - Password: `123456`
   - Confirm: `123456`
3. Click **"Đăng ký"**
4. Chờ → Chuyển về Login screen

### 3. Test Local Login

1. Nhập username: `mobile_test`
2. Nhập password: `123456`
3. Click **"Đăng nhập"**
4. Chờ → Chuyển đến HomeScreen

### 4. Test Microsoft SSO

1. Quay về Login screen (nếu cần)
2. Click **"Đăng nhập với Microsoft"**
3. Trình duyệt sẽ mở
4. Đăng nhập tài khoản Microsoft
5. Cho phép quyền truy cập
6. App sẽ nhận token và chuyển về HomeScreen

## 🔍 Monitor Backend

Xem log backend trong terminal:
```
INFO: 10.0.2.2:xxxxx - "POST /auth/register HTTP/1.1" 200
INFO: 10.0.2.2:xxxxx - "POST /auth/login HTTP/1.1" 200
INFO: 10.0.2.2:xxxxx - "POST /auth/sso-login HTTP/1.1" 200
```

## ⚠️ Nếu có lỗi

### Lỗi kết nối
```bash
# Test từ terminal:
curl http://10.0.2.2:8000/

# Hoặc từ emulator (dùng adb):
adb shell
curl http://10.0.2.2:8000/
```

### Xem log Flutter
Trong terminal đang chạy `flutter run`, nhấn `l` để xem logs.

### Restart app
Trong terminal đang chạy `flutter run`:
- Nhấn `r` để hot reload
- Nhấn `R` để hot restart
- Nhấn `q` để quit

## 📱 Emulator Controls

- **Quay lại:** Phím Back trên emulator
- **Home:** Phím Home trên emulator
- **Rotate:** Ctrl + F11 hoặc Ctrl + F12
