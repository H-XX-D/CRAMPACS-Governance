# CRAMPACS Governance Gotchas Printout

| Gotcha | Symptom | Fast sanity check |
| --- | --- | --- |
| Coordinate drift | Coordinate changes names, units, or definitions across sources | Write the coordinate formula and units on one line |
| Tolerance creep | Window widens after rows are seen | State tolerance source before scoring |
| Null starvation | Only positive anomalies are included | Find nulls, exclusions, failed replications, non-events |
| Duplicate evidence | Rows trace to one raw data source | Draw source-to-row dependence graph |
| Literature fashion | Many sources inspect same coordinate because it is popular | Add coordinate-fashion bias |
| Time leakage | Later knowledge shaped earlier-looking lock | Compare lock date with source dates |
| Unit trap | Alignment depends on hidden conversion | Recompute normalized values from raw values |
| One-source collapse | Remove one source and result disappears | Leave-one-source-out |
| Negative control failure | Controls also recur | Strengthen null model |
| AI extraction drift | AI summary becomes data | Trace each row to source evidence |
