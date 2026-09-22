 # AliExpress Listing Generator — Codex Skill

 一个 [Codex](https://codex.openai.com/) Skill，输入 1688 或国内电商商品链接，自动提取产品数据、挖掘卖点、生成速卖通上架文案（普通版 + GEO版），输出自包含 HTML 报告。

 A [Codex](https://codex.openai.com/) skill that takes a 1688 or domestic e-commerce product link, extracts product data, mines selling points, and generates AliExpress listing copy (standard + GEO-enhanced), outputting a self-contained HTML report.

 ---

 ## 功能 / Features

 - **产品数据提取** — 从 1688 页面抓取标题、图片、属性、价格、SKU、商家信息
 - **关键词挖掘与评分** — 3维度评分（频次/相关性/机会度），分层放置到标题/规格/描述/后端词
 - **5层卖点挖掘** — 属性清单 → Feature → FABE 优势与利益 → 转化驱动力 → 跨境文案
 - **速卖通普通版文案** — 标题、Item Specifics、SKU矩阵、描述HTML、搜索关键词、图片建议
 - **GEO优化版文案** — FAQ问答、场景化语义、JSON-LD结构化数据、长尾自然语言、多语言覆盖、竞品对比
 - **自包含HTML报告** — 内联CSS，无外部依赖，中英文双语

 ---

 ## 安装 / Installation

 将本目录复制到 Codex skills 目录：

 ```bash
 cp -r ae-listing-generator ~/.codex/skills/
 ```

 或从 GitHub 安装：

 ```bash
 npx skills@latest add <your-github-username>/ae-listing-generator
 ```

 ---

 ## 使用 / Usage

 在 Codex 对话中提供产品链接即可触发：

 ```
 帮我从这个链接生成速卖通上架文案：
 https://detail.1688.com/offer/1011475783495.html
 ```

 Skill 会自动执行 7 步工作流，最终生成一个 HTML 报告文件。

 The skill automatically executes a 7-step workflow and generates an HTML report file.

 ---

 ## 工作流 / Workflow

 | 步骤 Step | 说明 Description |
------|------|
 | 1. 提取产品数据 Extract product data | 运行 `fetch_product_data.py` 抓取 1688 页面，解析嵌入 JSON |
 | 2. 关键词挖掘与评分 Keyword scoring | 从标题/属性/卖点提取候选词，按3维度评分分层 |
 | 3. 卖点挖掘 (5层模型) Selling point mining (5-layer) | 属性 → FABE → 转化驱动力 → Buyer Reason Card → 跨境文案 |
 | 4. 速卖通普通版文案 Standard listing copy | 标题(≤128字符) / Item Specifics(≥8字段) / SKU / 描述 / 搜索关键词 |
 | 5. GEO版文案 GEO-enhanced copy | FAQ / 场景化语义 / JSON-LD / 长尾自然语言 / 多语言 / 竞品对比 |
 | 6. 渲染HTML报告 Render HTML report | 运行 `render_report.py` 生成自包含 HTML |
 | 7. Self-review | 校验来源可追溯、字符数、字段完整性、英文地道性 |

 ---

 ## 目录结构 / Project Structure

 ```
 ae-listing-generator/
 ├── SKILL.md                          # Skill 主指令文件
 ├── agents/
 │   └── openai.yaml                   # Codex agent 配置
 ├── assets/
 │   └── report_template.html          # HTML报告模板
 ├── references/
 │   ├── aliexpress-listing-fields.md  # 速卖通后台上架字段清单
 │   ├── geo-strategy.md               # GEO七大策略详解
 │   ├── keyword-scoring.md            # 关键词3维度评分方法
 │   └── visual-analysis.md            # 程序化视觉分析方法
 └── scripts/
     ├── fetch_product_data.py         # 1688数据抓取脚本
     └── render_report.py              # HTML报告渲染脚本
 ```

 ---

 ## GEO 策略 / GEO Strategy

 GEO (Generative Engine Optimization) 让 AI 搜索引擎（ChatGPT、Perplexity、Google AI Overviews）能找到并推荐你的产品。

 GEO (Generative Engine Optimization) makes AI search engines (ChatGPT, Perplexity, Google AI Overviews) able to find and recommend your product.

 1. **JSON-LD 结构化数据** — Schema.org Product 标记嵌入描述 HTML
 2. **FAQ 问答块** — AI 搜索引擎偏好问答内容，直接提取为 featured answer
 3. **场景化语义** — 用 when/where/why 句式替代纯规格描述
 4. **长尾自然语言** — 覆盖 AI 搜索用户的完整句子提问
 5. **竞品对比差异化** — 明确对比文案，应对 "X vs Y" 搜索
 6. **可量化证据** — 所有卖点附数字，避免模糊营销词
 7. **多语言自然语言** — 英/德/法/西语自然语言短语

 ---

 ## 约束 / Constraints

 - 不调用付费 API / No paid API calls
 - 不把批发价当1件零售价 / No wholesale price as retail price
 - 不编造认证/销量/测试数据 / No fabricated certifications/sales/test data
 - 不在标题放竞品品牌名 / No competitor brand names in title
 - 标题 ≤ 128字符（精确计算） / Title ≤ 128 chars (precisely calculated)
 - 英文为主输出，中文对照 / English-first output with Chinese reference
 - HTML 自包含（内联CSS，无外部依赖） / Self-contained HTML (inline CSS, no external deps)

 ---

 ## 许可证 / License

 MIT
