> **机器翻译。**日文原文（[architecture-parallel-map.md](../../../templates/architecture-parallel-map.md)）是正本 — 本页与原文不一致时，以日文为准。

# 并行安全地图模板（添加到各仓库 ARCHITECTURE.md 中的章节）

```markdown
## 並行安全マップ (Parallel Safety Map)

> 並行GO判定（family-dev-handbook L2-4）の判断材料。
> モジュール境界を動かす PR を merge したら、このマップも同じ PR で更新する。

### モジュール境界

| モジュール | パス | 主な責務 | 備考 |
|---|---|---|---|
| <!-- 例: iOS app --> | `ios-app/` | UI・音声入出力 | |
| <!-- 例: gateway --> | `gateway/` | セッション管理・LLM 中継 | |

**境界をまたがない Issue 同士は原則並行可**（ファイル集合の交差チェックは必須）。

### ホットスポット（並行注意ファイル）

| ファイル | 行数目安 | 同居している責務 | 分割 Issue |
|---|---|---|---|
| <!-- 例: MainView.swift --> | 2,500+ | UI + ジェスチャー + エンジン呼び出し | #NNN |

**ホットスポットを触る Issue は、他の同モジュール Issue と並行しない。**
分割 Issue（並行可能性への投資）を優先的に消化する。

### 広域 Issue の履歴

| Issue | 内容 | 実行時期 | 単独実行したか |
|---|---|---|---|
| <!-- 例: #NNN --> | UI 全面刷新 | | |
```
