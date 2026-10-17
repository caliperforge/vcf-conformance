import json
import subprocess
import sys
import tarfile
import urllib.request
from pathlib import Path

from vcf_conformance.readers import READERS

HTS_SPECS_SHA = "510c107ba89aa13113818c9e4fa3071283cb7f7b"
PROJECT = Path(__file__).resolve().parent.parent
HTS_SPECS = PROJECT / ".hts-specs"
MATRIX = PROJECT / "results" / "matrix.jsonl"
VERDICTS = {0: "accept", 1: "reject"}


def fetch() -> Path:
    if not HTS_SPECS.exists():
        url = f"https://codeload.github.com/samtools/hts-specs/tar.gz/{HTS_SPECS_SHA}"
        with urllib.request.urlopen(url) as response, tarfile.open(fileobj=response, mode="r|gz") as tar:
            tar.extractall(HTS_SPECS, filter="data")
    return HTS_SPECS / f"hts-specs-{HTS_SPECS_SHA}" / "test" / "vcf"


def rows(root: Path) -> list[dict]:
    paths = sorted(p for p in root.glob("*/*/*.vcf") if p.parent.name in ("passed", "failed"))
    return [row(reader, root, path) for path in paths for reader in READERS]


def row(reader: str, root: Path, path: Path) -> dict:
    done = subprocess.run(
        [sys.executable, "-m", "vcf_conformance.readers", reader, str(path)],
        capture_output=True,
        check=False,
        text=True,
        cwd=PROJECT,
    )
    verdict = VERDICTS.get(done.returncode, "crash")
    return {
        "reader": reader,
        "version": path.parent.parent.name,
        "file": path.relative_to(root).as_posix(),
        "expected": "reject" if path.parent.name == "failed" else "accept",
        "verdict": verdict,
        "records": int(done.stdout) if verdict == "accept" else None,
    }


def summary(matrix: list[dict]) -> list[str]:
    agreement: dict[tuple[str, str], list[bool]] = {}
    for r in matrix:
        agreement.setdefault((r["reader"], r["version"]), []).append(r["verdict"] == r["expected"])
    return [f"{reader} {version} {sum(agree)}/{len(agree)}" for (reader, version), agree in sorted(agreement.items())]


def main() -> None:
    matrix = rows(fetch())
    MATRIX.parent.mkdir(parents=True, exist_ok=True)
    MATRIX.write_text("".join(json.dumps(r) + "\n" for r in matrix))
    print("\n".join(summary(matrix)))


if __name__ == "__main__":
    main()
