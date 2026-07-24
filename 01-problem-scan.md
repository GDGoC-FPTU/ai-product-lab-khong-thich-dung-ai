# 01 — Problem Scan & Quick Problem Cards

> **Deliverable cá nhân — Phase 1 (SCAN) & Phase 2 (QUICK-ASSESS)**
> Đây là bài làm cá nhân, thể hiện tư duy tìm kiếm bài toán trước khi thảo luận nhóm.

---

## 🔍 Phase 1 — SCAN: Bảng Quét Cơ Hội

Sử dụng **4 Lenses** để quét qua hoạt động vận hành của các công ty thành viên Vingroup.

| # | Subsidiary (VinFast/Xanh SM...) | Lens | Mô tả ngắn bài toán |
|---|----------------------------------|------|----------------------|
| 1 | **Vinmec** | Tốn thời gian | Bác sĩ mất 20–30 phút/bệnh nhân để soạn thủ công bản tóm tắt xuất viện (Discharge Summary) từ bệnh án điện tử — tác vụ lặp lại có cấu trúc cố định mà LLM có thể draft tự động. |
| 2 | **Xanh SM** | Lặp lại | Điều phối viên tra cứu thủ công trạm sạc VinFast trống và soạn tin hướng dẫn tài xế khi xảy ra sự cố hết pin thực địa — mất 12–15 phút/lượt, xảy ra ~80 lần/ngày tại Hà Nội. |
| 3 | **Vinhomes** | Lặp lại | Nhân viên CSKH phân loại thủ công hàng trăm khiếu nại (mất nước, hỏng đèn, ồn ào) từ App Vinhomes Resident và route đến đúng ban quản lý tòa nhà — mất 12 giờ/phản hồi. |
| 4 | **VinFast** | AI-upgrade | Khách hàng mô tả triệu chứng lỗi xe bằng tiếng Việt thông thường (VD: *"xe kêu cụp cụp ở bánh trước khi qua gờ giảm tốc"*), nhân viên kỹ thuật phải dịch thủ công sang mã lỗi kỹ thuật (DTC) — tốn 15–20 phút/vé. |
| 5 | **Vinpearl** | Pain từ người khác | Quản lý khách sạn phải đọc thủ công hàng trăm review trên Booking.com, Agoda, Google Maps để lọc phàn nàn khẩn cấp — gây chậm trễ xử lý, khách không quay lại. |
| 6 | **Vinmec** | Pain từ người khác | Bệnh nhân chờ trung bình 45 phút để đặt lịch đúng chuyên khoa vì hệ thống chatbot hiện tại không phân loại đúng triệu chứng — bác sĩ phàn nàn về ca tái khám sai chuyên khoa tăng 30%. |

---

## 🃏 Phase 2 — QUICK-ASSESS: 3 Quick Problem Cards

Chọn top 3 bài toán tiềm năng nhất: **#1 (Vinmec Discharge Summary)**, **#2 (Xanh SM Sự cố sạc)**, **#3 (Vinhomes Phân loại khiếu nại)**.

---

### QUICK PROBLEM CARD #1

```
┌─────────────────────────────────────────────────────────────┐
│ QUICK PROBLEM CARD #1                                       │
│                                                             │
│ Bài toán: Tự động soạn thảo Tóm tắt Hồ sơ Xuất viện        │
│           (Discharge Summary) cho bệnh nhân Vinmec.         │
│ Công ty thành viên: [x] Vinmec                              │
│                                                             │
│ Ai đang đau (Actor)?                                        │
│   Bác sĩ điều trị (Attending Physician) phụ trách xuất      │
│   viện bệnh nhân — đang bị quá tải hành chính sau ca mổ     │
│   hoặc cuối ca chiều.                                        │
│                                                             │
│ Workflow thủ công hiện tại (5 bước):                        │
│   1. Bác sĩ mở bệnh án điện tử (HIS – Hospital              │
│      Information System)                                    │
│   → 2. Đọc thủ công toàn bộ ghi chú điều trị, kết quả      │
│        xét nghiệm, kết quả chẩn đoán hình ảnh               │
│   → 3. Soạn thủ công bản tóm tắt (chẩn đoán, điều trị,      │
│        thuốc về nhà, lịch tái khám) trên Word/Form          │
│   → 4. In và ký tên, đóng dấu                               │
│   → 5. Điều dưỡng trao tài liệu cho bệnh nhân              │
│                                                             │
│ Bước nào tốn thời gian/lỗi nhất?                            │
│   Bước 2–3 (⏱ 20–25 phút/bệnh nhân)                        │
│   Lỗi phổ biến: bỏ sót thuốc tương tác, ghi sai liều dùng.  │
│                                                             │
│ AI có thể nhảy vào hỗ trợ ở bước nào?                       │
│   Bước 2–3: LLM đọc dữ liệu HIS (JSON/HL7) → Tự động       │
│   tổng hợp và draft bản tóm tắt → Bác sĩ review & ký.      │
│                                                             │
│ Đo thành công bằng gì (Metric có số)?                        │
│   Giảm thời gian soạn từ 25 phút ──→ dưới 5 phút.          │
│   Tỉ lệ bác sĩ duyệt draft mà không cần chỉnh sửa lớn ≥ 80%│
│                                                             │
│ Quick Architecture: [x] LLM Feature                         │
│   (Structured output từ bệnh án có cấu trúc JSON/HL7,       │
│    không cần Agent tự trị — rủi ro y tế phải có HITL)       │
└─────────────────────────────────────────────────────────────┘
```

---

### QUICK PROBLEM CARD #2

```
┌─────────────────────────────────────────────────────────────┐
│ QUICK PROBLEM CARD #2                                       │
│                                                             │
│ Bài toán: Tài xế Xanh SM báo cáo sự cố sạc pin / hết pin   │
│           giữa đường, cần điều phối trạm sạc hoặc cứu hộ.  │
│ Công ty thành viên: [x] Xanh SM (GSM)                      │
│                                                             │
│ Ai đang đau (Actor)?                                        │
│   Điều phối viên (Dispatcher) tại Trung tâm Điều vận        │
│   Xanh SM — đang chịu tải >80 sự cố/ngày vào giờ cao điểm. │
│                                                             │
│ Workflow thủ công hiện tại (5 bước):                        │
│   1. Tài xế gọi tổng đài báo hết pin                       │
│   → 2. Dispatcher tra cứu vị trí GPS xe trên bản đồ         │
│   → 3. Tra cứu thủ công trạm sạc VinFast còn trụ trống      │
│        phù hợp với loại cổng sạc của xe (CCS2/GBT)          │
│   → 4. Soạn tin nhắn chỉ dẫn đường đi gửi qua App tài xế   │
│   → 5. Liên hệ đội cứu hộ nếu pin dưới 5%                  │
│                                                             │
│ Bước nào tốn thời gian/lỗi nhất?                            │
│   Bước 3–4 (⏱ 12 phút/lượt)                                 │
│   Lỗi phổ biến: chỉ sai loại trụ sạc không phù hợp dòng xe. │
│                                                             │
│ AI có thể nhảy vào hỗ trợ ở bước nào?                       │
│   Bước 3–4: Auto-pull vị trí + API trạm sạc → LLM draft    │
│   tin hướng dẫn → Dispatcher click duyệt → Gửi.            │
│                                                             │
│ Đo thành công bằng gì (Metric có số)?                        │
│   Giảm thời gian xử lý sự cố từ 15 phút ──→ dưới 3 phút.   │
│   Tỉ lệ chỉ đúng loại trụ sạc phù hợp đạt ≥ 98%.          │
│                                                             │
│ Quick Architecture: [x] LLM Feature                         │
│   (Kết hợp API tra cứu có cấu trúc + LLM soạn ngôn ngữ     │
│    tự nhiên, Dispatcher luôn phê duyệt trước khi gửi)       │
└─────────────────────────────────────────────────────────────┘
```

---

### QUICK PROBLEM CARD #3

```
┌─────────────────────────────────────────────────────────────┐
│ QUICK PROBLEM CARD #3                                       │
│                                                             │
│ Bài toán: Phân loại và điều hướng tự động các khiếu nại     │
│           của cư dân Vinhomes từ App Vinhomes Resident.     │
│ Công ty thành viên: [x] Vinhomes                            │
│                                                             │
│ Ai đang đau (Actor)?                                        │
│   Nhân viên CSKH Ban Quản Lý Tòa Nhà (Ops Staff) phải      │
│   đọc thủ công và phân loại toàn bộ yêu cầu từ app.        │
│                                                             │
│ Workflow thủ công hiện tại (4 bước):                        │
│   1. Cư dân gửi khiếu nại qua App (mô tả tự do bằng tiếng  │
│      Việt: "điện tắt cầu thang T3", "nước nóng mất từ 7h") │
│   → 2. Nhân viên CSKH đọc từng yêu cầu                     │
│   → 3. Phân loại thủ công: Điện / Nước / Môi trường /      │
│        Bảo vệ / Phí dịch vụ                                  │
│   → 4. Forward thủ công đến đúng tổ kỹ thuật phụ trách     │
│                                                             │
│ Bước nào tốn thời gian/lỗi nhất?                            │
│   Bước 2–3 (⏱ 3–5 phút/yêu cầu × 200 yêu cầu/ngày         │
│   = ~10–16 giờ nhân công/ngày)                              │
│                                                             │
│ AI có thể nhảy vào hỗ trợ ở bước nào?                       │
│   Bước 2–3: LLM đọc mô tả tự do → Phân loại + Gán độ       │
│   ưu tiên (khẩn/bình thường) + Route đúng team.             │
│                                                             │
│ Đo thành công bằng gì (Metric có số)?                        │
│   Giảm thời gian phản hồi từ 12 giờ ──→ dưới 30 phút.      │
│   Độ chính xác phân loại tự động đạt ≥ 90%.                │
│                                                             │
│ Quick Architecture: [x] LLM Feature                         │
│   (Classification + routing — đơn giản, không cần Agent.   │
│    Cần Rule-based fallback cho khiếu nại pháp lý/tài chính) │
└─────────────────────────────────────────────────────────────┘
```

---

*Cá nhân đã thảo luận với nhóm và đề xuất bài toán **#1 (Vinmec Discharge Summary)** để tiến hành Deep-Dive vì: (1) bài toán có cấu trúc rõ ràng với dữ liệu HIS có sẵn, (2) ranh giới HITL nghiêm ngặt dễ enforce, (3) metric giảm thời gian dễ đo lường, (4) tác động thực tế cao — giúp bác sĩ có thêm thời gian cho bệnh nhân.*
