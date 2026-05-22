import markdown
import re

with open(r'帝國海洋、金融先驅與當代政治僵局：荷蘭建國史、東印度公司興衰與當代地緣政經轉型研究報告.md', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.split('Source: https://gemini')[0].strip(' -\n')

# Preprocess markdown to fix MS Word style paragraph breaks (single newlines)
lines = text.split('\n')
new_lines = []
for i, line in enumerate(lines):
    new_lines.append(line)
    if i < len(lines) - 1:
        next_line = lines[i+1]
        if line.strip() and next_line.strip():
            # If neither line is a list item, table row, or heading
            if not re.match(r'^[\-\*\#\|]', line.lstrip()) and not re.match(r'^\d+\.', line.lstrip()):
                if not re.match(r'^[\-\*\#\|]', next_line.lstrip()) and not re.match(r'^\d+\.', next_line.lstrip()):
                    new_lines.append('')

text = '\n'.join(new_lines)
html_body = markdown.markdown(text, extensions=['tables', 'toc'])

images = {
    '1.': ('https://upload.wikimedia.org/wikipedia/commons/9/93/Map_of_Seventeen_Provinces_of_Low_Germanie_%28Zeventien_Provincien_der_Nederlanden%29_1626.jpg', '十六世紀的低地十七省地圖，描繪了當時受哈布斯堡王朝統治的疆域'),
    '2.': ('https://upload.wikimedia.org/wikipedia/commons/thumb/8/81/Flag_of_the_Dutch_East_India_Company.svg/960px-Flag_of_the_Dutch_East_India_Company.svg.png', '荷蘭東印度公司（VOC）旗幟，象徵金融革命與全球貿易擴張'),
    '3.': ('https://upload.wikimedia.org/wikipedia/commons/thumb/4/45/Fort_Zeelandia%2C_Anping_District%2C_Tainan_City_%28Taiwan%29.jpg/960px-Fort_Zeelandia%2C_Anping_District%2C_Tainan_City_%28Taiwan%29.jpg', '荷蘭統治台灣時期的熱蘭遮城 (Fort Zeelandia)'),
    '4.': ('https://upload.wikimedia.org/wikipedia/commons/thumb/3/3a/La_ronda_de_noche%2C_por_Rembrandt_van_Rijn.jpg/960px-La_ronda_de_noche%2C_por_Rembrandt_van_Rijn.jpg', '林布蘭名作《夜巡》，荷蘭黃金時代藝術巔峰'),
    '5.': ('https://upload.wikimedia.org/wikipedia/commons/thumb/b/b6/Joannes_van_Deutecum_-_Leo_Belgicus_1650_-_published_by_Claes_Jansz_Visscher_Amsterdam.jpg/960px-Joannes_van_Deutecum_-_Leo_Belgicus_1650_-_published_by_Claes_Jansz_Visscher_Amsterdam.jpg', '低地國家的獅子地圖 (Leo Belgicus)，象徵早期與神聖羅馬帝國的地緣淵源'),
    '6.': ('https://upload.wikimedia.org/wikipedia/commons/thumb/9/9b/Sint_Eustatius_from_ISS.jpg/960px-Sint_Eustatius_from_ISS.jpg', '聖尤斯特歇斯島，美國獨立戰爭期間最重要的軍火走私樞紐'),
    '7.': ('https://upload.wikimedia.org/wikipedia/commons/thumb/7/7a/Johan_Heinrich_Neuman_-_Johan_Rudolf_Thorbecke.jpg/960px-Johan_Heinrich_Neuman_-_Johan_Rudolf_Thorbecke.jpg', '約翰·魯道夫·托爾貝克（1848年憲法起草者，荷蘭民主奠基人）'),
    '8.': ('https://upload.wikimedia.org/wikipedia/commons/thumb/e/e0/Rotterdam_na_het_bombardement_14_mei_1940.jpg/800px-Rotterdam_na_het_bombardement_14_mei_1940.jpg', '1940年遭德軍殘酷轟炸摧毀的鹿特丹'),
    '9.': ('https://upload.wikimedia.org/wikipedia/commons/thumb/f/f3/Friedenspalast_Den_Haag_%28100MP%29.jpg/960px-Friedenspalast_Den_Haag_%28100MP%29.jpg', '位於海牙的和平宮，象徵當代荷蘭作為全球國際司法之都'),
    '10.': ('https://upload.wikimedia.org/wikipedia/commons/thumb/0/02/Den_Haag_Binnenhof_02.jpg/960px-Den_Haag_Binnenhof_02.jpg', '荷蘭國會大廈 (Binnenhof)，象徵高度協商與妥協的政治文化')
}

map_img = '<figure class="image-left" style="width: 38%; margin-bottom: 20px;"><img src="https://upload.wikimedia.org/wikipedia/commons/thumb/6/63/Seven_United_Netherlands_Janssonius_1658.jpg/960px-Seven_United_Netherlands_Janssonius_1658.jpg" alt="1658 Map"><figcaption class="caption">1658年聯省共和國地圖，清晰可見當時的須德海與低地國錯綜複雜的水路地貌</figcaption></figure>\\n'
html_body = re.sub(r'(<h1.*?>.*?</h1>)', r'\1\n' + map_img, html_body, count=1)

for prefix, (url, caption) in images.items():
    pattern = r'(<h2.*?>' + re.escape(prefix) + r'.*?</h2>)'
    img_html = f'\n<figure class="image-left"><img src="{url}" alt="{caption}"><figcaption class="caption">{caption}</figcaption></figure>\n'
    html_body = re.sub(pattern, r'\1' + img_html, html_body, count=1)

final_html = f'''<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>帝國海洋、金融先驅與當代政治僵局：荷蘭建國史</title>
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@400;700&family=Inter:wght@400;600&display=swap" rel="stylesheet">
    <style>
        :root {{ --primary-color: #0055A4; --secondary-color: #AE1C28; --bg-color: #f4f7f6; --text-color: #2d3748; --card-bg: #ffffff; --border-color: #e2e8f0; }}
        body {{ font-family: 'Inter', 'Noto Sans TC', sans-serif; background-color: var(--bg-color); color: var(--text-color); line-height: 1.8; margin: 0; padding: 0; }}
        
        /* Banner Styles */
        .site-banner {{
            width: 100%;
            height: 300px;
            background: linear-gradient(rgba(10, 25, 47, 0.75), rgba(10, 25, 47, 0.9)), url('history_banner_bg.png');
            background-size: cover;
            background-position: center;
            display: flex;
            align-items: center;
            justify-content: center;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            position: relative;
            overflow: hidden;
        }}
        .banner-content {{
            text-align: center;
            color: #ffffff;
            animation: fadeIn 1.5s ease-in-out;
            z-index: 1;
        }}
        .banner-subtitle {{
            font-size: 1.2rem;
            letter-spacing: 6px;
            text-transform: uppercase;
            color: #cbd5e0;
            margin-bottom: 12px;
            font-weight: 600;
        }}
        .banner-title {{
            font-size: 3.5rem;
            font-weight: 700;
            text-shadow: 2px 2px 10px rgba(0,0,0,0.6);
            margin: 0;
            background: linear-gradient(45deg, #fbd38d, #ffffff);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}
        @keyframes fadeIn {{
            from {{ opacity: 0; transform: translateY(20px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}

        /* Three column layout */
        .layout {{
            display: grid;
            grid-template-columns: 280px 1fr 300px;
            gap: 30px;
            max-width: 1600px;
            margin: 0 auto;
            padding: 20px;
            min-height: 100vh;
        }}
        
        @media (max-width: 1200px) {{
            .layout {{ grid-template-columns: 250px 1fr; }}
            .sidebar-right {{ display: none; }}
        }}
        @media (max-width: 800px) {{
            .layout {{ grid-template-columns: 1fr; }}
            .sidebar-left {{ display: none; }}
        }}

        /* Sidebars */
        .sidebar-left, .sidebar-right {{
            background: var(--card-bg);
            border-radius: 12px;
            padding: 20px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.03);
            position: sticky;
            top: 20px;
            height: calc(100vh - 40px);
            overflow-y: auto;
        }}
        
        .sidebar-title {{
            font-size: 1.2rem;
            font-weight: 700;
            color: var(--primary-color);
            margin-bottom: 20px;
            border-bottom: 2px solid var(--primary-color);
            padding-bottom: 10px;
        }}

        /* Table of Contents */
        .toc-item {{
            display: block;
            color: #4a5568;
            text-decoration: none;
            padding: 6px 0;
            font-size: 0.95rem;
            border-bottom: 1px solid var(--border-color);
            transition: all 0.2s;
        }}
        .toc-item:hover {{ color: var(--primary-color); padding-left: 5px; }}
        .toc-h3 {{ padding-left: 15px; font-size: 0.85rem; color: #718096; border-bottom: none; }}

        /* Main Content */
        .content-middle {{
            background-color: var(--card-bg);
            padding: 40px 60px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.05);
            border-radius: 12px;
        }}

        /* Search Box */
        .search-box input {{
            width: 100%;
            padding: 12px 15px;
            border: 1px solid var(--border-color);
            border-radius: 8px;
            font-size: 1rem;
            margin-bottom: 20px;
            box-sizing: border-box;
            outline: none;
            transition: border-color 0.2s;
        }}
        .search-box input:focus {{ border-color: var(--primary-color); }}
        
        .search-result-item {{
            background: #f7fafc;
            padding: 12px;
            border-radius: 6px;
            margin-bottom: 10px;
            font-size: 0.85rem;
            cursor: pointer;
            border-left: 3px solid var(--primary-color);
            transition: background 0.2s;
        }}
        .search-result-item:hover {{ background: #edf2f7; }}
        mark {{ background-color: #fbd38d; color: #000; padding: 0 2px; border-radius: 2px; }}

        /* Typography */
        h1 {{ font-size: 2.2rem; color: var(--primary-color); text-align: center; border-bottom: 3px solid var(--secondary-color); padding-bottom: 20px; margin-bottom: 30px; margin-top: 0; clear: both; }}
        h2 {{ font-size: 1.6rem; color: var(--primary-color); border-left: 5px solid var(--secondary-color); padding-left: 15px; margin-top: 50px; scroll-margin-top: 40px; clear: both; }}
        h3 {{ font-size: 1.3rem; color: #4a5568; margin-top: 30px; scroll-margin-top: 40px; }}
        p {{ font-size: 1.05rem; margin-bottom: 20px; text-align: justify; }}
        
        figure.image-left {{
            float: left;
            width: 25%;
            margin: 10px 25px 15px 0;
            background: var(--card-bg);
            padding: 10px;
            border-radius: 8px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.08);
            box-sizing: border-box;
        }}
        figure.image-left img {{
            width: 100%;
            height: auto;
            border-radius: 6px;
            display: block;
        }}
        figure.image-left figcaption {{
            text-align: center;
            font-size: 0.85rem;
            color: #718096;
            margin-top: 10px;
            line-height: 1.4;
        }}

        table {{ width: 100%; border-collapse: collapse; margin: 30px 0; font-size: 0.95rem; box-shadow: 0 4px 6px rgba(0,0,0,0.05); clear: both; }}
        th, td {{ padding: 12px; text-align: left; border: 1px solid var(--border-color); }}
        th {{ background-color: var(--primary-color); color: white; }}
        tr:nth-child(even) {{ background-color: #f7fafc; }}
        ul, ol {{ font-size: 1.05rem; line-height: 1.8; }}
        a {{ color: var(--primary-color); text-decoration: none; }}
        a:hover {{ text-decoration: underline; }}
    </style>
</head>
<body>

<!-- Beautiful Hero Banner -->
<div class="site-banner">
    <div class="banner-content">
        <div class="banner-subtitle">Gemini's History Series</div>
        <div class="banner-title">Gemini 的簡單歷史課</div>
    </div>
</div>

<div class="layout">
    <!-- Left Sidebar: TOC -->
    <aside class="sidebar-left">
        <div class="sidebar-title">章節目錄</div>
        <div id="toc"></div>
    </aside>

    <!-- Middle Column: Main Content -->
    <main class="content-middle" id="main-content">
        {html_body}
    </main>

    <!-- Right Sidebar: Search -->
    <aside class="sidebar-right">
        <div class="sidebar-title">關鍵字查詢</div>
        <div class="search-box">
            <input type="text" id="searchInput" placeholder="輸入關鍵字 (例如: VOC, 威廉)...">
            <div id="searchResults">
                <div style="color:#a0aec0; text-align:center; margin-top:30px; font-size: 0.9rem;">
                    輸入關鍵字以尋找內文段落
                </div>
            </div>
        </div>
        
        <div style="margin-top: 40px; padding: 15px; background: #edf2f7; border-radius: 8px; font-size: 0.85rem; color: #4a5568; text-align: center; border-top: 3px solid var(--primary-color);">
            <div style="font-weight: 600; margin-bottom: 8px; color: var(--primary-color);">📝 版本宣告</div>
            <div style="font-weight: 500;">版本：1.0</div>
            <div style="margin-bottom: 8px; color: #718096;">發布日期：2026-05-23</div>
            <hr style="border: none; border-top: 1px dashed #cbd5e0; margin: 10px 0;">
            本文內容由 Gemini 生成<br>
            Antigravity 設計網頁
        </div>
    </aside>
</div>

<script>
    // 1. Generate Table of Contents
    const tocContainer = document.getElementById('toc');
    const headings = document.querySelectorAll('.content-middle h2, .content-middle h3');
    headings.forEach((h, index) => {{
        if (!h.id) h.id = 'heading-' + index;
        const link = document.createElement('a');
        link.href = '#' + h.id;
        link.innerText = h.innerText;
        link.className = 'toc-item toc-' + h.tagName.toLowerCase();
        tocContainer.appendChild(link);
    }});

    // 2. Keyword Search Functionality
    const searchInput = document.getElementById('searchInput');
    const searchResults = document.getElementById('searchResults');
    const content = document.getElementById('main-content');
    const searchableElements = content.querySelectorAll('p, h2, h3, li, td');

    searchInput.addEventListener('input', (e) => {{
        const keyword = e.target.value.trim().toLowerCase();
        searchResults.innerHTML = '';
        
        if (!keyword) {{
            searchResults.innerHTML = '<div style="color:#a0aec0; text-align:center; margin-top:30px; font-size: 0.9rem;">輸入關鍵字以尋找內文段落</div>';
            return;
        }}

        let count = 0;
        searchableElements.forEach((el, index) => {{
            const text = el.innerText;
            if (text.toLowerCase().includes(keyword)) {{
                count++;
                if (count > 50) return; // limit results to prevent lag
                
                if (!el.id) el.id = 'search-match-' + index;
                
                const res = document.createElement('div');
                res.className = 'search-result-item';
                
                const idx = text.toLowerCase().indexOf(keyword);
                const start = Math.max(0, idx - 25);
                const end = Math.min(text.length, idx + 25);
                let snippet = text.substring(start, end);
                if (start > 0) snippet = '...' + snippet;
                if (end < text.length) snippet = snippet + '...';
                
                // Highlight keyword in snippet (case-insensitive)
                const regex = new RegExp('(' + keyword + ')', 'gi');
                snippet = snippet.replace(regex, '<mark>$1</mark>');
                
                res.innerHTML = snippet;
                res.onclick = () => {{
                    el.scrollIntoView({{behavior: 'smooth', block: 'center'}});
                    const originalBg = el.style.backgroundColor;
                    el.style.transition = 'background-color 0.3s';
                    el.style.backgroundColor = '#fbd38d';
                    setTimeout(() => {{ el.style.backgroundColor = originalBg; }}, 2000);
                }};
                searchResults.appendChild(res);
            }}
        }});
        
        if (count === 0) {{
            searchResults.innerHTML = '<div style="color:#e53e3e; text-align:center; margin-top:30px; font-size: 0.95rem;">找不到包含「' + e.target.value + '」的內容</div>';
        }} else if (count > 50) {{
            const note = document.createElement('div');
            note.style = "color:#718096; text-align:center; margin-top:10px; font-size: 0.8rem;";
            note.innerText = `找到超過 50 筆結果，僅顯示前 50 筆`;
            searchResults.appendChild(note);
        }}
    }});
</script>

</body>
</html>'''

with open(r'index.html', 'w', encoding='utf-8') as f:
    f.write(final_html)
