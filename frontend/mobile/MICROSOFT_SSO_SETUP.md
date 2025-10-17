# Microsoft SSO Setup Guide

## Tổng quan
Dự án đã tích hợp Microsoft SSO với các tính năng:
- Đăng nhập bằng Microsoft account
- Lưu thông tin user vào backend (PostgreSQL)
- Tự động đăng nhập khi mở lại app
- Logout và xóa session

## Các file đã tạo/cập nhật
1. `lib/msal_config.dart` - Cấu hình SSO
2. `lib/auth_service.dart` - Service xử lý auth và lưu trữ
3. `lib/login_screen.dart` - Màn hình đăng nhập với nút Microsoft SSO
4. `lib/main.dart` - Kiểm tra trạng thái đăng nhập khi khởi động
5. `lib/screen_home.dart` - Màn hình chính với logout
6. `pubspec.yaml` - Thêm dependencies

## Bước 1: Cài đặt dependencies

```powershell
cd frontend/mobile
flutter pub get
```

## Bước 2: Đăng ký app trên Azure Portal

1. Truy cập https://portal.azure.com
2. Azure Active Directory → App registrations → New registration
3. Điền thông tin:
   - Name: "Login Register Event"
   - Supported account types: Accounts in any organizational directory and personal Microsoft accounts
   - Redirect URI: (để trống, thêm sau)
4. Sau khi tạo, copy **Application (client) ID**

## Bước 3: Tạo Signature Hash cho Android

Chạy lệnh sau trong PowerShell để lấy SHA-1 fingerprint:

```powershell
keytool -list -v -keystore "$env:USERPROFILE\.android\debug.keystore" -alias androiddebugkey -storepass android -keypass android
```

Tìm dòng `SHA1:` và copy giá trị hex (ví dụ: `AA:BB:CC:DD:...`)

Chuyển SHA-1 hex sang Base64 URL-safe:

```powershell
# Thay YOUR_SHA1_HEX bằng giá trị SHA1 vừa lấy (bỏ dấu :)
$sha = "AABBCCDD...".Replace(":","")
$bytes = for ($i=0; $i -lt $sha.Length; $i += 2) { [Convert]::ToByte($sha.Substring($i,2),16) }
$base64 = [System.Convert]::ToBase64String($bytes)
$urlsafe = $base64.TrimEnd('=') -replace '\+','-' -replace '/','_'
Write-Output $urlsafe
```

Copy kết quả (ví dụ: `XYZabc123_UrlSafe`)

## Bước 4: Cấu hình Redirect URI trong Azure

1. Trong Azure Portal, vào app vừa tạo → Authentication → Add a platform
2. Chọn "Android":
   - Package name: `com.example.login_register_event`
   - Signature hash: paste giá trị Base64 URL-safe ở bước 3
3. Hoặc thêm thủ công redirect URI:
   - Android: `msauth://com.example.login_register_event/YOUR_SIGNATURE_HASH`
   - iOS: `msauth.com.example.loginRegisterEvent://auth`
4. Save

## Bước 5: Cập nhật msal_config.dart

Mở `lib/msal_config.dart` và thay:
- `YOUR_AZURE_CLIENT_ID` → Client ID từ bước 2
- `YOUR_SIGNATURE_HASH` → Signature hash từ bước 3
- `kBackendUrl` → URL backend thực tế (ví dụ: `http://10.0.2.2:8000` cho Android emulator)

## Bước 6: Cấu hình AndroidManifest.xml

Thêm intent-filter vào `android/app/src/main/AndroidManifest.xml`:

```xml
<activity
    android:name=".MainActivity"
    ...>
    <!-- Existing intent-filter -->
    <intent-filter>
        <action android:name="android.intent.action.MAIN" />
        <category android:name="android.intent.category.LAUNCHER" />
    </intent-filter>

    <!-- Deep link for MSAL redirect -->
    <intent-filter>
        <action android:name="android.intent.action.VIEW" />
        <category android:name="android.intent.category.DEFAULT" />
        <category android:name="android.intent.category.BROWSABLE" />
        <data
            android:scheme="msauth"
            android:host="com.example.login_register_event"
            android:path="/YOUR_SIGNATURE_HASH" />
    </intent-filter>
</activity>
```

Thay `YOUR_SIGNATURE_HASH` bằng giá trị thực.

## Bước 7: Cấu hình iOS (nếu dùng iOS)

Thêm vào `ios/Runner/Info.plist`:

```xml
<key>CFBundleURLTypes</key>
<array>
  <dict>
    <key>CFBundleURLSchemes</key>
    <array>
      <string>msauth.com.example.loginRegisterEvent</string>
    </array>
  </dict>
</array>
```

## Bước 8: Chạy app

```powershell
# Android emulator hoặc device
flutter run

# Web (Chrome)
flutter run -d chrome
```

## Luồng hoạt động

1. **Lần đầu mở app**: Hiển thị LoginScreen
2. **Nhấn "Đăng nhập bằng Microsoft"**: Mở trình duyệt → đăng nhập Microsoft → redirect về app
3. **Sau khi đăng nhập thành công**:
   - Lưu thông tin user vào SharedPreferences
   - Gửi thông tin lên backend `/auth/sso-login`
   - Chuyển sang HomeScreen
4. **Mở lại app**: Tự động chuyển vào HomeScreen (không cần đăng nhập lại)
5. **Logout**: Xóa SharedPreferences và quay lại LoginScreen

## Troubleshooting

### Lỗi "AADSTS50011: The redirect URI does not match"
- Kiểm tra redirect URI trong Azure Portal khớp với giá trị trong `msal_config.dart`
- Đảm bảo signature hash đúng

### Lỗi "PlatformException"
- Kiểm tra AndroidManifest.xml đã thêm intent-filter chưa
- Rebuild app sau khi sửa manifest

### Backend không nhận được request
- Kiểm tra `kBackendUrl` trong `msal_config.dart`
- Dùng `http://10.0.2.2:8000` cho Android emulator (thay vì localhost)
- Đảm bảo backend đang chạy

## TODO / Cải tiến

- [ ] Parse ID token để lấy thông tin user thực (name, email) thay vì dùng placeholder
- [ ] Thêm refresh token logic
- [ ] Xử lý token expiration
- [ ] Thêm loading indicator khi đăng nhập
- [ ] Secure storage cho token (flutter_secure_storage)
