# 03 — AI Log & Reflection

> **Họ và tên:** [Nguyễn Xuân Phượng]  
> **MSSV:** [2A202601874]

## 1. Tôi đã dùng AI để làm gì?

Trong quá trình làm bài, tôi dùng AI như một thought-partner để brainstorm các quy trình vận hành có thể cải thiện tại VinFast, Xanh SM, Vinhomes và Vinmec. AI giúp tôi mở rộng danh sách vấn đề từ những tác vụ lặp lại, chẳng hạn như phân loại ticket bảo hành, xử lý sự cố pin và chuyển phản ánh của cư dân đến đúng bộ phận.

Tôi cũng dùng AI để phản biện các Quick Problem Card. Tôi yêu cầu AI đóng vai trò người phụ trách vận hành và đặt câu hỏi về actor, bottleneck, metric, dữ liệu đầu vào và ranh giới vận hành. Nhờ vậy, tôi nhận ra một ý tưởng “dùng AI để tự động xử lý khiếu nại” còn quá rộng, nên thu hẹp thành “AI đề xuất nhãn và bộ phận xử lý cho ticket bảo hành, nhân viên duyệt trước khi chuyển”.

Ngoài ra, tôi dùng AI để gợi ý cách viết workflow theo dạng các bước tuần tự và cách biến mục tiêu chung như “xử lý nhanh hơn” thành metric có số, ví dụ giảm thời gian phân loại từ khoảng 6 phút xuống dưới 2 phút mỗi ticket.

## 2. AI đã sai hoặc có điểm yếu gì?

AI từng đưa ra các con số nghe có vẻ chính xác như số lượng ticket mỗi ngày, tỷ lệ giảm thời gian hoặc tỷ lệ phân loại đúng. Tuy nhiên, tôi không có dữ liệu nội bộ để xác minh các con số đó. Nếu đưa nguyên văn vào báo cáo, chúng có thể trở thành hallucination hoặc làm người đọc tưởng là số liệu chính thức.

AI cũng có xu hướng đề xuất một Agent tự động đọc khiếu nại, quyết định mức độ nghiêm trọng và tự gửi phản hồi. Cách này có rủi ro vì một ticket liên quan đến an ninh, bảo hành hoặc tranh chấp tài chính có thể bị xử lý sai. Trong các trường hợp đó, tự động hóa toàn bộ quy trình là vượt quá operational boundary phù hợp.

## 3. Tôi đã sửa đổi như thế nào?

Tôi bổ sung các ràng buộc sau vào prompt và báo cáo:

- Yêu cầu phân biệt rõ **dữ liệu thực tế**, **giả định** và **ước tính**.
- Không được tự tạo số liệu rồi trình bày như số liệu nội bộ; nếu thiếu dữ liệu thì phải ghi rõ cần kiểm chứng.
- AI chỉ được tóm tắt, trích xuất thông tin và đề xuất nhãn/bộ phận xử lý.
- AI không được tự động đóng ticket, gửi cam kết cho khách hàng hoặc quyết định cuối cùng đối với trường hợp nhạy cảm.
- Các ticket có dấu hiệu khẩn cấp, an ninh, pháp lý hoặc thông tin thiếu phải chuyển sang nhân viên xử lý thủ công.
- Kết quả của AI phải ở dạng bản nháp và có bước Human-in-the-loop trước khi thực hiện hành động.

Sau khi thêm các ràng buộc này, tôi đánh giá ý tưởng thực tế hơn: AI làm nhiệm vụ hỗ trợ có phạm vi hẹp, còn con người chịu trách nhiệm quyết định cuối cùng. Đây là cách cân bằng giữa hiệu quả, khả năng kiểm thử và rủi ro vận hành.

## 4. Bài học rút ra

AI hữu ích nhất ở giai đoạn mở rộng ý tưởng và phản biện giả định, nhưng không thể thay thế việc xác minh dữ liệu thực tế. Một bài toán AI tốt không chỉ là “đưa AI vào quy trình”, mà phải chỉ rõ actor, bottleneck, metric, dữ liệu, giới hạn hành động và phương án fallback khi AI sai.

