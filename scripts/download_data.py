"""Download the UCI Default of Credit Card Clients dataset into data/raw/."""

import hashlib
import io
import urllib.request
import zipfile

from credit_risk.config import load_config


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def main() -> None:
    config = load_config("uci_taiwan")
    source = config["source"]
    raw_dir = config["paths"]["raw_dir"]
    target = raw_dir / source["raw_file"]

    if target.exists():
        if sha256(target.read_bytes()) != source["sha256"]:
            raise ValueError(
                f"{target} exists but its checksum does not match; delete it and rerun."
            )
        print(f"Already present and verified: {target}")
        return

    print(f"Downloading {source['url']}")
    with urllib.request.urlopen(source["url"], timeout=60) as response:
        archive = response.read()
    with zipfile.ZipFile(io.BytesIO(archive)) as zf:
        data = zf.read(source["archive_member"])

    digest = sha256(data)
    if digest != source["sha256"]:
        raise ValueError(
            f"Checksum mismatch: expected {source['sha256']}, got {digest}"
        )

    raw_dir.mkdir(parents=True, exist_ok=True)
    target.write_bytes(data)
    print(f"Saved {target} ({len(data):,} bytes)")


if __name__ == "__main__":
    main()
