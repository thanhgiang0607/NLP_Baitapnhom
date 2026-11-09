# 2. Thuật toán Turney

1. Tách từ + gán từ loại tiếng Việt (underthesea / pyvi).
2. Trích các cụm 2 từ theo mẫu từ loại (tính từ + danh từ, trạng từ + tính từ, ...).
3. Chọn **1 từ đại diện tốt** và **1 từ đại diện xấu**.
4. Tính Semantic Orientation bằng PMI dựa trên số kết quả tìm kiếm (cụm + từ đặc trưng + "trí tuệ nhân tạo"):
   SO(phrase) = log2[ hits(phrase NEAR tốt) · hits(xấu) / ( hits(phrase NEAR xấu) · hits(tốt) ) ]
5. Điểm bình luận = trung bình SO các cụm → tích cực nếu > 0.

Slide tham khảo: `07 - sentiment.pptx` S56–65.
