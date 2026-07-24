# 01 — Problem Scan & Quick Problem Cards

> **Họ và tên:** [ĐIỀN HỌ VÀ TÊN]  
> **MSSV:** [ĐIỀN MSSV]  
> **Lưu ý:** Các thời gian và metric dưới đây là ước tính ban đầu để scoping, không phải số liệu nội bộ chính thức.

## Phase 1 — SCAN

Tôi quét các hoạt động vận hành của một số công ty thành viên Vingroup theo bốn lăng kính: tác vụ lặp lại, tốn thời gian, cơ hội nâng cấp bằng AI và nỗi đau của stakeholder.

| # | Công ty thành viên | Lens | Bài toán/bottleneck quan sát được |
|---:|---|---|---|
| 1 | VinFast | Lặp lại | Nhân viên chăm sóc khách hàng phải đọc và phân loại thủ công các yêu cầu bảo hành theo loại xe, bộ phận và mức độ khẩn cấp. |
| 2 | Xanh SM | Tốn thời gian | Điều phối viên phải tổng hợp thông tin từ cuộc gọi, vị trí xe và tình trạng pin để xử lý sự cố xe gần hết pin. |
| 3 | Vinhomes | AI-upgrade | Nhân viên CSKH phải đọc phản ánh của cư dân, xác định chủ đề rồi chuyển thủ công đến đúng bộ phận xử lý. |
| 4 | Vinmec | Tốn thời gian | Nhân viên phải tóm tắt nội dung cuộc gọi đặt lịch/đổi lịch khám và nhập lại thông tin vào hệ thống. |
| 5 | VinFast | Stakeholder Pain | Chủ xe khó nhận được câu trả lời nhất quán về tiến độ sửa chữa vì thông tin nằm rải rác giữa xưởng, CSKH và hệ thống đặt lịch. |

## Phase 2 — QUICK-ASSESS

Ba bài toán có tiềm năng nhất là: phân loại yêu cầu bảo hành VinFast, xử lý sự cố pin của Xanh SM và phân luồng phản ánh cư dân Vinhomes.

### Quick Problem Card #1 — Phân loại yêu cầu bảo hành VinFast

**Bài toán một câu:** Nhân viên CSKH cần phân loại nhanh yêu cầu bảo hành để chuyển đúng bộ phận và ưu tiên các trường hợp khẩn cấp.

- **Công ty:** VinFast
- **Actor/Operator:** Nhân viên chăm sóc khách hàng và bộ phận tiếp nhận bảo hành.
- **Workflow thủ công hiện tại:**
  1. Khách hàng gửi yêu cầu qua app, email hoặc tổng đài.
  2. Nhân viên đọc nội dung và kiểm tra thông tin xe.
  3. Nhân viên gắn nhãn lỗi, mức độ ưu tiên và bộ phận phụ trách.
  4. Nhân viên chuyển ticket và phản hồi thời gian dự kiến cho khách hàng.
- **Bước tốn thời gian/lỗi nhất:** Đọc nội dung tự do và chọn nhãn phù hợp, ước tính 5–8 phút/ticket.
- **AI có thể hỗ trợ:** Trích xuất biển số/model xe, tóm tắt triệu chứng, đề xuất nhãn và mức độ ưu tiên; nhân viên vẫn duyệt trước khi chuyển ticket.
- **Metric thành công:** Giảm thời gian phân loại trung bình từ khoảng 6 phút xuống dưới 2 phút/ticket; ít nhất 90% ticket được đề xuất đúng nhóm xử lý.
- **Quick Architecture:** LLM Feature kết hợp Rule-based validation.

### Quick Problem Card #2 — Xử lý sự cố pin xe Xanh SM

**Bài toán một câu:** Điều phối viên cần xử lý nhanh báo cáo xe gần hết pin để tài xế không phải chờ lâu hoặc nhận cuốc ngoài khả năng di chuyển.

- **Công ty:** Xanh SM
- **Actor/Operator:** Tài xế, điều phối viên và đội hỗ trợ/cứu hộ.
- **Workflow thủ công hiện tại:**
  1. Tài xế gọi hoặc nhắn tin báo mức pin và vị trí.
  2. Điều phối viên xác minh biển số, tọa độ và cuốc xe hiện tại.
  3. Điều phối viên tra cứu trạm sạc phù hợp hoặc đội hỗ trợ gần nhất.
  4. Điều phối viên gọi lại và soạn hướng dẫn cho tài xế.
  5. Điều phối viên cập nhật trạng thái sự cố vào log.
- **Bước tốn thời gian/lỗi nhất:** Tra cứu nhiều nguồn và chọn phương án hỗ trợ, ước tính 8–12 phút/lượt.
- **AI có thể hỗ trợ:** Tóm tắt thông tin sự cố, kiểm tra điều kiện pin/vị trí, đề xuất phương án và soạn tin nhắn dạng nháp.
- **Metric thành công:** Giảm thời gian xử lý từ khoảng 12 phút xuống dưới 4 phút/lượt; 100% tin nhắn phải được điều phối viên duyệt trước khi gửi.
- **Quick Architecture:** Rule + LLM Feature; không cho phép Agent tự gửi lệnh.

### Quick Problem Card #3 — Phân luồng phản ánh cư dân Vinhomes

**Bài toán một câu:** Phản ánh của cư dân cần được phân loại và chuyển đúng bộ phận nhanh hơn thay vì chờ nhân viên đọc thủ công.

- **Công ty:** Vinhomes
- **Actor/Operator:** Cư dân, nhân viên CSKH và các bộ phận kỹ thuật/an ninh/vệ sinh.
- **Workflow thủ công hiện tại:**
  1. Cư dân gửi phản ánh trên ứng dụng hoặc hotline.
  2. Nhân viên đọc nội dung, xác định tòa/căn hộ và chủ đề.
  3. Nhân viên chuyển yêu cầu đến bộ phận liên quan.
  4. Bộ phận xử lý cập nhật kết quả.
  5. CSKH phản hồi lại cư dân.
- **Bước tốn thời gian/lỗi nhất:** Xác định chủ đề, mức độ ưu tiên và bộ phận nhận việc, ước tính 4–6 phút/phản ánh.
- **AI có thể hỗ trợ:** Trích xuất địa điểm, phân loại chủ đề, phát hiện phản ánh khẩn cấp và soạn câu trả lời nháp.
- **Metric thành công:** 90% phản ánh được phân luồng trong dưới 1 phút; giảm tỷ lệ chuyển nhầm bộ phận xuống dưới 5%.
- **Quick Architecture:** LLM Feature có Rule-based kiểm tra các trường bắt buộc.

## Nhận xét lựa chọn

Bài toán Xanh SM có tác động vận hành tức thời nhưng yêu cầu kiểm soát an toàn chặt chẽ. Bài toán VinFast dễ bắt đầu bằng dữ liệu ticket lịch sử và có thể đo độ chính xác phân loại tương đối rõ. Bài toán Vinhomes có khối lượng lớn và phù hợp với mô hình phân loại văn bản, nhưng cần cẩn thận với phản ánh liên quan đến an ninh, tài chính hoặc tranh chấp.

Nếu được chọn một bài để làm prototype cá nhân, tôi chọn **phân loại yêu cầu bảo hành VinFast**, vì phạm vi ban đầu rõ, có thể giữ con người trong vòng phê duyệt và có metric kiểm thử cụ thể.

