# 02-deep-dive-report.md (Bài nhóm - 40 điểm)

## 1. Quyết định lựa chọn bài toán Deep-Dive
* **Tên bài toán:** Tự động hóa phân loại, trích xuất thông tin chứng từ kế toán và đối chiếu tự động với đơn đặt hàng (PO Matching).
* **Công ty thành viên:** **VinFast**
* **Lý do lựa chọn:** Đây là quy trình nghiệp vụ có khối lượng giao dịch khổng lồ hằng ngày, tính chất lặp đi lặp lại cao, tốn nhiều nhân lực thủ công, dễ phát sinh sai sót số học và là điểm nghẽn (bottleneck) trực tiếp ảnh hưởng đến thời gian thanh toán cho nhà cung cấp của VinFast.

---

## 2. Problem Statement (6-field) & Metrics

| Field | Nội dung chi tiết |
|---|---|
| **1. Actor / Operator** | Nhân viên kế toán thanh toán, Kế toán viên công nợ và Kế toán trưởng tại VinFast. |
| **2. Current Workflow** | Nhân viên kế toán nhận chứng từ hóa đơn từ nhà cung cấp (PDF, ảnh scan, bản cứng), mở phần mềm SAP/ERP thủ công để gõ lại toàn bộ các trường dữ liệu (mã số thuế, tên nhà cung cấp, tiền hàng, thuế suất VAT), sau đó lưu trữ file và chuyển bản cứng trình ký. |
| **3. Bottleneck** | Quá trình nhập liệu thủ công từng trường thông tin từ hóa đơn đa dạng định dạng vào SAP mất từ 8 - 12 phút/hóa đơn; thao tác kiểm tra chéo (cross-check) thông tin trên hóa đơn với hệ thống Đơn đặt hàng (PO) và Biên bản giao nhận hàng hóa (GR) tốn nhiều thời gian và dễ xảy ra sai sót lệch số tiền, mã số thuế. |
| **4. Business Impact** | Tổn thất thời gian nhân sự lớn (hàng trăm giờ công mỗi tháng), chậm trễ chu kỳ thanh toán cho nhà cung cấp (ảnh hưởng đến quan hệ đối tác chiến lược), rủi ro pháp lý và tài chính khi nhập sai thuế suất VAT hoặc hóa đơn giả mạo. |
| **5. Success Metric** | - Giảm thời gian xử lý mỗi hóa đơn từ **10 phút xuống dưới 1 phút**.<br>- Tỷ lệ trích xuất chính xác thông tin (Field-level Accuracy) đạt **>= 95%**.<br>- Giảm tỷ lệ sai sót nhập liệu từ **6% xuống dưới 0.5%**.<br>- Tự động hóa hoàn toàn 80% các hóa đơn đạt chuẩn (Straight-through Processing). |
| **6. Operational Boundary** | **Được phép:** Trích xuất tự động dữ liệu văn bản từ hóa đơn, phân loại cấu trúc, đối chiếu sơ bộ dữ liệu với PO và đề xuất trạng thái duyệt.<br>**TUYỆT ĐỐI KHÔNG ĐƯỢC PHÉP:** Tự động bấm nút phê duyệt (Approve) thanh toán chuyển tiền, tự động điều chỉnh số tiền trên hệ thống tài chính mà không có sự xác nhận của con người.<br>**Điểm cần duyệt (HITL):** Mọi lệnh chuyển tiền thanh toán thực tế và các hóa đơn có cảnh báo rủi ro/lệch số liệu bắt buộc phải qua bước kiểm duyệt và xác nhận của Kế toán trưởng hoặc Trưởng bộ phận Tài chính. |

---

## 3. Future-State Flow & AI Fit

### 3.1. Xác định mức AI Fit
* **AI-Fit Matrix:** **LLM Feature kết hợp OCR Pipeline & Rule-based Validation** (Ứng dụng Trích xuất thông minh kết hợp kiểm tra logic nghiệp vụ tài chính).

### 3.2. Sơ đồ quy trình tương lai (Future-State Flow)
1. **Nhận đầu vào tự động:** Nhà cung cấp gửi hóa đơn điện tử/PDF qua cổng thông tin hoặc email tập trung.
2. **🔵 AI Step (OCR & LLM Extraction):** Pipeline OCR đọc ảnh/PDF, trích xuất toàn bộ dữ liệu thô, sau đó LLM chuyển hóa dữ liệu thô thành định dạng JSON có cấu trúc chuẩn hóa (Tên, MST, Tổng tiền, Tiền thuế, Danh mục hàng hóa).
3. **Rule-based Check:** Hệ thống tự động chạy các luật kiểm tra (Validation Rules) đối chiếu dữ liệu JSON với hệ thống SAP (so khớp số PO, mã nhà cung cấp, dung sai số tiền).
4. **Phân nhánh xử lý:**
   * *Trường hợp khớp hoàn toàn (Match):* Chuyển thẳng sang trạng thái chờ kế toán trưởng bấm duyệt thanh toán.
   * *Trường hợp có sai lệch/bất thường (Mismatch/Anomaly):* Đưa vào danh sách cảnh báo (Flagged).
5. **🟢 Human Step (HITL - Human-in-the-loop):** Kế toán viên hoặc Kế toán trưởng kiểm tra lại các hóa đơn bị cảnh báo hoặc thực hiện phê duyệt cuối cùng lệnh thanh toán.
6. **↩️ Fallback Plan:** Nếu LLM trả về kết quả định dạng lỗi, điểm tự tin (confidence score) thấp hơn ngưỡng 0.85, hoặc hệ thống OCR không đọc được văn bản mờ, hệ thống sẽ tự động chuyển hóa đơn sang hàng đợi xử lý thủ công hoàn toàn (Manual Queue) như quy trình cũ để đảm bảo không bị gián đoạn vận hành.

---

## 4. Evaluate

### 4.1. AI Readiness Checklist
1. **[x] Chúng tôi có sẵn dữ liệu mẫu/logs sạch để test?** (Đã có bộ dữ liệu hóa đơn mẫu định dạng PDF và hình ảnh anonymized từ phòng kế toán VinFast).
2. **[x] Rủi ro khi AI sai có nằm trong tầm kiểm soát (qua HITL hoặc Fallback)?** (Có, toàn bộ các quyết định giải ngân tiền tệ đều bị chặn lại bởi cơ chế Human-in-the-loop và giới hạn ranh giới vận hành nghiêm ngặt).
3. **[x] Stakeholders sẵn sàng thay đổi quy trình làm việc cũ?** (Đã có sự cam kết đồng hành từ Trưởng bộ phận Kế toán thanh toán VinFast nhằm giảm tải áp lực mùa cao điểm).

### 4.2. Quyết định cuối cùng của Ban Giám Đốc Vin Smart Future
* **[x] GO (Bắt đầu xây dựng Prototype):** Bắt đầu phát triển với scope hẹp (tập trung vào nhóm hóa đơn nguyên vật liệu chuẩn).
* [ ] **NOT YET (Cần tích lũy thêm dữ liệu/xác lập baseline)**
* [ ] **NO-GO (Không khả thi / Rule-based tốt hơn)**

### 4.3. Justification (Lý giải quyết định dựa trên bằng chứng kỹ thuật và chi phí)
* **Luận điểm kỹ thuật:** Bài toán kết hợp giữa OCR truyền thống và LLM (Structured Output Extraction) giải quyết triệt để điểm yếu của công nghệ OCR cũ là không hiểu ngữ cảnh tài liệu. Các trường dữ liệu phức tạp, bố cục thay đổi linh hoạt giữa các nhà cung cấp khác nhau nay được LLM chuẩn hóa chính xác.
* **Hiệu quả chi phí (Cost-Benefit Analysis):** Chi phí vận hành API LLM và hạ tầng OCR ước tính cực kỳ thấp so với hàng nghìn giờ công lao động thủ công bị lãng phí mỗi tháng. Thời gian hoàn vốn (ROI) dự kiến đạt được trong vòng chưa đầy 3 tháng triển khai thực tế tại VinFast.
