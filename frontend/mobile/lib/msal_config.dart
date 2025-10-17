// Cấu hình Microsoft SSO
// Bạn cần thay thế các giá trị placeholder sau khi đăng ký app trên Azure Portal

const String kClientId = 'YOUR_AZURE_CLIENT_ID'; // Client ID từ Azure Portal
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
const String kBackendUrl = 'http://localhost:8000'; // Thay bằng URL backend thực tế
