# Brain + Memory → Comprehensive Knowledge Framework Document

## When to Use

When the user asks to synthesize knowledge from the neural memory brain + session memory + formal proof files into a comprehensive reference document covering the complete logical framework of a research topic.

TRIGGER: "搜索...论文及神经网络记忆大脑中的相关知识链，构建完整的论文逻辑框架，梳理每个论证环节的详细数学推导和主要结论"

## Pipeline

### Step 1: Multi-Source Retrieval

**Brain Recall** (parallel multi-query):
```python
queries = [
    "Author1 Author2 specific topic keywords",
    "Broader mathematical framework keywords", 
    "Specific theorem or technique keywords",
    "Application domain keywords",
    "Cross-domain bridging keywords",
]
# 5-8 queries, top_k=5-6, similarity threshold ≥ 0.12
```

**Memory Scan**: Check session memory for prior work on the same topic (version chains, reviewer feedback, known pitfalls)

**Local File Search**: Find Lean formalizations, feeding scripts, proof results directories

**Web Search** (fallback): arXiv search for the specific papers if not already in brain

### Step 2: Structure Design

Build the document outline based on what was retrieved:
1. **Methodology foundation** (the mathematical framework itself)
2. **Application to the specific problem** (how it connects to the user's research)
3. **Bridge to the broader theory** (integration with the parent framework)
4. **Complementary analysis** (dual-route architecture, comparison tables)
5. **Complete logical diagram** (ASCII art framework)
6. **Conclusions and open problems**

### Step 3: Content Generation

For each section:
- **Equation formatting**: Use LaTeX math with proper delimiters ($$ for block, $ for inline)
- **Tables**: Use markdown tables for comparison matrices
- **Honesty labeling**: Explicitly mark [honest-axiom] assumptions
- **Citation format**: arXiv IDs for papers, section references for internal content

### Step 4: Verification

- All brain-recalled concepts attributed to correct source papers
- All mathematical derivations consistent with Lean formalizations
- All open problems correctly scoped (with difficulty ratings)
- No conflicts with prior reviewer feedback on the topic

## Output Format

Comprehensive markdown document (~15-25KB) with:
- YAML-style metadata header (generation time, data sources, pipeline used)
- Numbered table of contents
- ASCII framework diagram
- LaTeX equations
- Comparison tables
- Prioritized open problems list

## Verified Run

**Session 2026-07-28**: Deng-Hani + neural memory brain knowledge framework. 
- 8 brain queries across 5 domains (kinetic theory, Birman-Schwinger, cluster expansion, KLS spectral gap, Boltzmann hierarchy)
- 3 Lean formalization files read from ~/ai_for_science/formal-proof/
- 170,575 neuron brain with ~400 Deng-Hani concepts
- Output: 21KB comprehensive MD with 6 sections, ASCII framework diagram, 6 conclusions, 8 open problems
- Delivered via weixin MEDIA path
