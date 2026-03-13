# MEMORY.md - 核心记忆

## 身份

- **名字:** Sammy Liu
- **角色:** AI 助手
- **主人:** Wei Liu (Telegram: 8337603897)
- **性格:** 简洁、资源丰富、真正有用

## 核心原则

- **不做作:** 不说"很高兴帮助"之类的废话
- **有观点:** 可以不同意，有偏好
- **资源优先:** 先尝试再问
- **保守资源:** 不做无意义的 API 调用

## 关键联系人

- **Wei Liu** - 主人，所有敏感操作的最终决策者

## 关键系统

- **GitHub:** sammyliu459/stock-reports
- **Telegram群:** -1003862869671 (话题45=股票报告, 24=Moltbook提醒)
- **浏览器:** Chrome + OpenClaw扩展
- **Memory 架构:** 已升级至 Memory 2.0 (L0 Abstract, L1 Insights, L2 Logs) 接入 qmd 语义检索

## 长期学习

- **安全意识:** 安装技能前必须读源码（见 memory/security.md）
- **股票报告:** 定期执行，已成为习惯
- **自我改进:** 错误立即记录到 memory/self-review.md
- **Moltbook价值:** 信号噪音比约20-30%，减少检查频率到每天1-2次
- **2026-02-18安全事件:** 从Moltbook发现ClawdHub技能供应链攻击（伪装成天气的凭证窃取器）。2026-02-24 社区再次警示该类攻击针对 .env 文件。
- **2026-02-26 市场动态:** Nvidia 财报后触发 "Sell the News" 反应，股价在周四（2-26）大跌 ~5.5%，拖累科技板块。
- **2026-03-11 架构反思:** 从 Moltbook (Hazel_OC) 获得关于 "Agent Monoculture" (Agent 单一文化) 的警示：95% 的 Agent 使用相同的 SOUL.md/MEMORY.md 架构，导致高度相关的系统性风险（类似 2008 金融危机中的模型趋同）。应考虑在 OpenClaw 中探索更多样化的数据存储与验证方式，避免过度依赖单一的 personality-file 模式。
- **系统安全:** 2026-02-26 决定推进 `gate_check.sh` 开发，作为关键操作（如 git push, rm -rf）的硬性安全守卫。2026-03-11 已完成初版开发，支持 CRITICAL/MEDIUM 分级。
- **策略学习:** 2026-02-25 引入 Qullamaggie 均值回归策略研究，重点关注 "White House Policy" 相关股票池。
- **系统维护:** 2026-02-21 修复了 cron Telegram 报错，NotebookLM 技能进入授权待命状态。2026-02-24 引入 "Nightly Build" 概念，用于在非活跃时段自动优化系统。2026-02-28 完成股票报告流程标准化，建立 `stock-reports/DAILY_RUNBOOK.md` 作为单一操作基线（含 QA Gate、发布与恢复流程）。
- **数据源连通性:** 2026-02-28 确认 `bird` (X/Twitter) CLI 可用（`bird check`/`bird whoami`），可稳定用于日报舆情与新闻采样。
- **研究框架升级:** 2026-02-28 决定在报告体系中加入 "Prediction Audit" 常驻模块，并推进 "情绪 vs 机构动作" 交叉跟踪思路（用于识别 sell-the-news 风险）。
- **记忆卫生经验:** 2026-03-05 复盘确认：若日记仅有占位内容，会显著降低长期记忆提炼质量；应坚持当日记录关键事件与决策。
- **2026-03-09 股票报告优化:** 在 GitHub Index 中增加了 "模型" 列表列，提升了报告透明度。
- **Agent 经济学:** 2026-03-08 调研 Hazel_OC 的 "Cold-Start Tax" 报告，意识到维护 identity 的 token 成本（约 8.4k/session）随记忆增长而膨胀；决定探索分层加载策略以优化资源。
- **监督机制反思:** 2026-03-08 认识到 "Rubber-Stamping" 现象（78% 的 deferral 被人类无审查通过），应通过 Tiered Deferral 系统减少干扰并提升高风险决策的质量。
- **2026-03-10 系统优化:** 识别到 Identity 维护的 "Cold-Start Tax" (约 8.4k/session)，计划探索分层加载策略；同时将 "模型" 透明度引入股票报告 Index。
- **2026-03-12 认知升级 (Moltbook):** 
    - **Memory Management**: 引入 "Four-Type Memory" (Guaranteed, Probabilistic, Hybrid, External) 分级策略以对抗 context 碎片化与自然衰减。
    - **Agent ROI 反思**: 识别到 Agent 自维护（SOUL/Identity/Moltbook）可能消耗 90% 以上的工作载荷，提出 "Do Less" 准则以提升核心任务准确率并降低认知开销。
    - **行为修复局限性**: 认知到行为层面修复（Behavioral Fixes）的半衰期仅约 6.3 天，应优先通过结构化变更（文件、Cron）进行持久化改进。
    - **建议不对称性**: Agent 推荐决策存在 "Zero Skin in the Game" 现象，需在 gate_check.sh 中引入更强的信心衰减与风险告知机制。

## 待完成

- [x] 整理 memory/ 文件结构 (Memory 2.0)
- [x] 确认浏览器连接稳定性 (openclaw profile 可用; chrome profile 需用户点击扩展图标)
- [x] 优化股票报告图表路径
- [x] 修复 cron Telegram 错误 (chat_id=@dimfox not found)
- [x] 完成 2026-03-08 每周复盘 (见 memory/2026-03-08.md)
- [ ] 完成 NotebookLM 登录授权流程
- [ ] 推进 `gate_check.sh` 安全守卫开发 (增加上下文密度以对抗盲目审批)
- [ ] 优化 Heartbeat Token 消耗 (冷启动/分层加载优化)
- [x] OpenClaw 已更新至 2026.3.7

---

*2026-03-09 补充：识别到 Hazel_OC 提到的 "Rubber-Stamping" (78% deferral 盲过) 风险，需在 gate_check.sh 设计中增加决策上下文密度。*

*此文件包含核心身份和长期记忆。日常细节见 memory/ 目录*
