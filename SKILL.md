---
name: ae-listing-generator
description: "Generate AliExpress listing content from a 1688 or domestic e-commerce product link. Supports multi-market targeting (US/EU/Russia/Mexico/Korea/etc.) with localized language output. Produces a self-contained HTML report with: (1) target market consumer analysis, (2) product selling points with FABE analysis, (3) AliExpress backend listing copy (regular version: title, item specifics, description, SKU, keywords), (4) GEO-enhanced listing copy (with AI search optimization: JSON-LD, FAQ, situational language, natural language keywords). Each content block includes a one-click copy button for foreign-language content. Use when user provides a product link and wants AliExpress-ready listing content for cross-border selling."
---

# AliExpress Listing Generator

给一个 1688 链接或其他国内电商链接，提取产品数据，分析目标市场消费者，挖掘卖点，生成速卖通上架文案（普通版 + GEO版），输出自包含 HTML 报告。支持多目标市场和多语言输出。

## When to Use

- 用户提供 1688 / 淘宝 / 拼多多 / 京东 等国内电商产品链接
- 用户要生成速卖通上架文案
- 用户要做 GEO/AEO 优化版本的上架文案
- 用户想从 1688 货源直接生成跨境 listing
- 用户指定目标市场和语言（如俄罗斯/俄语、墨西哥/英语、韩国/韩语）

## Input Parameters

| 参数 | 默认值 | 说明 |
|------|--------|------|
| 目标市场 Target Market | 北美 (North America) | 用户可指定：俄罗斯、墨西哥、韩国、欧洲、东南亚等 |
| 输出语言 Output Language | 英语 (English) | 用户可指定：俄语、韩语、西班牙语、法语、德语等 |
| 1688 链接 | 必填 | 国内电商商品链接 |

用户未指定时默认：目标市场=北美，语言=英语。中文翻译始终提供。

## Workflow

```
Task Progress:
- [ ] 1. 识别输入并提取产品数据
- [ ] 2. 目标市场消费者分析
- [ ] 3. 关键词挖掘与评分
- [ ] 4. 卖点挖掘 (5层模型)
- [ ] 5. 生成速卖通普通版上架文案
- [ ] 6. 生成GEO版上架文案
- [ ] 7. 渲染HTML报告
- [ ] 8. Self-review
```

### 1. 提取产品数据

运行 `scripts/fetch_product_data.py "<url>"` 抓取 1688 页面数据。脚本提取标题、图片、属性、价格、SKU、商家信息。

如果脚本报错或返回 insufficient_data（1688 页面 JS 渲染导致），用以下方式补抽：
- 用 curl 绕过代理抓取页面 HTML，从中用 Python 正则提取嵌入的 JSON 数据
- 用 SunBrowser CDP（如可用）直接执行 JS 提取 DOM 内容
- 从页面 HTML 中提取 `decisionCpv`、`normalCpv`、`skuProps`、`skuInfoMap` 等 JSON 块

对主图做程序化视觉分析（色彩分布、纹理方差、边缘密度），标为 `image-analysis` 来源。方法见 [references/visual-analysis.md](references/visual-analysis.md)。

价格纪律：
- 有1件价标1件价，批发阶梯价标"≥N件"
- 缺1件价标 `unknown`，禁止用批发价冒充
- CNY 和外币分开标

### 2. 目标市场消费者分析

**默认（未指定目标市场）：** 分析北美消费者群体特征。

**用户指定目标市场时：** 先分析该市场的适合该产品的消费者群体特征，包括：

| 分析维度 | 说明 | 示例 |
|----------|------|------|
| 目标人群画像 | 年龄/性别/职业/收入/生活方式 | 俄罗斯：25-45岁女性，重视家庭装饰，价格敏感 |
| 购买动机 | 该市场消费者为什么买这类产品 | 墨西哥：新居入伙送礼需求，偏好实用性 |
| 文化偏好 | 颜色/设计/尺寸偏好 | 韩国：偏好极简白色系，小尺寸公寓友好 |
| 搜索习惯 | 该市场消费者怎么搜索产品 | 俄罗斯：Yandex搜索，偏好俄语关键词 |
| 竞品环境 | 该市场同类产品定价/卖点/差异化 | 俄罗斯Ozon/Wildberries上的竞品分析 |
| 爆品潜力 | 该产品在该市场的爆品特质评估 | 是否有文化契合点/节日需求/社交媒体传播性 |

每个分析维度输出外文+中文对照。输出 Consumer Insight Card，指导后续卖点挖掘和文案生成，确保内容具有爆品高潜力特质。

### 3. 关键词挖掘与评分

从产品标题、属性、1688页面卖点短句中提取候选关键词。按3维度评分：

| 维度 | 评分标准 |
|------|----------|
| Frequency 频次 | 核心品类词=3 / 特征词=2 / 边缘词=1 |
| Relevance 相关性 | 直接描述产品=3 / 间接相关=2 / 弱相关=1 |
| Opportunity 机会度 | 差异化词=3 / 常用词=2 / 普遍词=1 |

分层放置：
- Primary (7-9分) -> 标题
- Secondary (4-6分) -> Item Specifics / Bullets
- Tertiary (2-3分) -> 描述
- Backend (1分) -> 搜索关键词

关键词用输出语言生成（默认英语），同时提供中文翻译对照。详细方法见 [references/keyword-scoring.md](references/keyword-scoring.md)。

### 4. 卖点挖掘 (5层模型)

**Layer 1 属性清单** — 列出全部属性，标来源（1688-page / image-analysis / inferred）

**Layer 2 Feature (FABE-F)** — 中文属性译成输出语言，分类 physical/functional/design/experience

**Layer 3 Advantage + Benefit (FABE-AB)** — 对每条feature写：
- Advantage: 比普通方案好在哪
- Benefit: 买家得到什么结果（先结果后规格）
- Evidence: 可追溯数字/材质/结构，没有就留空

**Layer 4 转化驱动力** — 基于目标市场消费者分析，选1个主驱动：
- Visual-Driven 视觉驱动: 靠外观/质感/礼品感成交
- Pain-Driven 痛点驱动: 靠解决反复问题成交
- Emotion-Value-Driven 情感价值驱动: 靠身份/关怀/新奇成交

写 Buyer Reason Card：Target Buyer / Purchase Trigger / Belief Shift / Primary Reason / Proof

**Layer 5 跨境文案** — 按主驱动排序的外语卖点 + 中文对照

### 5. 生成速卖通普通版上架文案

生成速卖通后台上架需要的全部字段。完整字段清单见 [references/aliexpress-listing-fields.md](references/aliexpress-listing-fields.md)。

**输出语言：** 用户指定语言（默认英语）。中文翻译始终提供。

核心字段：

**标题 (<=128字符)**
- 公式: [核心品类词] + [材质词] + [功能/场景词x2-3] + [差异化记忆点] + [规格数字] + [归类大词]
- 精确计算字符数，留余量
- 无品牌名（除非自有品牌已注册），无促销词
- 必须提供中文翻译对照

**Item Specifics (至少8个字段)**
- Material / Origin / High-concerned chemical / Additional Features / Function / Feature / Type / Installation Method
- 报告中分左右两栏显示：左栏=输出语言内容，右栏=中文翻译，便于一键复制外文内容

**SKU 矩阵**
- 2色 x 3规格 = 6个SKU（参考竞品常见做法）
- 每个SKU标注价格、库存、SKU图片

**描述 (HTML)**
- 速卖通AI Overview会从标题+Item Specifics自动生成描述
- 在描述中补充AI不会自动生成的内容：安装步骤、使用场景、包装内容
- 报告中先输出外语版本（合理分段），再输出中文版本（对应分段）
- 每段之间用分隔线区分

**搜索关键词 (Backend)**
- 用输出语言，空格分隔，无重复，<=250 bytes

**图片建议**
- 主图: 白底800x800px
- 副图: 5-6张，含场景图、细节图、尺寸图

### 6. 生成GEO版上架文案

在普通版基础上增加 GEO (Generative Engine Optimization) 内容，让AI搜索引擎能找到并推荐产品。详细策略见 [references/geo-strategy.md](references/geo-strategy.md)。

**GEO版额外内容：**

1. **FAQ问答块** — 4-6个问答，覆盖用户在AI搜索中的常见提问
   - 报告排版：先展示全部外语Q&A（Q和A外语在一起），再展示全部中文Q&A
   - 每个Q和A独立段落，便于整段复制
2. **场景化语义** — 每个卖点用 when/where/why 句式
3. **长尾自然语言** — 覆盖5-8个完整句子短语
4. **竞品对比差异化** — 一段明确对比文案
5. **可量化证据** — 所有卖点附数字
6. **JSON-LD结构化数据** — 嵌入描述HTML中
7. **多语言自然语言** — 根据目标市场覆盖相应语言的自然语言短语

### 7. 渲染HTML报告

```bash
python3 "$SKILL_DIR/scripts/render_report.py" report.json -o "<slug>-listing-<yyyymmdd>.html"
```

报告包含（全部外语+中文双语）：
1. 产品概览
2. 目标市场消费者分析
3. 关键词评分表
4. 属性清单
5. FABE卖点拆解
6. 转化驱动力分析
7. 速卖通普通版上架文案（标题含中文对照 / Item Specifics左右分栏 / 描述外语先分段再中文 / 搜索关键词 / 图片建议）
8. GEO版上架文案（FAQ外语集中+中文集中 / 场景化 / JSON-LD / 自然语言关键词 / 多语言）
9. 假设与推断项

**每个内容子模块必须包含「一键复制外文内容」按钮**，点击后将该模块内所有外文内容复制到剪贴板，方便用户粘贴到速卖通后台。

### 8. Self-review

- 每条规格可追溯到来源
- 标题字符数已精确计算
- 标题有中文翻译对照
- Item Specifics >=8字段，左右分栏显示
- 描述先外语后中文，已合理分段
- GEO版FAQ外语集中展示、中文集中展示
- 每个子模块有一键复制外文内容按钮
- 目标市场消费者分析已生成，含中文对照
- 关键词评分表含中文关键词对照
- 外语文案像目标市场本地文案不是中式直译
- 无编造价格/认证/销量
- HTML已生成且能打开

## Constraints

- 不调用付费 API
- 不把批发价当1件零售价
- 不编造认证/销量/测试数据
- 不在标题放竞品品牌名
- 标题 <=128字符（精确计算）
- 输出语言为主内容（默认英语），中文翻译始终提供
- 用户指定目标市场和语言时，先做消费者分析再生成文案
- HTML必须自包含（内联CSS+JS，无外部依赖）
- 每个子模块必须有一键复制外文内容按钮

## Source Attribution

| Label | 含义 |
|-------|------|
| `1688-page` / `1688页面` | 商品页或脚本抽出 |
| `image-analysis` / `图片分析` | 程序化视觉分析 |
| `user-provided` / `用户提供` | 用户明确说的 |
| `inferred` / `推断` | 从已有事实合理推出 |

## Additional Resources

- 速卖通上架字段清单: [references/aliexpress-listing-fields.md](references/aliexpress-listing-fields.md)
- GEO策略详解: [references/geo-strategy.md](references/geo-strategy.md)
- 关键词评分方法: [references/keyword-scoring.md](references/keyword-scoring.md)
- 视觉分析方法: [references/visual-analysis.md](references/visual-analysis.md)
- 1688数据抓取: `scripts/fetch_product_data.py`
- HTML渲染: `scripts/render_report.py`
- 报告模板: `assets/report_template.html`
