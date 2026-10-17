# 村田晴香 / MURATA Haruka — Portfolio

添付仕様書v1.12と `logo_kame01.zip` のロゴから作成した、日本語・英語の静的サイトです。完成したHTMLを同梱しています。表示・公開にNode.js、npm、Python、ビルド作業は不要です。

## 開き方

ZIPを展開し、`pf/index.html` をブラウザーで開いてください。英語版は `pf/en/index.html` です。CSS、画像、言語リンクは相対パスなので、ファイルとして開けます。

通常のHTTP配信をローカルで確認する場合は、`pf` 内で以下を実行します。

```sh
python3 -m http.server 8000
```

`http://localhost:8000/index.html` を開きます。Windowsでは必要に応じて `python3` を `py -3` に読み替えてください。

## 内容と軽量化

- 日本語・英語の本文とメタ情報をHTMLに事前出力。JavaScriptなしでも読めます。
- 亀はヘッダー・トップ・フッターの3か所。ファビコン・Apple touch icon・OGPも同じロゴです。
- 添付の高解像度透過PNGから輪郭を保持して余白を整理し、青に合わせてWeb用に縮小・最適化しました。
- ネットワークと基板模様は固定SVG。表示時のランダム生成やアニメーションはありません。
- JavaScriptはメニュー開閉と言語切り替え時のセクション位置の引き継ぎだけです。
- 外部ライブラリ、CDN、Webフォント、画像埋め込み動画、解析サービス、API通信は使いません。
- フッターにDesignEvoのクレジットと、標準HTMLで開閉する素材一覧を配置しています。
- ログイン、入力フォーム、データベースはありません。メールボタンは `mailto:` です。

画像の原寸5000pxファイルや添付ZIPは配布フォルダに重複して入れていません。元のロゴダウンロードデータは別途保管してください。

## 文章・基本情報の更新

編集元は `data/site.json` です。HTMLだけを直接編集すると再生成で上書きされます。

- `site`：氏名・肩書き・メール・公開URL・更新日・共同研究者。
- `ja` / `en`：各言語の文章・スキル・資格・素材一覧。
- 更新日は `YYYY-MM-DD` で指定し、画面では `Updated dd-MMM-yyyy` と表示します。閲覧日ではなく、内容を更新した日付を指定してください。

編集後、Python 3.9以降で実行します。生成・静的検証には標準ライブラリだけを使います。

```sh
python3 scripts/build.py
python3 scripts/check.py
```

生成された `index.html`、`en/index.html`、`sitemap.xml` も一緒に保存・コミットします。CSSは `assets/site.css`、メニュー動作は `assets/site.js`、HTML構造は `scripts/build.py` で管理します。

## GitHub Pagesへ反映

公開先の初期値：

- 日本語：https://tam829.github.io/pf/index.html
- 英語：https://tam829.github.io/pf/en/index.html

既存リポジトリをバックアップしたうえで、ZIP内の `pf` の**中身**をリポジトリのルートへコピーしてください。`pf/pf` の二重構造にしないでください。既存の `.git` は維持します。本ZIPはGit履歴やリモート設定を含みません。

```sh
python3 scripts/build.py --check
python3 scripts/check.py
node --check assets/site.js
node scripts/test_interactions.cjs
git status
git diff --check
git add index.html en assets favicon.ico .nojekyll sitemap.xml data scripts docs README.md .gitignore
git diff --cached --stat
git commit -m "Update bilingual portfolio website"
git push
```

Node.jsはJavaScriptの検証時のみ必要です。GitHub Pagesの公開元は使用するブランチの `/(root)` に設定します。既に別の公開ワークフローがある場合は既存設定に合わせてください。この納品では公開・pushは実行していません。

公開先を変更する場合は、`data/site.json` の `site.base_url` を末尾 `/` 付きのHTTPS URLに変更して再生成してください。canonical、hreflang、OGP URL、sitemapが更新されます。

## 検証・仕様・素材

- `docs/site-spec.md`：今回添付された仕様書v1.12をそのまま同梱。過去の「仕様書更新のみ」という作業範囲の記載は、今回の実装依頼で置き換えられています。
- `docs/VERIFICATION.md`：実施済み検証と、ブラウザーで追加確認する項目。
- `docs/THIRD_PARTY_NOTICES.md`：使用素材と提供元。

日英HTML・ローカル参照・メタ情報・文章・SVG接続・コントラストの静的検証と、メニュー操作ロジックのテストを通過しています。**実ブラウザーでの画面表示・実操作はこの作成環境では未検証です。** 公開前に日英ページのスマートフォン表示、拡大表示、キーボード操作を確認してください。

## ファイル構成

```text
pf/
  index.html
  en/index.html
  assets/
    site.css
    site.js
    turtle.png
    network.svg
    circuits.svg
    favicon.png
    apple-touch-icon.png
    og-image.png
  favicon.ico
  sitemap.xml
  .nojekyll
  .gitignore
  data/site.json
  scripts/build.py
  scripts/check.py
  scripts/test_interactions.cjs
  docs/site-spec.md
  docs/VERIFICATION.md
  docs/THIRD_PARTY_NOTICES.md
  README.md
```
