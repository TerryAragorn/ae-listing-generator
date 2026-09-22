# 关键词评分方法

Agent 执行关键词挖掘与评分时按需读取本文件。

## 关键词来源

1. 1688页面产品标题（中文）
2. 1688页面属性表（decisionCpv + normalCpv）
3. 1688页面卖点短句
4. 产品类目常识词
5. 竞品标题（如有）

## 关键词分类

从产品信息中提取以下5类关键词：

| 类别 | 说明 | 示例 |
|------|------|------|
| Product-type 产品类型词 | 产品是什么 | coat hook, wall hook, coat rack |
| Feature 特征词 | 产品有什么特征 | no drill, foldable, adhesive |
| Use-case 场景词 | 在哪用 | entryway, bedroom, bathroom |
| Audience 人群词 | 谁买 | renters, homeowners |
| Attribute 规格词 | 具体参数 | 8 hooks, beech wood, walnut |

## 3维度评分 (1-9分)

每个关键词按以下3个维度评分，总分1-9分：

| 维度 | 3分 | 2分 | 1分 |
|------|-----|-----|-----|
| Frequency 频次 | 核心品类词/标题必放 | 特征词/常用描述 | 边缘词/长尾 |
| Relevance 相关性 | 直接描述产品 | 间接相关 | 弱相关 |
| Opportunity 机会度 | 差异化词/少竞品用 | 常用词/多数竞品用 | 普遍词/全用 |

## 分层放置

| 层级 | 分数 | 放置位置 | 示例 |
|------|------|----------|------|
| Primary | 7-9分 | 标题 | coat hook, wall hook, no drill |
| Secondary | 4-6分 | Item Specifics / Bullets | foldable, beech wood, entryway |
| Tertiary | 2-3分 | 描述 | renter friendly, eco-friendly |
| Backend | 1分 | 搜索关键词(后端) | Japandi, Scandinavian, damage free |

## 关键词覆盖矩阵

输出 Keyword Coverage Map：

| Keyword | Score | Title | Specifics | Desc | Backend | Status |
|---------|-------|-------|-----------|------|---------|--------|
| coat hook | 9 | YES | YES | YES | - | GOOD |
| no drill | 8 | YES | YES | YES | YES | GOOD |
| piano key | 7 | YES | - | YES | - | GOOD |
| renter friendly | 4 | - | - | YES | YES | OK |

覆盖率目标: 90%+

## 标题优化公式 (<=128字符)

```
[核心品类词] + [材质词] + [功能/场景词x2-3] + [差异化记忆点] + [规格数字] + [归类大词]
```

示例 (115字符):
```
Solid Beech Wood Wall Hook No Drill Piano Key Coat Rack Entryway Bedroom Bathroom Hanger 8 Hooks Home Decor
```

注意事项：
- 精确计算字符数，在括号中标注
- 无品牌名（除非自有品牌已注册）
- 无促销词（best/free shipping/amazing）
- 128字符内尽量多覆盖Primary关键词
- 差异化记忆点（如Piano Key）必须出现在标题中
