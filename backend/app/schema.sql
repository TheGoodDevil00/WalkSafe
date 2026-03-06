-- Enable PostGIS extension
CREATE EXTENSION IF NOT EXISTS postgis;

-- Nodes: Represents intersections or points of interest
CREATE TABLE IF NOT EXISTS nodes (
    id BIGSERIAL PRIMARY KEY,
    location GEOGRAPHY(POINT, 4326) NOT NULL,
    osm_id BIGINT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_nodes_location ON nodes USING GIST(location);

-- Edges: Pedestrian pathways with risk attributes
CREATE TABLE IF NOT EXISTS edges (
    id BIGSERIAL PRIMARY KEY,
    source_node BIGINT REFERENCES nodes(id),
    target_node BIGINT REFERENCES nodes(id),
    geometry GEOGRAPHY(LINESTRING, 4326) NOT NULL,
    distance_meters FLOAT GENERATED ALWAYS AS (ST_Length(geometry)) STORED,
    
    -- Risk Factors
    base_risk_score FLOAT DEFAULT 0.0,
    lighting_score FLOAT DEFAULT 0.5,
    terrain_type TEXT,
    
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_edges_geometry ON edges USING GIST(geometry);

-- Incidents
CREATE TABLE IF NOT EXISTS incidents (
    id BIGSERIAL PRIMARY KEY,
    location GEOGRAPHY(POINT, 4326) NOT NULL,
    type TEXT NOT NULL,
    severity INT,
    description TEXT,
    reported_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    verified BOOLEAN DEFAULT FALSE,
    source TEXT
);

CREATE INDEX IF NOT EXISTS idx_incidents_location ON incidents USING GIST(location);

-- Users (Ephemeral)
CREATE TABLE IF NOT EXISTS users (
    id BIGSERIAL PRIMARY KEY,
    user_hash TEXT UNIQUE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
