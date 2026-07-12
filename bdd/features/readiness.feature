Feature: AMS readiness assessment
  The goal is to validate that transition readiness information is collected with evidence
  and role control, so that only complete, valid and authorized assessments are submitted.

  Background:
    Given a readiness assessment exists in draft status

  Scenario: Happy path — Transition Lead submits a complete readiness assessment
    Given a Transition Lead is authenticated
    And all mandatory readiness areas have complete and non-stale evidence
    When the Transition Lead submits the assessment
    Then the assessment is marked as submitted
    And no critical missing information is shown

  Scenario: Missing evidence — submission is blocked
    Given a Transition Lead is authenticated
    And the DR evidence is missing
    When the Transition Lead tries to submit the assessment
    Then the submission is blocked
    And the system displays the missing critical information
    And the assessment remains in draft status

  Scenario: Unauthorized user — Contributor cannot submit the final assessment
    Given a Contributor is authenticated
    And the assessment is complete and valid
    When the Contributor tries to submit the assessment
    Then the submission is denied
    And the assessment remains in draft status

  # Added by change request CR-01 (RFC tool)
  Scenario: RFC — only the Transition Lead can raise an RFC
    Given a Contributor is authenticated
    When the Contributor tries to raise an RFC on the intake
    Then the request is denied
    And no RFC is created

