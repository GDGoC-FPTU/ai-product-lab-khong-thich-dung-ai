# 02 — Deep-Dive Report: Xử lý sự cố xe gần hết pin

## Thông tin nhóm

- **Tên nhóm:** [Khong thich dung AI]
- **Thành viên:**
  - [Nguyễn Khắc Huy] — [2A202602036]
  - [Ngô Khánh Trượng] — [2A220601477]
  - [Nguyễn Thị Xuân Mai] — [2A220601691]
  - [Chu Thành Dũng] — [2A202601405]
  - [Nguyễn Quốc Hiệu] — [2A202601627]
  - [Nguyễn Xuân Phượng] — [2A202601874]

  

> Các thời gian, số lượng và chi phí trong báo cáo là giả định dùng cho scoping ban đầu. Nhóm cần thay bằng dữ liệu vận hành thực tế nếu được cung cấp.

## 1. Quyết định lựa chọn

Nhóm chọn bài toán **hỗ trợ điều phối sự cố xe Xanh SM gần hết pin**. Khi tài xế báo pin thấp hoặc xe gặp khó khăn khi tiếp tục di chuyển, điều phối viên phải thu thập thông tin, kiểm tra vị trí, tìm phương án sạc/cứu hộ và hướng dẫn tài xế. Quy trình hiện tại có nhiều bước tra cứu và chuyển giao thông tin, trong khi quyết định cuối cùng vẫn cần nhân viên vận hành chịu trách nhiệm.

Lý do chọn: bài toán có actor và workflow rõ, metric có thể đo bằng thời gian xử lý, và có thể giới hạn AI ở vai trò tóm tắt/đề xuất bản nháp thay vì cho AI tự điều phối phương tiện.

## 2. Current-State Workflow Mapping

Quy trình hiện tại gồm các bước sau:

1. **Nhận báo cáo:** Tài xế gọi hoặc nhắn tin cho trung tâm điều phối, cung cấp biển số, mức pin và vị trí. *(Khoảng 2 phút)*
2. **Xác minh thông tin:** Điều phối viên đối chiếu xe, cuốc hiện tại và tọa độ trên các màn hình/hệ thống liên quan. 🔄 **Handoff tài xế → điều phối viên** *(Khoảng 3 phút)*
3. **Tìm phương án:** Điều phối viên tra cứu trạm sạc phù hợp hoặc liên hệ đội hỗ trợ/cứu hộ. 🔴 **Bottleneck** *(Khoảng 6 phút)*
4. **Soạn hướng dẫn:** Điều phối viên tự viết tin nhắn về phương án, địa điểm và bước tiếp theo. 🔴 **Bottleneck** *(Khoảng 4 phút)*
5. **Duyệt và gửi:** Điều phối viên kiểm tra lại rồi gửi hướng dẫn cho tài xế. 🔄 **Handoff điều phối viên → tài xế** *(Khoảng 2 phút)*
6. **Cập nhật log:** Điều phối viên ghi nhận nguyên nhân, phương án và trạng thái xử lý. *(Khoảng 2 phút)*

**Tổng thời gian ước tính: 19 phút/lượt.** Hai bottleneck chính là tra cứu phương án và soạn hướng dẫn, tổng cộng khoảng 10 phút/lượt.

## 3. Problem Statement — 6 fields

| Field | Nội dung |
|---|---|
| **Actor / Operator** | Tài xế Xanh SM là người báo sự cố; điều phối viên là người xác minh, chọn phương án và giao tiếp; đội hỗ trợ/cứu hộ thực hiện hỗ trợ thực địa khi cần. |
| **Current Workflow** | Tài xế báo mức pin/vị trí → điều phối viên xác minh dữ liệu → tra cứu trạm sạc hoặc đội hỗ trợ → soạn hướng dẫn → duyệt và gửi → cập nhật log. Quy trình ước tính 19 phút/lượt. |
| **Bottleneck** | Điều phối viên phải tra cứu nhiều nguồn và chuyển thông tin thủ công, sau đó soạn lại hướng dẫn. Sai vị trí, sai khoảng cách hoặc bỏ sót mức pin có thể khiến phương án không an toàn. |
| **Business Impact** | Xe phải chờ lâu, tài xế có thể bỏ lỡ cuốc tiếp theo và điều phối viên bị gián đoạn. Với giả định 40 sự cố/ngày, 19 phút/lượt tương đương khoảng 12,7 giờ xử lý mỗi ngày. |
| **Success Metric** | Giảm thời gian xử lý trung bình từ khoảng 19 phút xuống dưới 5 phút/lượt; 100% bản nháp có tag `[DRAFT_ONLY]`; 100% trường hợp pin dưới 5% được chuyển sang phương án sạc di động hoặc nhân viên xác minh; không để AI tự gửi lệnh. |
| **Operational Boundary** | AI được phép tóm tắt báo cáo, kiểm tra các trường dữ liệu, đề xuất phương án dựa trên dữ liệu đã xác minh và soạn tin nhắn nháp. AI không được tự gửi tin, tự gọi cứu hộ, tự đặt chuyến, tự bịa tọa độ/tình trạng trạm, hoặc đề xuất trạm cách hơn 5 km khi pin dưới 5%. Mọi hành động cần điều phối viên duyệt. |

## 4. Future-State Flow & AI Fit

### AI Fit

Nhóm chọn **LLM Feature kết hợp Rule/State-Machine**, không chọn Agentic Loop. Rule dùng cho các điều kiện an toàn có thể xác định rõ, như pin dưới 5%, thiếu vị trí hoặc thiếu dữ liệu. LLM chỉ tóm tắt nội dung tự do và tạo bản nháp dễ đọc. Agent tự trị không phù hợp vì một quyết định sai có thể làm xe dừng giữa đường hoặc gửi thông tin sai cho tài xế.

### Future-State Flow

```text
Tài xế báo sự cố
       |
       v
[Rule] Kiểm tra đủ biển số, vị trí, mức pin?
       | thiếu dữ liệu                 | đủ dữ liệu
       v                              v
  Yêu cầu bổ sung              [Rule] Pin < 5%?
                                      | Có                 | Không
                                      v                    v
                         Đề xuất mobile charger     Tra cứu dữ liệu trạm/hỗ trợ
                                      \                    /
                                       v                  v
                              [LLM] Tóm tắt + tạo bản nháp
                                             |
                                             v
                              [HUMAN] Điều phối viên duyệt
                                      | duyệt              | sửa/từ chối
                                      v                    v
                              Gửi cho tài xế       Sửa thủ công / fallback
                                             |
                                             v
                                      Cập nhật log
```

- 🔵 **AI Step:** Tóm tắt báo cáo và tạo bản nháp JSON/tin nhắn có `[DRAFT_ONLY]`.
- 🟢 **Human-in-the-loop:** Điều phối viên kiểm tra mức pin, vị trí, khoảng cách và duyệt trước khi gửi.
- ↩️ **Fallback:** Nếu AI lỗi, dữ liệu thiếu, confidence thấp hoặc kết quả không hợp lệ, quay về quy trình thủ công: điều phối viên gọi lại tài xế, tra cứu hệ thống và tự soạn hướng dẫn.

## 5. Prompt Prototype và kiểm thử ranh giới

File `starter-code/prompt_prototype.py` triển khai các ranh giới chính:

1. Câu trả lời phải bắt đầu bằng `[DRAFT_ONLY]`.
2. Pin dưới 5% không được đề xuất trạm cách hơn 5 km; phải đề xuất `dispatch_mobile_charger`.
3. Không được bịa vị trí, khoảng cách hoặc tình trạng trạm.
4. `requires_human_approval` luôn phải là `true`.

Nhóm dùng ba adversarial inputs để thử: yêu cầu bỏ qua giới hạn pin, yêu cầu gửi tin trực tiếp không cần duyệt và yêu cầu AI tự đoán dữ liệu còn thiếu. Các test đều phải được kiểm tra trước khi triển khai prototype.

## 6. Evaluate — AI Readiness Checklist

| Câu hỏi | Đánh giá | Lý do / việc cần làm |
|---|---|---|
| Có dữ liệu mẫu/log sạch để test chưa? | **Một phần** | Có thể bắt đầu bằng log đã ẩn thông tin cá nhân, nhưng cần chuẩn hóa mức pin, vị trí, loại xe, thời gian xử lý và kết quả cuối cùng. |
| Rủi ro AI sai có kiểm soát được không? | **Có, với điều kiện** | Có Rule cho pin/khoảng cách, bắt buộc Human-in-the-loop, schema JSON và fallback thủ công. Cần log toàn bộ output để audit. |
| Stakeholder sẵn sàng thay đổi quy trình không? | **Cần pilot** | Điều phối viên cần được hướng dẫn và có nút sửa/từ chối bản nháp. Nên thử ở một ca trực hoặc một khu vực trước. |

## 7. Quyết định cuối cùng

### **GO — triển khai prototype phạm vi hẹp**

Nhóm đề xuất GO cho một prototype chỉ làm ba việc: tóm tắt báo cáo, kiểm tra dữ liệu bắt buộc và soạn bản nháp. Prototype chưa được tự động gửi tin hoặc tự gọi cứu hộ. Trước khi mở rộng, nhóm cần xác nhận baseline thời gian xử lý, tạo tập test có các trường hợp pin thấp/thiếu dữ liệu và đo tỷ lệ đề xuất đúng.

Chi phí ban đầu chủ yếu là tích hợp dữ liệu, xây dựng giao diện duyệt, kiểm thử và đào tạo điều phối viên. Vì scope hẹp và có fallback, nhóm có thể kiểm chứng giá trị trước khi đầu tư vào tích hợp tự động sâu hơn. Nếu pilot không đạt thời gian dưới 5 phút hoặc xuất hiện lỗi an toàn chưa kiểm soát, dự án phải quay về trạng thái **NOT YET** để bổ sung dữ liệu và rule.

