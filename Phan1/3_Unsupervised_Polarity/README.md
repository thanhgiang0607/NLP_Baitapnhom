# 3. Unsupervised – tạo polarity kiểu WordNet

1. Bắt đầu từ từ hạt giống (slide: good, well → positive; awful, evil → negative) – dùng bản tiếng Việt tương ứng.
2. Mở rộng tập từ: đồng nghĩa của từ tích cực + trái nghĩa của từ tiêu cực → positive; ngược lại → negative.
3. Đo đồng xuất hiện bằng tìm kiếm: Google (`+` cho đồng thời, `" "` cho cụm chính xác) hoặc tốt hơn là **DuckDuckGo API**.
4. Kết quả: bộ từ điển 2 cực, **50 keyword đặc trưng nhất cho positive và 50 cho negative**.
5. Áp dụng lên 200 bình luận + demo.

Slide tham khảo: `07 - sentiment.pptx` S66–67.
