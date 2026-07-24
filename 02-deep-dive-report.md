# 02 — Deep-Dive Report & Evaluation

> **Deliverable nhóm — Phase 3 (DEEP-DIVE) & Phase 5 (EVALUATE)**

---

## 👥 Thông tin Nhóm

| | |
|---|---|
| **Tên nhóm:** | `[TÊN NHÓM — nhóm điền vào]` |
| **Tên repo:** | `ai-product-lab-khong-thich-dung-ai` |
| **Môn học:** | Lab 02 — AI Product Scoping (Vin Smart Future) |
| **Ngày nộp:** | 2026-07-24 |

### Danh sách thành viên

| STT | Họ và Tên | MSSV | Vai trò |
|-----|-----------|------|---------|
| 1 | `[Họ tên thành viên 1]` | `[MSSV 1]` | Trưởng nhóm / Viết báo cáo |
| 2 | `[Họ tên thành viên 2]` | `[MSSV 2]` | Vẽ sơ đồ workflow |
| 3 | `[Họ tên thành viên 3]` | `[MSSV 3]` | Code prompt_prototype.py |
| 4 | `[Họ tên thành viên 4]` | `[MSSV 4]` | Viết AI Log & Evaluation |

> ⚠️ **Nhóm cần điền đầy đủ tên nhóm và thông tin thành viên vào bảng trên trước khi nộp bài.**

---

## 🗳️ Quyết định lựa chọn bài toán Deep-Dive

**Bài toán được chọn:** **Vinmec — Tự động soạn thảo Tóm tắt Hồ sơ Xuất viện (Discharge Summary)**

### Lý do lựa chọn:
- **Tác động cao & đo lường được:** Mỗi bác sĩ Vinmec xử lý 8–15 ca xuất viện/ngày, mất 20–30 phút/ca → lãng phí 2,5–7,5 giờ/ngày thuần hành chính. AI có thể giảm xuống dưới 5 phút/ca.
- **Dữ liệu có cấu trúc sẵn:** Bệnh án điện tử (HIS) của Vinmec lưu trữ dữ liệu theo chuẩn HL7/JSON — LLM có đủ context để tổng hợp chính xác.
- **Ranh giới HITL tự nhiên:** Bác sĩ bắt buộc phải ký xác nhận trước khi trao bệnh nhân — cơ chế Human-in-the-loop đã được quy định bởi pháp lý y tế, không cần thiết kế thêm.

### Lý do loại bỏ các thẻ khác:
- **Card #2 (Xanh SM Sự cố sạc):** Bài toán hay nhưng phụ thuộc vào API real-time (định vị GPS + trạm sạc) mà nhóm chưa có quyền truy cập để test trong scope Lab 2 giờ.
- **Card #3 (Vinhomes Phân loại khiếu nại):** Rủi ro pháp lý cao khi AI tự phân loại tranh chấp tài chính/pháp lý của cư dân — cần Rule-based router bổ sung trước khi đưa LLM vào.

---

## 🏗️ Phase 3 — DEEP-DIVE

### 3.1. Current-State Workflow (Sơ đồ quy trình hiện tại)

> *(Xem ảnh sơ đồ vẽ tay hoặc sơ đồ kỹ thuật số tại file `04-workflow-diagram.png`)*

```text
CURRENT-STATE: Quy trình soạn Discharge Summary tại Vinmec (Thủ công)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  ┌──────────────────┐      ┌──────────────────┐      ┌──────────────────┐
  │    BƯỚC 1        │      │    BƯỚC 2        │      │    BƯỚC 3        │
  │  Bác sĩ mở HIS  │      │ Đọc thủ công:   │      │ Soạn thủ công   │
  │  (Bệnh án điện  │─────▶│  - Ghi chú điều  │─────▶│  bản tóm tắt    │
  │   tử Vinmec)    │  🔄  │  trị             │  🔴  │  xuất viện      │
  │                 │Handoff│  - Kết quả XN   │ Bot  │  trên Word/Form │
  │ Actor: Bác sĩ   │      │  - Chẩn đoán HA │ tleneck│ Actor: Bác sĩ  │
  │ ⏱ 2 phút        │      │ Actor: Bác sĩ   │      │ ⏱ 10–15 phút 🔴 │
  │ In: Bệnh nhân   │      │ ⏱ 10 phút 🔴    │      │ In: Raw data    │
  │ Out: HIS open   │      │ Out: Mental notes│      │ Out: Draft Word │
  └──────────────────┘      └──────────────────┘      └──────────────────┘
                                                              │
                                                              ▼
  ┌──────────────────┐      ┌──────────────────┐
  │    BƯỚC 5        │      │    BƯỚC 4        │
  │  Điều dưỡng     │      │  Bác sĩ ký tên  │
  │  trao tài liệu  │◀─────│  & đóng dấu     │
  │  cho bệnh nhân  │  🔄  │  xác nhận       │
  │                 │Handoff│                 │
  │ Actor: Điều dưỡng│     │ Actor: Bác sĩ   │
  │ ⏱ 2 phút        │      │ ⏱ 2 phút        │
  └──────────────────┘      └──────────────────┘

🔴 = Bottleneck (Bước 2 + 3 tổng cộng ~20–25 phút)
🔄 = Handoff (Điểm chuyển giao giữa Bác sĩ ↔ Hệ thống ↔ Điều dưỡng)
⏱  Tổng thời gian thủ công: ~26–30 phút/bệnh nhân
```

---

### 3.2. Problem Statement (6-field) — Vin Smart Future Standard

| Field | Nội dung chi tiết |
|---|---|
| **1. Actor / Operator** | Bác sĩ điều trị (Attending Physician) tại các khoa Nội trú của Bệnh viện Vinmec — người chịu trách nhiệm pháp lý ký xác nhận tài liệu xuất viện. |
| **2. Current Workflow** | Khi bệnh nhân được chỉ định xuất viện, bác sĩ phải: (1) mở HIS để đọc toàn bộ hồ sơ điều trị trong kỳ nằm viện; (2) đọc kết quả xét nghiệm và chẩn đoán hình ảnh; (3) tự viết tay bản tóm tắt gồm: chẩn đoán chính/phụ, quá trình điều trị, thuốc xuất viện, lịch tái khám và chỉ dẫn theo dõi tại nhà; (4) in và ký duyệt; (5) trao cho điều dưỡng chuyển bệnh nhân. Toàn bộ quy trình **hoàn toàn thủ công**, mất **26–30 phút/bệnh nhân**. |
| **3. Bottleneck** | **Bước 2 & 3** chiếm 20–25 phút: Bác sĩ phải đọc và tổng hợp thủ công dữ liệu từ nhiều nguồn (ghi chú lâm sàng, xét nghiệm, CĐHA) rồi diễn giải lại bằng ngôn ngữ dễ hiểu cho bệnh nhân. Đây là tác vụ tổng hợp ngôn ngữ có cấu trúc cao — điểm mạnh cốt lõi của LLM. Lỗi phổ biến: bỏ sót tương tác thuốc, sai liều lượng trong hướng dẫn về nhà. |
| **4. Business Impact** | Mỗi khoa Nội trú Vinmec xử lý 15–30 ca xuất viện/ngày. Với 10 khoa nội trú tại một bệnh viện Vinmec lớn → **150–300 bộ Discharge Summary/ngày**. Mỗi ca tốn 25 phút bác sĩ = **62–125 giờ bác sĩ/ngày** tiêu tốn vào hành chính. Chi phí cơ hội ước tính: 1 giờ bác sĩ chuyên khoa ~ 500.000–800.000 VND → **lãng phí 31–100 triệu VND/ngày/bệnh viện** chỉ từ tác vụ soạn thảo này. |
| **5. Success Metric** | 1. **Efficiency:** Giảm tổng thời gian bác sĩ soạn Discharge Summary từ **25 phút → dưới 5 phút** (bác sĩ chỉ review & ký) — giảm 80%.<br>2. **Quality:** Tỉ lệ bác sĩ chấp nhận draft LLM mà không cần chỉnh sửa lớn (>50% nội dung) đạt **≥ 80%** sau 30 ngày vận hành.<br>3. **Safety:** Tỉ lệ draft có lỗi nghiêm trọng (sai thuốc, sai liều, sai bệnh nhân) = **0%** nhờ cơ chế HITL bắt buộc. |
| **6. Operational Boundary** | ✅ **AI được phép:** Truy xuất dữ liệu HIS của bệnh nhân đang được chỉ định xuất viện (với token phiên làm việc của bác sĩ xác thực); tổng hợp và draft bản Discharge Summary dạng `[DRAFT_ONLY]`; đề xuất danh sách thuốc xuất viện từ y lệnh đã có.<br>❌ **AI TUYỆT ĐỐI KHÔNG được:** Tự động gửi hoặc in Discharge Summary mà chưa có chữ ký điện tử xác nhận của bác sĩ; truy cập hồ sơ bệnh nhân không thuộc ca trực hiện tại; đề xuất thêm thuốc mới không có trong y lệnh đã được kê bởi bác sĩ; xử lý dữ liệu mà không có xác thực HIS session hợp lệ. |

---

### 3.3. Future-State Flow & AI Fit

**AI Fit:** ✅ **LLM Feature** (không cần Agentic Loop)

**Lý do chọn LLM Feature thay vì Agent:**
- Quy trình có cấu trúc cố định, đầu vào (HIS data) xác định rõ ràng, đầu ra (Discharge Summary template) có template cố định.
- Rủi ro y tế cực cao → **không thể** để AI tự trị hành động mà không có bác sĩ phê duyệt ở mỗi bước quan trọng.
- Rule-based không đủ vì bản tóm tắt cần diễn giải ngôn ngữ tự nhiên linh hoạt, không phải chỉ điền template cứng.

**Quy trình tương lai (Future-State):**

```text
FUTURE-STATE: Quy trình AI-Assisted Discharge Summary tại Vinmec
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  ┌──────────────────┐      ┌──────────────────┐      ┌──────────────────┐
  │    BƯỚC 1        │      │    BƯỚC 2 🔵      │      │    BƯỚC 3 🟢      │
  │  Bác sĩ click   │      │  AI tự động pull │      │  Bác sĩ review  │
  │  "Xuất Viện"    │─────▶│  dữ liệu HIS &  │─────▶│  draft trên màn │
  │  trong HIS      │  🔄  │  generate draft  │  🔄  │  hình, chỉnh    │
  │                 │Handoff│  Discharge       │Handoff│  sửa nếu cần   │
  │ Actor: Bác sĩ   │      │  Summary         │      │ Actor: Bác sĩ   │
  │ ⏱ 30 giây       │      │ Actor: LLM       │      │ ⏱ 2–4 phút      │
  │                 │      │ ⏱ 15–30 giây     │      │                 │
  └──────────────────┘      └──────────────────┘      └──────────────────┘
                                                              │
                                                              ▼
  ┌──────────────────┐      ┌──────────────────┐
  │    BƯỚC 5        │      │    BƯỚC 4 🟢      │
  │  Điều dưỡng     │      │  Bác sĩ ký điện  │
  │  trao tài liệu  │◀─────│  tử xác nhận    │
  │  cho bệnh nhân  │  🔄  │  → HIS lưu &    │
  │                 │Handoff│  in tự động     │
  │ Actor: Điều dưỡng│     │ Actor: Bác sĩ   │
  │ ⏱ 2 phút        │      │ ⏱ 30 giây        │
  └──────────────────┘      └──────────────────┘

         ↩️ FALLBACK:
         Nếu LLM generate lỗi hoặc HIS API timeout →
         Hệ thống hiển thị thông báo lỗi rõ ràng →
         Bác sĩ soạn thủ công như quy trình cũ.
         Không có downtime — hệ thống cũ luôn sẵn sàng dự phòng.

🔵 = AI Step (LLM tự động xử lý)
🟢 = Human Step — HITL bắt buộc (Bác sĩ phê duyệt/ký xác nhận)
🔄 = Handoff (Điểm chuyển giao)
⏱  Tổng thời gian mới ước tính: ~5–7 phút/bệnh nhân (giảm ~80%)
```

---

## 🏁 Phase 5 — EVALUATE

### AI Readiness Checklist

| # | Tiêu chí | Đánh giá | Ghi chú |
|---|----------|----------|---------|
| 1 | ✅ Chúng tôi có sẵn dữ liệu mẫu/logs sạch để test? | **CÓ** | Vinmec đã vận hành HIS từ 2012 với hàng triệu hồ sơ bệnh án có cấu trúc theo chuẩn HL7 FHIR. Có thể tạo dữ liệu ẩn danh hóa (de-identified) để test LLM trong môi trường sandbox. |
| 2 | ✅ Rủi ro khi AI sai có nằm trong tầm kiểm soát? | **CÓ** | Cơ chế HITL bắt buộc (bác sĩ ký xác nhận) đảm bảo AI không thể đưa sai thông tin đến tay bệnh nhân mà không qua review. Fallback về quy trình thủ công luôn sẵn sàng. |
| 3 | ✅ Stakeholders sẵn sàng thay đổi quy trình cũ? | **CÓ — CÓ ĐIỀU KIỆN** | Bác sĩ phàn nàn về tải hành chính → động lực thay đổi cao. Tuy nhiên cần training về cách sử dụng và xây dựng niềm tin vào chất lượng draft (pilot với 1 khoa trước). |

### Quyết định cuối cùng của Ban Giám Đốc Vin Smart Future

**[x] ✅ GO — Bắt đầu xây dựng Prototype với scope hẹp (1 khoa nội trú)**

### Justification (Lý giải quyết định dựa trên bằng chứng kỹ thuật và chi phí)

**Luận điểm GO:**

**1. Dữ liệu & Kỹ thuật:**
- Bệnh án HIS Vinmec có cấu trúc JSON/HL7 FHIR → LLM có thể parse và tổng hợp trực tiếp, không cần crawl dữ liệu phi cấu trúc.
- Bản Discharge Summary có template cố định (chẩn đoán, điều trị, thuốc, tái khám) → giảm rủi ro hallucination vì output có schema bắt buộc.
- Gemini 2.5 Flash đã chứng minh khả năng tổng hợp tài liệu y tế tiếng Việt trong các benchmark nội bộ của Vin Smart Future.

**2. Ranh giới & Kiểm soát rủi ro:**
- Bác sĩ **BẮT BUỘC** ký xác nhận trước khi tài liệu được chuyển bệnh nhân → rủi ro AI sai = 0 khi đến tay bệnh nhân.
- Fallback về quy trình thủ công luôn sẵn sàng, không có single point of failure.
- Dữ liệu bệnh nhân được xử lý trong môi trường on-premise Vinmec, không gửi ra ngoài → tuân thủ Luật An ninh mạng và quy định bảo mật y tế.

**3. Ước lượng chi phí & ROI:**
| Hạng mục | Chi phí ước tính |
|----------|-----------------|
| Gemini 2.5 Flash API (input ~2000 tokens/ca × 300 ca/ngày) | ~$0.45 USD/ngày |
| Development cost (4 tuần, 2 kỹ sư) | ~$8,000 USD one-time |
| Integration với HIS Vinmec | ~$5,000 USD one-time |
| **Tổng chi phí năm đầu** | **~$13,164 USD** |

| Lợi ích | Giá trị ước tính |
|---------|-----------------|
| Giảm 20 phút/ca × 300 ca/ngày × 300.000 VND/giờ bác sĩ | ~450 triệu VND/tháng |
| **ROI dự kiến** | **Hoàn vốn trong < 1 tháng vận hành** |

**Khuyến nghị triển khai:** Bắt đầu **pilot 1 khoa Nội Tim Mạch** trong 30 ngày để thu thập feedback bác sĩ và đo lường tỉ lệ chấp nhận draft trước khi rollout toàn bệnh viện.
