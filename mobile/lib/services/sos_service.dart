class SosService {
  Future<void> sendEmergencyAlert() async {
    // Simulates a network call to notify emergency contacts.
    await Future<void>.delayed(const Duration(seconds: 1));
  }
}
