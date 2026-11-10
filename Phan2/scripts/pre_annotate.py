import json
from collections import Counter
import random
import re
import string
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

GAZETTEER = {
    "PER": ["Geoffrey Everest Hinton", "Geoffrey Hinton", "Hinton", "Yoshua Bengio", "Bengio", "Yann LeCunn",
            "Yann LeCun", "Yann Le Cun", "LeCun", "David Rumelhart", "Terrence Sejnowski", "James McClelland",
            "David Ackley", "Terry Sejnowski", "Laurens van der Maaten", "Alex Krizhevsky", "Krizhevsky",
            "Ilya Sutskever", "Sutskever", "John Hopfield", "Jen-Hsun Huang", "Fei-Fei Li", "Arthur Samuel",
            "Walter Pitts", "Warren McCulloch", "Frank Rosenblatt", "Corinna Cortes", "Cortes",
            "Vladimir N. Vapnik", "Vladimir Vapnik", "Vapnik", "Sepp Hochreiter", "Hochreiter",
            "Jürgen Schmidhuber", "Schmidhuber", "Garry Kasparov", "Lee Sedol", "Masahiko Fukushima",
            "Kunihiko Fukushima", "Ciresan", "Andrew Ng", "James MacQueen", "Hugo Steinhaus", "Stuart Lloyd",
            "Edward W. Forgy", "Guido van Rossum", "Jeff Dean", "Kim"],
    "ORG": ["OpenAI", "Sama", "Stack Overflow", "Check Point Research", "Tập đoàn Teradata", "Seisint Inc.",
            "Tập đoàn LexisNexis", "LexisNexis", "ChoicePoint, Inc.", "Google DeepMind", "Google Brain", "Google",
            "Cơ quan An ninh Quốc gia Hoa Kỳ", "NSA", "Trung tâm Dữ liệu Utah", "EBay", "Amazon",
            "Đại học Toronto", "Viện Vector", "Carnegie Mellon", "CIFAR", "DNNresearch Inc.", "IBM", "Stanford",
            "NYU", "Atomwise", "Facebook", "Baidu", "ACM", "AT&T Labs", "Bell Labs", "Meta AI", "Meta",
            "Linux Foundation", "PyTorch Foundation", "Uber", "Hugging Face", "Microsoft", "NVIDIA", "AMD",
            "Apple", "Reddit", "GitHub", "Parallel Distributed Processing"],
    "LOC": ["San Francisco", "California", "Toronto", "Anh", "Canada", "Seoul", "London", "New York",
            "thung lũng Silicon"],
    "ALGO": ["máy Boltzmann", "t-SNE", "perceptron", "Support Vector Machine", "SVM", "Long Short-Term Memory",
             "LSTM", "LeNet-5", "LeNet", "AlexNet", "AlphaGo", "AlphaZero", "GPT3.5", "Neocognitron", "MapReduce",
             "DALL-E 3", "DALL·E 2", "Whisper", "AtomNet", "DeepFace", "Deep Blue", "CNN", "ANN", "YOLO", "R-CNN",
             "U-Net", "V-Net", "ResNet", "SORT", "bộ lọc Kalman", "thuật toán Hungarian", "GPT-4", "PCA",
             "Phân tích thành phần chính", "k -means", "Lloyd-Forgy", "Vapnik-Chervonenkis", "OpenAI Codex", "Codex"],
    "TOOL": ["ChatGPT Plus", "ChatGPT", "GPT Builder", "Python 0.9.0", "Python 2.7", "Python", "C++", "C",
             "MATLAB", "ABC", "DBC 1012", "HPCC", "High-Performance Computing Cluster", "Apache Hadoop", "Linux",
             "PyTorch Lightning", "PyTorch", "Pytorch", "Torch", "Tesla Autopilot", "Pyro", "Transformers",
             "Catalyst", "Caffe2", "Convolutional Architecture for Fast Feature Embedding",
             "The Open Neural Network Exchange", "ONNX", "NumPy", "SciPy", "Matplotlib", "Biopython", "Astropy",
             "TensorFlow", "Keras", "Scikit-learn", "Cython", "Numba", "LLVM", "Jython", "Java", "Django",
             "Pylons", "Pyramid", "TurboGears", "web2py", "Tornado", "Flask", "Bottle", "Zope", "CUDA", "ROCm",
             "Metal Framework", "DistBelief", "Wolfram Alpha", "Microsoft Word", "Google Docs"],
    "DATASET": ["ImageNet", "MNIST", "PASCAL VOC", "COCO", "EyePACS-1"],
    "METRIC": ["độ chuẩn xác trung bình", "trung bình độ chuẩn xác trung bình", "mean average precision",
               "average precision", "average recall", "độ bao phủ trung bình", "Độ chuẩn xác", "độ chuẩn xác", "độ bao phủ",
               "precision–recall", "precision", "recall", "Điểm F1", "điểm F1", "ROC", "AUC", "tỷ lệ lỗi top-5",
               "Lỗi top-5", "độ chính xác top-1", "Độ chính xác top-5", "top-5", "độ nhạy", "độ đặc hiệu",
               "độ chính xác", "tỉ lệ chính xác", "intersection over union", "IoU", "mAP", "AP50", "AP75", "AP",
               "AR", "sai số toàn phương trung bình", "Mean squared error", "MSE", "sai số root-mean-square",
               "RMSE", "độ lệch root-mean-square", "RMSD", "entropy chéo", "hàm mất mát Dice",
               "Dice coefficient", "Độ phức tạp", "perplexity", "BLEU", "BiLingual Evaluation Understudy",
               "NIST", "ma trận nhầm lẫn", "confusion matrix"],
}

RULES = {
    "Anh": lambda text, s, e: text[e:].startswith(" và Canada"),
    "AP": lambda text, s, e: "COCO" in text or "Trung bình AP" in text,
    "AR": lambda text, s, e: text[s - 2:s] == ", ",
    "độ chính xác": lambda text, s, e: "%" in text[e:e + 20] or text[e:].startswith(" được nâng cao"),
}

WORD_CHARS = set(string.ascii_letters + string.digits + "ÀÁÂÃÈÉÊÌÍÒÓÔÕÙÚÝàáâãèéêìíòóôõùúýĂăĐđĨĩŨũƠơƯư"
                 "ẠạẢảẤấẦầẨẩẪẫẬậẮắẰằẲẳẴẵẶặẸẹẺẻẼẽẾếỀềỂểỄễỆệỈỉỊịỌọỎỏỐốỒồỔổỖỗỘộỚớỜờỞởỠỡỢợỤụỦủỨứỪừỬửỮữỰựỲỳỴỵỶỷỸỹ-")


def find_entities(text):
    terms = sorted(((t, lab) for lab, ts in GAZETTEER.items() for t in ts), key=lambda x: -len(x[0]))
    taken = [False] * len(text)
    ents = []
    for term, label in terms:
        for m in re.finditer(re.escape(term), text):
            s, e = m.start(), m.end()
            if s > 0 and text[s - 1] in WORD_CHARS or e < len(text) and text[e] in WORD_CHARS:
                continue
            if any(taken[s:e]) or (term in RULES and not RULES[term](text, s, e)):
                continue
            taken[s:e] = [True] * (e - s)
            ents.append((s, e, label))
    return sorted(ents)


TO_TEACHER = {"PER": "PER", "ORG": "ORG", "LOC": "LOC",
              "ALGO": "MISC", "TOOL": "MISC", "DATASET": "MISC", "METRIC": "MISC", "MISC": "MISC"}

SNAPSHOT = ROOT / "data" / "export" / "ls_snapshot_v1.json"
PUNCT = r"[,.;:()\"“”–—…\[\]•]"

REL_RULES = [
    ("phát_triển", lambda a, o, b: o == "của" and a == "MISC" and b in ("PER", "ORG"), True),
    ("làm_việc_tại", lambda a, o, b: o == "của" and a == "PER" and b == "ORG"),
    ("thuộc_về", lambda a, o, b: re.search(r"(^|\s)của$", o) and a == "ORG" and b == "ORG"),
    ("phát_triển", lambda a, o, b: a == "MISC" and b in ("PER", "ORG") and re.search(r"(^|\s)(do|bởi)$", o), True),
    ("làm_việc_tại", lambda a, o, b: a == "PER" and b == "ORG" and re.search(r"(^|\s)(tại|ở)$", o)),
    ("nằm_ở", lambda a, o, b: a == "ORG" and b == "LOC" and re.search(r"(^|\s)(tại|ở)$", o)),
    ("phát_triển", lambda a, o, b: a in ("PER", "ORG") and b == "MISC"
     and re.search(r"(phát triển|giới thiệu|đề xuất|tạo ra|phát hành|ra mắt|công bố|xây dựng|phát minh)", o)),
    ("sử_dụng", lambda a, o, b: a == "MISC" and b == "MISC" and "được sử dụng" not in o
     and re.search(r"(sử dụng|dùng|dựa trên)( \S+){0,2}$", o)),
    ("cộng_sự", lambda a, o, b: a == "PER" and b == "PER" and o in ("và", "cùng", "cùng với")),
]


def snapshot_entities():
    if not SNAPSHOT.exists():
        return {}
    out = {}
    for item in json.loads(SNAPSHOT.read_text(encoding="utf-8")):
        res = item["annotations"][0]["result"]
        out[item["data"]["text"]] = [(r["value"]["start"], r["value"]["end"], r["value"]["labels"][0])
                                     for r in res if r["type"] == "labels"]
    return out


def o_chunks(text, ents):
    covered = [False] * len(text)
    for s, e, _ in ents:
        covered[s:e] = [True] * (e - s)
    chunks, i = [], 0
    while i < len(text):
        if covered[i] or re.match(PUNCT, text[i]):
            i += 1
            continue
        j = i
        while j < len(text) and not covered[j] and not re.match(PUNCT, text[j]):
            j += 1
        seg = text[i:j]
        lead = len(seg) - len(seg.lstrip())
        core = seg.strip()
        if re.search(r"\w", core):
            chunks.append((i + lead, i + lead + len(core), "O"))
        i = j
    return chunks


def find_relations(text, spans):
    rels = []
    for k in range(len(spans) - 2):
        a, o, b = spans[k], spans[k + 1], spans[k + 2]
        if a[2] == "O" or o[2] != "O" or b[2] == "O":
            continue
        trig = text[o[0]:o[1]]
        if a[1] > o[0] or o[1] > b[0] or re.search(PUNCT, text[a[1]:b[0]]):
            continue
        for rule in REL_RULES:
            label, cond = rule[0], rule[1]
            if cond(a[2], trig, b[2]):
                src, dst = (b, a) if len(rule) == 3 else (a, b)
                rels.append((src, dst, label))
                break
    return rels


def ls_result(text, spans, rels):
    rid = lambda: "".join(random.choices(string.ascii_letters + string.digits, k=10))
    ids = {sp: rid() for sp in spans}
    res = [{"value": {"start": s, "end": e, "text": text[s:e], "labels": [lab]}, "id": ids[(s, e, lab)],
            "from_name": "label", "to_name": "text", "type": "labels", "origin": "manual"} for s, e, lab in spans]
    res += [{"from_id": ids[a], "to_id": ids[b], "type": "relation", "direction": "right", "labels": [lab]}
            for a, b, lab in rels]
    return res


def main():
    random.seed(0)
    tasks = json.loads((ROOT / "data" / "data.json").read_text(encoding="utf-8"))
    human = snapshot_entities()
    pre, mock = [], []
    ent_count, rel_count, n_o, n_human = Counter(), Counter(), 0, 0
    for t in tasks:
        text = t["data"]["text"]
        if text in human:
            n_human += 1
            raw = human[text]
        else:
            raw = find_entities(text)
        ents = [(s, e, TO_TEACHER[lab]) for s, e, lab in raw if lab in TO_TEACHER]
        spans = sorted(ents + o_chunks(text, ents))
        rels = find_relations(text, spans)
        ent_count.update(lab for *_, lab in ents)
        rel_count.update(lab for *_, lab in rels)
        n_o += len(spans) - len(ents)
        result = ls_result(text, spans, rels)
        pre.append({"data": t["data"], "predictions": [{"model_version": "v2", "result": result}]})
        mock.append({"id": t["id"], "data": t["data"],
                     "annotations": [{"id": t["id"], "completed_by": 1, "result": result, "was_cancelled": False}]})

    (ROOT / "data" / "data_preannotated.json").write_text(json.dumps(pre, ensure_ascii=False, indent=2), "utf-8")
    out = ROOT / "data" / "export" / "MOCK_export.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(mock, ensure_ascii=False), "utf-8")
    print(f"Lấy từ nhãn người gán: {n_human} câu")
    print("Thực thể:", dict(ent_count), "| cụm O:", n_o)
    print("Quan hệ gợi ý:", dict(rel_count), "| tổng:", sum(rel_count.values()))


if __name__ == "__main__":
    main()
