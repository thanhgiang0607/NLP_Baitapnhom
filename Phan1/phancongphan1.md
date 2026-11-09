# Phần 1 

Chia thành **3 việc**. Nhóm 1 và 2 dùng chung 200 bình luận; nhóm 3 **tự cào dữ liệu riêng trên DuckDuckGo**:

| Nhóm | Việc | Dữ liệu đầu vào | Kết quả chính |
|---|---|---|---|
| 1 | Semi-supervised (bán giám sát) | 200 bình luận (`data/comments_raw.csv`) | Nhãn tích cực/tiêu cực cho 200 bình luận |
| 2 | Thuật toán Turney | 200 bình luận (`data/comments_raw.csv`) | Điểm SO của các cụm + nhãn cho từng bình luận |
| 3 | Từ điển cảm xúc không giám sát (kiểu WordNet) | Kết quả tìm kiếm tự cào trên DuckDuckGo | 50 từ tích cực + 50 từ tiêu cực |

---

## Dữ liệu

- Tiếng Việt, lấy từ một trang mạng xã hội (Facebook, Threads, ...).
- **Không có gán nhãn sẵn.**
- Khi thu thập phải chọn **một chủ đề**: ở đây là **trí tuệ nhân tạo**.
- Thu thập **200 bình luận** liên quan đến chủ đề đó.

**Đã xong:** bộ 200 bình luận nằm ở `Phan1/data/comments_raw.csv` (nguồn Threads). **Nhóm 1 và nhóm 2** dùng chung file này, không ai sửa.

**Nhóm 3 không dùng file này** để xây từ điển: nhóm 3 tự cào dữ liệu trên DuckDuckGo (xem mục Nhóm 3).

---

## Nhóm 1 – Semi-supervised (bán giám sát)

### Thầy yêu cầu
Gán nhãn thủ công theo nhóm **10 bình luận tích cực + 10 bình luận tiêu cực**, rồi áp dụng semi-supervised lên **toàn bộ dữ liệu**.

### Hiểu đơn giản
- *Supervised* (có giám sát) = máy học từ nhiều dữ liệu đã có nhãn. Ở đây ta chỉ có 20 nhãn, quá ít.
- *Semi-supervised* = dùng **ít dữ liệu có nhãn + nhiều dữ liệu chưa nhãn**. Máy học từ 20 bình luận có nhãn trước, sau đó **tự đoán nhãn** cho phần còn lại.
- Cách làm phổ biến (self-training): cho máy đoán nhãn các bình luận chưa gán. Bình luận nào máy **rất tự tin** thì coi như đã có nhãn, thêm vào tập học. Rồi học lại, đoán lại, lặp nhiều lần, tập có nhãn lớn dần.

### Các bước
1. Đọc và chọn 10 bình luận tích cực, 10 tiêu cực. Ghi `id` và nhãn lại (đề xuất lưu vào `data/labels_manual.csv`). **20 nhãn này cũng là bộ nhãn chung** để nhóm 2 kiểm tra kết quả của mình.
2. Cho máy học từ 20 bình luận này.
3. Máy đoán các bình luận còn lại, giữ lại những dự đoán chắc chắn, học lại, lặp.
4. Kết quả: nhãn đoán cho toàn bộ 200 bình luận.

---

## Nhóm 2 – Thuật toán Turney - Thanh Hằng

### Thầy yêu cầu
- Chọn **1 từ đại diện tốt** và **1 từ đại diện xấu**.
- Tính điểm cảm xúc bằng **PMI** dựa trên **số kết quả tìm kiếm** (search hits).
- Được phép thêm cụm **"trí tuệ nhân tạo"** vào các truy vấn tìm kiếm.

### Ý tưởng
Thuật toán của Turney dựa trên một nhận xét: **cụm từ tích cực thường xuất hiện gần các từ tốt, cụm từ tiêu cực thường xuất hiện gần các từ xấu.** Không cần ai gán nhãn: ta chỉ cần hai từ mẫu (ví dụ "tốt" và "tệ") rồi đo xem một cụm "gần" từ nào hơn.

Ví dụ: cụm "rất hay" mà hay đứng gần chữ "tốt" hơn chữ "tệ" thì nghiêng tích cực. Cụm "sai hoài" thì ngược lại.

### Các bước của thuật toán
1. **Tách từ và gán từ loại** (danh từ, động từ, tính từ, phó từ...) cho từng bình luận. Tiếng Việt dùng `underthesea` hoặc `pyvi`.
2. **Lấy ra các cụm 2 từ có mẫu từ loại mang ý kiến**: ví dụ tính từ + danh từ, phó từ + tính từ. (Lưu ý: tiếng Việt thường để tính từ đứng sau danh từ, nên cũng có mẫu "danh từ + tính từ".)
3. **Chọn 1 từ mẫu tốt và 1 từ mẫu xấu.**
4. **Tính điểm cho từng cụm** theo công thức:

   `SO(cụm) = log2 [ hits(cụm NEAR tốt) × hits(xấu) ] / [ hits(cụm NEAR xấu) × hits(tốt) ]`

   - `hits(...)` là **số kết quả** mà công cụ tìm kiếm trả về.
   - `NEAR` nghĩa là hai thứ đứng **gần nhau** trong văn bản.
   - `SO` > 0 → cụm tích cực; `SO` < 0 → cụm tiêu cực.
   - Thầy cho phép thêm "trí tuệ nhân tạo" vào truy vấn để kết quả sát chủ đề.
5. **Điểm của một bình luận** = trung bình điểm SO của các cụm trong nó. Dương → tích cực, âm → tiêu cực.

PMI (Pointwise Mutual Information) là thước đo "hai thứ cùng xuất hiện nhiều hơn mức ngẫu nhiên bao nhiêu". Công thức trên chính là hiệu của hai giá trị PMI (PMI với từ tốt trừ PMI với từ xấu).

### Kết quả cần có
- Danh sách các cụm và điểm SO của chúng.
- Nhãn tích cực/tiêu cực cho từng bình luận.
- So với 20 nhãn tay: máy đoán đúng bao nhiêu.

---

## Nhóm 3 – Từ điển cảm xúc không giám sát (kiểu WordNet) - Gia Khang

### Thầy yêu cầu
- Áp dụng **unsupervised** (không giám sát), theo hướng **WordNet**.
- Dùng **toán tử Google** (dấu `+`, dấu nháy kép `"..."`) hoặc tốt hơn là **API của DuckDuckGo**.
- Bắt đầu từ vài **từ mẫu** như *good – well* (tốt) và *awful – evil* (xấu).
- Kết quả cuối: **50 từ khoá đặc trưng nhất cho tích cực** và **50 từ khoá đặc trưng nhất cho tiêu cực**.
- Trình bày bằng **slide**. Demo là **tuỳ chọn**.

### Dữ liệu của nhóm 3
Nhóm 3 **không dùng 200 bình luận** để xây từ điển. Dữ liệu của nhóm là **kết quả tìm kiếm tự cào trên DuckDuckGo** (tiêu đề + đoạn trích của mỗi kết quả). Từ đó nhóm rút ra các từ mang cảm xúc.

### Hiểu đơn giản
Ta muốn có một **từ điển cảm xúc**: danh sách từ nào tích cực, từ nào tiêu cực. Làm tay thì tốn công. Cách "không giám sát": chỉ đưa vào vài từ mẫu, rồi **để máy tự tìm thêm** các từ cùng chiều hoặc ngược chiều.

Bài giảng (`07 - sentiment.pptx`, slide 66–67) mô tả cách làm bằng WordNet (Kim & Hovy): đi từ vài từ mẫu, tìm từ **đồng nghĩa** và **trái nghĩa** của chúng, rồi lặp lại:
- **Tập tích cực** = từ đồng nghĩa của từ tích cực + từ trái nghĩa của từ tiêu cực.
- **Tập tiêu cực** = từ đồng nghĩa của từ tiêu cực + từ trái nghĩa của từ tích cực.

Tiếng Anh tra đồng nghĩa/trái nghĩa bằng WordNet. Tiếng Việt không có WordNet dùng được, nên **dùng DuckDuckGo thay cho WordNet**, đúng như thầy gợi ý.

Bài giảng còn một cách bổ sung (Hatzivassiloglou & McKeown, slide 49 và 67): **"và" thường nối hai từ cùng chiều** ("rẻ và bền"), **"nhưng" thường nối hai từ ngược chiều** ("tốt nhưng đắt": *đắt* là tiêu cực).

Dấu nháy kép trong tìm kiếm nghĩa là "tìm đúng nguyên cụm này".

### Các bước
1. **Chọn từ mẫu** (bản tiếng Việt của các từ trong slide):
   - Tích cực: *tốt, hay*.
   - Tiêu cực: *tệ, xấu* (có thể thêm *ác*).
2. **Cào DuckDuckGo (bước thu dữ liệu của nhóm 3).** Với mỗi từ mẫu, tìm hai loại truy vấn:
   - *Kiểu WordNet:* `"đồng nghĩa với tốt"`, `"trái nghĩa với tốt"`. Kết quả thường là các trang từ điển liệt kê sẵn từ đồng nghĩa/trái nghĩa.
   - *Kiểu liên từ:* `"tốt và"`, `"tốt nhưng"`.
   - Có thể thêm `trí tuệ nhân tạo` vào truy vấn để từ tìm được sát chủ đề hơn.

   Lưu mọi kết quả vào một file CSV trong folder nhóm 3 (mỗi dòng: truy vấn, tiêu đề, đoạn trích, link). **Đây là bộ dữ liệu của nhóm 3**; lưu lại để khỏi phải cào lại.
3. **Rút từ mới từ kết quả.** Đọc các đoạn trích, lấy những từ mang cảm xúc (chủ yếu là tính từ), xếp vào tập tích cực hay tiêu cực theo quy tắc ở trên. Ví dụ:
   - "trái nghĩa với tốt" ra *kém* → *kém* vào tập tiêu cực.
   - "tốt nhưng đắt" → *đắt* vào tập tiêu cực.
4. **Lặp lại.** Dùng các từ mới làm từ mẫu cho vòng sau, làm 2–3 vòng. Mỗi vòng chỉ lấy khoảng 10 từ chắc chắn nhất cho mỗi chiều, nếu không số lần tìm tăng rất nhanh.
5. **Lọc** (slide 66 có bước "Filter"):
   - Bỏ từ nhiễu: từ nối, tên riêng, từ không mang cảm xúc.
   - Từ rơi vào cả hai tập thì xem bên nào được nhắc nhiều hơn; không rõ thì bỏ.
6. **Xếp hạng, lấy top 50.** Điểm của một từ = số lần được tìm thấy ở phía tích cực − số lần ở phía tiêu cực. Lấy **50 từ tích cực** và **50 từ tiêu cực** có điểm cao nhất.
7. **Làm slide:** từ mẫu, các truy vấn đã dùng, ví dụ một từ được suy ra thế nào, bảng 50 + 50 từ, hạn chế. Demo là tuỳ chọn.

*Tuỳ chọn:* thử áp từ điển lên 200 bình luận (đếm số từ tích cực và tiêu cực trong mỗi bình luận) để minh hoạ. Không bắt buộc.

### Lưu ý thực tế
- Cào DuckDuckGo bằng thư viện Python không chính thức (`ddgs`). Tìm liên tục dễ bị chặn tạm thời, nên mỗi lần tìm nghỉ vài giây.
- DuckDuckGo **không trả về tổng số kết quả**, nên nhóm 3 đếm số lần từ xuất hiện trong các đoạn trích đã cào (không dùng "số kết quả tìm kiếm" như Turney).
- Nên chạy thử vài truy vấn trước khi cào nhiều.

---

## Slide và nộp bài

- Mỗi nhóm trình bày cách làm và kết quả (tối thiểu: bài toán, ý tưởng, các bước, kết quả, hạn chế).
- Nhóm 3 bắt buộc có **danh sách 50 từ tích cực và 50 từ tiêu cực**.
- Thầy yêu cầu **báo cáo ngắn**, hạn **13/11**.

---
