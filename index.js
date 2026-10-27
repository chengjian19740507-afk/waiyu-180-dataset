/**
 * waiyu-180 · 出境无忧180句
 * 13 语种 2340 句 + 7 语种 7000 词的中文对照外语短句数据集
 *
 * 数据许可：CC BY-NC 4.0（见 LICENSE-DATA）
 * 项目主页：https://github.com/chengjian19740507-afk/waiyu-180-dataset
 */

'use strict';

const path = require('path');
const fs = require('fs');

const SENTENCE_LANGS = ['ar','de','en','es','fr','hi','it','ja','ko','pt','ru','th','vi'];
const VOCAB_LANGS = ['ar','en','es','fr','ja','ko','ru'];

const AUDIO_BASE = 'https://chengjian19740507-afk.github.io/waiyu-180-audio';

let _sentCache = Object.create(null);
let _vocabCache = Object.create(null);

function readJSON(rel) {
  return JSON.parse(fs.readFileSync(path.join(__dirname, rel), 'utf8'));
}

/** 取某语种全部句子（180 条） */
function getSentences(lang) {
  if (!SENTENCE_LANGS.includes(lang)) {
    throw new Error(`unsupported language: ${lang} (available: ${SENTENCE_LANGS.join(', ')})`);
  }
  if (!_sentCache[lang]) _sentCache[lang] = readJSON(`data/sentences/sentences-${lang}.json`);
  return _sentCache[lang];
}

/** 按类目取句，如 getSentencesByCategory('en', 'airport') */
function getSentencesByCategory(lang, category) {
  return getSentences(lang).filter((s) => s.category === category);
}

/** 取某语种词表（1000 词） */
function getVocabulary(lang) {
  if (!VOCAB_LANGS.includes(lang)) {
    throw new Error(`unsupported language: ${lang} (available: ${VOCAB_LANGS.join(', ')})`);
  }
  if (!_vocabCache[lang]) _vocabCache[lang] = readJSON(`data/vocab/vocabulary-${lang}.json`);
  return _vocabCache[lang];
}

/** 句子发音地址（离线生成，随数据集分发） */
function getSentenceAudioUrl(lang, id) {
  return `${AUDIO_BASE}/audio/${lang}/${id}.mp3`;
}

/** 单词发音地址 */
function getWordAudioUrl(lang, rank) {
  return `${AUDIO_BASE}/vocab_audio/${lang}/${rank}.mp3`;
}

/** 全部类目（各语种 18 类，并集 19 类） */
function getCategories() {
  const set = new Set();
  SENTENCE_LANGS.forEach((l) => getSentences(l).forEach((s) => set.add(s.category)));
  return Array.from(set).sort();
}

module.exports = {
  getSentences,
  getSentencesByCategory,
  getVocabulary,
  getSentenceAudioUrl,
  getWordAudioUrl,
  getCategories,
  SENTENCE_LANGS,
  VOCAB_LANGS,
  AUDIO_BASE,
};
