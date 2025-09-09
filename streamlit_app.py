import 'dart:async';
import 'package:flutter/material.dart';

void main() {
  runApp(const CaffeineApp());
}

class CaffeineApp extends StatelessWidget {
  const CaffeineApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: 'Caffeine Guard',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: const Color(0xFF3E2C25)),
        useMaterial3: true,
        fontFamily: 'Roboto',
      ),
      home: const SplashScreen(),
    );
  }
}

class SplashScreen extends StatefulWidget {
  const SplashScreen({super.key});

  @override
  State<SplashScreen> createState() => _SplashScreenState();
}

class _SplashScreenState extends State<SplashScreen> {
  @override
  void initState() {
    super.initState();
    // Navigate to Home after 3 seconds
    Timer(const Duration(seconds: 3), () {
      if (!mounted) return;
      Navigator.of(context).pushReplacement(
        PageRouteBuilder(
          transitionDuration: const Duration(milliseconds: 600),
          pageBuilder: (_, __, ___) => const HomeScreen(),
          transitionsBuilder: (context, animation, secondaryAnimation, child) {
            final curved = CurvedAnimation(parent: animation, curve: Curves.easeOutCubic);
            return FadeTransition(opacity: curved, child: child);
          },
        ),
      );
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFFF7F3F0),
      body: Center(
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            // Logo
            SizedBox(
              width: 160,
              height: 160,
              child: CustomPaint(
                painter: CoffeeBeanXLogoPainter(),
              ),
            ),
            const SizedBox(height: 20),
            // App name
            const Text(
              'Caffeine Guard',
              style: TextStyle(
                fontSize: 28,
                fontWeight: FontWeight.w700,
                letterSpacing: 0.5,
                color: Color(0xFF3E2C25),
              ),
            ),
            const SizedBox(height: 6),
            const Text(
              'Manage your daily caffeine safely',
              style: TextStyle(
                fontSize: 14,
                color: Color(0xFF6B5B53),
              ),
            ),
          ],
        ),
      ),
    );
  }
}

class HomeScreen extends StatelessWidget {
  const HomeScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Home'),
        backgroundColor: const Color(0xFF3E2C25),
        foregroundColor: Colors.white,
      ),
      body: const Center(
        child: Text(
          'Welcome! (앱 본 화면은 여기에 구성하면 돼요)',
          style: TextStyle(fontSize: 18),
          textAlign: TextAlign.center,
        ),
      ),
    );
  }
}

/// Draws a coffee bean with an X mark over it.
class CoffeeBeanXLogoPainter extends CustomPainter {
  @override
  void paint(Canvas canvas, Size size) {
    final w = size.width;
    final h = size.height;

    // Center and scale
    final center = Offset(w / 2, h / 2);
    final beanWidth = w * 0.68; // pill width
    final beanHeight = h * 0.88; // pill height

    // Bean base
    final beanRect = Rect.fromCenter(
      center: center,
      width: beanWidth,
      height: beanHeight,
    );

    final beanRRect = RRect.fromRectXY(beanRect, beanWidth * 0.5, beanWidth * 0.5);

    final beanPaint = Paint()
      ..color = const Color(0xFF6F4E37) // deep coffee brown
      ..style = PaintingStyle.fill;

    canvas.drawRRect(beanRRect, beanPaint);

    // Bean highlight (curved slit)
    final slitPath = Path();
    final left = beanRect.left + beanWidth * 0.22;
    final right = beanRect.right - beanWidth * 0.22;
    final top = beanRect.top + beanHeight * 0.16;
    final bottom = beanRect.bottom - beanHeight * 0.16;

    slitPath.moveTo(left, top);
    slitPath.quadraticBezierTo(center.dx + beanWidth * 0.06, center.dy, left, bottom);

    final slitPaint = Paint()
      ..color = const Color(0xFF3E2C25)
      ..strokeWidth = beanWidth * 0.10
      ..style = PaintingStyle.stroke
      ..strokeCap = StrokeCap.round;

    canvas.drawPath(slitPath, slitPaint);

    // Subtle top-left highlight
    final highlight = Paint()
      ..shader = RadialGradient(
        colors: [
          const Color(0xFFFFFFFF).withOpacity(0.22),
          const Color(0x00FFFFFF),
        ],
      ).createShader(Rect.fromCircle(center: Offset(center.dx - beanWidth * 0.18, center.dy - beanHeight * 0.18), radius: beanWidth * 0.7));

    canvas.drawRRect(beanRRect, highlight);

    // X mark
    final xPaint = Paint()
      ..color = const Color(0xFFD9534F) // alert red
      ..strokeWidth = beanWidth * 0.14
      ..strokeCap = StrokeCap.round
      ..style = PaintingStyle.stroke;

    final xInset = beanWidth * 0.05;
    final p1 = Offset(beanRect.left + xInset, beanRect.top + xInset);
    final p2 = Offset(beanRect.right - xInset, beanRect.bottom - xInset);
    final p3 = Offset(beanRect.right - xInset, beanRect.top + xInset);
    final p4 = Offset(beanRect.left + xInset, beanRect.bottom - xInset);

    canvas.drawLine(p1, p2, xPaint);
    canvas.drawLine(p3, p4, xPaint);

    // Soft shadow under the logo
    final shadowPaint = Paint()
      ..color = Colors.black.withOpacity(0.10)
      ..maskFilter = const MaskFilter.blur(BlurStyle.normal, 16);
    canvas.drawOval(
      Rect.fromCenter(center: Offset(center.dx, beanRect.bottom + 8), width: beanWidth * 0.9, height: beanHeight * 0.10),
      shadowPaint,
    );
  }

  @override
  bool shouldRepaint(covariant CustomPainter oldDelegate) => false;
}
