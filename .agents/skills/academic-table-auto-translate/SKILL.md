---
name: academic-table-auto-translate
description: >-
  當使用者提供純英文（或外文）的學術論文圖表、流程圖、架構圖或一般圖形截圖時，自動進行圖形結構解析、數據提取，
  並自主判斷翻譯為「臺灣習慣用語繁體中文」，繪製為高解析度現代化雙語 HTML（支援學術三線表與向量 SVG 圖形/流程圖/架構圖）。
  具備智慧排版（短詞同行、長句換行）、Times New Roman 與標楷體、高畫質 PNG 複製與另存圖片功能，以及「雙擊文字即轉輸入框即時修改與儲存」功能。
---

# Academic Table & Figure Auto-Translate to HTML Skill (英文圖表與各類圖形自動轉臺灣雙語 HTML)

本技能專門處理**「僅有原文（英文）圖片，無中文對照」**的情境。不僅支援**學術三線表格（Tables）**，亦全面支援**各類學術圖形（Figures：路徑分析模型圖、流程圖、系統架構圖、概念模型圖、統計折線/長條圖、示意圖）**。

AI 需自行辨識結構與內容，**並在無需外部詞庫的情況下，自主判斷上下文語境，精確翻譯為臺灣學術習慣繁體中文**，生成高品質、現代化、支援就地雙擊編輯與一鍵匯出高解析度 PNG 的雙語 HTML 成品。

---

## 📁 技能模組與目錄結構 (Skill Modules)

本技能具備完整模組化結構，包含指令、可執行驗證腳本、參考手冊與標準範本資源：

```text
academic-table-auto-translate/
├── SKILL.md                              # 核心流程與指令主文件
├── scripts/                              # 輔助與驗證工具腳本
│   └── validate_academic_html.py         # 自動檢驗產出 HTML 規範符合度之驗證腳本
├── references/                           # 詳細學術慣用語與渲染規範指南
│   ├── taiwan_academic_terminology.md    # 臺灣學術慣用語與大陸簡轉繁防禦指南
│   ├── canvas_rendering_guide.md         # Canvas 2D 高解析度繪圖引擎實作指南
│   └── three_line_table_guide.md         # APA 7th / Booktabs 學術三線表格規範
└── assets/                               # 靜態資源與 HTML 樣板
    └── templates/                        # 現代化雙語 HTML 範本庫
        ├── figure_template.html          # 學術模型架構圖範本 (DOM + SVG + Canvas 2D)
        └── table_template.html           # 學術三線表格範本 (Booktabs + html2canvas)
```

---

## 📌 重大除錯經驗與防坑指南（Critical Bug Prevention）

在過往實踐中曾發生重大渲染錯誤，**未來執行時務必嚴格遵守以下防範原則，絕對不可重蹈覆轍**：

### ⚠️ 陷阱一：SVG `<text>` 與 `html2canvas` 衝突導致畫面全毀
- **錯誤現象**：若直接使用 SVG 向量圖形包含 `<text>` 元素，並嘗試以 `html2canvas` 匯出圖片，`html2canvas` 無法正確解析 SVG 文字的排版矩陣與座標，會導致**所有文字被粗暴抽出並在右側堆疊成一長串雜亂純文字，左側圖形則縮成一團扭曲殘缺的線條（完全錯誤）**。
- **鐵律規範**：
  1. **禁止在架構圖/模型圖中使用包含大量 `<text>` 的純 SVG 搭配 `html2canvas`**。
  2. **圖形架構推薦標準：HTML DOM 卡片 + 純向量連接線圖層**：
     - **卡片／文字節點**：使用語意化 HTML `<div>`（如 `.model-box`）搭配 CSS 絕對定位或 Flex/Grid 佈局，所有文字皆為普通 DOM 元素。
     - **箭頭／連接線**：使用獨立的底層 `<svg class="figure-svg-layer">`（設定 `position: absolute; pointer-events: none;`），且 SVG 內**嚴禁包含任何 `<text>` 標籤**，僅負責繪製 `<line>`、`<path>` 與 `<marker>`。
  3. **圖形圖片匯出終極解法：原生 Canvas 2D 專屬繪製引擎（推薦）**：
     - 若為複雜圖形，**完全不依賴外部 `html2canvas`**，直接在 JS 內編寫輕量且精準的原生 `renderDiagramToCanvas()` 繪圖函式。
     - 透過 Canvas 2D API（`fillRect`、`strokeRect`、`lineTo`、`fillText`）以 2.5 倍 Retina 解析度直接繪製，無任何 CDN 網路依賴，保證離線可用、文字與線條絕對銳利，且 100% 杜絕圖形崩壞。

### ⚠️ 陷阱二：使用者自訂修改文字後，匯出圖片未同步更新
- **錯誤現象**：使用者在介面上修改了文字，但點擊「複製為圖片」或「另存圖片」時，下載的圖片依然是舊的預設文字。
- **鐵律規範**：
  - 匯出函式（無論是 Canvas 2D 繪製或 DOM 抓取）**必須動態讀取 DOM 節點中的即時文字（或 `localStorage` 暫存）**，嚴禁在繪製代碼中寫死靜態預設字串！
  - 透過 `getElementText(key, defaultVal)` 統一取得畫面最新文字，確保使用者修改能 100% 同步反應在輸出的 PNG 圖片中。

### ⚠️ 陷阱三：誤加已被使用者剔除的多餘按鈕
- **錯誤現象**：在工具列中加入了「複製圖表到剪貼簿」、「複製 Markdown」、「列印 / 另存 PDF」等無效或冗餘按鈕。
- **鐵律規範**：
  - 工具列**嚴格只保留**：
    1. 排版模式切換按鈕（智慧排版、置於下方、同行接續、純英文、純中文）
    2. `💡 雙擊任何文字可輸入修改`（提示膠囊標籤）
    3. `📷 複製為圖片 (PNG)`（高亮主按鈕）
    4. `💾 另存圖片`
    5. `↺ 重設文字`（提供使用者一鍵清除修改、還原為論文預設翻譯）

---

## 📌 AI 自主判斷臺灣習慣用語原則（無須外部詞庫）

本技能不依賴任何外部術語字典，**AI 必須根據自身訓練知識庫與論文上下文，主動執行以下判斷與轉換**：

1. **嚴格遵循臺灣在地學術與技術慣用語**：
   - 翻譯時必須完全以臺灣學術界（國科會、中研院、教育部、各大專院校期刊）之慣用語為唯一準則。
2. **主動識別並杜絕中國大陸簡轉繁詞彙**：
   - 遇到可能帶有大陸習慣的詞彙時，AI 必須自主過濾並更正為臺灣用語，常見判斷對比如下（僅供理解原則，AI 應主動推廣至所有類似詞彙）：
     - 統計/資料：**分群**（非「聚類」）、**變異數**（非「方差」）、**假設檢定**（非「假設檢驗」）、**事後檢定**（非「事後檢驗」）、**資料/數據**（非一律稱「數據」）。
     - 中心性/SNA：**度數/入度/出度**、**中介中心性**（Betweenness）、**接近中心性**（Closeness）。
     - 科技/資訊：**演算法**（非「算法」）、**資訊**（非「信息」）、**網路**（非「網絡」）、**預設**（非「默認」）、**使用者**（非「用戶」）、**程式碼**（非「代碼」）、**伺服器**（非「服務器」）、**最佳化**（非「優化」）。
     - 研究/教育：**同儕**（非「同輩/同伴」）、**專案**（非「項目」）、**互動**（非「交互」）、**前測**（非「前置測試」）、**作業/成績**（非「任務/作業」）、**表現/成效**（教育情境非「績效」）。
3. **上下文語意推導（Contextual Reasoning）**：
   - 當遇到新興科技（如生成式 AI、LLM）、跨領域術語或簡寫時，AI 應結合論文研究主題，自主選擇最通順、最符合臺灣讀者閱讀習慣的學術譯名。
   - 更多詳細術語對照與原則請參閱：[臺灣學術慣用語對照指南](./references/taiwan_academic_terminology.md)。

---

## 支援的內容類型與重繪技術架構

| 類型 | 常見範例 | 最佳 HTML 重繪技術 | 圖片匯出方案 | 對應範本與指引 |
| :--- | :--- | :--- | :--- | :--- |
| **學術表格 (Tables)** | 統計摘要表、ANOVA 檢定表、分群指標表、迴歸分析表 | 語意化 HTML `<table>` + Booktabs 三線表樣式 | `html2canvas` 渲染純表格 DOM（安全無誤） | [三線表格範本](./assets/templates/table_template.html)<br>[三線表格排版指南](./references/three_line_table_guide.md) |
| **模型架構圖 (Model Figures)** | 結構方程模型 (SEM)、路徑分析 (Path Analysis)、因果關係圖 | **HTML DOM 節點卡片 + 底層純 SVG 箭頭線** | **專屬 Canvas 2D 繪圖引擎（100% 防出錯）** | [模型架構圖範本](./assets/templates/figure_template.html)<br>[Canvas 繪圖指南](./references/canvas_rendering_guide.md) |
| **流程圖與管線圖 (Flowcharts)** | 資料處理流程、實驗步驟、演算法流程、決策樹 | HTML DOM 節點 + SVG 連接線 | 專屬 Canvas 2D 或 DOM 渲染 | [模型架構圖範本](./assets/templates/figure_template.html) |
| **系統架構圖 (Architectures)** | 深度學習模型架構、模組關聯圖、系統平台架構 | CSS Grid/Flexbox 卡片 + SVG 匯流排連線 | 專屬 Canvas 2D 繪圖引擎 | [模型架構圖範本](./assets/templates/figure_template.html) |
| **統計圖表 (Charts)** | 長條圖、折線趨勢圖、散佈圖、箱形圖 | 內嵌 `<svg>` 繪製向量刻度與路徑 | 專屬 Canvas 2D 或高解析 SVG 轉 Canvas | [Canvas 繪圖指南](./references/canvas_rendering_guide.md) |

---

## 雙語版面佈局規範

1. **英文在前，中文在後**：
   - **短標籤／短標題**：同行接續（例如 `Table 1 表 1`、`Figure 1 圖 1`、`Input 輸入`、`Degree 度數中心性`）。
   - **長句子／段落描述**：中文自動斷行換至英文正下方（`class="zh-block"` 或 `.zh-line`），例如分群描述、模型節點對比、表末/圖末附註（Note）。
2. **數值與代碼絕對不變**：
   - 所有的統計數據（$M$, $SD$, $F$, $p$）、路徑係數（$\beta$）、變異解釋量（$R^2$）、坐標軸刻度、事後檢定下標（$a$, $b$, $ab$）維持原樣，不可更改或省略小數點。
   - 數學變數字母（如 *k*, *N*, *M*, *SD*, *F*, *p*, *R*², *β* 等）一律採用斜體。
3. **字型規範**：
   - **中文**：全數使用**標楷體**（優先載入 `DFKai-SB`, `BiauKai`, `標楷體`, `KaiTi`, `serif`）。
   - **英文、數字與統計代碼**：標準學術期刊字型 `Times New Roman`, `serif`。

---

## 雙擊文字即時編輯（Inline Text Editing）標準實現

為賦予使用者就地調整文字之彈性，產出的 HTML 必須內建完整的就地編輯機制：

### 1. HTML 與 CSS 規範
- 所有包含文字的元素加上類別 `.editable-text`，並設定唯一的 `data-key="unique_id"`。
- CSS 樣式：
```css
.editable-text {
  cursor: pointer;
  transition: background-color 0.15s ease, outline 0.15s ease;
  border-radius: 3px;
  padding: 0 2px;
}
.editable-text:hover {
  outline: 1.5px dashed #3b82f6;
  background-color: rgba(239, 246, 255, 0.85);
}
.inline-edit-input {
  width: 95%;
  border: 1.5px solid #2563eb;
  border-radius: 3px;
  padding: 2px 4px;
  background: #ffffff;
  outline: none;
  box-shadow: 0 0 0 2px rgba(37, 99, 235, 0.2);
  color: #111111;
  box-sizing: border-box;
}
```

### 2. JavaScript 核心邏輯
```javascript
// 取得即時最新文字（支援動態讀取使用者自訂值）
function getElementText(key, defaultVal) {
  const el = document.querySelector(`[data-key="${key}"]`);
  if (!el) return defaultVal;
  return el.innerText.trim() || defaultVal;
}

// 初始化雙擊編輯監聽
function initDoubleTapEdit(storageKey = 'diagram_user_edits') {
  loadSavedEdits(storageKey);

  document.querySelectorAll('.editable-text').forEach(el => {
    el.setAttribute('title', '雙擊可直接編輯此文字');
    el.addEventListener('dblclick', function(e) {
      e.stopPropagation();
      startEditing(this, storageKey);
    });
  });
}

function startEditing(el, storageKey) {
  if (el.querySelector('input, textarea')) return;
  const key = el.getAttribute('data-key');
  const originalText = el.innerText.trim();

  const isMultiLine = originalText.length > 40;
  const input = document.createElement(isMultiLine ? 'textarea' : 'input');
  input.className = 'inline-edit-input';
  input.value = originalText;

  const style = window.getComputedStyle(el);
  input.style.fontSize = style.fontSize;
  input.style.fontFamily = style.fontFamily;
  input.style.textAlign = style.textAlign || 'center';
  if (isMultiLine) {
    input.style.minHeight = '55px';
    input.style.resize = 'vertical';
  }

  el.innerHTML = '';
  el.appendChild(input);
  input.focus();
  input.select();

  let isFinished = false;
  function commit() {
    if (isFinished) return;
    isFinished = true;
    const val = input.value.trim() || originalText;
    el.textContent = val;
    saveEdit(key, val, storageKey);
    showToast('✓ 已儲存修改！「複製為圖片」與「另存圖片」將自動同步更新');
  }

  input.addEventListener('blur', commit);
  input.addEventListener('keydown', function(evt) {
    if (evt.key === 'Enter' && !isMultiLine) {
      evt.preventDefault();
      commit();
    } else if (evt.key === 'Enter' && evt.ctrlKey && isMultiLine) {
      evt.preventDefault();
      commit();
    } else if (evt.key === 'Escape') {
      isFinished = true;
      el.textContent = originalText;
    }
  });
}

function saveEdit(key, val, storageKey) {
  if (!key) return;
  try {
    const edits = JSON.parse(localStorage.getItem(storageKey) || '{}');
    edits[key] = val;
    localStorage.setItem(storageKey, JSON.stringify(edits));
  } catch (e) {
    console.warn('儲存失敗', e);
  }
}

function loadSavedEdits(storageKey) {
  try {
    const edits = JSON.parse(localStorage.getItem(storageKey) || '{}');
    Object.keys(edits).forEach(key => {
      const el = document.querySelector(`[data-key="${key}"]`);
      if (el && edits[key]) {
        el.textContent = edits[key];
      }
    });
  } catch (e) {
    console.warn('載入自訂文字失敗', e);
  }
}

function resetToDefaults(storageKey) {
  if (!confirm('確定要清除所有文字修改，恢復為預設的論文原文翻譯嗎？')) return;
  localStorage.removeItem(storageKey);
  location.reload();
}
```

---

## 原生 Canvas 2D 專屬繪圖引擎標準結構（圖形專用）

對於圖形（Figure），**嚴禁呼叫 `html2canvas`**，必須採用專屬 Canvas 2D 繪製函式：

```javascript
function renderDiagramToCanvas() {
  const scale = 2.5; // 2.5x Retina 高畫質
  const width = 1040;
  const height = 480;
  const canvas = document.createElement('canvas');
  canvas.width = width * scale;
  canvas.height = height * scale;
  const ctx = canvas.getContext('2d');
  ctx.scale(scale, scale);

  // 1. 純白背景
  ctx.fillStyle = '#ffffff';
  ctx.fillRect(0, 0, width, height);

  // 2. 輔助函式：繪製箭頭 (支援實線與虛線)
  function drawArrow(x1, y1, x2, y2, isDashed) {
    ctx.save();
    ctx.strokeStyle = '#111111';
    ctx.fillStyle = '#111111';
    ctx.lineWidth = 1.35;
    if (isDashed) ctx.setLineDash([5, 4]);
    else ctx.setLineDash([]);

    ctx.beginPath();
    ctx.moveTo(x1, y1);
    ctx.lineTo(x2, y2);
    ctx.stroke();

    // 箭頭頭部
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

  // 3. 輔助函式：繪製節點方塊與文字 (動態讀取 DOM 最新文字)
  function drawBox(x, y, w, h, lines) {
    ctx.save();
    ctx.fillStyle = '#ffffff';
    ctx.strokeStyle = '#111111';
    ctx.lineWidth = 1.4;
    ctx.fillRect(x, y, w, h);
    ctx.strokeRect(x, y, w, h);

    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    const totalH = lines.length * 15;
    let startY = y + h / 2 - totalH / 2 + 7;

    lines.forEach(l => {
      if (l.font === 'kai') {
        ctx.font = '12px "DFKai-SB", "BiauKai", "標楷體", serif';
        ctx.fillStyle = '#374151';
      } else {
        ctx.font = (l.size || 13) + 'px "Times New Roman", serif';
        ctx.fillStyle = '#111111';
      }
      ctx.fillText(l.text, x + w / 2, startY);
      startY += 15;
    });
    ctx.restore();
  }

  // 依模型節點座標逐一繪製連接線與卡片，卡片文字一律透過 getElementText('key', 'default') 抓取...
  return canvas;
}

// 複製圖片
async function copyChartAsImage() {
  showToast('⏳ 正在生成高解析度圖片...');
  try {
    const canvas = renderDiagramToCanvas();
    canvas.toBlob(async (blob) => {
      if (!blob) throw new Error('Blob creation failed');
      try {
        await navigator.clipboard.write([
          new ClipboardItem({ 'image/png': blob })
        ]);
        showToast('✓ 圖形已成功複製為圖片！可於 Word、PPT 或 LINE 按 Ctrl+V 貼上');
      } catch (err) {
        downloadCanvas(canvas);
        showToast('✓ 因剪貼簿安全限制，已自動為您下載高畫質 PNG 圖片！');
      }
    }, 'image/png');
  } catch (err) {
    showToast('複製失敗，請直接使用「另存圖片」功能');
  }
}

// 另存圖片
function downloadChartImage() {
  showToast('⏳ 正在準備下載...');
  try {
    const canvas = renderDiagramToCanvas();
    downloadCanvas(canvas);
    showToast('✓ 圖形圖片下載成功！');
  } catch (err) {
    showToast('下載失敗，請嘗試使用列印功能存為 PDF');
  }
}

function downloadCanvas(canvas) {
  const link = document.createElement('a');
  link.download = (document.title || 'academic_figure').replace(/[^a-zA-Z0-9\u4e00-\u9fa5]/g, '_') + '.png';
  link.href = canvas.toDataURL('image/png');
  link.click();
}
```

---

## 環境維護與品質驗證原則

- 每次生成成品 HTML 後，可執行驗證腳本自動檢查規範符合性：
  ```bash
  python .agents/skills/academic-table-auto-translate/scripts/validate_academic_html.py <HTML路徑>
  ```
- 腳本詳情與驗證指標請參閱：[HTML 規範驗證工具](./scripts/validate_academic_html.py)。
- 除了最終產出的 `.html` 成品檔案外，**務必清理所有執行過程中產生的暫存截圖、除錯檔案、測試腳本或中介檔**，保持工作資料夾乾淨整潔。
