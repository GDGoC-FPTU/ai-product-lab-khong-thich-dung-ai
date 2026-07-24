# Phase 6 — AI Log & Reflection

## AI giúp gì

Trong buổi lab, tôi đã sử dụng AI như một người đồng hành để:

- Brainstorm và lọc ra các bài toán thực tế thuộc Vingroup.
- Tạo prompt để kiểm tra giới hạn an toàn của mô hình.
- Tìm cách viết một system prompt chặt chẽ để điều khiển định dạng đầu ra.
- Hỗ trợ sửa nhanh các lỗi Python trong file prototype và rà soát logic kiểm thử.

## AI sai gì

Một điểm AI làm sai là khi tôi yêu cầu soạn chỉ dẫn cho tình huống pin cực thấp, mô hình có xu hướng nhấn vào việc gợi ý trạm sạc gần nhất mà bỏ qua rủi ro khi xe đã ở mức pin dưới 5%. Đây là một dạng sai lệch ở cấp độ ranh giới vận hành. Nếu không có prompt chặt chẽ, AI dễ xem nhẹ điều kiện an toàn.

## Sửa đổi ra sao

Tôi đã cải thiện prompt bằng cách:

- Bắt buộc đầu ra bắt đầu bằng `[DRAFT_ONLY]`.
- Chỉ định rõ khi pin dưới 5% thì không được gợi ý trạm sạc xa hơn 5km.
- Tạo output JSON rõ ràng cho trường hợp dispatch mobile charger.
- Thêm các test case adversarial để ép mô hình phải tuân thủ các quy tắc này.

Kết luận: AI rất hữu ích như công cụ hỗ trợ tư duy, nhưng nếu không được ràng buộc bằng prompt và kiểm thử sau đó, các quyết định an toàn có thể bị vượt quá giới hạn.
