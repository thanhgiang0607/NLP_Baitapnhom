# 1. Semi-supervised

1. Gán nhãn thủ công **10 bình luận tích cực + 10 bình luận tiêu cực** (`seed_labeled.csv`).
2. Huấn luyện bộ phân loại ban đầu (Naive Bayes / MaxEnt) trên 20 câu này.
3. Self-training: dự đoán 180 câu còn lại, thêm các câu có độ tin cậy cao vào tập huấn luyện, lặp lại.
4. Xuất nhãn cho toàn bộ 200 bình luận + thống kê kết quả.

Slide tham khảo: `07 - sentiment.pptx` S48–55.
