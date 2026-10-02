#!/usr/bin/env node

const fs = require('node:fs');
const path = require('node:path');

// Claude Code caps hook stdout at 10,000 characters. Anything above that is
// written to a file and replaced by a preview, which defeats the hook.
const MAX_CHARS = 9500;

const FALLBACK_CONTEXT = `SKILL BAHASA INDONESIA SEDERHANA AKTIF OTOMATIS

Terapkan Bahasa Indonesia sederhana ala ASD-STE100 untuk tugas tulis teknis. Gunakan kalimat pendek, kalimat aktif, satu istilah untuk satu makna, dan syarat sebelum perintah. Jangan ubah kode, identifier, perintah, atau kutipan galat.`;

const HEADER = [
  'SKILL BAHASA INDONESIA SEDERHANA AKTIF OTOMATIS',
  '',
  'Ikuti aturan tulis ini tanpa menunggu pengguna menyebut skill. Skill penuh, dengan katalog aturan dan mode periksa, ada di SKILL.md pada plugin ini. Baca berkas itu untuk pemeriksaan kepatuhan atau untuk mode strict.',
  '',
].join('\n');

function candidates(pluginRoot, hookDirectory, relative) {
  const roots = [];
  if (pluginRoot) {
    roots.push(pluginRoot);
  }
  roots.push(path.join(hookDirectory, '..', '..'), path.join(hookDirectory, '..'));
  return roots.map((root) => path.join(root, ...relative));
}

function promptCandidates(pluginRoot, hookDirectory) {
  return candidates(pluginRoot, hookDirectory, ['prompts', 'system-prompt.md']);
}

function readFirstFile(list) {
  for (const candidate of list) {
    try {
      return fs.readFileSync(candidate, 'utf8');
    } catch (error) {
      // Missing, unreadable, or a directory: try the next candidate.
    }
  }
  return '';
}

function stripFrontmatter(content) {
  return content.replace(/^---\r?\n[\s\S]*?\r?\n---\r?\n?/, '');
}

// prompts/system-prompt.md is a page for people: a title, a paragraph that says
// where to paste the block, the rule block between two "---" lines, then a
// word-budget variant. The model gets the fenced block only.
function ruleBlock(content) {
  const fence = /^---[ \t]*\r?$/m;
  const first = content.search(fence);
  if (first === -1) {
    return content;
  }
  const rest = content.slice(first).replace(fence, '');
  const second = rest.search(fence);
  return second === -1 ? rest : rest.slice(0, second);
}

function buildContext(promptText) {
  if (!promptText) {
    return FALLBACK_CONTEXT;
  }
  const out = HEADER + ruleBlock(stripFrontmatter(promptText)).trim();
  if (out.length > MAX_CHARS) {
    process.stderr.write(`simple-indonesia hook: payload is ${out.length} characters, over the ${MAX_CHARS} cap; sending the fallback ruleset\n`);
    return FALLBACK_CONTEXT;
  }
  return out;
}

function main() {
  const pluginRoot = process.env.PLUGIN_ROOT || process.env.CLAUDE_PLUGIN_ROOT;
  process.stdout.write(buildContext(readFirstFile(promptCandidates(pluginRoot, __dirname))));
}

if (require.main === module) {
  main();
}

module.exports = {
  FALLBACK_CONTEXT,
  MAX_CHARS,
  buildContext,
  promptCandidates,
  readFirstFile,
  ruleBlock,
  stripFrontmatter,
};
