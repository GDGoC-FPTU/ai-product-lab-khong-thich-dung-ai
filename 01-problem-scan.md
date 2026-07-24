# 01 — Problem Scan (Phase 1 & 2)

## Phase 1 — SCAN: 5 bài toán

| # | Subsidiary | Lens | Mô tả ngắn bài toán |
|---|---|---|---|
| 1 | Xanh SM (GSM) | Stakeholder Pain | Khi tài xế báo pin nguy cấp (<5%), điều phối viên phải tự tra danh sách trạm sạc trên hệ thống riêng, tính khoảng cách bằng tay rồi mới quyết định gợi ý trạm hay gọi xe sạc di động — dễ trễ và dễ gợi ý sai trạm quá xa. |
| 2 | VinFast | Time-consuming | Nhân viên CSKH phải đọc và soạn tay từng phản hồi cho khiếu nại về pin chai/degradation, mỗi ca mất 8-10 phút vì phải tra cứu lịch sử bảo hành trước khi trả lời. |
| 3 | Vinhomes | AI-upgrade | Phản hồi đánh giá 1-star của cư dân trên app quản lý tòa nhà hiện dùng mẫu câu cứng nhắc, không cá nhân hóa theo từng khiếu nại (tiếng ồn, thang máy, phí dịch vụ...). |
| 4 | Vinmec | Repetitive | Bác sĩ chẩn đoán hình ảnh phải đối chiếu thủ công phim X-quang ngực với lịch sử bệnh án cũ của bệnh nhân trước khi kết luận, lặp lại với hàng chục ca/ngày. |
| 5 | Vinpearl / VinWonders | AI-upgrade | Chatbot CSKH đặt vé hiện tại chỉ trả lời được kịch bản cố định (giờ mở cửa, giá vé); các câu hỏi phức tạp hơn (đổi lịch, combo, hoàn tiền) đều bị đẩy qua tổng đài, gây quá tải nhân viên trực.

---

## Phase 2 — QUICK-ASSESS: 3 Quick Problem Cards

### QUICK PROBLEM CARD #1 (⭐ Chọn để Deep-Dive ở Phase 3)
- **Bài toán:** Điều phối viên Xanh SM phản hồi chậm/sai khi tài xế báo pin nguy cấp.
- **Công ty thành viên:** [x] Xanh SM
- **Ai đang đau (Actor):** Điều phối viên tổng đài (dispatcher) và tài xế xe điện.
- **Workflow thủ công hiện tại:**
  1. Tài xế gọi/nhắn báo pin thấp → 2. Điều phối tra hệ thống trạm sạc riêng → 3. Điều phối tính tay khoảng cách & quyết định (trạm hay xe sạc di động) → 4. Soạn & gửi tin nhắn cho tài xế.
- **Bước tốn thời gian/lỗi nhất:** Bước 2-3 (tra cứu + quyết định thủ công) — **⏱ ~5-8 phút/lượt**.
- **AI có thể hỗ trợ ở bước nào:** Bước 2-3 — AI đọc input, áp rule pin <5%, soạn draft gợi ý/lệnh điều xe sạc di động.
- **Metric thành công:** Giảm thời gian phản hồi case pin nguy cấp từ ~15 phút → dưới 3 phút; 100% case pin <5% không được gợi ý trạm >5km.
- **Quick Architecture:** [x] LLM (kết hợp Rule cứng cho ngưỡng pin)

### QUICK PROBLEM CARD #2
- **Bài toán:** Nhân viên CSKH VinFast tốn thời gian soạn phản hồi khiếu nại pin chai.
- **Công ty thành viên:** [x] VinFast
- **Ai đang đau (Actor):** Nhân viên CSKH tuyến 1.
- **Workflow thủ công hiện tại:**
  1. Nhận khiếu nại qua app → 2. Tra lịch sử bảo hành/số lần sạc → 3. Soạn phản hồi tay → 4. Gửi & chờ khách phản hồi lại.
- **Bước tốn thời gian/lỗi nhất:** Bước 2-3 — **⏱ ~8-10 phút/lượt**.
- **AI có thể hỗ trợ ở bước nào:** Bước 3 — AI soạn draft phản hồi dựa trên dữ liệu tra cứu sẵn có.
- **Metric thành công:** Giảm thời gian soạn phản hồi từ 10 phút → dưới 2 phút.
- **Quick Architecture:** [x] LLM

### QUICK PROBLEM CARD #3
- **Bài toán:** Phản hồi đánh giá 1-star cư dân Vinhomes rập khuôn, không cá nhân hóa.
- **Công ty thành viên:** [x] Vinhomes
- **Ai đang đau (Actor):** Nhân viên quản lý tòa nhà (Building Management).
- **Workflow thủ công hiện tại:**
  1. Cư dân đăng đánh giá 1-star → 2. Nhân viên đọc & phân loại vấn đề → 3. Chọn mẫu câu trả lời có sẵn → 4. Chỉnh sửa tay & đăng phản hồi.
- **Bước tốn thời gian/lỗi nhất:** Bước 3-4 — mẫu câu không khớp vấn đề thực tế, phải viết lại — **⏱ ~6-8 phút/lượt**.
- **AI có thể hỗ trợ ở bước nào:** Bước 3 — AI soạn phản hồi cá nhân hóa theo nội dung đánh giá.
- **Metric thành công:** Giảm thời gian xử lý 1 đánh giá từ 8 phút → dưới 2 phút; giữ điểm hài lòng phản hồi ≥ mức hiện tại.
- **Quick Architecture:** [x] LLM
