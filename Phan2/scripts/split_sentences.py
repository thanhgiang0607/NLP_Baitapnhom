import json
import re
from pathlib import Path

from underthesea import sent_tokenize

ROOT = Path(__file__).resolve().parent.parent
INPUT = ROOT / "data" / "raw" / "khdl_corpus.txt"
OUTPUT = ROOT / "data" / "data.json"
MIN_WORDS = 5


def main():
    raw = INPUT.read_text(encoding="utf-8")
    sentences, seen = [], set()
    for para in raw.split("\n"):
        para = para.strip()
        if not para:
            continue
        for s in sent_tokenize(para):
            s = re.sub(r"\s+", " ", s).strip()
            if len(s.split()) < MIN_WORDS or s in seen:
                continue
            seen.add(s)
            sentences.append(s)

    tasks = [{"id": i, "data": {"text": s}} for i, s in enumerate(sentences, 1)]
    OUTPUT.write_text(json.dumps(tasks, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Đã tách {len(tasks)} câu -> {OUTPUT.relative_to(ROOT)}")
    assert 50 <= len(tasks) <= 100, "Số câu nên nằm trong khoảng 50-100"


if __name__ == "__main__":
    main()
