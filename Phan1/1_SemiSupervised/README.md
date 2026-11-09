# 1. Semi-supervised

1. Gán nhãn thủ công **10 bình luận tích cực + 10 bình luận tiêu cực** (lưu vào `../data/labels_manual.csv`, cột `id,label`, nhãn `pos`/`neg`; nhóm 2 cũng dùng file này để kiểm tra).
2. Huấn luyện bộ phân loại ban đầu (Naive Bayes / MaxEnt) trên 20 câu này.
3. Self-training: dự đoán 180 câu còn lại, thêm các câu có độ tin cậy cao vào tập huấn luyện, lặp lại.
4. Xuất nhãn cho toàn bộ 200 bình luận + thống kê kết quả.

Slide tham khảo: `07 - sentiment.pptx` S24–26 (Naive Bayes cho cảm xúc) và S48 (ý tưởng semi-supervised: bắt đầu từ vài ví dụ có nhãn rồi tự mở rộng); bài `06 - naivebayes.pptx`.
(Lưu ý: S49–55 là phương pháp Hatzivassiloglou & McKeown để xây *từ điển*, gần với nhóm 3 hơn.)
