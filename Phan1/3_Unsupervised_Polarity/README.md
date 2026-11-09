# 3. Unsupervised – tạo polarity kiểu WordNet

**Dữ liệu:** nhóm 3 **không dùng** `data/comments_raw.csv` để xây từ điển. Dữ liệu là kết quả tìm kiếm **tự cào trên DuckDuckGo** (lưu vào một file CSV trong folder này: truy vấn, tiêu đề, đoạn trích, link).

1. Bắt đầu từ từ hạt giống (slide: good, well → positive; awful, evil → negative) – dùng bản tiếng Việt tương ứng.
2. Cào DuckDuckGo (API) cho từng từ mẫu, ví dụ `"đồng nghĩa với tốt"`, `"trái nghĩa với tốt"`, `"tốt và"`, `"tốt nhưng"` (có thể thêm `trí tuệ nhân tạo`). Thầy cho phép dùng toán tử Google (`+` cho đồng thời, `" "` cho cụm chính xác), nhưng ưu tiên **DuckDuckGo API**.
3. Mở rộng tập từ: đồng nghĩa của từ tích cực + trái nghĩa của từ tiêu cực → positive; ngược lại → negative ("và" = cùng chiều, "nhưng" = ngược chiều). Lặp 2–3 vòng, rồi lọc từ nhiễu.
4. Kết quả: bộ từ điển 2 cực, **50 keyword đặc trưng nhất cho positive và 50 cho negative**.
5. Slide trình bày cách làm + bảng 50/50 từ. **Demo: tuỳ chọn.**
6. *Tuỳ chọn:* áp từ điển lên 200 bình luận để minh hoạ (không bắt buộc).

Slide tham khảo: `07 - sentiment.pptx` S66–67.
