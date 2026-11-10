# Phần 1 – Semi-supervised (bán giám sát)

Nhóm mình chỉ làm **bài 1: semi-supervised** trên 200 bình luận tiếng Việt về **trí tuệ nhân tạo**.

---

## Thầy yêu cầu

- Dữ liệu tiếng Việt từ một mạng xã hội, **chưa gán nhãn**, chọn **một chủ đề** (trí tuệ nhân tạo), **200 bình luận**.
- Gán nhãn thủ công **10 bình luận tích cực + 10 bình luận tiêu cực**.
- Áp dụng **semi-supervised** lên **toàn bộ dữ liệu**.
- Trình bày bằng **slide**. Demo (chạy code trực tiếp khi thuyết trình) không bắt buộc.

---

## Hiểu đơn giản

- **Phân tích cảm xúc:** với mỗi bình luận, đoán nó **tích cực** (khen) hay **tiêu cực** (chê).
- **Supervised (có giám sát):** máy học từ thật nhiều câu đã có nhãn. Ở đây chỉ có 20 câu có nhãn, quá ít.
- **Semi-supervised (bán giám sát):** dùng **ít câu có nhãn + nhiều câu chưa nhãn**. Cách làm (self-training):
  1. Máy học từ 20 câu có nhãn.
  2. Máy đoán nhãn các câu còn lại.
  3. Câu nào máy **rất tự tin** thì coi như đã có nhãn, thêm vào tập học.
  4. Học lại, đoán lại, lặp đến khi không thêm được câu nào nữa.

---

## Các bước và tình trạng

| # | Bước | Kiến thức trong bài giảng | Tình trạng |
|---|---|---|---|
| 1 | Thu thập 200 bình luận | – | ✅ `data/comments_raw.csv` |
| 2 | Gán nhãn tay 10 pos + 10 neg | – | ✅ `data/labels_manual.csv` |
| 3 | Tiền xử lý: chữ thường, tách từ bằng regex, gắn `NOT_` sau từ phủ định | Lab 03 (Text Processing); `07 - sentiment` S23 (Negation) | Đang làm |
| 4 | Huấn luyện Naive Bayes trên 20 câu (đặc trưng: từ có mặt hay không) | Lab 06 (`nltk.NaiveBayesClassifier`); `06 - naivebayes`; `07 - sentiment` S25 (Boolean NB) | |
| 5 | Self-training: đoán 180 câu, thêm câu tự tin cao, học lại, lặp | `07 - sentiment` S48 (semi-supervised) | |
| 6 | Xuất nhãn 200 câu + thống kê; tự đọc kiểm tra 20–30 câu | – | |
| 7 | Làm slide | – | |

Code nằm trong `1_SemiSupervised/semi_supervised.ipynb` (Jupyter notebook trong VS Code). Chỉ dùng thư viện `nltk` và `pandas`.

---

## Slide nên có

1. Bài toán và dữ liệu (nguồn Threads, 200 câu, hạn chế: tiếng lóng, viết tắt, nhiều câu trung tính).
2. 20 câu gán nhãn tay.
3. Tiền xử lý (ví dụ một câu trước/sau, phần `NOT_`).
4. Naive Bayes và vòng lặp self-training (mỗi vòng thêm bao nhiêu câu).
5. Kết quả: số câu pos/neg trên 200 câu, vài ví dụ đúng và sai.
6. Hạn chế: chỉ 20 nhãn; không dùng bộ tách từ tiếng Việt ("trả lời" bị tách thành 2 chữ); câu trung tính bị ép vào pos/neg.

---

## Làm chung trên GitHub

- **Sync trước khi bắt đầu làm**, làm xong thì Commit + Sync (nhớ gõ ghi chú trước khi bấm Commit).
- Không sửa `data/comments_raw.csv` và `data/labels_manual.csv`.
