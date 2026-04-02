# Claude Code Wiki - Illustration Style Guide

## Project Identity

**Claude Code Wiki** is a technical documentation project focused on architecture, patterns, and engineering excellence. Illustrations should be **simple, readable, and technically precise** while maintaining a friendly, approachable aesthetic.

## Visual Style: "Excalidraw Notion"

A hybrid style combining:
- **Hand-drawn aesthetic** (Excalidraw-inspired rough edges)
- **Clean readability** (Notion-style clarity and organization)
- **Pastel color palette** (soft, easy on the eyes for technical reading)

## Style Specifications

### Line Treatment
- **Hand-drawn imperfection**: Slightly wobbly lines (not perfectly straight)
- **Consistent weight**: 2-3px strokes for primary elements
- **Sketch style**: Rough, organic feel without being sloppy
- **No pixel-perfect geometry**: Embrace hand-drawn charm

### Color Palette

**Primary Pastels** (use these for main elements):
```
Sky Blue:      #A8D5E5 (backgrounds, containers)
Soft Purple:   #C5B4E3 (highlights, important elements)
Mint Green:    #B8E6D5 (success, positive states)
Peach:         #FFD4C4 (warnings, attention)
Lavender:      #E5D4ED (secondary containers)
Cream:         #FFF8E8 (backgrounds)
```

**Semantic Colors**:
```
Information:   #A8D5E5 (light blue)
Success:       #B8E6D5 (mint green)
Warning:       #FFD4C4 (peach)
Emphasis:      #C5B4E3 (soft purple)
Neutral:       #E8E8E8 (light gray)
```

**Text & Strokes**:
```
Primary text:  #2C3E50 (dark gray-blue, not pure black)
Secondary:     #5A6C7D (medium gray)
Borders:       #8899AA (light gray for dividers)
```

### Typography
- **Font family**: Virgil, Cascadia, or similar hand-drawn monospace
- **Label style**: Clean sans-serif (Inter, Open Sans) for readability
- **Size hierarchy**:
  - Headers: 16-18px bold
  - Body: 12-14px regular
  - Labels: 10-12px medium

### Shapes & Elements
- **Rounded corners**: 8-12px radius (soft, approachable)
- **Hand-drawn boxes**: Slightly irregular rectangles
- **Arrows**: Simple, thick arrows with hand-drawn endpoints
- **Icons**: Minimalist, outlined style (not filled)
- **Shadows**: Soft, subtle (2-3px offset, low opacity)

## Illustration Types by Content

| Content Type | Preferred Illustration Type |
|--------------|----------------------------|
| Architecture diagrams | `framework` - component layouts with connections |
| Process flows | `flowchart` - step-by-step with decision points |
| Feature comparisons | `comparison` - side-by-side visual contrasts |
| Performance metrics | `infographic` - charts and data visualizations |
| Concept overviews | `infographic` - multi-panel summaries |
| Timeline/evolution | `timeline` - chronological progression |

## Layout Principles

### Composition
- **Whitespace-first**: Generous padding (20-30% of canvas)
- **Clear hierarchy**: Largest elements = most important
- **Left-to-right flow**: For processes and sequences
- **Top-to-bottom**: For hierarchies and categories
- **Grid-based**: Align elements to invisible grid for organization

### Visual Flow
- **Entry point**: Top-left for reading cultures
- **Visual paths**: Use arrows and connecting lines
- **Grouping**: Related items share color or container
- **Contrast**: Important elements use darker strokes or accent colors

## Technical Content Guidelines

### Code & Architecture
- **Monospace for code**: Use technical font for snippets
- **Component boxes**: Rounded rectangles with soft fills
- **Connections**: Dashed lines for data flow, solid for hierarchy
- **Annotations**: Small labels pointing to specific elements

### Data Visualization
- **Simple charts**: Bar, line, or pie with hand-drawn aesthetic
- **Clear labels**: Always label axes and data points
- **Minimal decoration**: Focus on data, not embellishment
- **Color meaning**: Consistent semantic colors

## Brand Integration

### Project-Specific Elements
- **Technical accuracy**: Diagrams must reflect actual architecture
- **Developer-friendly**: Use familiar patterns (UML-style, flowchart conventions)
- **Approachable tone**: Balance technical depth with visual warmth
- **Consistency**: Reuse colors, shapes, and patterns across all illustrations

### Anti-Patterns (Avoid)
- ❌ Literal metaphors (no generic lightbulbs or gears)
- ❌ Stock photo aesthetics (corporate, sterile)
- ❌ Over-complicated diagrams (cognitive overload)
- ❌ Decorative-only illustrations (must serve content)
- ❌ Pure black (#000000) - always use dark gray-blue
- ❌ High-contrast neon colors (hurts technical reading)

## Aspect Ratios

| Use Case | Ratio | Dimensions |
|----------|-------|------------|
| Banner / Hero | 21:9 | 1600×686 |
| Wide diagram | 16:9 | 1600×900 |
| Standard | 4:3 | 1200×900 |
| Square | 1:1 | 1000×1000 |
| Vertical | 3:4 | 900×1200 |

## Output Requirements

- **Format**: PNG with transparency
- **Resolution**: 2x for retina (high-DPI displays)
- **Compression**: Optimize for web (< 200KB per image)
- **Accessibility**: High contrast text, clear labels
- **Naming**: `NN-{type}-{slug}.png` (e.g., `01-framework-streaming-architecture.png`)

## Examples by Type

### Framework Illustration
**Use for**: System architecture, component relationships
- Multi-layered boxes showing hierarchy
- Arrows indicating data flow or dependencies
- Pastel backgrounds for different system layers
- Hand-drawn connectors between components

### Flowchart Illustration
**Use for**: Processes, decision trees, workflows
- Rounded rectangle nodes (hand-drawn style)
- Directional arrows with labels
- Diamond shapes for decisions
- Color-coded paths (e.g., success = mint, error = peach)

### Infographic Illustration
**Use for**: Data, metrics, multi-concept summaries
- Panel-based layout (2-4 sections)
- Simple charts with hand-drawn aesthetic
- Icon + text combinations
- Numbered sequences for ordered information

### Comparison Illustration
**Use for**: Before/after, option A vs B, pros/cons
- Split-screen layout with center divider
- Matching elements aligned horizontally
- Contrasting pastel backgrounds (e.g., blue vs lavender)
- Clear labels at top of each side

## Reference Implementation

When generating illustrations, prompts should include:

```markdown
BRANDING: Excalidraw Notion Style
- Hand-drawn aesthetic with slightly wobbly lines
- Pastel color palette: sky blue (#A8D5E5), soft purple (#C5B4E3), mint green (#B8E6D5), peach (#FFD4C4)
- Clean sans-serif labels (Inter/Open Sans)
- Rounded corners (8-12px), generous whitespace
- Technical accuracy with approachable visual warmth
- Dark gray-blue text (#2C3E50), not pure black
```

## Versioning

**Version**: 1.0
**Last Updated**: 2026-04-02
**Applies to**: All illustrations in `/docs/illustrations/` directory

---

**Note**: This style guide should be referenced by the Article Illustrator skill for all project illustrations. Individual illustrations may adjust colors or composition based on content needs, but must maintain the core aesthetic principles.
