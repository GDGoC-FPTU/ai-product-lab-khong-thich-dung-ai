# 03 — AI Log: Nhật Ký Chiêm Nghiệm về AI Thought-Partner

> **Deliverable cá nhân — Phase 6 (REFLECTION)**
> Ghi nhận trung thực quá trình tương tác với AI (Gemini / ChatGPT / Claude) trong suốt buổi Lab 02 hôm nay.

---

## 🤖 1. AI Giúp Gì Trong Buổi Lab Hôm Nay?

### 1.1. Brainstorm bài toán (Phase 1 — SCAN)

**Việc tôi đã làm:** Khi chưa nghĩ ra đủ 5 bài toán thực tế, tôi đã dùng prompt sau để brainstorm với Gemini:

```
Tôi là AI Engineer tại Vin Smart Future (Vingroup). Tôi đang tìm kiếm 
các pain point vận hành cụ thể có thể tối ưu bằng AI cho mảng Vinmec 
(Y Tế). Hãy gợi ý cho tôi 5 quy trình nghiệp vụ thủ công, tốn nhiều 
thời gian và gây rò rỉ hiệu suất, kèm con số thống kê ước tính về tổn thất.
```

**Kết quả hữu ích:** Gemini gợi ý nhanh 5 bài toán có con số cụ thể, trong đó bài toán Discharge Summary (20–30 phút/bệnh nhân) và phân loại lịch hẹn chuyên khoa là hai gợi ý chất lượng nhất. Tôi đã dùng chúng làm điểm khởi đầu rồi tự bổ sung chi tiết từ hiểu biết thực tế.

### 1.2. Stress-test Quick Problem Card (Phase 2)

Sau khi hoàn thiện Card #1 (Vinmec Discharge Summary), tôi paste nội dung vào Gemini với prompt CFO/Ops:

```
Đây là thẻ bài toán tôi đề xuất: [dán nội dung Card #1].
Hãy đóng vai một CFO và Trưởng phòng Vận hành cực kỳ khắt khe, 
chỉ ra 3 điểm yếu về logic, metric, và giải thích vì sao rule-based 
code thông thường có thể giải quyết bài toán này tốt hơn AI.
```

**Kết quả hữu ích:** Gemini phản biện đúng 2 điểm thật sự yếu: (1) metric "80% chấp nhận draft" quá mơ hồ — cần định nghĩa rõ "chỉnh sửa lớn là gì", (2) chưa giải thích tại sao rule-based template cứng không đủ. Tôi đã cải thiện cả hai điểm trong bản nộp cuối.

### 1.3. Viết System Prompt & Ranh giới (Phase 4)

Tôi dùng AI để draft SYSTEM_PROMPT cho prototype, yêu cầu AI giải thích lý do đằng sau từng ranh giới an toàn. Kết quả giúp nhóm hiểu sâu hơn về cơ chế jailbreak và cách phòng thủ.

### 1.4. Thiết kế Adversarial Test Cases

Tôi hỏi Gemini: *"Nếu bạn là hacker cố tình bypass ranh giới HITL của hệ thống AI y tế, bạn sẽ thử những câu prompt nào?"* — Đây là cách dùng AI để tấn công chính sản phẩm AI của mình nhằm tìm lỗ hổng.

---

## ❌ 2. AI Sai Gì? (Hallucination & Đề Xuất Không Phù Hợp)

### 2.1. Hallucination về con số thống kê Vinmec

**Vấn đề:** Khi tôi hỏi *"Vinmec xử lý bao nhiêu ca xuất viện mỗi ngày?"*, Gemini trả lời tự tin rằng **"Vinmec Times City xử lý 500 ca xuất viện/ngày"** kèm theo nguồn trích dẫn có vẻ hợp lý.

**Tại sao sai:** Con số này là **hallucination** — khi tôi kiểm tra lại với dữ liệu công khai từ báo cáo thường niên của Vinmec, con số thực tế gần hơn với 150–250 ca/ngày tại bệnh viện lớn nhất. Gemini đã "sáng tác" con số nghe có vẻ hợp lý mà không có nguồn thực.

**Tác hại tiềm tàng:** Nếu tôi dùng con số này trong báo cáo business impact mà không kiểm tra lại, ROI tính toán sẽ bị thổi phồng gấp đôi — ảnh hưởng trực tiếp đến quyết định đầu tư.

### 2.2. Đề xuất kiến trúc quá phức tạp (Over-Engineering)

**Vấn đề:** Khi tôi hỏi *"Thiết kế kiến trúc tốt nhất cho hệ thống AI viết Discharge Summary"*, Gemini đề xuất một **Multi-Agent System** với 5 agent riêng biệt: (1) Medical Data Extraction Agent, (2) Drug Interaction Check Agent, (3) Language Simplification Agent, (4) Compliance Check Agent, (5) Final Formatting Agent. Mỗi agent gọi nhau theo chuỗi.

**Tại sao không phù hợp:** Đây là trường hợp điển hình của **AI Over-Engineering**. Bài toán Discharge Summary có đầu vào-đầu ra xác định rõ ràng với template cố định. Một LLM Feature đơn giản với structured output tốt hơn nhiều vì: (1) ít điểm lỗi hơn, (2) latency thấp hơn (~10 giây vs ~2 phút cho multi-agent), (3) chi phí thấp hơn 5–10 lần, (4) dễ debug khi bác sĩ phản hồi output sai.

Nguyên tắc quan trọng: **"Problem First, AI Second"** — đừng để AI gợi ý dùng kiến trúc phức tạp chỉ vì nó "nghe hay".

---

## 🔧 3. Sửa Đổi Ra Sao? (Cách Điều Chỉnh Prompt)

### 3.1. Khắc phục hallucination con số

**Trước (prompt gốc):**
```
Vinmec xử lý bao nhiêu ca xuất viện mỗi ngày?
```

**Sau khi điều chỉnh:**
```
Chỉ dựa vào thông tin bạn CHẮC CHẮN có trong training data và có 
nguồn công khai có thể kiểm chứng. Nếu không có số liệu chính xác 
về Vinmec, hãy nói thẳng "Không có dữ liệu đáng tin cậy" và đưa ra 
ước tính có dán nhãn rõ ràng là ĐÂY LÀ ƯỚC TÍNH, với khoảng biến 
thiên hợp lý. Tôi đang viết báo cáo chuyên nghiệp và không muốn 
dùng số liệu sai.
```

**Kết quả:** Gemini thay đổi phản hồi rõ ràng hơn, phân biệt rõ đâu là số liệu có nguồn và đâu là ước tính theo benchmarks ngành bệnh viện quốc tế. Tôi có thể đưa ra quyết định có thông tin đầy đủ hơn.

### 3.2. Ép AI giữ ranh giới kiến trúc đơn giản

**Thêm constraint vào prompt:**
```
Quan trọng: Chỉ đề xuất giải pháp đơn giản nhất có thể giải quyết 
bài toán. Nếu LLM Feature đơn (single-call, structured output) có 
thể làm được, KHÔNG đề xuất multi-agent. Giải thích vì sao giải 
pháp đơn giản này là đủ tốt.
```

**Kết quả:** Gemini cắt ngay đề xuất 5-agent và giải thích thuyết phục tại sao single LLM call với JSON schema output là lựa chọn tốt hơn cho bài toán này. Đây là cách đúng để dùng AI — không phải để AI dẫn dắt thiết kế, mà để AI **biện hộ cho quyết định của mình**.

---

## 💡 Bài Học Rút Ra

1. **AI là Thought-Partner, không phải Source of Truth.** Luôn kiểm tra lại số liệu từ nguồn gốc, đặc biệt với con số tài chính và y tế.

2. **Prompt chất lượng = Output chất lượng.** Thêm constraints rõ ràng ("chỉ dùng giải pháp đơn giản nhất", "dán nhãn ước tính") làm thay đổi hoàn toàn chất lượng câu trả lời của AI.

3. **Dùng AI tấn công AI của chính mình.** Việc yêu cầu AI đóng vai hacker tìm cách bypass ranh giới là phương pháp stress-test hiệu quả nhất — miễn phí và nhanh hơn nhiều so với penetration testing truyền thống.

4. **Hallucination xảy ra nhiều nhất với số liệu cụ thể.** Hãy tăng độ hoài nghi khi AI đưa ra con số chính xác cho một tổ chức cụ thể mà bạn không thể kiểm chứng ngay lập tức.
