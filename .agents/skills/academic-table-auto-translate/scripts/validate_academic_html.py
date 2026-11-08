#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
學術圖表與雙語 HTML 規範驗證工具 (Academic HTML Validator)

用途：
  自動檢測產出的雙語學術 HTML 檔案是否符合本技能所規定的鐵律與規範：
  1. 包含雙語字型 (Times New Roman 與 標楷體 / DFKai-SB)
  2. 包含雙擊文字即時編輯機制 (.editable-text 與 data-key)
  3. 工具列規範（包含複製圖片、另存圖片、重設文字等按鈕）
  4. 杜絕致命錯誤：若使用 html2canvas，禁止在 SVG 內使用 <text> 標籤
  5. 語系與編碼宣告 (UTF-8, zh-Hant)
"""

import sys
import os
import re
from pathlib import Path

# 確保在 Windows 控制台輸出中文與符號時不發生編碼錯誤
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

def validate_academic_html(file_path: str) -> dict:
    path = Path(file_path)
    if not path.is_file():
        return {"file": file_path, "success": False, "errors": [f"檔案不存在: {file_path}"], "warnings": []}

    content = path.read_text(encoding="utf-8", errors="ignore")
    errors = []
    warnings = []
    checks_passed = []

    # 1. 編碼與語系
    if 'charset="UTF-8"' in content or "charset='UTF-8'" in content or 'charset="utf-8"' in content:
        checks_passed.append("已設定 UTF-8 編碼")
    else:
        errors.append("未找到 UTF-8 字元編碼宣告 (<meta charset=\"UTF-8\">)")

    if 'lang="zh-Hant"' in content or 'lang="zh-TW"' in content:
        checks_passed.append("語系宣告為繁體中文 (zh-Hant / zh-TW)")
    else:
        warnings.append("建議 <html> 標籤包含 lang=\"zh-Hant\" 語系宣告")

    # 2. 字型設定
    has_times = "Times New Roman" in content
    has_kai = any(font in content for font in ["DFKai-SB", "BiauKai", "標楷體", "KaiTi"])
    if has_times and has_kai:
        checks_passed.append("已設定標準學術字型 (Times New Roman + 標楷體)")
    else:
        if not has_times:
            warnings.append("未檢測到英文標準字型 Times New Roman")
        if not has_kai:
            warnings.append("未檢測到中文學術字型 標楷體 (DFKai-SB / BiauKai)")

    # 3. 雙擊文字編輯機制
    if ".editable-text" in content and "data-key=" in content:
        checks_passed.append("具備就地雙擊編輯機制 (.editable-text, data-key)")
    else:
        errors.append("缺少雙擊就地編輯支援：未發現 .editable-text 類別或 data-key 屬性")

    # 4. 關鍵錯誤檢測：html2canvas + SVG <text>
    has_html2canvas = "html2canvas" in content
    has_svg_text = bool(re.search(r"<svg[\s\S]*?<text[\s\S]*?</svg>", content, re.IGNORECASE))
    if has_html2canvas and has_svg_text:
        errors.append("致命錯誤：檢測到使用 html2canvas 且 SVG 內部含有 <text> 標籤！這會導致文字嚴重堆疊排版崩毀。請改用 Canvas 2D 或 HTML DOM 卡片。")
    elif not has_svg_text:
        checks_passed.append("SVG 規範檢查通過（未在 SVG 中使用 <text> 搭配截圖庫）")

    # 5. 操作按鈕與功能檢測
    if "copy" in content.lower() and "image" in content.lower():
        checks_passed.append("包含複製為圖片功能")
    else:
        warnings.append("建議提供一鍵「複製為圖片 (PNG)」按鈕")

    if "download" in content.lower() or "另存圖片" in content:
        checks_passed.append("包含另存圖片功能")
    else:
        warnings.append("建議提供「另存圖片」功能")

    success = len(errors) == 0
    return {
        "file": str(path),
        "success": success,
        "passed": checks_passed,
        "warnings": warnings,
        "errors": errors
    }

def print_report(res: dict):
    print("=" * 60)
    print(f"檔案: {res['file']}")
    print(f"結果: {'[通過 PASS]' if res['success'] else '[失敗 FAIL]'}")
    print("-" * 60)
    if res["passed"]:
        print("通過檢查項目:")
        for p in res["passed"]:
            print(f"  [OK] {p}")
    if res["warnings"]:
        print("\n警告提醒 (建議優化):")
        for w in res["warnings"]:
            print(f"  [WARN] {w}")
    if res["errors"]:
        print("\n錯誤清單 (必須修正):")
        for e in res["errors"]:
            print(f"  [ERR] {e}")
    print("=" * 60)

if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "."
    target_path = Path(target)
    
    files_to_check = []
    if target_path.is_file() and target_path.suffix.lower() == ".html":
        files_to_check.append(target_path)
    elif target_path.is_dir():
        files_to_check.extend(list(target_path.rglob("*.html")))

    if not files_to_check:
        print(f"未找到可驗證的 HTML 檔案: {target}")
        sys.exit(0)

    all_success = True
    for f in files_to_check:
        report = validate_academic_html(str(f))
        print_report(report)
        if not report["success"]:
            all_success = False

    sys.exit(0 if all_success else 1)
