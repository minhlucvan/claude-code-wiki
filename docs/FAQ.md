# Claude Code: Frequently Asked Questions

> **Quick answers to common developer questions about Claude Code**

This FAQ provides practical, actionable answers to the most common questions developers ask when learning Claude Code. For deep technical details, see the [full documentation](./README.md).

## Table of Contents

- [Getting Started](#getting-started)
- [Core Concepts](#core-concepts)
- [Workflow & Best Practices](#workflow--best-practices)
- [Integrations & Extensions](#integrations--extensions)
- [Performance & Optimization](#performance--optimization)
- [Troubleshooting](#troubleshooting)
- [Security & Permissions](#security--permissions)
- [Advanced Topics](#advanced-topics)
- [Enterprise & Fleet Management](#enterprise--fleet-management)
- [Sources & Further Reading](#sources--further-reading)

---

## Getting Started

### How do I install Claude Code?

**Via npm (recommended):**
```bash
npm install -g @anthropic/claude-code
```

**Via native installer:**
- macOS: Download from [claude.com/code](https://claude.com/code)
- Windows: Download from [claude.com/code](https://claude.com/code)
- Linux: Use npm or build from source

**Common issues:**
- **Permission errors**: Don't use `sudo npm install`. Fix npm permissions following [npm docs](https://docs.npmjs.com/resolving-eacces-permissions-errors-when-installing-packages-globally)
- **Windows**: Run terminal as Administrator for initial install
- **macOS**: May need to allow app in System Preferences > Security

See [Architecture Overview](./02-architecture-overview.md#runtime) for technical details.

### What are the system requirements?

**Minimum:**
- Node.js 18+ or Bun 1.0+
- 4GB RAM
- macOS 10.15+, Windows 10+, or Linux

**Recommended:**
- Bun runtime (2x faster startup)
- 8GB RAM for large codebases
- SSD for better file I/O performance

**Storage:** ~80MB for core installation, ~200MB with all MCP servers

### How do I configure CLAUDE.md?

Create `CLAUDE.md` in your project root:

```markdown
# Project: My Web App

## Tech Stack
- Next.js 14 with App Router
- TypeScript 5.0
- Tailwind CSS
- PostgreSQL with Prisma

## Coding Style
- Use functional components with hooks
- Prefer server components by default
- Always include TypeScript types
- Follow Airbnb style guide

## Important Context
- API routes in `app/api/`
- Database schema in `prisma/schema.prisma`
- Shared components in `components/ui/`

## Do NOT modify
- `package-lock.json` (use yarn)
- `prisma/migrations/` (create new migrations instead)
```

**Why Claude ignores CLAUDE.md:**
- File not in project root (must be exactly `CLAUDE.md`)
- Claude hasn't read it yet - explicitly ask "read CLAUDE.md first"
- Too vague - be specific about tech stack and patterns

See [Best Practices](https://code.claude.com/docs/en/best-practices) for examples.

### How do I authenticate?

**Via OAuth (recommended):**
```bash
claude login
```
Opens browser for authentication. Token stored securely in system keychain.

**Via API key:**
```bash
export ANTHROPIC_API_KEY=sk-ant-...
claude
```

**Check auth status:**
```bash
claude whoami
```

See [Architecture Overview](./02-architecture-overview.md#oauth-20) for PKCE flow details.

---

## Core Concepts

### What's the difference between streaming execution and traditional LLM tools?

**Traditional tools (sequential):**
```
[Wait 2s for LLM] → [Execute tool 1] → [Execute tool 2] → [Send results]
Total: 6-8 seconds
```

**Claude Code (streaming):**
```
[LLM starts streaming]
  ↓ (0.5s) Tool 1 detected → Execute immediately
  ↓ (1.0s) Tool 2 detected → Execute in parallel
  ↓ (2.0s) LLM completes, tools already done
Total: 2-3 seconds (2-5x faster)
```

**Key benefits:**
- Tools execute while LLM streams (no waiting)
- Safe operations run concurrently (FileRead, Grep, Glob)
- Real-time progress feedback in UI

See [Streaming Execution](./03-streaming-execution.md) for benchmarks.

### How does context management work with autocompaction?

**5-layer progressive compaction:**

```
Layer 1 (50 msgs):  Keep all messages
Layer 2 (100 msgs): Recent 25 + Compact 25→5 tokens
Layer 3 (200 msgs): Recent 25 + Mid 25→5 + Old 50→5
Layer 4 (400 msgs): Recent 25 + 3 compaction layers (175→15)
Layer 5 (500+ msgs): Recent 25 + 4 compaction layers (375→20)
```

**Result:** Unlimited conversation length without manual cleanup.

**Cost savings:** 85% reduction for long conversations (500+ messages).

See [Context Management](./04-context-management.md) for implementation details.

### What is the prompt cache fork pattern?

**Normal approach (expensive):**
```
Agent 1: Create cache (10K tokens) = $0.0375
Agent 2: Create cache (10K tokens) = $0.0375
Agent 3: Create cache (10K tokens) = $0.0375
Total: $0.1125
```

**Fork pattern (efficient):**
```
Base: Create cache once (10K tokens) = $0.0375
Agent 1: Read cache (10K tokens) = $0.003
Agent 2: Read cache (10K tokens) = $0.003
Agent 3: Read cache (10K tokens) = $0.003
Total: $0.0465 (59% savings)
```

**At scale:** $24K/year savings for 1000 multi-agent tasks/day.

See [Competitive Advantages](./01-competitive-advantages.md#3-prompt-cache-fork-optimization) for details.

### How do multi-agent workflows save costs?

**Specialized agents use fewer tools:**

- **General-purpose agent:** 40 tools, larger prompts, slower, more expensive
- **Explore agent:** 8 tools (Glob, Grep, Read only), 3x faster, 3x cheaper

**Example task:** "Find all API endpoints"
- General-purpose: $0.15, 45 seconds
- Explore agent: $0.05, 15 seconds

**With cache fork:** Shared context across agents reduces cost by 90%.

See [Multi-Agent Orchestration](./05-multi-agent-orchestration.md) for architecture.

---

## Workflow & Best Practices

### When should I use Plan Mode?

**Use Plan Mode for:**
- New feature implementation (unclear approach)
- Multi-file changes (3+ files affected)
- Architectural decisions (multiple valid approaches)
- Bug fixes requiring investigation
- Refactoring existing code

**Example:**
```
User: "Add user authentication"
Claude: [Enters Plan Mode]
  - Analyzes codebase structure
  - Proposes JWT vs session approach
  - Identifies files to modify
  - Gets user approval before coding
```

**According to best practices:** 80% of sessions should use Plan Mode to ensure alignment before implementation.

**Don't use Plan Mode for:**
- Simple one-line fixes
- Adding console.log for debugging
- Obvious typo corrections

See [Architecture Overview](./02-architecture-overview.md#2-query-engine) for implementation.

### How do I prevent context window degradation?

**Claude Code does this automatically** via autocompaction. No action needed.

**Manual optimization (optional):**
```bash
/clear              # Clear conversation (lose all context)
/compact            # Manually trigger compaction (usually automatic)
/remember [key]     # Save important context explicitly
```

**Signs you need /clear:**
- Conversation has drifted off-topic
- Working on completely unrelated tasks
- Context from hours ago is no longer relevant

**Best practice:** Let autocompaction handle it. Only use `/clear` when starting a new unrelated task.

### When should I run /clear?

**Run /clear when:**
- Starting a completely different project
- Context from previous task is irrelevant
- Conversation has become confused or off-track

**Don't run /clear when:**
- Just reached 50-100 messages (autocompaction handles this)
- Working on related tasks in same codebase
- Want to preserve any previous context

**Example workflow:**
```bash
# Morning: Working on authentication
$ claude
> "Add JWT authentication"
[150 messages, autocompaction at msg 50 and 100]

# Afternoon: Switching to different project
$ /clear
> "Now help with my Python data pipeline"
```

See [Context Management](./04-context-management.md#the-problem-context-window-limits) for automatic vs manual strategies.

### Should I use bypass permissions mode?

**Permission modes:**

| Mode | When to Use | Risk Level |
|------|-------------|-----------|
| **Ask** (default) | Learning, careful work | Low |
| **Allow** | Trusted operations | Medium |
| **Bypass** | Rapid prototyping, scripts | High |
| **Deny** | Read-only exploration | Zero |

**Bypass mode pros:**
- Faster workflow (no interruptions)
- Better for rapid iteration

**Bypass mode cons:**
- Can execute destructive commands
- No safety net for mistakes

**Recommendation:**
- **Development:** Use Ask or Allow
- **Production:** Never use Bypass
- **Scripts/automation:** Bypass with careful review

See [Security Model](./07-security-model.md) for AST-based permission system.

### How do I debug errors using MCP?

**Enable MCP debug mode:**
```bash
export MCP_DEBUG=1
claude
```

**View Chrome DevTools-style logs:**
```bash
# In another terminal
tail -f ~/.claude/logs/mcp-debug.log
```

**Common MCP errors:**

| Error | Cause | Fix |
|-------|-------|-----|
| `MCP server not found` | Server not installed | `npm install -g @modelcontextprotocol/server-*` |
| `Connection timeout` | Server crashed | Check server logs, restart Claude |
| `Tool not available` | Wrong server config | Verify `claude.json` MCP settings |
| `Authentication failed` | Missing credentials | Set env vars (e.g., `DATABASE_URL`) |

**Check MCP server status:**
```bash
/mcp-list           # List connected servers
/mcp-install [pkg]  # Install new server
/mcp-remove [name]  # Remove server
```

See [Integration Ecosystem](./08-integration-ecosystem.md#mcp-client) for MCP architecture.

---

## Integrations & Extensions

### How do I build a custom MCP server?

**Minimal MCP server (TypeScript):**

```typescript
// my-tools-server.ts
import { Server } from '@modelcontextprotocol/sdk/server/index.js'
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js'

const server = new Server({
  name: 'my-tools',
  version: '1.0.0',
}, {
  capabilities: {
    tools: {},
  },
})

// Define tool
server.setRequestHandler('tools/list', async () => ({
  tools: [{
    name: 'greet',
    description: 'Greet someone',
    inputSchema: {
      type: 'object',
      properties: {
        name: { type: 'string' },
      },
      required: ['name'],
    },
  }],
}))

// Implement tool
server.setRequestHandler('tools/call', async (request) => {
  if (request.params.name === 'greet') {
    const { name } = request.params.arguments
    return {
      content: [{ type: 'text', text: `Hello, ${name}!` }],
    }
  }
})

// Start server
const transport = new StdioServerTransport()
await server.connect(transport)
```

**Register in `~/.claude/config.json`:**
```json
{
  "mcpServers": {
    "my-tools": {
      "command": "node",
      "args": ["/path/to/my-tools-server.ts"]
    }
  }
}
```

See [MCP documentation](https://modelcontextprotocol.io/docs) for full API.

### Can I use Claude Code with VS Code?

**Yes, via Bridge Mode:**

```bash
# Terminal 1: Start Claude Code in bridge mode
claude --bridge

# VS Code: Install Claude Code extension
# Extension connects to running bridge
```

**Bridge mode allows:**
- Use Claude Code tools in VS Code
- Share conversation between terminal and IDE
- Leverage both UX paradigms simultaneously

**Limitations:**
- Requires Claude Code running in terminal
- Some terminal-specific features unavailable in IDE

See [Integration Ecosystem](./08-integration-ecosystem.md#ide-bridges) for architecture.

### How do I create custom skills?

**Skill anatomy:**

```
.claude/skills/my-skill/
├── SKILL.md           # Skill documentation
├── prompts/
│   └── system.md      # System prompt for skill
├── references/        # Reference docs
│   └── api.md
└── _meta.json         # Skill metadata
```

**Example skill metadata (`_meta.json`):**
```json
{
  "name": "my-skill",
  "version": "1.0.0",
  "description": "Custom workflow for my project",
  "allowedTools": ["FileRead", "Bash", "Grep"],
  "requiredFeature": null
}
```

**System prompt (`prompts/system.md`):**
```markdown
You are an expert in running my custom workflow.

When the user invokes /my-skill:
1. Read project configuration
2. Run validation checks
3. Generate report
```

**Invoke skill:**
```bash
/my-skill
```

See [Integration Ecosystem](./08-integration-ecosystem.md#skill-system) for conditional loading.

### How do I integrate with CI/CD pipelines?

**Headless automation:**

```bash
# Non-interactive mode
echo "Run tests and fix failures" | claude --headless --project=/path/to/repo
```

**GitHub Actions example:**
```yaml
name: Claude Code Review
on: [pull_request]

jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - run: npm install -g @anthropic/claude-code
      - run: |
          echo "Review this PR for issues" | \
          claude --headless --project=$GITHUB_WORKSPACE
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
```

**Best practices:**
- Use `--headless` for non-interactive
- Set `--max-turns` to limit API calls
- Use `--permissions=bypass` with caution
- Capture output to file for review

See [Production Engineering](./09-production-engineering.md) for fleet-scale patterns.

---

## Performance & Optimization

### Why is my conversation getting slower?

**Likely causes:**

1. **Context window filling up** (rare - autocompaction prevents this)
2. **Large file reads** in conversation history
3. **Many MCP servers** loading on startup
4. **Slow tool execution** (network requests, heavy computation)

**Check token usage:**
```bash
/tokens             # Show current conversation tokens
/cost               # Show total cost and token breakdown
```

**Solutions:**

```bash
/clear              # Nuclear option: start fresh
/compact            # Manually trigger compaction (usually automatic)
/mcp-remove [slow]  # Disable slow MCP servers
```

**Expected performance:**
- Fresh conversation: <100ms response start
- 100 messages: ~200ms response start (autocompaction at 50)
- 500+ messages: ~300ms response start (multiple compactions)

See [Architecture Overview](./02-architecture-overview.md#performance-characteristics) for benchmarks.

### How much does autocompaction cost vs. benefit?

**Cost breakdown for 500-message conversation:**

| Item | Without Compaction | With Compaction | Savings |
|------|-------------------|-----------------|---------|
| Input tokens/request | 500K | 30K | 94% |
| Input cost/request | $1.50 | $0.09 | 94% |
| Compaction LLM calls | $0 | $0.75 (10 calls) | -$0.75 |
| **Total (500 requests)** | **$750** | **$45.75** | **94%** |

**Compaction triggers:**
- Every ~50 messages
- Uses Haiku (cheaper model) for summarization
- ~5K output tokens per compaction = $0.075

**Net benefit:** Massive savings despite compaction costs.

**With prompt cache:** Additional 78% savings on cache reads.

See [Context Management](./04-context-management.md#token-economics) for detailed analysis.

### What's the cache hit rate in production?

**Typical cache performance:**

| Metric | Value |
|--------|-------|
| Cache hit rate | 85-95% |
| Cache write cost | $3.75/Mtok |
| Cache read cost | $0.30/Mtok (92% discount) |
| Break-even point | 2 requests (cache + 1 read) |

**Example session (10 requests):**

```
Request 1: Write cache (10K tokens) = $0.0375
Requests 2-10: Read cache (9 × 10K × $0.30/Mtok) = $0.027

Total: $0.0645
Without cache: 10 × 10K × $3.75/Mtok = $0.375
Savings: 83%
```

**Cache invalidation:**
- Expires after 5 minutes of inactivity
- Cleared on model change
- Cleared on system prompt change

See [Competitive Advantages](./01-competitive-advantages.md#3-prompt-cache-fork-optimization) for fork pattern.

### How do I optimize for my workflow?

**Profile your usage:**
```bash
/debug              # Show performance metrics
/cost --breakdown   # Show cost by tool/agent
```

**Optimization strategies:**

**For read-heavy workflows (exploration):**
- Use Explore agent (`/explore` or Task tool with `subagent_type=Explore`)
- 3x faster, 3x cheaper than general-purpose

**For multi-agent tasks:**
- Ensure cache fork pattern is working
- Check cache hit rate with `/cost --cache`

**For long conversations:**
- Let autocompaction work (don't manually `/clear` too often)
- Use `/remember` for critical context to survive compaction

**For fast iteration:**
- Use `--permissions=allow` or `bypass` to reduce prompts
- Disable unused MCP servers

**For cost control:**
- Use Haiku model for simple tasks (`/model haiku`)
- Set `--max-tokens` limit for responses
- Use Explore agent for codebase navigation

See [Production Engineering](./09-production-engineering.md#cost-optimization) for fleet-scale patterns.

---

## Troubleshooting

### Why does Claude ignore my CLAUDE.md instructions?

**Common reasons:**

1. **File not in project root**
   - Must be exactly `CLAUDE.md` in `$(pwd)`
   - Check: `ls CLAUDE.md` should show the file

2. **Claude hasn't read it yet**
   - Solution: "Read CLAUDE.md first, then help with X"
   - Or: Add to system prompt via `/config`

3. **Instructions too vague**
   - Bad: "Use good coding practices"
   - Good: "Always use TypeScript strict mode, prefer functional components"

4. **Conflicting with model's training**
   - Model may override if instructions contradict best practices
   - Solution: Be explicit about project-specific patterns

**Debug CLAUDE.md:**
```bash
/ask "What's in CLAUDE.md?"
# If Claude can't answer, it hasn't read the file
```

See [Best Practices](https://code.claude.com/docs/en/best-practices) for example CLAUDE.md files.

### What happens when tool execution fails mid-stream?

**Claude Code handles failures gracefully:**

1. **Error detected** during tool execution
2. **Cancel dependent tools** that rely on failed tool
3. **Report error to LLM** as tool result
4. **Continue streaming** (don't crash entire conversation)
5. **LLM adapts** based on error message

**Example:**
```
User: "Fix TypeScript errors in src/"
[LLM streams]
  Tool 1: Bash(npm run typecheck) → ERROR "npm not found"
  Tool 2: FileEdit(main.ts) → CANCELLED (depends on Tool 1)
[LLM sees error]
  "I see npm isn't installed. Would you like to install dependencies first?"
```

**Retry logic:**
- Transient errors (network timeout, 503): Auto-retry 3x
- Logic errors (file not found, syntax error): Report immediately

See [Streaming Execution](./03-streaming-execution.md#error-recovery) for implementation.

### How do I recover from permission errors?

**Permission error scenarios:**

1. **Command blocked by security**
   ```bash
   # Detected dangerous command
   $ rm -rf ../../../
   ❌ BLOCKED: Path traversal outside project
   ```

   **Solution:** Use safer alternative or adjust permissions
   ```bash
   /permissions allow  # Allow this session
   /permissions bypass # Allow all (dangerous)
   ```

2. **File write permission denied**
   ```bash
   ❌ ERROR: EACCES /etc/hosts
   ```

   **Solution:** Fix file permissions
   ```bash
   sudo chown $USER /path/to/file
   # Or: Run Claude Code with appropriate permissions
   ```

3. **MCP tool requires auth**
   ```bash
   ❌ ERROR: Database connection failed
   ```

   **Solution:** Set environment variables
   ```bash
   export DATABASE_URL=postgres://...
   claude
   ```

See [Security Model](./07-security-model.md#4-permission-modes) for permission system details.

### Why are my MCP servers not loading?

**Diagnostic steps:**

1. **Check MCP configuration**
   ```bash
   /mcp-list
   # Should show all configured servers
   ```

2. **Verify server installation**
   ```bash
   npm list -g @modelcontextprotocol/server-*
   ```

3. **Check server logs**
   ```bash
   export MCP_DEBUG=1
   claude
   # Watch logs in another terminal:
   tail -f ~/.claude/logs/mcp-debug.log
   ```

4. **Test server independently**
   ```bash
   npx @modelcontextprotocol/server-postgres
   # Should start without errors
   ```

**Common fixes:**

| Issue | Fix |
|-------|-----|
| Server not installed | `npm install -g @modelcontextprotocol/server-*` |
| Wrong Node version | Update to Node.js 18+ |
| Missing environment vars | Set `DATABASE_URL`, `API_KEY`, etc. |
| Server crashes on start | Check server-specific requirements |
| Permission denied | Run with appropriate user permissions |

See [Integration Ecosystem](./08-integration-ecosystem.md#mcp-client) for MCP architecture.

---

## Security & Permissions

### How does the AST-based bash security work?

**Traditional security (regex):**
```bash
# Regex pattern: ^rm -rf
rm -rf ./temp          ✅ Allowed (doesn't match)
rm -rf "$(pwd)/../.."  ✅ Allowed (regex misses complexity)
```

**Claude Code (AST parsing):**
```bash
# Parse command into syntax tree
rm -rf "$(pwd)/../.."
  ├─ Command: rm
  ├─ Flags: [-rf]
  └─ Argument: CommandSubstitution
       ├─ Command: pwd
       └─ PathTraversal: ../..

Risk: HIGH (destructive command + path escape)
Action: ❌ BLOCK
```

**Benefits:**
- Detects obfuscated commands
- Understands command substitution
- Analyzes pipe chains
- Catches path traversal

See [Security Model](./07-security-model.md#ast-level-bash-parsing) for implementation.

### What are the 4 permission modes?

| Mode | Behavior | Use Case |
|------|----------|----------|
| **Ask** | Prompt for every tool | Learning, careful work |
| **Allow** | Auto-allow safe tools, ask for risky | Balanced workflow |
| **Bypass** | Allow everything | Rapid prototyping (risky) |
| **Deny** | Block all tools | Read-only exploration |

**Set permission mode:**
```bash
/permissions ask     # Default: ask for everything
/permissions allow   # Auto-allow safe operations
/permissions bypass  # Allow all (DANGEROUS)
/permissions deny    # Block all modifications
```

**Tool risk levels:**
- **Safe:** FileRead, Grep, Glob (read-only)
- **Medium:** FileEdit, FileWrite (file modifications)
- **High:** Bash with destructive commands (rm, dd, etc.)

See [Security Model](./07-security-model.md#4-permission-modes) for risk assessment.

### How do I audit what agents did in a conversation?

**View conversation transcript:**
```bash
/save conversation.jsonl    # Save full conversation
```

**Parse tool usage:**
```bash
# Extract tool calls from transcript
cat conversation.jsonl | jq 'select(.type=="tool_use") | {tool: .name, input: .input}'
```

**Session recording (enterprise):**
```json
// MDM policy
{
  "sessionRecording": true,
  "recordingPath": "/var/log/claude-sessions/",
  "includeToolResults": true
}
```

**Built-in audit log:**
```bash
/debug --show-tools     # Show all tools used this session
/cost --by-tool         # Show cost breakdown by tool
```

See [Production Engineering](./09-production-engineering.md#fleet-management-features) for enterprise audit features.

### Can I prevent specific commands from running?

**Yes, via permission hooks or MDM policies:**

**Permission hook (`.claude/hooks/pre-bash.sh`):**
```bash
#!/bin/bash
# Block specific commands

if echo "$1" | grep -q "npm publish"; then
  echo "❌ BLOCKED: npm publish not allowed"
  exit 1
fi

# Allow other commands
exit 0
```

**MDM policy (enterprise):**
```json
{
  "blockedCommands": [
    "npm publish",
    "git push --force",
    "rm -rf /",
    "dd if=/dev/zero"
  ],
  "allowedDomains": ["company.com", "github.com"],
  "maxFileSize": "10MB"
}
```

**Tool-specific restrictions:**
```bash
/config set tools.Bash.enabled false    # Disable Bash entirely
/config set tools.FileWrite.readonly true # Block file writes
```

See [Security Model](./07-security-model.md#mdm-policy-enforcement) for enterprise policies.

---

## Advanced Topics

### How do specialized agents work?

**6 specialized agent types:**

| Agent | Tools Available | Use Case | Model |
|-------|----------------|----------|-------|
| **general-purpose** | All 40 tools | Complex multi-step tasks | Sonnet |
| **Explore** | Glob, Grep, Read, WebFetch, WebSearch | Fast codebase navigation | Haiku |
| **Plan** | Glob, Grep, Read, Task, AskUserQuestion | Implementation planning | Sonnet |
| **Bash** | Bash only | Command execution | Haiku |
| **statusline-setup** | Read, Edit | Config file editing | Haiku |
| **claude-code-guide** | Glob, Grep, Read, WebFetch, WebSearch | Documentation Q&A | Haiku |

**Performance comparison:**

```typescript
// Task: "Find all API endpoints"

// General-purpose agent (slow)
Tools: [Glob, Grep, Read, FileEdit, Bash, ...]  // 40 tools
Tokens: 50K (all tool definitions)
Cost: $0.15
Time: 45s

// Explore agent (fast)
Tools: [Glob, Grep, Read, WebFetch, WebSearch]  // 8 tools
Tokens: 15K (fewer tool definitions)
Cost: $0.05
Time: 15s

Speedup: 3x faster, 3x cheaper
```

See [Competitive Advantages](./01-competitive-advantages.md#7-6-specialized-agents) for details.

### What's the cache fork optimization?

**Problem:** Multiple agents creating duplicate caches

**Without fork pattern:**
```typescript
Agent 1: Create cache (base context) = $0.0375
Agent 2: Create cache (base context) = $0.0375  // DUPLICATE
Agent 3: Create cache (base context) = $0.0375  // DUPLICATE
Total: $0.1125
```

**With fork pattern:**
```typescript
// 1. Create base cache once
Base context → Cache (10K tokens) = $0.0375

// 2. All agents read from cache
Agent 1: Read cache + new task = $0.003
Agent 2: Read cache + new task = $0.003
Agent 3: Read cache + new task = $0.003

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

// Spawn agent with cached prefix
const agent = createAgent({
  messages: [
    ...cachedBase,  // Will be cache-read
    { role: 'user', content: newTask }
  ]
})
```

See [Competitive Advantages](./01-competitive-advantages.md#3-prompt-cache-fork-optimization) for economics.

### How does dead code elimination work with feature flags?

**Build-time feature flags remove unused code:**

```typescript
// src/features.ts
import { feature } from 'bun:bundle'

if (feature('VOICE_MODE')) {
  // This code is REMOVED from bundle if VOICE_MODE=false
  import('./voice/voiceMode.js')
  setupVoiceMode()
}

if (feature('ENTERPRISE_SSO')) {
  // This code only in enterprise builds
  import('./enterprise/sso.js')
  setupSSOProvider()
}
```

**Build commands:**
```bash
# Consumer build (no enterprise features)
bun build --define 'feature("ENTERPRISE_SSO")=false'
# Result: 28MB bundle

# Enterprise build (all features)
bun build --define 'feature("ENTERPRISE_SSO")=true'
# Result: 45MB bundle
```

**Benefits:**
- **37% smaller** consumer bundles
- **Faster startup** (less code to parse)
- **Better security** (enterprise code not exposed)
- **Type-safe** (compiler checks feature flags)

See [Competitive Advantages](./01-competitive-advantages.md#8-feature-flag-dead-code-elimination) for details.

### How do I build custom React components for terminal UI?

**Claude Code uses React + Ink:**

```tsx
// .claude/components/CustomProgress.tsx
import { Box, Text } from 'ink'
import Spinner from 'ink-spinner'

interface Props {
  status: 'pending' | 'running' | 'complete'
  message: string
  percent?: number
}

export function CustomProgress({ status, message, percent }: Props) {
  return (
    <Box flexDirection="column">
      <Box>
        {status === 'running' && <Spinner type="dots" />}
        {status === 'complete' && <Text color="green">✓</Text>}
        {status === 'pending' && <Text color="gray">○</Text>}
        <Text> {message}</Text>
      </Box>

      {percent !== undefined && (
        <Box marginLeft={2}>
          <Text color="cyan">
            {'█'.repeat(Math.floor(percent / 5))}
            {'░'.repeat(20 - Math.floor(percent / 5))}
            {' '}{percent}%
          </Text>
        </Box>
      )}
    </Box>
  )
}
```

**Use in tool:**
```typescript
// .claude/tools/MyTool.tsx
import { CustomProgress } from '../components/CustomProgress'

export const MyTool = buildTool({
  renderToolUseMessage(input, options) {
    return <CustomProgress status="running" message="Processing..." />
  }
})
```

See [Terminal UX](./06-terminal-ux.md) for component architecture.

---

## Enterprise & Fleet Management

### How do I deploy Claude Code to a team?

**MDM-based deployment (recommended):**

1. **Create MDM policy:**
   ```json
   // /etc/claude/policy.json
   {
     "allowedTools": ["FileRead", "Grep", "Glob", "Bash"],
     "blockedCommands": ["npm publish", "git push --force"],
     "maxTokensPerRequest": 50000,
     "allowedDomains": ["company.com", "github.com"],
     "sessionRecording": true,
     "recordingPath": "/var/log/claude-sessions/",
     "requiredAuth": true,
     "licenseKey": "enterprise-key-..."
   }
   ```

2. **Deploy via package manager:**
   ```bash
   # Homebrew (macOS)
   brew install --cask claude-code

   # Chocolatey (Windows)
   choco install claude-code

   # APT (Linux)
   sudo apt install claude-code
   ```

3. **Configure via env vars:**
   ```bash
   # /etc/environment
   ANTHROPIC_API_KEY=sk-ant-...
   CLAUDE_MDM_POLICY=/etc/claude/policy.json
   CLAUDE_SESSION_RECORDING=1
   ```

See [Production Engineering](./09-production-engineering.md#fleet-management) for patterns.

### What metrics should I monitor?

**Key metrics for fleet management:**

```typescript
interface FleetMetrics {
  // Usage
  activeUsers: number
  sessionsPerDay: number
  avgSessionLength: number

  // Cost
  tokensPerDay: number
  costPerUser: number
  cacheHitRate: number

  // Performance
  avgResponseTime: number
  errorRate: number
  toolFailureRate: number

  // Security
  blockedCommands: number
  permissionViolations: number
  suspiciousActivity: number
}
```

**Monitoring dashboard:**
```bash
# View fleet metrics
claude-admin metrics --team=engineering

# Sample output:
Active users:        147
Sessions/day:        523
Tokens/day:          12.5M
Cost/day:            $37.50
Cache hit rate:      89%
Avg response time:   1.2s
Error rate:          0.3%
```

See [Production Engineering](./09-production-engineering.md#observability) for OpenTelemetry integration.

### How do I handle cost overruns?

**Cost control strategies:**

1. **Set token budgets:**
   ```json
   // MDM policy
   {
     "maxTokensPerRequest": 50000,
     "maxTokensPerUser": 1000000,  // 1M tokens/month
     "maxCostPerUser": 30.00        // $30/month
   }
   ```

2. **Use cheaper models:**
   ```bash
   /model haiku               # Switch to Haiku (90% cheaper)
   /config set defaultModel haiku
   ```

3. **Optimize agent usage:**
   - Use specialized agents (Explore, Bash) instead of general-purpose
   - Ensure cache fork pattern is working
   - Monitor cache hit rate

4. **Alert on overruns:**
   ```typescript
   // Cost monitoring webhook
   if (userCostThisMonth > budgetLimit) {
     sendAlert({
       user: user.email,
       cost: userCostThisMonth,
       limit: budgetLimit,
       action: 'rate_limit_enabled'
     })
   }
   ```

See [Competitive Advantages](./01-competitive-advantages.md#10-fleet-scale-economics) for cost optimization patterns.

### What's the SLA for enterprise deployments?

**Anthropic enterprise SLA (typical):**

- **Uptime:** 99.9% (API availability)
- **Latency:** p50 < 500ms, p99 < 2s
- **Support:** 24/7 enterprise support
- **Rate limits:** Custom limits for enterprise
- **Security:** SOC 2 Type II, ISO 27001
- **Data residency:** Regional deployment options

**Claude Code-specific:**

- **Update frequency:** Monthly releases
- **Security patches:** Within 48h of disclosure
- **Breaking changes:** 90-day deprecation notice
- **Feature flags:** Gradual rollout for enterprise

**Monitoring:**
```bash
# Check Claude Code health
claude-admin health

# Sample output:
API Status:          ✓ Operational
Cache Service:       ✓ Operational
MCP Servers:         ✓ All connected (5/5)
Telemetry:           ✓ Operational
Last updated:        2026-04-02 10:23:45 UTC
```

See [Anthropic Enterprise](https://www.anthropic.com/enterprise) for official SLA details.

---

## Sources & Further Reading

This FAQ synthesizes information from:

### Official Documentation
- [Claude Code Best Practices](https://code.claude.com/docs/en/best-practices)
- [Anthropic API Documentation](https://docs.anthropic.com)
- [Model Context Protocol (MCP) Specification](https://modelcontextprotocol.io)

### Educational Resources (2026)
- [Claude Code CLI & Workflow Mastery: Interview Questions 2026](https://www.udemy.com/course/claude-code-cli-workflow-mastery-interview-questions-2026/)
- [The Claude Code Handbook](https://www.freecodecamp.org/news/claude-code-handbook/)
- [How I use Claude Code](https://www.builder.io/blog/claude-code)

### Developer Community
- [Claude Code: The Most Common Questions Beginners Ask](https://every.to/source-code/claude-code-the-most-common-questions-beginners-ask)
- [Best Practices for Claude Code](https://code.claude.com/docs/en/best-practices)
- [Claude Code GitHub Discussions](https://github.com/anthropics/claude-code/discussions)

### Technical Deep-Dives (This Wiki)
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

---

**Have more questions?**

- 📚 Read the [full technical documentation](./README.md)
- 🐛 Report issues at [github.com/anthropics/claude-code/issues](https://github.com/anthropics/claude-code/issues)
- 💬 Join discussions at [github.com/anthropics/claude-code/discussions](https://github.com/anthropics/claude-code/discussions)
- 📖 Learn more at [claude.com/code](https://claude.com/code)
