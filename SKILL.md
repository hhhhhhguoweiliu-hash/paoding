---
name: paoding-skill
description: Reverse-distill a finished AI-created artifact, especially a short video, into an evidence-backed equivalent production recipe and an executable production skill. Use when the user says “拆这个视频/还原它怎么做的/逆推提示词和模型/我也想做出这种效果/reverse engineer this artifact”. Do not claim exact historical prompts, seeds, models, LoRAs, or private workflow details unless the artifact or metadata provides direct evidence.
---

# paoding-skill — 成品逆向蒸馏元 Skill

## 使命

面对一个已经完成的成品，不止描述“它是什么”，而是回答：
- 它由哪些可观察结构组成？
- 哪些生产决策最可能导致这些结构？
- 哪些原料、模型能力和后期步骤可以等价实现？
- 哪些结论是事实、强推断、弱假设或未知？
- 怎样用最低成本做一次复现测试？
- 怎样把验证后的工艺封装为下次可调用的 Production Skill？

## v0.1 范围

优先支持：5–180 秒 AI 短视频（有 / 无音频均可）。

暂不把以下目标作为成功标准：
- 精确识别作者私有 Prompt、Seed、隐藏参数；
- 仅凭视觉“指纹”确认具体模型；
- 像素级复制原作；
- 未经授权复制真人身份、私有素材或受限制资产。

## TRACE-R 执行顺序

1. Stage 0 — Scope & Provenance：`methodology/01-stage0-scope.md`
2. Stage 1 — Trace：`methodology/02-stage1-trace.md`
3. Stage 2 — Parallel Reverse：`methodology/03-stage2-parallel-reverse.md`
4. Stage 3 — Evidence Verification：`methodology/04-stage3-verify.md`
5. Stage 4 — Assemble Equivalent Recipe：`methodology/05-stage4-assemble.md`
6. Stage 5 — Compare & Reproduce：`methodology/06-stage5-compare.md`
7. Stage 6 — Encode Production Skill：`methodology/07-stage6-encode.md`
8. Stage 7 — Ratchet & Deliver：`methodology/08-stage7-ratchet-deliver.md`

## 质量红线

1. `O/S/H/U` 证据等级必须存在；不得把 H 写成事实。
2. 具体模型识别如无直接证据，只能作为带替代候选的假设。
3. Recipe 必须区分 `capability_recipe` 与 `tool_adapter`。
4. 不能只给 Prompt；必须覆盖资产、镜头、运动、音频、剪辑与质量门。
5. 未实际复现时，测试状态必须是 `unverified`。
6. Skill 必须包含正触发、负触发、边界测试与至少一个迁移测试。
7. 核心推断必须能回指时间戳或元数据证据；若无证据，则明确标 U。
8. 复现相似度与历史归因是两件事：`reproduction_confidence` 高不等于 `attribution_confidence` 高。

## 默认执行策略

- 先获取 / 读取原始成品，不先猜模型。
- 对视频先全局观看，再按镜头和时间轴拆分；字幕只是证据之一。
- 为关键生产结论至少保留一个替代假设或说明“暂无替代”。
- 优先找“最小可行等价工艺”，再补复杂节点。
- 若没有真实生成工具，输出 Recipe + falsification plan，并保持 `unverified`。
- 若能真实复现，则至少比较 composition / style / identity / motion / timing / audio-sync / text / signature-effect 中适用的维度。

## 断点续跑

每阶段完成后更新 `PIPELINE_STATE.yaml`：
`source_hash`、`completed_stages`、`artifacts_produced`、`unresolved_hypotheses`、`reproduction_status`、`next_action`。

状态文件存在时，从最后一个合法阶段继续，不覆盖原始成品。
