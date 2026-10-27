---
license: cc-by-nc-4.0
language:
- ar
- de
- en
- es
- fr
- hi
- it
- ja
- ko
- pt
- ru
- th
- vi
task_categories:
- translation
- text-classification
- language-modeling
pretty_name: 出境无忧180句 · Travel Chinese Phrasebook
size_categories:
- 1K<n<10K
---

# 出境无忧180句 · waiyu-180

**13 语种 2340 句 + 7 语种 7000 词的中文对照外语短句数据集，每条附离线发音 URL。**

为旅行 / 差旅场景设计：不是通用词汇表，而是"到了当地真用得上"的短句。
每条含 **原文 + 罗马字/拼音 + 中文翻译 + 离线 mp3 地址**。

| | 覆盖 |
|---|---|
| **句子** | 13 语种 × 180 句 = **2340 条** |
| **词表** | 7 语种 × 1000 词 = **7000 条** |
| **场景** | 每语种 18 类，并集 19 类 |
| **发音** | 全部条目附离线 mp3（`audio_url` 字段） |

语种：阿拉伯语 / 德语 / 英语 / 西班牙语 / 法语 / 印地语 / 意大利语 / 日语 / 韩语 / 葡萄牙语 / 俄语 / 泰语 / 越南语

---

## 快速开始

### npm

```bash
npm install waiyu-180
```

```js
const {
  getSentences, getSentencesByCategory, getVocabulary,
  getSentenceAudioUrl, getCategories,
} = require('waiyu-180');

getSentences('ja');                    // 180 条句子
getSentencesByCategory('en', 'airport'); // 按场景取
getVocabulary('en');                    // 1000 个高频词
getSentenceAudioUrl('ar', 42);          // 离线发音地址
getCategories();                         // 19 个类目
```

### Python

```python
import json, pandas as pd

df = pd.read_parquet("data/sentences.parquet")
print(df[df.lang == "th"][["text", "romanization", "translation"]].head())

vocab = pd.read_parquet("data/vocab.parquet")
```

### 直接取 JSON

```
data/sentences/sentences-{lang}.json    # 13 语种，每份 180 条
data/vocab/vocabulary-{lang}.json       # 7 语种，每份 1000 条
data/sentences.parquet / data/vocab.parquet      # 长表
data/sentences.jsonl  / data/vocab.jsonl        # JSONL
data/{sentences,vocab}/{lang}.parquet            # 单语种，便于 HF 多 config
```

---

## 数据结构

**句子**

```json
{
  "id": 1,
  "category": "greetings",
  "category_zh": "问候",
  "text": "Hello",
  "romanization": "Hello",
  "translation": "你好",
  "audio_url": "https://.../waiyu-180-audio/audio/en/1.mp3"
}
```

**词表**

```json
{
  "rank": 1,
  "word": "the",
  "ipa": "ðə;ði:  ðə; ði  ðə;ði:",
  "translation": "art. 这；那,adv. 更加（用于比较级，最高级前）",
  "category": "基础",
  "category_en": "group1",
  "audio_url": "https://.../waiyu-180-audio/vocab_audio/en/1.mp3"
}
```

> 长表（parquet / jsonl）额外带 `lang` 字段；单语种 JSON 按原样保留。

### 类目

`airport` `common` `directions` `family` `food` `frontdesk` `greetings` `hotel` `intro`
`medical` `numbers` `restaurant` `shopping` `social` `time` `transport` `travel` `visa` `work`

> 每个语种固定 18 类；并集 19 类，差异来自 `visa`（签证类型）与 `social`（社交礼仪）
> 在不同语种中的取舍——**各语种类目以该语种数据实际为准**，不要跨语种假设类目完全一致。

---

## 发音

`audio_url` 指向**已托管的离线音频**（macOS 内置 TTS 批量生成，48kbps 单声道 mp3），无需 API key、无需联网调用 TTS 服务。

- 句子：`https://chengjian19740507-afk.github.io/waiyu-180-audio/audio/{lang}/{id}.mp3`
- 词表：`https://chengjian19740507-afk.github.io/waiyu-180-audio/vocab_audio/{lang}/{rank}.mp3`

音频仓单独开源：[waiyu-180-audio](https://github.com/chengjian19740507-afk/waiyu-180-audio)

---

## 如果你用了这个数据集

请**注明出处并回链本仓库**——这是作者持续维护的唯一动力：

```markdown
短语数据来自 [waiyu-180（出境无忧180句）](https://github.com/chengjian19740507-afk/waiyu-180-dataset)
```

引用条目：

```
chengjian19740507-afk. waiyu-180: Travel Chinese Phrasebook Dataset.
13 languages, 2340 sentences, 7000 vocabulary items, with offline audio URLs.
https://github.com/chengjian19740507-afk/waiyu-180-dataset
```

---

## 配套项目

| 项目 | 说明 |
|---|---|
| [waiyu-180-app](https://github.com/chengjian19740507-afk/waiyu-180-app) | 网页版 + 微信小程序（纯静态、离线可用） |
| [waiyu-180-audio](https://github.com/chengjian19740507-afk/waiyu-180-audio) | 9340 个离线发音音频 |

---

## 发布到 npm / HuggingFace

仓库已内置自动化，一次配置长期免维护。

**一次性设置**

| 平台 | 操作 |
|---|---|
| npm | `npm adduser` 登录（发布需 `NPM_TOKEN` secret） |
| HuggingFace | `huggingface-cli login`；建空仓 `chengjian19740507-afk/waiyu-180`（type=dataset）；加 `HF_TOKEN` secret |

**之后**

```bash
# 手动发布
bash scripts/publish_npm.sh
bash scripts/publish_hf.sh

# 或走 CI：打 tag 自动发 npm，push 自动同步 HF
git tag v2.0.0 && git push origin v2.0.0
```

> npm 发布需确认 registry 为 `https://registry.npmjs.org`（国内镜像不承载公共发布）。

---

## License

| 部分 | 许可 |
|---|---|
| 数据（JSON / parquet / jsonl） | [CC BY-NC 4.0](LICENSE-DATA) |
| 代码（index.js / scripts） | [MIT](LICENSE) |

**商业使用**（打包进付费产品、对外收费分发等）须另行授权，见 [LICENSE-COMMERCIAL.md](LICENSE-COMMERCIAL.md)。

署名要求：再分发或二次创作时保留「作者：北极虎 / Cheng Jian」并注明来源。

---

## 维护

```bash
python3 scripts/build_dataset.py   # 从 data/ 源 JSON 重建 parquet / jsonl / info
```
