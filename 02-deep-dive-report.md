# 02 — Deep-Dive Report (Bài nhóm)

**Tên nhóm:** [Điền tên nhóm]

**Thành viên:**
| # | Họ và tên | MSSV |
|---|---|---|
| 1 | Nguyễn Khắc Huy (Lead) | 23001525 |
| 2 | [Điền tên] | [Điền MSSV] |
| 3 | [Điền tên] | [Điền MSSV] |
| 4 | [Điền tên] | [Điền MSSV] |
| 5 | [Điền tên] | [Điền MSSV] |
| 6 | [Điền tên] | [Điền MSSV] |

---

## 🗳️ Quyết định lựa chọn của nhóm

Nhóm quyết định chọn **Quick Problem Card #2 — Vinhomes: Phân loại & điều hướng phản ánh cư dân** (từ `01-problem-scan.md`) để thực hiện Deep-Dive.

**Lý do lựa chọn và loại bỏ các card khác:**
* **Card #1 (VinFast — chẩn đoán lỗi xe):** Rủi ro kỹ thuật cao hơn vì gán sai mã lỗi ban đầu có thể ảnh hưởng đến an toàn vận hành xe; cần thêm dữ liệu lịch sử mã lỗi thực tế để huấn luyện/kiểm định trước khi tự tin triển khai.
* **Card #3 (Vinpearl — lọc review khẩn cấp):** Đây là tác vụ phân tích offline (back-office, theo ngày), không tạo áp lực vận hành real-time bằng bài toán phản ánh cư dân — nơi cư dân chờ phản hồi trực tiếp mỗi ngày và ảnh hưởng ngay đến trải nghiệm sống.
* **Card #2 được chọn vì:** Khối lượng phản ánh lớn, lặp lại hằng ngày, có ranh giới rõ ràng (chỉ phân loại + gợi ý điều hướng, không tự ý phản hồi/cam kết với cư dân), rủi ro khi AI sai nằm trong tầm kiểm soát (nhân viên vẫn duyệt trước khi chuyển phiếu).

---

# 🏗️ Phase 3 — DEEP-DIVE (Nhóm)

## 3.1. Current-State Workflow

*(Sơ đồ vẽ tay/A3 — xem file `04-workflow-diagram.png`. Tóm tắt bằng text bên dưới.)*

```text
┌──────────────┐     ┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│ Bước 1       │     │ Bước 2       │     │ Bước 3       │     │ Bước 4       │
│ Cư dân gửi   │     │ Nhân viên    │     │ Tra cứu ban  │     │ Chuyển phiếu │
│ phản ánh qua │ ──→ │ đọc & phân   │ ──→ │ phụ trách    │ ──→ │ & theo dõi   │
│ App Resident │     │ loại sự cố   │     │ theo tòa/tầng│     │ phản hồi     │
│ Ai: Cư dân   │     │ Ai: NV tổng đài│   │ Ai: NV tổng đài│  │ Ai: NV tổng đài│
│ ⏱ tức thời   │     │ ⏱ 5 phút 🔴  │     │ ⏱ 5 phút 🔴  │     │ ⏱ 2 phút     │
│ In: Nội dung │     │ In: Nội dung │     │ In: Loại sự cố│    │ Out: Phiếu   │
│ phản ánh     │     │ phản ánh     │     │ + vị trí     │     │ đã chuyển    │
└──────────────┘     └──────────────┘     └──────────────┘     └──────────────┘
🔴 = Bottleneck        🔄 Handoff: Nhân viên tổng đài → Ban Quản lý tòa nhà (bước 4)
⏱ Tổng thời gian xử lý thủ công: ~12 phút/lượt (chưa tính thời gian Ban Quản lý xử lý thực tế).
```

## 3.2. Problem Statement (6-field)

| Field | Nội dung chi tiết |
|---|---|
| **1. Actor / Operator** | Nhân viên tổng đài/lễ tân trực tổng hợp phản ánh của Ban Quản lý các tòa nhà Vinhomes. |
| **2. Current Workflow** | Cư dân gửi phản ánh (mất nước, hỏng đèn, ồn ào, gửi xe sai vị trí...) qua App Vinhomes Resident. Nhân viên đọc từng phản ánh, tự phân loại loại sự cố, tra cứu thủ công đúng ban/đội phụ trách theo tòa và tầng, rồi chuyển phiếu. Hoàn toàn thủ công, mất ~12 phút/lượt, dồn ứ mạnh vào giờ cao điểm buổi tối. |
| **3. Bottleneck** | Bước 2 & 3 (mất ~10 phút): Đọc hiểu nội dung phản ánh viết tự do bằng tiếng Việt, phân loại đúng nhóm sự cố, và tra cứu đúng ban phụ trách phù hợp — dễ nhầm lẫn khi khối lượng phản ánh lớn hoặc mô tả mập mờ. |
| **4. Business Impact** | Trung bình ~150 phản ánh/ngày/khu đô thị lớn. Tổng cộng lãng phí ~25 giờ nhân sự/ngày cho việc phân loại thủ công. Điều hướng sai ban phụ trách khiến phản hồi chậm trễ, gây bức xúc cư dân, ảnh hưởng điểm hài lòng (CSAT) và tăng nguy cơ khiếu nại lên cấp cao hơn. |
| **5. Success Metric** | 1. Giảm thời gian phân loại + điều hướng từ 10 phút xuống dưới 2 phút/lượt (Efficiency).<br>2. Tỉ lệ điều hướng đúng ban phụ trách ngay lần đầu đạt ≥ 95% (Quality). |
| **6. Operational Boundary** | AI được phép đọc nội dung phản ánh, phân loại loại sự cố, và **đề xuất (draft)** ban phụ trách phù hợp để nhân viên xem trước khi chuyển. **CẤM:** AI không được tự động gửi phản hồi trực tiếp cho cư dân, không được tự ý đóng/hủy phiếu phản ánh, không được suy diễn hoặc cam kết thời gian xử lý cụ thể thay cho Ban Quản lý. Mọi phiếu liên quan đến an toàn (cháy nổ, an ninh, y tế khẩn cấp) bắt buộc được gắn cờ ưu tiên cao nhất và chuyển ngay cho nhân viên xử lý thủ công, không qua bước AI phân loại thường. |

## 3.3. Future-State Flow & AI Fit

* **AI Fit:** Chọn **LLM Feature** (không cần Agent tự trị — quy trình có cấu trúc cố định là phân loại + gợi ý điều hướng; rủi ro khi AI gán sai ban phụ trách chỉ gây chậm trễ chứ không nguy hiểm tức thời, nên không cần mức Agentic Loop phức tạp).
* **Quy trình tương lai (Future-State):**

```text
┌──────────────┐     ┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│ Bước 1       │     │ Bước 2       │     │ Bước 3       │     │ Bước 4       │
│ Cư dân gửi   │     │ 🔵 AI phân   │     │ 🔵 AI gợi ý  │     │ 🟢 NV click  │
│ phản ánh qua │ ──→ │ loại loại sự │ ──→ │ ban phụ trách│ ──→ │ duyệt & chuyển│
│ App Resident │     │ cố tự động   │     │ + độ tin cậy │     │ phiếu        │
└──────────────┘     └──────────────┘     └──────────────┘     └──────────────┘
                                                                      │
                                                                      ▼
                                                               ↩️ Fallback:
                                                               Nếu AI không tự tin
                                                               (độ tin cậy thấp)
                                                               hoặc phát hiện từ
                                                               khóa khẩn cấp (cháy,
                                                               an ninh), tự động gắn
                                                               cờ "Cần xử lý thủ công
                                                               ngay" và chuyển thẳng
                                                               cho nhân viên, bỏ qua
                                                               bước gợi ý AI.
```

---

# 🏁 Phase 5 — EVALUATE

### AI Readiness Checklist:
1. [x] Chúng tôi có sẵn dữ liệu mẫu/logs sạch để test? — Có lịch sử phản ánh cư dân qua App Vinhomes Resident (nội dung + loại sự cố đã gán trước đây) làm dữ liệu tham chiếu.
2. [x] Rủi ro khi AI sai có nằm trong tầm kiểm soát (qua HITL hoặc Fallback)? — Có: mọi gợi ý của AI đều cần nhân viên duyệt trước khi chuyển phiếu (HITL), và có cơ chế Fallback tự động cho các trường hợp khẩn cấp/độ tin cậy thấp.
3. [x] Stakeholders sẵn sàng thay đổi quy trình làm việc cũ? — Nhân viên tổng đài chỉ cần chuyển từ "tự phân loại" sang "duyệt gợi ý AI", không thay đổi hệ thống App phía cư dân, mức độ xáo trộn quy trình thấp.

### Quyết định cuối cùng của Ban Giám Đốc Vin Smart Future:
[x] **GO (Bắt đầu xây dựng Prototype):** Bắt đầu phát triển với scope hẹp.
[ ] **NOT YET (Cần tích lũy thêm dữ liệu/xác lập baseline):** Trì hoãn để chuẩn bị thêm.
[ ] **NO-GO (Không khả thi / Rule-based tốt hơn):** Hủy bỏ dự án AI này.

**Justification:**
> Bài toán có khối lượng lặp lại lớn (~150 phản ánh/ngày), metric đo được rõ ràng (thời gian xử lý, tỉ lệ điều hướng đúng), và kiến trúc đề xuất (LLM Feature, không phải Agent) đơn giản, chi phí triển khai thấp (chỉ cần 1 API call phân loại + bảng tra cứu ban phụ trách sẵn có). Rủi ro chính — AI gán sai ban phụ trách hoặc bỏ sót phản ánh khẩn cấp — đã được kiểm soát qua HITL (nhân viên duyệt trước khi chuyển) và Fallback (tự động ưu tiên xử lý thủ công cho case khẩn cấp/độ tin cậy thấp). Vì vậy nhóm quyết định **GO**, triển khai thử nghiệm với scope hẹp (1 khu đô thị) trước khi nhân rộng.
