# Limitations — Project 01

1. **Simulated data.** Patterns illustrate QC and fitting behavior; they are not evidence about a real target or assay.
2. **Two plates only.** Plate-effect modeling is descriptive (control medians, Z′), not a full mixed-effects analysis.
3. **Technical vs biological replication.** Multiple wells ≠ independent experiments.
4. **IC50 outside range.** Extrapolated potencies are flagged; they must not be quoted as precise SAR values.
5. **Single reader / single wavelength assumption.** Drift, bubbles, precipitation and compound interference are not modeled beyond the planted edge effect and one missing well.
6. **Wald CI.** Relies on local normality of the MLE and may be miscalibrated for sparse or incomplete curves.
7. **Direction of assay.** Normalization assumes signal decreases with activity; flip the formula for the opposite assay polarity.
8. **Not a substitute for Assay Guidance Manual review** when transferring methods to laboratory data.
