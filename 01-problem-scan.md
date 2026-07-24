# 01-problem-scan.md - Bài cá nhân (15 điểm)

## Phase 1: Bảng quét cơ hội (SCAN)

Dưới đây là bảng quét 5 bài toán thực tế thuộc các công ty thành viên trong hệ sinh thái Vingroup, được phân tích qua các thấu kính nhận diện cơ hội:

| STT | Tên bài toán | Công ty thành viên | Mô tả ngắn bài toán | Thấu kính áp dụng |
| :-- | :-- | :-- | :-- | :-- |
| 1 | Tự động hóa phân loại và trích xuất thông tin hóa đơn/chứng từ kế toán | VinFast | Bộ phận kế toán phải xử lý hàng nghìn hóa đơn đầu vào, chứng từ thanh toán từ nhà cung cấp với nhiều định dạng khác nhau (PDF, scan tay, ảnh chụp), dẫn đến việc nhập liệu thủ công tốn nhiều thời gian và dễ sai sót. | Lặp lại (Repetitive) & Tốn thời gian (Time-consuming) |
| 2 | Trợ lý ảo AI hỗ trợ giải đáp quy trình nội bộ và chính sách nhân sự | Vinschool | Đội ngũ nhân sự và giáo viên thường xuyên phải tra cứu các quy chế, quy định phúc lợi, quy trình nghỉ phép dài dòng từ kho tài liệu nội bộ, gây quá tải cho bộ phận HR Helpdesk. | Tốn thời gian (Time-consuming) & AI-upgrade |
| 3 | Tự động kiểm tra và phản hồi lỗi code/Pull Request sơ bộ cho đội ngũ lập trình viên | VinBigData | Các kỹ sư phần mềm tốn nhiều thời gian cho việc review các lỗi cú pháp cơ bản, quy chuẩn code (coding convention) lặp đi lặp lại trước khi tiến hành review chuyên sâu. | Lặp lại (Repetitive) |
| 4 | Phân tích và tổng hợp, phân loại feedback khách hàng từ hệ thống tổng đài/CSKH | Vinpearl | Đội ngũ chăm sóc khách hàng nhận hàng nghìn cuộc gọi và tin nhắn mỗi ngày. Việc phân tích thủ công các chủ đề phàn nàn phổ biến làm chậm quá trình cải thiện dịch vụ. | Stakeholder Pain & AI-upgrade |
| 5 | Tối ưu hóa lộ trình giao hàng và điều phối xe nội bộ cho chuỗi cung ứng linh kiện | VinFast | Nhân viên điều phối vận tải phải xử lý thủ công các đơn hàng giao nhận linh kiện giữa các kho bãi, dễ dẫn đến việc chọn tuyến đường chưa tối ưu và lãng phí nhiên liệu. | Lặp lại (Repetitive) & Stakeholder Pain |

---

## Phase 2: 3 Quick Problem Cards

### Quick Problem Card 1: Tự động hóa phân loại và trích xuất thông tin chứng từ kế toán
* **Tên bài toán và công ty thành viên:** Tự động hóa xử lý chứng từ kế toán - **VinFast**
* **Tác nhân đang gặp khó khăn (Actor/Operator):** Nhân viên kế toán thanh toán / Kế toán viên công nợ.
* **Sơ đồ quy trình thủ công hiện tại:**
  1. Nhận chứng từ/hóa đơn từ nhà cung cấp (qua email hoặc bản cứng).
  2. Kiểm tra tính hợp lệ bằng mắt thường (mã số thuế, ngày tháng, chữ ký).
  3. Mở phần mềm kế toán (ERP/SAP) và nhập thủ công từng trường dữ liệu (tên, số tiền, thuế VAT, mã nhà cung cấp).
  4. Lưu trữ file scan vào thư mục nội bộ và chuyển bản cứng cho kế toán trưởng duyệt.
* **Bước tốn thời gian/gây lỗi nhiều nhất:** Bước nhập liệu thủ công các trường dữ liệu từ hóa đơn PDF/ảnh sang SAP. 
  * *Thời gian xử lý ước tính:* ~8 - 12 phút/hóa đơn; tỷ lệ sai sót nhập liệu khoảng 5-7%.
* **Bước mà AI có thể tham gia giải quyết:** Sử dụng công nghệ OCR kết hợp mô hình ngôn ngữ lớn (LLM) để tự động nhận diện, trích xuất toàn bộ các trường thông tin quan trọng từ hóa đơn và tự động đối chiếu với đơn đặt hàng (PO).
* **Metric đo thành công có con số cụ thể:** Giảm thời gian xử lý mỗi hóa đơn từ 10 phút xuống dưới 1 phút; giảm tỷ lệ sai sót nhập liệu xuống dưới 0.5%.
* **Đề xuất kiến trúc sơ bộ:** LLM (Kết hợp OCR Pipeline + LLM để trích xuất cấu trúc dữ liệu).

---

### Quick Problem Card 2: Trợ lý ảo AI giải đáp quy chế, chính sách nội bộ
* **Tên bài toán và công ty thành viên:** Trợ lý ảo tra cứu chính sách nhân sự nội bộ - **Vinschool**
* **Tác nhân đang gặp khó khăn (Actor/Operator):** Giáo viên, nhân viên khối hành chính và chuyên viên Nhân sự (HR).
* **Sơ đồ quy trình thủ công hiện tại:**
  1. Nhân viên gặp thắc mắc về quy chế (ví dụ: chế độ thai sản, quy định nghỉ phép, quy trình đào tạo).
  2. Nhân viên tìm kiếm thủ công trong hàng chục file PDF nội bộ trên cổng thông tin hoặc Google Drive.
  3. Nếu không tìm thấy, nhân viên nhắn tin hoặc gọi điện trực tiếp cho chuyên viên HR phụ trách.
  4. Chuyên viên HR phải dừng công việc hiện tại để tra cứu văn bản và trả lời từng cá nhân các câu hỏi lặp đi lặp lại.
* **Bước tốn thời gian/gây lỗi nhiều nhất:** Quá trình tìm kiếm thủ công trong tài liệu dài và việc HR phải trả lời lặp lại các câu hỏi cơ bản. 
  * *Thời gian xử lý ước tính:* ~15 - 20 phút cho mỗi lần tra cứu phức tạp; HR mất trung bình 2-3 giờ/ngày cho việc giải đáp thắc mắc chung.
* **Bước mà AI có thể tham gia giải quyết:** Xây dựng một Chatbot hỏi đáp thông minh dựa trên cơ sở tri thức nội bộ (RAG - Retrieval-Augmented Generation) để tự động đọc tài liệu và trả lời chính xác trích dẫn điều khoản cho người hỏi ngay lập tức.
* **Metric đo thành công có con số cụ thể:** Giảm 80% số lượng câu hỏi lặp lại gửi trực tiếp cho đội ngũ HR; thời gian nhân viên nhận được câu trả lời chính xác giảm từ 15 phút xuống dưới 30 giây.
* **Đề xuất kiến trúc sơ bộ:** LLM (Ứng dụng kiến trúc RAG kết hợp Vector Database).

---

### Quick Problem Card 3: Phân tích và phân loại tự động Feedback khách hàng
* **Tên bài toán và công ty thành viên:** Hệ thống phân tích tự động ý kiến phản hồi khách hàng - **Vinpearl**
* **Tác nhân đang gặp khó khăn (Actor/Operator):** Đội ngũ Chăm sóc khách hàng (CSKH) và Bộ phận Quản lý chất lượng dịch vụ.
* **Sơ đồ quy trình thủ công hiện tại:**
  1. Tổng hợp dữ liệu phản hồi từ nhiều kênh (email, ghi chú cuộc gọi tổng đài, đánh giá trên app, mạng xã hội).
  2. Nhân viên CSKH đọc thủ công từng phản hồi để gắn nhãn phân loại (vấn đề phòng ốc, thái độ nhân viên, dịch vụ F&B, thanh toán).
  3. Tổng hợp số liệu thủ công lên Excel hàng tuần để báo cáo ban quản lý.
  4. Trễ hạn trong việc phát hiện các khiếu nại khẩn cấp hoặc xu hướng phàn nàn nổi cộm.
* **Bước tốn thời gian/gây lỗi nhiều nhất:** Đọc, phân loại thủ công hàng nghìn dòng feedback và tổng hợp báo cáo tuần. 
  * *Thời gian xử lý ước tính:* Mất khoảng 4 - 6 giờ mỗi tuần cho việc tổng hợp và gắn nhãn dữ liệu.
* **Bước mà AI có thể tham gia giải quyết:** AI tự động phân tích độ cảm xúc (Sentiment Analysis), tự động phân loại chủ đề phàn nàn và gắn nhãn mức độ ưu tiên, đồng thời cảnh báo sớm các vấn đề nóng cho cấp quản lý.
* **Metric đo thành công có con số cụ thể:** Giảm thời gian tổng hợp báo cáo từ 5 giờ xuống còn 5 phút; thời gian phát hiện và chuyển tiếp phản hồi tiêu cực đến bộ phận xử lý giảm từ 24 giờ xuống dưới 1 giờ.
* **Đề xuất kiến trúc sơ bộ:** LLM / Agent (Phân tích ngữ nghĩa kết hợp tự động định tuyến ticket xử lý).
