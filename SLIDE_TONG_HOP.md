# Bố cục slide tổng hợp — Phần 1 + Phần 2 (20–25 phút)

Tổng hợp từ `Phan1/SLIDE_BO_CUC.md` và `Phan2/SLIDE_BO_CUC.md`.
**27 slide**, trình bày khoảng **23 phút**, cộng 3–5 phút hỏi đáp.

Mỗi slide có:
- **Nội dung**: chữ đưa lên slide
- **📸 / 🖼**: 📸 = chụp màn hình notebook `Phan1/1_SemiSupervised/semi_supervised.ipynb` (bấm **Run All** trước); 🖼 = file có sẵn trong `Phan2/results/` hoặc ảnh chụp Label Studio
- **🗣 Nói**: ý chính người trình bày nói, không cần đưa lên slide

## Phân bổ thời gian

| Khối | Slide | Thời gian | Người trình bày |
|---|---|---:|---|
| Mở đầu | 1–2 | 1.5 phút | [__] |
| Phần 1 – Phân tích cảm xúc bán giám sát | 3–12 | 8.5 phút | [__] |
| Phần 2 – NER + Label Studio (gồm demo 3 phút) | 13–25 | 12 phút | [__] |
| Kết luận | 26–27 | 1 phút | [__] |
| **Tổng** | | **23 phút** | |
| Hỏi đáp | | 3–5 phút | cả nhóm |

> Thiếu giờ thì bỏ trước: slide 20 (đồ thị quan hệ), slide 11 (phân tích lỗi Phần 1, chỉ nói miệng), bước 2 của demo. Dư giờ thì mở thêm notebook khi demo.

---

# MỞ ĐẦU (1.5 phút)

## Slide 1 — Tiêu đề · ⏱ 0.5 phút
- **Phân tích cảm xúc bán giám sát và Nhận dạng thực thể có tên trên văn bản tiếng Việt**
- Phần 1: Self-training + Naive Bayes · Phần 2: NER với Label Studio + spaCy
- Nhóm [__], thành viên [__], giảng viên [__], 11/2026
- 🗣 **Nói:** chào, giới thiệu nhóm và hai phần sẽ trình bày.

## Slide 2 — Nội dung trình bày · ⏱ 1 phút
| | Phần 1 · Cảm xúc | Phần 2 · NER |
|---|---|---|
| Bài toán | Phân loại câu: pos / neg | Tìm thực thể và quan hệ trong câu |
| Dữ liệu | 200 bình luận Threads về AI | 97 câu Wikipedia về KHDL |
| Gán nhãn | Tay 20 câu, máy gán phần còn lại | Label Studio qua LAN, duyệt 97/97 câu |
| Mô hình | Naive Bayes + self-training | spaCy NER |
| Kết quả | Đúng 61% trên câu có cảm xúc | F1 ≈ 0.77 |

- 🗣 **Nói:** hai phần chung một câu hỏi: gán nhãn văn bản tiếng Việt khi ít dữ liệu. Phần 1 gán nhãn cả câu, Phần 2 gán nhãn từng cụm từ.

---

# PHẦN 1 — PHÂN TÍCH CẢM XÚC BÁN GIÁM SÁT (8.5 phút)

## Slide 3 — Trang mở Phần 1 · ⏱ 0.25 phút
- **Phần 1: Phân tích cảm xúc bán giám sát**
- Bình luận tiếng Việt về Trí tuệ nhân tạo · Self-training với Naive Bayes

## Slide 4 — Bài toán và quy trình · ⏱ 0.75 phút
- **Bài toán:** xác định bình luận về AI là **tích cực (pos)** hay **tiêu cực (neg)**
- **Ràng buộc:** chỉ gán tay **20/200** câu, 180 câu còn lại máy tự gán → **semi-supervised**
- Sơ đồ 6 ô: **Thu thập 200 câu → Gán tay 20 câu → Tiền xử lý → Naive Bayes → Self-training → Đánh giá**
- 🗣 **Nói:** ý tưởng bán giám sát: mô hình học từ ít nhãn, tự gán nhãn câu nó chắc chắn, rồi học lại.

## Slide 5 — Dữ liệu · ⏱ 1 phút
- Nguồn: **Threads**, 10 bài đăng về AI (ChatGPT, Claude, Gemini…), thu thập 09/11/2026
- **200 bình luận**, trung bình 24.6 chữ/câu
- Lọc: bỏ quảng cáo, link, câu trùng, câu < 6 từ, câu không nói về AI; không lưu tên người dùng
- Đặc điểm: văn nói, viết tắt (ko, vs, đc), tiếng lóng; khoảng **một nửa là câu trung tính**
- Ví dụ: *"phải bỏ tiền ra mới biết con claude đỉnh cỡ nào"* · *"Nếu có source rồi thì dùng notebookLM á mom"*
- 📸 vài dòng đầu `Phan1/data/comments_raw.csv`
- 🗣 **Nói:** nhấn mạnh dữ liệu là văn nói, nhiều viết tắt, nhiều câu trung tính. Đây là lý do kết quả ở slide 10 thấp.

## Slide 6 — Gán nhãn tay 20 câu · ⏱ 0.75 phút
- **10 pos + 10 neg**. Tiêu chí: khen/chê **chính AI**, không chọn câu nửa khen nửa chê, từ ngữ đa dạng

  | Nhãn | Ví dụ |
  |---|---|
  | pos | "AI là thứ tuyệt vời nhất con người tạo ra" · "claude viết hay đến nỗi vỗ đùi khen hay" |
  | neg | "gemini rất đần" · "meta.ai quá phế để xài" |

- 📸 bảng thứ nhất ở **ô 6** (cột `text`, `pred`)

## Slide 7 — Tiền xử lý · ⏱ 0.75 phút
- Chữ thường + tách từ bằng **regex** (Lab 03)
- **Đánh dấu phủ định `NOT_`** (slide S23): thêm `NOT_` vào các từ sau "không/ko/k/chẳng/chả/chưa" đến dấu câu kế tiếp
- Ví dụ câu 155: `ko có sự liền mạch` → `ko NOT_có NOT_sự NOT_liền NOT_mạch`
- 📸 kết quả **ô 2** (`NaN 180 / pos 10 / neg 10`)
- 🗣 **Nói:** nhờ `NOT_` mà "không hay" và "hay" thành hai đặc trưng khác nhau.

## Slide 8 — Naive Bayes ban đầu · ⏱ 1 phút
- **Semi-supervised là phương pháp, Naive Bayes là mô hình** đoán nhãn trong mỗi vòng
- Đặc trưng `contains(từ) = True` cho từ có mặt (Boolean NB, S25), `nltk.NaiveBayesClassifier` (Lab 06)
- Khác Lab 06: **bỏ đặc trưng `False`**. Với 20 câu và 1385 từ vựng, các `False` lấn át từ có nghĩa → đoán "AI này trả lời hay ghê" là neg 100%
- Thử: "claude đỉnh thật" → **pos 0.94** · "gemini phế" → **neg 0.75**
- 📸 kết quả **ô 3** (Most Informative Features + 2 dòng thử)

## Slide 9 — Self-training · ⏱ 1 phút
- Vòng lặp 4 ô: **Huấn luyện → Đoán câu chưa nhãn → Nhận câu có độ tự tin ≥ 0.9 → Lặp đến khi không thêm được câu nào**

  | Vòng | Thêm neg | Thêm pos | Tổng có nhãn |
  |---|---:|---:|---:|
  | 0 (gán tay) | 10 | 10 | 20 |
  | 1 | 47 | 37 | 104 |
  | 2 | 53 | 9 | 166 |
  | 3 | 1 | 7 | 174 |
  | 4 | 4 | 1 | 179 |

- Kết quả 200 câu: **neg 115 · pos 64 · unknown 21**
- 📸 kết quả **ô 4** và crosstab **ô 5**
- 🗣 **Nói:** chỉ vào vòng 2: thêm 53 neg nhưng chỉ 9 pos. Đây là dấu hiệu lệch, sẽ giải thích ở slide 11.

## Slide 10 — Đánh giá Phần 1 ★ · ⏱ 1.5 phút
- Chấm tay toàn bộ **159 câu máy gán**:

  | | Số câu | Tỉ lệ |
  |---|---:|---:|
  | Đúng | 49 | 31% |
  | Sai | 31 | 19% |
  | Trung tính | 79 | 50% |

- Số lớn trên slide: **61%** = đúng 49/80 câu có cảm xúc (bỏ trung tính)
  - Máy gán pos đúng **81%** · máy gán neg đúng **44%**
  - Vòng 1 đúng **72%** · vòng 2 đúng **38%**
- 📸 kết quả **ô 8** + bảng quy tắc chấm **ô 7**
- 🗣 **Nói:** 31% thấp chủ yếu vì một nửa số câu là trung tính trong khi mô hình chỉ có 2 nhãn. 61% mới là khả năng phân biệt khen/chê.

## Slide 11 — Phân tích lỗi Phần 1 · ⏱ 1 phút
- **Lỗi tự khuếch đại:** nhãn sai ở vòng trước thành dữ liệu học ở vòng sau → độ đúng giảm 72% → 38%

  | Câu thử | Mô hình ban đầu | Mô hình cuối |
  |---|---|---|
  | Claude viết code đỉnh thật, dùng rất tiện | pos 0.68 ✓ | neg 0.56 ✗ |
  | Gemini trả lời ngu quá, toàn bịa | neg 0.90 ✓ | neg 0.99 ✓ |

- Ví dụ gán sai: châm biếm (*"Nó viết còn thấy hay thì rớt là đúng r"* → pos), phủ định đảo nghĩa (*"Tại nó không có phán xét tao"* → neg), khen kèm chê (*"Chat gpt số 1 lòng e, lâu lâu hay bịa số liệu…"* → neg)
- **21 câu unknown:** 14 trung tính, 6 tích cực, 1 tiêu cực → ngưỡng 0.9 giữ lại đúng phần lớn câu không có cảm xúc
- 📸 (tuỳ chọn) bảng thứ ba **ô 6**

## Slide 12 — Tóm tắt Phần 1 · ⏱ 0.5 phút
- Từ **20 câu gán tay**, self-training gán thêm **159 câu**, đúng **61%** trên câu có cảm xúc
- Hạn chế: ít nhãn ban đầu, lỗi tự khuếch đại (lệch về neg), chỉ 2 nhãn, khó nhận châm biếm
- Hướng phát triển: thêm nhãn trung tính; cân bằng pos/neg mỗi vòng hoặc tăng ngưỡng 0.99; tách từ tiếng Việt, chuẩn hoá teencode; thử MaxEnt, SVM
- 🗣 **Nói (chuyển phần):** "Phần 1 gán nhãn cả câu và chỉ có 20 nhãn tay. Phần 2 gán nhãn từng cụm từ trong câu, và toàn bộ 97 câu đều do nhóm duyệt."

---

# PHẦN 2 — NER + LABEL STUDIO (12 phút)

## Slide 13 — Trang mở Phần 2 · ⏱ 0.25 phút
- **Phần 2: Nhận dạng thực thể có tên (NER)**
- Văn bản Khoa học dữ liệu · Label Studio + spaCy

## Slide 14 — Bài toán và quy trình · ⏱ 0.75 phút
- **Bài toán:** tìm các thực thể trong câu và loại của chúng
  > **Vladimir Vapnik** *(PER)* giới thiệu thuật toán **SVM** *(MISC)* tại **Bell Labs** *(ORG)*
- Mở rộng: gán **quan hệ** giữa thực thể (Vapnik —phát_triển→ SVM) → bản đồ tương quan
- Sơ đồ 6 ô: **Wikipedia → Tách câu → Label Studio (LAN) → Export JSON → spaCy train/test → Đánh giá P/R/F1**
- 🗣 **Nói:** trọng tâm là NER. Quan hệ là phần mở rộng theo yêu cầu của thầy.

## Slide 15 — Thu thập dữ liệu và tách câu · ⏱ 0.75 phút
- Nguồn: **21 bài Wikipedia tiếng Việt** (CC BY-SA 4.0), tải qua MediaWiki API, ghi rõ URL và phiên bản từng bài
- Chọn **97 câu** nhiều thực thể: lịch sử học máy/học sâu (Hinton, LeCun, AlexNet), framework (PyTorch, TensorFlow), độ đo (precision, recall, F1, IoU, mAP)
- Tách câu: `underthesea.sent_tokenize` → làm sạch → bỏ câu ngắn, câu trùng → `data.json`
  ```json
  [{"id": 1, "data": {"text": "Vào tháng 3 năm 2023, OpenAI ..."}}]
  ```
- 🖼 bảng rút gọn từ `Phan2/data/raw/sources.md`

## Slide 16 — Label Studio qua mạng nội bộ · ⏱ 1 phút
- Lệnh: `label-studio start --host 0.0.0.0 --port 8080`
- Truy cập: `http://192.168.1.25:8080` (cùng Wi-Fi; người ở xa dùng Tailscale). Mọi người ghi chung một cơ sở dữ liệu nên nhãn đồng nhất
- Quy trình: máy **gán sẵn** (từ điển + luật) → nhóm **duyệt và sửa 97/97 câu**
- 🖼 ảnh trình duyệt thấy rõ IP trên thanh địa chỉ + danh sách 97/97 câu
- 🗣 **Nói:** `0.0.0.0` cho phép máy khác trong mạng truy cập. Gán sẵn giúp nhanh và đồng nhất, nhưng mỗi câu đều có người kiểm tra.

## Slide 17 — Bộ nhãn thực thể · ⏱ 1 phút
| Nhãn | Ý nghĩa | Ví dụ | Số lượng |
|---|---|---|---:|
| PER | Người | Geoffrey Hinton, Yann LeCun | 47 |
| ORG | Tổ chức | OpenAI, Google Brain | 44 |
| LOC | Địa điểm | San Francisco, Seoul | 8 |
| MISC | Thuật toán, công cụ, bộ dữ liệu, độ đo, giải thưởng | SVM, PyTorch, ImageNet, F1 | 196 |
| O | Phần còn lại: cụm động từ, giới từ | "của", "do", "tại" | 377 |

- Ý chính: **gán cả O**, không bỏ sót chữ nào → giữ cấu trúc câu
- 🖼 ảnh câu ID 144 trong Label Studio
- 🗣 **Nói:** bộ nhãn theo mẫu `annotation.json` của thầy. MISC chiếm nhiều nhất vì văn bản KHDL nhiều tên thuật toán, công cụ.

## Slide 18 — Gán nhãn quan hệ · ⏱ 0.75 phút
- 7 loại quan hệ, dùng 6 loại; **46 quan hệ** trong 35 câu
- phát_triển 25 · cộng_sự 9 · sử_dụng 5 · làm_việc_tại 3 · thuộc_về 3 · nằm_ở 1
- Gán sẵn bằng **luật mẫu** (slide 10 của thầy): "X **của** Y", "X **do/bởi** Y" → Y phát_triển X; "PER **tại** ORG" → làm_việc_tại
- Ví dụ nhóm sửa: `Meta AI → thuộc_về → Linux Foundation` (sai) → `PyTorch → thuộc_về → Linux Foundation`

## Slide 19 — Bản đồ tương quan · ⏱ 0.75 phút
- 🖼 `Phan2/results/correlation_map.png`
  - Trái: số quan hệ chủ thể → đối tượng: **ORG → MISC 16** nhiều nhất, sau đó **PER → MISC 9** và **PER → PER 9** (cộng sự)
  - Phải: số câu hai loại cùng xuất hiện: MISC đi cùng ORG (27) và PER (22) nhiều nhất
- 🗣 **Nói:** trong KHDL, tổ chức và người là bên phát triển, thuật toán và công cụ là thứ được phát triển.

## Slide 20 — Đồ thị quan hệ · ⏱ 0.5 phút (có thể bỏ)
- 🖼 `Phan2/results/relation_graph.png`: nút tô màu theo loại thực thể, mũi tên là quan hệ
- 🗣 **Nói:** chỉ vài cụm dễ thấy: OpenAI → ChatGPT, DALL-E 3; Meta AI / PyTorch Foundation → PyTorch → Linux Foundation; Hinton – Sutskever – Krizhevsky → AlexNet.

## Slide 21 — Huấn luyện spaCy · ⏱ 0.75 phút
- Theo notebook B5 của thầy: Export JSON → `[start, end, label]` → bỏ `O` → `spacy.blank("vi")` + NER
- Chia train/test 80/20: **78 / 19 câu**, 30 epoch
- Phát hiện: tokenizer pyvi gộp "A." thành 1 token → thực thể lệch biên bị bỏ qua (cảnh báo **W030** trong notebook mẫu) → kiểm tra trước khi train: chỉ **2/295** thực thể bị lệch

## Slide 22 — Kết quả NER ★ · ⏱ 1 phút
| | Precision | Recall | F1 |
|---|---:|---:|---:|
| **Tổng** | **0.77** | **0.76** | **0.77** |
| ORG | 0.83 | 0.77 | 0.80 |
| PER | 0.70 | 0.88 | 0.78 |
| MISC | 0.77 | 0.73 | 0.75 |

- So sánh tokenizer: `vi` (pyvi) F1 0.77 so với `xx` F1 0.72
- Đánh giá **theo thực thể** (khớp cả biên và nhãn). LOC không có trong tập test
- 🗣 **Nói:** ORG tốt nhất. PER recall cao nhưng precision thấp: mô hình hay đoán nhầm tên riêng khác thành người. F1 dao động khoảng ±0.02 giữa các lần chạy vì tập test nhỏ.

## Slide 23 — Demo · ⏱ 3 phút
- Slide chỉ có tiêu đề **"Demo"** + ảnh dự phòng `Phan2/results/demo.html`
- Làm trực tiếp theo **Kịch bản demo** cuối file

## Slide 24 — Phân tích lỗi Phần 2 · ⏱ 0.75 phút
| Câu (rút gọn) | Gold | Dự đoán | Loại lỗi |
|---|---|---|---|
| "…các đồng sự tại **AT&T Labs**…" | AT&T Labs (ORG) | T Labs (MISC) | Sai biên do ký tự "&" |
| "…quản lý bởi **PyTorch Foundation** - một tổ chức…" | PyTorch Foundation (ORG) | PyTorch Foundation - một (MISC) | Sai biên + sai nhãn |
| "…trên GPU **NVIDIA** có hỗ trợ **CUDA**." | NVIDIA (ORG), CUDA (MISC) | NVIDIA (MISC), CUDA. (PER) | Nhầm nhãn, dính dấu chấm |
| "…**Hinton** được trao **Giải Turing**…" | Hinton (PER) | Hinton (ORG) | Tên đứng một mình, thiếu ngữ cảnh |

- Lỗi chủ yếu: **sai biên** (dấu câu, ký tự đặc biệt) và **nhầm ORG ↔ MISC**

## Slide 25 — Tóm tắt Phần 2 · ⏱ 0.5 phút
- Đạt được: 97 câu có nguồn rõ ràng, gán thực thể + quan hệ trên Label Studio qua LAN, NER F1 ≈ 0.77
- Hạn chế: dữ liệu ít (test 19 câu); mất cân bằng (MISC 196 so với LOC 8); MISC gộp nhiều loại; quan hệ chưa có mô hình
- Hướng phát triển: thêm dữ liệu; tách MISC thành ALGO/TOOL/DATASET/METRIC; dùng PhoBERT; train mô hình trích xuất quan hệ

---

# KẾT LUẬN (1 phút)

## Slide 26 — Kết luận chung · ⏱ 0.75 phút
| | Phần 1 | Phần 2 |
|---|---|---|
| Kết quả chính | 20 nhãn tay → gán thêm 159 câu, đúng 61% | NER F1 ≈ 0.77 |
| Bài học | Ít nhãn thì lỗi dễ tự khuếch đại | Biên thực thể và tokenizer ảnh hưởng nhiều |

- Điểm chung: **chất lượng và số lượng nhãn** quyết định kết quả; tiếng Việt cần tiền xử lý riêng (teencode, tách từ, dấu câu)
- Hướng chung: thêm dữ liệu gán tay, dùng mô hình pretrained tiếng Việt (PhoBERT)

## Slide 27 — Cảm ơn / Hỏi đáp · ⏱ 0.25 phút
- "Cảm ơn thầy và các bạn đã lắng nghe"
- Link repo: `https://github.com/thanhgiang0607/NLP_Baitapnhom`

---

## Kịch bản demo (Slide 23, 3 phút)

**Chuẩn bị trước giờ trình bày** (mở sẵn):
```bash
cd ~/NLP_Baitapnhom && source .venv/bin/activate && cd Phan2
label-studio start --host 0.0.0.0 --port 8080      # tab 1: Label Studio
python scripts/demo_ner.py                          # tab 2: demo NER, để sẵn dấu nhắc ">"
```

| Bước | Thời gian | Làm gì | Nói gì |
|---|---:|---|---|
| 1 | 45 giây | Mở `http://192.168.1.25:8080` → project `NLP_Nhóm1_v2` → câu ID 144 | "Dữ liệu nhóm gán trên Label Studio qua LAN: thực thể tô màu, mũi tên là quan hệ" |
| 2 | 30 giây | (Tuỳ chọn) Tô thử 1 từ, kéo 1 quan hệ, rồi **bấm hủy, không Submit** | "Cách gán nhãn: chọn nhãn, bôi đen từ; quan hệ thì chọn 2 thực thể" |
| 3 | 45 giây | Sang terminal, gõ 2 câu đúng (dưới) | "Mô hình nhận diện thực thể trên câu chưa từng thấy" |
| 4 | 30 giây | Trình duyệt mở `results/demo.html` (tải lại trang sau mỗi câu) | Chỉ vào từng thực thể |
| 5 | 30 giây | Gõ câu có lỗi → chuyển sang Slide 24 | "Mô hình vẫn sai biên ở dấu chấm cuối câu" |

**Câu gợi ý đã chạy thử:**
- `Andrew Ng từng làm việc tại Google Brain và Baidu trước khi giảng dạy ở Đại học Stanford.` → đúng hết
- `Hugging Face phát hành thư viện Transformers cho Python.` → đúng hết
- `Mô hình YOLO đạt mAP cao trên bộ dữ liệu COCO.` → **lỗi:** `COCO.` thành PER

**Dự phòng:** máy lỗi thì chiếu ảnh `demo.html` trên Slide 23, hoặc mở `Phan2/NER_KHDL.ipynb` mục 9.

---

## Câu hỏi có thể gặp

### Phần 1
| Câu hỏi | Trả lời ngắn |
|---|---|
| Đề yêu cầu semi-supervised, sao lại dùng Naive Bayes? | Semi-supervised là cách học; mỗi vòng cần một bộ phân loại để đoán nhãn. Naive Bayes là bộ phân loại trong bài giảng (S20, Lab 06) |
| Vì sao ngưỡng 0.9? | Chỉ nhận câu mô hình rất chắc chắn để hạn chế nhãn sai đi vào tập học; thấp hơn thì lỗi lan nhanh hơn |
| Vì sao bỏ đặc trưng `False` của Lab 06? | Dữ liệu quá ít (20 câu, 1385 từ): các `False` lấn át từ có nghĩa, mô hình tự tin 100% nhưng sai |
| Vì sao không dùng pyvi/underthesea? | Bám sát công cụ trong bài giảng (regex, NLTK); đánh đổi là từ ghép bị tách đôi |
| Đánh giá kiểu gì khi không có nhãn chuẩn? | Chấm tay toàn bộ 159 câu máy gán theo quy tắc đúng/sai/trung tính; kết quả chấm không đưa ngược vào huấn luyện |
| Sao kết quả lệch về neg? | Lỗi tự khuếch đại: sau vòng 1 tập học nghiêng về neg, mô hình học lại càng nghiêng thêm |

### Phần 2
| Câu hỏi | Trả lời ngắn |
|---|---|
| Gán O để làm gì khi code spaCy lọc bỏ O? | spaCy vốn coi chữ không tô là O nên điểm NER không đổi. Giá trị nằm ở dữ liệu đầy đủ hơn: cụm nối ("của", "do", "tại") là dấu hiệu nhận biết quan hệ |
| Nhãn có phải do máy gán không? | Máy gán sẵn (từ điển + luật), nhóm duyệt và sửa 97/97 câu. Đây là cách gán nhãn có hỗ trợ của máy, phổ biến trong thực tế |
| Vì sao F1 dao động? | Tập test nhỏ (19 câu, 59 thực thể); đổi vài thực thể là F1 thay đổi vài phần trăm |
| Vì sao chọn tokenizer `vi`? | Giống notebook của thầy, F1 cao hơn `xx`, dù pyvi gây lệch biên ở một số từ cuối câu |
| P/R tính theo token hay thực thể? | Theo thực thể: chỉ đúng khi trùng cả biên và nhãn (slide 09) |

### Câu hỏi chung
| Câu hỏi | Trả lời ngắn |
|---|---|
| Phần 1 không dùng pyvi, Phần 2 lại dùng, có mâu thuẫn không? | Mỗi phần bám theo công cụ của bài giảng tương ứng: Phần 1 theo Lab 03/06 (regex, NLTK), Phần 2 theo notebook spaCy B5 (`spacy.blank("vi")` dùng pyvi) |
| Hai phần liên quan gì nhau? | Cùng là gán nhãn văn bản tiếng Việt khi ít dữ liệu: Phần 1 gán nhãn cả câu, Phần 2 gán nhãn từng cụm từ. Cả hai cho thấy nhãn tay ít thì mô hình dễ sai |
