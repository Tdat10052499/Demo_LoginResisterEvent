# Fix Build Error - appAuthRedirectScheme

## ✅ Đã fix lỗi

### Lỗi gốc:
```
Attribute data@scheme at AndroidManifest.xml requires a placeholder substitution 
but no value for <appAuthRedirectScheme> is provided.
```

### Nguyên nhân:
`flutter_appauth` yêu cầu cấu hình `appAuthRedirectScheme` trong `build.gradle.kts` để Android có thể xử lý redirect từ Microsoft SSO.

### Giải pháp đã áp dụng:

Đã thêm vào file `android/app/build.gradle.kts`:

```kotlin
defaultConfig {
    applicationId = "com.example.login_register_event"
    minSdk = flutter.minSdkVersion
    targetSdk = flutter.targetSdkVersion
    versionCode = flutter.versionCode
    versionName = flutter.versionName
    
    // Microsoft SSO configuration
    manifestPlaceholders["appAuthRedirectScheme"] = "msauth"  // <-- ADDED
}
```

## 🚀 Build lại

Sau khi fix:

```bash
cd frontend/mobile
flutter clean
flutter pub get
flutter run -d <device-id>
```

## 📱 Emulator đang khởi động

Pixel 7 emulator đang được khởi động. Đợi khoảng 30-60 giây để emulator sẵn sàng.

### Kiểm tra emulator:
```bash
flutter devices
```

Khi emulator sẵn sàng, sẽ hiển thị:
```
Pixel 7 (mobile) • emulator-5554 • android-x64 • Android XX (API XX)
```

### Build và chạy:
```bash
cd frontend/mobile
flutter run -d emulator-5554
```

## ⚠️ Lưu ý

- Emulator khởi động lần đầu mất 30-60 giây
- Nếu emulator không khởi động, thử:
  - Mở Android Studio → AVD Manager → Start emulator thủ công
  - Hoặc dùng Genymotion (nếu đã cài)
- Backend phải chạy trên `http://0.0.0.0:8000`
- `kBackendUrl` đã được set: `'http://10.0.2.2:8000'`
