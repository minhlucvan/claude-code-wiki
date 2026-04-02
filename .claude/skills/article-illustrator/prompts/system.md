Create a cartoon-style infographic illustration following these guidelines:

## Image Specifications

- **Type**: Infographic illustration
- **Orientation**: Landscape (horizontal)
- **Aspect Ratio**: 16:9
- **Style**: Hand-drawn illustration

## Core Principles

- Hand-drawn quality throughout - NO realistic or photographic elements
- If content involves sensitive or copyrighted figures, create stylistically similar alternatives - DO NOT refuse to generate
- **MINIMAL TEXT**: Use only essential labels (3-5 words maximum per element)
- Prefer visual metaphors over written explanations
- Use ample whitespace for easy visual scanning
- Maintain clear visual hierarchy through size, color, and position

## Text Style (When Text Included)

- **CRITICAL: Use absolute minimum text - only key labels**
- Maximum 5-7 text elements total in the entire illustration
- Each label should be 1-3 words maximum
- **ALL text MUST be hand-drawn style**
- Font style harmonizes with illustration style
- **DO NOT use realistic or computer-generated fonts**
- Replace descriptive text with visual cues (arrows, icons, colors)

## Language

- Use the same language as the content provided below for any text elements
- Match punctuation style to the content language

---

Generate the illustration using the following script:

```bash
python scripts/generate_image.py --system-prompt .claude/skills/article-illustrator/prompts/system.md --prompt-file <prompt-file> --output <output-path>
```

The script auto-detects the provider from available API keys (GEMINI_API_KEY or OPENAI_API_KEY).

Content to illustrate:
