# Phần 1 – Phân tích cảm xúc bình luận tiếng Việt về chủ đề "Trí tuệ nhân tạo"

**Dữ liệu:**
- Nhóm 1 và 2: 200 bình luận tiếng Việt, chưa gán nhãn, về chủ đề trí tuệ nhân tạo, thu thập từ Threads (`data/comments_raw.csv`).
- Nhóm 3: tự cào kết quả tìm kiếm trên DuckDuckGo (lưu trong folder nhóm 3).

Phân công và giải thích chi tiết: `phancongphan1.md`.

| Thư mục | Nội dung |
|---|---|
| `data/` | 200 bình luận (`comments_raw.csv`) cho nhóm 1, 2 + 20 nhãn tay (`labels_manual.csv`) |
| `1_SemiSupervised/` | Gán nhãn tay 10 tích cực / 10 tiêu cực → semi-supervised trên toàn bộ dữ liệu |
| `2_Turney/` | Thuật toán Turney (PMI với 1 từ đại diện tốt, 1 từ đại diện xấu) |
| `3_Unsupervised_Polarity/` | Unsupervised kiểu WordNet + DuckDuckGo/Google search → 50 keyword positive, 50 keyword negative |
| `slides/` | Slide báo cáo + demo |

Tham khảo bài giảng: `B3/07 - sentiment.pptx` (S24–26 Naive Bayes + S48 semi-supervised, S56–65 Turney, S49–55 và S66–67 xây từ điển / WordNet).
