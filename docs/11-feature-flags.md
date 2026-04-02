# Feature Flags & Configuration

## Overview

Claude Code uses a sophisticated **4-layer feature flag system** to control feature rollouts, A/B testing, and experimental functionality. This multi-layered approach provides flexibility for different use cases:

1. **Build-time flags** - Compiled out via dead code elimination for performance
2. **Runtime GrowthBook flags** - A/B testing and gradual rollouts with caching
3. **Environment variable flags** - Developer overrides and experimental opt-ins
4. **Beta headers** - API feature negotiation with Claude API

This document serves as the **single source of truth** for understanding which features are active, experimental, or deprecated across Claude Code.

---

## 1. Build-Time Feature Flags

Build-time flags are defined in `src/utils/config.ts` and use the `feature()` function with `bun:bundle` for compile-time dead code elimination. These flags are **compiled out** at build time when disabled, reducing bundle size.

### Active Production Flags

| Flag | Purpose | Default | Location |
|------|---------|---------|----------|
| `TEAMMATE` | Multi-agent teammate functionality | ✅ On | config.ts |
| `TRANSCRIPT_CLASSIFIER` | Auto-mode classification system | ✅ On | config.ts |
| `FAST_MODE` | Fast mode support | ✅ On | config.ts |
| `CONNECTOR_TEXT` | Connector text summarization | ✅ On | config.ts |
| `AGENT_SWARMS` | Agent teams/swarms coordination | ✅ On | config.ts |
| `AGENT_HANDOFF` | Agent-to-agent handoff | ✅ On | config.ts |
| `KAIROS_CHANNEL_NOTIFICATIONS` | Kairos channel notification system | ✅ On | config.ts |

### Experimental Flags

| Flag | Purpose | Default | Status |
|------|---------|---------|--------|
| `VOICE_MODE` | Voice interaction capabilities | ❌ Off | Experimental |
| `KAIROS` | Kairos orchestration mode | ❌ Off | Experimental |
| `COORDINATOR_MODE` | Multi-agent coordinator | ❌ Off | Experimental |
| `KAIROS_AGENT_OVERRIDE` | Override agent selection in Kairos | ❌ Off | Experimental |

### Usage Pattern

```typescript
import { feature } from '@/utils/config';

// Check if a feature is enabled at compile time
if (feature('TEAMMATE')) {
  // This code is included in the bundle
  enableTeammateFeatures();
} else {
  // This code is completely eliminated from the bundle
  disableTeammateFeatures();
}
```

### Key Implementation Details

- **Compile-time elimination**: When a flag is `false`, the entire conditional block is removed from the bundle
- **Zero runtime cost**: No performance impact for disabled features
- **Defined in**: `src/utils/config.ts` (lines 600-700)
- **Bundle optimization**: Uses `bun:bundle` feature detection

---

## 2. Runtime GrowthBook Flags

GrowthBook flags enable A/B testing and gradual feature rollouts with user-based targeting. These flags are evaluated at **runtime** and can be overridden by Anthropic users.

### Active Production Flags

| Flag | Purpose | Type | Override |
|------|---------|------|----------|
| `tengu_amber_flint` | Agent teams killswitch | Boolean | Ant users can override |
| `tengu_auto_mode_config` | Auto mode allowlist configuration | JSON | Ant users can override |
| `fast_mode_bypass_allowlist` | Fast mode availability override | JSON | Ant users can override |

### Experimental Flags

| Flag | Purpose | Status |
|------|---------|--------|
| `tengu_slate_prism` | Connector text summarization toggle | Experimental |
| `tengu_harbor` | Kairos channel notifications | Experimental |
| `tengu_willow_echo` | Agent handoff features | Experimental |

### Usage Pattern

```typescript
import { getFeatureValue_CACHED_MAY_BE_STALE } from '@/services/analytics/growthbook';

// Get a boolean flag (may be stale, uses cache)
const isAgentTeamsEnabled = getFeatureValue_CACHED_MAY_BE_STALE(
  'tengu_amber_flint',
  true // default value if flag not found
);

// Get a JSON flag with configuration
const autoModeConfig = getFeatureValue_CACHED_MAY_BE_STALE(
  'tengu_auto_mode_config',
  { allowlist: [] }
);
```

### Caching Behavior

- **Cache duration**: Flags are cached to avoid excessive API calls
- **Staleness warning**: Function name includes `MAY_BE_STALE` as a reminder
- **Ant user overrides**: Anthropic employees can override flags via internal tools
- **User targeting**: Supports user-based targeting for gradual rollouts

### Implementation Location

- **Service**: `src/services/analytics/growthbook.ts`
- **Integration**: GrowthBook SDK with feature value caching
- **Override mechanism**: Internal Anthropic user override system

---

## 3. Environment Variable Flags

Environment variables provide developer overrides and experimental feature opt-ins. These are **runtime flags** that can be set in shell configuration.

### Disable Flags

| Variable | Purpose | Effect When Set |
|----------|---------|-----------------|
| `CLAUDE_CODE_DISABLE_FAST_MODE` | Disable fast mode | Fast mode unavailable |
| `CLAUDE_CODE_DISABLE_EXPERIMENTAL_BETAS` | Disable experimental beta headers | No experimental API features |
| `DISABLE_PROMPT_CACHING` | Disable prompt caching | Forces fresh prompts every time |
| `CLAUDE_CODE_DISABLE_CONTEXT_MANAGEMENT` | Disable context management | No automatic context pruning |

### Experimental Opt-In Flags

| Variable | Purpose | Status |
|----------|---------|--------|
| `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS` | Enable agent teams | Experimental |
| `USE_CONNECTOR_TEXT_SUMMARIZATION` | Enable connector text summarization | Experimental |
| `CLAUDE_CODE_EXPERIMENTAL_AFK_MODE` | Enable AFK mode | Experimental |

### API Provider Flags

| Variable | Purpose | Use Case |
|----------|---------|----------|
| `CLAUDE_CODE_USE_BEDROCK` | Use AWS Bedrock API | AWS deployments |
| `CLAUDE_CODE_USE_VERTEX` | Use Google Vertex AI | GCP deployments |
| `ANTHROPIC_API_KEY` | Direct API key authentication | Development, testing |

### Development & Debugging Flags

| Variable | Purpose | Effect |
|----------|---------|--------|
| `CLAUDE_CODE_DEBUG` | Enable debug logging | Verbose output |
| `CLAUDE_CODE_VERBOSE` | Enable verbose mode | Additional logging |
| `LOG_LEVEL` | Set log level | Controls logging verbosity |
| `NODE_ENV` | Environment mode | `development` or `production` |

### Usage Pattern

```typescript
import { isEnvTruthy } from '@/utils/env';

// Check if environment variable is set to truthy value
if (isEnvTruthy(process.env.CLAUDE_CODE_DISABLE_FAST_MODE)) {
  // Fast mode is disabled
  disableFastMode();
}

// Direct environment variable check
if (process.env.ANTHROPIC_API_KEY) {
  // Use direct API key authentication
  useDirectAuth();
}
```

### Setting Environment Variables

```bash
# In ~/.bashrc or ~/.zshrc
export CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=true
export CLAUDE_CODE_DISABLE_FAST_MODE=false

# Or for a single session
CLAUDE_CODE_DEBUG=true claude-code
```

---

## 4. Beta Headers (API Features)

Beta headers are sent with API requests to negotiate feature availability with the Claude API. These enable **API-level features** that require server-side support.

### Production Beta Headers

| Beta Header | Purpose | Status |
|-------------|---------|--------|
| `claude-code-20250219` | Main Claude Code feature set | Production |
| `context-1m-2025-08-07` | 1M token context window | Production |
| `context-management-2025-06-27` | Context management features | Production |
| `structured-outputs-2025-12-15` | Structured output support | Production |
| `fast-mode-2026-02-01` | Fast mode API support | Production |
| `web-search-2025-03-05` | Web search capabilities | Production |
| `prompt-caching-2025-12-18` | Prompt caching optimization | Production |

### Experimental Beta Headers

| Beta Header | Purpose | Status |
|-------------|---------|--------|
| `afk-mode-2026-01-31` | AFK (Away From Keyboard) mode | Experimental |
| `redact-thinking-2026-02-12` | Redacted thinking blocks | Experimental |
| `agent-teams-2026-03-01` | Agent teams coordination | Experimental |
| `voice-interaction-2026-03-15` | Voice mode support | Experimental |

### Deprecated Beta Headers

| Beta Header | Purpose | Replacement |
|-------------|---------|-------------|
| `max-tokens-3-5-sonnet-2024-07-15` | Legacy max tokens | Superseded by newer versions |

### Usage Pattern

```typescript
import { getBetaHeaders } from '@/utils/betas';
import { BETAS } from '@/constants/betas';

// Get all applicable beta headers for API request
const headers = {
  ...getBetaHeaders(),
  'x-api-key': apiKey,
};

// Check if a specific beta is included
import { ENABLED_BETAS } from '@/constants/betas';

if (ENABLED_BETAS.includes(BETAS.FAST_MODE)) {
  // Fast mode beta is enabled
  enableFastMode();
}
```

### Implementation Location

- **Constants**: `src/constants/betas.ts` - Beta header definitions
- **Utility**: `src/utils/betas.ts` - Beta header selection logic
- **Integration**: Headers added to all API requests automatically

---

## Multi-Layer Flag Examples

Some features use **multiple flag layers** for defense-in-depth control. Here are real-world examples:

### Agent Teams (4-Layer Control)

```typescript
// Layer 1: Build-time flag (compile-time elimination)
import { feature } from '@/utils/config';
if (!feature('AGENT_SWARMS')) {
  return false; // Code eliminated from bundle
}

// Layer 2: GrowthBook killswitch (A/B testing)
import { getFeatureValue_CACHED_MAY_BE_STALE } from '@/services/analytics/growthbook';
const killswitchEnabled = getFeatureValue_CACHED_MAY_BE_STALE('tengu_amber_flint', true);
if (!killswitchEnabled) {
  return false; // Disabled via GrowthBook
}

// Layer 3: Environment variable override
import { isEnvTruthy } from '@/utils/env';
if (isEnvTruthy(process.env.CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS)) {
  return true; // Developer override
}

// Layer 4: Beta header (API feature negotiation)
import { ENABLED_BETAS, BETAS } from '@/constants/betas';
if (!ENABLED_BETAS.includes(BETAS.AGENT_TEAMS)) {
  return false; // API doesn't support it
}
```

**Location**: `src/utils/agentSwarmsEnabled.ts`

### Fast Mode (3-Layer Control)

```typescript
// Layer 1: Build-time flag
if (!feature('FAST_MODE')) {
  return false;
}

// Layer 2: Environment variable disable
if (isEnvTruthy(process.env.CLAUDE_CODE_DISABLE_FAST_MODE)) {
  return false;
}

// Layer 3: Beta header
if (!ENABLED_BETAS.includes(BETAS.FAST_MODE)) {
  return false;
}
```

**Location**: `src/utils/fastMode.ts`

### Connector Text Summarization (3-Layer Control)

```typescript
// Layer 1: Build-time flag
if (!feature('CONNECTOR_TEXT')) {
  return false;
}

// Layer 2: GrowthBook flag
const enabled = getFeatureValue_CACHED_MAY_BE_STALE('tengu_slate_prism', false);

// Layer 3: Environment variable override
if (isEnvTruthy(process.env.USE_CONNECTOR_TEXT_SUMMARIZATION)) {
  return true;
}
```

---

## Feature Flag Infrastructure

### Build-Time Flag System

**Technology**: `bun:bundle` compile-time feature detection

**How it works**:
1. `feature()` function checks if feature name is in enabled list
2. Bun's bundler detects constant conditionals at compile time
3. Dead code elimination removes disabled branches from bundle
4. Result: Zero runtime overhead for disabled features

**Configuration**: `src/utils/config.ts` (lines 600-700)

```typescript
// Simplified implementation
export function feature(name: string): boolean {
  if (import.meta.bundler === 'bun') {
    return ENABLED_FEATURES.includes(name);
  }
  return true; // Fallback for other bundlers
}
```

### GrowthBook Integration

**Technology**: GrowthBook SDK with custom caching layer

**How it works**:
1. GrowthBook client initialized with API credentials
2. Feature flags fetched from GrowthBook servers
3. Values cached to avoid excessive API calls
4. Ant users can override flags via internal tools
5. User-based targeting for gradual rollouts

**Configuration**: `src/services/analytics/growthbook.ts`

**Key functions**:
- `getFeatureValue_CACHED_MAY_BE_STALE(flagName, defaultValue)` - Get cached flag value
- GrowthBook SDK handles user targeting, A/B test assignment

### Environment Variable System

**Technology**: Standard Node.js `process.env` with helper utilities

**How it works**:
1. Environment variables read from shell environment
2. `isEnvTruthy()` helper converts string values to boolean
3. Variables can be set in shell config or per-session
4. Override precedence: env vars > GrowthBook > build-time

**Utilities**: `src/utils/env.ts`

```typescript
// Check if env var is truthy
export function isEnvTruthy(value: string | undefined): boolean {
  return value === 'true' || value === '1' || value === 'yes';
}
```

### Beta Header System

**Technology**: HTTP headers sent with API requests

**How it works**:
1. Beta constants defined in `src/constants/betas.ts`
2. `ENABLED_BETAS` array lists all active betas
3. `getBetaHeaders()` constructs header object
4. Headers automatically added to all API requests
5. API server enables features based on headers

**Implementation**:
```typescript
// src/constants/betas.ts
export const BETAS = {
  FAST_MODE: 'fast-mode-2026-02-01',
  CONTEXT_MANAGEMENT: 'context-management-2025-06-27',
  // ... more betas
} as const;

export const ENABLED_BETAS = [
  BETAS.FAST_MODE,
  BETAS.CONTEXT_MANAGEMENT,
  // ... enabled betas
];

// src/utils/betas.ts
export function getBetaHeaders() {
  return {
    'anthropic-beta': ENABLED_BETAS.join(','),
  };
}
```

---

## Migration & Deprecation

### Deprecated Build-Time Flags

The following build-time flags are marked for removal and should not be used in new code:

| Flag | Purpose | Migration Path | Status |
|------|---------|----------------|--------|
| `opusProMigrationComplete` | Opus Pro model migration | Remove after full rollout | Deprecated |
| `sonnet1m45MigrationComplete` | Sonnet 1M context migration | Remove after full rollout | Deprecated |

**Location**: `src/utils/config.ts` (lines 912-960)

### Deprecated Beta Headers

| Beta Header | Replacement | Removal Timeline |
|-------------|-------------|------------------|
| `max-tokens-3-5-sonnet-2024-07-15` | Use model-specific defaults | Q2 2026 |

### Flag Cleanup Process

When deprecating a feature flag:

1. **Identify unused flags**: Search codebase for flag references
2. **Mark as deprecated**: Add `@deprecated` JSDoc comment
3. **Set default to true/false**: Lock flag to final state
4. **Remove flag checks**: Replace conditional logic with final behavior
5. **Remove flag definition**: Delete from config/constants files

**Example migration**:
```typescript
// Before (flag-controlled)
if (feature('DEPRECATED_FLAG')) {
  newBehavior();
} else {
  oldBehavior();
}

// After (flag removed, feature fully rolled out)
newBehavior();
```

### Migration Tracking

Current active migrations:
- ✅ Opus Pro migration: Complete
- ✅ Sonnet 1M context migration: Complete
- 🔄 Agent teams rollout: In progress (controlled by `tengu_amber_flint`)
- 🔄 AFK mode: Experimental beta testing

---

## Adding New Feature Flags

### When to Use Each Flag Type

**Use build-time flags when**:
- Feature requires code that shouldn't ship to users yet
- Performance-sensitive code that should be eliminated when disabled
- Large features with significant bundle size impact

**Use GrowthBook flags when**:
- Gradual rollout needed (A/B testing)
- User-based targeting required
- Need killswitch for production features
- Want to enable features for specific user segments

**Use environment variables when**:
- Developer overrides needed
- Experimental opt-in features
- Configuration varies by deployment environment
- Debugging/testing features

**Use beta headers when**:
- Feature requires API server support
- API-level feature negotiation needed
- Version-specific API behavior

### Adding a New Build-Time Flag

1. **Add to `src/utils/config.ts`**:
```typescript
const ENABLED_FEATURES = [
  'EXISTING_FLAG',
  'NEW_FEATURE_FLAG', // Add new flag
] as const;
```

2. **Use in code**:
```typescript
import { feature } from '@/utils/config';

if (feature('NEW_FEATURE_FLAG')) {
  // New feature code
}
```

### Adding a New GrowthBook Flag

1. **Create flag in GrowthBook dashboard** (internal Anthropic process)
2. **Use in code**:
```typescript
import { getFeatureValue_CACHED_MAY_BE_STALE } from '@/services/analytics/growthbook';

const isEnabled = getFeatureValue_CACHED_MAY_BE_STALE('new_feature_flag', false);
```

### Adding a New Beta Header

1. **Add to `src/constants/betas.ts`**:
```typescript
export const BETAS = {
  // ... existing betas
  NEW_FEATURE: 'new-feature-2026-04-01',
} as const;

export const ENABLED_BETAS = [
  // ... existing betas
  BETAS.NEW_FEATURE,
];
```

2. **Coordinate with API team** to ensure server-side support

---

## Troubleshooting

### Common Issues

**Flag not working as expected**

1. Check all layers: build-time, GrowthBook, env vars, beta headers
2. Verify flag name spelling (case-sensitive)
3. Check GrowthBook cache staleness
4. Ensure beta header is in `ENABLED_BETAS` array

**Build-time flag changes not taking effect**

1. Rebuild the project: `bun run build`
2. Clear Bun's cache: `bun pm cache rm`
3. Verify flag is in `ENABLED_FEATURES` array

**GrowthBook flag returning stale values**

1. GrowthBook flags are cached - staleness is expected
2. Restart Claude Code to refresh cache
3. Check if Ant user override is active

**Environment variable not recognized**

1. Verify variable is exported: `echo $VARIABLE_NAME`
2. Restart Claude Code to pick up new env vars
3. Check spelling and prefix (`CLAUDE_CODE_` for most flags)

### Debug Mode

Enable debug logging to see flag evaluation:

```bash
export CLAUDE_CODE_DEBUG=true
export LOG_LEVEL=debug
claude-code
```

This will show:
- Which flags are enabled/disabled
- GrowthBook flag values
- Beta headers being sent
- Environment variables recognized

---

## References

### Primary Source Files

- **Build-time flags**: `src/utils/config.ts` (lines 600-700, 912-960)
- **GrowthBook integration**: `src/services/analytics/growthbook.ts`
- **Beta headers constants**: `src/constants/betas.ts`
- **Beta headers utility**: `src/utils/betas.ts`
- **Environment utilities**: `src/utils/env.ts`

### Multi-Layer Flag Examples

- **Agent teams**: `src/utils/agentSwarmsEnabled.ts`
- **Fast mode**: `src/utils/fastMode.ts`
- **Connector text**: `src/utils/connectorTextEnabled.ts`

### Related Documentation

- [Development Environment](./01-development-environment.md) - Environment setup
- [Build Process](./03-build-process.md) - Build-time flag compilation
- [API Integration](./05-api-configuration.md) - Beta headers and API features

---

## Summary

Claude Code's 4-layer feature flag system provides comprehensive control over feature rollouts:

1. **Build-time flags** (compile-time) - Zero overhead, bundle size optimization
2. **GrowthBook flags** (runtime) - A/B testing, user targeting, killswitches
3. **Environment variables** (runtime) - Developer overrides, experimental opt-ins
4. **Beta headers** (API) - Server-side feature negotiation

This multi-layered approach enables:
- Safe gradual rollouts
- Quick feature killswitches
- Developer experimentation
- Bundle size optimization
- User-based targeting

For questions or flag requests, consult the source files listed in the References section.
