import markdown
import re
import os

# Helper to process and format a markdown lesson
def process_markdown(file_path, image_replacements, content_version, main_img_html=None):
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()

    # Clean Voyager/Gemini footer source info if present
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

    # Add content version badge
    version_badge = f'<div style="text-align: center; color: #718096; margin-top: -15px; margin-bottom: 25px; font-size: 0.95rem; font-weight: 600; display: flex; align-items: center; justify-content: center; gap: 8px;"><span style="background-color: #ebf8ff; color: #2b6cb0; padding: 3px 8px; border-radius: 4px; font-size: 0.8rem; border: 1px solid #bee3f8;">內容版本：{content_version}</span></div>\n'

    # Insert version badge and main image under first H1
    header_insert = version_badge
    if main_img_html:
        header_insert += main_img_html

    html_body = re.sub(r'(<h1.*?>.*?</h1>)', r'\1\n' + header_insert, html_body, count=1)

    # Substitute specific headings with images for high-end text wrap
    for pattern, url, caption in image_replacements:
        img_html = f'\n<figure class="image-left"><img src="{url}" alt="{caption}" loading="lazy"><figcaption class="caption">{caption}</figcaption></figure>\n'
        html_body = re.sub(pattern, r'\1' + img_html, html_body, count=1)

    return html_body

# Page 1 (Holland) Config
file_p1 = r'帝國海洋、金融先驅與當代政治僵局：荷蘭建國史、東印度公司興衰與當代地緣政經轉型研究報告.md'
map_p1 = '<figure class="image-left" style="width: 38%; margin-bottom: 20px;"><img src="images/img_12_960px-Seven_United_Netherlands_Janssonius_1658.jpg" alt="1658 Map" loading="lazy"><figcaption class="caption">1658年聯省共和國地圖，清晰可見當時的須德海與低地國錯綜複雜的水路地貌</figcaption></figure>\n'
images_p1 = [
    (r'(<h2.*?>1\..*?</h2>)', 'images/img_00_Map_of_Seventeen_Provinces_of_Low_German.jpg', '十六世紀的低地十七省地圖，描繪了當時受哈布斯堡王朝統治的疆域'),
    (r'(<h2.*?>2\..*?</h2>)', 'images/img_16_960px-Flag_of_the_Dutch_East_India_Company.svg.png', '荷蘭東印度公司（VOC）旗幟，象徵金融革命與全球貿易擴張'),
    (r'(<h2.*?>3\..*?</h2>)', 'images/img_14_960px-Fort_Zeelandia__Anping_District__T.jpg', '荷蘭統治台灣時期的熱蘭遮城 (Fort Zeelandia)'),
    (r'(<h2.*?>4\..*?</h2>)', 'images/img_15_960px-La_ronda_de_noche__por_Rembrandt_v.jpg', '林布蘭名作《夜巡》，荷蘭黃金時代藝術巔峰'),
    (r'(<h2.*?>5\..*?</h2>)', 'images/img_03_960px-Joannes_van_Deutecum_-_Leo_Belgicu.jpg', '低地國家的獅子地圖 (Leo Belgicus)，象徵早期與神聖羅馬帝國的地緣淵源'),
    (r'(<h2.*?>6\..*?</h2>)', 'images/img_08_960px-Sint_Eustatius_from_ISS.jpg', '聖尤斯特歇斯島，美國獨立戰爭期間最重要的軍火走私樞紐'),
    (r'(<h2.*?>7\..*?</h2>)', 'images/img_07_960px-Johan_Heinrich_Neuman_-_Johan_Rudo.jpg', '約翰·魯道夫·托爾貝克（1848年憲法起草者，荷蘭民主奠基人）'),
    (r'(<h2.*?>8\..*?</h2>)', 'images/img_05_960px-Bundesarchiv_Bild_146-2005-0003__R.jpg', '1940年遭德軍殘酷轟炸摧毀的鹿特丹'),
    (r'(<h2.*?>9\..*?</h2>)', 'images/img_09_960px-Friedenspalast_Den_Haag__100MP_.jpg', '位於海牙的和平宮，象徵當代荷蘭作為全球國際司法之都'),
    (r'(<h2.*?>10\..*?</h2>)', 'images/img_01_960px-Den_Haag_Binnenhof_02.jpg', '荷蘭國會大廈 (Binnenhof)，象徵高度協商與妥協的政治文化')
]

# Page 2 (USA) Config
file_p2 = r'第一階段：三個世界的交會與前哥倫布時期的美洲（1607年以前）.md'
map_p2 = '<figure class="image-left" style="width: 38%; margin-bottom: 20px;"><img src="images/img_10_960px-Cahokia_Monks_Mound.jpg" alt="Cahokia Mounds" loading="lazy"><figcaption class="caption">卡霍基亞莫恩克斯土丘（Monks Mound）遠眺，前哥倫布時期繁榮的密西西比河流域社會核心遺跡</figcaption></figure>\n'
images_p2 = [
    (r'(<h2.*?>一、.*?</h2>)', 'images/img_04_Cliff_Palace_-_Mesa_Verde_National_Park.jpg', '梅薩維德國家公園的懸崖宮殿，展現普韋布洛人高超的石造建築技術'),
    (r'(<h2.*?>二、.*?</h2>)', 'images/img_06_Caravela_Redonda.jpg', '大航海時代的葡萄牙輕快帆船（Caravel），支撐起遠洋探索的技術革命'),
    (r'(<h2.*?>三、.*?</h2>)', 'images/img_02_Landing_of_Columbus.jpg', '哥倫布登陸美洲想像圖，開啟了改變全球生態與人類社會結構的哥倫布大交換'),
    (r'(<h3.*?>2\..*?</h3>)', 'images/img_17_960px-Castillo_de_San_Marcos_Fort_Panorama.jpg', '位於佛羅里達的聖馬科斯城堡，北美洲最古老的歐洲磚石要塞，象徵西班牙的早期霸權'),
    (r'(<h3.*?>3\..*?</h3>)', 'images/img_11_John_White_-_La_Virginea_Pars__map_of_th.jpg', '約翰·懷特約於1585年繪製的北美海岸地圖《La Virginea Pars》，記錄了早期對北美地理的探索與拓荒'),
    (r'(<h3.*?>4\..*?</h3>)', 'images/img_13_960px-Elizabeth_I__Armada_Portrait_.jpg', '伊麗莎白一世著名的「無敵艦隊畫像」（Armada Portrait），象徵擊敗西班牙霸權的地緣政治重大轉折點')
]

# Page 3 (Hussite Wars) Config
file_p3 = r'信仰衝突、軍事變革與波希米亞國家認同：胡斯戰爭的歷史脈絡、演進特徵與深遠影響研究報告.md'
map_p3 = '<figure class="image-left" style="width: 38%; margin-bottom: 20px;"><img src="images/hussite_wars_main.png" alt="Hussite Wars" loading="lazy"><figcaption class="caption">捷克歷史藝術家 Luděk Marold 著名巨作《利帕尼戰役全景圖》（Maroldovo panorama bitvy u Lipan），生動重現了這場終結激進派的史詩決戰</figcaption></figure>\n'
images_p3 = [
    (r'(<h2.*?>一、.*?</h2>)', 'images/jan_hus_preaching.png', '1563年布拉格印製的《胡斯講道集》（Postilla）中極具歷史意義的木刻版畫，記錄了揚·胡斯向波希米亞平民大眾宣教的經典場景'),
    (r'(<\/p>\s*<p>1414年，神聖羅馬帝國國王西吉斯蒙德)', 'images/jan_hus_execution.jpg', '歷史文獻插圖：上方描繪揚·胡斯在康斯坦茨被戴上寫有「異端首領」主教冠押赴火刑，下方描繪信徒用手推車收集其骨灰撒入萊茵河以防遺骨成為聖物，出自著名的《康斯坦茨公會議編年史》（Chronik des Konstanzer Konzils）'),
    (r'(<h2.*?>三、.*?</h2>)', 'images/hussite_crusade_battle.png', '源自15世紀末捷克國寶級手稿《耶拿法典》（Jena Codex）的著名插圖，展現高舉聖杯紅旗前仆後繼、行軍禦敵的胡斯派戰士們'),
    (r'(<h2.*?>四、.*?</h2>)', 'images/hussite_wagenburg.png', '歷史文獻中記載的經典「戰車壘」（Wagenburg）野戰工事與早期火炮協同防禦防線的精細還原圖')
]

print("Processing Page 1 (Holland)...")
html_body_p1 = process_markdown(file_p1, images_p1, "1.1", map_p1)

print("Processing Page 2 (USA)...")
html_body_p2 = process_markdown(file_p2, images_p2, "1.0", map_p2)

print("Processing Page 3 (Hussite)...")
html_body_p3 = process_markdown(file_p3, images_p3, "1.0", map_p3)

# Full Portal HTML Template
portal_template = """<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="google-site-verification" content="lueGudczLbvVhtRPh-JU6w8b3eu_yu5XCguU6RvfMxY" />
    <title>Gemini 的歷史課 - 三課堂動態門戶</title>
    <meta name="description" content="Gemini的簡單歷史課，帶你深入了解荷蘭建國史與東印度公司、前哥倫布時期美洲歷史，以及波希米亞宗教衝突與胡斯戰爭。專為歷史專題研究與報告打造的精緻長文。">
    <meta name="keywords" content="歷史, 歷史課, 荷蘭史, 東印度公司, 美國史, 宗教戰爭, 胡斯戰爭, 揚胡斯, 捷克歷史, 大航海時代, Gemini, 歷史專題">
    <meta property="og:title" content="Gemini 的歷史課 - 三課堂動態門戶">
    <meta property="og:description" content="Gemini的簡單歷史課，帶你深入了解荷蘭建國史、東印度公司、前哥倫布時期美洲歷史，以及波希米亞宗教衝突與胡斯戰爭。">
    <meta property="og:type" content="website">
    <meta property="og:url" content="https://ludwicia.github.io/gemini-history-lesson/">
    <meta property="og:image" content="https://ludwicia.github.io/gemini-history-lesson/history_banner_bg.png">
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@400;600;700&family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
    <style>
        :root { 
            --primary-color: #0055A4; 
            --secondary-color: #AE1C28; 
            --bg-color: #f4f7f6; 
            --text-color: #2d3748; 
            --card-bg: #ffffff; 
            --border-color: #e2e8f0; 
        }
        .desktop-only {
            display: inline;
        }
        body { 
            font-family: 'Inter', 'Noto Sans TC', sans-serif; 
            background-color: var(--bg-color); 
            color: var(--text-color); 
            line-height: 1.8; 
            margin: 0; 
            padding: 0; 
        }
        
        /* Premium Sticky Navigation Bar */
        .top-nav {
            position: sticky;
            top: 0;
            width: 100%;
            height: 70px;
            background: rgba(255, 255, 255, 0.85);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            border-bottom: 1px solid rgba(226, 232, 240, 0.8);
            z-index: 1000;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.04);
            box-sizing: border-box;
        }
        .nav-container {
            max-width: 1600px;
            height: 100%;
            margin: 0 auto;
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 0 30px;
            box-sizing: border-box;
        }
        .nav-brand {
            font-size: 1.3rem;
            font-weight: 700;
            color: var(--primary-color);
            text-decoration: none;
            display: flex;
            align-items: center;
            gap: 10px;
            letter-spacing: 1px;
        }
        .nav-links {
            display: flex;
            gap: 12px;
        }
        .nav-tab-btn {
            background: transparent;
            border: 2px solid transparent;
            border-radius: 8px;
            color: #4a5568;
            padding: 8px 16px;
            font-size: 0.95rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            outline: none;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        .nav-tab-btn:hover {
            color: var(--primary-color);
            background: rgba(0, 85, 164, 0.05);
        }
        .nav-tab-btn.active {
            color: white;
            background: var(--primary-color);
            border-color: var(--primary-color);
            box-shadow: 0 4px 12px rgba(0, 85, 164, 0.2);
        }
        
        /* Banner Styles */
        .site-banner {
            width: 100%;
            height: 260px;
            background: linear-gradient(rgba(10, 25, 47, 0.75), rgba(10, 25, 47, 0.9)), url('history_banner_bg.png');
            background-size: cover;
            background-position: center;
            display: flex;
            align-items: center;
            justify-content: center;
            box-shadow: 0 10px 30px rgba(0,0,0,0.15);
            position: relative;
            overflow: hidden;
        }
        .banner-content {
            text-align: center;
            color: #ffffff;
            animation: fadeIn 1.2s ease-in-out;
            z-index: 1;
        }
        .banner-subtitle {
            font-size: 1.1rem;
            letter-spacing: 6px;
            text-transform: uppercase;
            color: #cbd5e0;
            margin-bottom: 12px;
            font-weight: 600;
        }
        .banner-title {
            font-size: 3rem;
            font-weight: 700;
            text-shadow: 2px 2px 10px rgba(0,0,0,0.5);
            margin: 0;
            background: linear-gradient(45deg, #fbd38d, #ffffff);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(15px); }
            to { opacity: 1; transform: translateY(0); }
        }

        /* Three column layout */
        .layout {
            display: grid;
            grid-template-columns: 280px 1fr 300px;
            gap: 30px;
            max-width: 1600px;
            margin: 0 auto;
            padding: 30px 20px;
            min-height: 100vh;
            box-sizing: border-box;
        }

        /* Sidebars */
        .sidebar-left, .sidebar-right {
            background: var(--card-bg);
            border-radius: 12px;
            padding: 20px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.02);
            position: sticky;
            top: 100px;
            height: calc(100vh - 130px);
            overflow-y: auto;
            box-sizing: border-box;
            border: 1px solid var(--border-color);
        }
        
        .footer-header {
            display: none; /* Hidden on desktop */
        }
        
        #searchResults {
            max-height: calc(100vh - 280px);
            overflow-y: auto;
            margin-top: 10px;
        }
        
        .sidebar-title {
            font-size: 1.15rem;
            font-weight: 700;
            color: var(--primary-color);
            margin-bottom: 15px;
            border-bottom: 2px solid var(--primary-color);
            padding-bottom: 8px;
        }

        /* Table of Contents */
        .toc-item {
            display: block;
            color: #4a5568;
            text-decoration: none;
            padding: 6px 0;
            font-size: 0.92rem;
            border-bottom: 1px solid var(--border-color);
            transition: all 0.2s;
            line-height: 1.5;
        }
        .toc-item:hover { color: var(--primary-color); padding-left: 5px; }
        .toc-h3 { padding-left: 15px; font-size: 0.83rem; color: #718096; border-bottom: none; }

        /* Main Content */
        .content-middle {
            background-color: var(--card-bg);
            padding: 40px 50px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.03);
            border-radius: 12px;
            border: 1px solid var(--border-color);
            box-sizing: border-box;
            min-width: 0; /* Prevents flexbox/grid blowout */
        }
        
        .course-page {
            animation: contentFadeIn 0.4s ease-in-out;
        }
        @keyframes contentFadeIn {
            from { opacity: 0; transform: translateY(8px); }
            to { opacity: 1; transform: translateY(0); }
        }

        /* Search Box */
        .search-box input {
            width: 100%;
            padding: 10px 14px;
            border: 1px solid var(--border-color);
            border-radius: 8px;
            font-size: 0.95rem;
            margin-bottom: 15px;
            box-sizing: border-box;
            outline: none;
            transition: border-color 0.2s;
        }
        .search-box input:focus { border-color: var(--primary-color); }
        
        .search-result-item {
            background: #f7fafc;
            padding: 10px 12px;
            border-radius: 6px;
            margin-bottom: 8px;
            font-size: 0.83rem;
            cursor: pointer;
            border-left: 3px solid var(--primary-color);
            transition: background 0.2s;
            line-height: 1.5;
        }
        .search-result-item:hover { background: #edf2f7; }
        mark { background-color: #fbd38d; color: #000; padding: 0 2px; border-radius: 2px; }

        /* Typography */
        h1 { font-size: 2.1rem; color: var(--primary-color); text-align: center; border-bottom: 3px solid var(--secondary-color); padding-bottom: 20px; margin-bottom: 30px; margin-top: 0; clear: both; line-height: 1.4; }
        h2 { font-size: 1.55rem; color: var(--primary-color); border-left: 5px solid var(--secondary-color); padding-left: 15px; margin-top: 45px; scroll-margin-top: 90px; clear: both; line-height: 1.4; }
        h3 { font-size: 1.25rem; color: #4a5568; margin-top: 25px; scroll-margin-top: 90px; line-height: 1.4; }
        p { font-size: 1.02rem; margin-bottom: 20px; text-align: justify; }
        
        figure.image-left {
            float: left;
            width: 35%;
            margin: 10px 25px 15px 0;
            background: var(--card-bg);
            padding: 10px;
            border-radius: 8px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.06);
            box-sizing: border-box;
            border: 1px solid var(--border-color);
        }
        figure.image-left img {
            width: 100%;
            height: auto;
            border-radius: 6px;
            display: block;
        }
        figure.image-left figcaption {
            text-align: center;
            font-size: 0.83rem;
            color: #718096;
            margin-top: 10px;
            line-height: 1.4;
        }

        table { width: 100%; border-collapse: collapse; margin: 30px 0; font-size: 0.92rem; box-shadow: 0 4px 6px rgba(0,0,0,0.02); clear: both; }
        th, td { padding: 10px 12px; text-align: left; border: 1px solid var(--border-color); }
        th { background-color: var(--primary-color); color: white; }
        tr:nth-child(even) { background-color: #f7fafc; }
        ul, ol { font-size: 1.02rem; line-height: 1.8; }
        a { color: var(--primary-color); text-decoration: none; }
        a:hover { text-decoration: underline; }

        /* ===== Responsive Media Queries ===== */
        @media (max-width: 1200px) {
            .layout { grid-template-columns: 280px 1fr; }
            
            /* Sidebar transitions to floating bottom card */
            .sidebar-right {
                position: fixed;
                bottom: 0;
                left: 0;
                right: 0;
                width: 100%;
                height: 280px;
                top: auto;
                background: rgba(255, 255, 255, 0.96);
                backdrop-filter: blur(10px);
                -webkit-backdrop-filter: blur(10px);
                box-shadow: 0 -10px 30px rgba(0,0,0,0.12);
                border-top: 3px solid var(--primary-color);
                border-radius: 16px 16px 0 0;
                z-index: 1000;
                margin: 0;
                padding: 0;
                overflow: hidden;
                display: flex;
                flex-direction: column;
                transition: transform 0.35s cubic-bezier(0.4, 0, 0.2, 1);
            }
            
            /* Collapsed State */
            .sidebar-right.collapsed-footer {
                transform: translateY(calc(100% - 48px));
            }
            
            /* Show controls header */
            .footer-header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                min-height: 48px;
                height: 48px;
                background: linear-gradient(135deg, var(--primary-color), #0a252f);
                color: white;
                padding: 0 20px;
                cursor: pointer;
                user-select: none;
                flex-shrink: 0;
            }
            
            .footer-header-title {
                font-weight: 700;
                font-size: 0.92rem;
                letter-spacing: 1px;
            }
            
            .footer-toggle-btn {
                background: rgba(255, 255, 255, 0.2);
                border: none;
                color: white;
                padding: 4px 12px;
                border-radius: 20px;
                font-size: 0.78rem;
                font-weight: 600;
                cursor: pointer;
                transition: background 0.2s;
            }
            
            .footer-toggle-btn:hover {
                background: rgba(255, 255, 255, 0.3);
            }
            
            /* Grid inside floating footer */
            .footer-main-content {
                display: grid;
                grid-template-columns: 260px 1fr 240px;
                gap: 25px;
                padding: 20px 25px;
                height: calc(100% - 48px);
                box-sizing: border-box;
                overflow: hidden;
            }
            
            .footer-search-col {
                display: flex;
                flex-direction: column;
            }
            
            .footer-search-col .sidebar-title {
                margin-top: 0;
                margin-bottom: 12px;
                font-size: 1.05rem;
                border-bottom: 2px solid var(--primary-color);
                padding-bottom: 6px;
            }
            
            .footer-search-col .search-box input {
                margin-bottom: 0;
            }
            
            .footer-results-col {
                display: flex;
                flex-direction: column;
                overflow: hidden;
                border-left: 1px solid var(--border-color);
                border-right: 1px solid var(--border-color);
                padding: 0 20px;
            }
            
            #searchResults {
                flex: 1;
                max-height: 100%;
                overflow-y: auto;
                margin-top: 0;
                padding-right: 5px;
            }
            
            .footer-version-col {
                display: flex;
                align-items: flex-start;
                justify-content: center;
                overflow-y: auto;
                padding-right: 5px;
            }
            
            .version-card {
                background: #f7fafc;
                border-radius: 8px;
                padding: 12px;
                width: 100%;
                box-sizing: border-box;
                font-size: 0.78rem;
                color: #4a5568;
                text-align: center;
                border-top: 3px solid var(--primary-color);
                box-shadow: 0 2px 8px rgba(0,0,0,0.01);
            }
        }
        @media (max-width: 800px) {
            .top-nav {
                height: auto;
                padding: 10px 0;
            }
            .nav-container {
                flex-direction: column;
                gap: 10px;
                padding: 0 15px;
            }
            .nav-brand {
                font-size: 1.15rem;
            }
            .nav-links {
                display: flex;
                flex-wrap: wrap;
                width: 100%;
                justify-content: flex-start;
                gap: 8px;
            }
            .nav-tab-btn {
                padding: 6px 12px;
                font-size: 0.82rem;
                text-align: left;
                white-space: nowrap;
                justify-content: flex-start;
                box-sizing: border-box;
            }
            #nav-btn-page01, #nav-btn-page02, #nav-btn-page03 {
                flex: 0 0 calc(50% - 4px);
            }
            .desktop-only {
                display: none;
            }

            .layout { display: flex; flex-direction: column; padding: 15px; padding-bottom: 60px; }
            .site-banner { height: 180px; }
            .banner-title { font-size: 2rem; }
            .banner-subtitle { font-size: 0.85rem; letter-spacing: 3px; }
            .sidebar-left { display: none; }
            
            .sidebar-right {
                height: 340px;
            }
            .sidebar-right.collapsed-footer {
                transform: translateY(calc(100% - 48px));
            }
            .footer-main-content {
                display: flex;
                flex-direction: column;
                gap: 12px;
                padding: 15px 15px;
                height: calc(100% - 48px);
                overflow-y: auto;
            }
            .footer-search-col .sidebar-title {
                display: none;
            }
            .footer-results-col {
                border-left: none;
                border-right: none;
                padding: 0;
            }
            #searchResults {
                max-height: none;
                overflow-y: visible;
            }
            .footer-version-col {
                display: block;
                margin-top: 15px;
                border-top: 1px solid #e2e8f0;
                padding-top: 15px;
            }
            
            .content-middle { padding: 25px 18px; }
            figure.image-left { width: 100% !important; float: none !important; margin: 0 0 20px 0 !important; }
            h1 { font-size: 1.6rem; }
            
            /* Mobile Collapsible Heading Style */
            .content-middle h2 {
                cursor: pointer;
                position: relative;
                padding-right: 40px;
                padding-top: 12px;
                padding-bottom: 12px;
                margin-top: 25px;
                background-color: #f7fafc;
                border-radius: 6px;
                border-left: 5px solid var(--secondary-color);
                padding-left: 15px;
                font-size: 1.25rem;
                transition: background-color 0.2s, color 0.2s;
            }
            .content-middle h2:hover {
                background-color: #edf2f7;
            }
            .content-middle h2::after {
                content: '▲';
                position: absolute;
                right: 15px;
                top: 50%;
                transform: translateY(-50%);
                font-size: 0.75rem;
                color: var(--primary-color);
                transition: transform 0.3s ease;
            }
            .content-middle h2.collapsed::after {
                transform: translateY(-50%) rotate(180deg);
            }
            
            th, td { padding: 6px 8px; font-size: 0.8rem; }
        }
    </style>
</head>
<body>

<!-- Glassmorphism 置頂導覽列 -->
<nav class="top-nav">
    <div class="nav-container">
        <a href="#page01" class="nav-brand">🏛️ Gemini 的簡單歷史課</a>
        <div class="nav-links">
            <a href="#page01" id="nav-btn-page01" class="nav-tab-btn active" style="text-decoration: none;">荷蘭建國與地緣政經</a>
            <a href="#page02" id="nav-btn-page02" class="nav-tab-btn" style="text-decoration: none;">美國的誕生(一)</a>
            <a href="#page03" id="nav-btn-page03" class="nav-tab-btn" style="text-decoration: none;">宗教戰爭(一)：胡斯戰爭</a>
        </div>
    </div>
</nav>

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
        <!-- 課堂一：荷蘭建國史 -->
        <div id="course-page01" class="course-page">
            __HTML_BODY_PAGE01__
        </div>

        <!-- 課堂二：美國早期史 -->
        <div id="course-page02" class="course-page" style="display: none;">
            __HTML_BODY_PAGE02__
        </div>

        <!-- 課堂三：宗教戰爭(一)：胡斯戰爭 -->
        <div id="course-page03" class="course-page" style="display: none;">
            __HTML_BODY_PAGE03__
        </div>
    </main>

    <!-- Right Sidebar / Floating Footer: Search & Version -->
    <aside class="sidebar-right collapsed-footer" id="sidebarRight">
        <!-- Footer Header (Visible only when it behaves as mobile floating footer) -->
        <div class="footer-header" id="footerHeader">
            <span class="footer-header-title">🔍 快捷關鍵字搜尋與版本宣告</span>
            <button class="footer-toggle-btn" id="footerToggleBtn">展開 ▲</button>
        </div>
        
        <div class="footer-main-content">
            <!-- Col 1: Search Input -->
            <div class="footer-search-col">
                <div class="sidebar-title">關鍵字查詢</div>
                <div class="search-box">
                    <input type="text" id="searchInput" placeholder="輸入關鍵字 (例如: VOC, 印尼, 玉米)...">
                </div>
            </div>
            
            <!-- Col 2: Search Results -->
            <div class="footer-results-col">
                <div id="searchResults">
                    <div style="color:#a0aec0; text-align:center; margin-top:30px; font-size: 0.9rem;">
                        輸入關鍵字以尋找內文段落
                    </div>
                </div>
            </div>
            
            <!-- Col 3: Version Info -->
            <div class="footer-version-col">
                <div class="version-card">
                    <div style="font-weight: 600; margin-bottom: 8px; color: var(--primary-color);">📝 版本與課堂宣告</div>
                    <div style="font-weight: 500; margin-bottom: 6px;">版面設計：2.0 (動態三課堂)</div>
                    <div style="color: #718096; font-size: 0.75rem;">發布日期：2026-05-26</div>
                    <hr style="border: none; border-top: 1px dashed #cbd5e0; margin: 8px 0;">
                    <div id="dynamic-course-info" style="text-align: left; font-size: 0.8rem; line-height: 1.5;">
                        <!-- Dynamic metadata loaded by JS -->
                    </div>
                    <hr style="border: none; border-top: 1px dashed #cbd5e0; margin: 8px 0;">
                    <div style="font-size: 0.7rem; color: #a0aec0; text-align: left; line-height: 1.6;">
                        ⚠️ 本文由 AI 生成，可能包含事實性錯誤，請讀者自行查證。<br>
                        🖼️ 文中圖片來源：<a href="https://commons.wikimedia.org/" target="_blank" style="color: #718096;">Wikimedia Commons</a>。<br>
                        📜 本文採用 <a href="https://creativecommons.org/licenses/by-sa/4.0/deed.zh-hant" target="_blank" style="color: #718096;">CC BY-SA 4.0</a> 授權。
                    </div>
                    <hr style="border: none; border-top: 1px dashed #cbd5e0; margin: 8px 0;">
                    <div style="font-size: 0.7rem; color: #718096; text-align: left; line-height: 1.6; display: flex; flex-direction: column; gap: 4px;">
                        <span>👁️ 本站總瀏覽量：<span id="busuanzi_value_site_pv" style="font-weight: 600; color: var(--primary-color);">--</span> 次</span>
                        <span>👤 本站總訪客數：<span id="busuanzi_value_site_uv" style="font-weight: 600; color: var(--primary-color);">--</span> 人</span>
                    </div>
                </div>
            </div>
        </div>
    </aside>
</div>

<script>
    // 1. Dynamic Course Metadata
    const courseInfo = {
        'page01': `
            <div style="color: #4a5568;">
                <b>📚 當前課堂：</b>荷蘭建國史與地緣政經<br>
                <b>🏷️ 內容版本：</b>1.1<br>
                <b>👤 內容生成：</b>Gemini 深度研究<br>
                <b>🛠️ 網頁工程：</b>Antigravity 協作
            </div>
        `,
        'page02': `
            <div style="color: #4a5568;">
                <b>📚 當前課堂：</b>美國的誕生(一)<br>
                <b>🏷️ 內容版本：</b>1.0<br>
                <b>👤 內容生成：</b>Gemini 深度研究<br>
                <b>🛠️ 網頁工程：</b>Antigravity 協作
            </div>
        `,
        'page03': `
            <div style="color: #4a5568;">
                <b>📚 當前課堂：</b>宗教戰爭(一)：胡斯戰爭<br>
                <b>🏷️ 內容版本：</b>1.0<br>
                <b>👤 內容生成：</b>Gemini 深度研究<br>
                <b>🛠️ 網頁工程：</b>Antigravity 協作
            </div>
        `
    };

    // 2. Navigation Page Switching
    let activePageId = null;
    let searchableElements = [];

    function switchPage(pageId) {
        activePageId = pageId;
        
        // Update active tab buttons
        document.querySelectorAll('.nav-tab-btn').forEach(btn => btn.classList.remove('active'));
        const activeBtn = document.getElementById('nav-btn-' + pageId);
        if (activeBtn) activeBtn.classList.add('active');
        
        // Show/hide course content blocks
        document.querySelectorAll('.course-page').forEach(page => page.style.display = 'none');
        const activePage = document.getElementById('course-' + pageId);
        if (activePage) activePage.style.display = 'block';
        
        // Re-generate TOC for the active page
        generateTOC(pageId);
        
        // Re-index searchable elements for the active page
        updateSearchIndex(pageId);
        
        // Clear search inputs & results
        document.getElementById('searchInput').value = '';
        document.getElementById('searchResults').innerHTML = '<div style="color:#a0aec0; text-align:center; margin-top:30px; font-size: 0.9rem;">輸入關鍵字以尋找內文段落</div>';
        
        // Update copyright / details card
        const infoDiv = document.getElementById('dynamic-course-info');
        if (infoDiv && courseInfo[pageId]) {
            infoDiv.innerHTML = courseInfo[pageId];
        }
        
        // Re-init mobile collapsible headers
        initMobileCollapseForPage(pageId);

        // Smooth scroll to top of page/content
        if (window.scrollY > 280) {
            window.scrollTo({top: 260, behavior: 'smooth'});
        }
        
        // Update URL hash state
        const currentHash = window.location.hash.substring(1);
        if (!currentHash.startsWith(pageId)) {
            window.history.pushState(null, null, '#' + pageId);
        }
    }

    // 3. Generate Table of Contents on the Fly
    function generateTOC(pageId) {
        const tocContainer = document.getElementById('toc');
        tocContainer.innerHTML = '';
        
        const activePage = document.getElementById('course-' + pageId);
        if (!activePage) return;
        
        const headings = activePage.querySelectorAll('h2, h3');
        headings.forEach((h, index) => {
            // Always prefix with pageId to avoid cross-page collision and enable hash routing
            h.id = pageId + '-heading-' + index;
            const link = document.createElement('a');
            link.href = '#' + h.id;
            link.innerText = h.innerText;
            link.className = 'toc-item toc-' + h.tagName.toLowerCase();
            tocContainer.appendChild(link);
        });
    }

    // 4. Update Search Indexing Target
    function updateSearchIndex(pageId) {
        const activePage = document.getElementById('course-' + pageId);
        if (!activePage) return;
        searchableElements = activePage.querySelectorAll('p, h2, h3, li, td');
    }

    // 5. Keyword Search Engine
    const searchInput = document.getElementById('searchInput');
    const searchResults = document.getElementById('searchResults');

    searchInput.addEventListener('input', (e) => {
        const keyword = e.target.value.trim().toLowerCase();
        searchResults.innerHTML = '';
        
        if (!keyword) {
            searchResults.innerHTML = '<div style="color:#a0aec0; text-align:center; margin-top:30px; font-size: 0.9rem;">輸入關鍵字以尋找內文段落</div>';
            return;
        }

        let count = 0;
        searchableElements.forEach((el, index) => {
            const text = el.innerText;
            if (text.toLowerCase().includes(keyword)) {
                count++;
                if (count > 50) return; // Cap results to prevent lag
                
                if (!el.id) el.id = activePageId + '-search-match-' + index;
                
                const res = document.createElement('div');
                res.className = 'search-result-item';
                
                const idx = text.toLowerCase().indexOf(keyword);
                const start = Math.max(0, idx - 25);
                const end = Math.min(text.length, idx + 25);
                let snippet = text.substring(start, end);
                if (start > 0) snippet = '...' + snippet;
                if (end < text.length) snippet = snippet + '...';
                
                // Highlight keyword
                const regex = new RegExp('(' + keyword + ')', 'gi');
                snippet = snippet.replace(regex, '<mark>$1</mark>');
                
                res.innerHTML = snippet;
                res.onclick = () => {
                    // Mobile auto-expand collapsed heading if hidden inside one
                    if (window.innerWidth <= 800) {
                        const parentH2 = getParentH2(el);
                        if (parentH2 && parentH2.classList.contains('collapsed')) {
                            parentH2.click();
                        }
                    }
                    
                    // Close floating drawer on mobile / tablets
                    const sidebarRight = document.getElementById('sidebarRight');
                    const footerToggleBtn = document.getElementById('footerToggleBtn');
                    if (window.innerWidth <= 1200) {
                        if (sidebarRight && !sidebarRight.classList.contains('collapsed-footer')) {
                            sidebarRight.classList.add('collapsed-footer');
                            if (footerToggleBtn) footerToggleBtn.innerText = '展開 ▲';
                        }
                    }
                    
                    setTimeout(() => {
                        el.scrollIntoView({behavior: 'smooth', block: 'center'});
                        const originalBg = el.style.backgroundColor;
                        el.style.transition = 'background-color 0.3s';
                        el.style.backgroundColor = '#fbd38d';
                        setTimeout(() => { el.style.backgroundColor = originalBg; }, 2000);
                    }, window.innerWidth <= 800 ? 50 : 0);
                };
                searchResults.appendChild(res);
            }
        });
        
        if (count === 0) {
            searchResults.innerHTML = '<div style="color:#e53e3e; text-align:center; margin-top:30px; font-size: 0.95rem;">找不到包含「' + e.target.value + '」的內容</div>';
        } else if (count > 50) {
            const note = document.createElement('div');
            note.style = "color:#718096; text-align:center; margin-top:10px; font-size: 0.8rem;";
            note.innerText = `找到超過 50 筆結果，僅顯示前 50 筆`;
            searchResults.appendChild(note);
        }
    });

    // 6. Mobile Collapse Utilities
    function getParentH2(element) {
        let prev = element.previousElementSibling;
        while (prev) {
            if (prev.tagName === 'H2') {
                return prev;
            }
            prev = prev.previousElementSibling;
        }
        return null;
    }

    function initMobileCollapseForPage(pageId) {
        const isMobile = window.innerWidth <= 800;
        const activePage = document.getElementById('course-' + pageId);
        if (!activePage) return;
        
        const h2s = activePage.querySelectorAll('h2');
        h2s.forEach(h2 => {
            // Find related siblings to collapse/expand
            if (!h2._contentElements) {
                const contentElements = [];
                let next = h2.nextElementSibling;
                while (next && next.tagName !== 'H2') {
                    contentElements.push(next);
                    next = next.nextElementSibling;
                }
                h2._contentElements = contentElements;
                
                // Bind click toggle
                h2.addEventListener('click', () => {
                    if (window.innerWidth <= 800) {
                        const isCollapsed = h2.classList.toggle('collapsed');
                        h2._contentElements.forEach(el => {
                            el.style.display = isCollapsed ? 'none' : '';
                        });
                    }
                });
            }
            
            // Set initial state - Default to EXPANDED on all devices
            h2.classList.remove('collapsed');
            h2._contentElements.forEach(el => el.style.display = '');
        });
    }

    // Handles window resizing collapse resets
    let wasMobile = window.innerWidth <= 800;
    window.addEventListener('resize', () => {
        const isMobile = window.innerWidth <= 800;
        if (isMobile !== wasMobile) {
            wasMobile = isMobile;
            initMobileCollapseForPage(activePageId);
        }
    });

    // 7. Mobile Floating Drawer Collapse Toggle
    const sidebarRight = document.getElementById('sidebarRight');
    const footerHeader = document.getElementById('footerHeader');
    const footerToggleBtn = document.getElementById('footerToggleBtn');

    if (footerHeader && sidebarRight && footerToggleBtn) {
        const toggleFooter = () => {
            const isCollapsed = sidebarRight.classList.toggle('collapsed-footer');
            footerToggleBtn.innerText = isCollapsed ? '展開 ▲' : '收合 ▼';
        };
        footerHeader.addEventListener('click', toggleFooter);
    }

    // 8. Hash routing listener
    function handleHashRouting() {
        const hash = window.location.hash.substring(1);
        
        if (!hash) {
            if (activePageId !== 'page01') switchPage('page01');
            return;
        }

        const matchedPage = ['page01', 'page02', 'page03'].find(p => hash.startsWith(p));
        if (matchedPage) {
            if (activePageId !== matchedPage) {
                switchPage(matchedPage);
                setTimeout(() => {
                    const target = document.getElementById(hash);
                    if (target) target.scrollIntoView();
                }, 50);
            }
        } else {
            if (activePageId !== 'page01') switchPage('page01');
        }
    }
    
    window.addEventListener('hashchange', handleHashRouting);
    window.addEventListener('DOMContentLoaded', handleHashRouting);
</script>

<script async src="//busuanzi.ibruce.info/busuanzi/2.3/busuanzi.pure.mini.js"></script>
</body>
</html>"""

# Merge compiled markdown contents into template
final_html = portal_template.replace('__HTML_BODY_PAGE01__', html_body_p1)
final_html = final_html.replace('__HTML_BODY_PAGE02__', html_body_p2)
final_html = final_html.replace('__HTML_BODY_PAGE03__', html_body_p3)

# Write to file
print("Writing build output to index.html...")
with open(r'index.html', 'w', encoding='utf-8') as f:
    f.write(final_html)

# Generate sitemap.xml for SEO
sitemap_content = """\
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://ludwicia.github.io/gemini-history-lesson/</loc>
    <changefreq>weekly</changefreq>
    <priority>1.0</priority>
  </url>
</urlset>"""

with open(r'sitemap.xml', 'w', encoding='utf-8', newline='\n') as f:
    f.write(sitemap_content)
print("Generated sitemap.xml")

# Generate robots.txt for SEO
robots_content = """User-agent: *
Allow: /

Sitemap: https://ludwicia.github.io/gemini-history-lesson/sitemap.xml
"""

with open(r'robots.txt', 'w', encoding='utf-8') as f:
    f.write(robots_content)
print("Generated robots.txt")

print("Done! Site successfully built as dynamic triple-lesson portal.")
