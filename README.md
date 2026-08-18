# paoding-skill（庖丁.skill） v0.1

> 把“看得见 / 听得见 / 用得到的成品”逆向蒸馏为可复现的生产工艺，再封装成可执行 Skill。

## 一句话定位

`paoding-skill` 不是成品总结器，也不是“猜作者原始 Prompt”的取证工具。它做的是：

**Finished Artifact → Evidence → Production Hypotheses → Equivalent Recipe → Reproduction Test → Executable Skill**

首版聚焦 **5–180 秒 AI 短视频**，但数据模型为后续扩展到图片、音乐、PPT、网页和交互产品预留空间。

## 核心原则

1. **复现优先于考古**：无法证明作者实际用了什么模型 / Prompt 时，不伪装成事实；目标是找到能稳定产出相似结果的等价生产工艺。
2. **观察与推断分离**：任何模型、参数、工作流判断都必须标注证据等级、替代假设与置信度。
3. **Skill 不是报告**：最终交付必须能再次执行，而不是停留在“看懂了”。
4. **模型无关 + 适配器双层**：先写 capability-level recipe，再映射到具体工具，避免模型更新导致 Skill 失效。
5. **必须闭环验证**：没真实生成就保持 `unverified`，不能纸面宣布复现成功。
6. **可审计、可续跑、可进化**：推断回指证据，阶段写入状态，失败进入测试集。

## TRACE-R

- **T — Trace**：采集元数据、时间轴、关键帧、镜头和音频证据。
- **R — Reverse**：多视角提出生产假设，并保存替代解释。
- **A — Assemble**：组装最小等价生产图。
- **C — Compare**：复现、对比、消融，判断真正关键的决策。
- **E — Encode**：将验证后的 Recipe 编码为 Production Skill。
- **R — Ratchet**：把失败案例加入测试集并版本化迭代。

## 安装

需要 Python 3.10+。视频 Trace 需要系统安装 `ffmpeg` / `ffprobe`。

```bash
python -m pip install -e .
paoding --help
```

## 最小可运行流程

```bash
paoding init demo.mp4
paoding trace cases/demo
paoding reverse cases/demo
paoding assemble cases/demo
paoding reproduce cases/demo --adapter mock
paoding validate cases/demo
paoding package cases/demo
```

> `mock` 只验证闭环结构，不代表完成真实生成；复现状态仍为 `unverified`。

## Case Bundle

```text
cases/<case-slug>/
├── PIPELINE_STATE.yaml
├── ARTIFACT_OVERVIEW.md
├── source-metadata.json
├── EVIDENCE_LEDGER.json
├── SHOT_MANIFEST.json
├── hypotheses/
├── RECONSTRUCTION_PLAN.md
├── WORKFLOW.yaml
├── RECIPE.md
├── prompts/
├── reproduction/
│   ├── runs.json
│   └── comparison.md
├── skill/
│   ├── SKILL.md
│   ├── repro-tests.json
│   └── test-results.md
└── AUDIT.md
```

## 证据等级

| 等级 | 含义 | 允许措辞 |
|---|---|---|
| O | 直接观察到 | “成品中可见 / 可听 / 元数据表明……” |
| S | 多条证据支持的推断 | “更可能是……，因为……” |
| H | 合理但非唯一的假设 | “候选之一是……；替代方案为……” |
| U | 不可判断 | “仅凭成品无法可靠判断。” |

**禁止**仅凭视觉风格就断言具体模型、Prompt、Seed、LoRA 或隐藏参数。

## 当前 v0.1 能做什么

- 初始化 case、记录 SHA256 与媒体元数据；
- 用 ffmpeg 固定间隔抽取证据帧与可选音轨；
- 生成可人工或外部 LLM 填充的 Hypothesis scaffold；
- 生成 provider-agnostic Recipe / Workflow；
- 通过 JSON Schema 与交叉引用做结构验证；
- 用 `mock` 跑通 reproduction 结构但保持 `unverified`；
- 打包 case 供审计、续跑和迁移。

## 当前 v0.1 不声称什么

- 不声称能法证式识别作者真实模型或私有 Prompt；
- 不声称已经接入任何具体商业视频生成 API；
- 不把 mock 运行计作真实复现；
- 不保证像素级复制；
- 不复制未经授权的真人身份、私有素材或受限制资产。

## 给 Codex 的阅读顺序

`CODEX_BRIEF.md` → `SKILL.md` → `docs/ARCHITECTURE.md` → `methodology/` → `schemas/`。
