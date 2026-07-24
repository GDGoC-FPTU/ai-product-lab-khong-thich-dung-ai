# Phase 3 — DEEP-DIVE REPORT (Nhóm)

## Quyết định lựa chọn bài toán

Nhóm chọn bài toán: **Xanh SM — Xử lý sự cố pin / hết pin của tài xế thực địa**.

Lý do lựa chọn:

- Đây là bài toán có tác động trực tiếp đến khách hàng và tài xế.
- Quy trình hiện tại rõ, dễ mô hình hóa và đo lường.
- Thời gian xử lý thủ công dài, nên LLM Feature có thể đưa ra giá trị ngay.
- Ranh giới vận hành có thể kiểm soát rõ ràng qua prompt và phê duyệt của con người.

---

## Problem Statement (6-field)

| Field                       | Nội dung                                                                                                                                                                                                         |
| --------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **1. Actor / Operator**     | Điều phối viên Trung tâm Điều vận Xanh SM và tài xế VF8/VF5/VFe34 đang tham gia vào tình huống hết pin thực địa.                                                                                                 |
| **2. Current Workflow**     | Khi tài xế báo sự cố pin, điều phối viên thao tác thủ công: tra vị trí xe, tra trạm sạc gần nhất, soạn mật khẩu/định hướng, gửi tin nhắn cho tài xế, và gọi xe cứu hộ nếu cần.                                   |
| **3. Bottleneck**           | Bước tra cứu trạm sạc phù hợp và soạn tin nhắn chỉ dẫn chi tiết mất nhiều thời gian nhất (khoảng 10-12 phút trên mỗi lượt xử lý).                                                                                |
| **4. Business Impact**      | Mỗi sự cố mất trung bình 15 phút xử lý, gây lãng phí thời gian điều phối viên và kéo dài thời gian chờ của tài xế. Đây làm giảm hiệu quả vận hành và có thể gây mất doanh thu.                                   |
| **5. Success Metric**       | Giảm thời gian xử lý sự cố từ 15 phút xuống dưới 3 phút; đạt tỷ lệ đề xuất trạm phù hợp đúng trên 95%.                                                                                                           |
| **6. Operational Boundary** | AI được phép soạn draft chỉ dẫn và đề xuất trạm sạc. AI không được tự gửi tin mà không có phê duyệt của con người. Nếu pin dưới 5%, AI phải không đề xuất trạm sạc quá xa và phải yêu cầu xe cứu hộ pin di động. |

---

## Future-State Flow & AI Fit

### AI Fit

- Chọn: **LLM Feature**
- Vì: Quy trình có cấu trúc rõ ràng, cần xử lý ngôn ngữ và soạn tin nhắn, nhưng không cần được tự trị hoàn toàn.

### Future-State Flow

```text
Tài xế báo sự cố pin
   ↓
Điều phối viên nhập thông tin sự cố
   ↓
AI đọc vị trí + trạng thái pin + điều kiện xe
   ↓
AI draft một tin nhắn hướng dẫn hoặc JSON yêu cầu cứu hộ
   ↓
Dispatcher phê duyệt (Human-in-the-loop)
   ↓
Gửi tin nhắn cho tài xế / gọi xe cứu hộ
```

### Human-in-the-loop

- Người điều phối viên phải review và duyệt mọi draft trước khi gửi.
- Nếu kết quả AI có độ tin cậy thấp hoặc không chắc chắn, quay về quy trình thủ công cũ.

### Fallback

- Nếu AI không chắc chắn về trạm sạc, không gửi tin tự động.
- Dispatcher sẽ thao tác bằng tay như quy trình cũ.

---

## Evaluate

### AI Readiness Checklist

1. [x] Chúng tôi có dữ liệu mẫu/logs sạch để test.
2. [x] Rủi ro khi AI sai có nằm trong tầm kiểm soát nhờ HITL và fallback.
3. [x] Stakeholders sẵn sàng thay đổi quy trình làm việc cũ để giảm thời gian xử lý.

### Quyết định cuối cùng

- **GO**

### Lý giải quyết định

- Bài toán có phạm vi rõ ràng, nguồn dữ liệu tương đối có sẵn, và rủi ro khi sai có thể kiểm soát bằng phê duyệt người dùng.
- Với prompt boundary nghiêm ngặt, giải pháp LLM có thể giảm thời gian xử lý một cách đáng kể.
- Chi phí triển khai thấp hơn nhiều so với xây dựng agent phức tạp, phù hợp với scope lab.
