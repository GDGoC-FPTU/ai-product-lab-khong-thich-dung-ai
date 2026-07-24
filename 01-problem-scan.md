# 01 — Problem Scan (Cá nhân)

**Họ và tên:** Nguyễn Khắc Huy
**MSSV:** 23001525

---

# 🔍 Phase 1 — SCAN

Quét qua hoạt động vận hành của các công ty thành viên Vingroup bằng **4 Lenses**: Lặp lại (Repetitive), Tốn thời gian (Time-consuming), AI-upgrade, Pain từ người khác (Stakeholder Pain).

| # | Subsidiary | Lens | Mô tả ngắn bài toán |
|---|------------|------|----------------------|
| 1 | Xanh SM | Lặp lại | So khớp và phân bổ lại cuốc xe khi khách hàng yêu cầu đổi điểm đến giữa chừng, điều phối viên phải xử lý thủ công từng trường hợp. |
| 2 | VinFast | Tốn thời gian | Khách hàng mô tả sự cố xe bằng tiếng Việt tự nhiên (VD: "xe qua gờ giảm tốc kêu cụp cụp ở bánh trước"), nhân viên tổng đài phải tự phân loại mã lỗi kỹ thuật ban đầu trước khi chuyển kỹ thuật viên. |
| 3 | Vinhomes | AI-upgrade | Phản ánh của cư dân gửi qua App Vinhomes Resident (mất nước, hỏng đèn, ồn ào...) hiện được phân loại và điều hướng thủ công đến từng ban quản lý tòa nhà, phản hồi chậm và rập khuôn. |
| 4 | Vinmec | Pain từ người khác | Bác sĩ phải tự tay soạn tóm tắt hồ sơ xuất viện từ bệnh án điện tử, xét nghiệm và ghi chú lâm sàng, mất 20-30 phút/bệnh nhân, gây quá tải và phàn nàn từ chính bác sĩ. |
| 5 | Vinpearl | Tốn thời gian | Nhân viên phải tự đọc thủ công hàng loạt review trên Booking.com, Agoda, Google Map để lọc ra các phàn nàn khẩn cấp (phòng bẩn, thái độ nhân viên...) rồi mới báo cho Manager. |

---

# 🃏 Phase 2 — QUICK-ASSESS

Chọn top 3 từ danh sách SCAN: **#2 (VinFast chẩn đoán lỗi xe), #3 (Vinhomes phân loại phản ánh cư dân), #5 (Vinpearl lọc review khẩn cấp).** Ba bài toán này được ưu tiên vì đều là tác vụ phân loại/tóm tắt văn bản tiếng Việt phù hợp LLM Feature, có metric đo được rõ ràng, và rủi ro vận hành thấp hơn so với #1 (điều vận real-time ảnh hưởng an toàn giao thông) và #4 (dữ liệu y tế nhạy cảm tại Vinmec).

## Quick Problem Card #1 — VinFast: Chẩn đoán sơ bộ lỗi xe từ mô tả tiếng Việt

```text
┌─────────────────────────────────────────────────────────────┐
│ QUICK PROBLEM CARD #1                                       │
│                                                             │
│ Bài toán: Phân loại mã lỗi kỹ thuật ban đầu từ mô tả tự     │
│ nhiên bằng tiếng Việt của khách hàng qua tổng đài CSKH.     │
│ Công ty thành viên: [x] VinFast                             │
│                                                             │
│ Ai đang đau? Nhân viên tổng đài CSKH (tra cứu thủ công),    │
│ khách hàng (chờ lâu mới được điều kỹ thuật viên đúng chuyên) │
│                                                             │
│ Workflow thủ công hiện tại (4 bước):                         │
│   1. Khách gọi mô tả lỗi bằng lời tự nhiên                  │
│   → 2. Nhân viên tổng đài ghi chú lại mô tả                 │
│   → 3. Tra cứu thủ công bảng mã lỗi kỹ thuật nội bộ          │
│   → 4. Gán mã lỗi sơ bộ, chuyển phiếu cho kỹ thuật viên      │
│                                                             │
│ Bước nào tốn nhất? Bước 3 (⏱ 8 phút/lượt, dễ gán sai)       │
│ AI có thể nhảy vào hỗ trợ ở bước nào? Bước 3-4               │
│ (Tự động phân loại nhóm mã lỗi từ mô tả tiếng Việt)          │
│                                                             │
│ Đo thành công bằng gì (Metric có số)?                        │
│ Giảm thời gian gán mã lỗi từ 8 phút ──> dưới 1 phút;         │
│ độ chính xác gán đúng nhóm lỗi đạt ≥ 90%.                    │
│                                                             │
│ Quick Architecture: [x] LLM Feature                          │
└─────────────────────────────────────────────────────────────┘
```

## Quick Problem Card #2 — Vinhomes: Phân loại & điều hướng phản ánh cư dân

```text
┌─────────────────────────────────────────────────────────────┐
│ QUICK PROBLEM CARD #2                                       │
│                                                             │
│ Bài toán: Phân loại loại sự cố và điều hướng phản ánh cư dân │
│ gửi qua App Vinhomes Resident đến đúng ban quản lý phụ trách.│
│ Công ty thành viên: [x] Vinhomes                             │
│                                                             │
│ Ai đang đau? Nhân viên tổng đài/lễ tân Ban Quản lý tòa nhà,  │
│ cư dân (chờ phản hồi lâu, bị chuyển nhầm ban phụ trách)      │
│                                                             │
│ Workflow thủ công hiện tại (4 bước):                         │
│   1. Cư dân gửi phản ánh qua App                             │
│   → 2. Nhân viên đọc, phân loại thủ công loại sự cố          │
│   → 3. Tra cứu đúng ban/đội phụ trách theo tòa/tầng          │
│   → 4. Chuyển phiếu và theo dõi phản hồi                     │
│                                                             │
│ Bước nào tốn nhất? Bước 2-3 (⏱ 10 phút/lượt, cao điểm dồn    │
│ ứ hàng trăm phản ánh/ngày)                                   │
│ AI có thể nhảy vào hỗ trợ ở bước nào? Bước 2-3                │
│ (Tự động phân loại loại sự cố + gợi ý đúng ban phụ trách)     │
│                                                             │
│ Đo thành công bằng gì (Metric có số)?                        │
│ Giảm thời gian phân loại + điều hướng từ 10 phút ──> dưới    │
│ 2 phút; tỉ lệ điều hướng đúng ban phụ trách ngay lần đầu     │
│ đạt ≥ 95%.                                                   │
│                                                             │
│ Quick Architecture: [x] LLM Feature (kèm Rule routing table) │
└─────────────────────────────────────────────────────────────┘
```

## Quick Problem Card #3 — Vinpearl: Lọc review khẩn cấp cần xử lý gấp

```text
┌─────────────────────────────────────────────────────────────┐
│ QUICK PROBLEM CARD #3                                       │
│                                                             │
│ Bài toán: Quét và gắn cờ các review khẩn cấp (phòng bẩn,     │
│ thái độ nhân viên tệ...) trên Booking/Agoda/Google Map.      │
│ Công ty thành viên: [x] Vinpearl                             │
│                                                             │
│ Ai đang đau? Nhân viên CSKH/Duty Manager khách sạn           │
│ (đọc thủ công, dễ bỏ sót phàn nàn nghiêm trọng)               │
│                                                             │
│ Workflow thủ công hiện tại (4 bước):                         │
│   1. Nhân viên vào từng nền tảng review                      │
│   → 2. Đọc lần lượt các review mới                           │
│   → 3. Đánh giá thủ công mức độ khẩn cấp                     │
│   → 4. Soạn báo cáo gửi Manager                              │
│                                                             │
│ Bước nào tốn nhất? Bước 2-3 (⏱ 45 phút/ngày, dễ bỏ sót)      │
│ AI có thể nhảy vào hỗ trợ ở bước nào? Bước 2-3                │
│ (Tự động quét và gắn cờ mức độ khẩn cấp)                     │
│                                                             │
│ Đo thành công bằng gì (Metric có số)?                        │
│ Giảm thời gian rà soát review từ 45 phút ──> dưới 10 phút/   │
│ ngày; recall phát hiện đúng phàn nàn khẩn cấp ≥ 95%.         │
│                                                             │
│ Quick Architecture: [x] LLM Feature                          │
└─────────────────────────────────────────────────────────────┘
```
