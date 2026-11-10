# Project OS 2.0 设计与执行交接

| 工具 | 已验证版本 | 交接职责 |
| --- | --- | --- |
| [Spec Kit](https://github.com/github/spec-kit) | 1.3.0 | 输出需求、范围和验收条件 |
| [BMAD Method](https://github.com/bmad-code-org/BMAD-METHOD) | 6.12.0 | 评审规格、登记风险与决定 |
| GSD Core | 1.20.1 | 维护阶段计划、执行摘要和恢复状态 |

1. 在项目副本中写规格，记录范围和每个验收条件。
2. 评审人确认规格、风险和放行条件，将结果交给 GSD 执行人。
3. 从本仓库运行 `python p2_gate.py <项目路径> -- <已批准命令>`。命令在目标目录执行。
4. 遇到 CONFLICT 时暂停。执行人保留原状态和错误，复核人对照路线图、摘要、提交与验收结果。完成阶段 ID 由验收人登记在 `.planning/p2-completed.json`。
5. 状态恢复后重跑，登记退出码、产物路径、SHA-256 和放行结论。使用独立输出目录。

运行 `python test_p2_gate.py` 复测门禁。直接运行目标命令可恢复原入口。门禁适用于经该入口启动的命令，支持的状态格式见 README。
