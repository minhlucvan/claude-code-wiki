<div align="center">
  <img src="./assets/banner.svg" alt="Claude Code Wiki" width="100%">
</div>

# Claude Code Wiki

> **Hướng dẫn toàn diện về kiến trúc, mẫu thiết kế và đổi mới cạnh tranh của Claude Code — Tìm hiểu cách đạt được tốc độ thực thi nhanh hơn 2-5 lần, bộ nhớ hội thoại không giới hạn và tiết kiệm 90% chi phí**

[English](./README.md) | **Tiếng Việt** | [中文](./README.zh.md) | [Español](./README.es.md) | [日本語](./README.ja.md)

## Wiki Này Là Gì

**Claude Code Wiki** là hướng dẫn quyền định để hiểu kiến trúc, mẫu kỹ thuật và lợi thế cạnh tranh của Claude Code. Thông qua phân tích **512,000 dòng TypeScript production**, wiki này tiết lộ:

- **10 đổi mới kiến trúc** giúp Claude Code vượt trội so với các đối thủ
- **Thực thi công cụ streaming** chạy các công cụ trong khi LLM streaming (UX nhanh hơn 2-5 lần)
- **Quản lý ngữ cảnh 5 lớp** cho phép bộ nhớ hội thoại không giới hạn
- **Điều phối đa agent** với chia sẻ cache (giảm 90% chi phí)
- **React terminal UI** cung cấp UX production-grade trong CLI
- **Bảo mật cấp AST** cho phân tích lệnh sâu (không phải regex)
- **Mẫu kỹ thuật production** được tối ưu hóa cho kinh tế quy mô lớn

**Đây không chỉ là một công cụ AI coding thông thường** — nó được xây dựng bởi đội ngũ tạo ra Claude, với quyền truy cập API độc quyền và cơ hội tối ưu hóa mà đối thủ không có.

## Tại Sao Wiki Này Tồn Tại

Wiki này tồn tại để tài liệu hóa các mẫu production-grade và quyết định kiến trúc khiến Claude Code trở nên xuất sắc. Tìm hiểu cách nó giải quyết các vấn đề khó mà đối thủ gặp khó khăn:

- **Tốc độ**: Hầu hết công cụ đợi LLM hoàn thành trước khi chạy công cụ tuần tự. Claude Code chạy công cụ đồng thời trong khi streaming, đạt được các thao tác đa công cụ nhanh hơn 2-5 lần.
- **Bộ nhớ**: Đối thủ sử dụng cắt bớt ngữ cảnh cơ bản hoặc yêu cầu dọn dẹp thủ công. Claude Code sử dụng pipeline tự động nén 5 lớp cho hội thoại không giới hạn.
- **Chi phí**: Chạy nhiều agent rất tốn kém. Tối ưu hóa cache fork của Claude Code đạt được giảm 90% chi phí thông qua cache chia sẻ.
- **Bảo mật**: Hầu hết công cụ sử dụng regex để phân tích lệnh. Claude Code sử dụng phân tích Bash cấp AST cho phân tích bảo mật sâu.
- **Quy mô**: Được xây dựng cho kinh tế quy mô lớn, tối ưu hóa cho Gtok/tuần ở cấp tổ chức.

Wiki này tài liệu hóa các mẫu và kỹ thuật này để bạn có thể học hỏi và áp dụng vào công cụ AI của riêng mình.

## Bạn Sẽ Học Được Gì

### 🚀 Đổi Mới Cốt Lõi

1. **Thực Thi Công Cụ Streaming** - Cách chạy công cụ đồng thời trong khi LLM streaming phản hồi
2. **Quản Lý Ngữ Cảnh** - Pipeline 5 lớp cho bộ nhớ hội thoại không giới hạn với tự động nén
3. **Điều Phối Đa Agent** - 6 agent chuyên biệt với kiến trúc chia sẻ cache
4. **Tối Ưu Prompt Cache** - Mẫu fork đạt được giảm 90% chi phí trên các agent
5. **React Terminal UI** - Kiến trúc component production-grade cho công cụ CLI

### 🔒 Kỹ Thuật Production

6. **Bảo Mật Cấp AST** - Phân tích lệnh Bash sâu và hệ thống quyền
7. **Feature Flags** - Loại bỏ dead code với chi phí runtime bằng 0
8. **Tối Ưu Khởi Động** - Mẫu prefetch song song và lazy loading
9. **Hệ Sinh Thái Tích Hợp** - MCP hai vai trò (client + server), cầu nối IDE, hệ thống skill
10. **Tư Duy Quy Mô Lớn** - Tối ưu chi phí ở cấp tổ chức (tiết kiệm Gtok/tuần)

### 📊 Định Vị Cạnh Tranh

| Tính Năng | Claude Code | Cursor | Continue | Aider |
|-----------|-------------|--------|----------|-------|
| **Thực Thi Công Cụ Streaming** | ✅ Đồng thời | ❌ Tuần tự | ❌ Tuần tự | ❌ Tuần tự |
| **Quản Lý Ngữ Cảnh** | ✅ Tự động nén 5 lớp | ⚠️ Cắt bớt cơ bản | ⚠️ Cắt bớt cơ bản | ⚠️ Thủ công |
| **Đa Agent** | ✅ Native với chia sẻ cache | ❌ Không | ❌ Không | ⚠️ Hạn chế |
| **Bảo Mật** | ✅ Phân tích AST + quyền | ⚠️ Prompt cơ bản | ⚠️ Prompt cơ bản | ⚠️ Phê duyệt user |
| **Terminal UI** | ✅ React/Ink (phong phú) | N/A (IDE) | N/A (IDE) | ⚠️ CLI cơ bản |
| **Hỗ Trợ MCP** | ✅ Client + Server | ⚠️ Chỉ client | ⚠️ Chỉ client | ❌ Không |
| **Prompt Caching** | ✅ Tối ưu fork | ⚠️ Cơ bản | ⚠️ Cơ bản | ❌ Không |

**Chú thích**: ✅ Triển khai nâng cao • ⚠️ Triển khai cơ bản • ❌ Không có

## Cấu Trúc Wiki

```
claude-code-wiki/
├── docs/                           # 10 hướng dẫn wiki toàn diện
│   ├── README.md                   # Điều hướng và tổng quan wiki
│   ├── 01-competitive-advantages.md   # 10 lợi thế không công bằng
│   ├── 02-architecture-overview.md    # Thiết kế hệ thống và luồng dữ liệu
│   ├── 03-streaming-execution.md      # Thực thi công cụ thời gian thực
│   ├── 04-context-management.md       # Pipeline ngữ cảnh 5 lớp
│   ├── 05-multi-agent-orchestration.md # Hệ thống đa agent
│   ├── 06-terminal-ux.md              # React terminal UI
│   ├── 07-security-model.md           # Phân tích AST và quyền
│   ├── 08-integration-ecosystem.md    # MCP, cầu nối IDE, skills
│   ├── 09-production-engineering.md   # Mẫu tối ưu hóa
│   └── 10-lessons-learned.md          # Bài học chính
└── claude-code/                    # Mã nguồn đầy đủ (512K LOC)
    ├── src/                        # Triển khai TypeScript
    ├── skills/                     # 85+ lệnh slash
    └── package.json                # Dependencies và scripts
```

## Hướng Dẫn Nhanh

Điều hướng wiki dựa trên mục tiêu của bạn:

### 🎯 Xây Dựng Công Cụ AI Coding

**Bắt đầu tại đây**: [Lợi Thế Cạnh Tranh](./docs/01-competitive-advantages.md)

Khám phá 10 đổi mới kiến trúc:
- Thực thi công cụ streaming cho UX nhanh hơn 2-5 lần
- Điều phối đa agent với chia sẻ cache
- Quản lý ngữ cảnh cho hội thoại không giới hạn
- Bảo mật production và tối ưu chi phí

**Sau đó khám phá**: [Bài Học Đúc Kết](./docs/10-lessons-learned.md) cho những điểm chính có thể áp dụng vào công cụ của bạn.

### 🔍 Đánh Giá Claude Code

**Bắt đầu tại đây**: [Tổng Quan Kiến Trúc](./docs/02-architecture-overview.md)

Hiểu thiết kế hệ thống và sẵn sàng production:
- Kiến trúc cấp cao và luồng dữ liệu
- Các hệ thống con cốt lõi và trách nhiệm
- Phân tích ngăn xếp công nghệ (Bun, React, TypeScript)

**Sau đó xem xét**:
- [Mô Hình Bảo Mật](./docs/07-security-model.md) cho mối quan tâm doanh nghiệp
- [Hệ Sinh Thái Tích Hợp](./docs/08-integration-ecosystem.md) cho khả năng mở rộng

### 💡 Học Các Mẫu Nâng Cao

**Bắt đầu tại đây**: [Bài Học Đúc Kết](./docs/10-lessons-learned.md)

Nhận các mẫu có thể áp dụng cho production TypeScript/React:
- Kiến trúc React trong CLI
- Quản lý state ở quy mô lớn
- Kỹ thuật tối ưu chi phí
- Kỹ thuật quy mô lớn

**Sau đó tìm hiểu sâu**:
- [Terminal UX](./docs/06-terminal-ux.md) cho các mẫu React/Ink
- [Kỹ Thuật Production](./docs/09-production-engineering.md) cho kỹ thuật tối ưu hóa

## Chỉ Mục Wiki

| Hướng Dẫn | Mô Tả | Chủ Đề Chính |
|-----------|-------|--------------|
| [01. Lợi Thế Cạnh Tranh](./docs/01-competitive-advantages.md) | 10 đổi mới khiến Claude Code nổi bật | Thực thi streaming, tối ưu cache, bảo mật AST |
| [02. Tổng Quan Kiến Trúc](./docs/02-architecture-overview.md) | Thiết kế hệ thống và luồng dữ liệu | Hệ thống con cốt lõi, ngăn xếp công nghệ, kiến trúc production |
| [03. Thực Thi Streaming](./docs/03-streaming-execution.md) | Cách công cụ chạy đồng thời trong khi LLM streaming | Điều phối async, xử lý lỗi, tăng tốc 2-5 lần |
| [04. Quản Lý Ngữ Cảnh](./docs/04-context-management.md) | Pipeline 5 lớp cho hội thoại không giới hạn | Tự động nén, prompt caching, tối ưu bộ nhớ |
| [05. Điều Phối Đa Agent](./docs/05-multi-agent-orchestration.md) | 6 agent chuyên biệt với chia sẻ cache | Mẫu fork, chế độ coordinator, loại agent |
| [06. Terminal UX](./docs/06-terminal-ux.md) | Kiến trúc React terminal UI | Thiết kế component, quản lý state, 85+ lệnh |
| [07. Mô Hình Bảo Mật](./docs/07-security-model.md) | Phân tích Bash cấp AST và quyền | Phân tích lệnh, tích hợp sandbox, mô hình mối đe dọa |
| [08. Hệ Sinh Thái Tích Hợp](./docs/08-integration-ecosystem.md) | MCP, cầu nối IDE và hệ thống skill | MCP hai vai trò, VS Code/JetBrains, skills có điều kiện |
| [09. Kỹ Thuật Production](./docs/09-production-engineering.md) | Mẫu tối ưu hóa và tư duy quy mô lớn | Tốc độ khởi động, feature flags, tối ưu chi phí |
| [10. Bài Học Đúc Kết](./docs/10-lessons-learned.md) | Điểm chính và mẫu nên học | Insights có thể áp dụng, quyết định thiết kế, đánh đổi |

## Thống Kê Chính

| Chỉ Số | Giá Trị |
|--------|---------|
| **Tổng Dòng Code** | ~512,000 |
| **File TypeScript** | ~1,900 |
| **Công Cụ Tích Hợp** | 40+ |
| **Lệnh Slash** | 85+ |
| **Loại Agent** | 6 chuyên biệt |
| **Runtime** | Bun (hiệu năng cao) |
| **UI Framework** | React + Ink |
| **Trang Wiki** | 10 hướng dẫn toàn diện |

## Wiki Này Dành Cho Ai

### Nhà Phát Triển Xây Dựng AI Coding Assistants
Học các mẫu production-grade cho thực thi streaming, quản lý ngữ cảnh và điều phối đa agent. Hiểu cách đạt được UX nhanh hơn 2-5 lần và giảm 90% chi phí.

### Đội Sản Phẩm Đánh Giá Công Cụ AI
So sánh phương pháp kiến trúc giữa Claude Code, Cursor, Continue và Aider. Hiểu lợi thế cạnh tranh có thể đo lường về tốc độ, chi phí và khả năng.

### Kỹ Sư Học TypeScript/React Nâng Cao
Khám phá kiến trúc React trong CLI, quản lý state ở quy mô lớn và mẫu tối ưu production từ codebase 512K LOC.

### Kiến Trúc Sư Kỹ Thuật
Nghiên cứu quyết định thiết kế hệ thống, kiến trúc bảo mật và mẫu kỹ thuật quy mô lớn cho công cụ AI production.

## Phương Pháp Wiki

Wiki này được xây dựng từ:

- **Phân tích mã nguồn đầy đủ** của source maps gói npm Claude Code (tháng 3/2026)
- **Khám phá thực hành** và kiểm tra tất cả tính năng chính
- **Nghiên cứu so sánh** với kiến trúc Cursor, Continue và Aider
- **Điều tra cấp code** của 512,000 dòng TypeScript
- **Trích xuất mẫu** từ comments, types và chi tiết triển khai

Tất cả tài liệu được lấy từ code thực tế, không phải tài liệu marketing hoặc kiểm tra black-box.

## Đóng Góp Cho Wiki

Tìm thấy điều thú vị? Có thêm insights? Wiki này là tài liệu sống nhằm nắm bắt:

- Khoảnh khắc "Wow" trong kiến trúc
- Mẫu có thể áp dụng để xây dựng công cụ AI
- Quyết định thiết kế và đánh đổi
- Insights cạnh tranh và sự khác biệt

Issues và pull requests được chào đón cho:
- Tài liệu hoặc sửa lỗi bổ sung
- Khám phá mới trong codebase
- Giải thích và ví dụ mẫu
- Insights so sánh với các công cụ khác

## Giấy Phép & Ghi Công

**Mã Nguồn**: Claude Code là phần mềm độc quyền của Anthropic. Wiki này chỉ cho mục đích giáo dục.

**Nội Dung Wiki**: Tài liệu và phân tích © 2026. Chia sẻ cho mục đích giáo dục và nghiên cứu.

**Phương Pháp**: Mã nguồn được trích xuất từ source maps npm và tài liệu hóa thông qua xem xét code, không phải reverse engineering.

---

**Sẵn sàng học?** Bắt đầu với [🔥 Lợi Thế Cạnh Tranh](./docs/01-competitive-advantages.md) để khám phá 10 đổi mới khiến Claude Code đặc biệt.
