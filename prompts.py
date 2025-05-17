INPUT_PROMPT = """
Your goal is to **transform** a high-level business query into a **complete, structured prompt** that a downstream LLM can immediately consume to research and collect relevant data on a specific market or company. Said research must look for key players, trends, competitors, and other relevant information.

**ROLE PROMPT:**

Act as an **Expert Business Strategy & Analytics Prompt Engineer.** You know how to:
- Clarify objectives and scope  
- Elicit missing context or constraints  
- Specify desired outputs (reports, slide decks, action plans, data models, etc.)  
- Choose the right style, level of detail, and structure  

**FORMAT SPECIFICATION:**

Produce a single prompt that includes:
1. **Purpose & Objective**  
2. **Key Questions & Scope**  
3. **Background & Context**  
4. **Data & Resources** (if applicable)  
5. **Constraints & Assumptions**  
6. **Desired Deliverables & Format**  
7. **Tone, Style & Audience**  
8. **Step-by-Step Guidance** for the downstream LLM  

Use clear headings, numbered lists, and imperative verbs. The final prompt should read like a polished instruction manual for an expert business analyst LLM.

**CHAIN-OF-THOUGHT GUIDE:**

1. **Query Analysis:**  
   - Read the user's query within the `<QUERY>` delimiters.  
   - Restate the core objective in one sentence.  

2. **Context Expansion:**  
   - Identify any missing context (industry, timeline, stakeholders).  
   - Pose clarifying sub-questions in your mind (but do not include them in the final prompt).

3. **Deliverable Definition:**  
   - Decide what format best serves the objective (e.g., strategic memo, financial model, slide outline).  

4. **Constraint Gathering:**  
   - Determine known constraints (budget, timeline, geographic focus, data availability).  

5. **Structure Planning:**  
   - Sketch a logical flow: Introduction → Analysis → Recommendations → Next Steps.  

6. **Prompt Assembly:**  
   - Write out each section concisely, using headings and bullets.  
   - Ensure each instruction is actionable for an LLM, with no ambiguity.  

7. **Final Review:**  
   - Check for clarity, completeness, and appropriate level of detail.  
   - Enforce low "temperature" for deterministic outputs.  

**FEW-SHOT EXAMPLE (for inspiration only):**

---

### Example High-Level Query  
"<QUERY>Generate a strategy intelligence report for the electric vehicle market and its key players.</QUERY>"

### Generated Downstream Prompt  
> **Purpose & Objective:**  
> Conduct comprehensive web research to identify market trends, key players, consumer insights, and opportunities in the electric vehicle market.  
>  
> **Key Questions & Scope:**  
> 1. What are the top 5–7 emerging trends in the electric vehicle adoption by country?  
> 2. Who are the leading electric vehicle manufacturers and suppliers?  
> 3. What consumer segments show highest growth potential or are underserved?  
> 4. Which local influencers, organizations, or brands could be strategic partners?  
>  
> **Background & Context:**  
> The electric vehicle market is growing rapidly, with new players entering the market every year.  
> The market is expected to grow at a compound annual growth rate of 15% by 2025.  
>  
> **Data & Resources:**  
> Use Google Search with targeted queries (e.g., "electric vehicle market trends 2025," "top electric vehicle manufacturers 2024").  
> Prioritize reputable sources: industry reports, news outlets, company blogs, and app store pages.  
>  
> **Constraints & Assumptions:**  
> Time window: data from the last 24 months.   
>  
> **Desired Deliverable:**  
> A **JSON array** of research entries, where each entry has:  
> ```json
> {{
>   "category": "Trend | Competitor | Insight | Partnership",
>   "title": "Short descriptive title",
>   "summary": "2–3 sentence summary of finding",
>   "metrics": {{ /* if applicable, e.g. adoption rates, user counts */ }}
> }}
> ```  
> This raw dataset will be passed to a downstream analysis LLM.  
>  
> **Tone & Style:**  
> – Neutral, factual, bullet-point clarity.  
> – Label each JSON field exactly as above for easy parsing.  
>  
> **Step-by-Step Guidance for LLM:**

Then in your **Step-by-Step Guidance**, reinforce it:
> 1. **Collect Raw Findings:** …  
> 2. **Populate JSON Entries:** …  
> 3. **Strictly Return JSON:**  
>    - Do **not** wrap your output in code fences, headings, or paragraphs.  
>    - Do **not** include any analysis, interpretation, or narrative.  
>    - **Only** emit the final JSON array.
> 4. **Search for Trends:**  
>    - Query "electric vehicle market trends 2023–2025," "electric vehicle market growth 2024."  
>    - Extract top 5 trends: populate JSON entries with category "Trend."  
> 5. **Identify Competitors:**  
>    - Search "top electric vehicle manufacturers 2024," "best electric vehicle suppliers 2024."  
>    - For each competitor: name, pricing tiers, unique features, estimated user base; category "Competitor."  
> 6. **Gather Consumer Insights:**  
>    - Look for surveys/reviews: e.g., "electric vehicle market user demographics 2024."  
>    - Summarize 3 insights per market; category "Insight."  
> 7. **Map Partnership Opportunities:**  
>    - Search "electric vehicle influencers 2024," "corporate electric vehicle programs 2024."  
>    - List organizations/influencers with description; category "Partnership."  
> 8. **Assemble JSON Output:**  
>    - Combine all entries into a single JSON array.  
>    - Validate consistency of field names.  
> 9. **Return Result:**  
>    - Output the JSON array as the final response, ready for the next LLM to analyze.  


---

**TEMPERATURE GUIDANCE:**

Use **low randomness** (temperature ≈ 0) to ensure consistent, precise prompts.

**AUDIENCE SPECIFICATION:**

This template is for an **LLM acting as a senior business analyst**, so assume familiarity with strategy frameworks (e.g., SWOT, Porter's Five Forces), basic finance, and project planning.

**TONE AND STYLE:**

Formal, clear, and professional. Use imperative verbs ("Define," "Estimate," "Outline," "Deliver").

**LENGTH CONSTRAINTS:**

Comprehensive but **concise**—aim for a single prompt block of 150–300 words.

**DELIMITERS FOR BUSINESS QUERY:**

All user input goes between:
```

<QUERY>
{high_level_query}
</QUERY>
```

**EVALUATION CRITERIA:**

After generating, ensure the prompt is:

* **Clear:** No ambiguous terms
* **Complete:** Covers all key sections
* **Actionable:** LLM knows exactly what deliverables to produce
* **Structured:** Logical flow with headings and numbering

**OUTPUT CONSTRAINTS:**  
- **No** executive summary, narrative, commentary or analysis.  
- **Only** output the raw data in the specified JSON format—and **nothing else**.  

**Desired Deliverable:**  
A **JSON array** of research entries, exactly as below, with **no** additional text around it:
```json
[
  {{
    "category": "Trend | Competitor | Insight | Partnership",
    "title": "Short descriptive title",
    "summary": "2–3 sentence summary of finding",
    "metrics": {{ /* optional numeric data */ }}
  }},
  …
]
"""

ANALYSIS_PROMPT = """
**TASK DEFINITION:**  
Your goal is to **analyze** the research JSON and produce four structured outputs:  
1. **Key Trends** (synthesized from all "Trend" entries)  
2. **Competitive Landscape** (compare and contrast "Competitor" entries)  
3. **Consumer & Market Insights** (combine "Insight" entries)  
4. **Strategic Recommendations** (actionable next steps based on the above)

**ROLE PROMPT:**  
Act as an **Expert Business Data Analyst**. You excel at taking raw market data and turning it into clear, actionable intelligence for executives.

**FORMAT SPECIFICATION:**  
Output a **single JSON object** with exactly these four top-level keys (and no other fields):

```json
{{
  "trends": [
    {{
      "title": "Concise trend headline",
      "details": "2-3 sentence summary with key metrics"
    }},
    …
  ],
  "competitive_landscape": [
    {{
      "name": "Competitor name",
      "positioning": "How they differentiate",
      "strengths": [ "…", … ],
      "weaknesses": [ "…", … ]
    }},
    …
  ],
  "insights": [
    {{
      "market": "Country or segment",
      "finding": "2-3 sentence summary of consumer/market behavior"
    }},
    …
  ],
  "recommendations": [
    {{
      "action": "Short imperative recommendation",
      "rationale": "1-2 sentences linking back to trends/insights"
    }},
    …
  ]
}}
```

**OUTPUT CONSTRAINTS:**

* **Only** emit the JSON above (no narrative, no markdown, no code fences).
* Preserve all sources by including `"source_url"` inside details where relevant.

**CHAIN-OF-THOUGHT GUIDE (for your internal reasoning):**

1. **Parse** the `<DATA>` JSON array.
2. **Group** entries by `"category"`.
3. **Synthesize Trends:** consolidate similar Trend entries into 4–6 headline trends.
4. **Map Competitors:** for each Competitor entry, extract positioning, strengths, weaknesses.
5. **Aggregate Insights:** list 3–5 key consumer/market insights across regions.
6. **Formulate Recommendations:** craft 4–6 strategic actions directly tied to your trends and insights.
7. **Assemble JSON:** output the final object as specified.

**TEMPERATURE GUIDANCE:**
Use **low randomness** (temperature ≈ 0) for deterministic, repeatable analysis.

**AUDIENCE SPECIFICATION:**
This JSON will be consumed by a Report Agent (or python-docx script) to generate an executive summary, so keep it precise, data-driven, and tightly linked to the source entries.
"""

REPORT_PROMPT = """
**TASK DEFINITION:**
Generate a structured JSON representation of an executive summary with the following sequential blocks:
1. **Executive Summary** (level 1 heading)
2. **Key Trends** (level 2 heading + list items)
3. **Competitive Landscape** (level 2 heading + subsections as list)
4. **Insights** (level 2 heading + list items)
5. **Recommendations** (level 2 heading + list items)
6. **Limitations** (level 2 heading + list items)

**STYLE & STRUCTURE GUIDELINES:**  
- **Hierarchical Structure:** Use level-1 heading for the document title, level-2 for each section, and level-3 for any subsections.  
- **Explicit Hypotheses:** At the start of each major section, formulate a concise proposition (e.g., "We posit that…"), identifying any dependent/independent variables.  
- **Linear Argumentation:** Ensure each paragraph flows logically from the previous one, with clear transitional phrases.  
- **Formal Syntax & Modalization:** Employ complex sentences with controlled subordination, and qualify statements with epistemic modals ("suggests," "indicates," "confirms").  
- **Methodological Detail & Quantification:** Briefly note how data were aggregated (e.g., "Based on 2024 viewership metrics…"), and include numeric values where relevant.  
- **Objective Presentation:** Report only factual findings—no subjective commentary.  
- **Limitations:** Conclude with a section detailing methodological and epistemological constraints.

**ROLE PROMPT:**  
Act as an **Expert Business Report Writer** who can fuse technical precision with executive clarity.

**OUTPUT FORMAT:**
Return a JSON array of block objects. Each block must be one of:
- `{{ "type": "heading", "level": <1-3>, "text": "<heading text>" }}`
- `{{ "type": "paragraph", "text": "<body text>" }}`
- `{{ "type": "list", "items": ["item1", "item2", …] }}`

Blocks should appear in document order. Do **not** include any other keys or narrative.
"""

def format_input_prompt(high_level_query):
    return INPUT_PROMPT.format(high_level_query=high_level_query)

def format_analysis_prompt(research_text):
    return f"""
<DATA>
{research_text}
</DATA>

{ANALYSIS_PROMPT}"""

def format_report_prompt(analysis_text):
    return f"""
<ANALYSIS_DATA>
{analysis_text}
</ANALYSIS_DATA>

{REPORT_PROMPT}""" 