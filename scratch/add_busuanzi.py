target_file = r'build_html_md.py'

with open(target_file, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Insert Busuanzi HTML widget in footer
old_license_block = """                    <div style="font-size: 0.7rem; color: #a0aec0; text-align: left; line-height: 1.6;">
                        ⚠️ 本文由 AI 生成，可能包含事實性錯誤，請讀者自行查證。<br>
                        🖼️ 文中圖片來源：<a href="https://commons.wikimedia.org/" target="_blank" style="color: #718096;">Wikimedia Commons</a>。<br>
                        📜 本文採用 <a href="https://creativecommons.org/licenses/by-sa/4.0/deed.zh-hant" target="_blank" style="color: #718096;">CC BY-SA 4.0</a> 授權。
                    </div>"""

new_license_block = """                    <div style="font-size: 0.7rem; color: #a0aec0; text-align: left; line-height: 1.6;">
                        ⚠️ 本文由 AI 生成，可能包含事實性錯誤，請讀者自行查證。<br>
                        🖼️ 文中圖片來源：<a href="https://commons.wikimedia.org/" target="_blank" style="color: #718096;">Wikimedia Commons</a>。<br>
                        📜 本文採用 <a href="https://creativecommons.org/licenses/by-sa/4.0/deed.zh-hant" target="_blank" style="color: #718096;">CC BY-SA 4.0</a> 授權。
                    </div>
                    <hr style="border: none; border-top: 1px dashed #cbd5e0; margin: 8px 0;">
                    <div style="font-size: 0.7rem; color: #718096; text-align: left; line-height: 1.6; display: flex; flex-direction: column; gap: 4px;">
                        <span>👁️ 本站總瀏覽量：<span id="busuanzi_value_site_pv" style="font-weight: 600; color: var(--primary-color);">--</span> 次</span>
                        <span>👤 本站總訪客數：<span id="busuanzi_value_site_uv" style="font-weight: 600; color: var(--primary-color);">--</span> 人</span>
                    </div>"""

# 2. Insert Busuanzi script tag before </body>
old_body_end = """</body>
</html>"""

new_body_end = """<script async src="//busuanzi.ibruce.info/busuanzi/2.3/busuanzi.pure.mini.js"></script>
</body>
</html>"""

# Perform replacement
content_replaced = content.replace(old_license_block, new_license_block)
content_replaced = content_replaced.replace(old_body_end, new_body_end)

# Normalize newlines if replacement failed due to CR/LF
if content_replaced == content:
    normalized_content = content.replace('\r\n', '\n')
    norm_old1 = old_license_block.replace('\r\n', '\n')
    norm_new1 = new_license_block.replace('\r\n', '\n')
    norm_old2 = old_body_end.replace('\r\n', '\n')
    norm_new2 = new_body_end.replace('\r\n', '\n')
    
    normalized_content = normalized_content.replace(norm_old1, norm_new1)
    normalized_content = normalized_content.replace(norm_old2, norm_new2)
    
    with open(target_file, 'w', encoding='utf-8', newline='\r\n') as f:
        f.write(normalized_content)
    print("SUCCESS: Installed Busuanzi counter using newline normalization!")
else:
    with open(target_file, 'w', encoding='utf-8') as f:
        f.write(content_replaced)
    print("SUCCESS: Installed Busuanzi counter directly!")
