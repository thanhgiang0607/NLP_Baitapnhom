# Nguồn dữ liệu

Toàn bộ câu trong `khdl_corpus.txt` được trích nguyên văn từ **Wikipedia tiếng Việt** (giấy phép CC BY-SA 4.0), tải qua MediaWiki API ngày 2026-11-09 bằng `scripts/fetch_wikipedia.py`. Văn bản gốc lưu trong `sources/*.json`, danh sách câu được chọn lưu trong `selection.json`. Tiêu chí chọn: liên quan KHDL/AI, chứa thực thể (người, tổ chức, thuật toán, công cụ, bộ dữ liệu, độ đo).

Tổng: **97 câu** từ **21 bài viết**.

| Bài viết | Số câu | URL | Phiên bản (revid) |
|---|---|---|---|
| ChatGPT | 7 | https://vi.wikipedia.org/wiki/ChatGPT | [75669985](https://vi.wikipedia.org/w/index.php?oldid=75669985) (2026-10-26) |
| Dữ liệu lớn | 2 | https://vi.wikipedia.org/wiki/D%E1%BB%AF_li%E1%BB%87u_l%E1%BB%9Bn | [74519169](https://vi.wikipedia.org/w/index.php?oldid=74519169) (2025-11-25) |
| Geoffrey Hinton | 3 | https://vi.wikipedia.org/wiki/Geoffrey_Hinton | [75615048](https://vi.wikipedia.org/w/index.php?oldid=75615048) (2026-10-05) |
| Học máy | 13 | https://vi.wikipedia.org/wiki/H%E1%BB%8Dc_m%C3%A1y | [75614728](https://vi.wikipedia.org/w/index.php?oldid=75614728) (2026-10-05) |
| Học sâu | 13 | https://vi.wikipedia.org/wiki/H%E1%BB%8Dc_s%C3%A2u | [75355135](https://vi.wikipedia.org/w/index.php?oldid=75355135) (2026-07-25) |
| Máy vectơ hỗ trợ | 2 | https://vi.wikipedia.org/wiki/M%C3%A1y_vect%C6%A1_h%E1%BB%97_tr%E1%BB%A3 | [75631914](https://vi.wikipedia.org/w/index.php?oldid=75631914) (2026-10-11) |
| Mạng thần kinh tích chập | 4 | https://vi.wikipedia.org/wiki/M%E1%BA%A1ng_th%E1%BA%A7n_kinh_t%C3%ADch_ch%E1%BA%ADp | [75642669](https://vi.wikipedia.org/w/index.php?oldid=75642669) (2026-10-15) |
| Phân cụm k-means | 2 | https://vi.wikipedia.org/wiki/Ph%C3%A2n_c%E1%BB%A5m_k-means | [68153949](https://vi.wikipedia.org/w/index.php?oldid=68153949) (2022-02-14) |
| PyTorch | 8 | https://vi.wikipedia.org/wiki/PyTorch | [75115604](https://vi.wikipedia.org/w/index.php?oldid=75115604) (2026-05-27) |
| Python (ngôn ngữ lập trình) | 5 | https://vi.wikipedia.org/wiki/Python_%28ng%C3%B4n_ng%E1%BB%AF_l%E1%BA%ADp_tr%C3%ACnh%29 | [75702061](https://vi.wikipedia.org/w/index.php?oldid=75702061) (2026-11-07) |
| TensorFlow | 5 | https://vi.wikipedia.org/wiki/TensorFlow | [73708853](https://vi.wikipedia.org/w/index.php?oldid=73708853) (2025-07-25) |
| Xử lý ngôn ngữ tự nhiên | 1 | https://vi.wikipedia.org/wiki/X%E1%BB%AD_l%C3%BD_ng%C3%B4n_ng%E1%BB%AF_t%E1%BB%B1_nhi%C3%AAn | [74511609](https://vi.wikipedia.org/w/index.php?oldid=74511609) (2025-11-23) |
| Phát hiện bất thường | 6 | https://vi.wikipedia.org/wiki/Ph%C3%A1t_hi%E1%BB%87n_b%E1%BA%A5t_th%C6%B0%E1%BB%9Dng | [75640064](https://vi.wikipedia.org/w/index.php?oldid=75640064) (2026-10-14) |
| Phân loại đa lớp | 1 | https://vi.wikipedia.org/wiki/Ph%C3%A2n_lo%E1%BA%A1i_%C4%91a_l%E1%BB%9Bp | [75422916](https://vi.wikipedia.org/w/index.php?oldid=75422916) (2026-08-11) |
| Phân loại ảnh | 9 | https://vi.wikipedia.org/wiki/Ph%C3%A2n_lo%E1%BA%A1i_%E1%BA%A3nh | [75631094](https://vi.wikipedia.org/w/index.php?oldid=75631094) (2026-10-10) |
| Nhận dạng vật thể | 8 | https://vi.wikipedia.org/wiki/Nh%E1%BA%ADn_d%E1%BA%A1ng_v%E1%BA%ADt_th%E1%BB%83 | [75631095](https://vi.wikipedia.org/w/index.php?oldid=75631095) (2026-10-10) |
| Sai số toàn phương trung bình | 2 | https://vi.wikipedia.org/wiki/Sai_s%E1%BB%91_to%C3%A0n_ph%C6%B0%C6%A1ng_trung_b%C3%ACnh | [75238746](https://vi.wikipedia.org/w/index.php?oldid=75238746) (2026-06-27) |
| Entropy chéo | 2 | https://vi.wikipedia.org/wiki/Entropy_ch%C3%A9o | [75570148](https://vi.wikipedia.org/w/index.php?oldid=75570148) (2026-09-20) |
| U-Net | 1 | https://vi.wikipedia.org/wiki/U-Net | [75631932](https://vi.wikipedia.org/w/index.php?oldid=75631932) (2026-10-11) |
| Mô hình ngôn ngữ lớn | 2 | https://vi.wikipedia.org/wiki/M%C3%B4_h%C3%ACnh_ng%C3%B4n_ng%E1%BB%AF_l%E1%BB%9Bn | [75678113](https://vi.wikipedia.org/w/index.php?oldid=75678113) (2026-10-29) |
| Dịch tự động | 1 | https://vi.wikipedia.org/wiki/D%E1%BB%8Bch_t%E1%BB%B1_%C4%91%E1%BB%99ng | [75590145](https://vi.wikipedia.org/w/index.php?oldid=75590145) (2026-09-26) |
