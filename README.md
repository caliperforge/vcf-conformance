# vcf-conformance
How VCF readers disagree on the same files: a conformance matrix across htslib/bcftools, pysam, cyvcf2, noodles, htsjdk and vcfpy

Readers: pysam 0.24.1, cyvcf2 0.34.0, vcfpy 0.14.2.

Files: `test/vcf` of [hts-specs](https://github.com/samtools/hts-specs) at commit `510c107ba89aa13113818c9e4fa3071283cb7f7b`, fetched into `.hts-specs/` on first run.

Run: `uv run python -m vcf_conformance.run` writes `results/matrix.jsonl` and prints `<reader> <version> <agree>/<total>` per reader and VCF version.

Test: `uv run pytest`
