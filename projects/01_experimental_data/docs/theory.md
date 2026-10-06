# Theory — concentration–response and assay QC

## Scientific question

Do the plate readings support a reliable comparison of compound potency under the
declared assay design?

## Readout and controls

This demo uses a simulated absorbance-like signal in relative fluorescence /
absorbance units (**RFU**). Vehicle (**NEG**) controls estimate the uninhibited
baseline; reference-inhibitor (**POS**) controls estimate the fully inhibited
reference. Buffer wells are excluded from fitting.

## Z′ factor

\[
Z' = 1 - \frac{3(\sigma_{\mathrm{neg}} + \sigma_{\mathrm{pos}})}{|\mu_{\mathrm{neg}} - \mu_{\mathrm{pos}}|}
\]

Z′ summarizes separation of controls on a plate. It is a QC diagnostic, not a
proof that sample IC50 values are biologically meaningful.

## Percent response

With signal decreasing upon activity:

\[
\%\mathrm{response} = 100 \times \frac{y - \mathrm{median}(y_{\mathrm{pos}})}{\mathrm{median}(y_{\mathrm{neg}}) - \mathrm{median}(y_{\mathrm{pos}})}
\]

Vehicle ≈ 100%; reference inhibition ≈ 0%. The normalization uses **per-plate**
control medians after exclusion of flagged edge-control wells.

## Four-parameter logistic (4PL)

Let \(x = \log_{10}(c)\) with \(c\) in molar units:

\[
y(x) = b + \frac{t - b}{1 + 10^{(x - L)\,h}}
\]

where \(t\) = top (low-concentration asymptote), \(b\) = bottom (high-concentration
asymptote), \(L = \log_{10}(\mathrm{IC}_{50})\), \(h\) = Hill slope (> 0 for a
decreasing inhibition-style curve in percent response).

**IC50 definition used here:** the concentration at the inflection of this fitted
model on the log-concentration axis (mid-response between estimated top and
bottom). Estimates outside the tested concentration window are flagged and must
not be reported with unwarranted precision.

## Independence

Wells on the same plate share liquid-handling and reader effects. Technical
replicates are retained as observations for curve shape but are **not** treated
as independent biological experiments. Approximate Wald intervals from the fit
covariance describe parameter uncertainty under the model, not between-experiment
biological CI.

## References

1. Assay Guidance Manual — Assay Operations for SAR Support.
2. Assay Guidance Manual — Data Standardization for Results Management.
