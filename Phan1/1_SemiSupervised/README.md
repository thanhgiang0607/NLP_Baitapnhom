# Semi-supervised

Notebook: `semi_supervised.ipynb` (chạy trong VS Code, thư viện `nltk`, `pandas`).

1. Đọc `../data/comments_raw.csv` và 20 nhãn tay `../data/labels_manual.csv`.
2. Tiền xử lý: chữ thường, tách từ bằng regex, gắn `NOT_` sau từ phủ định (S23).
3. Naive Bayes (`nltk.NaiveBayesClassifier`, Lab 06) với đặc trưng "từ có mặt" (Boolean NB, S25).
4. Self-training: đoán 180 câu còn lại, thêm câu tự tin cao vào tập học, lặp lại.
5. Xuất nhãn cho 200 bình luận + thống kê.
