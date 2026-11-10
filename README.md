# Project OS 2.0

面向本地项目的规格、评审、执行和证据交接流程。Spec Kit 1.3.0 管理规格，BMAD Method 6.12.0 用于评审，GSD Core 1.20.1 用于阶段执行。三个框架独立获取。

## 快速开始

门禁使用 Python 3 标准库。从仓库根目录执行：

    python test_p2_gate.py
    python p2_gate.py examples/demo
    python p2_gate.py examples/demo -- python -c "print('demo')"

门禁检查 GSD 的 STATE.md 进度与 ROADMAP.md 阶段复选框。已有完成阶段时，由验收人依据完成证据登记 .planning/p2-completed.json，例如 ["1"]。CONFLICT 表示暂停并核对证据，UNKNOWN 表示当前资料不足。直接启动工具会绕过门禁。并行任务各自使用独立的工作目录。

## 交接与验收

先用 Spec Kit 定规格，交 BMAD 记录评审与风险，再经门禁执行 GSD 或本地命令。登记退出码、产物、复核结论及可公开的证据。回归测试覆盖冲突拦截和受控启动。

doc_split 是已验证的外部使用场景。持有该工具和输入使用权限时，在独立工作目录准备脚本及获准输入，通过 python p2_gate.py <项目目录> -- python extract_refs.py 调用，再核对产物数量与内容。此发布候选包提供门禁、测试和虚构规划样例。

## 设计与交接

见 [设计与执行交接手册](docs/HANDOVER.md)。
