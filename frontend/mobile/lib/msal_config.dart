// Cấu hình Microsoft SSO
// Bạn cần thay thế các giá trị placeholder sau khi đăng ký app trên Azure Portal

const String kClientId = 'f0f9e0b2-d6ff-40c0-b0b5-9b6a9acf4abc'; // Client ID từ Azure Portal
const String kRedirectUriAndroid = 'msauth://com.example.login_register_event/qitkjCObmVXTpHslEaOpznysgEk';
const String kRedirectUriIOS = 'msauth.com.example.loginRegisterEvent://auth';

// Microsoft endpoints
const String kAuthorizationEndpoint = 'https://login.microsoftonline.com/common/oauth2/v2.0/authorize';
const String kTokenEndpoint = 'https://login.microsoftonline.com/common/oauth2/v2.0/token';
const String kEndSessionEndpoint = 'https://login.microsoftonline.com/common/oauth2/v2.0/logout';

// Scopes cần thiết
const List<String> kScopes = [
  'openid',
  'profile',
  'email',
  'User.Read',
];

// Backend API endpoint
// Android Emulator: dùng 10.0.2.2 để trỏ đến localhost của máy host
// iOS Simulator/Web: dùng localhost
// Device thật: dùng IP của máy (ví dụ: http://192.168.1.x:8000)
// Android Emulator: 10.0.2.2, Web/iOS Simulator: localhost
const String kBackendUrl = 'http://10.0.2.2:8000';
