import sys
import webbrowser
from pathlib import Path

import spacy
from spacy import displacy

ROOT = Path(__file__).resolve().parent.parent
MODEL = ROOT / "models" / "ner_khdl_vi"
HTML = ROOT / "results" / "demo.html"
COLORS = {"PER": "#e74c3c", "ORG": "#3498db", "LOC": "#2ecc71", "MISC": "#f39c12"}


def show(nlp, text, history):
    doc = nlp(text)
    if not doc.ents:
        print("  (không tìm thấy thực thể)")
    for ent in doc.ents:
        print(f"  {ent.label_:<5} {ent.text}")
    history.append(doc)
    HTML.write_text(
        displacy.render(history, style="ent", page=True, options={"colors": COLORS}),
        encoding="utf-8",
    )


def main():
    nlp = spacy.load(MODEL)
    history = []
    if len(sys.argv) > 1:
        for text in sys.argv[1:]:
            print(text)
            show(nlp, text, history)
        webbrowser.open(HTML.as_uri())
        return
    print("Nhập câu (Enter trống để thoát):")
    opened = False
    while True:
        text = input("> ").strip()
        if not text:
            break
        show(nlp, text, history)
        if not opened:
            webbrowser.open(HTML.as_uri())
            opened = True
        else:
            print(f"  → tải lại {HTML.name} trên trình duyệt để xem màu")


if __name__ == "__main__":
    main()
