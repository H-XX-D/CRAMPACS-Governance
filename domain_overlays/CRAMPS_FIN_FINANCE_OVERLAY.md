# CRAMPS-FIN Finance Overlay

**Aliases:** CRAMPS-F, CRAMPS-FIN  
**Domain:** Finance, fraud, market surveillance, credit, operational risk, and model risk

## Definition

CRAMPS-FIN tests whether weak financial, fraud, risk, market, or operational anomalies recur at pre-specified financial coordinates more often than expected under a registered market, customer, or operational null model.

## Coordinate Families

- Asset, instrument, issuer, sector, counterparty, desk.
- Price level, spread, volatility, liquidity, tenor, maturity.
- Time of day, trading session, settlement window, reporting period.
- Transaction amount, velocity, merchant category, account age.
- Network position, entity cluster, wallet, device, IP, geography.
- Credit score band, adverse action reason, delinquency window.
- Model version, feature, threshold, override reason.

## Eligible Rows

- Fraud alerts.
- Suspicious activity signals.
- Market surveillance residuals.
- Model drift events.
- Credit model anomalies.
- Liquidity stress near-misses.
- Operational loss events.
- Null alerts and cleared investigations.
- Backtests with no breach.

## Null and Non-Events

Nulls include:

- Investigated alerts cleared as false positive.
- Comparable accounts or trades without event.
- Backtesting periods without breach.
- Monitored thresholds not crossed.
- Control portfolios without anomaly.

## Dependence Hazards

- Same market data vendor.
- Same trading calendar.
- Same customer population.
- Same fraud rule engine.
- Same alert suppression rule.
- Same model feature store.
- Same desk or strategy.
- Same regulatory report.
- Same vendor model.

## Bias Hazards

- Survivorship bias.
- Backtest overfitting.
- Look-ahead bias.
- Data snooping.
- Regime shift.
- Vendor data revisions.
- Corporate-action adjustment drift.
- Alert triage bias.
- Feedback loops from prior controls.

## Null-Model Requirements

Minimum confirmatory null:

- Preserve market regime, calendar, asset universe, customer exposure, transaction volume, and alert opportunity.

Preferred null:

- Time-blocked, entity-blocked, and regime-aware nulls with holdout periods and leakage tests.

## Standards Anchors

- Federal Reserve SR 11-7 and OCC 2011-12 model risk management guidance for model governance.
- OCC Model Risk Management handbook for supervisory expectations.
- BCBS 239 for risk data aggregation and reporting.
- FFIEC IT examination guidance for technology and operational controls.
- SEC Regulation SCI where market systems integrity applies.
- SEC cybersecurity disclosure rules where public-company cyber risk disclosure is implicated.
- FINRA AI and market-supervision guidance where broker-dealer use applies.
- GLBA, FCRA, ECOA, BSA/AML, sanctions, and local privacy laws where applicable.

## Checksum Additions

- Market data vendor and snapshot.
- Price timestamp.
- Corporate action adjustment version.
- Currency conversion source.
- Trading calendar.
- Model inventory ID.
- Feature store snapshot.
- Alert rule hash.
- Case-management export hash.

## Claim Limits

CRAMPS-FIN can prioritize risk, fraud, market, or model-drift coordinates. It cannot establish legal fraud, market manipulation, credit discrimination, regulatory breach, or trading signal validity without domain-standard investigation and legal/compliance review.

