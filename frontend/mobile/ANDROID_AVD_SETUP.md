# Hướng dẫn Test với Android Virtual Device (AVD) trên Android Studio

## 📱 Tổng quan

Android Virtual Device (AVD) là emulator chính thức của Google, được tích hợp sẵn trong Android Studio. Đây là công cụ test phổ biến nhất cho Android development.

---

## 📦 Bước 1: Cài đặt Android Studio

### 1.1. Download Android Studio

1. Truy cập: [https://developer.android.com/studio](https://developer.android.com/studio)
2. Download **Android Studio** (Latest version)
3. File size: ~1GB

### 1.2. Cài đặt Android Studio

1. Chạy file installer
2. Chọn **Standard Installation**
3. Chọn UI theme (Light/Dark)
4. Đợi download Android SDK, Android SDK Platform, Android Virtual Device

**Components sẽ được cài đặt:**
- Android SDK
- Android SDK Platform
- Android SDK Build-Tools
- Android Emulator
- Android SDK Platform-Tools
- Intel x86 Emulator Accelerator (HAXM) hoặc Hyper-V

### 1.3. Kiểm tra cài đặt

Mở Android Studio và kiểm tra:
- **File** → **Settings** (hoặc Ctrl+Alt+S)
- **Appearance & Behavior** → **System Settings** → **Android SDK**
- Xem SDK Path: `C:\Users\<YourName>\AppData\Local\Android\Sdk`

---

## 🔧 Bước 2: Cấu hình Android SDK

### 2.1. Cài đặt SDK Platforms

1. Mở Android Studio
2. **File** → **Settings** → **Android SDK**
3. Tab **SDK Platforms**
4. Tick các Android versions bạn cần (khuyến nghị):

   **Recommended:**
   - ✅ **Android 13.0 (Tiramisu)** - API Level 33
   - ✅ **Android 12.0 (S)** - API Level 31
   - ✅ **Android 11.0 (R)** - API Level 30
   - ✅ **Android 10.0 (Q)** - API Level 29

5. Click **Apply** → **OK**
6. Đợi download (mỗi version ~200-300MB)

### 2.2. Cài đặt SDK Tools

1. Trong **Android SDK**, chuyển sang tab **SDK Tools**
2. Tick các tools sau:

   **Required:**
   - ✅ **Android SDK Build-Tools**
   - ✅ **Android SDK Command-line Tools**
   - ✅ **Android Emulator**
   - ✅ **Android SDK Platform-Tools**
   - ✅ **Intel x86 Emulator Accelerator (HAXM installer)** (cho Intel CPU)
   
   **Optional:**
   - ✅ **Google Play Services**
   - ✅ **Google USB Driver** (cho physical device)

3. Click **Apply** → **OK**

### 2.3. Cài đặt HAXM (Intel) hoặc Hyper-V (AMD)

#### **Cho Intel CPU:**

1. Sau khi download HAXM, vào:
   ```
   C:\Users\<YourName>\AppData\Local\Android\Sdk\extras\intel\Hardware_Accelerated_Execution_Manager
   ```
2. Chạy file `intelhaxm-android.exe`
3. Follow hướng dẫn cài đặt
4. Allocate RAM: 2-4GB

#### **Cho AMD CPU hoặc Windows 11:**

Dùng **Hyper-V** thay vì HAXM:

1. Mở PowerShell **as Administrator**
2. Chạy lệnh:
   ```powershell
   Enable-WindowsOptionalFeature -Online -FeatureName Microsoft-Hyper-V -All
   ```
3. Restart máy

---

## 📱 Bước 3: Tạo Android Virtual Device (AVD)

### 3.1. Mở Device Manager

**Cách 1:**
- Android Studio → Top toolbar → Click icon **Device Manager** (icon điện thoại)

**Cách 2:**
- **Tools** → **Device Manager**

**Cách 3:**
- **View** → **Tool Windows** → **Device Manager**

### 3.2. Create New Virtual Device

1. Click **Create Device** (hoặc nút **+**)

2. **Select Hardware**:
   
   **Recommended devices:**
   - **Pixel 5** - 6.0" 1080x2340, 8GB RAM
   - **Pixel 6** - 6.4" 1080x2400, 8GB RAM
   - **Pixel 7 Pro** - 6.7" 1440x3120, 12GB RAM
   - **Medium Phone** - 6.0" generic device
   
   Click **Next**

3. **Select System Image**:
   
   **Recommended:**
   - **Tiramisu** (API 33) - Android 13.0
   - **S** (API 31) - Android 12.0
   - **R** (API 30) - Android 11.0
   
   **Chọn image có label:**
   - 📦 **x86_64** (cho Intel CPU)
   - 🎮 **Google Play** (có Google Play Store)
   - 🔥 **Google APIs** (có Google services)
   
   **Download nếu chưa có** (click link Download)
   
   Click **Next**

4. **Verify Configuration**:
   
   - **AVD Name**: `Pixel_5_API_33` (hoặc tên bạn thích)
   - **Startup orientation**: Portrait
   - **Graphics**: Automatic (hoặc Hardware - GLES 2.0)
   
   **Advanced Settings** (nếu cần customize):
   - **Boot option**: Cold boot (hoặc Quick boot)
   - **Camera**: 
     - Front: Webcam0 (dùng camera máy bạn)
     - Back: VirtualScene (giả lập)
   - **Network**:
     - Speed: Full
     - Latency: None
   - **Memory and Storage**:
     - RAM: 2048 MB (tối thiểu) - 4096 MB (recommended)
     - VM heap: 256 MB
     - Internal Storage: 2048 MB
     - SD card: 512 MB (optional)
   
   Click **Finish**

### 3.3. Tạo nhiều AVD cho test

Khuyến nghị tạo ít nhất 2-3 devices với cấu hình khác nhau:

1. **Pixel 5 - API 33** (Android 13) - High-end
2. **Medium Phone - API 30** (Android 11) - Mid-range
3. **Small Phone - API 29** (Android 10) - Low-end

---

## 🚀 Bước 4: Khởi động AVD

### 4.1. Start từ Device Manager

1. Mở **Device Manager**
2. Tìm AVD bạn vừa tạo
3. Click nút **▶ (Play)** để start

Emulator sẽ mở trong cửa sổ mới (đợi 30-60 giây lần đầu)

### 4.2. Start từ Command Line

```bash
# List tất cả emulators
flutter emulators

# Hoặc
emulator -list-avds
```

Output:
```
Pixel_5_API_33
Medium_Phone_API_30
```

Start emulator:

```bash
# Cách 1: Dùng Flutter
flutter emulators --launch Pixel_5_API_33

# Cách 2: Dùng emulator command
emulator -avd Pixel_5_API_33
```

### 4.3. Kiểm tra device đã sẵn sàng

```bash
flutter devices
```

Output:
```
Found 4 connected devices:
  sdk gphone64 x86 64 (mobile) • emulator-5554 • android-x64 • Android 13 (API 33)
  Windows (desktop)            • windows       • windows-x64 • Microsoft Windows
  Chrome (web)                 • chrome        • web-javascript • Google Chrome
  Edge (web)                   • edge          • web-javascript • Microsoft Edge
```

Hoặc:

```bash
adb devices
```

Output:
```
List of devices attached
emulator-5554   device
```

---

## 🔐 Bước 5: Cấu hình cho Microsoft SSO

### 5.1. Kiểm tra Google Play Services

1. Trong emulator, mở **Settings**
2. Scroll xuống → **About emulated device**
3. Kiểm tra **Google Play services** version

Nếu không có, bạn cần chọn system image có **Google Play** khi tạo AVD.

### 5.2. Đăng nhập Google Account (Quan trọng!)

1. Trong emulator, mở **Settings**
2. **Accounts** → **Add account** → **Google**
3. Đăng nhập với Google account
4. Accept terms
5. Kiểm tra **Play Store** có hoạt động không

**Lưu ý**: Microsoft SSO cần Google Play Services để hoạt động!

### 5.3. Update AndroidManifest.xml

Mở file `android/app/src/main/AndroidManifest.xml` và thêm intent-filter cho deep linking:

```xml
<manifest xmlns:android="http://schemas.android.com/apk/res/android">
    <application>
        <activity
            android:name=".MainActivity"
            android:exported="true"
            android:launchMode="singleTop"
            android:theme="@style/LaunchTheme"
            android:configChanges="orientation|keyboardHidden|keyboard|screenSize|smallestScreenSize|locale|layoutDirection|fontScale|screenLayout|density|uiMode"
            android:hardwareAccelerated="true"
            android:windowSoftInputMode="adjustResize">
            
            <!-- Standard launcher intent -->
            <intent-filter>
                <action android:name="android.intent.action.MAIN"/>
                <category android:name="android.intent.category.LAUNCHER"/>
            </intent-filter>
            
            <!-- Deep linking for Microsoft SSO -->
            <intent-filter>
                <action android:name="android.intent.action.VIEW" />
                <category android:name="android.intent.category.DEFAULT" />
                <category android:name="android.intent.category.BROWSABLE" />
                <data
                    android:scheme="msauth"
                    android:host="com.example.login_register_event"
                    android:path="/qitkjCObmVXTpHslEaOpznysgEk" />
            </intent-filter>
            
            <meta-data
                android:name="io.flutter.embedding.android.NormalTheme"
                android:resource="@style/NormalTheme" />
        </activity>
        
        <meta-data
            android:name="flutterEmbedding"
            android:value="2" />
    </application>
    
    <!-- Internet permission -->
    <uses-permission android:name="android.permission.INTERNET"/>
</manifest>
```

### 5.4. Verify msal_config.dart

Kiểm tra file `lib/msal_config.dart`:

```dart
// Backend URL cho Android Emulator
const String kBackendUrl = 'http://10.0.2.2:8000';

// Android redirect URI
const String kRedirectUriAndroid = 'msauth://com.example.login_register_event/qitkjCObmVXTpHslEaOpznysgEk';
```

**Giải thích:**
- `10.0.2.2` là IP đặc biệt trong Android Emulator trỏ đến `localhost` của máy host
- Port `8000` là port backend FastAPI đang chạy

---

## ▶️ Bước 6: Run Flutter App trên AVD

### 6.1. Khởi động Backend

Mở terminal và start backend:

```bash
cd c:\Users\tdat1\Demo_LoginResisterEvent\backend
uvicorn app.main:app --reload
```

Kiểm tra backend hoạt động: [http://localhost:8000/docs](http://localhost:8000/docs)

### 6.2. Run Flutter App

Mở terminal mới:

```bash
cd c:\Users\tdat1\Demo_LoginResisterEvent\frontend\mobile
flutter run
```

Flutter sẽ tự động detect emulator và deploy app.

**Hoặc chỉ định device cụ thể:**

```bash
flutter run -d emulator-5554
```

### 6.3. Xem Logs

Trong terminal đang chạy `flutter run`, bạn sẽ thấy realtime logs.

**Hoặc xem logs riêng:**

```bash
flutter logs
```

**Hoặc dùng ADB logcat:**

```bash
adb logcat | findstr flutter
```

---

## 🧪 Bước 7: Test Microsoft SSO Flow

### 7.1. Test Complete Flow

1. **App khởi động**:
   - SplashScreen hiển thị
   - Check user đã đăng nhập chưa
   - Navigate đến LoginScreen (nếu chưa login)

2. **Click "Đăng nhập bằng Microsoft"**:
   - App gọi `flutter_appauth`
   - Browser mở Microsoft login page

3. **Đăng nhập Microsoft**:
   - Nhập email/password Microsoft
   - Accept permissions

4. **Redirect về app**:
   - Browser redirect với msauth:// scheme
   - App nhận ID token
   - Gọi API backend `/auth/sso-login`
   - Lưu user info vào SharedPreferences
   - Navigate đến HomeScreen

5. **Restart app**:
   - App tự động đăng nhập
   - Navigate thẳng đến HomeScreen

### 7.2. Verify Backend Connection

Trong emulator, mở **Chrome** và test:

```
http://10.0.2.2:8000/docs
```

Bạn sẽ thấy FastAPI Swagger UI nếu backend đang chạy.

### 7.3. Test Các Chức Năng Khác

- ✅ Navigation: LoginScreen → HomeScreen
- ✅ Auto-login: Restart app
- ✅ Logout: Clear SharedPreferences
- ✅ Event Registration Form (khi implement)
- ✅ API calls đến backend

---

## 🐛 Bước 8: Debug và Troubleshooting

### 8.1. Enable Developer Options trong Emulator

1. Trong emulator, mở **Settings**
2. **About emulated device**
3. Tap **Build number** 7 lần
4. "You are now a developer!"
5. Quay lại Settings → **System** → **Developer options**

**Enable các options:**
- ✅ **USB debugging** (mặc định đã bật)
- ✅ **Stay awake** (màn hình không tắt khi charge)
- ❌ **Window animation scale** → Off (nhanh hơn)
- ❌ **Transition animation scale** → Off
- ❌ **Animator duration scale** → Off

### 8.2. Debug với Android Studio

1. Mở project Android trong Android Studio:
   ```
   File → Open → c:\Users\tdat1\Demo_LoginResisterEvent\frontend\mobile\android
   ```

2. Set breakpoints trong MainActivity.kt (nếu cần)

3. Run with debugger:
   ```bash
   flutter run --debug
   ```

### 8.3. Common Issues

#### **Issue 1: Emulator không start**

**Symptoms:**
```
PANIC: Cannot find AVD system path. Please define ANDROID_SDK_ROOT
```

**Solution:**

```bash
# Set environment variable
setx ANDROID_SDK_ROOT "C:\Users\<YourName>\AppData\Local\Android\Sdk"
setx ANDROID_HOME "C:\Users\<YourName>\AppData\Local\Android\Sdk"
```

Restart terminal và thử lại.

---

#### **Issue 2: "flutter devices" không thấy emulator**

**Solution:**

```bash
# Kill và restart ADB
adb kill-server
adb start-server

# Check lại
adb devices
flutter devices
```

---

#### **Issue 3: Emulator chậm**

**Solutions:**

1. **Tăng RAM cho AVD:**
   - Device Manager → AVD → Edit (pencil icon)
   - Advanced Settings → RAM: 4096 MB

2. **Enable Hardware Acceleration:**
   - Graphics: Hardware - GLES 2.0

3. **Giảm resolution:**
   - Chọn device nhỏ hơn (Medium Phone thay vì Pixel 7 Pro)

4. **Cold boot thay vì Quick boot:**
   - Advanced Settings → Boot option: Cold boot

---

#### **Issue 4: "Cannot connect to backend"**

**Verify:**

```bash
# Check backend đang chạy
curl http://localhost:8000/docs

# Check từ emulator Chrome
# Trong emulator: http://10.0.2.2:8000/docs
```

**Solution:**

- Đảm bảo backend chạy
- Đảm bảo `msal_config.dart` dùng `10.0.2.2:8000`
- Check firewall không block port 8000

---

#### **Issue 5: "SSO redirect không hoạt động"**

**Verify:**

1. AndroidManifest.xml có intent-filter với scheme `msauth`
2. Redirect URI trong Azure Portal khớp với app
3. Google Play Services đã cài trong emulator
4. Đã đăng nhập Google account trong emulator

**Debug:**

```dart
// Trong login_screen.dart, thêm logs
print('Starting SSO login...');
print('Redirect URI: $redirectUri');
print('Auth result: $result');
```

---

#### **Issue 6: "Accept Android licenses"**

**Solution:**

```bash
flutter doctor --android-licenses
```

Nhấn `y` để accept tất cả licenses.

---

## 📊 Bước 9: Performance Testing

### 9.1. Profile Mode

Build app ở profile mode để test performance:

```bash
flutter run --profile
```

### 9.2. Release Mode

Build production APK:

```bash
flutter build apk --release
```

Install vào emulator:

```bash
adb install build/app/outputs/flutter-apk/app-release.apk
```

### 9.3. Flutter DevTools

Open DevTools để monitor performance:

```bash
flutter pub global activate devtools
flutter pub global run devtools
```

Trong terminal đang run app:

```
# Copy URL và paste vào DevTools
An Observatory debugger and profiler on sdk gphone64 x86 64 is available at: http://127.0.0.1:xxxxx/
```

---

## 🎯 Tips & Best Practices

### 10.1. Emulator Shortcuts

| Shortcut | Action |
|----------|--------|
| **Ctrl + M** | Menu |
| **Ctrl + H** | Home |
| **Ctrl + Backspace** | Back |
| **Ctrl + F11** | Rotate left |
| **Ctrl + F12** | Rotate right |
| **Ctrl + P** | Power button |
| **Ctrl + K** | Volume up |
| **Ctrl + L** | Volume down |

### 10.2. Quick Actions

- **Wipe data**: Device Manager → AVD → ⋮ (More) → Wipe Data
- **Cold boot**: Device Manager → AVD → ⋮ → Cold Boot Now
- **Take screenshot**: Emulator → ... (Extended controls) → Screenshot
- **Record screen**: Extended controls → Record and Playback

### 10.3. Multi-device Testing

Run app trên nhiều emulators cùng lúc:

```bash
# Terminal 1
flutter run -d emulator-5554

# Terminal 2
flutter run -d emulator-5556
```

### 10.4. Snapshot để boot nhanh

1. Start emulator
2. Setup app (login, data, etc.)
3. Emulator → ... → Snapshots → Save snapshot
4. Lần sau boot, emulator restore từ snapshot (rất nhanh!)

---

## ✅ Pre-flight Checklist

Trước khi test, đảm bảo:

- [ ] Android Studio đã cài đặt
- [ ] Android SDK đã setup (API 30-33)
- [ ] AVD đã tạo với Google Play image
- [ ] Emulator đã khởi động thành công
- [ ] `flutter devices` hiển thị emulator
- [ ] Google account đã đăng nhập trong emulator
- [ ] AndroidManifest.xml có intent-filter cho msauth://
- [ ] Backend đang chạy (`http://localhost:8000/docs`)
- [ ] `msal_config.dart` dùng `http://10.0.2.2:8000`
- [ ] Azure Portal đã cấu hình redirect URI với signature hash
- [ ] Test backend từ emulator Chrome: `http://10.0.2.2:8000/docs`

---

## 🚀 Quick Start Guide

Nếu đã setup xong, workflow test nhanh:

```bash
# Terminal 1: Start backend
cd c:\Users\tdat1\Demo_LoginResisterEvent\backend
uvicorn app.main:app --reload

# Terminal 2: Start emulator
flutter emulators --launch Pixel_5_API_33

# Terminal 3: Run app
cd c:\Users\tdat1\Demo_LoginResisterEvent\frontend\mobile
flutter run
```

---

## 📚 Resources

- [Android Emulator Documentation](https://developer.android.com/studio/run/emulator)
- [Flutter + Android Setup](https://docs.flutter.dev/get-started/install/windows#android-setup)
- [AVD Manager Guide](https://developer.android.com/studio/run/managing-avds)
- [ADB Commands](https://developer.android.com/studio/command-line/adb)

---

**Next Steps:**
1. ✅ Cài đặt Android Studio
2. ✅ Setup Android SDK
3. ✅ Tạo AVD với Google Play
4. ✅ Start emulator và đăng nhập Google
5. ✅ Update AndroidManifest.xml
6. ✅ Run `flutter run` và test SSO
7. ✅ Debug và fix issues nếu có

Happy Testing! 🎉
