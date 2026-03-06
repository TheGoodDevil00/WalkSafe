enum SafetyLevel { unsafe, moderate, safe }

class SafetyZone {
  const SafetyZone({
    required this.id,
    required this.latitude,
    required this.longitude,
    required this.safetyScore,
    this.radiusMeters = 120,
  });

  final String id;
  final double latitude;
  final double longitude;
  final int safetyScore;
  final double radiusMeters;

  // Converts a numeric score into one of three safety classes.
  SafetyLevel get safetyLevel {
    if (safetyScore < 40) {
      return SafetyLevel.unsafe;
    }
    if (safetyScore < 70) {
      return SafetyLevel.moderate;
    }
    return SafetyLevel.safe;
  }
}
