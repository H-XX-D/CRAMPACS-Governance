# Validation Report Template

**Validation ID:**  
**Version:**  
**Validator:**  
**Date:**  

## 1. Scope

State which CRAMPACS workflow, tool, template, or domain overlay is validated.

## 2. Test Batteries

| battery | dataset_or_fixture | seed | expected_result | observed_result | pass_fail | notes |
|---|---|---|---|---|---|---|
| A Known negative |  |  | no high-confidence recurrence |  |  |  |
| B Planted cluster |  |  | planted cluster detected |  |  |  |
| C Duplicate trap |  |  | dependence demotes/collapses |  |  |  |
| D Missing-null trap |  |  | missing evidence flagged |  |  |  |
| E Unit-conversion trap |  |  | conversion drift detected |  |  |  |
| F Inter-rater |  |  | disagreements measured/adjudicated |  |  |  |

## 3. Acceptance Criteria

Minimum:

- no false release on known negative
- planted cluster detected under registered statistic
- duplicate-evidence trap demoted or held
- missing-null trap demoted or held
- unit-conversion trap detected
- reviewer disagreements recorded and adjudicated

## 4. Deviations

List validation deviations and CAPA references.

## 5. Conclusion

Choose one:

- validated_for_pilot
- validated_for_standard_use
- validated_with_limitations
- not_validated

