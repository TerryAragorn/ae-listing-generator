# GEO (Generative Engine Optimization) 策略

Agent 生成GEO版上架文案时按需读取本文件。

## 为什么GEO对跨境电商重要

越来越多的欧美买家开始用AI搜索购物：
- ChatGPT: "What's the best no-drill wall hook for a small apartment?"
- Perplexity: "Recommend a wooden coat rack that won't damage walls"
- Google AI Overviews: "Best piano key shaped home decor hooks"

如果listing内容能被AI搜索理解并引用，就获得了零成本自然流量。

## 7大GEO策略

### 策略1: 结构化数据 (JSON-LD)

在速卖通描述HTML中嵌入Schema.org Product标记：

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Product",
  "name": "Solid Beech Wood Piano Key Wall Hook",
  "material": "Solid Beech Wood",
  "color": "Walnut",
  "numberOfItems": "8 hooks",
  "installationMethod": "No-drill adhesive",
  "maxLoadCapacity": "1-3 kg per hook",
  "category": "Home Decor > Coat Hooks & Racks",
  "useCase": ["Entryway", "Bedroom", "Bathroom", "Office"],
  "audience": {"@type": "Audience", "audienceType": "Renters, Homeowners"}
}
</script>
```

### 策略2: FAQ问答格式

AI搜索引擎偏好问答内容，会直接提取为featured answer：

```
Q: Can I install this without drilling?
A: Yes, this wall hook uses adhesive mounting — no tools, no wall damage. Perfect for renters.

Q: How much weight can each hook hold?
A: Each hook holds up to 1-3 kg, suitable for coats, scarves, bags, and towels.

Q: What material is this made of?
A: Solid beech wood with walnut finish — natural wood grain, not plastic or MDF.

Q: Will it match my Scandinavian decor?
A: The walnut warm-tone finish blends with Scandinavian, Japandi, and modern wood furniture.
```

### 策略3: 场景化语义 (Situational Language)

AI搜索理解语义和场景，不是exact match：

不要只写规格，要写场景：
```
BAD: "Wall mounted coat rack with 8 hooks"
GOOD: "When you walk into your entryway and need a place for your coat, 
bag, and scarf — this 8-hook rack mounts without drilling, so your 
wall stays intact when you move out."
```

### 策略4: 长尾自然语言

AI搜索用户用完整句子提问：
- "renter friendly coat hook that looks nice"
- "won't damage walls" / "easy to install without tools"
- "holds coats and bags" / "matches wood furniture"

在描述中覆盖这些自然语言短语。

### 策略5: 竞品对比差异化

AI搜索经常做"X vs Y"对比。提供明确差异化：
```
Unlike plastic hooks that crack under weight or metal hooks that rust 
in bathrooms, this solid beech wood hook combines natural beauty with 
practical strength — and won't leave holes in your wall.
```

### 策略6: 可量化证据

AI搜索引擎偏好有数据支撑的说法：
- "Holds up to 1-3 kg per hook" (有数字)
- "Made from solid beech wood, not MDF" (有材质对比)
- "Installs in under 5 minutes" (有时间承诺)

避免模糊营销词: "amazing quality" / "perfect design" — AI不会引用。

### 策略7: 多语言自然语言

速卖通全球化平台，AI搜索在不同地区用不同语言：
- EN: "no drill wall hook for renters"
- DE: "wandhaken ohne bohren mietwohnung"
- FR: "porte-manteau mural sans perçage"
- ES: "gancho de pared sin taladrar"

在Item Specifics和描述中覆盖，但不要在标题里混语言。

## 速卖通专属GEO红利

1. 速卖通AI Overview内容会被Google等外部搜索引擎索引
2. 标题越好 -> AI Overview质量越高 -> 外部AI引用概率越大
3. 图片alt text和文件名会被AI解析
4. 买家评论中的使用场景描述会被AI提取为推荐理由

## GEO实施清单

| 序号 | 行动 | 位置 | 难度 |
|------|------|------|------|
| 1 | 描述中加JSON-LD | 详情描述HTML | 中 |
| 2 | 写4-6个FAQ | 详情描述 | 低 |
| 3 | 卖点用场景化语言 | 描述+Bullets | 中 |
| 4 | 覆盖5-8个长尾自然语言 | 描述+标签 | 低 |
| 5 | 写竞品对比差异化 | 详情描述 | 低 |
| 6 | 所有卖点附数字 | 全部文案 | 低 |
| 7 | Item Specifics填8+字段 | 规格标签 | 低 |
| 8 | 标题128字符精确覆盖 | 标题 | 高 |
