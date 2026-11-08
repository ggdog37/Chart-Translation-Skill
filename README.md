# 📊 Chart-Translation-Skill (英文學術圖表自動轉臺灣雙語 HTML 技能)

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Antigravity Skill](https://img.shields.io/badge/Antigravity-Agent%20Skill-green.svg)](https://github.com/ggdog37/Chart-Translation-Skill)
[![Language: Traditional Chinese](https://img.shields.io/badge/Language-繁體中文%20(臺灣)-red.svg)](https://github.com/ggdog37/Chart-Translation-Skill)

專為學術研究者與論文撰寫者設計的 **AI Agent 技能模組**。
專門處理**「僅有原文（英文或外文）論文截圖，無中文對照」**的情境。AI 能自動辨識圖表結構與數據、自主推導符合**臺灣學術習慣之繁體中文**，並重繪為高品質、高解析度、可就地編輯並一鍵匯出圖片的現代化雙語 HTML 成品。

---

## 🌟 核心特色 (Key Features)

- 🇹🇼 **嚴格遵循臺灣學術慣用語（自主判斷，無須外部字典）**
  - 完全以臺灣學術界（國科會、中研院、教育部期刊）為準則。
  - 主動防禦並杜絕大陸簡轉繁詞彙（如：**分群**而非「聚類」、**變異數**而非「方差」、**入度/中介中心性**、**演算法**而非「算法」、**學習成效**而非「績效」）。
- 📑 **全面支援學術圖表與模型架構圖**
  - **學術三線表 (Booktabs Tables)**：符合 APA 7th 規範（粗頂線、細欄線、粗底線，嚴禁垂直線）。
  - **模型與架構圖 (Model Figures)**：SEM 結構方程模型、路徑分析、流程圖、演算法管線圖。
- 🎨 **現代化雙語互動體驗 (Interactive HTML)**
  - **5 種排版模式一鍵切換**：智慧排版（短詞同行、長句換行）、置於下方、同行接續、純英文、純中文。
  - **💡 雙擊文字就地編輯**：雙擊畫面上任何文字即刻轉為輸入框修改，並自動透過 `localStorage` 儲存記憶。
- 📷 **原生 Canvas 2D 專屬繪圖引擎 (超高解析匯出)**
  - 具備 2.5 倍 Retina 高畫質輸出。
  - **📷 複製為圖片 (PNG)**：一鍵複製進系統剪貼簿，可直接在 **Word、PowerPoint、LINE 按 Ctrl+V 貼上**。
  - **💾 另存圖片**：直接下載高畫質 PNG 檔案。
  - 徹底解決 `html2canvas` 遇到 SVG `<text>` 時字體堆疊崩壞的致命缺陷。

---

## 📁 專案目錄結構 (Directory Structure)

```text
Chart-Translation-Skill/
├── .agents/skills/academic-table-auto-translate/
│   ├── SKILL.md                              # Skill 核心規範與決策主指令
│   ├── assets/templates/                     # 雙語 HTML 範本庫
│   │   ├── figure_template.html              # 模型架構圖樣板 (DOM + SVG + Canvas 2D)
│   │   └── table_template.html               # 學術三線表樣板 (Booktabs + 雙擊編輯)
│   ├── references/                           # 專業指引手冊（漸進揭露）
│   │   ├── taiwan_academic_terminology.md    # 臺灣學術慣用語對照指南
│   │   ├── canvas_rendering_guide.md         # Canvas 2D 繪圖引擎與防坑手冊
│   │   └── three_line_table_guide.md         # APA 7th 三線表格排版標準
│   └── scripts/                              # 輔助與驗證工具腳本
│       └── validate_academic_html.py         # 產出 HTML 規格自動合規檢驗工具
├── io/                                       # [不納入 Git] 輸入與輸出工作區
│   ├── input/                                # 放置待處理的原始截圖或文檔
│   └── output/                               # 存放產出的雙語 HTML 與匯出檔案
├── .gitignore                                # Git 忽略清單 (已忽略 io/)
└── README.md                                 # 專案介紹與使用說明手冊
```

---

## 🚀 使用說明 (Usage Instructions)

### 1. 安裝與載入 Skill
將本專案置於支援 Antigravity 或 Agent Skills 的工作目錄下（即 `.agents/skills/academic-table-auto-translate` 目錄結構）。
AI Agent 將自動感應並載入此技能。

### 2. 進行圖表雙語轉換
1. 將欲轉換的外文學術論文圖表（PNG/JPG 截圖）放至 `io/input/` 目錄中。
2. 對 AI 提出提示詞，例如：
   > 「請參考 `io/input/` 中的論文圖表截圖，使用 `academic-table-auto-translate` 技能將其轉換為臺灣繁體中文雙語 HTML，並將成品儲存至 `io/output/`。」
3. AI 將自動分析結構、提取數值與變數、精準翻譯術語，並在 `io/output/` 生成對應的雙語 `.html` 檔案。

### 3. 驗證產出品質 (可選)
可隨時使用內建的自動檢驗腳本，檢查產出的 HTML 是否符合規範：
```bash
python .agents/skills/academic-table-auto-translate/scripts/validate_academic_html.py io/output/your_output.html
```

腳本將自動檢測：
- [x] 是否具備繁體中文與 UTF-8 編碼宣告
- [x] 是否套用標準學術字型（Times New Roman 與 標楷體）
- [x] 是否包含雙擊文字即時編輯功能
- [x] 是否杜絕 SVG `<text>` 搭配 `html2canvas` 的崩壞隱患
- [x] 是否包含複製與下載功能

### 4. 預覽與匯出成果
- 在瀏覽器中開啟產出的 `.html` 檔案。
- 點擊工具列切換所需的語言排版模式。
- 若對翻譯有特定偏好，**直接在畫面上雙擊文字**即可就地修改。
- 點擊 **「📷 複製為圖片 (PNG)」**，即可在論文撰寫軟體（如 Microsoft Word）中直接貼上超高清晰圖表！

---

## 🛠 技術規格標準

| 項目 | 規範標準 |
| :--- | :--- |
| **中文字型** | 優先載入標準標楷體 (`DFKai-SB`, `BiauKai`, `標楷體`) |
| **英文字型 / 數字** | 國際學術期刊標準 `Times New Roman`, serif |
| **統計變數** | *N*, *M*, *SD*, *F*, *p*, *t*, *r*, *R*², *β* 一律維持斜體 |
| **圖片匯出** | 2.5x Retina Canvas 2D 離線繪製或純 DOM 渲染，嚴防模糊或排版錯位 |

---

## 📄 開源授權 (License)

本專案採用 [MIT License](LICENSE) 授權開源。歡迎學術界與開發者自由使用、微調與擴充！
