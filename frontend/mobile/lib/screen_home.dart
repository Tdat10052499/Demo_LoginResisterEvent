import 'package:flutter/material.dart';
import 'login_screen.dart';
import 'auth_service.dart';

class HomeScreen extends StatelessWidget {
  final String userName;
  const HomeScreen({Key? key, required this.userName}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Home')),
      body: Padding(
        padding: const EdgeInsets.all(24.0),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          crossAxisAlignment: CrossAxisAlignment.center,
          children: [
            Text(
              'Xin chào $userName',
              style: const TextStyle(fontSize: 28, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 24),
            ElevatedButton(
              onPressed: () {
                // Placeholder for event registration feature
                ScaffoldMessenger.of(context).showSnackBar(
                  const SnackBar(content: Text('Chức năng đăng ký sự kiện chưa được xây dựng')),
                );
              },
              child: const Text('Đăng ký sự kiện'),
            ),
            const SizedBox(height: 12),
            ElevatedButton(
              onPressed: () async {
                // Xóa thông tin đăng nhập
                await AuthService.logout();
                
                // Quay lại LoginScreen
                Navigator.of(context).pushReplacement(
                  MaterialPageRoute(builder: (_) => const LoginScreen()),
                );
              },
              style: ElevatedButton.styleFrom(backgroundColor: Colors.red),
              child: const Text('Đăng xuất'),
            ),
          ],
        ),
      ),
    );
  }
}
