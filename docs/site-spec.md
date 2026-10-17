# 村田晴香 自己紹介サイト 更新仕様

- 仕様作成日：2026-10-17（JST）
- バージョン：1.12
- 状態：最新の合意を整理した実装用仕様。掲載本文と配置方針を本書に統一し、実ファイルの準備・公開前の確認は第10節にまとめる。
- 対象：既存の自己紹介サイトを更新し、日本語・英語の画面を用意する。
- 現行URL：https://tam829.github.io/pf/index.html
- 今回は仕様書の更新のみを行う。既存ソースとZIPの更新、サイト公開・Gitへのpushは今回の対象外とする。

## 1. 目的

名刺から訪れた人に、村田晴香の現在の仕事、研究活動、これまでの経験、制作活動、連絡先が伝わる自己紹介サイトにする。

すっきりしたプロフェッショナルな見た目を基調とし、名刺と共通の亀と新しく制作するネットワーク模様で個性を加える。装飾の多い実験ノート風やコラージュ風にはしない。

## 2. 基本情報・統一表記

| 項目 | 表記・仕様 |
| --- | --- |
| 日本語氏名 | 村田晴香 |
| 英字氏名 | MURATA Haruka |
| 肩書き | 独立研究者 |
| 英語肩書き | Independent Researcher |
| メール | mttk.mrt238@gmail.com |
| 現在の仕事 | SES企業に所属し、銀行の内部利用システム開発に従事 |
| 共同研究 | 一橋大学 本武陽一准教授と共同研究 |
| 共通の言葉 | HELLO NEW WORLD |

- 旧姓・旧名義による表示は「村田晴香」「MURATA Haruka」に統一する。
- 氏名・メールの更新対象は、本文、ヘッダー、フッター、ページタイトル、メタ情報、画像内の文字、代替テキスト、リンク先など。
- メールリンクは `mailto:mttk.mrt238@gmail.com` とする。
- 所属企業名、銀行名、顧客名、非公開の案件名は掲載しない。
- SES企業での仕事と、独立研究者としての研究活動の両方を紹介する。

## 3. ページ構成

日本語・英語それぞれ、同じ構成の縦スクロール型1ページを用意する。

1. ヘッダー
2. トップ
3. プロフィール
4. 研究内容
5. これまでの経験
6. 制作・スキル
7. 連絡先
8. フッター（基板模様・亀・クレジット・使用素材一覧）

## 4. デザイン

### 4.1 全体

- 白を基調とし、ごく薄い青の背景を一部のセクションに使用する。
- 本文は濃いグレー、アクセントは名刺に合う青とする。
- 余白と細い区切り線で情報を整理する。
- 名前や一部の見出しに明朝体、本文とメニューに読みやすいゴシック体を使用する。
- 見出しに小さな番号と日英のラベルを添える。
- 大量のカード、写真、イラスト、手書き注釈、紙の質感は使用しない。
- 架空の成果グラフ、実績写真、アプリ画面は掲載しない。

### 4.2 亀

- DesignEvo由来の既存の亀を、各言語ページのヘッダー・トップ右下付近・フッターの3か所に配置する。
- ヘッダーでは氏名の横に小さく、トップではネットワーク模様の近くに、フッターでは中央に控えめに配置する。
- フッターの亀は控えめな大きさとし、DesignEvoのクレジットを近くに常時表示する。
- 亀とネットワークは別の素材として管理する。

### 4.3 ネットワーク・基板模様

- トップの右側に、サイト用に新しく制作したネットワーク模様を薄く配置する。既存素材や名刺の画像を切り抜き・反転して流用しない。
- 名刺のように整然とした点と線の雰囲気を参考に、線の方向と余白を整理する。細い直線を点の中心へつなぎ、線が途中で外れたり、先細りの太い三角形の面になったりしないようにする。
- 点と接続線を増やしすぎず、主となる流れと疎密を設計する。本文側を薄くして、氏名・コピー・研究へのリンクの可読性を確保する。
- 配置は固定のSVG素材とし、表示時にランダム生成しない。
- ページ最下部のフッターに、基板を連想させる回路模様を少量使用する。細い青の配線、水平・垂直・45度の折れ、小さな丸い端子で表現する。
- 回路模様は左右の端や下辺を中心に置き、中央の亀・クレジット・著作権表記の周囲には白い余白を残す。写真の基板、大きなチップ、発光表現、アニメーションは使用しない。
- 本文の可読性を優先し、背景模様を文字と強く重ねない。

### 4.4 配色・アクセシビリティ

- 今回はライトモードのみを実装する。OSのテーマ設定による配色の自動切り替えとダークモード切り替えUIは追加しない。
- 本文、見出し、リンク、更新日、ボタン文字を含む掲載文字は、背景とのコントラスト比を4.5:1以上とする。大きな見出しにも同じ基準を適用する。
- ボタン等の識別に必要な枠線・アイコンは、隣接色とのコントラスト比を3:1以上とする。意味を持たないネットワーク模様や区切り線は対象外とする。
- 言語の選択状態は色に加えて下線または太字でも示す。本文リンクは下線等で識別できるようにする。
- キーボード操作時のフォーカスを明示する。装飾用の亀や模様は重複して読み上げさせない。
- 本文を200%に拡大しても情報や操作を失わないようにする。
- 本節は個別の実装要件であり、チェック完了前にWCAG全体への適合を宣言しない。

### 4.5 ファビコン・OGP画像

- ファビコンとApple touch iconも共通の亀を使用する。小さい表示に合わせて余白とサイズを調整する。
- `favicon.ico` とPNG版を用意し、各言語のHTMLから同じ素材を参照する。
- SNS共有用のOGP画像を1200×630pxで1点作成する。白と青、共通の亀、薄いネットワーク模様を使う。
- OGP画像内の文字は `MURATA Haruka` と `Independent Researcher` とし、日英で共通利用する。
- 先生の所属、共同研究の表記、更新日、メールはOGP画像に埋め込まない。これらはサイト本文の編集可能なテキストで管理する。

## 5. ヘッダー・更新日・言語切り替え

### 5.1 ヘッダー

- 幅960px以上をPC表示、960px未満をコンパクト表示とする。
- PCは2段構成とし、上段左に亀と氏名、上段右に更新日と `日本語 / EN`、下段にセクションへのナビゲーションを配置する。
- ナビゲーション項目はプロフィール、研究内容、経験、制作・スキル、連絡先とする。
- ヘッダーは通常の文書フローに置き、画面上部には固定しない。

### 5.2 更新日

- 表示形式：`Updated dd-MMM-yyyy`。
- 2026年10月17日に内容を更新した場合の例：`Updated 17-Oct-2026`。
- 日は2桁、月は英語3文字（Jan、Feb、Mar、Apr、May、Jun、Jul、Aug、Sep、Oct、Nov、Dec）、年は4桁。
- 日本語・英語画面で同じ形式とする。
- 表示するのは内容の最終更新日。閲覧日時に応じて自動的に今日の日付にしない。
- 小さめの文字と控えめなグレーを使いつつ、十分に読める濃さを保つ。
- 更新日は編集可能なテキスト・データとして管理する。画像に埋め込まない。

### 5.3 言語切り替え・URL

| 言語 | URL | HTML言語属性 |
| --- | --- | --- |
| 日本語 | https://tam829.github.io/pf/index.html | `<html lang="ja">` |
| 英語 | https://tam829.github.io/pf/en/index.html | `<html lang="en">` |

- 日本語・英語の本文をそれぞれ静的HTMLとして出力する。JavaScriptを実行しなくても本文とメタ情報を取得できるようにする。
- 既存の日本語URLを維持する。`?lang=en` による切り替えは採用しない。
- `日本語 / EN` は、それぞれのURLへ移動する通常のリンクとする。
- 選択中の言語は青と下線または太字で明示し、`aria-current="page"` を設定する。
- セクションIDは日英で共通の `home`、`profile`、`research`、`experience`、`projects`、`contact` とする。
- セクション内で言語を切り替える場合、既知のハッシュがあれば対応先にも引き継ぐ。引き継ぎ処理が動かない場合も、通常の言語リンクで対応ページを開けるようにする。
- 言語はURLで決定し、ブラウザー設定による強制転送や保存済み言語による自動転送は行わない。言語の保持は遷移先URLで行う。
- メニュー、見出し、本文、ボタン、補助文、ページタイトル、代替テキストは対応言語で掲載する。
- 日本語と英語で意味を揃え、英語の文章量に合わせて改行と余白を調整する。

### 5.4 スマートフォン・コンパクト表示

- 上段左に亀と氏名、上段右にメニューボタンを配置する。
- 下段左に更新日、下段右に `日本語 / EN` を配置する。更新日と言語切り替えはメニュー内に隠さず、常時表示する。
- メニューボタンは44×44px以上の操作領域を設け、言語ごとに「メニューを開く／閉じる」「Open menu / Close menu」の名前を付ける。
- メニューは初期状態で閉じ、ボタン直下から本文の上に通常フローで展開する。モーダルや画面全体を覆う形式にはしない。
- 開閉ボタンに `aria-expanded` と `aria-controls` を付ける。ナビゲーションは通常の `nav` とリンクで構成し、アプリ用の `role="menu"` は使わない。
- 同じボタンで開閉できる。リンク選択時は閉じて該当セクションに移動する。Escapeで閉じた場合は開閉ボタンにフォーカスを戻す。
- キーボードのTabで開閉ボタンと展開中のリンクを操作できるようにする。閉じた内容にフォーカスが入らないようにする。
- JavaScriptが無効でもナビゲーションのリンクにアクセスできるようにする。
- 経験欄等の複数カラムは縦に並べる。スキルの値は折り返す。
- 320px幅以上で横スクロールを発生させず、メールや長い英語表記を収める。

## 6. 日本語の掲載内容

以下を日本語の採用本文とする。制作物や担当範囲を具体化する際には、事実に合う内容のみ追加する。

### 6.1 トップ

- 小さな言葉：HELLO NEW WORLD
- 肩書き：独立研究者
- 氏名：村田晴香
- 英字氏名：MURATA Haruka
- ひとこと：出会いをきっかけに、まだ知らない世界へ。

紹介文：

> 店舗運営・企画、アプリの品質保証を経て、現在は銀行の内部利用システム開発に従事。独立研究者として、AIを用いた研究にも取り組んでいます。

- リンク：研究内容を見る
- 名前を主役とし、肩書きは名前の上に小さく配置する。
- 最新の画面案では省略された「HELLO NEW WORLD」も、名刺との共通要素として併記する。

### 6.2 プロフィール / Profile

> 店舗運営・企画、アプリ・Webサービスの品質保証など、さまざまな現場を経験してきました。現在はSES企業に所属し、銀行の内部利用システム開発に従事しています。
>
> また、独立研究者として、インタビュー由来のペルソナ情報がLLMの回答に与える影響を研究しています。

### 6.3 研究内容 / Research

研究見出し：

> ペルソナ情報が、LLMの回答に与える影響

共同研究の表記：

> 一橋大学 本武陽一准教授と共同研究

概要：

> 科学者の経験や考え方をAIに取り入れ、科学的な問題解決に生かす研究を行っています。インタビューに基づく人物情報を与える場合、同程度の長さのランダムな文章を与える場合、人物情報を与えない場合の3条件を比較しています。論文中の誤った数式を見つける課題に繰り返し回答させ、人物情報がAIの回答傾向に与える影響を検証しています。

取り組みの表記：

> 実験プログラムの整備・回答生成・結果の集計と比較

- 状態表示：研究・検証中。
- 右側に `AI × Persona` を文字要素として配置する。
- 先生の所属・氏名・役職は独立した編集可能なテキストとし、画像に埋め込まない。
- 将来の所属変更は共同研究の一文を修正することで対応できるようにする。
- 所属と役職の表記は今回のユーザー指定を採用している。公開時点の記載に合わせて更新する。
- 現時点では研究成果を断定する文言、有意差の主張、具体的な実測グラフは追加しない。

### 6.4 これまでの経験 / Experience

#### 店舗運営・企画

> 売場構成、運営改善、スタッフ育成など。

#### 品質保証・テスト

> テスト仕様書作成、検証、不具合報告、開発者との連携など。

#### システム開発（現在）

> SES企業に所属し、銀行の内部利用システム開発に従事。

- PCでは3項目を並べ、スマートフォンでは縦に配置する。
- 現在の項目に小さな「現在」ラベルを付ける。
- 担当工程、使用技術、在籍開始日など、未確認の情報は追加しない。
- 詳細な学歴・職歴の年表は今回の基本構成に含めず、必要に応じて後で追加する。

### 6.5 制作・スキル / Projects & Skills

#### Pythonによるツール制作

> 作業の自動化やデータの処理・整理など、目的に応じたツールを制作しています。

#### 楽譜・動画などの個人制作

> 楽譜制作や、ゲーム実況動画の撮影・編集などの個人制作を行ってきました。

- リンク表示：ゲーム実況動画（YouTube）
- 「制作・スキル」の個人制作欄に、小さなテキストリンクを1件掲載する。
- リンク先（ユーザー指定）：https://www.youtube.com/@zougames7703
- 日本語の掲載リンク：[ゲーム実況動画（YouTube）](https://www.youtube.com/@zougames7703)。
- 大きなサムネイル、動画埋め込み、自動再生、独立した動画一覧セクションは設けない。
- 研究・開発の成果物とは区別し、趣味・個人制作の経験として紹介する。
- 現段階で研究資料やコードへの公開リンクを新たに設ける必要はない。公開可能な成果物ができた時点で追加を検討する。

#### スキル一覧

スキルは次のカテゴリ別一覧を1回だけ表示する。カテゴリ名と折り返し可能な値の組み合わせとし、同じ内容をタグの一覧や別表で繰り返さない。

| 分類 | 掲載内容 |
| --- | --- |
| 言語・データベース | Python / VB.NET / Oracle SQL |
| Web・業務ツール | HTML / CSS / Excel |
| 品質保証 | テスト仕様書作成 |
| OS・実行環境 | Windows / Linux / WSL |
| ローカルLLM | Ollama / Open WebUI |
| 開発環境・ツール | Docker / 仮想環境 / GitHub |
| AI活用 | 生成AI活用 |

- 本一覧は使用技術・経験の要約とする。全項目を同じ熟練度として示す星やパーセントは使用しない。
- ローカルLLMの説明文は環境構築の経験を説明する役割とし、一覧は技術を探す役割とする。説明文中に必要な技術名が登場することは許容する。
- 制作物の公開リンクはYouTubeのテキストリンク1件とする。動作確認を行い、未指定の制作時期は追加しない。

#### ローカルLLMの環境構築

> Windows上にWSLでLinux環境を用意し、Ollama・Open WebUI・Dockerを利用したローカルLLMの実行環境を構築しています。仮想環境やGitHubも利用しています。

使用技術の表示は前項のスキル一覧に統合し、この説明の下に重複する技術表やタグを追加しない。

ツールの接続構成、仮想環境の種類、モデル名、GPU設定、GitHubの利用範囲は未指定のため断定しない。GitHubをローカルLLMの実行基盤としては説明しない。モデル学習・ファインチューニング・本番運用まで経験があるとは記載しない。

#### 取得資格

- 基本情報技術者試験 合格

「制作・スキル」セクション内に、スキル一覧とは分けた小さな「取得資格」欄を設ける。取得年は未指定のため記載しない。Oracle SQL・VB.NETの追加だけを根拠として、現在の業務での使用や熟練度は断定しない。

### 6.6 連絡先 / Contact

- 独立研究者
- 村田晴香
- MURATA Haruka
- mttk.mrt238@gmail.com
- ボタン：メールを送る

### 6.7 フッター

- 既存の亀を1体のみ配置する。
- DesignEvoへのクレジットを常時表示する。
- 控えめな回路模様。
- 著作権表記：`© MURATA Haruka`。

## 7. 英語画面

### 7.1 共通ラベル

| 日本語 | 英語 |
| --- | --- |
| 独立研究者 | Independent Researcher |
| プロフィール | Profile |
| 研究内容 | Research |
| これまでの経験 | Experience |
| 制作・スキル | Projects & Skills |
| 連絡先 | Contact |
| 取得資格 | Qualifications |
| 出会いをきっかけに、まだ知らない世界へ。 | New encounters, new worlds to explore. |
| 研究内容を見る | Explore my research |
| 研究・検証中 | Research in progress |
| 現在 | Current |
| メールを送る | Get in touch |

### 7.2 英語の採用本文・表記規則

- 肩書きとして独立表示する場合は `Independent Researcher` とする。ヘッダー・トップ・連絡先・ページタイトル・OGPでも統一する。
- 文中の職業名は一般名詞として `independent researcher` とする。文頭は `As an independent researcher, ...` のように通常の文法に従う。これは表記揺れではなく、表示用途による使い分けとする。
- `MURATA Haruka`、`Yoh-ichi Mototake`、`Oracle SQL`、`VB.NET`、`Ollama`、`Open WebUI`、`Docker`、`GitHub` の表記を統一する。
- 以下を日本語版と意味を揃えた英語の採用本文とする。

#### Top

> With a background in store operations, planning, and app quality assurance, I now develop internal systems for a bank. Alongside my professional work, I conduct AI research as an independent researcher.

#### Profile

> My experience spans store operations and planning, as well as quality assurance for apps and web services. I currently work for an IT services company, developing internal systems for a bank.
>
> As an independent researcher, I also study how interview-derived persona information influences LLM responses.

#### Research

見出し：

> How interview-derived persona information influences LLM responses

共同研究表記は、ラベルと本文を分けて次のように表示する。

- ラベル：Joint Research
- 本文：Associate Professor Yoh-ichi Mototake
- 所属：Graduate School of Social Data Science, Hitotsubashi University

名前・役職と所属は同一の説明ブロックに置き、画面幅に応じて改行する。日本語版の共同研究の一文と意味を揃え、いずれも画像ではなくテキストで表示する。

ユーザー提供の先生のプロフィール画像に基づき、以下の表記を採用する。

| 項目 | 確認した表記 |
| --- | --- |
| 氏名 | Yoh-ichi Mototake |
| 役職 | Associate Professor |
| 研究科 | Graduate School of Social Data Science |
| 大学 | Hitotsubashi University |

氏名は `Yoh-ichi Mototake` とし、`Yoichi Mototake` に置き換えない。研究科まで含めた所属表記も編集可能なテキストとして管理する。画像にある学位表記 `Ph.D` と先生のメールアドレスは、共同研究者紹介に必要な項目ではないため追加しない。

概要：

> My research explores how scientists’ experiences and ways of thinking can be incorporated into AI to support scientific problem-solving. I compare three conditions: providing interview-based persona information, providing random text of a similar length, and providing no persona information. By repeatedly asking AI to identify incorrect equations in a research paper, I examine how persona information influences its response patterns.

取り組み：

> Experiment code development, response generation, and analysis of response distributions.

#### Experience

| 見出し | 説明 |
| --- | --- |
| Store Operations & Planning | Store layout, operational improvements, and staff training. |
| Quality Assurance & Testing | Test specification writing, testing, bug reporting, and collaboration with developers. |
| Systems Development — Current | Developing internal systems for a bank as an employee of an IT services company. |

SESは略語だけで掲載せず、海外の閲覧者に伝わる `IT services company` などの表現を使う。

#### Projects & Skills

| 見出し | 説明 |
| --- | --- |
| Python Tools | Creating tools for task automation, data processing, and organization. |
| Personal Creative Projects | Personal projects have included creating musical arrangements and recording and editing gameplay videos. |

個人制作欄のリンク表示：`Gameplay Videos (YouTube)`。リンク先は https://www.youtube.com/@zougames7703 とし、日本語版と同じURLを使う。掲載リンク：[Gameplay Videos (YouTube)](https://www.youtube.com/@zougames7703)。小さなテキストリンクを1件のみ掲載する。動画の埋め込みや大きなサムネイルは使用しない。

スキルは日本語版と同じカテゴリ構造で1回だけ表示する。

| Category | Skills |
| --- | --- |
| Languages & Databases | Python / VB.NET / Oracle SQL |
| Web & Productivity Tools | HTML / CSS / Excel |
| Quality Assurance | Test Specification Writing |
| Operating Systems & Runtime | Windows / Linux / WSL |
| Local LLMs | Ollama / Open WebUI |
| Development Tools | Docker / Virtual Environments / GitHub |
| AI Tools | Generative AI Tools |

#### Local LLM Setup

> I have set up a Linux environment on Windows using WSL and built a local LLM environment using Ollama, Open WebUI, and Docker. I also use virtual environments and GitHub.

使用技術の表示は上のカテゴリ別一覧に統合する。仮想環境の種類は未指定のため、venv・Conda等の具体名に置き換えない。

#### Qualifications

- Passed the Fundamental Information Technology Engineer Examination (FE).

日本語の「基本情報技術者試験 合格」に対応する。取得年は記載しない。

#### Contact

- Independent Researcher
- MURATA Haruka
- mttk.mrt238@gmail.com
- Get in touch

## 8. 情報の公開範囲

- 現在の会社名・銀行名・顧客名は記載しない。
- 過去の案件も「健康支援アプリ」「機器操作アプリ」など対象分野で説明する。
- 公開する具体性は、担当業務・役割・工夫・公開できる成果物を中心にする。
- 「赤字店舗」「会社初」などの内部事情や裏付けが必要な表現は避ける。
- 内部資料、非公開の画面、未公開データは使用しない。
- 氏名、肩書き、メール、指定された共同研究の情報は掲載する。

## 9. 編集・実装上の要件

- 所属、肩書き、共同研究者表記、更新日、日英本文は画像ではなく編集可能なテキストとする。
- 複数箇所にあるメール・氏名・肩書き・更新日は共通のデータを基に管理し、日英HTML間で不一致が起きないようにする。ビルド方法やテンプレート技術は指定しない。
- デザイン画像は見た目の参考。画像内の誤字や文字崩れを正式な掲載内容として採用しない。
- 本仕様の掲載文章を基に、実際のHTML等のテキストとして実装する。
- 亀は既存素材をヘッダー・トップ・フッターで使用し、ネットワークは新しく制作する。別の素材として管理する。
- ページタイトル：日本語 `村田晴香 | 独立研究者`、英語 `MURATA Haruka | Independent Researcher`。
- セクション移動、言語切り替え、メールリンクをPC・スマートフォンで利用できるようにする。
- テキストのコントラスト、キーボード操作、適切な見出し構造、画像の代替テキストに配慮する。
- 公開先は既存のGitHub Pagesとし、第5.3節のURLを維持する。フレームワークを使用する場合も最終出力は静的ファイルとする。本タスクは仕様更新のみであり、実装・デプロイは別の依頼で行う。

### 9.1 言語別メタ情報・SNS共有

- 各HTMLの先頭付近に `<meta charset="utf-8">` を指定し、ソースもUTF-8で保存する。文字化け対策は文字コードで行い、OGPや `lang` 属性の問題と混同しない。
- ページ全体の言語は第5.3節の `lang` 属性で示す。
- 各ページに自己参照のcanonicalを設定する。日本語と英語の両方に、`hreflang="ja"` と `hreflang="en"` の相互参照を設定する。`x-default` は日本語URLとする。
- `title`、`meta description`、`og:title`、`og:description`、`og:url`、`og:locale` を言語ごとにHTMLへ出力する。これらの生成をブラウザー側JavaScriptだけに依存させない。
- `og:type` は `website` とする。`og:locale` は日本語 `ja_JP`、英語 `en_US` とし、相手言語を `og:locale:alternate` に設定する。
- `og:url` は対応する言語のcanonical URLと同じ値とする。
- `og:image` は第4.5節の共通OGP画像の絶対URLとする。画像のサイズ、言語に合った `og:image:alt` も指定する。
- 日英ページの共有プレビューは、それぞれのURLを起点に確認する。SNS側のキャッシュがあるため、即時更新を保証する記載はしない。

| 項目 | 日本語 | 英語 |
| --- | --- | --- |
| title / og:title | 村田晴香 &#124; 独立研究者 | MURATA Haruka &#124; Independent Researcher |
| description / og:description | 独立研究者・村田晴香の自己紹介。AIを用いた共同研究、システム開発、品質保証、個人制作の取り組みを紹介します。 | Personal website of MURATA Haruka, an independent researcher. Explore my collaborative AI research, systems development, quality assurance, and personal projects. |

### 9.2 外部リンク

- YouTubeリンクは `target="_blank" rel="noopener noreferrer"` を設定し、新しいタブで開く。
- 視覚的な外部リンク表示と、対応言語の「新しいタブで開きます / Opens in a new tab」という補足を付ける。
- 日英切り替えとページ内移動は同じタブで行う。メールリンクに外部サイト向けの属性を機械的に付けない。

## 10. 実装前の残確認事項

1. 新しいネットワークとフッターの基板模様の最終素材を準備し、PC・スマートフォンでの見え方を確認する。
2. ファビコンとOGP画像の実ファイルの作成・書き出し。使用方針は第4.5節で確定済み。
3. 公開時点での先生の所属・役職と、実際の内容の最終更新日。

URL方式、モバイルでの更新日・言語切り替えの位置、メニュー動作、スキル表示形式、外部リンク属性は本仕様で確定しており、残確認事項には含めない。

## 11. 参照資料

- `pf.zip`：既存サイトのHTML・CSS・画像等。
- `261014934418_01L.pdf`：名刺の印刷確認用PDF。白と青の配色や全体の雰囲気のみ参照する。既存の亀は共通素材として使用し、ネットワーク画像は転用しない。
- 2026-10-17の会話で作成した最新の画面イメージ：肩書き・現在の業務追加後の白と青の画面案。更新日と言語切り替えは画像生成後に追加合意した仕様であり、同画像にはまだ未反映。

## 12. 改訂履歴

- 1.0：2026-10-17。構成・日英対応・更新日を含む初版を作成。
- 1.1：2026-10-17。ユーザー提供の先生のプロフィール画像に基づき、氏名を `Yoh-ichi Mototake` に修正。英語の所属に `Graduate School of Social Data Science` を追加し、役職と大学名を確認。該当項目の未確認扱いを解除。
- 1.2：2026-10-17。スキルにOracle SQL・VB.NETを追加。取得資格に基本情報技術者試験の合格を追加し、日本語・英語の掲載内容に反映。
- 1.3：2026-10-17。Linux環境でのローカルLLM実行環境の構築を、日英のスキル・取り組み紹介に追加。
- 1.4：2026-10-17。Windows上でWSLを使ったLinux環境構築と、Ollama・Open WebUI・Docker・仮想環境・GitHubの利用を日英に追記。
- 1.5：2026-10-17。個人制作欄にゲーム実況動画（YouTube）の小さなテキストリンクを1件掲載する方針を日英に追加。撮影・編集の経験を紹介し、リンク先URLを残確認事項として明記。
- 1.6：2026-10-17。ユーザー指定のYouTubeチャンネルURL `https://www.youtube.com/@zougames7703` を日英共通のリンク先として設定。URLの未指定扱いを解除。
- 1.7：2026-10-17。レビューを反映し、断定的な仕様表現、英語の大小文字規則、共同研究ラベル、言語別URL・メタ情報、モバイルナビゲーション、コントラスト、スキル表示、資格表記、ファビコン・OGP・外部リンクを整理・具体化。

- 1.8：2026-10-17。承認済みコピー・研究概要と、簡潔な使用素材一覧を仕様化。
- 1.9：2026-10-17。亀とネットワークを新規制作に変更。既存ロゴ・名刺からの素材流用を取りやめ、新素材確定後にクレジットを決定する。

- 1.10：2026-10-17。既存の亀をフッター1体のみ残し、DesignEvoクレジットを維持。亀の作り直しは名刺の次回改版時に延期。ネットワークは新規制作を継続。
- 1.11：2026-10-17。キャッチコピー、詳細な研究概要、固定SVGのネットワーク、フッターの基板模様、簡潔なクレジットを統合。試作ロゴは不採用とし、亀のフッター1体のみという配置は維持。改訂履歴を集約。

- 1.12：2026-10-17。亀をヘッダー・トップ・フッターの3か所に復活し、関連アイコン・OGPも亀で統一。購入プラン・購入確認の記載を削除。

## 13. 実装完了時の確認項目

- [ ] 日英とも氏名・肩書き・メール・共同研究者表記が本仕様と一致する。
- [ ] 更新日は実際の内容の最終更新日で、`dd-MMM-yyyy` の形式になっている。
- [ ] 既存の日本語URLと英語URLを直接開ける。
- [ ] 言語切り替え、セクション移動、メール、YouTubeのリンクが動作する。
- [ ] 言語別HTML、UTF-8、canonical、hreflang、OGPが初期HTMLに出力されている。
- [ ] 日英それぞれのURLでSNS共有用のタイトル・説明・画像を確認する。
- [ ] スキルはカテゴリ別に1回表示され、取得資格は独立した小さな欄になっている。
- [ ] 320px・375px・768px・960px・1440px幅で、日英とも横スクロールや重なりがない。
- [ ] 200%拡大、キーボード操作、メニュー開閉、Escape、フォーカス、読み上げ用名称を確認する。
- [ ] 本文・補助文・更新日・ボタン文字のコントラスト比が4.5:1以上である。
- [ ] 操作部品の識別に必要な枠線・アイコンのコントラスト比が3:1以上である。
- [ ] 亀が各言語ページのヘッダー・トップ・フッターの3か所に配置され、ファビコン・Apple touch icon・OGPも共通の亀を使用している。DesignEvoクレジットが表示され、ネットワークは新素材に差し替わっている。
- [ ] 未確認の技術経験、取得年、研究成果、顧客名、仮のURLを追加していない。

## 14. 技術要件の参照先

- [W3C: Contrast (Minimum)](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html)
- [W3C: Non-text Contrast](https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html)
- [W3C: Disclosure Navigation Menu](https://www.w3.org/WAI/ARIA/apg/patterns/disclosure/examples/disclosure-navigation/)
- [Google Search Central: Localized versions](https://developers.google.com/search/docs/specialty/international/localized-versions)
- [MDN: rel=noopener](https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Attributes/rel/noopener)
- [The Open Graph protocol](https://ogp.me/)

## 15. 使用素材・ライセンス

- 日英両ページに「使用素材・ライセンス / Credits & Licenses」を設ける。HTMLのdetails/summaryで開閉し、JavaScriptを必須としない。
- 公開画面は、実際に使用する素材名・提供元・必要なリンクのみを簡潔に表示する。未確認事項、加工の詳細、規約の解説は掲載しない。
- 亀の提供元はDesignEvoとし、提供元と利用条件へのリンクを記載する。公開画面には購入プラン、価格、購入状況は記載しない。新しいネットワークの表記は制作後に決定する。
- DesignEvoのクレジットはフッターの亀の近くに常時表示する。文言は `Logo created with DesignEvo` とし、`https://www.designevo.com/` にリンクする。
- システムフォントや開発環境の説明は公開ライセンス欄には掲載しない。
- 本文・サイトの著作権表記と、第三者提供の亀のクレジットは区別する。亀の独占権や著作権を取得したとする表示は行わない。

公開表示例：

- 常時表示：`Logo created with DesignEvo`（DesignEvoへのリンク）。
- 日本語の使用素材一覧：`亀のロゴ：DesignEvo / 利用条件`。
- 英語の使用素材一覧：`Turtle logo: DesignEvo / Terms of use`。
- 提供元リンク：`https://www.designevo.com/`。利用条件リンク：`https://www.designevo.com/terms.html`。

## 16. 今回の更新範囲

- 本更新の納品対象は仕様書。新しい画像の制作とサイトソースへの反映は次の作業とする。公開・Gitへのpushは行わない。
- 承認済みのキャッチコピーと研究概要を反映する。
- 既存の亀をヘッダー・トップ・フッターの3か所へ戻し、ファビコン・Apple touch icon・OGPでも使用する。ネットワークは新素材へ差し替える。
- 印刷済み名刺のデータは今回変更しない。

## 17. 今回までの変更点のまとめ

| 対象 | 最終方針 |
| --- | --- |
| キャッチコピー | 出会いをきっかけに、まだ知らない世界へ。 |
| 英語コピー | New encounters, new worlds to explore. |
| トップのネットワーク | 整然とした点と細い直線の固定SVGへ変更。名刺の雰囲気を参考に新規制作する。 |
| ページ下部 | 控えめな基板・回路模様を配置。 |
| 研究概要 | 科学者の経験・考え方をAIに取り入れる目的と、人物情報・同程度の長さのランダム文・情報なしの3条件、論文中の誤った数式を探す反復課題を説明する。第6.3節と第7.2節の採用本文を使用。 |
| 亀の素材 | 既存の文字なしロゴを継続。生成した試作ロゴは使用しない。 |
| 亀の配置 | 各言語ページのヘッダー・トップ・フッターの3か所に復活。ファビコン・Apple touch icon・OGPも亀で統一。 |
| 使用素材・ライセンス | 日英で簡潔な一覧を設け、DesignEvoのクレジットを常時表示。未確認事項や詳細な説明は公開しない。 |
| 既に確定した内容 | 氏名・メール統一、独立研究者の肩書き、SES企業での銀行システム開発、共同研究者のテキスト表記、日英対応・更新日、スキル・資格・ローカルLLM環境構築、YouTubeリンクは維持。 |

本表は変更点の要約とし、実装時には各節の具体的な仕様と採用本文を優先する。
