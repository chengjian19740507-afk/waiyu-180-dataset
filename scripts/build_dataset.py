#!/usr/bin/env python3
"""
构建 HuggingFace / npm 数据集产物。

产物：
  data/sentences/<lang>.json    13 语种 × 180 句
  data/vocab/<lang>.json         7 语种 × 1000 词
  data/sentences.parquet          句子（长表，含 audio_url）
  data/vocab.parquet              词表（长表，含 audio_url）
  data/sentences.jsonl            句子（JSONL）
  data/vocab.jsonl                词表（JSONL）
  dataset_info.json               统计元信息

audio_url 指向已上线的 GitHub Pages 音频库（不重复存 74MB 音频）。
"""
import json, hashlib, sys
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
AUDIO_BASE = "https://chengjian19740507-afk.github.io/waiyu-180-audio"

SENT_LANGS = ['ar','de','en','es','fr','hi','it','ja','ko','pt','ru','th','vi']
VOCAB_LANGS = ['ar','en','es','fr','ja','ko','ru']

def md5(p: Path) -> str:
    return hashlib.md5(p.read_bytes()).hexdigest()

def build_sentences():
    rows = []
    for lang in SENT_LANGS:
        src = ROOT / 'data' / 'sentences' / f'sentences-{lang}.json'
        for it in json.load(open(src, encoding='utf-8')):
            rows.append({
                'lang': lang,
                'id': it['id'],
                'category': it['category'],
                'category_zh': it['category_zh'],
                'text': it['text'],
                'romanization': it['romanization'],
                'translation': it['translation'],
                'audio_url': f'{AUDIO_BASE}/audio/{lang}/{it["id"]}.mp3',
            })
    return rows

def build_vocab():
    rows = []
    for lang in VOCAB_LANGS:
        src = ROOT / 'data' / 'vocab' / f'vocabulary-{lang}.json'
        for it in json.load(open(src, encoding='utf-8')):
            rows.append({
                'lang': lang,
                'rank': it['rank'],
                'word': it['word'],
                'ipa': it.get('ipa', ''),
                'translation': it.get('translation', ''),
                'category': it.get('category', ''),
                'category_en': it.get('category_en', ''),
                'audio_url': f'{AUDIO_BASE}/vocab_audio/{lang}/{it["rank"]}.mp3',
            })
    return rows

def write_jsonl(rows, path):
    with open(path, 'w', encoding='utf-8') as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + '\n')

def main():
    sent = build_sentences()
    vocab = build_vocab()

    pd.DataFrame(sent).to_parquet(ROOT / 'data' / 'sentences.parquet', index=False)
    pd.DataFrame(vocab).to_parquet(ROOT / 'data' / 'vocab.parquet', index=False)
    write_jsonl(sent, ROOT / 'data' / 'sentences.jsonl')
    write_jsonl(vocab, ROOT / 'data' / 'vocab.jsonl')

    # 每个语种单独一份 parquet（HF 多 config 用）
    for lang in SENT_LANGS:
        pd.DataFrame([r for r in sent if r['lang'] == lang]).to_parquet(
            ROOT / 'data' / 'sentences' / f'{lang}.parquet', index=False)
    for lang in VOCAB_LANGS:
        pd.DataFrame([r for r in vocab if r['lang'] == lang]).to_parquet(
            ROOT / 'data' / 'vocab' / f'{lang}.parquet', index=False)

    cats = sorted({r['category'] for r in sent})
    info = {
        'name': 'waiyu-180',
        'version': '2.0.0',
        'license': 'CC-BY-NC-4.0',
        'audio_base': AUDIO_BASE,
        'sentences': {
            'total': len(sent),
            'langs': SENT_LANGS,
            'per_lang': 180,
            'categories': cats,
            'category_count': len(cats),
        },
        'vocabulary': {
            'total': len(vocab),
            'langs': VOCAB_LANGS,
            'per_lang': 1000,
        },
        'files': {},
    }
    for f in sorted((ROOT / 'data').rglob('*')):
        if f.is_file():
            rel = f.relative_to(ROOT).as_posix()
            info['files'][rel] = {'bytes': f.stat().st_size, 'md5': md5(f)}
    (ROOT / 'dataset_info.json').write_text(
        json.dumps(info, ensure_ascii=False, indent=2), encoding='utf-8')

    print(f'✓ sentences: {len(sent)} 行 ({len(SENT_LANGS)} 语种 × 180, {len(cats)} 类)')
    print(f'✓ vocabulary: {len(vocab)} 行 ({len(VOCAB_LANGS)} 语种 × 1000)')
    print(f'✓ parquet + jsonl + 单语种 parquet 已生成')
    print(f'✓ dataset_info.json: {len(info["files"])} 个文件带 md5')

if __name__ == '__main__':
    sys.exit(main())
