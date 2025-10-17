# Quick Start - Test với Android Virtual Device

## ✅ Bạn đã có sẵn:

- Android Studio 2025.1.3
- Android SDK 36.1.0-rc1
- Android Emulator 36.1.9.0
- 2 AVDs: **Pixel_7** và **Small_Phone**

---

## 🚀 Các bước Test nhanh:

### Bước 1: Start Emulator

Chọn một trong hai emulators:

```bash
# Option 1: Pixel 7 (Recommended - high-end device)
flutter emulators --launch Pixel_7

# Option 2: Small Phone (low-end device testing)
flutter emulators --launch Small_Phone
```

Đợi emulator boot lên (30-60 giây lần đầu).

### Bước 2: Kiểm tra device đã sẵn sàng

```bash
flutter devices
```

Bạn sẽ thấy emulator trong list:

```
sdk gphone64 x86 64 (mobile) • emulator-5554 • android-x64 • Android XX (API XX)
```

### Bước 3: Start Backend

Mở terminal mới:

```bash
cd c:\Users\tdat1\Demo_LoginResisterEvent\backend
uvicorn app.main:app --reload
```

Kiểm tra: [http://localhost:8000/docs](http://localhost:8000/docs)

### Bước 4: Run Flutter App

Mở terminal mới:

```bash
cd c:\Users\tdat1\Demo_LoginResisterEvent\frontend\mobile
flutter run
```

Flutter sẽ tự động deploy app lên emulator đang chạy.

### Bước 5: Test trong Emulator

1. **App sẽ mở** → SplashScreen → LoginScreen
2. **Click "Đăng nhập bằng Microsoft"**
3. **Browser mở** → Microsoft login page
4. **Đăng nhập** với Microsoft account
5. **Redirect** về app → HomeScreen

### Bước 6: Test Backend Connection

Trong emulator, mở **Chrome** và truy cập:

```
http://10.0.2.2:8000/docs
```

Nếu thấy FastAPI Swagger UI → Backend connection thành công! ✅

---

## 🐛 Nếu gặp vấn đề:

### Emulator không start?

```bash
# List available emulators
flutter emulators

# Try launch với command khác
emulator -list-avds
emulator -avd Pixel_7
```

### Flutter không thấy device?

```bash
# Restart ADB
adb kill-server
adb start-server
adb devices
```

### Google Play Services warning?

1. Trong emulator: **Settings** → **Accounts** → **Add account** → **Google**
2. Đăng nhập Google account
3. Restart app

### SSO không hoạt động?

Kiểm tra:
- [ ] Google account đã đăng nhập trong emulator
- [ ] AndroidManifest.xml có intent-filter (xem ANDROID_AVD_SETUP.md)
- [ ] Azure Portal đã config redirect URI
- [ ] Backend đang chạy

---

## 📱 Workflow hàng ngày:

```bash
# Terminal 1: Backend
cd backend
uvicorn app.main:app --reload

# Terminal 2: Emulator (chỉ cần chạy 1 lần)
flutter emulators --launch Pixel_7

# Terminal 3: Flutter app
cd frontend/mobile
flutter run

# Hot reload: Press 'r' trong terminal
# Hot restart: Press 'R'
# Quit: Press 'q'
```

---

## 📚 Xem thêm:

- **ANDROID_AVD_SETUP.md** - Hướng dẫn chi tiết setup AVD từ đầu
- **GENYMOTION_SETUP.md** - Alternative emulator (nhanh hơn)
- **FLUTTER_WEB_SETUP.md** - Test trên web browser
- **MICROSOFT_SSO_SETUP.md** - Setup Microsoft authentication

---

**Ready to test! 🎉**

Chạy lệnh sau để bắt đầu:

```bash
flutter emulators --launch Pixel_7
```
