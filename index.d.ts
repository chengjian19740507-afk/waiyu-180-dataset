/** 出境无忧180句 · 13 语种 2340 句 + 7 语种 7000 词 */

export type SentenceLang =
  | 'ar' | 'de' | 'en' | 'es' | 'fr' | 'hi' | 'it'
  | 'ja' | 'ko' | 'pt' | 'ru' | 'th' | 'vi';

export type VocabLang = 'ar' | 'en' | 'es' | 'fr' | 'ja' | 'ko' | 'ru';

export interface Sentence {
  id: number;
  category: string;
  category_zh: string;
  text: string;
  romanization: string;
  translation: string;
}

export interface VocabEntry {
  rank: number;
  word: string;
  ipa: string;
  translation: string;
  category?: string;
  category_en?: string;
}

export const SENTENCE_LANGS: SentenceLang[];
export const VOCAB_LANGS: VocabLang[];
export const AUDIO_BASE: string;

export function getSentences(lang: SentenceLang): Sentence[];
export function getSentencesByCategory(lang: SentenceLang, category: string): Sentence[];
export function getVocabulary(lang: VocabLang): VocabEntry[];
export function getSentenceAudioUrl(lang: SentenceLang, id: number): string;
export function getWordAudioUrl(lang: VocabLang, rank: number): string;
export function getCategories(): string[];
