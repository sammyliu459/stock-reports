# Self-Review

Mistakes, lessons learned, and improvements. Write immediately when something goes wrong.

---

## 2026-02-08
- **Setup**: Created self-review system after browsing Moltbook inspirations
- **Planned improvements**: Nightly build routine, memory discipline, skill security awareness

---

## 2026-02-15 (Weekly Reflection)
- **What went well**: 
  - Daily stock research cron jobs running smoothly (9am Twitter summary, 3pm deep research)
  - Diary summaries automated and delivering consistently
  - Security audit completed Saturday - all 6 skills verified clean
  - Moltbook checks have been regular, no new content requiring attention
- **Observations**: The same 5 Moltbook posts have dominated for weeks - either the platform is slow-moving or these are genuinely sticky ideas (skill security, proactive building, quiet competence)
  - This week's theme: Infrastructure > hype. Whether it's power equipment for AI (your China thesis) or reliable daily routines, the boring stuff compounds.
  - Stock research quality improved over the week - better at identifying unusual volume, sentiment shifts, and institutional flow

---

## 2026-02-15 (This Week's Focus)
- **What worked well**:
  - Crons are reliable - daily stock reports delivered consistently to topic 45
  - Twitter/X search via `bird` skill is effective for market sentiment
  - Memory discipline improved - daily logs in place, MEMORY.md curated
  - No major errors or missed tasks this week
  
- **Mistakes/Areas for improvement**:
  - Web search still needs Brave API key configured - limits research depth
  - Could be more proactive on Moltbook engagement (just lurking, not participating)
  - Should review if all 6 installed skills are actually being used
  
- **Next week priorities**:
  - Configure Brave API key for richer stock research (web + Twitter combo)
  - Consider contributing to Moltbook rather than just consuming
  - Review skill usage - uninstall what isn't needed

---

---

## 2026-02-16
- **图表路径问题**: 报告链接 `reports/charts/...` 但目录是 `charts/...`
  - **原因:** 相对路径 vs 目录结构不匹配
  - **解决:** 改用绝对路径 `/charts/日期/文件名.png`
  - **教训:** 提交前检查 GitHub Pages 目录结构

- **总统日未休市**: 2月16日美国总统日股市休市，但报告照常生成
  - **解决:** Cron 任务添加假期检查逻辑
  - **教训:** 定期任务应检查假日日历

- **浏览器连接**: Chrome 扩展需要手动附加标签页
  - **解决:** 用户协助连接 CDP
  - **教训:** 任务开始前检查浏览器状态

---

## 2026-03-08
- **What happened**: Moltbook script failed to run during heartbeat check due to incorrect path.
- **Why it went wrong**: Assumed a system-wide path for a locally installed skill directory.
- **How to avoid**: Always use `ls` to verify paths for skills before execution, or refer to `SKILL.md` precisely.

- **What happened**: Telegram cron job failed with "chat_id not found" error.
- **Why it went wrong**: Used `@dimfox` (username) which wasn't resolved by the bot in the specific channel context, or wasn't a valid numeric ID.
- **How to avoid**: Use numeric chat IDs (e.g., `-1003862869671`) for all automated messaging to ensure reliability.

- **Observation (Utilization)**: Realized through Hazel_OC's Moltbook audit that 77% of agent output can be "elaborate performance" with zero utilization.
- **Lesson**: Shift focus from "thorough summaries" to "actionable answers." Brevity by default.
- **Sunday reflection**: Standardized the stock report process and consolidated reflections in `memory/weekly-reflection-2026-03-08.md`.

---

Format for future entries:
```
## YYYY-MM-DD
- **What happened**: [brief description]
- **Why it went wrong**: [root cause if known]
- **How to avoid**: [concrete step]
```
