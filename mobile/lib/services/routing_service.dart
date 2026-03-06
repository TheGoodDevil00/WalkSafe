import 'dart:convert';

import 'package:http/http.dart' as http;
import 'package:latlong2/latlong.dart';
import 'package:polyline_codec/polyline_codec.dart';

import '../models/incident_report.dart';
import '../models/osrm_route.dart';
import '../models/route_segment_safety.dart';
import '../models/scored_route.dart';
import 'safety_score_service.dart';

class RoutingService {
  RoutingService({SafetyScoreService? safetyScoreService})
    : _safetyScoreService = safetyScoreService ?? SafetyScoreService();

  static const String _osrmBaseUrl = 'https://router.project-osrm.org';
  final SafetyScoreService _safetyScoreService;

  Future<List<LatLng>> getRoute(LatLng start, LatLng end) async {
    final ScoredRoute? safestRoute = await getSafestRoute(start, end);
    return safestRoute?.points ?? <LatLng>[];
  }

  Future<ScoredRoute?> getSafestRoute(LatLng start, LatLng end) async {
    // Step 1: Build OSRM walking URL and request alternative candidates.
    final Uri uri = Uri.parse(
      '$_osrmBaseUrl/route/v1/foot/'
      '${start.longitude},${start.latitude};'
      '${end.longitude},${end.latitude}'
      '?overview=full&geometries=polyline&alternatives=true&steps=false',
    );

    // Step 2: Call the OSRM public API.
    final http.Response response = await http.get(uri);
    if (response.statusCode != 200) {
      throw Exception(
        'OSRM request failed with status ${response.statusCode}.',
      );
    }

    // Step 3: Parse the JSON payload and read the first route geometry.
    final Map<String, dynamic> payload =
        jsonDecode(response.body) as Map<String, dynamic>;
    final Object? code = payload['code'];
    if (code != 'Ok') {
      throw Exception('OSRM returned code "$code".');
    }

    final List<dynamic>? routeObjects = payload['routes'] as List<dynamic>?;
    if (routeObjects == null || routeObjects.isEmpty) {
      return null;
    }

    // Step 4: Load reports once and score each candidate route by risk.
    final List<IncidentReport> incidentReports = await _safetyScoreService
        .loadIncidentReports();
    final DateTime evaluationTime = DateTime.now();
    final List<ScoredRoute> scoredRoutes = <ScoredRoute>[];

    for (final dynamic routeObject in routeObjects) {
      if (routeObject is! Map<String, dynamic>) {
        continue;
      }

      final OsrmRoute route = OsrmRoute.fromJson(routeObject);
      final List<LatLng> routePoints = _decodePolyline(route.geometry);
      if (routePoints.length < 2) {
        continue;
      }

      final List<RouteSegmentSafety> segments = await _safetyScoreService
          .scoreRouteSegments(
            routePoints,
            reports: incidentReports,
            evaluationTime: evaluationTime,
          );
      if (segments.isEmpty) {
        continue;
      }

      final double totalDistanceMeters = route.distanceMeters > 0
          ? route.distanceMeters
          : segments.fold<double>(
              0,
              (double sum, RouteSegmentSafety segment) =>
                  sum + segment.distanceMeters,
            );

      scoredRoutes.add(
        ScoredRoute(
          points: routePoints,
          segments: segments,
          totalDistanceMeters: totalDistanceMeters,
          averageSafetyScore: _safetyScoreService.calculateAverageSafetyScore(
            segments,
          ),
          totalRisk: _safetyScoreService.calculateRouteRisk(segments),
        ),
      );
    }

    if (scoredRoutes.isEmpty) {
      return null;
    }

    // Step 5: Select the route with minimum risk (distance + safety penalty).
    scoredRoutes.sort((ScoredRoute a, ScoredRoute b) {
      final int riskOrder = a.totalRisk.compareTo(b.totalRisk);
      if (riskOrder != 0) {
        return riskOrder;
      }
      return a.totalDistanceMeters.compareTo(b.totalDistanceMeters);
    });

    return scoredRoutes.first;
  }

  List<LatLng> _decodePolyline(String geometry) {
    final List<List<num>> decodedPoints = PolylineCodec.decode(geometry);
    return decodedPoints
        .where((List<num> point) => point.length >= 2)
        .map(
          (List<num> point) => LatLng(point[0].toDouble(), point[1].toDouble()),
        )
        .toList(growable: false);
  }
}
