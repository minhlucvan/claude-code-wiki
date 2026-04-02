<div align="center">
  <img src="./assets/banner.svg" alt="Claude Code Wiki" width="100%">
</div>

# Claude Code Wiki

> **Cẩm nang đầy đủ về kiến trúc, các mẫu thiết kế và những điểm vượt trội của Claude Code. Tìm hiểu cách nó đạt tốc độ thực thi nhanh hơn 2-5 lần, bộ nhớ hội thoại gần như không giới hạn và giảm tới 90% chi phí.**

[English](./README.md) | **Tiếng Việt** | [中文](./README.zh.md) | [Español](./README.es.md) | [日本語](./README.ja.md)

## Đây là gì?

**Claude Code Wiki** là tài liệu đầy đủ nhất để tìm hiểu cách Claude Code được thiết kế, cách nó vận hành trong thực tế, và vì sao nó có lợi thế rõ rệt so với nhiều đối thủ khác. Dựa trên quá trình phân tích **512.000 dòng TypeScript production**, bộ wiki này chỉ ra:

- **10 cải tiến kiến trúc** giúp Claude Code vượt trội hơn các công cụ cùng loại
- **Cơ chế chạy tool theo luồng streaming**: tool được thực thi ngay khi LLM còn đang sinh phản hồi, giúp trải nghiệm nhanh hơn 2-5 lần
- **Hệ thống quản lý ngữ cảnh 5 lớp** cho phép duy trì hội thoại dài mà không bị bí bộ nhớ
- **Điều phối đa tác tử (multi-agent)** có chia sẻ cache, giúp **giảm tới 90% chi phí**
- **Giao diện terminal viết bằng React** cho trải nghiệm CLI ở mức production
- **Bảo mật ở mức AST** để phân tích lệnh sâu, thay vì chỉ dựa vào regex
- **Các mẫu kỹ thuật production** được tối ưu cho vận hành quy mô lớn

**Đây không chỉ là thêm một công cụ AI để viết code**. Nó được xây dựng bởi chính đội ngũ tạo ra Claude, với quyền truy cập API first-party và những cơ hội tối ưu mà phần lớn đối thủ không có.

## Bắt đầu nhanh & Câu hỏi thường gặp

**Mới tìm hiểu wiki?** Bắt đầu tại đây để có câu trả lời nhanh về kiến trúc Claude Code:

### Hiểu về Kiến trúc

- **Điểm khác biệt là gì?** → 10 cải tiến: streaming execution, autocompaction, cache fork, React CLI, AST security
- **Cấu trúc tổ chức?** → Nhiều lớp: UI (React) → Commands (85) → Query Engine → Tools (40+) → Services
- **Tại sao React cho CLI?** → UI declarative, tái sử dụng component, quản lý state dễ hơn

### Câu hỏi Kỹ thuật Chính

- **Streaming execution hoạt động thế nào?** → Tools chạy song song trong khi LLM stream (nhanh hơn 2-5x)
- **Autocompaction hoạt động thế nào?** → 5 lớp tự động tóm tắt tin nhắn cũ (tiết kiệm 85% chi phí)
- **Cache fork pattern là gì?** → Agents chia sẻ cached context (giảm 90% chi phí cho multi-agent)
- **AST parsing cải thiện bảo mật như thế nào?** → Phân tích Bash sâu phát hiện lệnh nguy hiểm regex bỏ sót
- **Tại sao 6 specialized agents?** → Agents chuyên biệt hiệu quả hơn 3x (ví dụ: Explore agent cho tìm kiếm codebase)

📚 **[Đọc FAQ đầy đủ](./docs/FAQ.md)** | **[Phân tích Kiến trúc chi tiết](./docs_vi/)** | **[Áp dụng các Mẫu này](./docs_vi/10-lessons-learned.md)**

## Vì sao wiki này tồn tại?

Wiki này được tạo ra để ghi lại những quyết định kiến trúc và các mẫu triển khai production đã làm nên chất lượng của Claude Code. Đây cũng là nơi để thấy rõ cách nó giải quyết những bài toán khó mà nhiều công cụ khác vẫn còn lúng túng:

- **Tốc độ**: Phần lớn công cụ sẽ đợi LLM trả lời xong rồi mới chạy tool theo kiểu tuần tự. Claude Code chạy tool song song ngay trong lúc streaming, nên các thao tác nhiều tool nhanh hơn 2-5 lần.
- **Bộ nhớ**: Nhiều đối thủ chỉ cắt bớt context đơn giản hoặc buộc người dùng phải tự dọn hội thoại. Claude Code dùng pipeline autocompaction 5 lớp để duy trì hội thoại rất dài.
- **Chi phí**: Vận hành nhiều agent thường rất tốn. Claude Code dùng mô hình fork cache để chia sẻ cache giữa các agent, nhờ đó giảm được khoảng 90% chi phí.
- **Bảo mật**: Nhiều công cụ chỉ dùng regex để phân tích lệnh. Claude Code phân tích Bash ở mức AST để đánh giá rủi ro chính xác hơn nhiều.
- **Quy mô**: Hệ thống được thiết kế theo tư duy vận hành ở cấp độ tổ chức, tối ưu cho bài toán Gtok/tuần.

Wiki này ghi lại các mẫu thiết kế và kỹ thuật đó để bạn có thể học, đối chiếu và áp dụng vào các công cụ AI của riêng mình.

## Bạn sẽ học được gì?

### 🚀 Những cải tiến cốt lõi

1. **Streaming Tool Execution** - Cách chạy tool song song trong khi LLM vẫn đang stream phản hồi
2. **Context Management** - Pipeline 5 lớp để duy trì hội thoại dài với cơ chế autocompaction
3. **Multi-Agent Orchestration** - Hệ thống 6 agent chuyên biệt với kiến trúc chia sẻ cache
4. **Prompt Cache Optimization** - Mô hình fork giúp giảm tới 90% chi phí giữa các agent
5. **React Terminal UI** - Kiến trúc component đạt chuẩn production cho công cụ CLI

### 🔒 Kỹ thuật production

6. **AST-Level Security** - Phân tích sâu lệnh Bash và hệ thống phân quyền
7. **Feature Flags** - Loại bỏ dead code để không phát sinh chi phí runtime
8. **Startup Optimization** - Các mẫu prefetch song song và lazy loading
9. **Integration Ecosystem** - MCP hai vai trò (client + server), cầu nối IDE, hệ thống skill
10. **Fleet-Scale Thinking** - Tối ưu chi phí ở cấp độ tổ chức (tiết kiệm Gtok/tuần)

### 📊 So sánh năng lực cạnh tranh

| Tính năng | Claude Code | Cursor | Continue | Aider |
|---------|-------------|--------|----------|-------|
| **Streaming Tool Execution** | ✅ Song song | ❌ Tuần tự | ❌ Tuần tự | ❌ Tuần tự |
| **Context Management** | ✅ Autocompaction 5 lớp | ⚠️ Cắt ngữ cảnh cơ bản | ⚠️ Cắt ngữ cảnh cơ bản | ⚠️ Thủ công |
| **Multi-Agent** | ✅ Tích hợp sẵn, có chia sẻ cache | ❌ Không | ❌ Không | ⚠️ Hạn chế |
| **Security** | ✅ Phân tích AST + phân quyền | ⚠️ Prompt cơ bản | ⚠️ Prompt cơ bản | ⚠️ Chờ người dùng duyệt |
| **Terminal UI** | ✅ React/Ink (đầy đủ) | N/A (IDE) | N/A (IDE) | ⚠️ CLI cơ bản |
| **MCP Support** | ✅ Vừa client vừa server | ⚠️ Chỉ client | ⚠️ Chỉ client | ❌ Không |
| **Prompt Caching** | ✅ Tối ưu theo mô hình fork | ⚠️ Cơ bản | ⚠️ Cơ bản | ❌ Không |

**Chú thích**: ✅ Nâng cao • ⚠️ Cơ bản • ❌ Không có

## Cấu trúc wiki

```text
claude-code-wiki/
├── docs/                           # Bộ tài liệu gốc tiếng Anh
│   ├── README.md                   # Điều hướng và tổng quan
│   ├── 01-competitive-advantages.md   # 10 lợi thế vượt trội
│   ├── 02-architecture-overview.md    # Thiết kế hệ thống và luồng dữ liệu
│   ├── 03-streaming-execution.md      # Thực thi tool theo thời gian thực
│   ├── 04-context-management.md       # Pipeline ngữ cảnh 5 lớp
│   ├── 05-multi-agent-orchestration.md # Hệ thống multi-agent
│   ├── 06-terminal-ux.md              # Giao diện terminal với React
│   ├── 07-security-model.md           # Phân tích AST và phân quyền
│   ├── 08-integration-ecosystem.md    # MCP, cầu nối IDE, skill
│   ├── 09-production-engineering.md   # Các mẫu tối ưu production
│   └── 10-lessons-learned.md          # Những bài học rút ra
├── docs_vi/                        # Bộ tài liệu tiếng Việt
│   ├── README.md                   # Điều hướng và tổng quan
│   └── ...
└── claude-code/                    # Toàn bộ mã nguồn (512K LOC)
    ├── src/                        # Phần triển khai bằng TypeScript
    ├── skills/                     # Hơn 85 slash command
    └── package.json                # Dependency và script
```

## Hướng dẫn bắt đầu nhanh

Hãy chọn đường đọc phù hợp với mục tiêu của bạn:

### 🎯 Nếu bạn đang xây dựng công cụ AI hỗ trợ lập trình

**Bắt đầu từ đây**: [Competitive Advantages](./docs_vi/01-competitive-advantages.md)

Bạn sẽ thấy 10 cải tiến kiến trúc nổi bật:
- Thực thi tool theo kiểu streaming để UX nhanh hơn 2-5 lần
- Điều phối multi-agent có chia sẻ cache
- Quản lý ngữ cảnh cho các cuộc hội thoại rất dài
- Tối ưu bảo mật và chi phí ở mức production

**Sau đó đọc tiếp**: [Lessons Learned](./docs_vi/10-lessons-learned.md) để lấy các bài học có thể áp dụng ngay vào công cụ của chính bạn.

### 🔍 Nếu bạn đang đánh giá Claude Code

**Bắt đầu từ đây**: [Architecture Overview](./docs_vi/02-architecture-overview.md)

Phần này giúp bạn nắm được thiết kế hệ thống và mức độ sẵn sàng để dùng trong production:
- Kiến trúc tổng thể và luồng dữ liệu
- Các hệ thống lõi và trách nhiệm của từng phần
- Phân tích stack công nghệ (Bun, React, TypeScript)

**Nên đọc thêm**:
- [Security Model](./docs_vi/07-security-model.md) nếu bạn quan tâm tới yêu cầu doanh nghiệp
- [Integration Ecosystem](./docs_vi/08-integration-ecosystem.md) nếu bạn cần khả năng mở rộng

### 💡 Nếu bạn muốn học các mẫu thiết kế nâng cao

**Bắt đầu từ đây**: [Lessons Learned](./docs_vi/10-lessons-learned.md)

Bạn sẽ tìm thấy nhiều mẫu thực chiến cho TypeScript/React ở môi trường production:
- Kiến trúc React trong CLI
- Quản lý state ở quy mô lớn
- Các kỹ thuật tối ưu chi phí
- Tư duy kỹ thuật cho hệ thống vận hành quy mô lớn

**Sau đó đào sâu thêm**:
- [Terminal UX](./docs_vi/06-terminal-ux.md) để xem các mẫu React/Ink
- [Production Engineering](./docs_vi/09-production-engineering.md) để xem các kỹ thuật tối ưu

## Chỉ mục wiki

| Bài viết | Mô tả | Chủ đề chính |
|-------|-------------|------------|
| [01. Competitive Advantages](./docs_vi/01-competitive-advantages.md) | 10 cải tiến tạo nên khác biệt của Claude Code | Streaming execution, tối ưu cache, bảo mật AST |
| [02. Architecture Overview](./docs_vi/02-architecture-overview.md) | Thiết kế hệ thống và luồng dữ liệu | Hệ thống lõi, stack công nghệ, kiến trúc production |
| [03. Streaming Execution](./docs_vi/03-streaming-execution.md) | Cách tool chạy song song khi LLM đang stream | Điều phối async, xử lý lỗi, tăng tốc 2-5 lần |
| [04. Context Management](./docs_vi/04-context-management.md) | Pipeline 5 lớp cho hội thoại dài | Autocompaction, prompt caching, tối ưu bộ nhớ |
| [05. Multi-Agent Orchestration](./docs_vi/05-multi-agent-orchestration.md) | 6 agent chuyên biệt có chia sẻ cache | Mô hình fork, chế độ coordinator, các loại agent |
| [06. Terminal UX](./docs_vi/06-terminal-ux.md) | Kiến trúc UI terminal bằng React | Thiết kế component, quản lý state, hơn 85 command |
| [07. Security Model](./docs_vi/07-security-model.md) | Phân tích Bash ở mức AST và hệ phân quyền | Phân tích lệnh, tích hợp sandbox, mô hình đe doạ |
| [08. Integration Ecosystem](./docs_vi/08-integration-ecosystem.md) | MCP, cầu nối IDE và hệ thống skill | MCP hai vai trò, VS Code/JetBrains, skill điều kiện |
| [09. Production Engineering](./docs_vi/09-production-engineering.md) | Các mẫu tối ưu và tư duy vận hành quy mô lớn | Tốc độ khởi động, feature flag, tối ưu chi phí |
| [10. Lessons Learned](./docs_vi/10-lessons-learned.md) | Những bài học đáng lấy nhất | Insight thực thi, quyết định thiết kế, trade-off |

## Các số liệu đáng chú ý

| Chỉ số | Giá trị |
|--------|-------|
| **Tổng số dòng mã** | ~512.000 |
| **Số file TypeScript** | ~1.900 |
| **Tool tích hợp sẵn** | 40+ |
| **Slash command** | 85+ |
| **Loại agent** | 6 loại chuyên biệt |
| **Runtime** | Bun (hiệu năng cao) |
| **UI Framework** | React + Ink |
| **Số trang wiki** | 10 bài chuyên sâu |

## Wiki này dành cho ai?

### Nhà phát triển đang xây công cụ AI hỗ trợ viết code

Tìm hiểu các mẫu production cho streaming execution, context management và multi-agent orchestration. Xem cách Claude Code đạt UX nhanh hơn 2-5 lần và cắt giảm tới 90% chi phí.

### Đội ngũ sản phẩm đang đánh giá công cụ AI

So sánh cách tiếp cận kiến trúc giữa Claude Code, Cursor, Continue và Aider. Hiểu rõ những lợi thế cạnh tranh đo được về tốc độ, chi phí và năng lực.

### Kỹ sư muốn học TypeScript/React ở mức nâng cao

Khám phá cách đưa React vào CLI, quản lý state ở quy mô lớn, và các mẫu tối ưu production rút ra từ một codebase 512K LOC.

### Kiến trúc sư kỹ thuật

Nghiên cứu các quyết định thiết kế hệ thống, kiến trúc bảo mật và những mẫu kỹ thuật dành cho công cụ AI production ở quy mô lớn.

## Phương pháp xây dựng wiki

Wiki này được xây dựng dựa trên:

- **Phân tích đầy đủ mã nguồn** từ source map của gói npm Claude Code (tháng 3 năm 2026)
- **Khảo sát và kiểm thử thực tế** các tính năng chính
- **Nghiên cứu đối chiếu** với kiến trúc của Cursor, Continue và Aider
- **Điều tra ở cấp độ mã nguồn** trên 512.000 dòng TypeScript
- **Rút trích mẫu thiết kế** từ comment, kiểu dữ liệu và chi tiết triển khai

Toàn bộ tài liệu đều được rút ra từ mã nguồn thật, không dựa vào tài liệu marketing hay kiểm thử kiểu hộp đen.

## Đóng góp cho wiki

Bạn phát hiện thêm điều thú vị? Có góc nhìn nào đáng bổ sung? Wiki này là một tài liệu sống, được tạo ra để ghi lại:

- Những khoảnh khắc "à ha" trong kiến trúc hệ thống
- Các mẫu thực tiễn có thể áp dụng khi xây công cụ AI
- Các quyết định thiết kế và trade-off đi kèm
- Những khác biệt cạnh tranh đáng chú ý

Issue và pull request đều được chào đón cho các nội dung như:
- Bổ sung tài liệu hoặc sửa lỗi
- Khám phá mới trong codebase
- Giải thích mẫu thiết kế và ví dụ minh hoạ
- So sánh thêm với các công cụ khác

## Giấy phép và ghi nhận

**Mã nguồn**: Claude Code là phần mềm độc quyền của Anthropic. Wiki này chỉ phục vụ mục đích giáo dục.

**Nội dung wiki**: Tài liệu và phần phân tích © 2026. Được chia sẻ cho mục đích học thuật và nghiên cứu.

**Phương pháp**: Mã nguồn được trích xuất từ source map npm và được tài liệu hoá thông qua code review, không phải reverse engineering.

---

**Sẵn sàng khám phá?** Hãy bắt đầu với [🔥 Competitive Advantages](./docs_vi/01-competitive-advantages.md) để xem 10 cải tiến làm nên sự khác biệt của Claude Code.
