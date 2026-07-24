# 02 — Deep-Dive Report (Phase 3 & 5)

**Tên nhóm:** _____________
**Thành viên (Họ tên — MSSV):**
- _____________ — _____________
- _____________ — _____________
- _____________ — _____________

**Bài toán được chọn Deep-Dive:** Điều phối viên Xanh SM phản hồi chậm/sai khi tài xế báo pin nguy cấp (<5%) — xem `04-workflow-diagram.svg` cho sơ đồ vẽ tay/số hóa của Phase 3.1.

---

## 3.2. Problem Statement (6-field)

| Field | Nội dung chi tiết |
|---|---|
| **1. Actor / Operator** | Điều phối viên tổng đài (dispatcher) Xanh SM, người trực tiếp nhận yêu cầu hỗ trợ từ tài xế qua app/hotline. |
| **2. Current Workflow** | Tài xế gọi/nhắn báo pin thấp → dispatcher tra hệ thống trạm sạc (công cụ tách rời với app điều xe) → tự tính khoảng cách và quyết định gợi ý trạm hay điều xe sạc di động → soạn tay tin nhắn gửi tài xế → nếu cần điều xe sạc di động, gọi thêm đội logistics riêng để xác nhận. |
| **3. Bottleneck** | Bước tra cứu + ra quyết định thủ công (bước 2-3): dispatcher phải tự đối chiếu 2 hệ thống, tính khoảng cách, và tự nhớ ngưỡng an toàn pin — dễ chậm và dễ gợi ý sai khi khối lượng ca tăng vào giờ cao điểm. |
| **4. Business Impact** | Trễ phản hồi ở case pin nguy cấp làm tăng rủi ro xe hết pin giữa đường (SOS/breakdown), phát sinh chi phí cứu hộ ngoài kế hoạch và ảnh hưởng trải nghiệm tài xế/khách hàng đi cùng chuyến. *(Số liệu cụ thể — thời gian phản hồi trung bình, số ca SOS/tháng — cần đội vận hành xác nhận thực tế trước khi đưa vào báo cáo chính thức; đây là ước lượng giả định để scoping.)* |
| **5. Success Metric** | Giảm thời gian phản hồi trung bình cho case pin <5% từ ~15 phút xuống dưới 3 phút; 100% case pin <5% không được gợi ý trạm sạc cách hơn 5km (đo qua log audit). |
| **6. Operational Boundary** | AI chỉ được tạo **bản nháp** (`[DRAFT_ONLY]`), không tự động gửi tin nhắn cho tài xế; khi pin <5%, AI **tuyệt đối không** được gợi ý trạm >5km mà phải trigger lệnh điều xe sạc di động; mọi output bắt buộc qua dispatcher duyệt trước khi gửi; nếu dữ liệu GPS/pin thiếu hoặc mâu thuẫn, AI phải escalate cho người, không tự suy diễn. |

---

## 3.3. Future-State Flow & AI Fit

**AI-Fit Matrix:** [x] LLM Feature (kết hợp Rule cứng cho ngưỡng pin an toàn)
> Lý do không chọn thuần Rule/State-Machine: input từ tài xế là văn bản tự do (nhiều cách diễn đạt), cần LLM để trích xuất thông tin (pin %, vị trí, mức độ khẩn cấp). Lý do không cần Agentic Loop: tác vụ chỉ 1 bước quyết định + 1 bước soạn thảo, không cần chuỗi hành động tự trị nhiều bước.

**Future-State Flow:**
1. Tài xế nhắn tin/app báo tình trạng pin → 🔵 **AI Step:** LLM trích xuất % pin, vị trí GPS, mức khẩn cấp từ văn bản tự do.
2. 🔵 **AI Step:** Áp rule cứng — nếu pin <5% → sinh lệnh JSON `dispatch_mobile_charger` + draft giải thích; nếu không → LLM soạn draft gợi ý trạm sạc phù hợp gần nhất.
3. 🟢 **Human Step (HITL):** Dispatcher xem bản nháp gắn thẻ `[DRAFT_ONLY]`, duyệt hoặc chỉnh sửa trong vài giây trước khi gửi — bắt buộc vì đây là quyết định ảnh hưởng an toàn.
4. ↩️ **Fallback:** Nếu AI không trích xuất được pin %/vị trí, hoặc dữ liệu mâu thuẫn (VD: pin báo thấp nhưng vị trí không khớp GPS xe) → escalate thẳng cho dispatcher xử lý thủ công, không đưa ra gợi ý tự động.

---

## Phase 5 — EVALUATE

### AI Readiness Checklist
1. [ ] Chúng tôi có sẵn dữ liệu mẫu/logs sạch để test?
   → *Có log GPS + danh sách trạm sạc, nhưng chưa có tập tin nhắn tài xế thực tế đã gắn nhãn (labeled) để test độ chính xác trích xuất pin%/vị trí — cần thu thập thêm trước khi mở rộng.*
2. [x] Rủi ro khi AI sai có nằm trong tầm kiểm soát (qua HITL hoặc Fallback)?
   → *Có — nhờ HITL bắt buộc (`[DRAFT_ONLY]`) và rule cứng không phụ thuộc LLM cho ngưỡng pin nguy cấp (đã stress-test ở Phase 4, xem `extras/prompt_prototype.py`).*
3. [ ] Stakeholders sẵn sàng thay đổi quy trình làm việc cũ?
   → *Cần xác nhận thêm với đội vận hành thực địa (dispatcher + logistics) về việc tích hợp thêm 1 bước duyệt AI vào quy trình hiện tại.*

### Quyết định cuối cùng của Ban Giám Đốc Vin Smart Future:
[x] **GO (phạm vi hẹp):** Bắt đầu xây dựng Prototype **chỉ cho nhánh pin nguy cấp (<5%)** — phần rule-cứng ít rủi ro nhất và đã được chứng minh giữ vững ranh giới qua adversarial testing ở Phase 4.
[ ] NOT YET
[ ] NO-GO

**Justification:**
> Rule ngưỡng pin (<5% → điều xe sạc di động, không gợi ý trạm xa) là logic quyết định-đơn (deterministic) có thể kiểm chứng độc lập với LLM, nên rủi ro sai lệch thấp và dễ audit. Phần trích xuất thông tin từ văn bản tự do (LLM) vẫn cần thêm dữ liệu mẫu thực tế để đánh giá độ chính xác trước khi mở rộng sang các case pin không nguy cấp (gợi ý trạm sạc thường). Vì vậy quyết định GO có điều kiện: triển khai pilot hẹp, thu thập thêm dữ liệu song song, review lại sau 4-6 tuần trước khi mở rộng phạm vi.
