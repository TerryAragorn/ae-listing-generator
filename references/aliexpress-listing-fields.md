# AliExpress 后台上架字段清单

Agent 执行速卖通上架文案生成时按需读取本文件。

## 基本信息区

| 字段 | 必填 | 说明 | 字符限制 |
|------|------|------|----------|
| Product Title 标题 | 是 | 关键词矩阵覆盖，无品牌名/促销词 | <=128 chars |
| Category 类目 | 是 | 选择最精准的叶子类目 | - |
| Product Properties 产品属性 | 是 | 系统属性 + 自定义属性 | - |
| Reference Price 参考价 | 是 | 非公开，用于平台参考 | - |

## Item Specifics 规格标签区

速卖通要求填写的结构化产品属性。至少填8个字段。

| 常见字段 | 示例值 | 说明 |
|----------|--------|------|
| Material 材质 | Solid Beech Wood | 写具体材质，不要只写Wood |
| Brand Name 品牌 | (自有品牌或留空) | 未授权不放他人品牌 |
| Origin 产地 | Mainland China | - |
| CN 省份 | Zhejiang | - |
| Type 类型 | Coat Hooks & Racks | 选择系统类目属性 |
| Feature 特征 | Eco-friendly, Stocked | 多选标签词 |
| Function 功能 | Multi-functional, Reusable | - |
| Additional Features 额外特性 | No Drill, Foldable, Lightweight | 差异化特性 |
| High-concerned chemical | None | 欧美合规必填 |
| Installation Method | Adhesive / No-drill | 安装方式 |
| Model Number 型号 | (产品标题简化版) | 可用标题填 |
| Frame Material | None / Wood | 视产品而定 |

## SKU & 价格区

| 字段 | 说明 |
|------|------|
| SKU Properties | 颜色 + 规格（如4 Hook/6 Hook），最多2个维度 |
| SKU Price | 每个SKU的单价（USD） |
| SKU Stock | 每个SKU的库存数量 |
| SKU Image | 每个SKU配一张图 |
| Retail Price 零售价 | 原价（划线价） |
| Sale Price 促销价 | 折扣后价格 |
| MOQ 起订量 | 默认1件 |
| Bulk Discount 批量折扣 | 如10件+额外1% off |
| Unit | piece / set / pair |

## 描述区

| 字段 | 说明 |
|------|------|
| AI Overview | 速卖通AI从标题+Item Specifics自动生成，无需手动填 |
| Description 商品描述 | HTML格式，补充AI不会生成的内容 |
| Mobile Description | 移动端专属描述（可选） |
| User Manual PDF | 可上传PDF说明书（可选） |

描述HTML建议结构：
1. 产品特点（3-5条，benefit-led）
2. 安装步骤（分步说明）
3. 使用场景（覆盖多个房间/场景）
4. 包装内容清单
5. FAQ问答（GEO版才加）

## 图片区

| 字段 | 要求 |
|------|------|
| Main Image 主图 | 白底，800x800px以上，无文字/水印 |
| Product Images 副图 | 5-6张：场景图、细节图、尺寸图、包装图 |
| Detail Images 详情图 | 可放长图，展示更多细节 |

## 物流与服务区

| 字段 | 说明 |
|------|------|
| Shipping Template 运费模板 | 选择预设模板 |
| Delivery Time 发货时效 | 如48小时发货 |
| Service Promise | 7天无理由、品质不符包赔等 |
| Shipping From | 发货地 |
| Unit Weight | 单件重量（g） |
| Package Size | 包装尺寸 |

## 搜索优化区

| 字段 | 说明 |
|------|------|
| Search Keywords 搜索关键词 | Backend关键词，空格分隔，<=250 bytes，买家不可见 |
| Product Tags | 产品标签（如有） |
| Store Category | 店铺内分类 |

## 合规区

| 字段 | 说明 |
|------|------|
| High-concerned Chemical | None（必填） |
| Product Compliance | 视类目要求 |
| Intellectual Property | 品牌授权（如用品牌） |
| Certification | 视类目要求（CE/FCC等） |

## 速卖通 AI Overview 机制

速卖通现在用AI自动生成产品描述（标注"AI overview of item"），完全替代了人工长描述。

- AI从标题和Item Specifics提取信息
- 每段首句用benefit-led短语开头
- 生成5-7段，覆盖功能/规格/材质/安全/包装
- 标题写得越好，AI生成质量越高
- Item Specifics越完整，AI段落数越多

**策略：标题里有什么词，AI Overview就会展开什么。把想让AI展开的关键词都放进标题和Item Specifics。**
