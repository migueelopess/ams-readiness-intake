-- AMS Readiness Intake — SQLite schema
-- Entities: user_role, assessment, evidence, rfc, rfc_response
-- Aligned with docs/10_data_architecture.md

PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS rfc_response;
DROP TABLE IF EXISTS rfc;
DROP TABLE IF EXISTS evidence;
DROP TABLE IF EXISTS assessment;
DROP TABLE IF EXISTS user_role;

CREATE TABLE user_role (
    id       INTEGER PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    role     TEXT NOT NULL CHECK (role IN ('Transition Lead','AMS Manager','Contributor','Security Officer'))
);

CREATE TABLE assessment (
    id           INTEGER PRIMARY KEY,
    name         TEXT NOT NULL,
    status       TEXT NOT NULL DEFAULT 'draft' CHECK (status IN ('draft','submitted')),
    created_date TEXT NOT NULL
);

CREATE TABLE evidence (
    id             INTEGER PRIMARY KEY,
    assessment_id  INTEGER NOT NULL REFERENCES assessment(id),
    area           TEXT NOT NULL CHECK (area IN ('monitoring','DR','access','integrations','SLA')),
    source         TEXT NOT NULL,
    owner          TEXT NOT NULL,
    freshness_date TEXT NOT NULL,
    category       TEXT,
    criticality    TEXT CHECK (criticality IN ('high','medium','low') OR criticality IS NULL)
);

-- Added by change request CR-01
CREATE TABLE rfc (
    id            INTEGER PRIMARY KEY,
    assessment_id INTEGER NOT NULL REFERENCES assessment(id),
    title         TEXT NOT NULL,
    content       TEXT NOT NULL,
    raised_by     INTEGER NOT NULL REFERENCES user_role(id),
    status        TEXT NOT NULL DEFAULT 'open' CHECK (status IN ('open','answered')),
    created_date  TEXT NOT NULL
);

CREATE TABLE rfc_response (
    id           INTEGER PRIMARY KEY,
    rfc_id       INTEGER NOT NULL REFERENCES rfc(id),
    author       INTEGER NOT NULL REFERENCES user_role(id),
    comment      TEXT NOT NULL,
    is_knowledge INTEGER NOT NULL DEFAULT 0 CHECK (is_knowledge IN (0,1)),
    created_date TEXT NOT NULL
);
