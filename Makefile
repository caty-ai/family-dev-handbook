# CI 門番 test-lint.yml の充て先 (#25 決裁: 4言語 README 構造検査を機械ゲート化 — R-6 の自己適用)。
# scripts/readme-check/inspect_readme.py は readme-craft skill 正本からのバイト同一 vendoring。
# ここでは改変しない — 更新は正本からの再コピーのみ。
# 正本 = README.ja.md (日本語が正)。翻訳 = README.md (en) / README.zh.md / README.th.md。
# カバー範囲はルート README 4本 + i18n/README.md のみ (docs/・templates/ 本文は無検査 — FP-5 明示)。

PY := python3 -B
CHECK := $(PY) scripts/readme-check/inspect_readme.py
READMES := README.ja.md README.md README.zh.md README.th.md
LINT_TARGETS := $(READMES) i18n/README.md

.PHONY: test lint

# test: 非空ガード + 4言語 README の構造一致 (見出し階層・コードブロック数・リンク/画像集合) — fail-closed
test:
	@set -e; for f in $(READMES); do test -s $$f || { echo "empty README: $$f" >&2; exit 1; }; done
	$(CHECK) langs README.ja.md README.md README.zh.md README.th.md

# lint: 各ファイル単体の整合 (相対リンク実在・アンカー解決・placeholder・見出し階層) — fail-closed
lint:
	@set -e; for f in $(LINT_TARGETS); do $(CHECK) inspect --no-work $$f; done
