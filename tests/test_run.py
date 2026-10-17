from pathlib import Path

from vcf_conformance.run import rows, summary

KEYS = ["reader", "version", "file", "expected", "verdict", "records"]


def test_rows_and_summary():
    matrix = rows(Path(__file__).parent / "data")

    assert [list(r) for r in matrix] == [KEYS, KEYS]
    assert matrix == [
        {
            "reader": "pysam",
            "version": "4.2",
            "file": "4.2/failed/no_header.vcf",
            "expected": "reject",
            "verdict": "reject",
            "records": None,
        },
        {
            "reader": "pysam",
            "version": "4.2",
            "file": "4.2/passed/tiny.vcf",
            "expected": "accept",
            "verdict": "accept",
            "records": 2,
        },
    ]
    assert summary(matrix) == ["pysam 4.2 2/2"]
