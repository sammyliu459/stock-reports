# Stock Theme & Narrative Research Skill

## Description
Research the core fundamental themes, social narratives, and market sentiment driving a specific stock. This helps uncover non-traditional classifications (like "Drone stock" or "Political stock") alongside standard sector analysis.

## Trigger
Use this skill when the user asks to "research the theme of", "check the narrative for", or "what kind of stock is" a specific ticker.

## Instructions

Whenever you are tasked with researching a stock's theme, follow these specific steps:

### 1. Fundamental & Core Business Search
Determine what the company *actually* does versus what it is trading on.
- Use `web_search` to find the core business focus. 
- **CRITICAL:** Do NOT use `country`, `language`, or `freshness` filters in the `web_search` tool (unsupported by the current Gemini provider constraint).
- Example Query: `[TICKER] stock core business what do they make`

### 2. Social Narrative & "Fringe" Theme Search
Many stocks trade on themes untethered to their direct fundamentals (e.g., political ties, retail short squeezes, sympathy plays). Twitter/X is a primary source for this.
- If the `bird` CLI is available in the workspace, use it: `exec` -> `bird search "$[TICKER]" --limit 10` (or `bird search "$[TICKER] narrative"`).
- Fallback to `web_search`: `[TICKER] stock narrative twitter discussion` or `[TICKER] stock why is it moving retail sentiment`.

### 3. Identify Specific Associations
Actively parse the search results for:
- **Sympathy Alignments:** Is it trading in sympathy with AI, Crypto, Defense/Drones, or Energy?
- **Political/Social Ties:** Are famous investors, political figures, or influencers involved? (e.g., the "Trump stock" phenomenon).
- **Retail Mechanics:** Is it a meme stock, a high short-interest play, or a low-float pump?

### 4. Synthesis & Output Format
Present the findings clearly to the user using the following structure:

**📊 Thematic Profile for $[TICKER]**

- **Primary Fundamental Theme:** (What the business actually does, e.g., "Small-cap materials processor")
- **Social / Narrative Theme:** (What the market is trading it as, e.g., "Sympathy Drone Play" or "Political affiliation stock")
- **The "Why":** (Briefly explain *how* it got this narrative—e.g., "Trump's sons reportedly invested in it" or "Pivoted to drone parts in recent PR")
- **Catalysts to Watch:** (Events that could validate or destroy the narrative)
- **Narrative Risks:** (e.g., "Highly susceptible to news-cycle fade rather than earnings")