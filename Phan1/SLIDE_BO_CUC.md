# Bố cục slide — Phần 1: Phân tích cảm xúc bán giám sát

Khoảng **10 slide**, trình bày 6–8 phút. Phần chữ trong mỗi slide có thể copy thẳng vào slide. Dòng **📸 Chụp** chỉ chỗ cần chụp màn hình trong `1_SemiSupervised/semi_supervised.ipynb` (mở notebook, bấm **Run All** trước khi chụp).

---

## Slide 1 — Tiêu đề
- **Phân tích cảm xúc bán giám sát trên bình luận tiếng Việt về Trí tuệ nhân tạo**
- Self-training với bộ phân loại Naive Bayes
- Tên nhóm, thành viên, môn học, ngày

## Slide 2 — Bài toán và quy trình
- **Bài toán:** xác định bình luận về AI là **tích cực (pos)** hay **tiêu cực (neg)**
- **Ràng buộc:** chỉ gán tay **20/200** câu, 180 câu còn lại máy tự gán (**semi-supervised**)
- Sơ đồ quy trình (vẽ 6 ô, mũi tên ngang):
  **Thu thập 200 câu → Gán tay 20 câu → Tiền xử lý → Naive Bayes → Self-training → Đánh giá**

## Slide 3 — Dữ liệu
- Nguồn: **Threads**, 10 bài đăng về AI (ChatGPT, Claude, Gemini…), thu thập 09/11/2026
- **200 bình luận**, trung bình 24.6 chữ/câu, chưa gán nhãn
- Lọc: bỏ quảng cáo, link, câu trùng, câu < 6 từ, câu không nói về AI; không lưu tên người dùng
- Đặc điểm: văn nói, viết tắt (ko, vs, đc), tiếng lóng; khoảng một nửa là câu trung tính
- Ví dụ:
  > "phải bỏ tiền ra mới biết con claude đỉnh cỡ nào"
  > "Nếu có source rồi thì dùng notebookLM á mom"
- 📸 **Chụp:** bảng thứ nhất ở **ô 6** (20 câu gán tay) hoặc vài dòng đầu `data/comments_raw.csv` mở trong VS Code

## Slide 4 — Gán nhãn tay 20 câu
- **10 pos + 10 neg**, tiêu chí: khen/chê **chính AI**, không chọn câu nửa khen nửa chê, từ ngữ đa dạng

  | Nhãn | Ví dụ |
  |---|---|
  | pos | "AI là thứ tuyệt vời nhất con người tạo ra" · "claude viết hay đến nỗi vỗ đùi khen hay" |
  | neg | "gemini rất đần" · "meta.ai quá phế để xài" |

- 📸 **Chụp:** bảng thứ nhất ở **ô 6** (cột `text`, `pred`)

## Slide 5 — Tiền xử lý
- Chữ thường + tách từ bằng **regex** (Lab 03)
- **Đánh dấu phủ định `NOT_`** (slide S23): thêm `NOT_` vào các từ sau "không/ko/k/chẳng/chả/chưa" đến dấu câu kế tiếp → "không hay" khác "hay"
- Ví dụ câu 155:
  > ko có sự liền mạch → `ko NOT_có NOT_sự NOT_liền NOT_mạch`
- 📸 **Chụp:** kết quả **ô 2** (`NaN 180 / pos 10 / neg 10`)

## Slide 6 — Naive Bayes ban đầu
- **Semi-supervised là phương pháp, Naive Bayes là mô hình** đoán nhãn trong mỗi vòng
- Đặc trưng: `contains(từ) = True` cho từ **có mặt** (Boolean NB, S25), `nltk.NaiveBayesClassifier` (Lab 06)
- Khác Lab 06: **bỏ đặc trưng `False`** (từ không có mặt). Với 20 câu và 1385 từ vựng, các giá trị `False` lấn át từ có nghĩa → đoán "AI này trả lời hay ghê" là `neg` 100%
- Thử: "claude đỉnh thật" → **pos 0.94** · "gemini phế" → **neg 0.75**
- 📸 **Chụp:** kết quả **ô 3** (bảng Most Informative Features + 2 dòng thử)

## Slide 7 — Self-training
- Thuật toán (vẽ vòng lặp 4 ô):
  **Huấn luyện → Đoán câu chưa nhãn → Nhận câu có độ tự tin ≥ 0.9 → Lặp đến khi không thêm được câu nào**

  | Vòng | Thêm neg | Thêm pos | Tổng có nhãn |
  |---|---:|---:|---:|
  | 0 (gán tay) | 10 | 10 | 20 |
  | 1 | 47 | 37 | 104 |
  | 2 | 53 | 9 | 166 |
  | 3 | 1 | 7 | 174 |
  | 4 | 4 | 1 | 179 |

- Kết quả 200 câu: **neg 115 · pos 64 · unknown 21**
- 📸 **Chụp:** kết quả **ô 4** (dòng "Vong 1…Vong 5") và bảng crosstab **ô 5**

## Slide 8 — Đánh giá ★
- Chấm tay toàn bộ **159 câu máy gán**: đúng / sai / trung tính

  | | Số câu | Tỉ lệ |
  |---|---:|---:|
  | Đúng | 49 | 31% |
  | Sai | 31 | 19% |
  | Trung tính | 79 | 50% |

- **Trên câu có cảm xúc** (bỏ trung tính): đúng **49/80 = 61%**
  - Máy gán pos đúng **81%** · máy gán neg đúng **44%**
  - Vòng 1 đúng **72%** · vòng 2 đúng **38%**
- Lưu ý khi trình bày: **31%** thấp chủ yếu vì một nửa số câu là trung tính, mô hình chỉ có 2 nhãn; **61%** mới đo khả năng phân biệt khen/chê
- 📸 **Chụp:** kết quả **ô 8** + bảng quy tắc chấm ở **ô 7**

## Slide 9 — Phân tích lỗi và câu unknown
- **Lỗi tự khuếch đại:** vòng 2 thêm 53 neg / 9 pos, độ đúng giảm 72% → 38%. Nhãn sai ở vòng trước thành dữ liệu học ở vòng sau

  | Câu thử | Mô hình ban đầu | Mô hình cuối |
  |---|---|---|
  | Claude viết code đỉnh thật, dùng rất tiện | pos 0.68 ✓ | neg 0.56 ✗ |
  | Gemini trả lời ngu quá, toàn bịa | neg 0.90 ✓ | neg 0.99 ✓ |

- Ví dụ gán sai:

  | Câu | Máy gán | Lý do |
  |---|---|---|
  | "Nó viết còn thấy hay thì rớt là đúng r" | pos | châm biếm |
  | "Tại nó không có phán xét tao" | neg | "không" + ý xấu = ý tốt |
  | "Chat gpt số 1 lòng e, lâu lâu hay bịa số liệu…" | neg | khen kèm một ý chê |

- **21 câu unknown:** 14 trung tính, 6 tích cực, 1 tiêu cực → ngưỡng 0.9 giữ lại đúng phần lớn câu không có cảm xúc; câu bị bỏ sót do từ mới ("khôn", "okela"), châm biếm, câu quá ngắn
- 📸 **Chụp (tuỳ chọn):** vài dòng ở bảng thứ ba **ô 6** (21 câu unknown)

## Slide 10 — Kết luận và hướng phát triển
- Từ **20 câu gán tay**, self-training gán thêm **159 câu**, đúng **61%** trên câu có cảm xúc
- Hạn chế: ít nhãn ban đầu, lỗi tự khuếch đại (lệch về neg), chỉ 2 nhãn, tiền xử lý đơn giản, khó nhận châm biếm
- Hướng phát triển:
  - Thêm nhãn trung tính, gán tay nhiều câu hơn
  - Mỗi vòng nhận số câu pos/neg bằng nhau hoặc tăng ngưỡng lên 0.99
  - Tách từ tiếng Việt, chuẩn hoá teencode
  - Thử MaxEnt, SVM (slide S20) làm bộ phân loại nền

---

## Câu hỏi có thể gặp
| Câu hỏi | Trả lời ngắn |
|---|---|
| Đề yêu cầu semi-supervised, sao lại dùng Naive Bayes? | Semi-supervised là cách học; mỗi vòng cần một bộ phân loại để đoán nhãn. Naive Bayes là bộ phân loại trong bài giảng (S20, Lab 06) |
| Vì sao ngưỡng 0.9? | Chỉ nhận câu mô hình rất chắc chắn để hạn chế nhãn sai đi vào tập học; thấp hơn thì lỗi lan nhanh hơn |
| Vì sao bỏ đặc trưng `False` của Lab 06? | Dữ liệu quá ít (20 câu, 1385 từ): các `False` lấn át từ có nghĩa, mô hình tự tin 100% nhưng sai |
| Vì sao không dùng pyvi/underthesea? | Bám sát công cụ trong bài giảng (regex, NLTK); đánh đổi là từ ghép bị tách đôi |
| Đánh giá kiểu gì khi không có nhãn chuẩn? | Đọc và chấm tay toàn bộ 159 câu máy gán theo quy tắc đúng/sai/trung tính; kết quả chấm không đưa ngược vào huấn luyện |
| Sao kết quả lệch về neg? | Lỗi tự khuếch đại: sau vòng 1 tập học nghiêng về neg, mô hình học lại càng nghiêng thêm |
