import '../models/safety_zone.dart';

class SafetyHeatmapService {
  // Static mock data used to visualize safe/moderate/unsafe pockets.
  List<SafetyZone> getMockSafetyZones() {
    return const <SafetyZone>[
      SafetyZone(
        id: 'zone_1',
        latitude: 18.5246,
        longitude: 73.8664,
        safetyScore: 25,
      ),
      SafetyZone(
        id: 'zone_2',
        latitude: 18.5175,
        longitude: 73.8502,
        safetyScore: 35,
      ),
      SafetyZone(
        id: 'zone_3',
        latitude: 18.5311,
        longitude: 73.8597,
        safetyScore: 58,
      ),
      SafetyZone(
        id: 'zone_4',
        latitude: 18.5131,
        longitude: 73.8717,
        safetyScore: 66,
      ),
      SafetyZone(
        id: 'zone_5',
        latitude: 18.5272,
        longitude: 73.8429,
        safetyScore: 82,
      ),
      SafetyZone(
        id: 'zone_6',
        latitude: 18.5067,
        longitude: 73.8563,
        safetyScore: 91,
      ),
    ];
  }
}
