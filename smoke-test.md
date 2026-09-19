# Smoke Test · 2026-09-19

结果：**通过**

## 结构检查

- frontmatter `name`: `ai-decision-evidence-auditor`，lowercase-hyphen，通过。
- description: 77 字符，以 `Audits` 开头，并包含触发条件，通过。
- 必要章节：核心定位、触发场景、工作流、输出格式、Gotchas 均存在。
- 工作流：7 步，位于要求的 3–8 步范围内。
- Gotchas：8 条；未发现 TODO、TBD 或未填充占位符。

## README 检查

- 安装路径、仓库名和文件树均使用 `ai-decision-evidence-auditor`。
- 中文开发目录未被误写为安装目录。
- 示例触发词与 SKILL.md 一致；示例说明 BLOCK 会返回退出码 2。

## 自动测试

命令：`python -m unittest discover -s tests -v`

结果：6/6 通过。覆盖直接证据、缺证、部分支持、高影响主张、矛盾、重复 ID 与重复 URL。

## 触发干运行

1. 中文：“帮我审计这份 AI 竞品报告的证据链，哪些结论不能用于采购决策？”
   - 自然触发；输出主张台账、来源支持判断、时效检查和 PASS/REVIEW/BLOCK，不停在抽象建议。
2. English：“Audit the evidence chain in this AI-generated policy memo before we brief leadership.”
   - 自然触发；输出 claim ledger、source/support review、decision gate 和 scoped decision note。
3. 非触发：“把这份报告润色得更专业。”
   - 不触发，应转写作/润色技能。

## CLI 干运行

命令：`python scripts/audit_claims.py examples/demo-claims.json --out demo-audit.md`

结果：报告正确产生；一条官方来源主张为 PASS，一条故意缺证的高影响主张为 BLOCK；退出码 2 属预期阻断信号。

## 限制

本 smoke test 验证结构、规则和示例路由推理，不是宿主级独立技能路由测试；脚本不联网，也不替人工判断网页内容是否真实支持主张。
