# 03 — AI Log & Reflection (Cá nhân)

## Nguyễn Khắc Huy — MSSV 23001525

**AI giúp gì:**
Trong buổi lab, mình dùng Claude (Claude Code) làm thought-partner xuyên suốt: thiết lập lại môi trường `.venv` đúng phiên bản Python yêu cầu, tạo branch Git riêng theo quy ước nhóm, brainstorm và cấu trúc lại 5 bài toán ở Phase 1 (SCAN) dựa trên gợi ý từ `03-inspiration-kit.md`, viết 3 Quick Problem Card ở Phase 2 đúng format rubric, và soạn thảo `02-deep-dive-report.md` (Problem Statement 6-field, Future-State Flow, Fallback/HITL, Evaluate) cho bài toán nhóm chọn (Vinhomes — phân loại phản ánh cư dân). Vì thời gian buổi lab bị rút ngắn còn ~40 phút, AI giúp mình nén nhanh các bước lập kế hoạch phân công cho 6 người và tự động chạy `autograder.py` để kiểm tra tiến độ nộp bài theo thời gian thực.

**AI sai gì:**
Khi mình yêu cầu tạo file `01-problem-scan.md`, AI đã tự động điền MSSV là "23001525" dựa trên suy đoán từ địa chỉ email của mình (`23001525@hus.edu.vn`) mà không hỏi lại để xác nhận — đây là một dạng giả định (assumption) có thể sai nếu email không phải MSSV thật. May mắn là suy đoán đúng, nhưng đây vẫn là hành vi rủi ro: AI không nên tự ý điền thông tin định danh cá nhân vào tài liệu chính thức chỉ dựa trên suy luận gián tiếp. Ngoài ra, khi mình yêu cầu lưu "mã học viên" vào bộ nhớ, AI ban đầu có xu hướng dễ nhầm lẫn giữa "mã học viên chương trình AI thực chiến" và "MSSV trường đại học" nếu không được nhắc rõ — hai mã số khác nhau nhưng dễ bị gộp chung nếu không có ngữ cảnh phân biệt.

**Sửa đổi ra sao:**
Mình yêu cầu AI ghi rõ trong bộ nhớ cục bộ ranh giới phân biệt giữa hai loại mã số (mã học viên AI thực chiến dùng cho các dự án trong `D:\project\Lab_AI20k_2026`, còn MSSV trường dùng riêng cho bài nộp học thuật như Lab 02 này), để tránh AI dùng nhầm mã trong các lần làm việc sau. Đây là bài học về việc luôn phải chỉ rõ ranh giới ngữ cảnh (Operational Boundary) khi giao cho AI xử lý thông tin định danh — giống hệt nguyên tắc mà cả nhóm đang áp dụng cho chính bài toán AI đang Deep-Dive (không để AI tự suy diễn/quyết định thay con người ở những điểm nhạy cảm).
