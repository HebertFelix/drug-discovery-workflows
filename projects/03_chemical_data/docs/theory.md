# Theory — bioactivity curation

## Endpoints

IC50, Ki, Kd and EC50 answer related but non-identical questions. Mixing them
without an explicit model of their relationship invents false precision.

## Logarithmic transforms

For a point IC50 in molar units:

\[
\mathrm{pIC}_{50} = -\log_{10}(\mathrm{IC}_{50}[\mathrm{M}])
\]

Example: 100 nM = \(10^{-7}\) M → pIC50 = 7. Censored values (`<`, `>`) keep
their qualifier and do **not** receive a point pIC50 in this demo.

## Parent structures

Salts and solvents are stripped; the largest organic fragment is retained.
Tautomer enumeration and stereo perception beyond what SMILES already encode
are out of scope for v0.
