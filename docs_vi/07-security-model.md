# Security Model: phòng thủ nhiều lớp

> **Cách Claude Code bảo vệ người dùng bằng AST parsing, permission, sandbox và control cho môi trường doanh nghiệp**

## TLDR

- Parse Bash ở mức AST để phát hiện lệnh nguy hiểm bị ngụy trang
- Hệ thống permission có nhiều chế độ, từ tương tác đến tự động
- Hỗ trợ wildcard rule để kiểm soát linh hoạt
- Có MDM policy cho triển khai doanh nghiệp
- Có sandbox để cô lập thực thi
- Mô hình zero-trust: thao tác nào cũng phải được xem xét

## Vấn đề: LLM là bề mặt tấn công mới

AI coding assistant có khả năng:

- chạy lệnh shell
- đọc file nhạy cảm
- sửa file hàng loạt
- kết nối công cụ ngoài

Nếu không có security model thực sự, các tình huống nguy hiểm rất dễ xảy ra:

- prompt injection
- chạy nhầm lệnh phá hoại
- rò rỉ dữ liệu
- leo thang quyền truy cập

## Lời giải của Claude Code: phòng thủ nhiều lớp

Claude Code không đặt niềm tin hoàn toàn vào:

- model
- prompt
- người dùng
- tool

Thay vào đó, nó ghép nhiều lớp bảo vệ:

- phân tích lệnh
- permission rule
- sandbox
- enterprise policy
- auditability

## Đi sâu vào kiến trúc

### 1. Phân tích Bash ở mức AST

Đây là lớp quan trọng nhất. Lệnh không bị đánh giá như một chuỗi text đơn thuần mà được parse thành cấu trúc shell thực sự.

Nhờ vậy hệ thống có thể thấy:

- command substitution
- path traversal bị che giấu
- chuỗi lệnh lồng nhau
- biến thể dùng quote hoặc expansion để đánh lừa regex

### 2. Phân tích an ninh

Sau khi có AST, hệ thống tiếp tục đánh giá:

- lệnh đang chạm tới đâu
- có hành vi xóa hay ghi không
- có truy cập tài nguyên nhạy cảm không
- có dấu hiệu exfiltration không

### 3. Hệ thống permission

Permission không chỉ có kiểu “cho” hoặc “không cho”. Thường sẽ có nhiều chế độ, ví dụ:

- hỏi người dùng cho từng thao tác
- cho phép một số nhóm lệnh an toàn
- chạy tự động trong sandbox
- mức tự động cao hơn với rule đã được duyệt

### 4. Wildcard rule

Với sản phẩm doanh nghiệp, rule phải đủ thực dụng. Wildcard cho phép định nghĩa pattern như:

- cho đọc thư mục dự án
- chặn thư mục hệ thống
- cho phép một số command family nhất định

### 5. MDM policy

Ở quy mô tổ chức, cài đặt cục bộ là chưa đủ. Cần có policy phân phối tập trung để:

- ép mode bảo mật
- chặn một số hành vi
- thống nhất trải nghiệm giữa các máy

### 6. Sandbox execution

Sandbox là lớp “nếu có vấn đề thì thiệt hại vẫn bị giới hạn”. Nó giảm rủi ro khi agent cần chạy command mà vẫn phải giữ biên an toàn.

## Ngăn chặn tấn công thực tế

### Ví dụ 1: lệnh nguy hiểm bị ngụy trang

Một lệnh nhìn bề ngoài có vẻ vô hại có thể che path traversal hoặc shell expansion nguy hiểm. AST parsing giúp bóc lớp ngụy trang này.

### Ví dụ 2: data exfiltration

Những pipeline kiểu đọc khóa riêng tư rồi gửi ra ngoài là thứ phải bị phát hiện từ sớm.

### Ví dụ 3: privilege escalation

Nếu command chạm tới vùng vượt ra ngoài workspace hoặc cố leo lên thư mục cha, đó là tín hiệu phải kiểm soát chặt.

### Ví dụ 4: prompt injection

Người dùng hoặc nội dung trong repo có thể cố lừa agent làm điều không nên làm. Security model tốt sẽ không dựa hoàn toàn vào việc “model tự biết từ chối”.

## Phân tích cạnh tranh

### Cách tiếp cận bảo mật

- Nhiều công cụ dựa mạnh vào prompt
- Một số công cụ dựa vào yêu cầu người dùng xác nhận
- Claude Code bổ sung tầng phân tích cấu trúc lệnh và policy enforcement, nên phòng thủ sâu hơn

### Khả năng ngăn chặn tấn công

Sự khác biệt lớn nhất là Claude Code hiểu shell tốt hơn. Đó là nền tảng để chặn các kiểu bypass tinh vi, không chỉ các mẫu quá lộ liễu.

## Những điểm “wow”

### 1. Parser rất khó lách

Đây là kiểu bảo vệ làm tăng chất lượng toàn hệ thống, không chỉ một tính năng riêng.

### 2. Chống được các biến thể chưa biết trước

Khi hiểu cấu trúc AST, hệ thống bớt phụ thuộc vào danh sách pattern hữu hạn.

### 3. Có dấu vết kiểm tra

Audit trail giúp cả người dùng lẫn doanh nghiệp hiểu điều gì đã được phép và điều gì bị chặn.

## Điều rút ra

- Bảo mật cho AI tool không thể chỉ là “hãy cẩn thận”
- AST parsing là khoản đầu tư đắt nhưng đáng giá
- Permission, sandbox và policy phải đi cùng nhau mới tạo thành một mô hình phòng thủ đủ mạnh
