import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:shared_preferences/shared_preferences.dart';
import 'msal_config.dart';

class AuthService {
  // Lưu thông tin user vào local storage
  static Future<void> saveUserInfo(String name, String email) async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString('user_name', name);
    await prefs.setString('user_email', email);
    await prefs.setBool('is_logged_in', true);
  }

  // Kiểm tra user đã đăng nhập chưa
  static Future<bool> isLoggedIn() async {
    final prefs = await SharedPreferences.getInstance();
    return prefs.getBool('is_logged_in') ?? false;
  }

  // Lấy thông tin user từ local storage
  static Future<Map<String, String?>> getUserInfo() async {
    final prefs = await SharedPreferences.getInstance();
    return {
      'name': prefs.getString('user_name'),
      'email': prefs.getString('user_email'),
    };
  }

  // Đăng xuất
  static Future<void> logout() async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.clear();
  }

  // Gửi thông tin user lên backend sau khi đăng nhập SSO
  static Future<void> sendUserToBackend(String name, String email, String provider) async {
    try {
      final response = await http.post(
        Uri.parse('$kBackendUrl/auth/sso-login'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({
          'username': email.split('@')[0],
          'email': email,
          'password': 'dummy', // Backend có thể bỏ qua hoặc dùng token
        }),
      );

      if (response.statusCode == 200) {
        print('User saved to backend successfully');
      } else {
        print('Failed to save user: ${response.body}');
      }
    } catch (e) {
      print('Error sending user to backend: $e');
    }
  }
}
