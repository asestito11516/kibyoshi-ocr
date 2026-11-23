import sys
from pathlib import Path
import requests


def fetch_book(pid):
    manifest_url = f"https://www.dl.ndl.go.jp/api/iiif/{pid}/manifest.json"

    print(f"Fetching manifest for {pid}...")

    response = requests.get(manifest_url)
    response.raise_for_status()

    manifest = response.json()

    output_dir = Path("data") / "raw" / pid
    output_dir.mkdir(parents=True, exist_ok=True)

    canvases = manifest["sequences"][0]["canvases"]

    print(f"Found {len(canvases)} pages.")

    for i, canvas in enumerate(canvases, start=1):
        image_url = canvas["images"][0]["resource"]["@id"]

        print(f"Downloading page {i}/{len(canvases)}...")

        image_response = requests.get(image_url)
        image_response.raise_for_status()

        output_path = output_dir / f"page_{i:03}.jpg"

        with open(output_path, "wb") as f:
            f.write(image_response.content)

    print(f"Done. Pages saved to {output_dir}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python scripts/fetch_book.py <PID>")
        sys.exit(1)

    fetch_book(sys.argv[1])