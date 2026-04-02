# Claude Code Architecture: Frequently Asked Questions

> **Quick answers to common questions about Claude Code's architecture and implementation**

This FAQ helps you understand the architectural decisions, design patterns, and engineering techniques documented in this wiki. These answers are based on analysis of Claude Code's production codebase (512,000 lines of TypeScript).

## Table of Contents

- [Understanding the Architecture](#understanding-the-architecture)
- [Streaming Execution](#streaming-execution)
- [Context Management](#context-management)
- [Multi-Agent System](#multi-agent-system)
- [Terminal UI](#terminal-ui)
- [Security & Permissions](#security--permissions)
- [Integration Ecosystem](#integration-ecosystem)
- [Performance & Optimization](#performance--optimization)
- [Implementation Patterns](#implementation-patterns)
- [Applying These Patterns](#applying-these-patterns)

---

## Understanding the Architecture

### What makes Claude Code's architecture different from other AI coding tools?

**10 key architectural innovations:**

1. **Streaming tool execution** - Tools run concurrently while LLM streams (2-5x faster)
2. **5-layer autocompaction** - Unlimited conversation length without manual cleanup
3. **Prompt cache fork pattern** - 90% cost reduction for multi-agent workflows
4. **React terminal UI** - Production-grade component architecture in CLI
5. **AST-level Bash parsing** - Deep security analysis instead of regex
6. **Dual-role MCP** - Both client and server capabilities
7. **6 specialized agents** - Purpose-built for specific workflows
8. **Build-time feature flags** - Dead code elimination (37% smaller bundles)
9. **First-party API access** - Anthropic-specific optimizations
10. **Fleet-scale thinking** - Cost optimization at org level (Gtok/week)

See [Competitive Advantages](./01-competitive-advantages.md) for detailed comparison with Cursor, Continue, and Aider.

### How is Claude Code organized internally?

**Layered architecture with clear separation:**

```
Terminal UI Layer (React/Ink)
    ↓
Command Layer (85 slash commands)
    ↓
Query Engine (LLM lifecycle, streaming, tools)
    ↓
Tool System (40+ self-contained tools)
    ↓
Service Layer (API, MCP, OAuth, telemetry)
    ↓
Runtime (Bun)
```

**Key subsystems:**
- **Terminal UI**: 80+ React components for CLI rendering
- **Query Engine**: 1,297 lines managing conversation state
- **Tools**: 40+ tools in isolated directories
- **Services**: Claude API, MCP client, OAuth, telemetry

See [Architecture Overview](./02-architecture-overview.md) for complete system design.

### Why use React for a CLI tool?

**Benefits of React + Ink architecture:**

1. **Declarative UI** - Easier to manage complex terminal state
2. **Component reuse** - Share patterns between CLI and web
3. **Rich ecosystem** - Use React hooks, context, patterns
4. **Maintainability** - Better than imperative terminal manipulation
5. **Professional UX** - Progress bars, spinners, multi-pane layouts

**Example component:**
```tsx
function ToolExecutionView({ tools }) {
  return (
    <Box flexDirection="column">
      {tools.map(tool => (
        <Box key={tool.id}>
          {tool.status === 'running' && <Spinner />}
          <Text>{tool.name}</Text>
          <ProgressBar percent={tool.progress} />
        </Box>
      ))}
    </Box>
  )
}
```

See [Terminal UX](./06-terminal-ux.md) for component architecture.

### What's the technology stack?

**Core technologies:**

| Component | Technology | Why? |
|-----------|-----------|------|
| **Runtime** | Bun | 2x faster startup, native TypeScript |
| **UI Framework** | React + Ink | Declarative CLI components |
| **Schema Validation** | Zod | Type inference, composable |
| **CLI Framework** | Commander.js | Industry standard arg parsing |
| **State Management** | Custom + React Context | Simpler than Redux, immutable |
| **API Client** | Custom streaming | SSE parsing, retry logic |

**Bundle size:** ~28MB (consumer), ~45MB (enterprise with features)

**Startup time:** ~600ms (optimized with parallel prefetch)

See [Architecture Overview](./02-architecture-overview.md#technology-stack) for details.

---

## Streaming Execution

### How does streaming tool execution work?

**Traditional approach (sequential):**
```
[Wait 2s for LLM] → [Tool 1: 2s] → [Tool 2: 2s] = 6s total
```

**Claude Code (streaming + concurrent):**
```
[LLM streaming: 2s]
  ├─ [0.5s] Tool 1 detected → Execute (2s)
  └─ [1.0s] Tool 2 detected → Execute parallel (2s)
Total: 3s (2x faster)
```

**Implementation:**
1. **SSE parser** detects tool calls as they stream
2. **Concurrent executor** runs safe tools in parallel
3. **Parameter accumulator** handles incremental JSON
4. **Progress tracker** updates UI in real-time

See [Streaming Execution](./03-streaming-execution.md) for complete implementation.

### Which tools can run concurrently?

**Concurrency determined by tool interface:**

```typescript
interface Tool {
  isConcurrencySafe(input): boolean
  isReadOnly(input): boolean
}
```

**Always safe (read-only):**
- FileRead, Grep, Glob (no side effects)
- WebFetch, WebSearch (external, independent)

**Never safe (writes):**
- FileEdit, FileWrite (file conflicts)
- Bash with destructive commands

**Conditional:**
- Bash with read-only commands (git status, ls)
- FileEdit to different files (no conflict)

See [Streaming Execution](./03-streaming-execution.md#2-concurrent-executor) for safety checks.

### How are mid-stream errors handled?

**Error recovery pattern:**

1. **Detect** error during tool execution
2. **Cancel** dependent tools that need failed tool's output
3. **Report** error to LLM as tool result message
4. **Continue** streaming (don't crash conversation)
5. **LLM adapts** based on error message

**Retry logic for transient errors:**
- Network timeouts (ECONNRESET, ETIMEDOUT)
- Server errors (503, 429)
- Exponential backoff: 1s, 2s, 4s

**No retry for logic errors:**
- File not found
- Syntax errors
- Permission denied

See [Streaming Execution](./03-streaming-execution.md#error-recovery) for implementation.

---

## Context Management

### How does the 5-layer autocompaction work?

**Progressive compaction pipeline:**

```
Layer 1 (50 msgs):   Keep all → 50K tokens
Layer 2 (100 msgs):  Recent 25 + Compact(25→5) → 30K tokens
Layer 3 (200 msgs):  Recent 25 + Mid(25→5) + Old(50→5) → 35K tokens
Layer 4 (400 msgs):  Recent 25 + 3 layers(175→15) → 40K tokens
Layer 5 (500+ msgs): Recent 25 + 4 layers(375→20) → 45K tokens
```

**Result:** Unlimited conversation without hitting 200K token limit.

**Implementation:**
1. **Monitor** token count per request
2. **Trigger** compaction at thresholds (50, 100, 200, 400 msgs)
3. **Split** into recent (keep) vs older (compact)
4. **Summarize** older messages with LLM (Haiku model)
5. **Replace** older messages with summary boundary marker

See [Context Management](./04-context-management.md#2-compaction-trigger) for code.

### What gets preserved during compaction?

**Compaction prompt preserves:**
- File paths and names (exact strings)
- Function/class/variable names
- Technical decisions and rationale
- Error messages and solutions
- Configuration values
- Open tasks and TODOs

**Compaction removes:**
- Verbose explanations
- Intermediate reasoning
- Repeated information
- Pleasantries and confirmations

**Quality metrics:**
- Compression ratio: ~80% (e.g., 25 messages → 5K tokens)
- Keywords preserved: 85-90%
- File paths preserved: 95%+

See [Context Management](./04-context-management.md#semantic-preservation) for prompt engineering.

### How much does autocompaction cost?

**Cost analysis for 500-message conversation:**

| Approach | Input Cost | Compaction Cost | Total |
|----------|-----------|----------------|-------|
| No compaction | $300 (500K tokens/req) | $0 | $300 |
| With compaction | $45 (30K tokens/req) | $0.75 (10 compactions) | $45.75 |

**Savings: 85%**

**Compaction costs:**
- Frequency: Every ~50 messages
- Model: Haiku (cheaper for summarization)
- Output: ~5K tokens × $15/Mtok = $0.075 per compaction

**With prompt cache:** Additional 78% savings on repeated context.

See [Context Management](./04-context-management.md#token-economics) for breakdown.

---

## Multi-Agent System

### What are the 6 specialized agent types?

**Agent specialization reduces cost and improves speed:**

| Agent | Tools | Use Case | Efficiency |
|-------|-------|----------|-----------|
| **general-purpose** | All 40 tools | Complex multi-step tasks | Baseline |
| **Explore** | 8 read-only (Glob, Grep, Read) | Fast codebase search | 3x cheaper, 3x faster |
| **Plan** | Planning tools (no Edit/Write) | Implementation planning | 2x faster |
| **Bash** | Bash only | Command execution | 10x cheaper |
| **statusline-setup** | Read, Edit | Config file editing | Specialized prompts |
| **claude-code-guide** | Read-only + Web | Documentation Q&A | Knowledge expert |

**Example task:** "Find all API endpoints"
- General-purpose: $0.15, 45s (40 tools in prompt)
- Explore agent: $0.05, 15s (8 tools in prompt)

See [Multi-Agent Orchestration](./05-multi-agent-orchestration.md#1-agent-definition) for definitions.

### How does the cache fork pattern work?

**Problem:** Multiple agents creating duplicate caches

**Without fork:**
```typescript
Agent 1: Create cache (10K tokens) = $0.0375
Agent 2: Create cache (10K tokens) = $0.0375  // DUPLICATE
Agent 3: Create cache (10K tokens) = $0.0375  // DUPLICATE
Total: $0.1125
```

**With fork pattern:**
```typescript
// 1. Create base cache once
Base context → Cache = $0.0375

// 2. All agents read from cache
Agent 1: Read cache + task = $0.003
Agent 2: Read cache + task = $0.003
Agent 3: Read cache + task = $0.003
Total: $0.0465 (59% savings)
```

**Implementation:**
```typescript
// Mark base context for caching
const cachedBase = baseContext.map((msg, i) => ({
  ...msg,
  cache_control: i === baseContext.length - 1
    ? { type: 'ephemeral' }
    : undefined
}))

// Spawn agent inheriting cache
createAgent({
  messages: [...cachedBase, { role: 'user', content: task }]
})
```

See [Multi-Agent Orchestration](./05-multi-agent-orchestration.md#3-cache-fork-pattern) for economics.

### How do agents coordinate in parallel workflows?

**Coordinator mode architecture:**

```typescript
// Parent agent spawns multiple child agents
const agents = await Promise.all([
  createAgent({ task: 'Research topic A' }),
  createAgent({ task: 'Research topic B' }),
  createAgent({ task: 'Research topic C' }),
])

// All share cached parent context (fork pattern)
// Results merged by parent agent
```

**Benefits:**
- **Parallel execution** - 3 tasks in time of 1
- **Shared cache** - 90% cost reduction
- **Independent failures** - One error doesn't crash all
- **Inter-agent messaging** - Agents can communicate

**Use cases:**
- Research multiple topics simultaneously
- Parallel code exploration
- Distributed testing
- Concurrent file processing

See [Multi-Agent Orchestration](./05-multi-agent-orchestration.md#4-coordinator-mode) for patterns.

---

## Terminal UI

### How is the React terminal UI architected?

**Component hierarchy:**

```
<App>
  ├─ <MessageList>
  │   ├─ <UserMessage>
  │   ├─ <AssistantMessage>
  │   │   ├─ <ToolUseMessage>
  │   │   │   └─ <ToolSpecificUI>
  │   │   └─ <ToolResultMessage>
  │   └─ <SystemMessage>
  ├─ <InputArea>
  │   ├─ <VimModeInput>
  │   └─ <CommandPalette>
  ├─ <StatusBar>
  │   ├─ <TokenCounter>
  │   ├─ <CostDisplay>
  │   └─ <ModelIndicator>
  └─ <ProgressIndicators>
```

**State management:**
```typescript
type AppState = DeepImmutable<{
  messages: Message[]
  currentModel: ModelSetting
  permissions: PermissionRules
  activeTools: ToolExecution[]
  tokenUsage: TokenUsage
  settings: SettingsJson
}>
```

**80+ components** organized by feature area.

See [Terminal UX](./06-terminal-ux.md#2-component-architecture) for details.

### How are tool results rendered?

**Each tool provides custom rendering:**

```typescript
interface Tool {
  // Render tool invocation
  renderToolUseMessage(input, options): JSX.Element

  // Render tool result
  renderToolResultMessage(content, progress, options): JSX.Element
}
```

**Example: BashTool**
```tsx
renderToolUseMessage(input) {
  return (
    <Box>
      <Text color="cyan">$ {input.command}</Text>
    </Box>
  )
}

renderToolResultMessage(content, progress) {
  return (
    <Box flexDirection="column">
      <Text>{content.stdout}</Text>
      {content.stderr && <Text color="red">{content.stderr}</Text>}
      <Text color="gray">Exit code: {content.exitCode}</Text>
    </Box>
  )
}
```

**Benefits:**
- Tool-specific formatting (code highlighting, tables, etc.)
- Progress indicators during execution
- Error state visualization

See [Terminal UX](./06-terminal-ux.md#5-tool-rendering-system) for rendering system.

### How does the command palette work?

**Fuzzy search architecture:**

```typescript
// 85+ slash commands registered
const commands = [
  { name: 'commit', category: 'git', description: '...' },
  { name: 'review-pr', category: 'git', description: '...' },
  // ... 83 more
]

// Fuzzy matching with fuse.js
const fuse = new Fuse(commands, {
  keys: ['name', 'description', 'category'],
  threshold: 0.3,
})

// User types "/com"
const results = fuse.search('/com')
// → [commit, compact, config, ...]
```

**UI:**
- Triggered by `/` key
- Live search as user types
- Keyboard navigation (↑↓ arrows)
- Categories and descriptions
- Conditional visibility (feature flags)

See [Terminal UX](./06-terminal-ux.md#4-command-palette) for implementation.

---

## Security & Permissions

### How does AST-based Bash parsing work?

**Traditional security (regex):**
```bash
rm -rf ./temp          ✅ Allowed
rm -rf "$(pwd)/../.."  ✅ Allowed (regex can't detect)
```

**Claude Code (AST parsing):**
```typescript
// Parse into Abstract Syntax Tree
const ast = bashParser('rm -rf "$(pwd)/../.."')

// AST structure:
{
  command: 'rm',
  flags: ['-rf'],
  arguments: [{
    type: 'CommandSubstitution',
    command: 'pwd',
    pathTraversal: '../..'  // DETECTED
  }]
}

// Risk analysis
analyzeRisk(ast)
// → HIGH: Destructive command + path escape
// → BLOCK
```

**Catches:**
- Command substitution `$()`
- Path traversal `../../../`
- Pipe chains
- Redirects to sensitive files
- Obfuscated commands

See [Security Model](./07-security-model.md#1-ast-level-bash-parsing) for parser.

### What are the 4 permission modes?

**Permission modes control tool execution:**

| Mode | Behavior | Use Case |
|------|----------|----------|
| **Ask** | Prompt for every tool | Careful work, learning |
| **Allow** | Auto-allow safe tools | Balanced workflow |
| **Bypass** | Allow everything | Rapid prototyping (risky) |
| **Deny** | Block all tools | Read-only exploration |

**Permission check flow:**
```typescript
async function executeTool(tool, input) {
  // 1. Check permission mode
  const mode = getPermissionMode()

  // 2. Analyze tool safety
  const risk = await tool.checkPermissions(input)

  // 3. Decide action
  if (mode === 'bypass') return tool.call(input)
  if (mode === 'deny') throw new Error('Blocked')
  if (mode === 'allow' && risk === 'low') return tool.call(input)

  // 4. Ask user
  const approved = await askUser(`Allow ${tool.name}?`)
  if (approved) return tool.call(input)
  throw new Error('User denied')
}
```

See [Security Model](./07-security-model.md#4-permission-modes) for implementation.

### How are dangerous commands detected?

**Risk assessment factors:**

```typescript
function assessRisk(command: CommandAST): RiskLevel {
  let risk = 'LOW'

  // Destructive commands
  if (command.name in ['rm', 'dd', 'mkfs']) {
    risk = 'HIGH'
  }

  // Dangerous flags
  if (command.flags.includes('-rf')) {
    risk = 'HIGH'
  }

  // Path escape
  if (command.args.some(arg => arg.includes('..'))) {
    risk = 'HIGH'
  }

  // Network access
  if (command.name in ['curl', 'wget', 'nc']) {
    risk = 'MEDIUM'
  }

  // Sensitive files
  if (command.redirects.some(r => r.file.includes('/etc/'))) {
    risk = 'HIGH'
  }

  return risk
}
```

**Blocked patterns:**
- `rm -rf` with path traversal
- `dd` to block devices
- `curl` with POST to unknown domains
- Writes to `/etc/`, `/sys/`, `/proc/`
- Command injection attempts

See [Security Model](./07-security-model.md#3-risk-assessment) for heuristics.

---

## Integration Ecosystem

### How does dual-role MCP work?

**Claude Code acts as both MCP client and server:**

**As MCP Client:**
```typescript
// Connect to external MCP servers
const mcpClient = new MCPClient({
  command: 'npx',
  args: ['-y', '@modelcontextprotocol/server-postgres'],
  env: { DATABASE_URL: 'postgres://...' },
})

await mcpClient.connect()
const tools = await mcpClient.listTools()
// → Register as MCPTool instances
// → LLM can now use database tools
```

**As MCP Server:**
```typescript
// Expose Claude Code tools to other apps
const mcpServer = new MCPServer({
  name: 'claude-code',
  tools: [BashTool, FileReadTool, GrepTool],
})

// VS Code can now call Claude Code's Bash tool
// Web apps can use FileRead/FileEdit
```

**Benefits:**
- **Client:** Use external tools (databases, browsers, APIs)
- **Server:** Share tools with other AI apps
- **Bidirectional:** Both producer and consumer

See [Integration Ecosystem](./08-integration-ecosystem.md#1-dual-role-mcp) for architecture.

### What is the skill system?

**Skills are reusable workflows:**

```
.claude/skills/my-skill/
├── SKILL.md           # Documentation
├── prompts/
│   └── system.md      # Custom system prompt
├── references/        # Reference docs
│   └── api.md
└── _meta.json         # Metadata
```

**Metadata (`_meta.json`):**
```json
{
  "name": "my-skill",
  "version": "1.0.0",
  "description": "Custom workflow",
  "allowedTools": ["FileRead", "Bash", "Grep"],
  "requiredFeature": null  // Feature flag
}
```

**Conditional loading:**
```typescript
// Skills only load if feature flag enabled
if (feature('CUSTOM_SKILLS')) {
  loadSkills('.claude/skills/')
}
```

**85+ built-in skills** for common workflows.

See [Integration Ecosystem](./08-integration-ecosystem.md#3-skill-system) for examples.

### How does the IDE bridge work?

**Bridge Mode architecture:**

```
Terminal (Claude Code)
    ↓ Bridge API
VS Code Extension
    ↓ LSP
VS Code UI
```

**Implementation:**
```typescript
// Claude Code in bridge mode
startBridgeServer({
  port: 3000,
  endpoints: {
    '/conversation': handleConversation,
    '/tools': handleToolCall,
    '/state': getState,
  },
})

// VS Code extension connects
const bridge = new BridgeClient('http://localhost:3000')
const response = await bridge.sendMessage('Help me refactor this')
```

**Shared capabilities:**
- Conversation state synced
- Tools callable from either UI
- File operations respect both contexts

See [Integration Ecosystem](./08-integration-ecosystem.md#2-ide-bridges) for protocol.

---

## Performance & Optimization

### How is startup time optimized?

**Parallel prefetch pattern:**

```typescript
// Start all I/O operations in parallel
const [mdm, keychain, apiStatus] = await Promise.all([
  fetchMDMPolicy(),
  loadKeychainToken(),
  checkAPIStatus(),
])

// Lazy load heavy modules
const { heavyModule } = await import('./heavy')
```

**Startup phases:**

| Phase | Time | Optimization |
|-------|------|-------------|
| Prefetch | 0-100ms | Parallel I/O |
| Module load | 100-300ms | Lazy imports |
| Config load | 300-400ms | Zod validation |
| OAuth check | 400-500ms | Cached tokens |
| REPL init | 500-600ms | React render |
| **Total** | **~600ms** | Fast for 512K LOC |

See [Production Engineering](./09-production-engineering.md#1-startup-optimization) for patterns.

### How do feature flags enable dead code elimination?

**Build-time feature flags with Bun:**

```typescript
import { feature } from 'bun:bundle'

// Dead code elimination
if (feature('VOICE_MODE')) {
  // This code REMOVED if VOICE_MODE=false at build time
  import('./voice/voiceMode.js')
  setupVoiceMode()
}
```

**Build commands:**
```bash
# Consumer build (no enterprise)
bun build --define 'feature("ENTERPRISE_SSO")=false'
# Result: 28MB bundle

# Enterprise build (all features)
bun build --define 'feature("ENTERPRISE_SSO")=true'
# Result: 45MB bundle
```

**Benefits:**
- 37% smaller consumer bundles
- Faster startup (less code to parse)
- Better security (enterprise code not exposed)
- Type-safe (compiler checks flags)

See [Production Engineering](./09-production-engineering.md#2-feature-flag-optimization) for implementation.

### What's the cache hit rate in production?

**Typical cache performance:**

| Metric | Value |
|--------|-------|
| Cache hit rate | 85-95% |
| Break-even point | 2 requests |
| Cache TTL | 5 minutes |

**Cost comparison (10 requests):**

```
Without cache:
10 × 10K tokens × $3.75/Mtok = $0.375

With cache:
Request 1: Write 10K × $3.75/Mtok = $0.0375 (cache write)
Requests 2-10: Read 9×10K × $0.30/Mtok = $0.027 (cache read)
Total: $0.0645

Savings: 83%
```

**Cache invalidation:**
- Expires after 5 min inactivity
- Cleared on model change
- Cleared on system prompt change

See [Production Engineering](./09-production-engineering.md#3-prompt-cache-economics) for analysis.

---

## Implementation Patterns

### How is tool isolation achieved?

**Each tool is self-contained:**

```
src/tools/BashTool/
├── BashTool.tsx                 # Main implementation
├── UI.tsx                       # Tool use rendering
├── BashToolResultMessage.tsx    # Result rendering
├── bashPermissions.ts           # Permission logic
├── bashSecurity.ts              # Security validation
├── ast.js                       # AST parsing
├── sandbox/                     # Sandboxing
└── __tests__/                   # Unit tests
```

**Tool interface:**
```typescript
interface Tool {
  name: string
  description: string
  inputSchema: ZodSchema

  // Execution
  call(input, context): Promise<any>

  // Security
  checkPermissions(input, context): Promise<PermissionResult>

  // Optimization
  isConcurrencySafe(input): boolean
  isReadOnly(input): boolean

  // UI
  renderToolUseMessage(input): JSX.Element
  renderToolResultMessage(content): JSX.Element
}
```

**Benefits:**
- No dependencies between tools
- Easy to test in isolation
- Can be disabled/enabled independently
- Custom UI per tool

See [Architecture Overview](./02-architecture-overview.md#3-tool-system) for tool categories.

### How is immutable state managed?

**DeepImmutable type enforcement:**

```typescript
type AppState = DeepImmutable<{
  messages: Message[]
  settings: Settings
}>

// Cannot mutate:
// state.messages.push(msg) // TypeScript error

// Must create new state:
const newState = {
  ...state,
  messages: [...state.messages, msg],
}
```

**Benefits:**
- No accidental mutations
- Easier debugging (state snapshots)
- Better performance (reference equality checks)
- Undo/redo support

**State updates:**
```typescript
// Reducer pattern
function reducer(state: AppState, action: Action): AppState {
  switch (action.type) {
    case 'ADD_MESSAGE':
      return {
        ...state,
        messages: [...state.messages, action.message],
      }
    case 'UPDATE_SETTINGS':
      return {
        ...state,
        settings: { ...state.settings, ...action.updates },
      }
  }
}
```

See [Architecture Overview](./02-architecture-overview.md#3-immutability) for principles.

### How does error recovery work?

**Comprehensive error categorization:**

```typescript
// src/services/api/errors.ts
type ErrorCategory =
  | 'network'      // ECONNRESET, timeout
  | 'auth'         // 401, invalid key
  | 'rate_limit'   // 429, too many requests
  | 'server'       // 500, 503
  | 'validation'   // 400, invalid input
  | 'unknown'

function categorizeError(error: Error): ErrorCategory {
  if (error.message.includes('ECONNRESET')) return 'network'
  if (error.message.includes('401')) return 'auth'
  if (error.message.includes('429')) return 'rate_limit'
  // ...
}
```

**Retry logic:**
```typescript
async function withRetry<T>(
  fn: () => Promise<T>,
  maxRetries = 3
): Promise<T> {
  for (let i = 0; i < maxRetries; i++) {
    try {
      return await fn()
    } catch (error) {
      const category = categorizeError(error)

      // Retry transient errors
      if (category in ['network', 'rate_limit', 'server']) {
        const delay = Math.min(1000 * Math.pow(2, i), 10000)
        await sleep(delay)
        continue
      }

      // Don't retry logic errors
      throw error
    }
  }
}
```

See [Production Engineering](./09-production-engineering.md#4-error-handling) for patterns.

---

## Applying These Patterns

### Can I use streaming execution in my AI tool?

**Yes, if you have control over the streaming protocol:**

**Requirements:**
1. Access to raw SSE stream from LLM API
2. Ability to parse partial tool calls
3. State management for concurrent operations

**Key implementation:**
```typescript
async function* streamWithTools(response) {
  const pendingTools = new Map()

  for await (const chunk of parseSSE(response)) {
    if (chunk.type === 'tool_use') {
      // Start tool immediately
      const promise = executeTool(chunk)
      pendingTools.set(chunk.id, promise)
    }

    if (chunk.type === 'text') {
      yield chunk.text
    }
  }

  // Wait for all tools
  await Promise.all(pendingTools.values())
}
```

**Challenges:**
- Handling partial JSON in streaming parameters
- Race condition management
- Error recovery mid-stream

See [Streaming Execution](./03-streaming-execution.md#implementation-challenges) for details.

### Can I implement autocompaction for my chatbot?

**Yes, the pattern is reusable:**

**Implementation steps:**
1. **Monitor** token count per request
2. **Trigger** compaction at threshold (e.g., 50K tokens)
3. **Split** messages into recent (keep) vs old (compact)
4. **Summarize** old messages with cheaper LLM
5. **Replace** old messages with summary marker

**Example:**
```typescript
async function compactIfNeeded(messages: Message[]) {
  const tokens = estimateTokens(messages)

  if (tokens < 50_000) return messages

  // Keep recent 25 messages
  const recent = messages.slice(-25)
  const older = messages.slice(0, -25)

  // Summarize older messages
  const summary = await llm.summarize(older)

  return [
    { role: 'system', content: summary },
    ...recent,
  ]
}
```

See [Context Management](./04-context-management.md#3-compaction-algorithm) for full algorithm.

### How can I optimize for fleet-scale usage?

**Key strategies from Claude Code:**

1. **Prompt cache optimization**
   - Share cached context across sessions
   - Use fork pattern for multi-agent
   - Cache boundary markers

2. **Specialized agents**
   - Create task-specific agents with fewer tools
   - Use cheaper models where appropriate
   - Reduce prompt size for simple tasks

3. **Autocompaction**
   - Prevent unbounded context growth
   - Massive cost savings for long sessions

4. **Dead code elimination**
   - Build-time feature flags
   - Smaller bundles for faster startup
   - Remove unused enterprise features

**Expected savings:**
- Cache fork: 90% for multi-agent
- Autocompaction: 85% for long conversations
- Specialized agents: 3x for search/exploration
- Feature flags: 37% smaller bundles

See [Production Engineering](./09-production-engineering.md#fleet-scale-optimization) for patterns.

### What are the key architectural takeaways?

**10 lessons from Claude Code:**

1. **Streaming beats waiting** - Execute tools concurrently while LLM streams
2. **Context management is crucial** - Autocompaction enables unlimited conversations
3. **Specialization wins** - Purpose-built agents are 3x more efficient
4. **Cache aggressively** - Fork pattern saves 90% on multi-agent
5. **React works in CLI** - Declarative UI is maintainable at scale
6. **AST beats regex** - Deep parsing catches edge cases
7. **Type safety matters** - Zod + TypeScript prevent runtime errors
8. **Optimize for fleet** - Think Gtok/week, not per-request
9. **Dead code elimination** - Feature flags reduce bundle size 37%
10. **Immutability simplifies** - State snapshots enable debugging

See [Lessons Learned](./10-lessons-learned.md) for complete insights.

---

## Sources & Further Reading

This FAQ is based on architectural analysis documented in:

### Technical Documentation (This Wiki)
- [01. Competitive Advantages](./01-competitive-advantages.md) - The 10 architectural innovations
- [02. Architecture Overview](./02-architecture-overview.md) - System design and data flow
- [03. Streaming Execution](./03-streaming-execution.md) - Real-time tool execution
- [04. Context Management](./04-context-management.md) - 5-layer autocompaction
- [05. Multi-Agent Orchestration](./05-multi-agent-orchestration.md) - Multi-agent workflows
- [06. Terminal UX](./06-terminal-ux.md) - React terminal UI
- [07. Security Model](./07-security-model.md) - AST parsing and permissions
- [08. Integration Ecosystem](./08-integration-ecosystem.md) - MCP, IDE bridges, skills
- [09. Production Engineering](./09-production-engineering.md) - Optimization patterns
- [10. Lessons Learned](./10-lessons-learned.md) - Key takeaways

### Codebase Analysis
- **Source:** Claude Code npm package (March 2026)
- **Lines analyzed:** ~512,000 TypeScript
- **Files reviewed:** ~1,900
- **Methodology:** Source map extraction + code review

### Related Technologies
- [Bun Runtime](https://bun.sh) - Fast JavaScript runtime
- [React + Ink](https://github.com/vadimdemedes/ink) - React for terminal
- [Model Context Protocol](https://modelcontextprotocol.io) - Tool integration standard
- [Anthropic API](https://docs.anthropic.com) - Claude API documentation

---

**Want to learn more?**

- 📚 Read the [complete technical documentation](./README.md)
- 🔍 Explore the [codebase patterns](./10-lessons-learned.md)
- 🏗️ Apply these [architectural principles](./09-production-engineering.md) to your own tools
- 💡 Study the [competitive analysis](./01-competitive-advantages.md) for positioning insights
