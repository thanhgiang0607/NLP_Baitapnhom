# Dữ liệu Phần 1

**Các file:**
- `comments_raw.csv` – 200 dòng, đúng 2 cột `id`, `text`.
- `labels_manual.csv` – 20 nhãn tay (10 `pos`, 10 `neg`), cột `id`, `label`.

| id | text |
|---|---|
| 1 | lý do là sử dụng AI vô tội vạ, prompt thì viết như loz ấy ông |
| 4 | Ê t sợ r, nó giống cái góc học của nhà ngoại t |

Quy tắc: UTF-8 · mỗi bình luận một dòng · giữ nguyên chữ gốc (không viết thường, không bỏ dấu câu/emoji) · **đã chốt, không sửa**.
Đọc file bằng Python: `pd.read_csv("comments_raw.csv", encoding="utf-8-sig")`. Kiểm tra: `python3 check_data.py`.

## Nguồn
- Nền tảng: **Threads** (bình luận công khai, tiếng Việt), chủ đề **trí tuệ nhân tạo / ChatGPT / Claude / Gemini**
- Ngày thu thập: **09/11/2026**
- 10 bài đăng (lấy bình luận trả lời của từng bài):
  1. threads.com/@bachvuthien0129600/post/DWA5MiKDxZE – tâm sự với ChatGPT
  2. threads.com/@henry_qdn_/post/DZtm5d0koTh – nộp bài viết bằng AI bị rớt môn
  3. threads.com/@cobebonghong/post/DX042AtGjug – lý do AI không thể thay thế con người
  4. threads.com/@panda.tmth/post/DaFpfaBk0dQ – tự học AI
  5. threads.com/@cttnhh.motminhtao/post/DZFG0UCEYC7 – chấm điểm các AI đã dùng
  6. threads.com/@cucdabietbay/post/De168uKD_w1 – nhờ Claude làm tiểu luận
  7. threads.com/@yagi.dayyy/post/DejYdG9ksuD – bong bóng AI
  8. threads.com/@sieunhangioitoanthan/post/DdAwHURErTR – xếp hạng AI viết luận
  9. threads.com/@hailuunehihi/post/DanUrGKn2Z6 – ChatGPT tạo ảnh
  10. threads.com/@phanpt200395/post/DZBhQw5EyQ- – học dùng Claude

## Cách lọc (để ghi vào báo cáo)
- Đọc bằng trình duyệt khi đã đăng nhập Threads; lấy chữ bình luận, **không lưu tên người dùng**.
- Mỗi bài lấy mẫu rải đều qua các bình luận; bỏ quảng cáo/bán tài khoản, link, số điện thoại, bình luận dưới 6 từ, bình luận trùng, bình luận không nói về AI.
- Xóa tên tài khoản dính ở cuối câu và phần quảng cáo dính vào cuối một vài bình luận; không sửa nội dung khác.
- Trộn ngẫu nhiên (seed 42) rồi đánh `id` 1–200.

## Lưu ý về dữ liệu
- Phần lớn là văn nói, viết tắt, tiếng lóng, kèm tiếng Anh (prompt, free, pro...).
- Có cả khen, chê và trung tính; **chưa gán nhãn**; 20 câu rõ khen/chê đã gán tay trong `labels_manual.csv`.
- Khoảng một nửa số câu bàn về việc dùng AI để viết bài/học tập và so sánh các AI (ChatGPT, Claude, Gemini...).
