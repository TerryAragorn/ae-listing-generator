---
name: ae-listing-generator
description: "Generate AliExpress listing content from a 1688 or domestic e-commerce product link. Produces a self-contained HTML report with: (1) product selling points with FABE analysis and pain-point targeting, (2) AliExpress backend listing copy (regular version: title, item specifics, description, SKU, keywords), (3) GEO-enhanced listing copy (with AI search optimization: JSON-LD, FAQ, situational language, natural language keywords). Use when user provides a product link and wants AliExpress-ready listing content for cross-border selling to US/EU markets."
---

# AliExpress Listing Generator

给一个 1688 链接或其他国内电商链接，提取产品数据，挖掘卖点，生成速卖通上架文案（普通版 + GEO版），输出自包含 HTML 报告。

## When to Use

- 用户提供 1688 / 淘宝 / 拼多多 / 京东 等国内电商产品链接
- 用户要生成速卖通上架文案
- 用户要做 GEO/AEO 优化版本的上架文案
- 用户想从 1688 货源直接生成跨境 listing

## Workflow

```
Task Progress:
- [ ] 1. 识别输入并提取产品数据
- [ ] 2. 关键词挖掘与评分
- [ ] 3. 卖点挖掘 (5层模型)
- [ ] 4. 生成速卖通普通版上架文案
- [ ] 5. 生成GEO版上架文案
- [ ] 6. 渲染HTML报告
- [ ] 7. Self-review
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

### 2. 关键词挖掘与评分

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

详细方法见 [references/keyword-scoring.md](references/keyword-scoring.md)。

### 3. 卖点挖掘 (5层模型)

**Layer 1 属性清单** — 列出全部属性，标来源（1688-page / image-analysis / inferred）

**Layer 2 Feature (FABE-F)** — 中文属性译成英文，分类 physical/functional/design/experience

**Layer 3 Advantage + Benefit (FABE-AB)** — 对每条feature写：
- Advantage: 比普通方案好在哪
- Benefit: 买家得到什么结果（先结果后规格）
- Evidence: 可追溯数字/材质/结构，没有就留空

**Layer 4 转化驱动力** — 选1个主驱动：
- Visual-Driven 视觉驱动: 靠外观/质感/礼品感成交
- Pain-Driven 痛点驱动: 靠解决反复问题成交
- Emotion-Value-Driven 情感价值驱动: 靠身份/关怀/新奇成交

写 Buyer Reason Card：Target Buyer / Purchase Trigger / Belief Shift / Primary Reason / Proof

**Layer 5 跨境文案** — 按主驱动排序的英文卖点 + 中文对照

### 4. 速卖通普通版上架文案

生成速卖通后台上架需要的全部字段。完整字段清单见 [references/aliexpress-listing-fields.md](references/aliexpress-listing-fields.md)。

核心字段：

**标题 (<=128字符)**
- 公式: [核心品类词] + [材质词] + [功能/场景词x2-3] + [差异化记忆点] + [规格数字] + [归类大词]
- 精确计算字符数，留余量
- 无品牌名（除非自有品牌已注册），无促销词

**Item Specifics (至少8个字段)**
- Material / Origin / High-concerned chemical / Additional Features / Function / Feature / Type / Installation Method

**SKU 矩阵**
- 2色 x 3规格 = 6个SKU（参考竞品常见做法）
- 每个SKU标注价格、库存、SKU图片

**描述 (HTML)**
- 速卖通AI Overview会从标题+Item Specifics自动生成描述
- 在描述中补充AI不会自动生成的内容：安装步骤、使用场景、包装内容

**搜索关键词 (Backend)**
- 空格分隔，无重复，<=250 bytes

**图片建议**
- 主图: 白底800x800px
- 副图: 5-6张，含场景图、细节图、尺寸图

### 5. GEO版上架文案

在普通版基础上增加 GEO (Generative Engine Optimization) 内容，让AI搜索引擎能找到并推荐产品。详细策略见 [references/geo-strategy.md](references/geo-strategy.md)。

**GEO版额外内容：**

1. **FAQ问答块** — 4-6个问答，覆盖用户在AI搜索中的常见提问
2. **场景化语义** — 每个卖点用 when/where/why 句式
3. **长尾自然语言** — 覆盖5-8个完整句子短语（如"renter friendly coat hook"）
4. **竞品对比差异化** — 一段明确对比文案
5. **可量化证据** — 所有卖点附数字
6. **JSON-LD结构化数据** — 嵌入描述HTML中
7. **多语言自然语言** — 英/德/法/西语自然语言短语

### 6. 渲染HTML报告

```bash
python3 "$SKILL_DIR/scripts/render_report.py" report.json -o "<slug>-listing-<yyyymmdd>.html"
```

报告包含（全部中英双语）：
1. 产品概览
2. 关键词评分表
3. 属性清单
4. FABE卖点拆解
5. 转化驱动力分析
6. 速卖通普通版上架文案（标题/Item Specifics/SKU/描述/搜索关键词/图片建议）
7. GEO版上架文案（FAQ/场景化/JSON-LD/自然语言关键词/多语言）
8. 假设与推断项

### 7. Self-review

- 每条规格可追溯到来源
- 标题字符数已精确计算
- Item Specifics >=8字段
- GEO版包含FAQ和JSON-LD
- 英文像美国电商文案不是中式直译
- 无编造价格/认证/销量
- HTML已生成且能打开

## Constraints

- 不调用付费 API
- 不把批发价当1件零售价
- 不编造认证/销量/测试数据
- 不在标题放竞品品牌名
- 标题 <=128字符（精确计算）
- 英文为主输出，中文对照
- HTML必须自包含（内联CSS，无外部依赖）

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
