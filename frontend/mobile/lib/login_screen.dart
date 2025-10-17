import 'package:flutter/material.dart';
import 'package:flutter_appauth/flutter_appauth.dart';
import 'dart:io' show Platform;
import 'screen_home.dart';
import 'msal_config.dart';
import 'auth_service.dart';

class LoginScreen extends StatefulWidget {
  const LoginScreen({Key? key}) : super(key: key);

  @override
  State<LoginScreen> createState() => _LoginScreenState();
}

class _LoginScreenState extends State<LoginScreen> {
  final TextEditingController _emailController = TextEditingController();
  final TextEditingController _passwordController = TextEditingController();
  bool _isLoading = false;
  final FlutterAppAuth _appAuth = const FlutterAppAuth();

  // Đăng nhập demo (email/password - chỉ dùng test)
  void _login() async {
    setState(() { _isLoading = true; });
    await Future.delayed(const Duration(seconds: 1));
    setState(() { _isLoading = false; });
    final email = _emailController.text.trim();
    final username = email.contains('@') ? email.split('@')[0] : email;
    
    // Lưu thông tin và chuyển màn hình
    await AuthService.saveUserInfo(username, email);
    Navigator.of(context).pushReplacement(
      MaterialPageRoute(builder: (_) => HomeScreen(userName: username)),
    );
  }

  // Đăng nhập Microsoft SSO
  void _loginWithMicrosoft() async {
    setState(() { _isLoading = true; });

    try {
      // Chọn redirect URI dựa trên platform
      String redirectUri = kRedirectUriAndroid;
      if (Platform.isIOS) {
        redirectUri = kRedirectUriIOS;
      }

      // Gọi OAuth flow
      final AuthorizationTokenResponse? result = await _appAuth.authorizeAndExchangeCode(
        AuthorizationTokenRequest(
          kClientId,
          redirectUri,
          serviceConfiguration: const AuthorizationServiceConfiguration(
            authorizationEndpoint: kAuthorizationEndpoint,
            tokenEndpoint: kTokenEndpoint,
            endSessionEndpoint: kEndSessionEndpoint,
          ),
          scopes: kScopes,
        ),
      );

      if (result != null) {
        // Lấy thông tin user từ ID token (decode JWT hoặc gọi Microsoft Graph API)
        // Đơn giản hóa: giả sử lấy được name và email
        final String userName = 'Microsoft User'; // TODO: parse từ result.idToken
        final String userEmail = 'user@microsoft.com'; // TODO: parse từ result.idToken

        // Gửi thông tin lên backend
        await AuthService.sendUserToBackend(userName, userEmail, 'Microsoft');

        // Lưu thông tin local
        await AuthService.saveUserInfo(userName, userEmail);

        // Chuyển sang HomeScreen
        Navigator.of(context).pushReplacement(
          MaterialPageRoute(builder: (_) => HomeScreen(userName: userName)),
        );
      }
    } catch (e) {
      print('Microsoft SSO error: $e');
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Lỗi đăng nhập: $e')),
      );
    } finally {
      setState(() { _isLoading = false; });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Đăng nhập')),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            // Nút đăng nhập Microsoft SSO
            ElevatedButton.icon(
              onPressed: _isLoading ? null : _loginWithMicrosoft,
              icon: const Icon(Icons.login),
              label: const Text('Đăng nhập bằng Microsoft'),
              style: ElevatedButton.styleFrom(
                backgroundColor: Colors.blue,
                foregroundColor: Colors.white,
                minimumSize: const Size(double.infinity, 50),
              ),
            ),
            const SizedBox(height: 24),
            const Divider(),
            const SizedBox(height: 24),
            
            // Đăng nhập thủ công (demo)
            TextField(
              controller: _emailController,
              decoration: const InputDecoration(labelText: 'Email (Demo)'),
            ),
            const SizedBox(height: 16),
            TextField(
              controller: _passwordController,
              decoration: const InputDecoration(labelText: 'Mật khẩu (Demo)'),
              obscureText: true,
            ),
            const SizedBox(height: 24),
            _isLoading
                ? const CircularProgressIndicator()
                : ElevatedButton(
                    onPressed: _login,
                    child: const Text('Đăng nhập Demo'),
                  ),
          ],
        ),
      ),
    );
  }
}
