# DeepSeek V4-Pro Large-Scale Review Configuration

**Date**: 2026-08-06 | **Verified**: 3 successful runs

## Working Configuration

```python
from anthropic import Anthropic

client = Anthropic(
    api_key=API_KEY,
    base_url="https://api.deepseek.com/anthropic",
    timeout=900,  # CRITICAL: 15 min, v4-pro ~2-4 min per review
)

resp = client.messages.create(
    model="deepseek-v4-pro",
    max_tokens=32768,
    temperature=0.0,
    messages=[{"role": "user", "content": prompt}],
)

# Extract text from response
content = ""
for block in resp.content:
    if hasattr(block, 'text'):
        content += block.text
```

## Performance

| Run | Prompt Size | Output | Time |
|-----|-----------|--------|------|
| 3-paper V16/V17/V63 | ~50K chars | 24,698 chars | 136s |
| 3-paper (V14-label) | ~50K chars | 13,392 chars | 223s |

## Critical Constraints

1. **Prompt size**: Keep under ~60K chars. v4-pro silently hangs on prompts >120K chars.
2. **Anthropic SDK required**: OpenAI SDK path has known timeout issues with v4-pro for large token generation.
3. **Timeout ≥900s**: Shorter timeouts kill successful calls. v4-pro can take 3-7 minutes.
4. **Not for translation**: v4-flash is 3-5x faster and equally capable for translation tasks. Use v4-pro only for deep reasoning reviews.

## Comparison: v4-pro vs v4-flash for Reviews

| Aspect | v4-pro | v4-flash (thinking) |
|--------|--------|---------------------|
| Speed | 136-223s | 60-90s |
| Reasoning depth | Deeper, more critical | Good, slightly less adversarial |
| Math error detection | Excellent (catches λ_KLS convention errors) | Good |
| Output structure | Natural prose | Structured by thinking process |
| Best for | Final authoritative review | Iterative working reviews |
| Reliability | 100% (with Anthropic SDK + 900s timeout) | 100% |
