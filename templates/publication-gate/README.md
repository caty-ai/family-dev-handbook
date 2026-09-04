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
| 個人用 URL | `--account-slug` の個人アカウント URL が残らないこと | アカウント profile、slug 下のリポ URL、gist、GitHub Pages の any-hit が1件でも見つかれば赤 |
| 個人 URL の registry allowlist | 台帳で公開対象と宣言した URL だけを個人用 URL 検査から免除すること | allowlist 検査を skip し、明示的な notice を出す |
| 公開ラベル | 台帳の対象に公開ラベルが無い状態を残さないこと | 「ラベル欠落」検査を skip し、notice を出す |
| SVG 状態 | README の表示と台帳の公開状態が食い違わないこと | 検査を skip し、notice を出す |
| label whitelist の stale | 一時的な例外が台帳変更後も残らないこと | whitelist が不在/空なら検査を skip して notice、1件以上なら赤 |

通常検査では `--registry` か `--no-registry` のどちらかを明示する。両方を省略した場合と、両方を
指定した場合は設定不備として赤になる。`--no-registry` を明示した場合も denylist と個人用 URL の
検査は実行し、`<root>/registry/modules.json` と非空の `.publication-label-whitelist` のどちらも無い時に限り、
確認不能な4検査を黙って緑にせず、それぞれ skip notice を出す。`<root>/registry/modules.json` が存在する、
または非空の `.publication-label-whitelist` がある状態で `--no-registry` を指定した場合は赤になる。
`registry/modules.json` と非空の label whitelist だけが checker が
知り得る on-disk signal であり、custom path の registry は caller が `--registry` で渡す責任を負う。corpus の
アンカーは、レジストリ有りなら指定した JSON ファイル、明示的なレジストリなしなら
`<root>/README.md` へ fallback する。カレントディレクトリ下の別 README を偶然拾って判定の起点には
しない。レジストリなしで `<root>/README.md` も無い場合は、corpus floor を確立できないため赤になる。

個人用 URL は URL 候補を解析して host を正規化してから照合する。`github.com/<slug>` に加え、
`github.com:443/<slug>`、`github.com./<slug>`、`gist.github.com/<slug>`、
`<slug>.github.io` も対象になる。host の port は無視し、末尾の dot は1個だけ除く。
URL 候補の path 内に `github.com/<slug>`・`gist.github.com/<slug>`・`<slug>.github.io` が現れる場合
（`foo.bar/github.com/<slug>/<repo>`、`?u=github.com/<slug>/...`、`github.com\/<slug>\/...`）も
personal-url として赤にする。`https://example.org/docs/github.com/<slug>/<repo>` のような無関係ホストの
path に personal URL が現れる場合や、`<slug>.github.io` という segment があるだけでも赤になる fail-closed
の設計であり、nested URL は次の `?`・`#`・`=`・`&` query/fragment field 境界までを照合する。該当テキストを
修正するか registry allowlist へ追加して対処する。
`--account-slug` は前後の空白を除いた後、GitHub slug 形の
`^[A-Za-z0-9](?:[A-Za-z0-9-]{0,37})$` に一致しなければ設定不備として赤になる。
`@` の直前が英数字または `_` の word character でない場合は bare
`@host/...` として URL 検査の対象になる。

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
3. CI に通常検査を配線する。レジストリを持つリポは `--registry` を渡す。
   ```bash
   python3 -B tools/check_publication_gate.py \
     --root . \
     --account-slug "$PUBLICATION_ACCOUNT_SLUG" \
     --registry path/to/modules.json
   ```
   レジストリを持たないリポは、代わりに opt-out を明示する。
   ```bash
   python3 -B tools/check_publication_gate.py \
     --root . \
     --account-slug "$PUBLICATION_ACCOUNT_SLUG" \
     --no-registry
   ```
   `--registry` と `--no-registry` の両方を省略すると赤になる。また、
   `<root>/registry/modules.json` が存在するリポで `--no-registry` を渡しても赤になる。機微パターンを
   CI secret から注入する場合は `--denylist "$PUBLICATION_DENYLIST_PATH"` も渡す。
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
- 1行目の先頭に UTF-8 BOM があれば、BOM だけを除いてからコメント/ルールとして解釈する。
- 最初のタブで `NAME` と `REGEX` に分ける。追加の literal tab は列ずれとして拒否するため、
  正規表現で tab を表したいときは `\t` と書く。
- `NAME` は空にできず、space/tab/newline などの whitespace を一切含められない。
  `REGEX` も空にできず、先頭・末尾に whitespace を置けない。whitespace 自体を照合したい場合は
  `\s` または `[ ]` を明示する。`REGEX` は Python `re` の構文で、
  `re.IGNORECASE` でコンパイル・照合する。
- タブの無い行、不正な `NAME`、空または前後 whitespace 付きの `REGEX`、追加の literal tab、
  コンパイルできない正規表現、UTF-8 として読めないファイルは
  **malformed = 赤**。
- `.publication-denylist` 自体の不在と、コメント/空行を除く有効ルール0件はどちらも**赤**。

個人用 URL 検査は e-mail 形（`local@host/...`）を意図的に URL とみなさない。したがって採用リポの
`.publication-denylist` は e-mail ルールを**必ず**含めること（sample には `email-address` ルールを同梱。
sample を使わず自前 denylist を書く場合も同等のルールを載せる）。

denylist は検出すべき禁止リテラルを必然的に含む。そのため checker は、スキャン対象から
既定の `<root>/.publication-denylist`、または `--denylist` で明示したファイルが root 内にある場合は
そのファイルを**パスで**自己除外する。この path-exclusion は、拡張子 allowlist を廃止して全 regular file を
読む現在の実装で load-bearing な安全条件である。過去のようにスクリプト内で禁止語を分割文字列にして
検出をかわすハックは不要。ポリシーと実装を分けたまま、自己検知だけを明示的に除外できる。

検査結果には `denylist rules loaded : N` を必ず表示する。構文上は有効でも決して一致しない正規表現の
意味的な妥当性は、trusted policy を書く作者の責任としてこの件数とレビューで確認する。

## denylist 自体の公開リスク

denylist を commit すると、そのパターンも公開物になる。導入先は次の3つから方針を選ぶ。

- **(a) 公開安全なパターン記法で書く**: sample の流儀で、パターン文字列自体が秘密を含まない形にする。
- **(b) 推奨（機微パターン）**: denylist を `.gitignore` に入れ、CI では secret から一時ファイルへ注入し、
  `--denylist PATH` でそのファイルを指定する。
- **(c) 公開を明示的に受け入れる**: パターンの公開リスクを評価し、commit する判断を記録する。

B9 移行では、各リポが (a)〜(c) のどれを採ったかをリポごとに選び、移行記録へ残す。

## 任意の `.publication-label-whitelist`

公開ラベルの既知の例外が必要なときだけ、リポルートに作成する。UTF-8、1行1例外で形式は次の通り。

```text
PATH<TAB>EXACT_LINE
```

`PATH` と、そのファイル内で許可する `EXACT_LINE` の完全一致だけを免除する。このファイルは
**言い訳だけを追加する** allowlist であり、新しい問題を検出するポリシーではない。したがって不在時は
fail-open（免除なしとして継続）でよい。denylist の不存を赤にするのとは非対称だが、意図的な設計である。
`--no-registry` を明示した場合、whitelist が不在または空なら whitelist-staleness を判定できないため
その検査は notice 付きで skip する。一方、1件以上の whitelist がある場合は staleness を検査できない
状態を許可せず、fail-closed で赤になる。

## CLI

| 引数 | 必須性 / 既定値 | 意味 |
|---|---|---|
| `--root PATH` | 任意、既定 `.` | 検査対象リポのルート。ポリシーファイルと、`--no-registry` 時の `README.md` のアンカー |
| `--account-slug SLUG` | 通常検査で必須、既定なし | 公開物に残してはいけない個人アカウントの slug。未指定は赤 |
| `--registry PATH` | `--no-registry` と二者択一 | 公開リポ台帳の JSON ファイル。相対パスは root 基準 |
| `--no-registry` | `--registry` と二者択一、既定 `false` | 公開台帳を持たないリポであることを明示し、台帳依存の4検査を notice 付きで skip |
| `--denylist PATH` | 任意、既定 `<root>/.publication-denylist` | 外部 denylist。相対パスは root 基準。root 内なら明示指定したファイルもスキャンから path-exclude |
| `--selftest` | 任意、既定 `false` | 内蔵 fixture で parser・検出・fail posture を検査して終了 |

## スキャン対象と Git の無い環境

Git worktree（root に `.git` entry がある場合）では、`git ls-files --cached --others --exclude-standard`
が列挙する全 path を publishable corpus とみなす。Git mode では下記ディレクトリ除外を適用せず、
commit 済みなら `node_modules/` 下も検査する。root に `.git` entry があるのに Git 列挙が失敗した場合は、
`rglob` へ黙って fallback せず `gate-error` で赤にする。

root に `.git` entry が無いアーカイブ展開後やコピー先では、検査自体を消さず `Path.rglob()` 相当で
ルート以下を再帰走査する。この `rglob-fallback` でだけ、次のディレクトリを対象外にする。

```text
.git
.omc
.omx
.venv
venv
node_modules
__pycache__
```

列挙された regular file は suffix やファイル名で選別せず、`.env.local`、`.cs`、`.csproj`、`.ipynb`、
`.txt`、`.csv`、`LICENSE`、`Dockerfile`、拡張子なしもすべて先に UTF-8 decode を試す。decode
できなかった場合だけ、明示した既知の binary suffix、exact filename `.DS_Store`、または先頭が
`bplist00` で suffix が `.plist` / `.bplist` の binary plist を binary としてスキャン対象外にする。それ以外は未知の
text-like file として
`source-read: ... is not valid UTF-8 text (fail-closed)` で赤にする。binary と判定したファイルは
`binary files skipped: N` に集計した直後へ
`  skipped (binary): <relative path>` と1ファイル1行で名前も表示する。Git mode の symlink は Git が
公開する readlink text を検査する。`rglob-fallback` は symlink を follow せず、
`symlinks skipped: N` に集計する。

binary suffix の例には `.png` と `.icns` が含まれる。`.plist` は binary set に入れず、UTF-8 XML plist は
通常どおり全文を検査し、UTF-16 XML plist は source-read として赤にする。binary plist は `.plist` / `.bplist`
の `bplist00` signature により skip する。鍵・証明書コンテナは意図的に binary set に入れない＝赤。

`BINARY_SUFFIXES` は stencil 上流の公開ポリシーであり、byte-identical copy を採用するリポが局所的に
調整する対象ではない。未知の suffix が非 UTF-8 として赤になった場合は、ファイルを UTF-8 へ変換する、
Git mode なら publishable corpus から untrack する、または suffix 追加の upstream PR を開く、のいずれかで
対処する。

summary は必ず `enumeration: git` または `enumeration: rglob-fallback` と、
`denylist rules loaded : N` を表示する。raw view の hit は raw text の行番号を使い、percent/HTML decode 後に
初めて見つかった hit は decoded text の行番号と `(decoded view)` marker を表示する。

`--selftest` の violating corpus、clean twin、sample denylist は checker 自体の string constants として
埋め込まれている。disk 上の `fixtures/` は人間向け資料であり selftest の依存ではないため、checker の
`.py` だけを別ディレクトリへコピーしても `--selftest` は完走する。

## 2026-09 改訂（#97 / #98）— 採用リポの再コピー差分

`2d2d4b3` の byte-identical copy を保持している採用リポは、この変更を含む handbook release
（この PR の merge 時に `v0.24.0` として切る）の checker を再コピーし、次の caller-visible な差分を取り込む。

- 既知の binary suffix または exact filename `.DS_Store` 以外のファイルが UTF-8 でなければ、
  `source-read: ... is not valid UTF-8 text (fail-closed)` で赤になる。既知の binary file は decode に
  失敗した場合だけ skip し、`binary files skipped:` の直下へ相対パスを列挙する。caller 側の
  `binary files skipped: 0` grep guard は追加の guard として引き続き有効である。
- `--registry` の省略は赤になる。レジストリを持たない caller は `--no-registry` を追加する。
  `registry/modules.json` が disk 上にある状態、または非空の `.publication-label-whitelist` がある状態での
  `--no-registry` も赤になる。
- bare `@github.com/<slug>/<repo>` と `@github.com/<slug>` も personal-url として検出する。
  `+@github.com/<slug>/<repo>` と `%@github.com/<slug>/<repo>` も検出する一方、`@` の直前が英数字または
  `_` の word character の e-mail 形は意図的に URL とみなさないため、採用リポの
  `.publication-denylist` は e-mail ルールを**必ず**含めること。sample には `email-address` ルールを同梱し、
  sample を使わず自前 denylist を書く場合も同等のルールを載せる。
- nested host を含む URL 候補の personal-url 検査は、上記「個人用 URL」節を参照する。
- 再コピー対象は、この変更を含む handbook release（この PR の merge 時に `v0.24.0` として切る）。

## family-os / organization `.github` からの移行

`family-os` と organization `.github` にある局所コピーは、この stencil の挙動を先に確定した後、
後続の **B9 lane** で置き換える。このテンプレート導入と既存リポの移行を同じ diff で混ぜない。

移行時の意図的な差分は4つ。

- 旧コピーの email masking のバグは修正済みで、新チェッカーの方が**厳格**。以前通っていた表記が
  新しく赤になった場合、検知退行ではなく bug fix の結果として対象テキストを直す。
- 外部 `.publication-denylist` は必須。先にファイルを配置・カスタマイズせず checker だけを切り替えると、
  ゲートは意図的に赤のままになる。
- 既知の binary suffix または exact filename `.DS_Store` 以外の decode failure は binary skip にせず赤にする。
  これは旧コピーの fail-closed な挙動と一致し、template 化の途中で生じた検査姿勢の緩みを戻す差分である。
- 通常実行では `--registry` か `--no-registry` の明示が必須。レジストリを持たない移行先は CI と
  ローカルの呼び出しへ `--no-registry` を追加する。

移行 PR では `--selftest`、対象リポの `make test`、通常 CLI の実行結果、CI status check の
required 登録を証拠として残す。
