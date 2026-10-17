import sys
from collections.abc import Callable
from pathlib import Path

import pysam


def pysam_records(path: Path) -> int:
    with pysam.VariantFile(str(path)) as vcf:
        return sum(1 for _ in vcf)


READERS: dict[str, Callable[[Path], int]] = {"pysam": pysam_records}

if __name__ == "__main__":
    print(READERS[sys.argv[1]](Path(sys.argv[2])))
