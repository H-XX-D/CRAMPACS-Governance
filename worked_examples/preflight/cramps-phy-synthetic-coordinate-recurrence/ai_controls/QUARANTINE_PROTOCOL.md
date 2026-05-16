# Quarantine Protocol

Quarantine this worked example if:

- real source data is added
- a private or restricted file is copied in
- synthetic rows are described as real evidence
- the preflight is presented as a full `CRAMPS-PHY` result
- additional preflight agents are deployed against the one-agent rule

Run:

```bash
rm -rf /tmp/cramps-phy-worked-example
cp -R worked_examples/preflight/cramps-phy-synthetic-coordinate-recurrence /tmp/cramps-phy-worked-example
python tools/cramps_cli.py quarantine /tmp/cramps-phy-worked-example --reason "<reason>"
```

Quarantine does not delete artifacts. It marks the package as no-release and no-escalation until a reviewer clears the issue.
