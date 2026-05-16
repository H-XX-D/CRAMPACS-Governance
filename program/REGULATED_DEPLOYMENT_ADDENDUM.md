# Regulated Deployment Addendum

**Document ID:** CRAMPS-REGDEP-001  
**Version:** 0.1  
**Status:** Draft procedure

## 1. Purpose

This addendum defines controls required when CRAMPS supports safety, security, regulated research, public agency, financial, clinical, or operational decisions.

## 2. Required Additions

### Records Retention

Define:

- record owner
- retention period
- storage location
- access roles
- archive process
- destruction process

### Access Control

Define:

- data classification
- role-based access
- reviewer access
- external auditor access
- secrets/API-key handling
- access review cadence

### Privacy and Security Review

Required if the package contains:

- personal data
- protected health information
- financial customer data
- security telemetry
- embargoed research data
- proprietary operational data

### Change Control Board

Required for:

- protocol changes after lock
- code changes affecting analysis
- transform changes
- null model changes
- release-language changes
- emergency overrides

### Legal or Compliance Review

Required before:

- public release
- regulator submission
- clinical or safety action
- adverse action or customer-impacting decision
- security attribution claim

### Incident Handling

Open an incident if:

- restricted data is exposed
- package is released with Critical error
- unsupported claim is made externally
- reproduction package is tampered with
- records are lost

## 3. Required Evidence

- data classification record
- access review record
- legal/compliance signoff where applicable
- change-control board minutes
- incident log if applicable
- retention plan

## 4. Boundary

This addendum makes CRAMPS more audit-ready. It does not by itself create legal, regulatory, clinical, safety, or security compliance.

