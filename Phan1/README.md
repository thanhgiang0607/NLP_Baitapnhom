# Phần 1 – Phân tích cảm xúc bình luận tiếng Việt về chủ đề "Trí tuệ nhân tạo"

**Dữ liệu chung:** 200 bình luận tiếng Việt, chưa gán nhãn, thu thập từ mạng xã hội (Facebook, Threads, ...) về chủ đề trí tuệ nhân tạo.

| Thư mục | Nội dung |
|---|---|
| `data/` | Dữ liệu thô 200 bình luận (`comments_raw.csv`) và các file đã xử lý |
| `1_SemiSupervised/` | Gán nhãn tay 10 tích cực / 10 tiêu cực → semi-supervised trên toàn bộ dữ liệu |
| `2_Turney/` | Thuật toán Turney (PMI với 1 từ đại diện tốt, 1 từ đại diện xấu) |
| `3_Unsupervised_Polarity/` | Unsupervised kiểu WordNet + DuckDuckGo/Google search → 50 keyword positive, 50 keyword negative |
| `slides/` | Slide báo cáo + demo |

Tham khảo bài giảng: `B3/07 - sentiment.pptx` (S48–55 semi-supervised, S56–65 Turney, S66–67 WordNet).
