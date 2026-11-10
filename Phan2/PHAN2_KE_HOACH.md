# PHẦN 2: NER + Label Studio trên văn bản Khoa học dữ liệu

## 0. Trạng thái

| # | Yêu cầu | Trạng thái | Kết quả |
|---|---------|------------|---------|
| 1 | Thu thập văn bản KHDL (50–100 câu) | ✅ Xong | 97 câu trích nguyên văn từ 21 bài Wikipedia tiếng Việt |
| 2 | Script tách câu → `data.json` | ✅ Xong | `scripts/split_sentences.py` → `data/data.json` |
| 3 | Host Label Studio qua IP LAN, gán nhãn Entity + Relation | ✅ Xong | `http://192.168.1.25:8080`, project `NLP_Nhóm1_v2`, 97/97 câu |
| 4 | Export → chạy script spaCy (B5) | ✅ Xong | `data/export/annotation.json` → `NER_KHDL.ipynb`, F1 ≈ 0.77 |
| 5 | Tổng hợp kết quả vào slide + demo | ⏳ Còn lại | Bố cục và kịch bản demo: `SLIDE_BO_CUC.md` |

---

## 1. Bài toán

**Nhận dạng thực thể có tên (Named Entity Recognition – NER)** trên văn bản tiếng Việt thuộc lĩnh vực Khoa học dữ liệu (KHDL).

- **Đầu vào:** một câu tiếng Việt, ví dụ
  > Vladimir Vapnik giới thiệu thuật toán SVM tại Bell Labs.
- **Đầu ra:** các cụm từ là thực thể, kèm loại của chúng:
  > **Vladimir Vapnik** → PER · **SVM** → MISC · **Bell Labs** → ORG

Bài toán phụ là **trích xuất quan hệ (Relation Extraction)**: tìm mối liên hệ giữa các thực thể, ví dụ `Vladimir Vapnik —phát_triển→ SVM`. Từ các quan hệ này nhóm vẽ **bản đồ tương quan** (thực thể loại nào hay liên kết với loại nào).

Trọng tâm khi trình bày là **NER**: gán nhãn, huấn luyện và đánh giá mô hình. Quan hệ là phần mở rộng theo yêu cầu của thầy.

---

## 2. Các khái niệm cần biết

| Khái niệm | Giải thích ngắn |
|---|---|
| **Thực thể (entity)** | Cụm từ chỉ một đối tượng cụ thể: người, tổ chức, địa điểm, thuật toán… |
| **NER** | Tìm vị trí (biên) và loại của từng thực thể trong câu |
| **Nhãn PER / ORG / LOC** | Người / Tổ chức / Địa điểm |
| **Nhãn MISC** | Thực thể khác. Ở đây gồm thuật toán, mô hình, công cụ, bộ dữ liệu, độ đo, giải thưởng (SVM, PyTorch, ImageNet, F1, Giải Turing) |
| **Nhãn O (Outside)** | Phần không phải thực thể: cụm động từ, giới từ ("giới thiệu thuật toán", "tại"). Nhóm vẫn tô O để không bỏ sót chữ nào và giữ cấu trúc câu |
| **Quan hệ (relation)** | Liên kết có hướng giữa 2 thực thể: chủ thể → đối tượng |
| **Span `[start, end, label]`** | Cách lưu thực thể theo vị trí ký tự trong câu, định dạng spaCy dùng để train |
| **Tokenizer** | Bộ tách câu thành từ (token). `vi` dùng thư viện pyvi, gộp từ ghép tiếng Việt ("học_máy"). `xx` tách theo khoảng trắng và dấu câu |
| **Lệch biên (misalignment, cảnh báo W030)** | Biên thực thể không trùng biên token, ví dụ pyvi gộp "A." thành 1 token nên thực thể "A" không khớp. spaCy bỏ qua các thực thể này khi train |
| **Pre-annotation (gán sẵn)** | Máy gán nhãn trước bằng từ điển và luật, người duyệt và sửa. Giúp gán nhanh và đồng nhất |
| **Luật mẫu (Hearst pattern)** | Mẫu câu chỉ ra quan hệ, ví dụ "X **của** Y", "X **do** Y", "PER **tại** ORG" (slide 10 của thầy) |
| **Precision (P)** | Trong các thực thể mô hình đoán ra, bao nhiêu % đúng |
| **Recall (R)** | Trong các thực thể thật, mô hình tìm được bao nhiêu % |
| **F1** | Trung bình điều hoà của P và R: `2PR / (P + R)` |
| **Đánh giá theo thực thể** | Dự đoán chỉ tính là đúng khi **trùng cả biên và nhãn** (slide 09: "per entity, not per token") |
| **Train/test split** | Chia dữ liệu: phần train để học, phần test (mô hình chưa thấy) để chấm điểm |
| **Epoch** | Một lượt mô hình học hết tập train |

---

## 3. Tổng quan quy trình

```
Wikipedia ──► Chọn câu ──► Tách câu ──► Gán sẵn ──► Label Studio ──► Export ──► spaCy ──► Đánh giá
 (21 bài)    (97 câu)    data.json    (máy)      (nhóm duyệt,      JSON      train     P/R/F1,
                                                  qua LAN)                   30 epoch  bản đồ tương quan
```

| Bước | Công cụ | Đầu vào | Đầu ra |
|---|---|---|---|
| 1. Thu thập | MediaWiki API, `fetch_wikipedia.py` | Tên 21 bài | `data/raw/khdl_corpus.txt`, `sources.md` |
| 2. Tách câu | underthesea, `split_sentences.py` | corpus | `data/data.json` |
| 3a. Gán sẵn | `pre_annotate.py` | `data.json` | `data/data_preannotated.json` |
| 3b. Gán nhãn | Label Studio | file gán sẵn | nhãn đã duyệt (97/97) |
| 4. Export | Label Studio → JSON | | `data/export/annotation.json` |
| 5. Train + đánh giá | spaCy, `NER_KHDL.ipynb` | `annotation.json` | `models/ner_khdl_vi`, `results/*` |
| 6. Demo | `demo_ner.py` | câu mới | thực thể + `results/demo.html` |

---

## 4. Dữ liệu

- **Nguồn:** 21 bài **Wikipedia tiếng Việt** (giấy phép CC BY-SA 4.0) về học máy, học sâu, framework, mô hình ngôn ngữ và độ đo đánh giá. Danh sách đầy đủ kèm URL và phiên bản (revid): `data/raw/sources.md`.
- **Quy mô:** 97 câu, mỗi câu trích **nguyên văn**, không tự viết.
- **Tiêu chí chọn câu:** liên quan KHDL, có nhiều thực thể (người, tổ chức, thuật toán, độ đo).
- **Thống kê nhãn** (sau khi nhóm duyệt):

| Nhãn | Ví dụ | Số lượng |
|------|-------|---------:|
| PER | Geoffrey Hinton, Yann LeCun | 47 |
| ORG | OpenAI, Google Brain, Bell Labs | 44 |
| LOC | San Francisco, Seoul | 8 |
| MISC | SVM, PyTorch, ImageNet, F1, Giải Turing | 196 |
| O | "của", "do", "đã được tích hợp vào" | 377 |

- **Thống kê quan hệ:** 46 quan hệ trong 35 câu

| Quan hệ | Ví dụ | Số lượng |
|---------|-------|---------:|
| phát_triển | OpenAI → DALL-E 3 | 25 |
| cộng_sự | Corinna Cortes → Vladimir Vapnik | 9 |
| sử_dụng | ChatGPT → GPT3.5 | 5 |
| làm_việc_tại | Yann LeCun → AT&T Labs | 3 |
| thuộc_về | PyTorch → Linux Foundation | 3 |
| nằm_ở | OpenAI → San Francisco | 1 |
| đánh_giá_bằng | (có trong cấu hình, chưa dùng) | 0 |

- **Chia dữ liệu:** train 78 câu, test 19 câu (80/20, seed 42). Tập test có 59 thực thể.

---

## 5. Các bước làm chi tiết

### Bước 1 — Thu thập văn bản (`scripts/fetch_wikipedia.py`)
1. Gọi MediaWiki API lấy văn bản thuần của từng bài. Mỗi lần gọi cách nhau 5 giây để không bị chặn. Bài nào đã tải thì bỏ qua. Lưu vào `data/raw/sources/*.json`.
2. Cắt bỏ các mục cuối bài ("Tham khảo", "Xem thêm", "Liên kết ngoài"…).
3. Chọn câu theo `data/raw/selection.json`: mỗi bài có danh sách **đầu câu** cần lấy. Script tìm câu khớp và báo lỗi nếu một đầu câu khớp 0 hoặc nhiều hơn 1 câu, để không chọn nhầm.
4. Ghi `khdl_corpus.txt` (các câu đã chọn) và `sources.md` (bảng nguồn).

### Bước 2 — Tách câu (`scripts/split_sentences.py`)
1. Đọc corpus, tách câu từng đoạn bằng `underthesea.sent_tokenize` (thư viện NLP tiếng Việt).
2. Làm sạch khoảng trắng thừa. Bỏ câu ngắn dưới 5 từ và câu trùng.
3. Kiểm tra số câu nằm trong khoảng 50–100 (được 97).
4. Xuất `data/data.json` theo định dạng import của Label Studio:
   ```json
   [{"id": 1, "data": {"text": "Vào tháng 3 năm 2023, OpenAI ..."}}]
   ```

### Bước 3a — Gán sẵn bằng máy (`scripts/pre_annotate.py`)
1. **Thực thể:** dùng từ điển (gazetteer) các tên đã biết, ví dụ "PyTorch" → MISC, "OpenAI" → ORG. Có luật riêng cho từ dễ nhầm: "Anh" chỉ là LOC khi đứng trước "và Canada"; "AP" chỉ là độ đo khi câu nói về COCO; "độ chính xác" chỉ là độ đo khi có "%" gần đó.
2. **Nhãn O:** phần còn lại của câu được cắt thành các cụm O theo vị trí thực thể và dấu câu.
3. **Quan hệ:** xét bộ ba liền nhau (thực thể – cụm O – thực thể) và áp luật mẫu:
   - `MISC của PER/ORG`, `MISC do/bởi PER/ORG` → PER/ORG **phát_triển** MISC
   - `PER/ORG giới thiệu/phát triển/công bố… MISC` → **phát_triển**
   - `PER tại/ở ORG` → **làm_việc_tại**; `ORG tại/ở LOC` → **nằm_ở**; `ORG của ORG` → **thuộc_về**
   - `PER và/cùng PER` → **cộng_sự**; `MISC sử dụng/dựa trên MISC` → **sử_dụng**
4. Xuất `data/data_preannotated.json` dưới dạng *predictions* để Label Studio hiển thị sẵn. Máy gán được 288 thực thể, 377 cụm O và 45 quan hệ.

### Bước 3b — Gán nhãn trên Label Studio
1. Chạy `label-studio start --host 0.0.0.0 --port 8080`. `0.0.0.0` cho phép máy khác cùng mạng truy cập qua `http://192.168.1.25:8080`. Thành viên ở xa dùng Tailscale.
2. Tạo project `NLP_Nhóm1_v2` với giao diện `labelstudio/config.xml` (5 nhãn + 7 quan hệ), import file gán sẵn, bật *Use predictions to prelabel tasks*.
3. Các thành viên mở từng câu và **kiểm tra toàn bộ** nhãn máy gán:
   - sửa biên, sửa loại thực thể, thêm thực thể bị thiếu (ví dụ Giải Turing, Apache 2.0);
   - sửa quan hệ sai, ví dụ câu ID 144: `Meta AI → thuộc_về → Linux Foundation` sửa thành `PyTorch → thuộc_về → Linux Foundation`;
   - bấm Submit. Mọi thành viên cùng ghi vào một cơ sở dữ liệu trên máy chủ nên dữ liệu đồng nhất.
4. Kết quả: 97/97 câu đã duyệt.

### Bước 4 — Export
- Export định dạng **JSON** (không dùng JSON-MIN vì không chứa quan hệ) → `data/export/annotation.json`.

### Bước 5 — Huấn luyện và đánh giá (`NER_KHDL.ipynb`, sinh bởi `scripts/build_notebook.py`)
Làm theo `B5/spacy.ipynb` của thầy, bổ sung phần đánh giá:

| Mục | Làm gì |
|---|---|
| 1. Chuyển định dạng | Export → `data/spacy_train.json` dạng `[text, {"entities": [[start, end, label]]}]` (code của thầy) |
| 2. Lọc O | Bỏ nhãn O (spaCy tự coi chữ không có nhãn là O), thống kê số nhãn |
| 3. Kiểm tra lệch biên | Đếm thực thể không khớp token với `vi` và `xx`: `vi` lệch 2/295, `xx` lệch 1/295 |
| 4. Chia train/test | 78 / 19 câu |
| 5. Train | `spacy.blank("vi")` + NER, 30 epoch, minibatch, dropout 0.2. Lưu mô hình vào `models/ner_khdl_vi` |
| 6. Đánh giá | P/R/F1 tổng và theo từng nhãn trên tập test |
| 7. So sánh tokenizer | Train lại với `xx` để so sánh |
| 8. Phân tích lỗi | Liệt kê câu test có dự đoán khác nhãn thật (13/19 câu có ít nhất 1 lỗi) |
| 9. Test câu mới | 5 câu tự đặt + hiển thị bằng displaCy (giống phần `# test` của thầy) |
| 10. Quan hệ | Thống kê quan hệ → `results/relations.csv` |
| 11. Bản đồ tương quan | Heatmap số quan hệ và heatmap đồng xuất hiện giữa các loại thực thể → `correlation_map.png` |
| 12. Đồ thị quan hệ | Đồ thị networkx các thực thể và quan hệ → `relation_graph.png` |

---

## 6. Kết quả

| | Precision | Recall | F1 | Support (test) |
|---|---:|---:|---:|---:|
| **Tổng** | **0.772** | **0.759** | **0.765** | 59 |
| MISC | 0.771 | 0.730 | 0.750 | 38 |
| ORG | 0.833 | 0.769 | 0.800 | 13 |
| PER | 0.700 | 0.875 | 0.778 | 8 |
| LOC | — | — | — | 0 (không có trong tập test) |

| Tokenizer | Thực thể lệch biên | P | R | F1 |
|-----------|---:|---:|---:|---:|
| `vi` (pyvi, như thầy) | 2 | 0.772 | 0.759 | **0.765** |
| `xx` | 1 | 0.705 | 0.729 | 0.717 |

**Nhận xét:**
- ORG tốt nhất. MISC thấp hơn vì gộp nhiều loại khác nhau (thuật toán, công cụ, độ đo).
- PER có recall cao nhưng precision thấp: mô hình hay đoán nhầm tên riêng khác thành người.
- Lỗi thường gặp: **sai biên** do dấu câu hoặc ký tự đặc biệt ("AT&T Labs" → "T Labs", "CUDA." dính dấu chấm), và **nhầm ORG ↔ MISC** (NVIDIA đoán thành MISC).
- Bản đồ tương quan: nhiều quan hệ nhất là **ORG → MISC** và **PER → MISC** (tổ chức, người phát triển thuật toán, công cụ).
- F1 dao động khoảng ±0.02 giữa các lần chạy vì tập test nhỏ → trên slide ghi **F1 ≈ 0.75–0.77**.

File kết quả trong `results/`: `ner_per_type_vi.csv`, `ner_metrics_vi.json`, `ner_compare_tokenizer.csv`, `relations.csv`, `correlation_map.png`, `relation_graph.png`, `demo.html`.

---

## 7. Demo

Demo trực tiếp khoảng 2–3 phút. Slide chỉ cần 1 trang "Demo" kèm ảnh chụp dự phòng. Kịch bản chi tiết ở cuối `SLIDE_BO_CUC.md`.

1. **Label Studio:** mở `http://192.168.1.25:8080` → câu ID 144, cho xem thực thể tô màu và mũi tên quan hệ. Nếu tô thử thì **bấm hủy, không Submit**.
2. **Mô hình:** chạy `python scripts/demo_ner.py`, gõ câu mới. Terminal in ra thực thể, trình duyệt mở `results/demo.html` tô màu (tải lại trang sau mỗi câu).

| Câu gợi ý | Kết quả |
|---|---|
| Andrew Ng từng làm việc tại Google Brain và Baidu trước khi giảng dạy ở Đại học Stanford. | Đúng hết |
| Hugging Face phát hành thư viện Transformers cho Python. | Đúng hết |
| Mô hình YOLO đạt mAP cao trên bộ dữ liệu COCO. | Sai: `COCO.` → PER, dùng để chuyển sang phân tích lỗi |

Demo nhanh bằng cách truyền câu vào lệnh: `python scripts/demo_ner.py "câu 1" "câu 2"`.

---

## 8. Hạn chế

- **Dữ liệu ít:** 97 câu, tập test chỉ 19 câu (59 thực thể) → điểm chưa ổn định, dao động ±0.02.
- **Mất cân bằng nhãn:** MISC 196 so với LOC 8. Tập test không có LOC nên không đánh giá được nhãn này.
- **MISC quá rộng:** gộp thuật toán, công cụ, bộ dữ liệu, độ đo nên mô hình khó học ranh giới.
- **Tokenizer pyvi:** gộp dấu câu vào từ ("A.", "COCO.") gây lệch biên và lỗi dự đoán.
- **Mô hình đơn giản:** `spacy.blank` học từ đầu, không có kiến thức ngôn ngữ có sẵn.
- **Quan hệ chưa có mô hình:** 46 quan hệ mới dùng để thống kê và vẽ bản đồ, chưa train mô hình trích xuất quan hệ. Một số loại quá ít (nằm_ở 1, đánh_giá_bằng 0).
- **Nhãn gán sẵn bằng máy:** dù đã duyệt 97/97 câu, người duyệt vẫn có thể bỏ sót lỗi máy gán khó thấy.

## 9. Hướng cải thiện

- Thu thập thêm dữ liệu (300–500 câu), cân bằng các nhãn, nhất là LOC.
- Tách MISC thành nhãn chi tiết: ALGO, TOOL, DATASET, METRIC (`pre_annotate.py` đã có sẵn các nhãn này).
- Tiền xử lý tách dấu câu khỏi từ cuối câu, hoặc viết tokenizer riêng để giảm lệch biên.
- Dùng mô hình pretrained cho tiếng Việt (PhoBERT, spaCy transformer) thay vì `spacy.blank`.
- Dùng cross-validation (k-fold) để điểm ổn định hơn.
- Train mô hình trích xuất quan hệ từ dữ liệu quan hệ đã gán, bổ sung quan hệ `đánh_giá_bằng` (mô hình → độ đo).
- Cho nhiều người gán cùng một câu để đo độ đồng thuận (Cohen's kappa).

---

## 10. Cấu trúc thư mục

```
Phan2/                           # (trong repo NLP_Baitapnhom, cạnh Phan1/)
├── B5/                          # tài liệu + notebook spaCy của thầy
├── data/
│   ├── raw/
│   │   ├── sources/*.json       # văn bản gốc tải từ Wikipedia API
│   │   ├── selection.json       # danh sách câu được chọn
│   │   ├── sources.md           # nguồn: URL + revid từng bài
│   │   └── khdl_corpus.txt      # văn bản ghép từ các câu đã chọn
│   ├── data.json                # 97 câu, định dạng import Label Studio
│   ├── data_preannotated.json   # 97 câu + nhãn gán sẵn (predictions)
│   ├── spacy_train.json         # [start, end, label], theo code của thầy
│   └── export/
│       ├── annotation.json      # ★ export cuối từ Label Studio (nhãn thật)
│       ├── ls_snapshot_v1.json  # 23 câu gán ở project cũ (đã chuyển sang v2)
│       └── MOCK_export.json     # export giả lập, chỉ để chạy thử pipeline
├── labelstudio/config.xml       # giao diện gán nhãn (5 nhãn + 7 quan hệ)
├── scripts/
│   ├── fetch_wikipedia.py       # tải bài + chọn câu → khdl_corpus.txt, sources.md
│   ├── split_sentences.py       # tách câu → data.json
│   ├── pre_annotate.py          # gán sẵn: từ điển + cụm O + luật quan hệ
│   ├── build_notebook.py        # sinh NER_KHDL.ipynb
│   └── demo_ner.py              # demo: nhập câu → in thực thể + mở demo.html
├── models/ner_khdl_vi/          # mô hình đã train (có trong git để demo chạy ngay)
├── NER_KHDL.ipynb               # train + đánh giá NER + quan hệ + bản đồ tương quan
├── results/                     # bảng điểm, hình cho slide, demo.html
├── PHAN2_KE_HOACH.md
└── SLIDE_BO_CUC.md
```

## 11. Cách chạy lại

```bash
cd ~/NLP_Baitapnhom                                         # .venv nằm ở gốc repo, không đưa lên git
python3.12 -m venv .venv                                    # chỉ lần đầu
source .venv/bin/activate
cd Phan2                                                    # mọi lệnh dưới chạy trong Phan2/
pip install label-studio spacy pyvi underthesea pandas matplotlib networkx nbclient ipykernel   # chỉ lần đầu

python scripts/fetch_wikipedia.py                # 1. tải bài + chọn câu (bài đã tải thì bỏ qua)
python scripts/split_sentences.py                # 2. tách câu → data/data.json
python scripts/pre_annotate.py                   # 3a. gán sẵn → data/data_preannotated.json
label-studio start --host 0.0.0.0 --port 8080    # 3b. gán nhãn (dữ liệu cũ vẫn còn)
python scripts/build_notebook.py                 # 5. sinh lại notebook
python scripts/demo_ner.py                       # 6. demo
```

- **Bước 4:** trên Label Studio vào project → **Export** → **JSON** → lưu đè `data/export/annotation.json`.
- **Bước 5:** mở `NER_KHDL.ipynb` trong VS Code (chọn kernel `.venv`) và bấm **Run All**. Mô hình lưu vào `models/ner_khdl_vi`, kết quả vào `results/`.
- Nếu chỉ cần chạy lại phần train và đánh giá thì bỏ qua bước 1–4.

## 12. Việc còn lại

- [ ] Chụp màn hình Label Studio: thanh địa chỉ `192.168.1.25:8080`, danh sách 97/97 câu, câu ID 144 có mũi tên quan hệ
- [ ] Chụp `results/demo.html` làm ảnh dự phòng cho slide Demo
- [ ] Làm slide theo `SLIDE_BO_CUC.md`
- [ ] Tập demo, tập trình bày, chuẩn bị câu hỏi (mục "Câu hỏi có thể gặp" trong `SLIDE_BO_CUC.md`)
