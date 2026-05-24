target_file = r'build_html_md.py'

with open(target_file, 'r', encoding='utf-8') as f:
    content = f.read()

# Emojis on some Windows systems render as letters or icons. Let's remove them as requested by the user.
old_btn1 = """            <button id="nav-btn-page01" class="nav-tab-btn active" onclick="switchPage('page01')">🏛️ 課堂一：荷蘭建國與地緣政經</button>"""
new_btn1 = """            <button id="nav-btn-page01" class="nav-tab-btn active" onclick="switchPage('page01')">課堂一：荷蘭建國與地緣政經</button>"""

old_btn2 = """            <button id="nav-btn-page02" class="nav-tab-btn" onclick="switchPage('page02')">🇺🇸 課堂二：美國的誕生(一)</button>"""
new_btn2 = """            <button id="nav-btn-page02" class="nav-tab-btn" onclick="switchPage('page02')">課堂二：美國的誕生(一)</button>"""

if old_btn1 in content:
    content = content.replace(old_btn1, new_btn1)
if old_btn2 in content:
    content = content.replace(old_btn2, new_btn2)

# If it's a newline issue, let's normalize and replace
normalized_content = content.replace('\r\n', '\n')
norm_old1 = old_btn1.replace('\r\n', '\n')
norm_new1 = new_btn1.replace('\r\n', '\n')
norm_old2 = old_btn2.replace('\r\n', '\n')
norm_new2 = new_btn2.replace('\r\n', '\n')

if norm_old1 in normalized_content:
    normalized_content = normalized_content.replace(norm_old1, norm_new1)
if norm_old2 in normalized_content:
    normalized_content = normalized_content.replace(norm_old2, norm_new2)

with open(target_file, 'w', encoding='utf-8', newline='\r\n') as f:
    f.write(normalized_content)

print("SUCCESS: Removed icons and flag letters from navigation tab buttons in build_html_md.py!")
