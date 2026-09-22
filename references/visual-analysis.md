# 视觉分析方法

Agent 对产品主图做程序化视觉分析时按需读取本文件。

当运行时支持图片直接查看时，优先用 view_image 直接分析。否则用以下Python程序化方法。

## 分析脚本

使用Python PIL + numpy对产品图片做程序化分析：

### 1. 基本信息提取
```python
from PIL import Image
img = Image.open('product.jpg').convert('RGB')
print(f"Dimensions: {img.size}")  # 尺寸
print(f"Mode: {img.mode}")        # 色彩模式
```

### 2. 色彩分析
```python
import numpy as np
arr = np.array(img.resize((100, 100)))
r_avg = arr[:,:,0].mean()
# 暖色/冷色判断
warm = sum(1 for p in pixels if p[0] > p[2] + 10) / total
# 主色调提取
q = img.quantize(colors=6)
```

### 3. 纹理分析
```python
gray = np.array(img.convert('L'))
variance = np.var(gray)  # 高=木纹/纹理明显
# 水平vs垂直纹理方向
h_var = np.var(np.diff(gray, axis=0))
v_var = np.var(np.diff(gray, axis=1))
```

### 4. 边缘密度
```python
gx = np.abs(np.diff(gray, axis=1))  # 水平梯度
gy = np.abs(np.diff(gray, axis=0))  # 垂直梯度
edge_density = (gx + gy > 25).sum() / gray.size
```

### 5. 图案重复检测
```python
# 检测中带亮度变化次数，判断是否有重复元素
middle = gray[h//3:2*h//3, :]
col_profile = middle.mean(axis=0)
smoothed = np.convolve(col_profile, np.ones(15)/15, mode='same')
transitions = sum(1 for i in range(1,len(diffs)) if diffs[i-1]*diffs[i] < 0)
```

### 6. OCR文字检测
```bash
tesseract product.jpg stdout -l chi_sim+eng
```

## 输出格式

每个视觉分析结果标注为 `image-analysis` 来源：

| 属性 | 示例值 | 来源 |
|------|--------|------|
| Image Resolution | 1440x1440 pixels | image-analysis |
| Color Tone | Predominantly warm (96.4% warm pixels) | image-analysis |
| Color Distribution | Cream/Beige/Walnut brown/Dark brown | image-analysis |
| Wood Grain Direction | Horizontal | image-analysis |
| Texture Complexity | High variance (4161), visible grain | image-analysis |
| Edge Density | Medium-high (34.5%), detailed craftsmanship | image-analysis |
| Pattern Repetition | ~91 transitions, repeated elements visible | image-analysis |
| Image Text | No OCR text, no watermarks | image-analysis |
| Composition | Square 1:1, product centered | image-analysis |

## 合并规则

- 同一属性 1688 与图冲突：尺寸/材质名/型号以 1688-page 为准
- 颜色/风格/质感以 image-analysis 为准
- 图上读到的文字标 image-analysis，OCR不确定则 inferred
