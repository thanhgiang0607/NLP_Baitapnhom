# Giải thích bài làm: Phân tích cảm xúc bán giám sát (semi-supervised)

Tài liệu này mô tả toàn bộ quy trình của bài, từ dữ liệu đầu vào đến kết quả cuối cùng, để người đọc chưa học NLP vẫn hiểu được mỗi bước làm gì và vì sao làm như vậy. Code tương ứng nằm trong `semi_supervised.ipynb`.

---

## 1. Bài toán

**Đầu vào:** 200 bình luận tiếng Việt trên mạng xã hội Threads, cùng chủ đề **trí tuệ nhân tạo** (ChatGPT, Claude, Gemini...). Các bình luận **chưa có nhãn**.

**Đầu ra:** mỗi bình luận được gán một trong ba nhãn:

| Nhãn | Ý nghĩa |
|---|---|
| `pos` | tích cực: khen, ủng hộ AI |
| `neg` | tiêu cực: chê, lo ngại, phản đối AI |
| `unknown` | mô hình không đủ chắc chắn để gán `pos` hay `neg` |

Đây là bài toán **phân tích cảm xúc** (sentiment analysis), dạng đơn giản nhất: xác định thái độ của văn bản là tích cực hay tiêu cực (`07 - sentiment.pptx`, S15).

**Ràng buộc:** chỉ được gán nhãn tay **20 bình luận** (10 `pos`, 10 `neg`). 180 bình luận còn lại phải do máy tự gán bằng phương pháp **bán giám sát**.

---

## 2. Các khái niệm cần biết

| Khái niệm | Giải thích |
|---|---|
| **Học có giám sát** (supervised) | Máy học từ nhiều ví dụ đã có đáp án (nhãn), rồi đoán nhãn cho dữ liệu mới. Cần rất nhiều dữ liệu có nhãn. |
| **Học bán giám sát** (semi-supervised) | Chỉ có **ít** dữ liệu có nhãn và **nhiều** dữ liệu chưa nhãn. Máy dùng phần ít ỏi đó để tự mở rộng dần (`07 - sentiment.pptx`, S48). |
| **Self-training** (tự huấn luyện) | Một cách làm bán giám sát: học từ phần có nhãn → đoán phần chưa nhãn → câu nào đoán **rất chắc chắn** thì coi như đã có nhãn, thêm vào tập học → học lại → lặp. |
| **Bộ phân loại** (classifier) | Mô hình nhận vào một câu và trả lời "câu này thuộc nhãn nào, chắc chắn bao nhiêu %". Bài dùng **Naive Bayes**. |
| **Token / tách từ** | Cắt câu thành các đơn vị nhỏ (từ, dấu câu) để máy đếm được. |
| **Đặc trưng** (feature) | Thông tin rút ra từ câu để máy học. Ở đây là: câu có chứa từ X hay không. |
| **Độ tự tin** (confidence) | Xác suất mô hình gán cho nhãn nó chọn, từ 0.5 (phân vân) đến 1.0 (chắc chắn). |

**Semi-supervised là phương pháp, Naive Bayes là mô hình.** Semi-supervised quy định *cách học* (tự mở rộng tập dữ liệu học qua nhiều vòng). Trong mỗi vòng vẫn cần một mô hình để *đoán nhãn*. Naive Bayes đảm nhận vai trò đó. Bài làm vì vậy được gọi đầy đủ là: **self-training với bộ phân loại nền Naive Bayes**.

---

## 3. Tổng quan quy trình

```
 200 bình luận thô (comments_raw.csv)
        │
        ▼
 [Bước 1] Gán nhãn tay 20 câu (labels_manual.csv)
        │
        ▼
 [Bước 2] Tiền xử lý: chữ thường, tách từ, đánh dấu phủ định
        │
        ▼
 [Bước 3] Huấn luyện Naive Bayes trên 20 câu có nhãn
        │
        ▼
 [Bước 4] Self-training: đoán 180 câu → nhận câu chắc chắn ≥ 0.9 → học lại → lặp
        │
        ▼
 [Bước 5] Xuất kết quả 200 câu (results.csv) + thống kê
        │
        ▼
 [Bước 6] Đọc kiểm tra thủ công độ đúng của các câu máy gán
```

Công cụ: Python, Jupyter Notebook (trong VS Code), thư viện `pandas` (xử lý bảng) và `nltk` (Naive Bayes, giống Lab 06).

---

## 4. Dữ liệu

**Nguồn:** bình luận công khai trên Threads, thu thập ngày 09/11/2026 từ 10 bài đăng về AI (danh sách bài đăng trong `../data/README.md`).

**Cách lọc:**
- Bỏ quảng cáo, link, số điện thoại, bình luận trùng, bình luận dưới 6 từ, bình luận không nói về AI.
- Không lưu tên người dùng.
- Giữ nguyên chữ gốc (viết tắt, tiếng lóng, emoji).
- Trộn ngẫu nhiên rồi đánh số `id` từ 1 đến 200.

**File:** `../data/comments_raw.csv`, 2 cột:

| id | text |
|---|---|
| 1 | lý do là sử dụng AI vô tội vạ, prompt thì viết như loz ấy ông |
| 3 | Nếu có source rồi thì dùng notebookLM á mom |

Trong file CSV, câu nào có dấu phẩy được bọc trong dấu `"..."` để máy không nhầm dấu phẩy trong câu với dấu phẩy ngăn cột. Khi đọc bằng Python, dấu `"` tự biến mất.

**Đặc điểm cần lưu ý:**
- Văn nói, viết tắt nhiều ("ko", "vs", "t", "đc"), tiếng lóng, xen tiếng Anh.
- Khoảng một nửa số câu **trung tính**: hỏi đáp, kể chuyện, không khen không chê.

---

## 5. Bước 1: Gán nhãn tay 20 câu

Chọn 10 câu **khen rõ ràng** và 10 câu **chê rõ ràng**, lưu vào `../data/labels_manual.csv` (cột `id`, `label`).

**Tiêu chí chọn:**
- Khen/chê **chính AI**, không phải chê người dùng.
- Không chọn câu nửa khen nửa chê.
- Từ ngữ đa dạng, vì mô hình chỉ học được những từ có trong 20 câu này.

| Nhãn | id | Ví dụ (rút gọn) |
|---|---|---|
| `pos` | 8, 18, 45, 56, 57, 70, 103, 111, 131, 165 | "AI là thứ tuyệt vời nhất con người tạo ra" (18), "phải bỏ tiền ra mới biết claude đỉnh cỡ nào" (70) |
| `neg` | 16, 46, 59, 104, 116, 120, 125, 155, 187, 192 | "gemini rất đần" (16), "meta.ai quá phế để xài" (104) |

---

## 6. Bước 2: Tiền xử lý

**Mục đích:** máy không hiểu nghĩa câu, chỉ đếm từ. Cần đưa mọi câu về một dạng thống nhất để việc đếm có ý nghĩa.

**Code (ô 2 của notebook) làm 3 việc:**

1. **Đọc và ghép dữ liệu:** đọc 200 câu, ghép thêm 20 nhãn tay theo `id`. 180 câu còn lại có nhãn trống (`NaN`).
2. **Chữ thường + tách từ bằng biểu thức chính quy (regex)** (Lab 03): `re.findall(r"\w+|[.,!?;]", ...)` cắt câu thành từng chữ và từng dấu câu. Emoji và ký tự lạ bị loại tự động.
3. **Đánh dấu phủ định** (`07 - sentiment.pptx`, S23): mọi từ đứng **sau** một từ phủ định ("không", "ko", "k", "chẳng", "chả", "chưa") cho đến **dấu câu kế tiếp** được thêm tiền tố `NOT_`. Từ phủ định vẫn được giữ.

**Ví dụ (câu 155):**

| | Nội dung |
|---|---|
| Gốc | cảm thấy con Gemini nó ko có sự liền mạch để trả lời trong 1 topic, nhiều khi... |
| Sau xử lý | `cảm, thấy, con, gemini, nó, ko, NOT_có, NOT_sự, NOT_liền, NOT_mạch, ..., NOT_topic, nhiều, khi, ...` |

**Vì sao cần đánh dấu phủ định:** nếu không, "hay" và "không hay" đều chứa từ "hay", máy sẽ coi chúng giống nhau. Sau khi đánh dấu, "không hay" thành `không NOT_hay`, là một từ khác hẳn "hay".

**Kết quả kiểm tra:** `NaN 180 | pos 10 | neg 10`.

**Hạn chế:** không dùng bộ tách từ tiếng Việt nên từ ghép bị tách đôi ("trả lời" thành `trả` và `lời`); viết tắt và teencode không được chuẩn hoá ("thic", "vs"). Với Naive Bayes chỉ đếm sự có mặt của từ, ảnh hưởng này chấp nhận được.

---

## 7. Bước 3: Huấn luyện Naive Bayes ban đầu

### 7.1. Naive Bayes hoạt động thế nào

Naive Bayes (`06 - naivebayes.pptx`) học bằng cách **đếm**: mỗi từ xuất hiện trong bao nhiêu câu `pos` và bao nhiêu câu `neg`. Khi gặp câu mới, nó gom các bằng chứng từ từng từ trong câu để tính:

- P(pos | câu): xác suất câu là tích cực
- P(neg | câu): xác suất câu là tiêu cực

Nhãn có xác suất cao hơn là nhãn được chọn, và xác suất đó chính là **độ tự tin**.

"Naive" (ngây thơ) vì mô hình giả định các từ độc lập với nhau. Giả định không đúng hoàn toàn nhưng mô hình vẫn hoạt động tốt với văn bản.

**Làm mịn (smoothing):** nếu một từ chưa từng xuất hiện trong câu `neg`, xác suất của nó trong lớp `neg` bằng 0 và sẽ triệt tiêu mọi bằng chứng khác. Để tránh điều này, NLTK cộng thêm 0.5 vào mọi lần đếm (bài giảng dạy cộng 1, tức làm mịn Laplace; ý tưởng giống nhau).

### 7.2. Đặc trưng

Mỗi câu được biểu diễn bằng tập các từ **có mặt**, dạng `{contains(claude): True, contains(đỉnh): True, ...}`. Một từ xuất hiện nhiều lần cũng chỉ tính một lần. Đây là **Boolean Naive Bayes** (`07 - sentiment.pptx`, S25): với cảm xúc, việc một từ *có xuất hiện* quan trọng hơn số lần xuất hiện.

**Khác biệt so với Lab 06:** Lab 06 ghi thêm các từ **không có mặt** (`contains(x) = False`) cho toàn bộ từ vựng. Bài này đã thử cách đó và loại bỏ, vì:
- Từ vựng có 1385 từ, mỗi câu chỉ khoảng 25 từ, nên mỗi câu bị gắn thêm khoảng 1360 giá trị `False`.
- Chỉ có 20 câu để học, nên các giá trị `False` này tạo ra hàng nghìn "bằng chứng" ngẫu nhiên, lấn át các từ thực sự có ý nghĩa.
- Kết quả thử nghiệm: câu "AI này trả lời hay ghê" bị đoán `neg` với độ tự tin **100%**, vừa sai vừa quá chắc chắn.

Lab 06 không gặp vấn đề này vì học trên 2000 bài review phim. Với dữ liệu nhỏ, chỉ giữ từ có mặt cho kết quả hợp lý hơn: độ tự tin trên 180 câu trải đều từ khoảng 0.5 đến 1.0.

### 7.3. Kết quả

**Các từ phân biệt mạnh nhất** (`show_most_informative_features`):

```
contains(luôn) = True     pos : neg = 3.0 : 1.0
contains(là)   = True     pos : neg = 3.0 : 1.0
contains(tâm)  = True     pos : neg = 2.3 : 1.0
contains(NOT_có) = True   neg : pos = 1.7 : 1.0
...
```

Cách đọc dòng đầu: câu có chữ "luôn" thì khả năng là `pos` gấp 3 lần `neg`. Con số đến từ việc đếm: "luôn" có trong 4 câu `pos` (8, 45, 103, 111) và 1 câu `neg` (155), sau làm mịn: (4 + 0.5) / (1 + 0.5) = 3.0.

**Nhận xét:**
- Danh sách chứa nhiều từ vô nghĩa ("là", "luôn", "chứ"). Với chỉ 20 câu, trùng hợp ngẫu nhiên cũng được mô hình coi là quy luật. Đây chính là lý do cần self-training.
- Các từ chỉ xuất hiện ở **một** nhãn (như "đỉnh" chỉ trong câu `pos`, "phế" chỉ trong câu `neg`) là những từ phân biệt mạnh nhất, nhưng hàm hiển thị của NLTK xếp chúng xuống cuối nên không thấy trong bảng. Khi đoán nhãn, mô hình vẫn dùng đúng các từ này.

**Thử đoán câu mới:**

| Câu | Dự đoán | Độ tự tin |
|---|---|---|
| claude đỉnh thật | `pos` | 0.94 |
| gemini phế | `neg` | 0.75 |

"đỉnh" có trong câu `pos` số 70, nên mô hình khá chắc. "phế" có trong câu `neg` số 104, nhưng "gemini" xuất hiện ở cả câu khen (131) lẫn câu chê (16, 155), nên độ tự tin thấp hơn.

---

## 8. Bước 4: Self-training (phần bán giám sát)

### 8.1. Thuật toán

```
Tập có nhãn  = 20 câu gán tay
Lặp:
    1. Huấn luyện Naive Bayes trên Tập có nhãn
    2. Với mỗi câu chưa có nhãn: đoán nhãn + độ tự tin
    3. Câu nào độ tự tin ≥ 0.9 → nhận nhãn máy đoán, đưa vào Tập có nhãn
    4. Nếu vòng này không thêm được câu nào → dừng
```

**Ngưỡng 0.9** đảm bảo chỉ những câu mô hình rất chắc chắn mới được thêm, hạn chế đưa nhãn sai vào tập học.

**Các cột được tạo ra:**

| Cột | Ý nghĩa |
|---|---|
| `pred` | Nhãn cuối cùng (ban đầu chỉ có 20 nhãn tay) |
| `conf` | Độ tự tin khi máy gán |
| `round` | Vòng gán nhãn: `0` = gán tay, `1`, `2`... = máy gán ở vòng đó, trống = chưa bao giờ được gán |

### 8.2. Kết quả

```
Vòng 1: thêm 84 câu, tổng có nhãn 104
Vòng 2: thêm 62 câu, tổng có nhãn 166
Vòng 3: thêm  8 câu, tổng có nhãn 174
Vòng 4: thêm  5 câu, tổng có nhãn 179
Vòng 5: thêm  0 câu → dừng
```

Từ 20 câu ban đầu, mô hình tự gán thêm **159 câu** qua 4 vòng. **21 câu** không bao giờ đạt ngưỡng 0.9, được giữ là `unknown`.

---

## 9. Bước 5: Xuất kết quả và thống kê

Kết quả 200 câu được lưu vào `results.csv` 

**Phân bố nhãn cuối cùng:**

| Nhãn | Số câu | Tỉ lệ |
|---|---|---|
| `neg` | 115 | 57.5% |
| `pos` | 64 | 32% |
| `unknown` | 21 | 10.5% |
| **Tổng** | **200** | |

**Số câu theo vòng và nhãn:**

| Vòng | neg | pos | unknown |
|---|---|---|---|
| 0 (gán tay) | 10 | 10 | 0 |
| 1 | 47 | 37 | 0 |
| 2 | 53 | 9 | 0 |
| 3 | 1 | 7 | 0 |
| 4 | 4 | 1 | 0 |
| không gán | 0 | 0 | 21 |

**Nhận xét quan trọng: lỗi tự khuếch đại.** Ở vòng 1, số câu `neg` và `pos` thêm vào còn tương đối cân bằng (47 và 37). Sang vòng 2, mô hình thêm 53 câu `neg` nhưng chỉ 9 câu `pos`. Nguyên nhân: sau vòng 1, tập học đã nghiêng về `neg`, nên mô hình học lại càng nghiêng về `neg` hơn. Những câu bị gán sai ở vòng trước cũng trở thành dữ liệu học ở vòng sau, khiến lỗi lan dần. Đây là điểm yếu cố hữu của self-training.

---

## 10. Bước 6: Kiểm tra độ đúng

Đọc từng câu và chấm theo quy tắc:

| Trường hợp | Kết quả chấm |
|---|---|
| Máy gán đúng | đúng |
| Câu khen mà máy gán `neg`, hoặc câu chê mà máy gán `pos` | `sai` |
| Câu trung tính (không khen, không chê) mà máy vẫn gán `pos`/`neg` | `tt` (trung tính) |

Câu vừa khen vừa chê được chấm theo ý chính; ví dụ câu 105 "Con claude tạo ảnh hơi ngu. Còn lại thì bá" nghiêng về khen.

Id các câu `sai` và `tt` được ghi trực tiếp vào hai danh sách trong notebook, code tự tính tỉ lệ đúng.

**Kết quả chấm 159 câu máy gán:**

| | Số câu | Tỉ lệ |
|---|---|---|
| Đúng | __ | __% |
| Sai | __ | __% |
| Trung tính | __ | __% |

**21 câu `unknown`** được thống kê riêng: __ câu thực sự trung tính, __ câu có cảm xúc rõ nhưng mô hình không đủ chắc chắn.

---

## 11. Hạn chế

1. **Quá ít dữ liệu nhãn (20 câu):** mô hình ban đầu học cả những trùng hợp ngẫu nhiên ("là", "luôn" bị coi là từ tích cực).
2. **Lỗi tự khuếch đại:** nhãn sai ở vòng trước trở thành dữ liệu học ở vòng sau; tập nhãn lệch dần về `neg`.
3. **Chỉ có hai nhãn pos/neg:** khoảng một nửa dữ liệu là câu trung tính nhưng vẫn bị ép vào `pos` hoặc `neg`.
4. **Tiền xử lý đơn giản:** không tách từ ghép tiếng Việt, không chuẩn hoá viết tắt/teencode; phủ định chỉ nhận một số từ cố định.
5. **Ngôn ngữ mạng xã hội:** châm biếm, nói mỉa ("con của t vẫn khôn mà") khó nhận ra chỉ bằng việc đếm từ.
6. **Đánh giá thủ công:** việc chấm đúng/sai phụ thuộc cảm nhận của người chấm.

## 12. Hướng cải thiện

- Gán tay nhiều câu hơn hoặc đa dạng hơn ở Bước 1.
- Tăng ngưỡng (ví dụ 0.99) hoặc mỗi vòng chỉ nhận số câu `pos` và `neg` bằng nhau để tránh lệch nhãn.
- Thêm nhãn trung tính.
- Dùng bộ tách từ tiếng Việt và từ điển chuẩn hoá teencode.

---

## 13. Cách chạy lại

1. Cài Python, VS Code (extension **Python** và **Jupyter**).
2. Mở `semi_supervised.ipynb`, chọn kernel Python.
3. Chạy ô đầu tiên để cài thư viện (`%pip install nltk pandas`), chỉ cần một lần.
4. Bấm **Run All**. Kết quả giống hệt mô tả ở trên (thuật toán không có yếu tố ngẫu nhiên).

