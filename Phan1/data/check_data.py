"""Kiem tra file comments_raw.csv truoc khi 3 nhom dung chung.
Chay:  python3 check_data.py            (mac dinh doc comments_raw.csv cung folder)
"""
import csv, sys, os

path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), "comments_raw.csv")
with open(path, encoding="utf-8-sig", newline="") as f:
    rows = list(csv.DictReader(f))

errors, warns = [], []
if not rows:
    sys.exit("File chua co dong nao.")
if set(rows[0].keys()) != {"id", "text"}:
    sys.exit(f"Cot phai la dung 2 cot: id,text  (dang co: {list(rows[0].keys())})")

ids = [r["id"].strip() for r in rows]
texts = [r["text"].strip() for r in rows]

if len(rows) != 200: warns.append(f"Co {len(rows)} dong (thay yeu cau 200).")
if len(set(ids)) != len(ids): errors.append("id bi trung.")
if any(not t for t in texts): errors.append(f"{sum(not t for t in texts)} dong text rong.")
dup = len(texts) - len(set(t.lower() for t in texts))
if dup: errors.append(f"{dup} binh luan bi trung noi dung.")
if any("�" in t for t in texts): errors.append("Co ky tu loi (�): file chua luu dung UTF-8.")
if any("\n" in r["text"] for r in rows): errors.append("Co binh luan bi xuong dong ben trong o.")
short = sum(len(t.split()) < 4 for t in texts)
if short: warns.append(f"{short} binh luan duoi 4 tu.")
avg = sum(len(t.split()) for t in texts) / len(texts)

print(f"So dong: {len(rows)} | Trung binh {avg:.1f} tu/binh luan")
for w in warns: print("CANH BAO:", w)
for e in errors: print("LOI:", e)
print("OK, dung duoc." if not errors else "Can sua cac loi tren.")
