# Successful Framework Patterns

**Document ID:** CRAMPS-RSCH-001  
**Version:** 0.1  
**Status:** Research synthesis  
**Date:** 2026-05-16  
**Purpose:** Identify design patterns CRAMPS should adopt from durable, teachable, and auditable frameworks.

## 1. Sources Reviewed

| Framework | Source | Relevant pattern |
|---|---|---|
| PRISMA 2020 | https://www.prisma-statement.org/prisma-2020 | checklist, expanded checklist, abstract checklist, flow diagrams |
| Cochrane ROB-ME and Handbook | https://www.cochrane.org/authors/handbooks-and-manuals/handbook/current/chapter-13 | missing-evidence risk, planning, signalling questions, judgment categories |
| GRADE | https://www.gradeworkinggroup.org/ | transparent evidence certainty and recommendation strength |
| ISO quality management principles | https://www.iso.org/quality-management/principles | process approach, evidence-based decisions, improvement, leadership |
| NIST AI RMF | https://www.nist.gov/itl/ai-risk-management-framework | voluntary risk framework, companion playbook, consensus process |
| NIST Cybersecurity Framework | https://www.nist.gov/cyberframework/faqs | core outcomes, implementation examples, references, maturity tiers |
| NASA Systems Engineering Handbook | https://ntrs.nasa.gov/archive/nasa/casi.ntrs.nasa.gov/20080008301.pdf | disciplined lifecycle reviews and recursive/iterative engineering processes |
| FDA Quality Systems Approach to cGMP | https://www.fda.gov/regulatory-information/search-fda-guidance-documents/quality-systems-approach-pharmaceutical-current-good-manufacturing-practice-regulations | quality-system model paired with regulatory requirements and risk management |

## 2. Design Lessons

### Lesson 1: A framework needs a small core and supporting artifacts

PRISMA is not just a paper. It has checklists and flow-diagram templates. NIST CSF separates core outcomes, implementation examples, and informative references. CRAMPS should keep the core method compact while giving practitioners checklists, registers, examples, and templates.

CRAMPS adoption:

- core operating manual
- canonical gate map
- control catalog
- evidence package scaffold
- domain packs
- printouts
- workbooks

### Lesson 2: Maturity levels help teams adopt without pretending they are finished

NIST CSF uses tiers that move from informal to adaptive practice. CRAMPS should preserve a similar progression from lowercase preflight to full externally validated packages.

CRAMPS adoption:

| Level | Meaning |
|---|---|
| L1 `cramps-*` | lightweight triage |
| L2 pilot | narrow locked package |
| L3 standard | complete retrospective package |
| L4 regulated | full package plus domain controls |
| L5 externally validated | independent reproduction or external audit |

### Lesson 3: Missing evidence must be treated as a first-class risk

Cochrane emphasizes that missing evidence can bias synthesis when result availability depends on direction, magnitude, or statistical significance. CRAMPS should never treat positive or anomaly-like rows alone as a credible package.

CRAMPS adoption:

- null and non-event rows required
- source flow required
- missing-evidence assessment required
- bias gate can hold release

### Lesson 4: Certainty and action should be separated

GRADE separates evidence certainty from recommendation strength. CRAMPS should separate recurrence evidence tier from the decision requested by a supervisor.

CRAMPS adoption:

- evidence tier table
- decision memo
- prohibited claims
- conditions and limits
- emergency action without tier upgrade

### Lesson 5: Quality systems require ownership and improvement

ISO quality management principles emphasize process, evidence-based decisions, leadership, and improvement. FDA quality-system guidance pairs process controls with risk management and regulatory boundaries. CRAMPS should define owners, evidence records, CAPA, and review cadence.

CRAMPS adoption:

- document control procedure
- release RACI
- CAPA procedure
- register data dictionary
- training matrix
- audit procedure

### Lesson 6: Practical playbooks make frameworks usable

NIST AI RMF has a companion playbook and related implementation resources. CRAMPS should teach "what to do Monday morning," not only define ideals.

CRAMPS adoption:

- deployment playbook
- instructor guide
- learner workbook
- exercises
- package scaffold command
- sidecar command

### Lesson 7: Lifecycle reviews prevent late-stage surprises

NASA systems engineering uses lifecycle and technical reviews across design, development, operation, maintenance, and closeout. CRAMPS should use gates as lifecycle reviews.

CRAMPS adoption:

- G0 charter
- G1 coordinate lock
- G2 source universe
- G3 row integrity
- G4 dependence and bias
- G5 statistical method
- G6 reproducibility
- G7 release

## 3. CRAMPS Framework Design Rules

1. Keep the assurance boundary visible on every artifact.
2. Separate fast preflight from full assurance.
3. Require null and non-event evidence.
4. Use gates as lifecycle reviews.
5. Make every claim trace to an evidence package.
6. Treat missing evidence, dependence, and bias as release risks.
7. Use maturity levels so adoption can start small without overclaiming.
8. Pair every framework principle with a practitioner artifact.
9. Teach the method through exercises, not only policies.
10. Preserve domain humility: CRAMPS supports prioritization, not domain proof.

## 4. Gaps To Watch

| Gap | Risk | CRAMPS control |
|---|---|---|
| Over-formalizing preflight | Teams avoid using the lightweight route | keep `cramps-*` to 1 to 2 days |
| Under-formalizing full packages | Results are not defensible | enforce G0-G7 gates and sidecar blockers |
| Training without assessment | People think attendance equals competence | competency rubric and practical exercise |
| Pretty documents without evidence | Brand hides weak controls | control evidence register and audit procedure |
| Domain-general language too abstract | Teams cannot apply it | domain packs and field examples |
