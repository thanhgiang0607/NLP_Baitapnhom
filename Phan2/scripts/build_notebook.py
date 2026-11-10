import nbformat as nbf
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
md, code = nbf.v4.new_markdown_cell, nbf.v4.new_code_cell

cells = [
    md("# NER văn bản Khoa học dữ liệu với spaCy\n"
       "Quy trình theo `B5/spacy.ipynb`: nhãn **PER / ORG / LOC / MISC / O** như mẫu của thầy; **Label Studio export → spacy_train.json → train `spacy.blank('vi')` → test**, "
       "bổ sung chia train/test và đánh giá **Precision / Recall / F1 theo từng thực thể** (slide 09 – Evaluation of NER).\n\n"
       "Dữ liệu: 97 câu trích từ Wikipedia tiếng Việt (xem `data/raw/sources.md`).\n\n"
       "> Đổi `INPUT_FILE` thành file export thật của nhóm. `MOCK_export.json` chỉ là dữ liệu giả lập từ gazetteer để chạy thử."),
    code('INPUT_FILE = "data/export/annotation.json"\n'
         'OUTPUT_FILE = "data/spacy_train.json"\n'
         'LANG = "vi"\n'
         'N_EPOCHS = 30\n'
         'TEST_RATIO = 0.2\n'
         'SEED = 42\n'
         'import os; os.chdir(os.path.abspath(".."))  if os.path.basename(os.getcwd()) == "notebooks" else None'),
    md("## 1. Chuyển file export Label Studio → spacy_train.json (giống code của thầy)"),
    code('import json\n\n'
         'with open(INPUT_FILE, "r", encoding="utf-8") as f:\n'
         '    data = json.load(f)\n\n'
         'spacy_data = []\n'
         'for item in data:\n'
         '    text = item["data"]["text"]\n'
         '    entities = []\n'
         '    annotation = item["annotations"][0]\n'
         '    for res in annotation["result"]:\n'
         '        if res["type"] == "labels":\n'
         '            entities.append([res["value"]["start"], res["value"]["end"], res["value"]["labels"][0]])\n'
         '    spacy_data.append({"text": text, "entities": entities})\n\n'
         'with open(OUTPUT_FILE, "w", encoding="utf-8") as f:\n'
         '    json.dump(spacy_data, f, ensure_ascii=False, indent=2)\n'
         'print("✅ Done! Saved:", OUTPUT_FILE, "| số câu:", len(spacy_data))'),
    md("## 2. Đọc lại, bỏ nhãn `O`, thống kê nhãn"),
    code('from collections import Counter\n\n'
         'with open(OUTPUT_FILE, "r", encoding="utf-8") as f:\n'
         '    data = json.load(f)\n\n'
         'spacy_data = []\n'
         'for item in data:\n'
         '    entities = [(s, e, lab) for s, e, lab in item["entities"] if lab != "O"]\n'
         '    spacy_data.append((item["text"], {"entities": entities}))\n\n'
         'label_count = Counter(lab for _, ann in spacy_data for *_, lab in ann["entities"])\n'
         'print("Số câu:", len(spacy_data), "| Số thực thể:", sum(label_count.values()))\n'
         'print(dict(label_count.most_common()))\n'
         'print(spacy_data[1])'),
    md("## 3. Kiểm tra khớp biên token (nguyên nhân cảnh báo W030 trong notebook của thầy)\n"
       "Thực thể không khớp ranh giới token sẽ bị spaCy **bỏ qua** khi train."),
    code('import spacy, warnings\n'
         'warnings.filterwarnings("ignore", message=r"\\[W030\\]")\n\n'
         'def check_alignment(lang):\n'
         '    nlp_tmp = spacy.blank(lang)\n'
         '    bad = []\n'
         '    for text, ann in spacy_data:\n'
         '        doc = nlp_tmp.make_doc(text)\n'
         '        bad += [(text[s:e], lab) for s, e, lab in ann["entities"] if doc.char_span(s, e) is None]\n'
         '    return bad\n\n'
         'for lang in ["vi", "xx"]:\n'
         '    bad = check_alignment(lang)\n'
         '    print(f"{lang}: {len(bad)} thực thể lệch biên", bad)'),
    md("## 4. Chia train / test"),
    code('import random\n'
         'random.seed(SEED)\n'
         'shuffled = spacy_data[:]\n'
         'random.shuffle(shuffled)\n'
         'n_test = max(1, int(len(shuffled) * TEST_RATIO))\n'
         'test_data, train_data = shuffled[:n_test], shuffled[n_test:]\n'
         'print("Train:", len(train_data), "câu | Test:", len(test_data), "câu")'),
    md("## 5. Train NER với `spacy.blank` (giống vòng lặp của thầy, thêm shuffle)"),
    code('from spacy.training import Example\n'
         'from spacy.util import minibatch, compounding\n\n'
         'def train_ner(lang, train_data, n_epochs=N_EPOCHS, verbose=True):\n'
         '    nlp = spacy.blank(lang)\n'
         '    ner = nlp.add_pipe("ner")\n'
         '    for _, ann in train_data:\n'
         '        for *_, label in ann["entities"]:\n'
         '            ner.add_label(label)\n'
         '    examples = [Example.from_dict(nlp.make_doc(t), a) for t, a in train_data]\n'
         '    optimizer = nlp.initialize(lambda: examples)\n'
         '    for epoch in range(n_epochs):\n'
         '        random.shuffle(examples)\n'
         '        losses = {}\n'
         '        for batch in minibatch(examples, size=compounding(4.0, 32.0, 1.001)):\n'
         '            nlp.update(batch, sgd=optimizer, drop=0.2, losses=losses)\n'
         '        if verbose and (epoch + 1) % 5 == 0:\n'
         '            print(f"Epoch {epoch+1}, Losses: {losses}")\n'
         '    return nlp\n\n'
         'random.seed(SEED); spacy.util.fix_random_seed(SEED)\n'
         'nlp = train_ner(LANG, train_data)\n'
         'nlp.to_disk(f"models/ner_khdl_{LANG}")'),
    md("## 6. Đánh giá trên tập test — Precision / Recall / F1 (theo thực thể)"),
    code('import pandas as pd\n\n'
         'def evaluate(nlp, data):\n'
         '    examples = [Example.from_dict(nlp.make_doc(t), a) for t, a in data]\n'
         '    return nlp.evaluate(examples)\n\n'
         'scores = evaluate(nlp, test_data)\n'
         'print(f"TỔNG  P={scores[\'ents_p\']:.3f}  R={scores[\'ents_r\']:.3f}  F1={scores[\'ents_f\']:.3f}")\n'
         'test_count = Counter(lab for _, a in test_data for *_, lab in a["entities"])\n'
         'per_type = pd.DataFrame(scores["ents_per_type"]).T.rename(columns={"p": "Precision", "r": "Recall", "f": "F1"})\n'
         'per_type["Support(test)"] = [test_count.get(l, 0) for l in per_type.index]\n'
         'per_type = per_type.round(3).sort_index()\n'
         'os.makedirs("results", exist_ok=True)\n'
         'per_type.to_csv(f"results/ner_per_type_{LANG}.csv")\n'
         'json.dump({k: scores[k] for k in ["ents_p", "ents_r", "ents_f", "ents_per_type"]},\n'
         '          open(f"results/ner_metrics_{LANG}.json", "w"), ensure_ascii=False, indent=2)\n'
         'per_type'),
    md("## 7. So sánh tokenizer `vi` (pyvi) và `xx`"),
    code('rows = []\n'
         'for lang in ["vi", "xx"]:\n'
         '    random.seed(SEED); spacy.util.fix_random_seed(SEED)\n'
         '    m = nlp if lang == LANG else train_ner(lang, train_data, verbose=False)\n'
         '    s = evaluate(m, test_data)\n'
         '    rows.append({"Tokenizer": lang, "Lệch biên": len(check_alignment(lang)),\n'
         '                 "Precision": round(s["ents_p"], 3), "Recall": round(s["ents_r"], 3), "F1": round(s["ents_f"], 3)})\n'
         'compare = pd.DataFrame(rows); compare.to_csv("results/ner_compare_tokenizer.csv", index=False)\n'
         'compare'),
    md("## 8. Phân tích lỗi trên tập test (gold vs dự đoán)"),
    code('def ents_of(text, ann):\n'
         '    return {(text[s:e], lab) for s, e, lab in ann["entities"]}\n\n'
         'n_err = 0\n'
         'for text, ann in test_data:\n'
         '    gold = ents_of(text, ann)\n'
         '    pred = {(e.text, e.label_) for e in nlp(text).ents}\n'
         '    if gold != pred:\n'
         '        n_err += 1\n'
         '        print("📝", text)\n'
         '        print("   Thiếu (FN):", sorted(gold - pred))\n'
         '        print("   Thừa/sai (FP):", sorted(pred - gold))\n'
         'print(f"\\n{n_err}/{len(test_data)} câu test có lỗi")'),
    md("## 9. Test với câu mới (giống phần `# test` của thầy)"),
    code('tests = [\n'
         '    "Năm 2017, Andrew Ng rời Baidu và làm việc tại Stanford.",\n'
         '    "Nhóm nghiên cứu của Google Brain dùng TensorFlow và Python để huấn luyện mạng LSTM.",\n'
         '    "Mạng LeNet của Yann LeCun đạt độ chính xác cao trên tập MNIST.",\n'
         '    "OpenAI có trụ sở tại San Francisco và phát triển ChatGPT.",\n'
         '    "Mô hình YOLO được đánh giá bằng mAP và IoU trên bộ dữ liệu COCO.",\n'
         ']\n'
         'for s in tests:\n'
         '    doc = nlp(s)\n'
         '    print(s)\n'
         '    for ent in doc.ents:\n'
         '        print("   ", ent.text, "→", ent.label_)'),
    code('from spacy import displacy\n'
         'displacy.render(nlp(tests[2]), style="ent", jupyter=True)'),
    md("## 10. Quan hệ giữa các thực thể (Relation)\n"
       "Đọc các cạnh `type == \"relation\"` trong file export: mỗi quan hệ nối 2 thực thể (`from_id` → `to_id`)."),
    code('import matplotlib.pyplot as plt\n'
         'import numpy as np\n\n'
         'with open(INPUT_FILE, "r", encoding="utf-8") as f:\n'
         '    raw = json.load(f)\n\n'
         'rel_rows = []\n'
         'cooc = Counter()\n'
         'ENT_TYPES = ["PER", "ORG", "LOC", "MISC"]\n'
         'for item in raw:\n'
         '    res = item["annotations"][0]["result"]\n'
         '    spans = {r["id"]: (r["value"]["text"], r["value"]["labels"][0]) for r in res if r["type"] == "labels"}\n'
         '    types = sorted({lab for _, lab in spans.values() if lab in ENT_TYPES})\n'
         '    for i, a in enumerate(types):\n'
         '        for b in types[i:]:\n'
         '            cooc[(a, b)] += 1\n'
         '    for r in res:\n'
         '        if r["type"] == "relation" and r["from_id"] in spans and r["to_id"] in spans:\n'
         '            (h, ht), (t, tt) = spans[r["from_id"]], spans[r["to_id"]]\n'
         '            rel_rows.append({"Chủ thể": h, "Loại CT": ht, "Quan hệ": (r.get("labels") or ["?"])[0],\n'
         '                             "Đối tượng": t, "Loại ĐT": tt})\n\n'
         'rel_df = pd.DataFrame(rel_rows)\n'
         'rel_df.to_csv("results/relations.csv", index=False)\n'
         'print("Tổng số quan hệ:", len(rel_df))\n'
         'print(rel_df["Quan hệ"].value_counts().to_string())\n'
         'rel_df.head(15)'),
    md("## 11. Bản đồ tương quan (correlation map)\n"
       "- **Trái:** số quan hệ giữa từng cặp loại thực thể (hàng = chủ thể, cột = đối tượng)\n"
       "- **Phải:** số câu mà hai loại thực thể cùng xuất hiện (đồng xuất hiện)"),
    code('def heat(ax, M, title):\n'
         '    ax.imshow(M, cmap="Blues")\n'
         '    ax.set_xticks(range(4), ENT_TYPES); ax.set_yticks(range(4), ENT_TYPES)\n'
         '    for i in range(4):\n'
         '        for j in range(4):\n'
         '            ax.text(j, i, int(M[i, j]), ha="center", va="center",\n'
         '                    color="white" if M[i, j] > M.max() / 2 else "black")\n'
         '    ax.set_title(title)\n\n'
         'idx = {t: i for i, t in enumerate(ENT_TYPES)}\n'
         'R = np.zeros((4, 4))\n'
         'for _, row in rel_df.iterrows():\n'
         '    if row["Loại CT"] in idx and row["Loại ĐT"] in idx:\n'
         '        R[idx[row["Loại CT"]], idx[row["Loại ĐT"]]] += 1\n'
         'C = np.zeros((4, 4))\n'
         'for (a, b), n in cooc.items():\n'
         '    C[idx[a], idx[b]] = C[idx[b], idx[a]] = n\n\n'
         'fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))\n'
         'heat(axes[0], R, "Số quan hệ: chủ thể → đối tượng")\n'
         'axes[0].set_ylabel("Chủ thể"); axes[0].set_xlabel("Đối tượng")\n'
         'heat(axes[1], C, "Số câu đồng xuất hiện")\n'
         'plt.tight_layout(); plt.savefig("results/correlation_map.png", dpi=150); plt.show()'),
    md("## 12. Đồ thị quan hệ giữa các thực thể"),
    code('import networkx as nx\n\n'
         'G = nx.DiGraph()\n'
         'for _, row in rel_df.iterrows():\n'
         '    G.add_node(row["Chủ thể"], t=row["Loại CT"]); G.add_node(row["Đối tượng"], t=row["Loại ĐT"])\n'
         '    G.add_edge(row["Chủ thể"], row["Đối tượng"], label=row["Quan hệ"])\n'
         'COLORS = {"PER": "#e74c3c", "ORG": "#3498db", "LOC": "#2ecc71", "MISC": "#f39c12"}\n'
         'plt.figure(figsize=(14, 10))\n'
         'pos = nx.spring_layout(G, k=0.9, seed=SEED)\n'
         'nx.draw_networkx_nodes(G, pos, node_color=[COLORS.get(G.nodes[n]["t"], "#999") for n in G], node_size=600, alpha=0.85)\n'
         'nx.draw_networkx_labels(G, pos, font_size=8)\n'
         'nx.draw_networkx_edges(G, pos, arrows=True, arrowsize=12, edge_color="#888")\n'
         'nx.draw_networkx_edge_labels(G, pos, edge_labels=nx.get_edge_attributes(G, "label"), font_size=6)\n'
         'for t, c in COLORS.items():\n'
         '    plt.scatter([], [], c=c, label=t)\n'
         'plt.legend(loc="lower left"); plt.axis("off")\n'
         'plt.title("Đồ thị quan hệ thực thể (KHDL)")\n'
         'plt.savefig("results/relation_graph.png", dpi=150, bbox_inches="tight"); plt.show()'),
]

nb = nbf.v4.new_notebook(cells=cells, metadata={"kernelspec": {"name": "python3", "display_name": "Python 3", "language": "python"}})
out = ROOT / "NER_KHDL.ipynb"
nbf.write(nb, out)
print("Saved", out)
