import json
import re
import time
import urllib.parse
import urllib.request
from pathlib import Path

from underthesea import sent_tokenize

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "data" / "raw"
SRC_DIR = RAW / "sources"
SELECTION = RAW / "selection.json"
CORPUS = RAW / "khdl_corpus.txt"
SOURCES_MD = RAW / "sources.md"

API = "https://vi.wikipedia.org/w/api.php"
STOP_SECTIONS = r"\n== (Tham khảo|Xem thêm|Liên kết ngoài|Chú thích|Đọc thêm) =="


def fetch(title):
    out = SRC_DIR / f"{title}.json"
    if out.exists():
        return
    params = {"action": "query", "prop": "extracts|revisions", "explaintext": 1, "rvprop": "ids|timestamp",
              "redirects": 1, "format": "json", "titles": title}
    req = urllib.request.Request(API + "?" + urllib.parse.urlencode(params),
                                 headers={"User-Agent": "NLP-student-coursework/1.0"})
    out.write_bytes(urllib.request.urlopen(req, timeout=30).read())
    time.sleep(5)


def page_of(title):
    return list(json.load(open(SRC_DIR / f"{title}.json", encoding="utf-8"))["query"]["pages"].values())[0]


def sentences(title):
    text = re.split(STOP_SECTIONS, page_of(title)["extract"])[0]
    out = []
    for para in text.split("\n"):
        para = para.strip()
        if para and not para.startswith("="):
            out += [re.sub(r"\s+", " ", s).strip() for s in sent_tokenize(para)]
    return out


def main():
    SRC_DIR.mkdir(parents=True, exist_ok=True)
    selection = json.loads(SELECTION.read_text(encoding="utf-8"))
    groups, table, total = [], [], 0
    for title, prefixes in selection.items():
        fetch(title)
        sents = sentences(title)
        chosen = []
        for pre in prefixes:
            hits = [s for s in sents if s.startswith(pre)]
            if len(hits) != 1:
                raise ValueError(f"{title}: '{pre}' khớp {len(hits)} câu")
            chosen.append(hits[0])
        groups.append(" ".join(chosen))
        total += len(chosen)
        p = page_of(title)
        rev = p["revisions"][0]
        url = "https://vi.wikipedia.org/wiki/" + urllib.parse.quote(p["title"].replace(" ", "_"))
        table.append(f"| {p['title']} | {len(chosen)} | {url} | "
                     f"[{rev['revid']}](https://vi.wikipedia.org/w/index.php?oldid={rev['revid']}) ({rev['timestamp'][:10]}) |")

    CORPUS.write_text("\n\n".join(groups) + "\n", encoding="utf-8")
    SOURCES_MD.write_text(
        "# Nguồn dữ liệu\n\n"
        "Toàn bộ câu trong `khdl_corpus.txt` được trích nguyên văn từ **Wikipedia tiếng Việt** (giấy phép CC BY-SA 4.0), "
        "tải qua MediaWiki API ngày 2026-11-09 bằng `scripts/fetch_wikipedia.py`. Văn bản gốc lưu trong `sources/*.json`, "
        "danh sách câu được chọn lưu trong `selection.json`. Tiêu chí chọn: liên quan KHDL/AI, chứa thực thể "
        "(người, tổ chức, thuật toán, công cụ, bộ dữ liệu, độ đo).\n\n"
        f"Tổng: **{total} câu** từ **{len(selection)} bài viết**.\n\n"
        "| Bài viết | Số câu | URL | Phiên bản (revid) |\n|---|---|---|---|\n" + "\n".join(table) + "\n",
        encoding="utf-8")
    print(f"Chọn {total} câu từ {len(selection)} bài")


if __name__ == "__main__":
    main()
