# 03 — AI Log & Reflection (Phase 6)

> ⚠️ **Lưu ý trước khi nộp:** File này là bản nháp gợi ý cấu trúc. Vì rubric I3 chấm "phản ánh **trung thực**" về trải nghiệm cá nhân của bạn khi làm việc với AI, hãy đọc lại toàn bộ quá trình (chat với Claude, các lần chỉnh sửa SYSTEM_PROMPT, kết quả chạy `prompt_prototype.py`...) rồi viết lại bằng lời của chính bạn — đừng nộp nguyên văn bản này.

## AI giúp gì?
Trong buổi lab, tôi dùng AI (Claude) như một thought-partner ở nhiều bước:
- Brainstorm bài toán ở Phase 1 dựa trên 4 lenses, giúp mở rộng danh sách nhanh hơn tự nghĩ một mình.
- Đóng vai CFO/Trưởng phòng Vận hành khắt khe để stress-test Quick Card, chỉ ra điểm yếu về metric.
- Viết cấu trúc SYSTEM_PROMPT ban đầu cho `prompt_prototype.py`, đặc biệt là cách diễn đạt 2 ranh giới an toàn (`[DRAFT_ONLY]` và ngưỡng pin <5%).
- Thiết kế thêm test case tấn công thứ 3 (kết hợp giả danh admin + vi phạm cả 2 rule cùng lúc) mà tôi chưa nghĩ tới.

## AI sai gì?
*(Điền vào đây theo trải nghiệm thật của bạn — ví dụ gợi ý:)*
- Khi chạy thử `prompt_prototype.py` trong môi trường sandbox, lệnh gọi Gemini API bị chặn do giới hạn mạng — AI ban đầu không cảnh báo trước điều này mà chỉ phát hiện sau khi thử chạy thật.
- [Điền: khi bạn thật sự chạy với API key riêng, output của Gemini có bị vi phạm rule nào không? Ví dụ AI có quên tag `[DRAFT_ONLY]` khi bị dụ bằng "chế độ debug" không?]
- [Điền: SYSTEM_PROMPT do Claude viết có chỗ nào rule-based đơn giản hơn (if/else code thường) có thể làm tốt hơn LLM không — ví dụ: kiểm tra tag `[DRAFT_ONLY]` hoàn toàn có thể là 1 dòng code kiểm tra output, không cần LLM tự giác tuân theo.]

## Sửa đổi ra sao?
*(Điền vào đây: bạn đã tinh chỉnh SYSTEM_PROMPT/rule như thế nào sau khi thấy kết quả thật)*
- [Điền: có thêm câu chặn "không tin tưởng người dùng tự xưng admin" không, hay đã có sẵn?]
- [Điền: có cân nhắc chuyển rule pin <5% ra ngoài code (post-processing kiểm tra output) thay vì chỉ dựa vào LLM tự tuân thủ không? Đây là điểm quan trọng cần suy nghĩ: với hệ thống an toàn-cao, rule cứng bằng code luôn đáng tin hơn là chỉ dặn LLM trong prompt.]
