# Phase 1 — SCAN: Tìm kiếm cơ hội (Cá nhân)

Dưới đây là danh sách 5 bài toán tiềm năng thuộc các công ty thành viên Vingroup, được quét theo 4 lens.

| #   | Subsidiary   | Lens             | Mô tả ngắn bài toán                                                                                                       |
| --- | ------------ | ---------------- | ------------------------------------------------------------------------------------------------------------------------- |
| 1   | **Xanh SM**  | Lặp lại          | Điều phối viên phải xác định lại lộ trình và ưu tiên cuốc xe khi khách hàng thay đổi điểm đến hoặc hủy chuyến giữa chừng. |
| 2   | **Xanh SM**  | Tốn thời gian    | Tài xế báo sự cố hết pin hoặc chậm sạc, đội điều vận phải tra cứu vị trí, trạm sạc, và soạn tin nhắn chỉ dẫn thủ công.    |
| 3   | **VinFast**  | AI-upgrade       | Nhân viên hỗ trợ khách hàng phải soạn thư trả lời và xử lý nhiều yêu cầu lặp lại về pin, bảo dưỡng, và lịch hẹn trạm sạc. |
| 4   | **Vinhomes** | Stakeholder Pain | Cư dân gửi phản ánh qua ứng dụng, đội CSKH phải phân loại, tóm tắt và trả lời thủ công, làm chậm SLA.                     |
| 5   | **Vinmec**   | Tốn thời gian    | Bác sĩ/nhân viên y tế mất thời gian tóm tắt hồ sơ bệnh án hoặc ghi chú hậu xét, ảnh hưởng đến khung giờ khám bệnh.        |

---

# Phase 2 — QUICK-ASSESS: 3 Quick Problem Cards

## Quick Problem Card #1 — Xanh SM: Xử lý sự cố hết pin thực địa

```text
┌─────────────────────────────────────────────────────────────┐
│ QUICK PROBLEM CARD #1                                       │
│                                                             │
│ Bài toán: Tài xế Xanh SM báo sự cố pin hoặc hết pin giữa   │
│ đường cần được hỗ trợ nhanh.                                │
│ Công ty thành viên: [x] Xanh SM (GSM)                       │
│                                                             │
│ Ai đang đau? Tài xế (chờ đợi) và điều phối viên (quá tải)  │
│                                                             │
│ Workflow thủ công hiện tại (5 bước):                        │
│ 1. Tài xế gọi tổng đài báo sự cố pin                         │
│ 2. Điều phối viên tra cứu vị trí GPS xe                     │
│ 3. Tra cứu trạm sạc VinFast còn trụ trống gần nhất         │
│ 4. Soạn tin nhắn chỉ đường gửi tài xế                       │
│ 5. Nếu cần, gọi xe cứu hộ hoặc hỗ trợ pin di động           │
│                                                             │
│ Bước nào tốn thời gian/lỗi nhất? Bước 3-4 (≈ 12 phút/lượt) │
│ AI có thể nhảy vào hỗ trợ ở bước nào? Bước 3-4              │
│                                                             │
│ Đo thành công bằng gì (Metric có số)?                       │
│ Giảm thời gian xử lý sự cố từ 15 phút xuống dưới 3 phút.   │
│                                                             │
│ Quick Architecture: [ ] No AI  [ ] Rule  [x] LLM  [ ] Agent│
└─────────────────────────────────────────────────────────────┘
```

## Quick Problem Card #2 — Vinhomes: Phân loại phản hồi cư dân

```text
┌─────────────────────────────────────────────────────────────┐
│ QUICK PROBLEM CARD #2                                       │
│                                                             │
│ Bài toán: CSKH Vinhomes phải phân loại, tóm tắt và trả lời   │
│ các phản ánh của cư dân nhanh chóng.                        │
│ Công ty thành viên: [x] Vinhomes                            │
│                                                             │
│ Ai đang đau? Nhân viên CSKH và cư dân                      │
│                                                             │
│ Workflow thủ công hiện tại (4 bước):                        │
│ 1. Nhận phản ánh qua app hoặc hotline                       │
│ 2. Đọc và phân loại chủ đề phản ánh                         │
│ 3. Viết phản hồi chuẩn hóa dựa trên template                │
│ 4. Chuyển cho bộ phận liên quan nếu cần                     │
│                                                             │
│ Bước nào tốn thời gian/lỗi nhất? Bước 2-3 (≈ 10 phút/lượt) │
│ AI có thể nhảy vào hỗ trợ ở bước nào? Bước 2-3              │
│                                                             │
│ Đo thành công bằng gì (Metric có số)?                       │
│ Giảm thời gian phản hồi trung bình từ 12 phút xuống dưới 3 phút. │
│                                                             │
│ Quick Architecture: [ ] No AI  [x] Rule  [ ] LLM  [ ] Agent│
└─────────────────────────────────────────────────────────────┘
```

## Quick Problem Card #3 — Vinmec: Tóm tắt hồ sơ bệnh án

```text
┌─────────────────────────────────────────────────────────────┐
│ QUICK PROBLEM CARD #3                                       │
│                                                             │
│ Bài toán: Bác sĩ mất thời gian tóm tắt hồ sơ bệnh án và    │
│ ghi chú xuất viện.                                          │
│ Công ty thành viên: [x] Vinmec                              │
│                                                             │
│ Ai đang đau? Bác sĩ và nhân viên thực hành y tế             │
│                                                             │
│ Workflow thủ công hiện tại (4 bước):                        │
│ 1. Đọc lịch sử bệnh án                                      │
│ 2. Chọn thông tin cần giữ lại                               │
│ 3. Viết tóm tắt cho hồ sơ xuất viện                         │
│ 4. Gửi cho bộ phận phụ trách                                │
│                                                             │
│ Bước nào tốn thời gian/lỗi nhất? Bước 2-3 (≈ 20 phút/bệnh nhân) │
│ AI có thể nhảy vào hỗ trợ ở bước nào? Bước 2-3              │
│                                                             │
│ Đo thành công bằng gì (Metric có số)?                       │
│ Giảm thời gian tóm tắt từ 20 phút xuống còn dưới 5 phút. │
│                                                             │
│ Quick Architecture: [ ] No AI  [ ] Rule  [x] LLM  [ ] Agent│
└─────────────────────────────────────────────────────────────┘
```
