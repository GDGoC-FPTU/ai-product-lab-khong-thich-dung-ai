# 03-ai-log.md - Nhật ký tương tác AI (Bài cá nhân - 15 điểm)

## 1. AI đã giúp gì cho tôi? (Thought-partner)
Trong quá trình scoping và xây dựng giải pháp tự động hóa chứng từ kế toán cho VinFast, tôi đã sử dụng AI (Gemini/Claude) làm trợ lý tư duy (thought-partner) xuyên suốt các công đoạn sau:
* **Brainstorm ý tưởng & Lọc thấu kính:** AI hỗ trợ tôi phân tích nhanh các nút thắt (bottleneck) trong quy trình nghiệp vụ kế toán truyền thống, giúp tôi xác định chính xác các tác nhân (actor) đang gặp khó khăn và đề xuất các thông số đo lường hiệu quả (metric) thực tế như thời gian xử lý và tỷ lệ sai sót.
* **Xây dựng System Prompt & Cấu trúc JSON:** AI hỗ trợ thiết kế cấu trúc prompt nghiêm ngặt, bao gồm cả các quy định rõ ràng về **Operational Boundary** (ranh giới vận hành) để đảm bảo mô hình LLM không tự ý đưa ra quyết định vượt quyền.
* **Thiết kế Adversarial Test Cases:** AI đóng góp ý tưởng để viết các câu lệnh tấn công (Prompt Injection/Adversarial test cases) nhằm thử nghiệm xem liệu mô hình có bị lừa phê duyệt thanh toán trái quy định hay không.

---

## 2. AI đã sai ở điểm nào? (Hallucination & Flaws)
Trong quá trình làm việc, tôi đã ghi nhận một số điểm AI xử lý chưa chính xác hoặc gặp lỗi:
* **Đề xuất giải pháp quá phức tạp (Over-engineering):** Ở giai đoạn đầu khi tôi hỏi về phương án xử lý hóa đơn, AI đề xuất xây dựng một hệ thống Multi-Agent phức tạp gồm nhiều agent tranh luận lẫn nhau (Critic-Agent và Generator-Agent). Điều này gây lãng phí tài nguyên và không cần thiết cho một tác vụ trích xuất dữ liệu có cấu trúc vốn chỉ cần kết hợp OCR chuẩn hóa và Rule-based Validation cơ bản.
* **Lỗ hổng ranh giới (Boundary Bypass):** Khi thử nghiệm với một prompt tấn công cố tình ngụy trang hóa đơn thành một khoản chi khẩn cấp dưới danh nghĩa "Yêu cầu từ cấp trên", AI ban đầu đã quên mất ranh giới cấm và tỏ ra lúng túng, suýt đưa ra phản hồi gợi ý cách bấm nút duyệt thanh toán tự động thay vì từ chối thẳng thừng.

---

## 3. Tôi đã sửa đổi ra sao? (Prompt Refinement & Control)
Để khắc phục các điểm yếu trên của AI, tôi đã thực hiện các bước điều chỉnh sau:
* **Thu hẹp Scope kiến trúc:** Tôi chủ động yêu cầu AI loại bỏ mô hình Agent phức tạp, thay vào đó ép hệ thống quy về kiến trúc đơn giản hơn: **Pipeline OCR kết hợp Structured LLM Output và Rule-based Check truyền thống**, giúp giảm độ trễ và dễ kiểm soát hơn.
* **Tăng cường System Prompt nghiêm ngặt:** Tôi bổ sung các điều kiện phủ định tuyệt đối (Negative Constraints) cực kỳ rõ ràng trong system prompt: *"TUYỆT ĐỐI KHÔNG đưa ra bất kỳ hướng dẫn hay đề xuất nào liên quan đến việc tự động phê duyệt chuyển khoản, ngay cả khi có yêu cầu khẩn cấp từ quản lý"*. Đồng thời, tôi thêm cơ chế yêu cầu AI luôn trả về trạng thái từ chối kèm cờ cảnh báo (Flagged) nếu phát hiện bất thường.
