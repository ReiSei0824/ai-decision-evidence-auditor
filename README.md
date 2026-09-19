# AI 决策证据链审计师 · AI Decision Evidence Auditor

把 AI 生成的研究、报告和决策材料拆成可核验主张，逐项检查来源、蕴含关系、时效和决策影响，并交付 PASS / REVIEW / BLOCK 结论。

## 触发词

- “审计这份 AI 报告的证据链”
- “逐条核对研究结论和来源”
- “Audit the evidence chain in this AI-generated decision memo”

## 流程

冻结决策边界 → 建立主张台账 → 阅读来源并判断支持关系 → 检查时效与独立性 → 运行结构检查 → 设置决策门槛 → 交付证据包。

## 示例

```powershell
python scripts/audit_claims.py examples/demo-claims.json --out demo-audit.md
python -m unittest discover -s tests -v
```

演示包含一条有官方来源的主张和一条故意缺证据的高影响主张，因此命令会生成报告并以退出码 2 提示存在 BLOCK。这是预期行为。

## 安装

仓库名和安装目录必须使用 frontmatter slug：

```bash
git clone https://github.com/ReiSei0824/ai-decision-evidence-auditor.git ~/.claude/skills/ai-decision-evidence-auditor
```

不要把开发机上的中文目录名当作安装目录；若目标目录已存在，请选新位置，不覆盖。

## 文件树

```text
ai-decision-evidence-auditor/
├── SKILL.md
├── README.md
├── scripts/audit_claims.py
├── tests/test_audit.py
├── examples/demo-claims.json
├── examples/trigger-dry-runs.md
├── smoke-test.md
└── publish-checklist.md
```

## 边界

脚本只检查台账结构和决策规则，不访问网络，也不证明来源为真。高风险领域必须保留人工阅读和专业复核；真实敏感材料不得提交到公开仓库。
