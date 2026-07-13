-- AMS Readiness Intake — reproducible seed data
-- Reference date for freshness examples: 2026-07-01
-- Includes valid and invalid (for submission) cases, plus boundary evidence (90 vs 91 days).

-- Users / roles
INSERT INTO user_role (id, username, role) VALUES
  (1, 'alice', 'Transition Lead'),
  (2, 'bob',   'Contributor'),
  (3, 'carol', 'AMS Manager'),
  (4, 'dan',   'Security Officer');

-- Assessments
INSERT INTO assessment (id, name, status, created_date) VALUES
  (1, 'OrderCare - complete',       'draft', '2026-06-20'),
  (2, 'OrderCare - missing DR',     'draft', '2026-06-21'),
  (3, 'OrderCare - stale evidence', 'draft', '2026-06-22');

-- Assessment 1: complete, all evidence fresh (valid / ready case)
INSERT INTO evidence (assessment_id, area, source, owner, freshness_date, category, criticality) VALUES
  (1, 'monitoring',   'Grafana dashboard', 'Ops Team',      '2026-06-15', 'monitoring', 'high'),
  (1, 'DR',           'DR runbook',        'Infra Team',    '2026-06-10', 'continuity', 'high'),
  (1, 'access',       'IAM export',        'Security Team', '2026-06-12', 'access',     'medium'),
  (1, 'integrations', 'API catalog',       'Dev Team',      '2026-06-05', 'integration','high'),
  (1, 'SLA',          'SLA document',      'Service Owner', '2026-06-18', 'sla',        'medium');

-- Assessment 2: missing DR evidence (invalid for submission — negative case)
INSERT INTO evidence (assessment_id, area, source, owner, freshness_date, category, criticality) VALUES
  (2, 'monitoring',   'Grafana dashboard', 'Ops Team',      '2026-06-15', 'monitoring', 'high'),
  (2, 'access',       'IAM export',        'Security Team', '2026-06-12', 'access',     'medium'),
  (2, 'integrations', 'API catalog',       'Dev Team',      '2026-06-05', 'integration','high'),
  (2, 'SLA',          'SLA document',      'Service Owner', '2026-06-18', 'sla',        'medium');

-- Assessment 3: complete areas but DR is stale (91 days); access is exactly 90 days (boundary, NOT stale)
INSERT INTO evidence (assessment_id, area, source, owner, freshness_date, category, criticality) VALUES
  (3, 'monitoring',   'Grafana dashboard', 'Ops Team',      '2026-06-15', 'monitoring', 'high'),
  (3, 'DR',           'Old DR runbook',    'Infra Team',    '2026-04-01', 'continuity', 'high'),   -- 91 days -> stale
  (3, 'access',       'IAM export',        'Security Team', '2026-04-02', 'access',     'medium'),  -- 90 days -> NOT stale (boundary)
  (3, 'integrations', 'API catalog',       'Dev Team',      '2026-06-05', 'integration','high'),
  (3, 'SLA',          'SLA document',      'Service Owner', '2026-06-18', 'sla',        'medium');

-- RFC (CR-01): raised by the Transition Lead, answered by a Contributor with reusable knowledge
INSERT INTO rfc (id, assessment_id, title, content, raised_by, status, created_date) VALUES
  (1, 1, 'Clarify integration dependencies', 'Please list the external integrations of OrderCare.', 1, 'open', '2026-06-25');

INSERT INTO rfc_response (id, rfc_id, author, comment, is_knowledge, created_date) VALUES
  (1, 1, 2, 'OrderCare integrates with PayHub (payments) and ShipFast (logistics).', 1, '2026-06-26');
