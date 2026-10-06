"""Minimal FASTA helpers."""

from __future__ import annotations

from pathlib import Path


def read_fasta(path: Path) -> list[tuple[str, str]]:
    records: list[tuple[str, str]] = []
    header: str | None = None
    chunks: list[str] = []
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        if line.startswith(">"):
            if header is not None:
                records.append((header, "".join(chunks)))
            header = line[1:]
            chunks = []
        else:
            chunks.append(line.upper())
    if header is not None:
        records.append((header, "".join(chunks)))
    return records


def parse_uniprot_header(header: str) -> dict[str, str]:
    # sp|P24941|CDK2_HUMAN ... OS=Homo sapiens OX=9606 GN=CDK2
    parts = header.split(" ", 1)
    ids = parts[0].split("|")
    accession = ids[1] if len(ids) > 1 else parts[0]
    entry_name = ids[2] if len(ids) > 2 else ""
    rest = parts[1] if len(parts) > 1 else ""
    organism = ""
    gene = ""
    if "OS=" in rest:
        organism = rest.split("OS=")[1].split(" OX=")[0].strip()
    if "GN=" in rest:
        gene = rest.split("GN=")[1].split(" ")[0].strip()
    return {
        "accession": accession,
        "entry_name": entry_name,
        "organism": organism,
        "gene": gene,
        "header": header,
    }
