import 'package:latlong2/latlong.dart';

class RouteSegmentSafety {
  const RouteSegmentSafety({
    required this.start,
    required this.end,
    required this.distanceMeters,
    required this.safetyScore,
    required this.incidentRisk,
    required this.timeOfDayRisk,
    required this.lightingLevel,
    required this.crowdDensity,
    required this.distanceWeight,
    required this.safetyPenalty,
    required this.risk,
  });

  final LatLng start;
  final LatLng end;
  final double distanceMeters;

  // Normalized segment safety score from 0 (unsafe) to 100 (safe).
  final double safetyScore;

  // Factor contributions used by the scoring engine.
  final double incidentRisk;
  final double timeOfDayRisk;
  final double lightingLevel;
  final double crowdDensity;

  // Risk formula terms:
  // risk = distance_weight + safety_penalty
  final double distanceWeight;
  final double safetyPenalty;
  final double risk;
}
