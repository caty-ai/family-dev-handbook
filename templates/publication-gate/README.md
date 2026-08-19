# templates/publication-gate — 公開前ゲートの配布用 stencil

家族のリポが対外公開用の表示に個人用 URL・公開禁止語・不整合な公開ラベルを残したまま
merge されるのを、ローカルと CI の同じ検査で止めるための配布用の型。正本は
`templates/publication-gate/check_publication_gate.py`。導入先では例えば
`tools/check_publication_gate.py` としてコピーし、リポ固有のポリシーだけをルートの外部ファイルで持つ。

これは公開前の**機械の一次ゲート**であり、人間の公開決裁や多席レビューの代替ではない。
スクリプトが赤を返すだけでは merge は止まらないため、導入先の CI job を branch protection の
required status check に登録して初めて「保護済み」と扱う。

## 何を守るか

| 検査 | 守るもの | レジストリなしの挙動 |
|---|---|---|
| 外部 denylist | リポ固有の公開禁止語が corpus に残らないこと | 常に検査 |
| 個人用 URL | `--account-slug` の個人アカウント URL が残らないこと | アカウント profile もその slug 下のリポ URL も、corpus 内の any-hit で1件でも見つかれば赤 |
| 個人 URL の registry allowlist | 台帳で公開対象と宣言した URL だけを個人用 URL 検査から免除すること | allowlist 検査を skip し、明示的な notice を出す |
| 公開ラベル | 台帳の対象に公開ラベルが無い状態を残さないこと | 「ラベル欠落」検査を skip し、notice を出す |
| SVG 状態 | README の表示と台帳の公開状態が食い違わないこと | 検査を skip し、notice を出す |
| label whitelist の stale | 一時的な例外が台帳変更後も残らないこと | 検査を skip し、notice を出す |

`--registry` は任意。省略した場合も denylist と個人用 URL の検査は実行し、確認不能な
4検査を黙って緑にせず、それぞれ skip notice を出す。corpus のアンカーは、レジストリ有りなら
指定した JSON ファイル、無しなら `<root>/README.md` へ fallback する。カレントディレクトリ下の別 README を
偶然拾って判定の起点にはしない。レジストリなしで `<root>/README.md` も無い場合は、corpus floor を
確立できないため赤になる。

## 展開手順（コピペ順）

1. checker を導入先へコピーする。配置先はリポの慣例に合わせてよいが、以下では
   `tools/check_publication_gate.py` とする。
   ```bash
   cp templates/publication-gate/check_publication_gate.py <target-repo>/tools/check_publication_gate.py
   ```
2. sample denylist を導入先リポのルートへコピーし、実ポリシーに置き換える。
   `.publication-denylist` は必須で、無い・空のままなら赤になる。
   ```bash
   cp templates/publication-gate/fixtures/sample.publication-denylist <target-repo>/.publication-denylist
   ```
3. CI に通常検査を配線する。レジストリを持つリポは `--registry` も渡す。
   ```bash
   python3 -B tools/check_publication_gate.py \
     --root . \
     --account-slug "$PUBLICATION_ACCOUNT_SLUG" \
     --registry path/to/modules.json
   ```
   レジストリを使わないリポは最後の2引数を省略する。`--registry` を省略しても
   `--account-slug` は省略できない。個人用 URL 検査は通常実行で常に有効で、slug 未指定は
   ゲートの設定不備として赤になる。
4. checker の self-test と導入先のテストを同じ CI job か依存 job で実行し、その status
   check を branch protection の required に登録する。ローカルでも同じ経路が通るよう
   Makefile の `test` ターゲットに配線し、導入完了前に実行する。
   ```bash
   python3 -B tools/check_publication_gate.py --selftest
   make test
   ```

本ハンドブック自身の `make test` も、配布用 checker の `--selftest` を実行する。

## `.publication-denylist` の正確な形式

ファイルは UTF-8 テキスト。1行1ルールで、次の形式だけを受け付ける。

```text
NAME<TAB>REGEX
```

- 空行と、**先頭文字**が `#` の行は無視する。`#` の前に空白がある行はコメントではない。
- 最初のタブだけで `NAME` と `REGEX` に分ける。正規表現側にタブを含める場合も、第2フィールドの
  一部として扱う。
- `NAME` と `REGEX` はどちらも空にできない。`REGEX` は Python `re` の構文で、
  `re.IGNORECASE` でコンパイル・照合する。
- タブの無い行、空のフィールド、コンパイルできない正規表現、UTF-8 として読めないファイルは
  **malformed = 赤**。
- `.publication-denylist` 自体の不在と、コメント/空行を除く有効ルール0件はどちらも**赤**。

denylist は検出すべき禁止リテラルを必然的に含む。そのため checker は、スキャン対象から
`<root>/.publication-denylist` を**パスで**自己除外する。過去のようにスクリプト内で禁止語を分割文字列にして
検出をかわすハックは不要。ポリシーと実装を分けたまま、自己検知だけを明示的に除外できる。

## 任意の `.publication-label-whitelist`

公開ラベルの既知の例外が必要なときだけ、リポルートに作成する。UTF-8、1行1例外で形式は次の通り。

```text
PATH<TAB>EXACT_LINE
```

`PATH` と、そのファイル内で許可する `EXACT_LINE` の完全一致だけを免除する。このファイルは
**言い訳だけを追加する** allowlist であり、新しい問題を検出するポリシーではない。したがって不在時は
fail-open（免除なしとして継続）でよい。denylist の不存を赤にするのとは非対称だが、意図的な設計である。
`--registry` が無い場合は whitelist-staleness を判定できないため、その検査は notice 付きで skip する。

## CLI

| 引数 | 必須性 / 既定値 | 意味 |
|---|---|---|
| `--root PATH` | 任意、既定 `.` | 検査対象リポのルート。ポリシーファイルと、レジストリ省略時の `README.md` のアンカー |
| `--account-slug SLUG` | 通常検査で必須、既定なし | 公開物に残してはいけない個人アカウントの slug。未指定は赤 |
| `--registry PATH` | 任意、既定なし | 公開リポ台帳の JSON ファイル。無い場合は台帳依存の4検査だけを notice 付きで skip |
| `--selftest` | 任意、既定 `false` | 内蔵 fixture で parser・検出・fail posture を検査して終了 |

## スキャン対象と Git の無い環境

Git worktree では Git から得られる corpus を使う。アーカイブ展開後やコピー先など Git の無い環境でも
検査自体を消さず、`Path.rglob()` 相当でルート以下を再帰走査する。その際は次のディレクトリを対象外にする。

```text
.git
.omc
.omx
.venv
venv
node_modules
__pycache__
```

## family-os / organization `.github` からの移行

`family-os` と organization `.github` にある局所コピーは、この stencil の挙動を先に確定した後、
後続の **B9 lane** で置き換える。このテンプレート導入と既存リポの移行を同じ diff で混ぜない。

移行時の意図的な差分は2つ。

- 旧コピーの email masking のバグは修正済みで、新チェッカーの方が**厳格**。以前通っていた表記が
  新しく赤になった場合、検知退行ではなく bug fix の結果として対象テキストを直す。
- 外部 `.publication-denylist` は必須。先にファイルを配置・カスタマイズせず checker だけを切り替えると、
  ゲートは意図的に赤のままになる。

移行 PR では `--selftest`、対象リポの `make test`、通常 CLI の実行結果、CI status check の
required 登録を証拠として残す。
