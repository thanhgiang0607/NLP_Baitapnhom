# Bố cục slide — Phần 2: NER + Label Studio

Khoảng **12 slide**, trình bày 8–10 phút. Cột *Hình/Bảng* chỉ file có sẵn trong project.

---

## Slide 1 — Tiêu đề
- **Nhận dạng thực thể có tên (NER) trên văn bản Khoa học dữ liệu với Label Studio và spaCy**
- Tên nhóm, thành viên, môn học, ngày

## Slide 2 — Mục tiêu và quy trình
- Mục tiêu: xây dựng bộ dữ liệu NER tiếng Việt miền KHDL, huấn luyện và đánh giá mô hình spaCy
- Sơ đồ quy trình (vẽ 6 ô, mũi tên ngang):
  **Wikipedia → Tách câu → Label Studio (LAN) → Export JSON → spaCy train/test → Đánh giá P/R/F1**

## Slide 3 — Thu thập dữ liệu
- Nguồn: **21 bài Wikipedia tiếng Việt** (CC BY-SA 4.0), tải qua MediaWiki API
- Chọn **97 câu** có nhiều thực thể, nhóm theo chủ đề:
  - Lịch sử học máy, học sâu (Hinton, LeCun, AlexNet, LSTM…)
  - Framework, công cụ (PyTorch, TensorFlow, Python)
  - Độ đo đánh giá (precision, recall, F1, IoU, mAP, MSE, BLEU)
- 1–2 câu ví dụ
- *Hình/Bảng:* bảng rút gọn từ `data/raw/sources.md` (tên bài + số câu)

## Slide 4 — Tách câu, tạo data.json
- `underthesea.sent_tokenize` → làm sạch → bỏ câu ngắn, câu trùng → 97 câu
- Đoạn mã ngắn `scripts/split_sentences.py`, mẫu 2 dòng `data.json`:
  ```json
  [{"id": 1, "data": {"text": "Vào tháng 3 năm 2023, OpenAI ..."}}]
  ```

## Slide 5 — Host Label Studio qua mạng nội bộ
- Lệnh: `label-studio start --host 0.0.0.0 --port 8080`
- Truy cập: `http://192.168.1.25:8080` (cùng Wi-Fi; người ở xa dùng Tailscale)
- *Hình:* ảnh chụp trình duyệt thấy rõ IP trên thanh địa chỉ, ảnh danh sách 97/97 câu đã hoàn thành

## Slide 6 — Bộ nhãn và quy tắc gán
- Bảng 5 nhãn (theo mẫu của thầy): PER, ORG, LOC, MISC, O, kèm ví dụ và số lượng (47 / 44 / 8 / 196 / 377)
- Ý chính: **gán cả O**, không bỏ sót cụm động từ, giới từ → dữ liệu giữ được cấu trúc câu
- Ví dụ một câu đã tô màu:
  > **Vladimir Vapnik** *(PER)* · giới thiệu thuật toán *(O)* · **SVM** *(MISC)* · tại *(O)* · **Bell Labs** *(ORG)*
- *Hình:* ảnh chụp câu ID 144 trong Label Studio (thực thể tô màu + mũi tên quan hệ)

## Slide 7 — Gán nhãn quan hệ
- 7 loại quan hệ, đã dùng 6 loại; **46 quan hệ** trong 35 câu
- Bảng: phát_triển 25 · cộng_sự 9 · sử_dụng 5 · làm_việc_tại 3 · thuộc_về 3 · nằm_ở 1
- Gán sẵn bằng **luật mẫu** (giống slide 10 của thầy: hand-written patterns):
  "X **của** Y", "X **do/bởi** Y" → Y phát_triển X; "PER **tại** ORG" → làm_việc_tại
- Nhóm duyệt và sửa, ví dụ: `Meta AI → thuộc_về → Linux Foundation` (sai) → `PyTorch → thuộc_về → Linux Foundation`
- *Hình/Bảng:* `results/relations.csv` (vài dòng)

## Slide 8 — Bản đồ tương quan và đồ thị quan hệ
- *Hình:* `results/correlation_map.png`
  - Trái: số quan hệ giữa các loại thực thể → **ORG → MISC** và **PER → MISC** nhiều nhất (tổ chức, người phát triển thuật toán, công cụ)
  - Phải: số câu mà hai loại thực thể cùng xuất hiện → MISC đi cùng ORG/PER nhiều
- *Hình:* `results/relation_graph.png` (có thể đặt ở slide phụ)

## Slide 9 — Huấn luyện spaCy (theo notebook B5)
- Export JSON → `spacy_train.json` `[start, end, label]` → bỏ `O` → `spacy.blank("vi")` + NER
- Chia train/test 80/20: **78 / 19 câu**, 30 epoch
- Phát hiện: tokenizer pyvi gộp "A." thành 1 token → thực thể lệch biên bị bỏ qua khi train (cảnh báo **W030** trong notebook mẫu) → kiểm tra trước khi train: chỉ 2/295 thực thể bị lệch

## Slide 10 — Kết quả đánh giá NER ★
- Bảng chính (từ `results/ner_per_type_vi.csv`):

  | | Precision | Recall | F1 |
  |---|---:|---:|---:|
  | **Tổng** | **0.77** | **0.76** | **0.77** |
  | ORG | 0.83 | 0.77 | 0.80 |
  | PER | 0.70 | 0.88 | 0.78 |
  | MISC | 0.77 | 0.73 | 0.75 |

- So sánh tokenizer: `vi` (pyvi) F1 0.77 so với `xx` F1 0.72
- Ghi chú: đánh giá **theo thực thể** (khớp cả biên và nhãn), như slide 09 của thầy. LOC không có trong tập test.

## Slide 10b — Demo (chuyển sang demo trực tiếp)
- Slide chỉ có tiêu đề **"Demo"** + 1 ảnh chụp dự phòng `results/demo.html` (phòng khi máy lỗi)
- Nội dung demo: xem mục **Kịch bản demo** cuối file

## Slide 11 — Phân tích lỗi
Chọn 3–4 ví dụ từ mục 8 của notebook:

| Câu (rút gọn) | Gold | Dự đoán | Loại lỗi |
|---|---|---|---|
| "…Yann LeCun và các đồng sự tại **AT&T Labs**…" | AT&T Labs (ORG) | T Labs (MISC) | Sai biên do ký tự "&" |
| "…được quản lý bởi **PyTorch Foundation** - một tổ chức…" | PyTorch Foundation (ORG) | PyTorch Foundation - một (MISC) | Sai biên + sai nhãn |
| "…trên GPU **NVIDIA** có hỗ trợ **CUDA**." | NVIDIA (ORG), CUDA (MISC) | NVIDIA (MISC), CUDA. (PER) | Nhầm nhãn, dính dấu chấm cuối câu |
| "…**Hinton** được trao **Giải Turing**…" | Hinton (PER) | Hinton (ORG) | Tên đứng một mình, thiếu ngữ cảnh |

- Nhận xét: lỗi chủ yếu là **sai biên** (dấu câu, ký tự đặc biệt) và **nhầm ORG ↔ MISC** (tên công ty và tên sản phẩm giống nhau)

## Slide 12 — Kết luận và hướng phát triển
- Đạt được: bộ dữ liệu 97 câu có nguồn rõ ràng, gán nhãn thực thể và quan hệ trên Label Studio qua LAN, NER F1 ≈ 0.77
- Hạn chế:
  - Dữ liệu ít (97 câu), tập test chỉ 19 câu → điểm dao động ±0.02
  - Mất cân bằng nhãn: MISC 196 so với LOC 8
  - MISC gộp nhiều loại (thuật toán, công cụ, độ đo) → khó phân biệt
- Hướng phát triển: thêm dữ liệu; tách MISC thành ALGO/TOOL/DATASET/METRIC; dùng mô hình pretrained (PhoBERT); huấn luyện mô hình trích xuất quan hệ từ 46 quan hệ đã gán

---

## Kịch bản demo (~2–3 phút, làm trực tiếp trên máy)

**Chuẩn bị trước giờ trình bày** (mở sẵn, khỏi chờ):
```bash
cd ~/NLP_Baitapnhom && source .venv/bin/activate && cd Phan2
label-studio start --host 0.0.0.0 --port 8080      # tab 1: Label Studio
python scripts/demo_ner.py                          # tab 2: demo NER, để sẵn dấu nhắc ">"
```

| Bước | Làm gì | Nói gì |
|---|---|---|
| 1 | Mở `http://192.168.1.25:8080` → project `NLP_Nhóm1_v2` → câu ID 144 | "Đây là dữ liệu nhóm gán trên Label Studio qua LAN: thực thể tô màu, mũi tên là quan hệ" |
| 2 | (Tuỳ chọn) Tô thử 1 từ → chọn nhãn → kéo 1 quan hệ, rồi **bấm hủy, không Submit** | "Cách gán nhãn: chọn nhãn, bôi đen từ; quan hệ thì chọn 2 thực thể" |
| 3 | Sang terminal, gõ câu mới không có trong dữ liệu (gợi ý dưới) | "Mô hình spaCy nhóm đã train nhận diện thực thể trên câu chưa từng thấy" |
| 4 | Trình duyệt tự mở `results/demo.html`, câu được tô màu (tải lại trang sau mỗi câu) | Chỉ vào từng thực thể |
| 5 | Gõ câu có lỗi → dẫn sang slide 11 | "Mô hình vẫn sai biên ở dấu chấm cuối câu, phần tiếp theo phân tích lỗi" |

**Câu gợi ý đã chạy thử:**
- `Andrew Ng từng làm việc tại Google Brain và Baidu trước khi giảng dạy ở Đại học Stanford.` → đúng hết (PER, ORG×3)
- `Hugging Face phát hành thư viện Transformers cho Python.` → đúng hết (ORG, MISC×2)
- `Mô hình YOLO đạt mAP cao trên bộ dữ liệu COCO.` → **lỗi:** `COCO.` thành PER (dính dấu chấm), dùng để chuyển sang slide 11

**Dự phòng:** nếu máy lỗi hoặc không có mạng, chiếu ảnh chụp `results/demo.html` trên slide 10b. Hoặc mở `NER_KHDL.ipynb` mục 9 (đã có sẵn output).

---

## Câu hỏi có thể gặp
| Câu hỏi | Gợi ý trả lời |
|---|---|
| Gán O để làm gì khi code spaCy lọc bỏ O? | spaCy vốn coi chữ không tô là O, nên gán O không đổi điểm NER. Giá trị nằm ở dữ liệu đầy đủ hơn: cụm từ nối ("của", "do", "tại") là dấu hiệu nhận biết quan hệ, dùng được cho mô hình trích xuất quan hệ hoặc mô hình gán nhãn chuỗi khác. |
| Nhãn có phải do máy gán không? | Máy gán sẵn (từ điển + luật), nhóm duyệt và sửa 97/97 câu (thêm MISC cho Giải Turing, Apache 2.0…; sửa quan hệ sai). Đây là cách gán nhãn có hỗ trợ của máy, phổ biến trong thực tế. |
| Vì sao F1 dao động? | Tập test nhỏ (19 câu, 59 thực thể); chỉ cần đổi vài thực thể là F1 thay đổi vài phần trăm. |
| Vì sao chọn tokenizer `vi`? | Giống notebook của thầy, F1 cao hơn `xx` trên dữ liệu này, dù pyvi có gây lệch biên ở một số từ cuối câu. |
| Precision/Recall tính theo token hay thực thể? | Theo thực thể: dự đoán chỉ đúng khi trùng cả biên và nhãn (slide 09 – "per entity, not per token"). |
