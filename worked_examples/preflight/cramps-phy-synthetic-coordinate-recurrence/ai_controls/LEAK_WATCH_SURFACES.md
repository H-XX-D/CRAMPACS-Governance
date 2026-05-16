# Leak Watch Surfaces

This worked example is synthetic and should contain no private, restricted, or real experimental source data.

Watch these surfaces:

| surface | risk | response |
|---|---|---|
| source-kit boundary | example work spills into reusable templates or policies | stop and move work back into the worked-example folder |
| evidence rows | synthetic rows are mistaken for real evidence | keep `synthetic_status` visible and quarantine from full scoring |
| AI logs | AI adds unsupported claims | rewrite claim language and record the correction |
| handoff | preflight is treated as full assurance | create a separate `CRAMPS-PHY` package before full work |

Run:

```bash
rm -rf /tmp/cramps-phy-worked-example
cp -R worked_examples/preflight/cramps-phy-synthetic-coordinate-recurrence /tmp/cramps-phy-worked-example
python tools/cramps_cli.py leak-scan /tmp/cramps-phy-worked-example
```
