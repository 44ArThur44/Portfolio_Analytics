-- Migration: create events table for analytics
CREATE TABLE IF NOT EXISTS events (
  id SERIAL PRIMARY KEY,
  ts TIMESTAMPTZ NOT NULL DEFAULT now(),
  ip_hash VARCHAR(128) NOT NULL,
  country VARCHAR(2) NOT NULL DEFAULT 'ZZ',
  user_agent TEXT,
  page VARCHAR(512)
);

CREATE INDEX IF NOT EXISTS idx_events_ts ON events (ts DESC);
CREATE INDEX IF NOT EXISTS idx_events_country ON events (country);
