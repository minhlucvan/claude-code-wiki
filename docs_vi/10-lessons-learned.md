# Lessons Learned: những bài học khi xây AI tool ở mức production

> **Những đúc kết quan trọng từ việc thiết kế, xây dựng và triển khai Claude Code ở quy mô lớn**

## TLDR

- **Kiến trúc rất quan trọng**: abstraction tốt giúp phát triển nhanh hơn về sau
- **Hiệu năng là tính năng**: startup 600ms có giá trị thật với người dùng
- **Bảo mật là bắt buộc**: AST parsing cứu người dùng khỏi nhiều sai lầm nghiêm trọng
- **Quan sát hệ thống tiết kiệm thời gian**: có trace thì debug bằng phút, không có thì bằng ngày
- **Quy mô phơi bày sự thật**: pattern ổn ở prototype thường vỡ khi lên 10K user

## 1. Kiến trúc: nền móng quyết định rất nhiều

### Vấn đề đã gặp

Nếu dồn mọi thứ vào một khối query khổng lồ, việc kiểm thử, debug và mở rộng sẽ sớm trở nên đau đớn.

### Lời giải: kiến trúc phân lớp

Claude Code đi theo hướng phân tách:

- UI
- query engine
- tools
- services
- policy và integration

### Bài học

Code “nhanh để bắt đầu” thường chậm hơn rất nhiều khi cần duy trì lâu dài. Kiến trúc tốt không phải xa xỉ; nó là điều kiện để sản phẩm tiếp tục tiến hóa.

## 2. Hiệu năng: tốc độ là một tính năng

### Bài toán startup

Một công cụ dùng nhiều lần trong ngày mà khởi động chậm sẽ tạo ma sát rất lớn.

### Lời giải: prefetch song song và lazy loading

Không phải thứ gì cũng cần nạp ngay từ đầu. Cần phân biệt:

- cái gì quyết định cảm giác phản hồi ban đầu
- cái gì có thể nạp muộn
- cái gì nên được cache hoặc prefetch

### Bài học

Người dùng cảm nhận hiệu năng theo từng nhịp rất nhỏ. Một thiết kế “đẹp” nhưng chậm thường thua một thiết kế thực dụng mà nhanh.

## 3. Bảo mật: đừng mặc định điều gì cả

### Cú cảnh tỉnh

Khi tool có thể chạy shell hoặc đọc file, hậu quả của một quyết định sai không còn là bug nhỏ nữa.

### Lời giải: AST parsing

Security model phải hiểu lệnh ở mức cấu trúc, kết hợp permission và sandbox, thay vì hy vọng prompt sẽ đủ mạnh để model luôn ngoan.

### Bài học

Bảo mật không thể vá thêm ở cuối. Nó phải được đưa vào từ những ngày đầu, ngay trong cách hệ thống gọi tool.

## 4. Observability: debug trong vài phút, không phải vài ngày

### Kịch bản ác mộng

Người dùng báo “nó bị treo” nhưng không có trace, không có correlation ID, không biết lỗi ở model, tool hay UI.

### Bài học

Observability tốt không chỉ giúp sửa lỗi. Nó còn giúp đội ngũ tự tin rollout và cải tiến nhanh hơn.

## 5. Quy mô: pattern của prototype sẽ sớm lộ giới hạn

### Cú sốc khi lên 10K user

Mọi thứ tưởng ổn ở quy mô nhỏ có thể vỡ rất nhanh khi số phiên, số request và số người dùng tăng mạnh.

### Vấn đề 1: bùng nổ chi phí

Nếu không để ý token economics, multi-agent và context dài sẽ trở thành gánh nặng cực lớn.

### Vấn đề 2: cache thrashing

Cache chỉ có ích khi pattern sử dụng được thiết kế cho cache. Nếu không, overhead còn có thể cao hơn lợi ích.

### Vấn đề 3: permission fatigue

Xin phép quá nhiều khiến người dùng bực và mất cảnh giác. Security tốt phải đủ chặt nhưng cũng phải thực dụng.

## 6. Chiến lược cạnh tranh: lợi thế đến từ những quyết định sớm

### Những gì đã làm đúng từ đầu

- React trong terminal
- AST parsing cho shell
- fork cache cho multi-agent
- MCP hai vai trò

### Bài học

Những quyết định ban đầu nghe có vẻ đắt đỏ có thể trở thành lợi thế rất khó sao chép về sau.

## 7. Văn hóa kỹ thuật: điều gì thực sự hiệu quả

### 1. Prototype phải được thay thế

Prototype rất tốt để học, nhưng rất nguy hiểm nếu bị biến thành sản phẩm thật mà không tái cấu trúc.

### 2. Có ngân sách hiệu năng

Nếu không đặt ngưỡng cụ thể, hiệu năng sẽ xuống dốc dần mà không ai để ý.

### 3. Hơi “paranoid” về bảo mật là tốt

Với AI tool có quyền thực thi, thái độ cẩn trọng cao là hợp lý.

### 4. Observability trước

Đợi tới khi có lỗi mới thêm trace thì đã quá muộn.

## 8. Những sai lầm đã mắc

### 1. Quá nhiều tính năng

Thêm tính năng mới dễ hơn giữ hệ thống mạch lạc. Sự kỷ luật về phạm vi rất quan trọng.

### 2. Tài liệu chưa đủ

Khi hệ thống lớn lên, thiếu docs khiến kiến thức bị giữ trong đầu một vài người.

### 3. Tối ưu hóa quá sớm

Không phải tối ưu nào cũng đáng làm ngay. Cần phân biệt điểm nóng thật và điểm nóng tưởng tượng.

### 4. Feature flag ở khắp nơi

Feature flag hữu ích, nhưng nếu quá nhiều sẽ làm hệ thống khó suy luận và khó kiểm thử.

## 9. Những canh bạc lớn đã mang lại kết quả

### 1. React trong terminal

Giúp UX CLI bước sang một cấp khác.

### 2. AST parsing

Là nền tảng cho security model đủ nghiêm túc.

### 3. Prompt cache fork

Biến multi-agent từ thứ xa xỉ thành thứ dùng được hàng ngày.

### 4. Dual MCP

Mở cánh cửa cho rất nhiều tích hợp thay vì khóa sản phẩm trong một hệ kín.

## 10. Lời khuyên khi xây AI tool

### Cho startup

- Đừng cố làm tất cả cùng lúc
- Chọn một lợi thế thật sự và làm tới nơi
- Đầu tư sớm vào thứ khó sao chép

### Cho doanh nghiệp

- Quan tâm policy, audit, rollout và cost ngay từ đầu
- Đừng đánh giá công cụ AI chỉ theo demo
- Hãy nhìn cả hạ tầng vận hành phía sau

### Cho kỹ sư

- Hãy coi prompt chỉ là một phần của hệ thống
- Nút thắt thật thường nằm ở orchestration, state và UX
- Thiết kế cho khả năng debug ngay từ ngày đầu

## Kết luận: chơi đường dài

### Điều quan trọng trong năm đầu

- tìm ra abstraction đúng
- làm tốc độ đủ nhanh
- dựng nền bảo mật và quan sát hệ thống

### Điều quan trọng ở năm thứ ba

- mở rộng mà không vỡ
- kiểm soát chi phí
- giữ sản phẩm vẫn dễ tiến hóa

### Bài học cuối cùng

Điều làm nên một AI tool tốt không nằm ở một model mạnh hơn đôi chút, mà ở cách toàn bộ hệ thống được thiết kế để nhanh, an toàn, dễ mở rộng và dễ vận hành trong thời gian dài.
