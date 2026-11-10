# PHẦN 1: Phân tích cảm xúc bán giám sát (semi-supervised) trên bình luận tiếng Việt về Trí tuệ nhân tạo

## 0. Trạng thái

| # | Yêu cầu | Trạng thái | Kết quả |
|---|---------|------------|---------|
| 1 | Thu thập 200 bình luận tiếng Việt về một chủ đề, chưa gán nhãn | ✅ Xong | 200 bình luận Threads về AI → `data/comments_raw.csv` |
| 2 | Gán nhãn thủ công 10 tích cực + 10 tiêu cực | ✅ Xong | `data/labels_manual.csv` |
| 3 | Áp dụng semi-supervised lên toàn bộ dữ liệu | ✅ Xong | Self-training + Naive Bayes, 4 vòng, gán thêm 159 câu → `1_SemiSupervised/results.csv` |
| 4 | Đánh giá kết quả | ✅ Xong | Chấm tay 159 câu máy gán: đúng 61% trên câu có cảm xúc; thống kê 21 câu `unknown` |
| 5 | Tổng hợp kết quả vào slide (demo không bắt buộc) | ⏳ Còn lại | Số liệu cho slide ở mục 6 |

---

## 1. Bài toán

**Phân tích cảm xúc (sentiment analysis)** trên bình luận tiếng Việt về **trí tuệ nhân tạo**, dạng đơn giản nhất: xác định thái độ của văn bản là tích cực hay tiêu cực (`07 - sentiment.pptx`, S15).

- **Đầu vào:** một bình luận, ví dụ
  > phải bỏ tiền ra mới biết con claude đỉnh cỡ nào
- **Đầu ra:** một trong ba nhãn

| Nhãn | Ý nghĩa |
|---|---|
| `pos` | tích cực: khen, ủng hộ AI |
| `neg` | tiêu cực: chê, lo ngại, phản đối AI |
| `unknown` | mô hình không đủ chắc chắn để gán `pos` hay `neg` |

**Ràng buộc:** chỉ gán tay **20 bình luận** (10 `pos`, 10 `neg`). 180 bình luận còn lại do máy tự gán bằng phương pháp **bán giám sát**.

Tên đầy đủ của phương pháp: **self-training với bộ phân loại nền Naive Bayes**. Semi-supervised quy định *cách học* (tự mở rộng tập học qua nhiều vòng), còn trong mỗi vòng cần một mô hình để *đoán nhãn*; Naive Bayes đảm nhận vai trò đó (`07 - sentiment.pptx`, S20: tokenization → feature extraction → phân loại bằng Naive Bayes).

---

## 2. Các khái niệm cần biết

| Khái niệm | Giải thích ngắn |
|---|---|
| **Học có giám sát (supervised)** | Máy học từ nhiều ví dụ đã có nhãn rồi đoán nhãn cho dữ liệu mới. Cần rất nhiều dữ liệu có nhãn |
| **Học bán giám sát (semi-supervised)** | Chỉ có **ít** dữ liệu có nhãn và **nhiều** dữ liệu chưa nhãn; máy dùng phần ít ỏi đó để tự mở rộng (S48) |
| **Self-training** | Học từ phần có nhãn → đoán phần chưa nhãn → câu nào đoán **rất chắc chắn** thì nhận nhãn đó, thêm vào tập học → học lại → lặp |
| **Bộ phân loại (classifier)** | Mô hình nhận một câu, trả lời "thuộc nhãn nào, chắc chắn bao nhiêu %" |
| **Naive Bayes** | Bộ phân loại dựa trên đếm: mỗi từ xuất hiện trong bao nhiêu câu `pos`, bao nhiêu câu `neg`, rồi gom bằng chứng của các từ trong câu (`06 - naivebayes.pptx`) |
| **Token / tách từ** | Cắt câu thành từng chữ và dấu câu để máy đếm được |
| **Đặc trưng (feature)** | Thông tin rút ra từ câu để máy học. Ở đây: `contains(từ) = True` nếu câu có chứa từ đó |
| **Boolean Naive Bayes** | Chỉ xét từ **có mặt hay không**, một từ lặp nhiều lần cũng tính một lần (S25) |
| **Đánh dấu phủ định `NOT_`** | Thêm `NOT_` vào các từ sau từ phủ định đến dấu câu kế tiếp, để "không hay" khác "hay" (S23) |
| **Làm mịn (smoothing)** | Cộng thêm một lượng nhỏ vào mọi lần đếm để không có xác suất bằng 0. Bài giảng cộng 1 (Laplace), NLTK cộng 0.5 |
| **Độ tự tin (confidence)** | Xác suất của nhãn được chọn, từ 0.5 (phân vân) đến 1.0 (chắc chắn) |
| **Ngưỡng (threshold)** | Độ tự tin tối thiểu để một câu được nhận nhãn máy đoán. Bài dùng **0.9** |
| **Lỗi tự khuếch đại** | Nhãn sai ở vòng trước trở thành dữ liệu học ở vòng sau, khiến lỗi lan dần. Điểm yếu cố hữu của self-training |

---

## 3. Tổng quan quy trình

```
Threads ──► Lọc bình luận ──► Gán tay ──► Tiền xử lý ──► Naive Bayes ──► Self-training ──► Xuất kết quả ──► Chấm tay
(10 bài)     (200 câu)       (20 câu)    regex + NOT_    (20 câu)       (ngưỡng 0.9,      results.csv      159 câu máy gán
                                                                         4 vòng)                           + 21 câu unknown
```

| Bước | Công cụ | Đầu vào | Đầu ra |
|---|---|---|---|
| 1. Thu thập | Trình duyệt (Threads), `data/check_data.py` | 10 bài đăng về AI | `data/comments_raw.csv` |
| 2. Gán tay | Đọc và chọn thủ công | `comments_raw.csv` | `data/labels_manual.csv` |
| 3. Tiền xử lý | `re`, `pandas` (ô 2 notebook) | 2 file trên | cột `tokens` |
| 4. Naive Bayes ban đầu | `nltk.NaiveBayesClassifier` (ô 3) | 20 câu có nhãn | bộ phân loại ban đầu |
| 5. Self-training | `nltk` (ô 4) | 20 câu có nhãn + 180 câu chưa nhãn | cột `pred`, `conf`, `round` |
| 6. Xuất kết quả | `pandas` (ô 5) | | `1_SemiSupervised/results.csv` |
| 7. Đánh giá | Hiển thị bảng + chấm tay (ô 6–8) | 159 câu máy gán, 21 câu `unknown` | tỉ lệ đúng/sai/trung tính |

Toàn bộ code nằm trong một notebook: `1_SemiSupervised/semi_supervised.ipynb`. Chỉ dùng `pandas` và `nltk` (giống Lab 06).

---

## 4. Dữ liệu

- **Nguồn:** bình luận công khai trên **Threads**, chủ đề trí tuệ nhân tạo (ChatGPT, Claude, Gemini...), thu thập ngày 09/11/2026 từ 10 bài đăng. Danh sách bài đăng: `data/README.md`.
- **Quy mô:** 200 bình luận, trung bình **24.6 chữ/bình luận**, từ vựng sau tiền xử lý **1385 từ**.
- **Cách lọc:** bỏ quảng cáo, link, số điện thoại, bình luận trùng, bình luận dưới 6 từ, bình luận không nói về AI; không lưu tên người dùng; giữ nguyên chữ gốc (viết tắt, tiếng lóng, emoji); trộn ngẫu nhiên (seed 42) rồi đánh `id` 1–200.
- **Định dạng:** `data/comments_raw.csv`, 2 cột `id`, `text`. Câu có dấu phẩy được bọc trong `"..."` theo quy tắc CSV; khi đọc bằng Python dấu `"` tự biến mất.
- **Nhãn tay** (`data/labels_manual.csv`):

| Nhãn | id | Ví dụ |
|------|----|-------|
| `pos` | 8, 18, 45, 56, 57, 70, 103, 111, 131, 165 | "AI là thứ tuyệt vời nhất con người tạo ra" (18), "phải bỏ tiền ra mới biết claude đỉnh cỡ nào" (70) |
| `neg` | 16, 46, 59, 104, 116, 120, 125, 155, 187, 192 | "gemini rất đần" (16), "meta.ai quá phế để xài" (104) |

Tiêu chí chọn 20 câu: khen/chê **chính AI** (không phải người dùng), không chọn câu nửa khen nửa chê, từ ngữ đa dạng vì mô hình chỉ học được những từ có trong 20 câu này.

- **Đặc điểm:** văn nói, viết tắt ("ko", "vs", "t", "đc"), tiếng lóng, xen tiếng Anh; khoảng **một nửa số câu trung tính** (hỏi đáp, kể chuyện).

---

## 5. Các bước làm chi tiết

### Bước 1 — Thu thập dữ liệu
1. Mở 10 bài đăng về AI trên Threads (đã đăng nhập để xem đủ bình luận trả lời).
2. Lấy chữ của bình luận, lọc theo tiêu chí ở mục 4.
3. Trộn ngẫu nhiên, đánh `id`, ghi `data/comments_raw.csv`.
4. Kiểm tra bằng `python3 data/check_data.py`: đúng 2 cột, đủ 200 dòng, không trùng, không ô trống, không lỗi mã hoá.

### Bước 2 — Gán nhãn tay
- Đọc 200 câu, chọn 10 câu khen rõ và 10 câu chê rõ theo tiêu chí ở mục 4, ghi `data/labels_manual.csv` (cột `id`, `label`).

### Bước 3 — Tiền xử lý (ô 2)
1. Đọc 200 câu, ghép 20 nhãn tay theo `id`. 180 câu còn lại có nhãn trống (`NaN`).
2. **Chữ thường + tách từ bằng regex** (Lab 03): `re.findall(r"\w+|[.,!?;]", ...)` cắt câu thành chữ và dấu câu; emoji, ký tự lạ tự bị loại.
3. **Đánh dấu phủ định** (S23): sau một trong các từ "không, ko, k, chẳng, chả, chưa", mọi từ đến dấu câu kế tiếp được thêm `NOT_`. Từ phủ định vẫn giữ.

| | Câu 155 |
|---|---|
| Gốc | cảm thấy con Gemini nó ko có sự liền mạch để trả lời trong 1 topic, nhiều khi... |
| Sau xử lý | `cảm, thấy, con, gemini, nó, ko, NOT_có, NOT_sự, NOT_liền, NOT_mạch, ..., NOT_topic, nhiều, khi, ...` |

- Kết quả kiểm tra: `NaN 180 | pos 10 | neg 10`.
- **Không dùng bộ tách từ tiếng Việt** (pyvi, underthesea) để bám sát công cụ trong bài giảng; đánh đổi là từ ghép bị tách đôi ("trả lời" → `trả`, `lời`).

### Bước 4 — Huấn luyện Naive Bayes ban đầu (ô 3)
1. Mỗi câu biến thành tập đặc trưng `{contains(từ): True}` cho các từ **có mặt** (Boolean NB, S25), giống hàm `document_features` của Lab 06.
2. Huấn luyện `nltk.NaiveBayesClassifier` trên 20 câu có nhãn.
3. In 10 đặc trưng phân biệt mạnh nhất và thử đoán 2 câu mới.

**Khác Lab 06:** Lab 06 ghi cả từ **không có mặt** (`contains(x) = False`) cho toàn bộ từ vựng. Cách này đã được thử và loại bỏ:
- Từ vựng 1385 từ, mỗi câu khoảng 25 từ → mỗi câu kèm khoảng 1360 giá trị `False`.
- Chỉ 20 câu để học → các giá trị `False` tạo hàng nghìn "bằng chứng" ngẫu nhiên, lấn át từ có nghĩa.
- Kết quả thử: "AI này trả lời hay ghê" bị đoán `neg` với độ tự tin **100%**.

Lab 06 không gặp vấn đề vì học trên 2000 bài review phim. Chỉ giữ từ có mặt cho độ tự tin trải đều từ khoảng 0.5 đến 1.0, đúng như self-training cần.

**Đặc trưng phân biệt mạnh nhất:**

```
contains(luôn)   = True    pos : neg = 3.0 : 1.0
contains(là)     = True    pos : neg = 3.0 : 1.0
contains(tâm)    = True    pos : neg = 2.3 : 1.0
contains(NOT_có) = True    neg : pos = 1.7 : 1.0
```

- Cách đọc: câu có chữ "luôn" thì khả năng `pos` gấp 3 lần `neg`. "luôn" có trong 4 câu `pos` (8, 45, 103, 111) và 1 câu `neg` (155); sau làm mịn: (4 + 0.5) / (1 + 0.5) = 3.0.
- Danh sách có nhiều từ vô nghĩa ("là", "luôn", "chứ"): với 20 câu, trùng hợp cũng thành quy luật. Đây là lý do cần self-training.
- Từ chỉ xuất hiện ở **một** nhãn ("đỉnh" chỉ trong câu `pos`, "phế" chỉ trong câu `neg`) phân biệt mạnh nhất nhưng hàm hiển thị của NLTK xếp xuống cuối; khi đoán nhãn mô hình vẫn dùng đúng các từ này.

| Câu thử | Dự đoán | Độ tự tin |
|---|---|---:|
| claude đỉnh thật | `pos` | 0.94 |
| gemini phế | `neg` | 0.75 |

### Bước 5 — Self-training (ô 4)
```
Tập có nhãn = 20 câu gán tay
Lặp:
    1. Huấn luyện Naive Bayes trên Tập có nhãn
    2. Đoán nhãn + độ tự tin cho mỗi câu chưa có nhãn
    3. Câu nào độ tự tin ≥ 0.9 → nhận nhãn máy đoán, đưa vào Tập có nhãn
    4. Vòng không thêm được câu nào → dừng
```

| Cột | Ý nghĩa |
|---|---|
| `pred` | Nhãn cuối cùng (ban đầu chỉ có 20 nhãn tay) |
| `conf` | Độ tự tin khi máy gán |
| `round` | `0` = gán tay; `1`, `2`... = vòng máy gán; trống = chưa bao giờ được gán |

### Bước 6 — Xuất kết quả (ô 5)
- Câu không bao giờ đạt ngưỡng → `unknown`.
- Ghi `1_SemiSupervised/results.csv` (cột `id, text, label, pred, conf, round`, mã hoá `utf-8-sig` để mở bằng Excel không lỗi tiếng Việt).
- Thống kê số câu theo nhãn và theo vòng (`pd.crosstab`).

### Bước 7 — Đánh giá bằng chấm tay (ô 6–8)
1. Hiển thị 3 bảng trong notebook: 20 câu gán tay, 159 câu máy gán (xếp theo nhãn), 21 câu `unknown`.
2. Đọc toàn bộ 159 câu máy gán, chấm theo quy tắc:

| Trường hợp | Kết quả chấm |
|---|---|
| Máy gán đúng | đúng |
| Câu khen mà máy gán `neg`, hoặc câu chê mà máy gán `pos` | `sai` |
| Câu trung tính (không khen, không chê) mà máy vẫn gán `pos`/`neg` | `tt` |

   - Câu vừa khen vừa chê: chấm theo ý chính (câu 105 "Con claude tạo ảnh hơi ngu. Còn lại thì bá" → khen). Khen chê ngang nhau → `tt`.
   - Câu khen/chê **người dùng** chứ không phải AI → `tt`.
   - Các câu cùng kiểu được chấm thống nhất (ví dụ mọi câu "bong bóng AI không vỡ, AI là tương lai" đều tính là ủng hộ AI).
3. Ghi id các câu `sai`, `tt` vào hai danh sách trong notebook; code tự tính tỉ lệ.
4. Đọc riêng 21 câu `unknown`, phân loại thủ công thành trung tính / tích cực / tiêu cực.

Kết quả chấm tay **chỉ dùng để đánh giá**, không đưa ngược vào huấn luyện (nếu không, bài thành học có giám sát).

---

## 6. Kết quả

**Self-training qua các vòng:**

| Vòng | Thêm `neg` | Thêm `pos` | Tổng thêm | Tổng có nhãn |
|---|---:|---:|---:|---:|
| 0 (gán tay) | 10 | 10 | 20 | 20 |
| 1 | 47 | 37 | 84 | 104 |
| 2 | 53 | 9 | 62 | 166 |
| 3 | 1 | 7 | 8 | 174 |
| 4 | 4 | 1 | 5 | 179 |
| 5 | 0 | 0 | 0 | dừng |

**Nhãn cuối cùng của 200 câu:**

| Nhãn | Số câu | Tỉ lệ |
|---|---:|---:|
| `neg` | 115 | 57.5% |
| `pos` | 64 | 32.0% |
| `unknown` | 21 | 10.5% |

**Chấm tay 159 câu máy gán:**

| | Số câu | Tỉ lệ |
|---|---:|---:|
| Đúng | 49 | 31% |
| Sai | 31 | 19% |
| Trung tính | 79 | 50% |

**Độ đúng trên câu có cảm xúc** (bỏ câu trung tính):

| | Đúng / có cảm xúc | Tỉ lệ |
|---|---:|---:|
| **Tổng** | **49 / 80** | **61%** |
| Máy gán `pos` | 30 / 37 | 81% |
| Máy gán `neg` | 19 / 43 | 44% |
| Vòng 1 | 33 / 46 | 72% |
| Vòng 2 | 10 / 26 | 38% |
| Vòng 3–4 | 6 / 8 | 75% (quá ít câu, không đủ để kết luận) |

**21 câu `unknown`:**

| Đánh giá thủ công | Số câu | id |
|---|---:|---|
| Trung tính (hỏi đáp, kể chuyện, chê người dùng) | 14 | 5, 6, 10, 30, 42, 73, 87, 117, 140, 142, 146, 148, 153, 181 |
| Tích cực | 6 | 34, 64, 91, 122, 169, 180 |
| Tiêu cực | 1 | 119 |

**Nhận xét:**
- Từ 20 câu gán tay, mô hình tự gán thêm **159 câu** qua 4 vòng; trên các câu có cảm xúc, đúng **61%**.
- **Một nửa số câu máy gán là câu trung tính** (79/159): với chỉ hai nhãn `pos`/`neg`, các câu này bị ép vào một trong hai. Đây là hạn chế lớn nhất.
- Mô hình nhận câu khen khá tốt (81%) nhưng **gán `neg` quá tay** (44%).
- **Lỗi tự khuếch đại:** vòng 2 thêm 53 câu `neg` nhưng chỉ 9 câu `pos`, và độ đúng giảm từ 72% (vòng 1) xuống 38% (vòng 2). Sau vòng 1 tập học đã nghiêng về `neg`, nhãn sai tích tụ nên mô hình càng lệch.
- **2/3 câu `unknown` là trung tính:** ngưỡng 0.9 giữ lại đúng những câu không có cảm xúc rõ. 7 câu có cảm xúc bị bỏ sót chủ yếu vì từ cảm xúc không có trong 20 câu gán tay ("khôn", "okela"), vì châm biếm (119, 180), hoặc vì câu quá ngắn (15/21 câu dưới 15 chữ).
- Lỗi thường gặp ở câu máy gán sai: **châm biếm, nói mỉa** (172 "Nó viết còn thấy hay thì rớt là đúng r" bị gán `pos`), **câu khen có từ phủ định** (29 "nó không có phán xét" bị gán `neg`), **câu khen kèm một ý chê** (164 "Chat gpt số 1 lòng e, lâu lâu hay bịa số liệu..." bị gán `neg`).

Mô hình sau self-training lệch về `neg` rõ rệt khi so với mô hình ban đầu:

| Câu thử | Mô hình ban đầu (20 câu) | Mô hình cuối (179 câu) |
|---|---|---|
| Claude viết code đỉnh thật, dùng rất tiện | `pos` 0.68 ✓ | `neg` 0.56 ✗ |
| Gemini trả lời ngu quá, toàn bịa | `neg` 0.90 ✓ | `neg` 0.99 ✓ |
| ChatGPT không hay lắm | `pos` 0.70 ✗ | `neg` 0.51 ✓ |
| Có ai dùng Copilot chưa ạ (trung tính) | `neg` 0.63 | `neg` 0.95 |

File kết quả: `1_SemiSupervised/results.csv`; số liệu chấm tay nằm trong 2 ô cuối của `semi_supervised.ipynb`.

---

## 7. Hạn chế

- **Quá ít dữ liệu nhãn:** 20 câu → mô hình ban đầu học cả trùng hợp ngẫu nhiên ("là", "luôn" bị coi là từ tích cực).
- **Lỗi tự khuếch đại:** nhãn sai ở vòng trước thành dữ liệu học ở vòng sau; tập nhãn lệch dần về `neg`.
- **Chỉ hai nhãn `pos`/`neg`:** khoảng một nửa dữ liệu là câu trung tính nhưng vẫn bị ép vào `pos` hoặc `neg`.
- **Tiền xử lý đơn giản:** không tách từ ghép tiếng Việt, không chuẩn hoá viết tắt/teencode; phủ định chỉ nhận 6 từ cố định và không xử lý "không có phán xét" (phủ định của một ý xấu = ý tốt).
- **Ngôn ngữ mạng xã hội:** châm biếm, nói mỉa khó nhận ra chỉ bằng việc đếm từ.
- **Đánh giá thủ công:** việc chấm đúng/sai phụ thuộc cảm nhận người chấm; chưa có người chấm thứ hai để đối chiếu.

## 8. Hướng cải thiện

- Gán tay nhiều câu hơn và đa dạng từ ngữ hơn ở bước gán nhãn.
- Tăng ngưỡng (ví dụ 0.99) hoặc mỗi vòng chỉ nhận số câu `pos` và `neg` bằng nhau để tránh lệch nhãn.
- Thêm nhãn trung tính (`neu`) và gán tay thêm một số câu trung tính.
- Dùng bộ tách từ tiếng Việt và từ điển chuẩn hoá teencode.
- Thử bộ phân loại khác trong bài giảng (MaxEnt, SVM, S20) làm bộ phân loại nền.
- Cho hai người cùng chấm để đo độ đồng thuận (Cohen's kappa).

---

## 9. Cấu trúc thư mục

```
Phan1/                           # (trong repo NLP_Baitapnhom, cạnh Phan2/)
├── data/
│   ├── comments_raw.csv         # ★ 200 bình luận (id, text), đã chốt, không sửa
│   ├── labels_manual.csv        # ★ 20 nhãn tay (id, label)
│   ├── check_data.py            # kiểm tra comments_raw.csv
│   └── README.md                # nguồn: 10 bài đăng Threads + cách lọc
├── 1_SemiSupervised/
│   ├── semi_supervised.ipynb    # tiền xử lý + Naive Bayes + self-training + chấm tay
│   ├── results.csv              # nhãn cuối cùng của 200 câu
│   └── README.md
├── slides/                      # slide báo cáo
├── README.md
├── PHAN1_KE_HOACH.md
└── SLIDE_BO_CUC.md
```

## 10. Cách chạy lại

1. Cài Python và VS Code (extension **Python**, **Jupyter**).
2. Mở `1_SemiSupervised/semi_supervised.ipynb`, chọn kernel Python.
3. Chạy ô đầu tiên để cài thư viện (`%pip install nltk pandas`), chỉ cần một lần.
4. Bấm **Run All**. Kết quả giống hệt mục 6 vì thuật toán không có yếu tố ngẫu nhiên.

- Kiểm tra dữ liệu: `cd Phan1/data && python3 check_data.py`.
- Cảnh báo `FutureWarning` ở ô hiển thị bảng chỉ là thông báo của pandas về phiên bản sau, không ảnh hưởng kết quả.

## Tài liệu tham khảo (bài giảng)

| Nội dung | Nguồn |
|---|---|
| Phân tích cảm xúc, quy trình cơ bản | `07 - sentiment.pptx` S15, S20 |
| Đánh dấu phủ định `NOT_` | `07 - sentiment.pptx` S23 |
| Boolean Naive Bayes | `07 - sentiment.pptx` S25 |
| Học bán giám sát | `07 - sentiment.pptx` S48 |
| Naive Bayes, làm mịn | `06 - naivebayes.pptx` |
| Tách từ bằng regex | Lab 03 – Text Processing |
| `nltk.NaiveBayesClassifier`, `document_features` | Lab 06 – Learning to Classify Text |
