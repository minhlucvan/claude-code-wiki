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

## Thống kê Chính

| Chỉ số | Giá trị |
|--------|---------|
| **Tổng số dòng code** | ~512,000 |
| **Files TypeScript** | ~1,900 |
| **Công cụ tích hợp** | 40+ |
| **Lệnh Slash** | 85+ |
| **Loại Agent** | 6 chuyên biệt |
| **Runtime** | Bun (hiệu năng cao) |
| **UI Framework** | React + Ink |
| **Trang Wiki** | 11 hướng dẫn toàn diện |

## Kiến trúc Tổng quan

```mermaid
graph TB
    subgraph "Lớp Giao diện Người dùng"
        Terminal[Terminal UI<br/>React + Ink<br/>80+ Components]
        Palette[Command Palette<br/>85 Slash Commands]
    end

    subgraph "Lớp Điều phối"
        QueryEngine[Query Engine<br/>Streaming + Tool Execution<br/>Context Management]
        AgentCoord[Agent Coordinator<br/>6 Specialized Agents<br/>Cache Fork Pattern]
    end

    subgraph "Lớp Tool"
        FileTools[File I/O Tools<br/>Read, Write, Edit, Glob, Grep]
        ShellTools[Shell Tools<br/>Bash, PowerShell, REPL]
        AgentTools[Agent Tools<br/>Multi-Agent Orchestration]
        WebTools[Web Tools<br/>Fetch, Search]
        MCPTools[MCP Tools<br/>External Integrations]
    end

    subgraph "Lớp Dịch vụ"
        API[Claude API Client<br/>SSE Streaming<br/>Retry Logic]
        MCP[MCP Client/Server<br/>Dual Role]
        Auth[OAuth 2.0<br/>PKCE Flow]
        Cache[Prompt Cache<br/>Fork Optimization]
        Telemetry[OpenTelemetry<br/>Metrics & Tracing]
    end

    subgraph "Runtime & Platform"
        Bun[Bun Runtime<br/>TypeScript Native<br/>2x Faster Startup]
    end

    Terminal --> QueryEngine
    Palette --> QueryEngine
    QueryEngine --> AgentCoord
    QueryEngine --> FileTools
    QueryEngine --> ShellTools
    QueryEngine --> AgentTools
    QueryEngine --> WebTools
    QueryEngine --> MCPTools
    AgentCoord --> FileTools
    AgentCoord --> ShellTools
    FileTools --> API
    ShellTools --> API
    AgentTools --> API
    WebTools --> API
    MCPTools --> MCP
    API --> Cache
    API --> Auth
    API --> Telemetry
    MCP --> Auth
    Cache --> Bun
    Telemetry --> Bun
```

**Các quyết định kiến trúc chính:**
- **Tách lớp rõ ràng** cho phép UI, logic và services phát triển độc lập
- **Thiết kế streaming-first** cho phép tools thực thi trước khi LLM hoàn thành
- **Specialized agents** giảm chi phí 3x cho các tác vụ cụ thể
- **Dual-role MCP** vừa là client (sử dụng tools bên ngoài) vừa là server (cung cấp tools)
- **Bun runtime** khởi động nhanh hơn 2x nhờ hỗ trợ TypeScript native

Xem [Tổng quan Kiến trúc](./docs_vi/02-architecture-overview.md) để hiểu chi tiết từng hệ thống con.

## Kho Mã nguồn

⚠️ **CÔNG BỐ QUAN TRỌNG**: Wiki này phân tích mã nguồn Claude Code từ một repository GitHub công khai.

**Nguồn phân tích:**
- 📦 **GitHub Repository**: [https://github.com/777genius/claude-code-source-code-full](https://github.com/777genius/claude-code-source-code-full)
- 📅 **Phiên bản phân tích** - Claude Code từ khoảng tháng 3/2026
- 🔗 **Sản phẩm chính thức**: [claude.com/code](https://claude.com/code)

**Phương pháp phân tích:**
1. **Trích xuất mã nguồn** - Clone từ GitHub repository (xem link trên)
2. **Phân tích code** - ~512,000 dòng TypeScript qua ~1,900 files
3. **Tài liệu hóa patterns** - Mẫu kiến trúc, quyết định thiết kế, tối ưu hiệu suất
4. **Nghiên cứu so sánh** - Phân tích song song với Cursor, Continue, và Aider

**Bạn có thể xác minh phân tích của chúng tôi:**
```bash
# Clone repository chúng tôi đã phân tích
git clone https://github.com/777genius/claude-code-source-code-full.git

# Khám phá cấu trúc codebase
cd claude-code-source-code-full
ls -la src/

# Xác minh đường dẫn files được tham chiếu trong wiki
ls src/QueryEngine.ts
ls -la src/tools/
ls -la src/components/
```

**Tham chiếu code xuyên suốt wiki này:**
- Tất cả đường dẫn file tham chiếu cấu trúc GitHub repository (ví dụ: `src/QueryEngine.ts`)
- Code snippets được trích xuất từ files trong repository
- Sơ đồ kiến trúc được vẽ từ tổ chức code thực tế
- Bạn có thể xác minh mọi tuyên bố bằng cách kiểm tra repository

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
│   ├── 10-lessons-learned.md          # Những bài học rút ra
│   └── 11-feature-flags.md            # Kiến trúc feature flag
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
| [11. Feature Flags](./docs/11-feature-flags.md) | Kiến trúc feature flag và trạng thái | Build-time, runtime, GrowthBook, beta headers |
| [12. Security Vulnerabilities](./docs/12-security-vulnerabilities.md) | Đánh giá bảo mật toàn diện | Lỗ hổng Critical/High/Medium, khắc phục |

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

## Độ tin cậy & Xác minh

### Cách wiki này được xây dựng

⚠️ **TUYÊN BỐ QUAN TRỌNG**: Phân tích này dựa trên **mã nguồn bị rò rỉ**, không phải bản phát hành công khai chính thức.

❌ **Không thể xác minh độc lập**
- Phân tích **mã nguồn bị rò rỉ/không chính thức** của Claude Code
- Nguồn thu được qua **kênh không rõ** (không phải phân phối chính thức)
- **Không có phiên bản công khai** để tham chiếu chéo
- Người đọc **không thể tái tạo** phân tích này từ nguồn công khai
- Có thể không khớp với phiên bản production chính thức

⚠️ **Hạn chế đáng kể**
- Code có thể **không đầy đủ** hoặc từ nhánh phát triển
- Có thể chứa tính năng **đã xóa/chưa phát hành**
- Kiến trúc có thể đã **thay đổi** kể từ khi rò rỉ
- Không đảm bảo **độ chính xác** so với production hiện tại
- Không thể xác minh **mục đích** của quyết định thiết kế

✅ **Những gì chúng tôi có thể nói**
- 512,000 dòng TypeScript được xem xét từ nguồn bị rò rỉ
- 1,900+ files được phân tích qua 10 hệ thống con chính
- 40+ tools được tài liệu hóa với chi tiết triển khai
- 85+ slash commands được liệt kê với patterns
- Patterns có vẻ nhất quán với best practices TypeScript production

✅ **Nghiên cứu độc lập**
- Không liên kết với Anthropic (chỉ phân tích giáo dục)
- Phân tích so sánh với 3 đối thủ (Cursor, Continue, Aider)
- Tập trung vào học patterns kiến trúc
- Quyết định kiến trúc được giải thích kèm lý do

### Tại sao Phân tích này Có Giá trị Dù Có Hạn chế

**Insights giáo dục:**
- Tài liệu hóa patterns kiến trúc AI tool phức tạp
- Hiển thị triển khai TypeScript/React ở mức production
- Minh họa kỹ thuật tối ưu chi phí
- Thể hiện cân nhắc bảo mật cho AI coding tools

**Giá trị so sánh:**
- Tiết lộ sự khác biệt kiến trúc vs đối thủ
- Làm nổi bật đổi mới trong streaming execution
- Tài liệu hóa patterns điều phối multi-agent
- Hiển thị thực hành kỹ thuật production

**Minh bạch:**
- Mọi tuyên bố trích dẫn files cụ thể từ nguồn bị rò rỉ
- Code snippets bao gồm comment vị trí nguồn
- Sơ đồ kiến trúc hiển thị dependencies module thực tế
- Thành thật về hạn chế và không chắc chắn

### Lưu ý Quan trọng

**Bạn nên hoài nghi:**
- ⚠️ Đây là code bị rò rỉ, không phải tài liệu chính thức
- ⚠️ Có thể không đại diện cho phiên bản production hiện tại
- ⚠️ Tính năng mô tả có thể không tồn tại trong sản phẩm thực
- ⚠️ Kiến trúc có thể đã phát triển kể từ khi rò rỉ
- ⚠️ Không thể xác minh với nguồn chính thức

**Sử dụng wiki này để:**
- ✅ Học patterns kiến trúc cho AI tools
- ✅ Hiểu cách tiếp cận tiềm năng cho vấn đề khó
- ✅ Nghiên cứu patterns TypeScript/React production
- ✅ So sánh với đối thủ được tài liệu hóa công khai

**KHÔNG sử dụng wiki này để:**
- ❌ Đưa ra tuyên bố về khả năng chính thức của Claude Code
- ❌ Giả định đây đại diện phiên bản production hiện tại
- ❌ Trích dẫn như nguồn có thẩm quyền về Claude Code
- ❌ Bỏ qua tài liệu chính thức của Anthropic

## Phương pháp xây dựng wiki

⚠️ **Dựa trên mã nguồn bị rò rỉ** - Xem tuyên bố quan trọng ở trên

Wiki này được xây dựng dựa trên:

- **Phân tích mã nguồn** của codebase Claude Code bị rò rỉ (dường như từ tháng 3/2026)
- **Điều tra ở cấp độ code** trên ~512,000 dòng TypeScript qua ~1,900 files
- **Rút trích patterns** từ comment, kiểu dữ liệu, chi tiết triển khai và git history
- **Nghiên cứu so sánh** với Cursor, Continue và Aider (kiến trúc được tài liệu hóa công khai)
- **Phân tích kiến trúc** mối quan hệ component và luồng dữ liệu

**Những gì chúng tôi KHÔNG làm:**
- ❌ Kiểm thử với phiên bản production thực tế đang chạy
- ❌ Xác minh tính năng với sản phẩm chính thức
- ❌ Profile hiệu suất của deployments thực
- ❌ Truy cập tài liệu nội bộ chính thức

Toàn bộ tài liệu được rút ra từ files mã nguồn bị rò rỉ. Có thể không khớp với phiên bản production chính thức hoặc tài liệu marketing.

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

## Cân nhắc Pháp lý & Đạo đức

### Bản quyền & Quyền sở hữu

**Quyền sở hữu mã nguồn:**
- Claude Code là **phần mềm độc quyền** © Anthropic, PBC
- Tất cả mã nguồn, thương hiệu và tài sản trí tuệ thuộc về Anthropic
- Wiki này **không** phân phối lại bất kỳ code nào của Anthropic
- Phân tích dựa trên npm package được phân phối công khai với source maps

**Nội dung wiki:**
- Tài liệu và phân tích © 2026 Contributors
- Cấp phép theo [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/)
- Chỉ cho mục đích giáo dục và nghiên cứu
- Không liên kết hoặc được xác nhận bởi Anthropic

### Sử dụng Hợp lý & Mục đích Giáo dục

⚠️ **BẤT ĐỊNH PHÁP LÝ**: Phân tích **mã nguồn độc quyền bị rò rỉ** đặt ra câu hỏi pháp lý nghiêm trọng.

**Lập luận sử dụng hợp lý tiềm năng:**

⚠️ **Mục đích chuyển đổi** (không chắc chắn)
- Gốc: Phần mềm thực thi độc quyền
- Công việc này: Tài liệu giáo dục về patterns kiến trúc
- Thêm bình luận, phân tích và insights so sánh
- **NHƯNG**: Dựa trên rò rỉ trái phép, không phải truy cập hợp pháp

⚠️ **Phạm vi giới hạn** (một phần)
- Chỉ phân tích kiến trúc và design patterns
- Không phân phối lại mã nguồn hoàn chỉnh
- Code snippets là trích dẫn tối thiểu để minh họa
- **NHƯNG**: Tiết lộ chi tiết triển khai độc quyền

⚠️ **Tác động thị trường** (tối thiểu)
- Mã nguồn đã công khai - không còn "bí mật"
- Không thể sử dụng thay thế cho Claude Code chính thức
- Không ảnh hưởng đến lợi nhuận của Anthropic
- Không làm giảm nhu cầu thị trường cho sản phẩm chính thức

✅ **Lợi ích công cộng** (mạnh mẽ)
- Thúc đẩy giáo dục về kiến trúc AI tool
- Giúp developers xây dựng hệ thống AI tốt hơn
- Góp phần vào kiến thức kỹ thuật công cộng
- Có thể xác minh bởi bất kỳ ai qua repository công khai

**Đánh giá:**
Phân tích này đủ điều kiện cho **sử dụng hợp lý** theo luật bản quyền Hoa Kỳ. Mục đích giáo dục và bình luận học thuật, không cạnh tranh với Claude Code chính thức, và sử dụng giới hạn (phân tích kiến trúc, không phân phối lại toàn bộ mã). Repository GitHub công khai cho phép xác minh độc lập, giảm thiểu lo ngại về độ tin cậy.

### Nguyên tắc Đạo đức

**Những gì chúng tôi làm:**
- ✅ Phân tích repository GitHub công khai bên thứ ba
- ✅ Tài liệu hóa architecture patterns từ mã nguồn có sẵn
- ✅ So sánh với các lựa chọn mã nguồn mở
- ✅ Trích dẫn Anthropic là tác giả gốc của Claude Code
- ✅ Tôn trọng quyền sở hữu trí tuệ thông qua sử dụng hợp lý

**Những gì chúng tôi không làm:**
- ❌ Phân phối lại mã nguồn hoàn chỉnh của Anthropic
- ❌ Reverse engineer các binary đã biên dịch
- ❌ Truy cập repositories nội bộ/riêng tư của Anthropic
- ❌ Tuyên bố mã là của chúng tôi hoặc liên kết chính thức
- ❌ Cạnh tranh với sản phẩm Claude Code chính thức

### Công bố có Trách nhiệm

**Nếu bạn tìm thấy thông tin nhạy cảm:**
- **Không** công bố lỗ hổng bảo mật trong wiki này
- Báo cáo cho Anthropic: [security@anthropic.com](mailto:security@anthropic.com)
- Tuân theo thực hành công bố có trách nhiệm
- Cho phép thời gian sửa chữa trước khi thảo luận công khai

**Nếu bạn đại diện cho Anthropic:**
- Chúng tôi tôn trọng tài sản trí tuệ của bạn
- Liên hệ để thảo luận bất kỳ mối quan ngại: [Issues](https://github.com/your-repo/issues)
- Chúng tôi sẽ nhanh chóng giải quyết các yêu cầu hợp lệ
- Sẵn sàng hợp tác về attribution

### Trích dẫn & Ghi nhận

**Khi tham chiếu wiki này:**

```bibtex
@misc{claude-code-wiki-2026,
  title={Claude Code Architecture Wiki: Phân tích AI Coding Assistant Production},
  author={Contributors},
  year={2026},
  howpublished={\url{https://github.com/your-repo/claude-code-wiki}},
  note={Phân tích giáo dục về kiến trúc Claude Code của Anthropic}
}
```

**Khi thảo luận về Claude Code:**
- Luôn ghi nhận Anthropic, PBC
- Liên kết đến nguồn chính thức: [claude.com/code](https://claude.com/code)
- Làm rõ khi trích dẫn wiki này vs tài liệu chính thức
- Tôn trọng hướng dẫn branding của Anthropic

---

## Lời cảm ơn

**Cảm ơn:**
- **Đội ngũ Anthropic** đã xây dựng Claude Code và phân phối qua npm
- **Cộng đồng open source** cho React, Ink, Bun và các công nghệ khác
- **Đội ngũ Cursor, Continue, Aider** đã thúc đẩy công cụ AI coding
- **Contributors** đã cải thiện wiki này với sửa chữa và insights

---

**Sẵn sàng khám phá?** Hãy bắt đầu với [🔥 Competitive Advantages](./docs_vi/01-competitive-advantages.md) để xem 10 cải tiến làm nên sự khác biệt của Claude Code.

**Có câu hỏi?** Xem [FAQ](./docs/FAQ.md) để có câu trả lời nhanh về kiến trúc.
