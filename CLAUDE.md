# CLAUDE.md (歷史專案專屬 AI 協作守則) 🏛️

本專案是「Gemini 的簡單歷史課」自動化網頁生成專案。為確保每次網頁設計更新、文章修訂都符合專案架構並維持優雅排版，請遵循以下 AI 協作守則。

## 🛠️ 專案基礎指令 (Commands)
* **網頁生成**：`python build_html_md.py` (每次修改 Markdown 或 Python 腳本後，必須在本機執行此指令以覆寫 `index.html` 並檢查排版)
* **部署上線**：
  ```bash
  git add .
  git commit -m "發布或優化：[填寫具體變更]"
  git push
  ```

## 🎨 雙軌獨立版本號規範 (Versioning Rules)
本專案採用**雙軌獨立版本號**以區分排版變更與文章修訂，修改時請嚴格遵守：
1. **版面設計版本 (Layout & Design Version)**：
   * **升級時機**：變更 CSS 樣式、JavaScript 互動、網頁結構或底層轉換腳本邏輯時。
   * **修改位置**：`build_html_md.py` 內 HTML 模板中的版權卡片（約第 496 行：`<div>版面設計：X.X</div>`）。
2. **內容版本 (Content Version)**：
   * **升級時機**：修改歷史文章內容、史實勘誤、錯字修正或段落補充時。
   * **修改位置**：`build_html_md.py` 中的 `version_badge` 變數（約第 39 行：`內容版本：X.X`）。

## 📝 程式碼與編輯規範 (Development Guidelines)
1. **編碼前先研究 (Think & Verify)**：
   * 專案內的歷史長文（.md 檔）內容較大，在讀取或修改內文時，必須精確讀取對應的段落，切勿自行胡亂假設史實，亦不可擅自截斷內容。
   * 調整視覺設計時，必須保持**響應式佈局**的完整性：
     * **桌機版 (Width > 1200px)**：三欄式（左目錄 TOC、中主內文、右搜尋與版本卡片）。
     * **平板/窄螢幕 (Width 800px ~ 1200px)**：兩欄式，右側邊欄轉為底部懸浮欄。
     * **手機版 (Width < 800px)**：單欄式，左側目錄隱藏，中間 H2 章節轉為點擊摺疊展開，右側轉為底部懸浮摺疊欄。
2. **精準修改與文繞圖 (Surgical Changes & Image Wrap)**：
   * 修改 `build_html_md.py` 時，應使用精準修改工具，只調整必要代碼，保留原有的 Markdown 預處理邏輯（Word 單行換行修復機制）。
   * 若新增歷史圖片，應將圖片與圖說登錄於 `images` 字典中，並確保圖片套用 `<figure class="image-left">` 浮動樣式以維持高質感文繞圖（Text Wrap）效果。
3. **極簡優先 (Simplicity First)**：
   * 堅持使用 Vanilla JavaScript 與 Vanilla CSS 進行開發，除非使用者要求，否則不引入外部繁重的框架或程式庫。
4. **目標驅動 (Goal-Driven)**：
   * 每次修改完腳本或文章後，必須立刻本機運行 `python build_html_md.py`，驗證生成出的 `index.html` 結構是否完整、標籤是否閉合、搜尋引擎是否運作正常，再向使用者回報。
