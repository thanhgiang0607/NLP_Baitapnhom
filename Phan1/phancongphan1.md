# Phần 1 

Chia thành **3 việc**, đều chạy trên **cùng một bộ dữ liệu**:

| Nhóm | Việc |
|---|---|---|
| 1 | Semi-supervised (bán giám sát) |
| 2 | Thuật toán Turney |
| 3 | Từ điển cảm xúc không giám sát (kiểu WordNet) |

---

## Dữ liệu

- Tiếng Việt, lấy từ một trang mạng xã hội (Facebook, Threads, ...).
- **Không có gán nhãn sẵn.**
- Khi thu thập phải chọn **một chủ đề**: ở đây là **trí tuệ nhân tạo**.
- Thu thập **200 bình luận** liên quan đến chủ đề đó.

**Đã xong:** bộ 200 bình luận nằm ở `Phan1/data/comments_raw.csv` (nguồn Threads). Cả 3 nhóm dùng chung file này, không sửa.

---

## Nhóm 1 – Semi-supervised (bán giám sát)

### Thầy yêu cầu
Gán nhãn thủ công theo nhóm **10 bình luận tích cực + 10 bình luận tiêu cực**, rồi áp dụng semi-supervised lên **toàn bộ dữ liệu**.

### Hiểu đơn giản
- *Supervised* (có giám sát) = máy học từ nhiều dữ liệu đã có nhãn. Ở đây ta chỉ có 20 nhãn, quá ít.
- *Semi-supervised* = dùng **ít dữ liệu có nhãn + nhiều dữ liệu chưa nhãn**. Máy học từ 20 bình luận có nhãn trước, sau đó **tự đoán nhãn** cho phần còn lại.
- Cách làm phổ biến (self-training): cho máy đoán nhãn các bình luận chưa gán. Bình luận nào máy **rất tự tin** thì coi như đã có nhãn, thêm vào tập học. Rồi học lại, đoán lại, lặp nhiều lần, tập có nhãn lớn dần.

### Các bước
1. Đọc và chọn 10 bình luận tích cực, 10 tiêu cực. Ghi `id` và nhãn lại (đề xuất lưu vào `data/labels_manual.csv`). **20 nhãn này cũng là bộ nhãn chung** để nhóm 2 và nhóm 3 kiểm tra kết quả của mình.
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

### Hiểu đơn giản
Ta muốn có một **từ điển cảm xúc**: danh sách từ nào tích cực, từ nào tiêu cực. Làm tay thì tốn công. Cách "không giám sát": chỉ đưa vào vài từ mẫu, rồi **để máy tự tìm thêm** các từ cùng nghĩa/cùng chiều.

Hai ý tưởng trong bài giảng:
- **WordNet** (Kim & Hovy): từ nào là **đồng nghĩa** của từ tích cực thì cũng tích cực; từ **trái nghĩa** của nó thì tiêu cực. Cứ mở rộng dần từ các từ mẫu.
- **Liên từ** (Hatzivassiloglou & McKeown): trong câu, **"và" thường nối hai từ cùng chiều** ("rẻ và bền" cùng tích cực), còn **"nhưng" thường nối hai từ ngược chiều** ("tốt nhưng đắt": đắt là tiêu cực). Dùng công cụ tìm kiếm để tìm các cụm như "tốt và ...", "tốt nhưng ...", lấy từ ở chỗ trống rồi suy ra cực tính.

Dấu nháy kép trong tìm kiếm nghĩa là "tìm đúng nguyên cụm này", nên rất tiện để tìm mẫu "tốt và ...".

### Các bước
1. Chọn từ mẫu tích cực (ví dụ "tốt", "hay") và tiêu cực (ví dụ "tệ", "xấu").
2. Từ mỗi từ mẫu, tìm các từ mới (đồng nghĩa/trái nghĩa hoặc qua liên từ "và/nhưng").
3. Từ mới thành từ mẫu cho vòng kế tiếp; lặp vài vòng.
4. Xếp hạng, lấy **50 từ tích cực** và **50 từ tiêu cực** đặc trưng nhất.
5. Làm slide trình bày cách làm và kết quả (demo nếu muốn).

---

## Slide và nộp bài

- Mỗi nhóm trình bày cách làm và kết quả (tối thiểu: bài toán, ý tưởng, các bước, kết quả, hạn chế).
- Nhóm 3 bắt buộc có **danh sách 50 từ tích cực và 50 từ tiêu cực**.
- Thầy yêu cầu **báo cáo ngắn**, hạn **13/11**.

---
