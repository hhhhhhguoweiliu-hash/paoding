# Codex Implementation Brief — paoding-skill v0.1

## MVP 目标

给一个本地 mp4，系统产生结构完整、可审计、Schema 合法的 case bundle；即使没有视频生成 API，也必须明确区分事实 / 推断 / 未知，不伪造“已复现”。

## 已实现的 P0 基础

1. `paoding init <video>`：case 目录、SHA256、ffprobe、状态文件。
2. `paoding trace <case>`：固定间隔抽帧、时间戳 manifest、可选 wav。
3. Schema validator：Evidence / Shots / Hypotheses / Workflow / Reproduction。
4. Provider-agnostic reverse scaffold：可由人工或外部 LLM 填入结构化 hypothesis JSON。
5. Recipe assembler：强制 O/S/H/U、alternatives 与 unverified reproduction。
6. `paoding validate <case>`：文件完整性、Schema、证据引用、状态一致性。

## 后续 P1

- LLM provider interface 与 JSON repair 重试；
- 场景切分 + 多策略关键帧；
- Image / Video / Audio / Editor adapters；
- comparison engine 与 ablation runner；
- 首个真实视频生成 adapter。

## 关键约束

- 不把具体模型名写死在核心 Recipe Schema。
- `model_candidates` 是 hypothesis，不是 truth。
- 没运行真实生成器时：`reproduction.status = unverified`。
- source artifact 永不原地修改。
- mock 只测试结构，不提升 reproduction confidence。

## 推荐验收

用 3 个差异明显的短视频：产品广告、动漫叙事、音乐卡点 montage。每个 case 应满足：
- 核心推断可追溯到证据 ID；
- 无无证据的具体模型断言；
- 有完整 capability recipe；
- Schema 全通过；
- 未接真实生成器时明确 `unverified`；
- Production Skill 能迁移到同工艺不同主题。
