from pathlib import Path

from vcf_conformance.run import rows, summary

KEYS = ["reader", "version", "file", "expected", "verdict", "records"]


def test_rows_and_summary():
    matrix = rows(Path(__file__).parent / "data")

    assert [list(r) for r in matrix] == [KEYS] * 6
    assert matrix == [
        {
            "reader": reader,
            "version": "4.2",
            "file": "4.2/failed/no_header.vcf",
            "expected": "reject",
            "verdict": "reject",
            "records": None,
        }
        for reader in ("pysam", "cyvcf2", "vcfpy")
    ] + [
        {
            "reader": reader,
            "version": "4.2",
            "file": "4.2/passed/tiny.vcf",
            "expected": "accept",
            "verdict": "accept",
            "records": 2,
        }
        for reader in ("pysam", "cyvcf2", "vcfpy")
    ]
    assert summary(matrix) == ["cyvcf2 4.2 2/2", "pysam 4.2 2/2", "vcfpy 4.2 2/2"]
