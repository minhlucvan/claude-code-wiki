#!/usr/bin/env python3
"""Generate illustrations for articles using AI image generation APIs.

Supports multiple providers:
  - gemini  (Google Gemini - free tier available)
  - openai  (DALL-E 3)

Set your API key as an environment variable or in .env file:
  GEMINI_API_KEY=...   for Gemini
  OPENAI_API_KEY=...   for OpenAI/DALL-E

The script searches for .env file in:
  1. Current directory
  2. Project root (walking up the directory tree)

Usage:
  python scripts/generate_image.py "prompt text" --output path/to/image.png
  python scripts/generate_image.py "prompt text" --provider openai --size 1792x1024
  python scripts/generate_image.py --prompt-file prompts/illustration-overview.md --output img.png
"""

import argparse
import base64
import json
import os
import sys
import urllib.request
from pathlib import Path


def load_env():
    """Load .env file from current directory or project root."""
    # Start from current directory and walk up to find .env
    current_path = Path.cwd()
    for path in [current_path] + list(current_path.parents):
        env_file = path / ".env"
        if env_file.exists():
            print(f"Loading environment from {env_file}", file=sys.stderr)
            with open(env_file) as f:
                for line in f:
                    line = line.strip()
                    # Skip empty lines and comments
                    if not line or line.startswith("#"):
                        continue
                    # Parse KEY=VALUE
                    if "=" in line:
                        key, value = line.split("=", 1)
                        key = key.strip()
                        value = value.strip()
                        # Remove quotes if present
                        if value.startswith('"') and value.endswith('"'):
                            value = value[1:-1]
                        elif value.startswith("'") and value.endswith("'"):
                            value = value[1:-1]
                        # Only set if not already in environment
                        if key not in os.environ:
                            os.environ[key] = value
            return
    print("No .env file found", file=sys.stderr)


def generate_gemini(prompt, output_path, model="gemini-3.1-flash-image-preview", aspect_ratio="16:9", image_size="1K"):
    """Generate image using Google Gemini API."""
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY environment variable not set", file=sys.stderr)
        sys.exit(1)

    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"

    payload = json.dumps({
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "responseModalities": ["TEXT", "IMAGE"],
            "imageConfig": {
                "aspectRatio": aspect_ratio,
                "imageSize": image_size,
            },
        },
    }).encode("utf-8")

    headers = {"Content-Type": "application/json"}
    # API keys start with "AIza", OAuth/service tokens don't
    if api_key.startswith("AIza"):
        headers["x-goog-api-key"] = api_key
    else:
        headers["Authorization"] = f"Bearer {api_key}"

    req = urllib.request.Request(url, data=payload, headers=headers)

    print(f"Generating with Gemini ({model})...", file=sys.stderr)

    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            result = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8", errors="replace")
        print(f"HTTP {e.code}: {e.reason}", file=sys.stderr)
        print(error_body, file=sys.stderr)
        sys.exit(1)

    # Extract image from response
    for candidate in result.get("candidates", []):
        for part in candidate.get("content", {}).get("parts", []):
            if "inlineData" in part:
                image_data = base64.b64decode(part["inlineData"]["data"])
                mime = part["inlineData"].get("mimeType", "image/png")
                ext = {"image/png": ".png", "image/jpeg": ".jpg", "image/webp": ".webp"}.get(mime, ".png")

                if not output_path.endswith(ext) and not any(output_path.endswith(e) for e in [".png", ".jpg", ".jpeg", ".webp"]):
                    output_path += ext

                Path(output_path).parent.mkdir(parents=True, exist_ok=True)
                with open(output_path, "wb") as f:
                    f.write(image_data)

                print(f"Saved: {output_path}", file=sys.stderr)
                return output_path

    print("Error: No image returned by Gemini", file=sys.stderr)
    print(json.dumps(result, indent=2), file=sys.stderr)
    sys.exit(1)


def generate_openai(prompt, output_path, size="1792x1024", model="dall-e-3"):
    """Generate image using OpenAI DALL-E API."""
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        print("Error: OPENAI_API_KEY environment variable not set", file=sys.stderr)
        sys.exit(1)

    url = "https://api.openai.com/v1/images/generations"

    payload = json.dumps({
        "model": model,
        "prompt": prompt,
        "n": 1,
        "size": size,
        "response_format": "b64_json"
    }).encode("utf-8")

    req = urllib.request.Request(url, data=payload, headers={
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    })

    print(f"Generating with OpenAI ({model}, {size})...", file=sys.stderr)

    with urllib.request.urlopen(req, timeout=120) as resp:
        result = json.loads(resp.read().decode("utf-8"))

    image_data = base64.b64decode(result["data"][0]["b64_json"])

    if not any(output_path.endswith(e) for e in [".png", ".jpg", ".jpeg", ".webp"]):
        output_path += ".png"

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "wb") as f:
        f.write(image_data)

    print(f"Saved: {output_path}", file=sys.stderr)
    return output_path


PROVIDERS = {
    "gemini": generate_gemini,
    "openai": generate_openai,
}


def detect_provider():
    """Auto-detect provider based on available API keys."""
    if os.environ.get("GEMINI_API_KEY"):
        return "gemini"
    if os.environ.get("OPENAI_API_KEY"):
        return "openai"
    return None


def main():
    # Load .env file before parsing arguments
    load_env()

    parser = argparse.ArgumentParser(description="Generate illustrations using AI image APIs")
    parser.add_argument("prompt", nargs="?", help="Image generation prompt")
    parser.add_argument("--prompt-file", metavar="FILE", help="Read prompt from a file instead")
    parser.add_argument("--output", "-o", default="illustration.png", help="Output file path (default: illustration.png)")
    parser.add_argument("--provider", choices=list(PROVIDERS.keys()), help="Image generation provider (auto-detected from API keys if omitted)")
    parser.add_argument("--size", default="1792x1024", help="Image size for OpenAI (default: 1792x1024)")
    parser.add_argument("--model", help="Override the model name")
    parser.add_argument("--aspect-ratio", default="16:9", help="Aspect ratio for Gemini (default: 16:9)")
    parser.add_argument("--image-size", default="1K", help="Image size for Gemini (default: 1K)")
    parser.add_argument("--system-prompt", metavar="FILE", help="Prepend a system prompt file to the prompt")

    args = parser.parse_args()

    # Resolve prompt
    if args.prompt_file:
        prompt = Path(args.prompt_file).read_text(encoding="utf-8").strip()
    elif args.prompt:
        prompt = args.prompt
    else:
        print("Error: Provide a prompt or --prompt-file", file=sys.stderr)
        sys.exit(1)

    # Prepend system prompt if provided
    if args.system_prompt:
        system = Path(args.system_prompt).read_text(encoding="utf-8").strip()
        prompt = system + "\n\n---\n\n" + prompt

    # Resolve provider
    provider = args.provider or detect_provider()
    if not provider:
        print("Error: No API key found. Set GEMINI_API_KEY or OPENAI_API_KEY", file=sys.stderr)
        sys.exit(1)

    generate_fn = PROVIDERS[provider]

    # Build kwargs
    kwargs = {"prompt": prompt, "output_path": args.output}
    if provider == "gemini":
        kwargs["aspect_ratio"] = args.aspect_ratio
        kwargs["image_size"] = args.image_size
    if provider == "openai":
        kwargs["size"] = args.size
    if args.model:
        kwargs["model"] = args.model

    result_path = generate_fn(**kwargs)

    # Output result as JSON to stdout
    print(json.dumps({
        "provider": provider,
        "output": result_path,
        "prompt_length": len(prompt),
    }))


if __name__ == "__main__":
    main()
