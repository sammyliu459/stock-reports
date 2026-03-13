# Runbook: 每日日记文件（memory/YYYY-MM-DD.md）

## 目的
保证 `memory/` 每天都有当日文件，避免连续性中断。

## 范围
- 仅管理文件存在性（create-if-missing）
- 不覆盖已有内容
- 不做历史批量改写

## 文件规范
- 路径：`/home/dimfox/.openclaw/workspace/memory/`
- 命名：`YYYY-MM-DD.md`（本地时区：America/Los_Angeles）
- 模板（新建时）：

```md
# Daily Log

- Created automatically to keep daily memory continuity.
- Add key events, decisions, and follow-ups here.
```

## 执行时机
1. 每次会话启动时
2. 每次收到用户消息时（轻量检查）
3. 心跳轮询时（若启用）

## 标准流程（SOP）
1. 计算“今天”日期（PST/PDT）
2. 检查 `memory/YYYY-MM-DD.md` 是否存在
3. 若不存在：按模板创建
4. 若存在：不改动
5. （可选）补建“昨天”文件，仅在缺失时创建

## 命令参考（手动修复）
```bash
for d in $(date +%F) $(date -d 'yesterday' +%F); do
  f="/home/dimfox/.openclaw/workspace/memory/${d}.md"
  [ -f "$f" ] || cat > "$f" <<'EOF'
# Daily Log

- Created automatically to keep daily memory continuity.
- Add key events, decisions, and follow-ups here.
EOF
done
```

## 异常处理
- `memory/` 不存在：先创建目录后重试
- 权限不足：记录错误并提示人工处理
- 日期异常（时区配置错）：优先修正时区，再补建文件

## 验收标准
- 当天文件存在
- 文件未覆盖已有日志
- 近两天（today/yesterday）无缺口

## 变更记录
- 2026-03-02：初版创建
