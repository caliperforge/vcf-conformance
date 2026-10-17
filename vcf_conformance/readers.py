import sys
from collections.abc import Callable
from pathlib import Path

import pysam
import vcfpy
from cyvcf2 import VCF


def pysam_records(path: Path) -> int:
    with pysam.VariantFile(str(path)) as vcf:
        return sum(1 for _ in vcf)


def cyvcf2_records(path: Path) -> int:
    return sum(1 for _ in VCF(str(path)))


def vcfpy_records(path: Path) -> int:
    with vcfpy.Reader.from_path(path) as reader:
        return sum(1 for _ in reader)


READERS: dict[str, Callable[[Path], int]] = {
    "pysam": pysam_records,
    "cyvcf2": cyvcf2_records,
    "vcfpy": vcfpy_records,
}

if __name__ == "__main__":
    print(READERS[sys.argv[1]](Path(sys.argv[2])))
