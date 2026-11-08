# 學術圖形 Canvas 2D 專屬繪製引擎指南

本文件說明為何學術圖形（Figures / Models / Flowcharts）**嚴禁使用 `html2canvas` 搭配 SVG `<text>`**，以及如何以原生 Canvas 2D API 實作 100% 穩定且高解析度（Retina 2.5x）的圖片匯出機制。

---

## 1. 核心陷阱與原因分析

### 陷阱現象
當架構圖中使用 SVG 元素並在 `<svg>` 內撰寫文字（`<text>` 標籤）時，若使用 `html2canvas` 截圖：
- `html2canvas` 內部無法精準解析 SVG `<text>` 的字體基線、旋轉角度與矩陣座標。
- 結果造成**文字全部脫離節點並擠壓堆疊至畫面右側，左側圖形節點縮減為扭曲殘線**。

### 正確技術路線
1. **網頁 DOM 檢視**：
   - 節點方塊：採用普通 HTML `<div>`（搭配 Flexbox / Grid 或絕對定位），文字為純 HTML DOM 節點。
   - 連接線與箭頭：使用獨立底層 `<svg class="figure-svg-layer">`，**禁止在 SVG 內放任何 `<text>` 元素**。
2. **圖片匯出引擎**：
   - 使用原生 JavaScript `canvas.getContext('2d')` 自行繪製。
   - 離線可用、不依賴外部龐大庫、繪製速度極快且絕不崩壞。

---

## 2. Canvas 2D 引擎實作規範

### 2.1 高解析度 (2.5x Retina) 設定
```javascript
const scale = 2.5; // 2.5 倍超高清晰度
const width = 1040;
const height = 480;
const canvas = document.createElement('canvas');
canvas.width = width * scale;
canvas.height = height * scale;
const ctx = canvas.getContext('2d');
ctx.scale(scale, scale);

// 繪製前必須填滿純白背景（避免匯出時背景呈透明或黑色）
ctx.fillStyle = '#ffffff';
ctx.fillRect(0, 0, width, height);
```

### 2.2 箭頭與連線輔助函式
```javascript
function drawArrow(ctx, x1, y1, x2, y2, isDashed = false) {
  ctx.save();
  ctx.strokeStyle = '#111111';
  ctx.fillStyle = '#111111';
  ctx.lineWidth = 1.35;
  if (isDashed) ctx.setLineDash([5, 4]);
  else ctx.setLineDash([]);

  // 主線
  ctx.beginPath();
  ctx.moveTo(x1, y1);
  ctx.lineTo(x2, y2);
  ctx.stroke();

  // 箭頭
  ctx.setLineDash([]);
  const angle = Math.atan2(y2 - y1, x2 - x1);
  const arrowLen = 8;
  ctx.beginPath();
  ctx.moveTo(x2, y2);
  ctx.lineTo(x2 - arrowLen * Math.cos(angle - Math.PI / 6), y2 - arrowLen * Math.sin(angle - Math.PI / 6));
  ctx.lineTo(x2 - arrowLen * Math.cos(angle + Math.PI / 6), y2 - arrowLen * Math.sin(angle + Math.PI / 6));
  ctx.closePath();
  ctx.fill();
  ctx.restore();
}
```

### 2.3 動態取得最新文字（關鍵防護）
為避免使用者在畫面上修改文字後，匯出的圖片仍是舊內容，**嚴格禁止在 Canvas 繪製中寫死靜態字串**：

```javascript
function getElementText(key, defaultVal) {
  const el = document.querySelector(`[data-key="${key}"]`);
  if (!el) return defaultVal;
  return el.innerText.trim() || defaultVal;
}
```

---

## 3. 匯出與剪貼簿複製標準函式

```javascript
async function copyCanvasToClipboard(canvas) {
  canvas.toBlob(async (blob) => {
    if (!blob) throw new Error('Blob creation failed');
    try {
      await navigator.clipboard.write([
        new ClipboardItem({ 'image/png': blob })
      ]);
      showToast('✓ 圖形已成功複製為圖片！可於 Word、PPT 或 LINE 貼上');
    } catch (err) {
      downloadCanvas(canvas);
      showToast('✓ 因剪貼簿安全限制，已自動為您下載高畫質 PNG 圖片！');
    }
  }, 'image/png');
}
```
