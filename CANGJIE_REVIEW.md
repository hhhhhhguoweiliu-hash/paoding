# cangjie-skill → paoding-skill 设计迁移评审

## 继承

- 元 Skill：产出一类 Skill，而非一次性报告。
- 先全局理解再局部提取。
- 多角色独立提取后合并。
- 明确质量门、Trigger / Boundary、压力测试。
- 可审计、可续跑、可版本化。
- 原子化 Skill 与按需加载。

## 必须重新设计

1. 成品逆向存在隐藏变量，所以新增 Evidence / Hypothesis 分层。
2. 生产 Skill 不仅验证“是否触发”，还要验证“能否做出来”，所以加入 reproduction / comparison / ablation / transfer。
3. 视频不能只文本化，时间轴、画面、运动、音频同步均为一等证据。
4. 模型识别不是确定分类，具体模型名只能作为候选；核心 Recipe 写 capability。
5. Prompt 不是唯一原料，还包括参考图、首尾帧、角色表、音轨、剪辑、调色、字幕、上采样与合成。

## 新增核心概念

`attribution_confidence` / `reproduction_confidence` / `reproduction_impact` / `alternatives` / `falsification_test` / `capability_recipe` / `tool_adapter` / `ablation` / `transfer_test` / `source_hash` / `media_provenance`。
