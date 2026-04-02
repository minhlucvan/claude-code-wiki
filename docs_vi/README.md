# Claude Code Wiki

> **Bản tiếng Việt của bộ tài liệu phân tích kiến trúc, mẫu thiết kế và các lợi thế kỹ thuật của Claude Code**

## Wiki này bao quát những gì?

`Claude Code Wiki` là bộ tài liệu tổng hợp nhằm giải thích Claude Code được thiết kế như thế nào, vì sao nó cho trải nghiệm tốt hơn nhiều công cụ AI coding khác, và những mẫu kỹ thuật nào đáng học lại. Trọng tâm của bộ wiki này gồm:

- **Kiến trúc và pattern**: cách streaming execution, context management và multi-agent orchestration hoạt động trong thực tế
- **Góc nhìn kỹ thuật**: những quyết định triển khai thông minh ẩn trong codebase hơn 512K dòng
- **Phân tích cạnh tranh**: 10 điểm khác biệt rõ nhất giữa Claude Code với Cursor, Continue và Aider
- **Kỹ thuật production**: những pattern có thể áp dụng lại khi tự xây công cụ AI
- **Bài viết chuyên sâu**: từng subsystem chính đều có một bài giải thích riêng

## Vì sao nên nghiên cứu kiến trúc Claude Code?

Claude Code là một ví dụ rất rõ của **AI tooling ở cấp độ production**. Khi mổ xẻ kiến trúc của nó, bạn có thể học được:

1. Cách xây cơ chế chạy tool theo thời gian thực, thay vì chỉ request rồi chờ phản hồi
2. Cách xử lý hội thoại dài bằng pipeline nén ngữ cảnh 5 lớp
3. Cách điều phối nhiều AI agent nhưng vẫn tận dụng được cache chung
4. Cách làm giao diện terminal chuyên nghiệp bằng React + Ink
5. Cách áp dụng bảo mật đủ chặt cho môi trường thực thi code

**Đây không chỉ là một AI coding assistant nữa**. Nó được xây bởi chính đội ngũ phát triển Claude, nên có lợi thế về quyền truy cập API nội bộ, mô hình tối ưu hóa prompt và cách tổ chức hệ thống mà phần lớn đối thủ khó sao chép nguyên vẹn.

## Điều hướng nhanh

### Những cải tiến cốt lõi

1. **[Competitive Advantages](./01-competitive-advantages.md)** 🔥
   - 10 lợi thế mà đối thủ khó bắt chước
   - Vì sao từng cải tiến lại quan trọng ngoài thực tế
   - Những gì có thể học và áp dụng lại

### Các bài đi sâu về kiến trúc

2. **[Architecture Overview](./02-architecture-overview.md)**
   - Toàn cảnh thiết kế hệ thống và luồng dữ liệu
   - Các subsystem chính và vai trò của từng phần
   - Phân tích stack công nghệ

3. **[Streaming Execution](./03-streaming-execution.md)**
   - Cách tool được chạy song song khi LLM còn đang stream
   - Lý do UX nhanh hơn 2-5 lần so với mô hình tuần tự
   - Cấu trúc triển khai ở mức kỹ thuật

4. **[Context Management](./04-context-management.md)**
   - Pipeline 5 lớp để duy trì hội thoại dài
   - Cách autocompaction hoạt động
   - Kinh tế token và prompt cache

5. **[Multi-Agent Orchestration](./05-multi-agent-orchestration.md)**
   - 6 loại agent chuyên biệt
   - Mô hình fork cache để giảm chi phí
   - Coordinator mode cho workflow song song

### UX và tích hợp

6. **[Terminal UX](./06-terminal-ux.md)**
   - Vì sao React trong CLI là một quyết định rất đúng
   - Kiến trúc component và cách quản lý state
   - Cách hơn 85 slash command được tổ chức

7. **[Security Model](./07-security-model.md)**
   - Phân tích Bash ở mức AST, không chỉ regex
   - Hệ thống quyền và wildcard rule
   - Sandbox, audit trail và enterprise policy

8. **[Integration Ecosystem](./08-integration-ecosystem.md)**
   - MCP hai vai trò: vừa client vừa server
   - Tích hợp IDE với VS Code và JetBrains
   - Plugin, skill và bridge mode

### Kỹ thuật production

9. **[Production Engineering](./09-production-engineering.md)**
   - Tối ưu khởi động và prefetch song song
   - Feature flag, dead code elimination
   - Quan sát hệ thống, cost tracking và fleet management

10. **[Lessons Learned](./10-lessons-learned.md)**
    - 10 bài học đáng lấy nhất
    - Những pattern đáng “mượn”
    - Trade-off và quyết định kiến trúc

## So sánh nhanh với đối thủ

| Tính năng | Claude Code | Cursor | Continue | Aider |
|---------|-------------|--------|----------|-------|
| **Streaming Tool Execution** | ✅ Song song | ❌ Tuần tự | ❌ Tuần tự | ❌ Tuần tự |
| **Context Management** | ✅ Tự nén 5 lớp | ⚠️ Cắt bớt cơ bản | ⚠️ Cắt bớt cơ bản | ⚠️ Thủ công |
| **Multi-Agent** | ✅ Có sẵn, chia sẻ cache | ❌ Không | ❌ Không | ⚠️ Hạn chế |
| **Security** | ✅ AST + quyền | ⚠️ Prompt cơ bản | ⚠️ Prompt cơ bản | ⚠️ Chờ duyệt |
| **Terminal UI** | ✅ React/Ink | N/A | N/A | ⚠️ Cơ bản |
| **MCP Support** | ✅ Client + Server | ⚠️ Client | ⚠️ Client | ❌ Không |
| **Prompt Caching** | ✅ Tối ưu fork | ⚠️ Cơ bản | ⚠️ Cơ bản | ❌ Không |
| **IDE Integration** | ✅ Bridge mode | ✅ Có sẵn | ✅ Có sẵn | ❌ CLI-only |

**Chú thích**: ✅ Nâng cao • ⚠️ Cơ bản • ❌ Không có

## Số liệu đáng chú ý

| Chỉ số | Giá trị |
|--------|-------|
| **Tổng số dòng mã** | ~512.000 |
| **Số file TypeScript** | ~1.900 |
| **Tool tích hợp** | 40+ |
| **Slash command** | 85+ |
| **Loại agent** | 6 loại |
| **Runtime** | Bun |
| **UI Framework** | React + Ink |

## Đọc wiki này như thế nào?

**Nếu bạn đang xây công cụ AI:**
- Bắt đầu từ [Competitive Advantages](./01-competitive-advantages.md)
- Sau đó đọc [Lessons Learned](./10-lessons-learned.md)
- Rồi đào sâu vào subsystem mình quan tâm

**Nếu bạn đang đánh giá AI coding assistant:**
- Xem [Competitive Advantages](./01-competitive-advantages.md) để hiểu khác biệt
- Đọc [Architecture Overview](./02-architecture-overview.md) để đánh giá độ production
- Kiểm tra [Security Model](./07-security-model.md) nếu bạn quan tâm bảo mật doanh nghiệp

**Nếu bạn muốn học TypeScript/React nâng cao:**
- Đọc [Terminal UX](./06-terminal-ux.md) cho pattern React trong CLI
- Đọc [Production Engineering](./09-production-engineering.md) cho kỹ thuật tối ưu
- Đọc [Context Management](./04-context-management.md) để xem cách quản lý state/ngữ cảnh ở quy mô lớn

## Ghi chú phương pháp

Bản phân tích này được xây trên:

- Mã nguồn lấy từ npm source map của Claude Code, thời điểm tháng 3/2026
- Quá trình tự khám phá và thử nghiệm tính năng
- So sánh đối chiếu với Cursor, Continue và Aider

Đây là tài liệu sống, được tạo ra để ghi lại những “wow moment” trong kiến trúc và những bài học thực tế có thể tái sử dụng.

---

**Bắt đầu từ đâu?** Hãy đọc [🔥 Competitive Advantages](./01-competitive-advantages.md) trước để có bức tranh tổng quát nhất.
