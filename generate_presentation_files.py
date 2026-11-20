import os
import sys

# Import slide definitions from build_presentation
from build_presentation import slides_data

def escape_pdf(text):
    if not text:
        return ""
    text = str(text)
    return text.replace('\\', '\\\\').replace('(', '\\(').replace(')', '\\)')

def wrap_text(text, max_chars=48):
    words = text.split(' ')
    lines = []
    curr = []
    curr_len = 0
    for w in words:
        if curr_len + len(w) + 1 <= max_chars:
            curr.append(w)
            curr_len += len(w) + 1
        else:
            if curr:
                lines.append(' '.join(curr))
            curr = [w]
            curr_len = len(w)
    if curr:
        lines.append(' '.join(curr))
    return lines

def generate_pdf(slides, output_path):
    W, H = 960, 540 # 16:9 widescreen presentation slide in points
    
    objects = []
    def add_obj(data):
        objects.append(data)
        return len(objects)

    # Base Fonts
    # Obj 1: Helvetica-Bold, Obj 2: Helvetica
    font_bold = add_obj('<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold >>')
    font_reg = add_obj('<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>')
    
    page_obj_ids = []
    
    for slide in slides:
        cmds = []
        
        # 1. Background (Dark Slate/Navy #0B1120 -> 0.043, 0.067, 0.125)
        cmds.append('q')
        cmds.append('0.043 0.067 0.125 rg 0 0 960 540 re f')
        
        # Top gradient-like accent bar (Indigo / Violet #6366F1 -> 0.388, 0.400, 0.945)
        cmds.append('0.388 0.400 0.945 rg 0 534 960 6 re f')
        
        # 2. Header Area
        # Category Badge
        cat = slide.get('category', 'CAMPUSCREW MASTER SPECIFICATION')
        cmds.append('0.15 0.20 0.35 rg 50 488 280 22 re f')
        cmds.append('0.50 0.65 1.00 rg')
        cmds.append('BT /F1 9 Tf 62 494 Td (' + escape_pdf(cat) + ') Tj ET')
        
        # Title & Subtitle
        title = slide.get('title', '')
        subtitle = slide.get('subtitle', '')
        cmds.append('0.98 0.98 1.00 rg')
        cmds.append('BT /F1 20 Tf 50 458 Td (' + escape_pdf(title) + ') Tj ET')
        cmds.append('0.60 0.68 0.82 rg')
        cmds.append('BT /F2 11 Tf 50 440 Td (' + escape_pdf(subtitle) + ') Tj ET')
        
        # Subtle divider line
        cmds.append('0.15 0.20 0.30 RG 1 w 50 428 m 910 428 l S')
        
        # 3. Cards Content
        cards = slide.get('cards', [])
        num_cards = len(cards)
        
        if num_cards == 2:
            card_w = 415
            card_gap = 30
            start_x = 50
        elif num_cards == 3:
            card_w = 270
            card_gap = 25
            start_x = 50
        elif num_cards == 4:
            card_w = 200
            card_gap = 20
            start_x = 50
        else:
            card_w = 860
            card_gap = 0
            start_x = 50
            
        card_h = 345
        card_y = 65
        
        for i, card in enumerate(cards):
            cx = start_x + i * (card_w + card_gap)
            cy = card_y
            
            # Card background
            cmds.append('0.08 0.12 0.22 rg ' + f'{cx} {cy} {card_w} {card_h} re f')
            cmds.append('0.18 0.25 0.40 RG 1 w ' + f'{cx} {cy} {card_w} {card_h} re S')
            
            # Card header band
            cmds.append('0.11 0.17 0.30 rg ' + f'{cx} {cy + card_h - 40} {card_w} 40 re f')
            
            # Card badge
            badge = card.get('badge', '')
            if badge:
                cmds.append('0.22 0.35 0.65 rg ' + f'{cx + card_w - 95} {cy + card_h - 30} 85 20 re f')
                cmds.append('0.85 0.92 1.00 rg')
                cmds.append(f'BT /F1 8 Tf {cx + card_w - 90} {cy + card_h - 24} Td (' + escape_pdf(badge) + ') Tj ET')
            
            # Card title
            ctitle = card.get('title', '')
            cmds.append('1 1 1 rg')
            cmds.append(f'BT /F1 12 Tf {cx + 14} {cy + card_h - 25} Td (' + escape_pdf(ctitle) + ') Tj ET')
            
            # Card items
            items = card.get('items', [])
            item_y = cy + card_h - 60
            
            max_c = 44 if num_cards == 2 else (28 if num_cards == 3 else 22)
            
            for item in items:
                lines = wrap_text(item, max_chars=max_c)
                # Draw bullet
                cmds.append('0.388 0.500 0.945 rg')
                cmds.append(f'BT /F1 10 Tf {cx + 14} {item_y} Td (>) Tj ET')
                
                # Draw text lines
                cmds.append('0.82 0.88 0.95 rg')
                for l_idx, line in enumerate(lines):
                    cmds.append(f'BT /F2 9.5 Tf {cx + 26} {item_y} Td (' + escape_pdf(line) + ') Tj ET')
                    item_y -= 13
                item_y -= 6
                if item_y < cy + 15:
                    break
        
        # 4. Footer Area
        cmds.append('0.15 0.20 0.30 RG 1 w 50 50 m 910 50 l S')
        cmds.append('0.45 0.55 0.70 rg')
        cmds.append('BT /F2 8.5 Tf 50 35 Td (CampusCrew Architecture & Specification Presentation | Confidential & Proprietary) Tj ET')
        
        s_num = slide.get('slide_num', 1)
        cmds.append(f'BT /F1 8.5 Tf 840 35 Td (Slide {s_num} of {len(slides)}) Tj ET')
        cmds.append('Q')
        
        stream_content = '\n'.join(cmds).encode('latin1')
        c_obj = add_obj(f'<< /Length {len(stream_content)} >>\nstream\n' + stream_content.decode('latin1') + '\nendstream')
        page_obj = add_obj(f'<< /Type /Page /Parent 0 0 R /MediaBox [0 0 {W} {H}] /Resources << /Font << /F1 {font_bold} 0 R /F2 {font_reg} 0 R >> >> /Contents {c_obj} 0 R >>')
        page_obj_ids.append(page_obj)

    # Pages container object
    kids_str = ' '.join([f'{pid} 0 R' for pid in page_obj_ids])
    pages_obj = add_obj(f'<< /Type /Pages /Kids [{kids_str}] /Count {len(page_obj_ids)} >>')
    
    # Update Parent pointer in page objects
    catalog_obj = add_obj(f'<< /Type /Catalog /Pages {pages_obj} 0 R >>')
    
    # Construct final PDF string and fix parent pointers
    body = '%PDF-1.4\n'
    offsets = []
    
    for i, obj in enumerate(objects):
        obj_num = i + 1
        # If this is a Page object, update /Parent 0 0 R with actual pages_obj
        if '<< /Type /Page /Parent 0 0 R' in obj:
            obj = obj.replace('/Parent 0 0 R', f'/Parent {pages_obj} 0 R')
        offsets.append(len(body.encode('latin1')))
        body += f'{obj_num} 0 obj\n{obj}\nendobj\n'
        
    xref_offset = len(body.encode('latin1'))
    body += f'xref\n0 {len(objects)+1}\n0000000000 65535 f \n'
    for off in offsets:
        body += f'{off:010d} 00000 n \n'
    body += f'trailer\n<< /Size {len(objects)+1} /Root {catalog_obj} 0 R >>\nstartxref\n{xref_offset}\n%%EOF\n'
    
    with open(output_path, 'wb') as f:
        f.write(body.encode('latin1'))
    
    print(f"Generated PDF with {len(slides)} slides at: {output_path} ({os.path.getsize(output_path)} bytes)")

def generate_html(slides, output_path):
    slides_html = []
    for idx, slide in enumerate(slides):
        s_num = slide.get('slide_num', idx + 1)
        cat = slide.get('category', '')
        title = slide.get('title', '')
        subtitle = slide.get('subtitle', '')
        cards = slide.get('cards', [])
        
        cards_html = []
        col_class = "grid-cols-2" if len(cards) == 2 else ("grid-cols-3" if len(cards) == 3 else "grid-cols-4")
        
        for c in cards:
            c_title = c.get('title', '')
            c_badge = c.get('badge', '')
            items = c.get('items', [])
            
            items_li = "".join([f"""
                <li class="flex items-start gap-2.5 text-slate-300 text-sm leading-relaxed">
                    <span class="text-indigo-400 font-bold mt-0.5 select-none">▸</span>
                    <span>{item}</span>
                </li>
            """ for item in items])
            
            cards_html.append(f"""
                <div class="bg-slate-900/80 border border-slate-700/60 rounded-xl p-5 flex flex-col justify-between shadow-lg backdrop-blur hover:border-indigo-500/50 transition">
                    <div>
                        <div class="flex items-center justify-between mb-3.5 pb-2 border-b border-slate-800">
                            <h3 class="font-semibold text-slate-100 text-base tracking-tight">{c_title}</h3>
                            {f'<span class="px-2.5 py-0.5 rounded text-[11px] font-medium bg-indigo-500/20 text-indigo-300 border border-indigo-500/30">{c_badge}</span>' if c_badge else ''}
                        </div>
                        <ul class="space-y-2.5">
                            {items_li}
                        </ul>
                    </div>
                </div>
            """)
        
        slides_html.append(f"""
        <!-- SLIDE {s_num} -->
        <section class="slide-container {'active' if idx == 0 else ''}" id="slide-{s_num}">
            <div class="slide-card bg-slate-950 border border-slate-800 rounded-2xl shadow-2xl overflow-hidden flex flex-col justify-between p-8 relative">
                <!-- Top Accent Line -->
                <div class="absolute top-0 left-0 right-0 h-1 bg-gradient-to-r from-indigo-500 via-purple-500 to-pink-500"></div>
                
                <!-- Slide Header -->
                <div>
                    <div class="flex items-center justify-between mb-2">
                        <span class="px-3 py-1 rounded-md text-xs font-semibold bg-indigo-950/80 text-indigo-400 border border-indigo-800/60 uppercase tracking-wider">
                            {cat}
                        </span>
                        <span class="text-xs font-medium text-slate-400 bg-slate-900 px-3 py-1 rounded-full border border-slate-800">
                            Slide {s_num} / {len(slides)}
                        </span>
                    </div>
                    <h2 class="text-2xl md:text-3xl font-extrabold text-white tracking-tight mt-1">{title}</h2>
                    <p class="text-slate-400 text-sm mt-1">{subtitle}</p>
                </div>
                
                <!-- Slide Body / Cards Grid -->
                <div class="grid {col_class} gap-5 my-6 flex-1 items-stretch">
                    {"".join(cards_html)}
                </div>
                
                <!-- Slide Footer -->
                <div class="pt-4 border-t border-slate-800/80 flex items-center justify-between text-xs text-slate-400">
                    <div class="flex items-center gap-2">
                        <span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
                        <span class="font-medium text-slate-300">CampusCrew Architecture & Specification Master</span>
                    </div>
                    <span>For Cross-Check & Sign-Off Prior to Website Development</span>
                </div>
            </div>
        </section>
        """)
        
    html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CampusCrew - Platform Modules & Architecture Specification</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
    <style>
        body {{
            font-family: 'Plus Jakarta Sans', sans-serif;
            background-color: #030712;
            color: #f3f4f6;
            margin: 0;
            padding: 0;
            overflow-x: hidden;
        }}
        .slide-container {{
            display: none;
            width: 100vw;
            min-height: 100vh;
            padding: 2rem;
            box-sizing: border-box;
            align-items: center;
            justify-content: center;
        }}
        .slide-container.active {{
            display: flex;
        }}
        .slide-card {{
            width: 100%;
            max-width: 1200px;
            min-height: 650px;
        }}
        @media print {{
            body {{
                background-color: white !important;
                color: black !important;
            }}
            .no-print {{
                display: none !important;
            }}
            .slide-container {{
                display: flex !important;
                page-break-after: always;
                min-height: 100vh;
                padding: 1cm;
            }}
            .slide-card {{
                border: 1px solid #e2e8f0 !important;
                background-color: #ffffff !important;
                color: #0f172a !important;
                box-shadow: none !important;
            }}
            .text-white {{
                color: #0f172a !important;
            }}
            .text-slate-100, .text-slate-300, .text-slate-400 {{
                color: #334155 !important;
            }}
            .bg-slate-900\/80, .bg-slate-950 {{
                background-color: #f8fafc !important;
                border: 1px solid #cbd5e1 !important;
            }}
        }}
    </style>
</head>
<body class="selection:bg-indigo-500 selection:text-white">

    <!-- Top Floating Toolbar -->
    <header class="no-print fixed top-4 left-1/2 -translate-x-1/2 bg-slate-900/90 backdrop-blur-md border border-slate-700/80 px-6 py-2.5 rounded-full shadow-2xl z-50 flex items-center gap-4">
        <div class="flex items-center gap-2 pr-4 border-r border-slate-700">
            <span class="w-3 h-3 rounded-full bg-indigo-500"></span>
            <span class="font-bold text-sm tracking-tight text-white">CampusCrew</span>
            <span class="text-[11px] text-indigo-400 bg-indigo-950 px-2 py-0.5 rounded-full border border-indigo-800">Presentation Deck</span>
        </div>
        
        <div class="flex items-center gap-2">
            <button onclick="prevSlide()" class="p-1.5 rounded-lg hover:bg-slate-800 text-slate-300 hover:text-white transition">
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/></svg>
            </button>
            <span id="slideCounter" class="text-xs font-mono text-slate-300 min-w-[70px] text-center">Slide 1 / {len(slides)}</span>
            <button onclick="nextSlide()" class="p-1.5 rounded-lg hover:bg-slate-800 text-slate-300 hover:text-white transition">
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/></svg>
            </button>
        </div>
        
        <div class="flex items-center gap-2 pl-4 border-l border-slate-700">
            <button onclick="window.print()" class="flex items-center gap-1.5 text-xs font-medium px-3 py-1.5 rounded-lg bg-indigo-600 hover:bg-indigo-500 text-white transition shadow-sm">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 17h2a2 2 0 002-2v-4a2 2 0 00-2-2H5a2 2 0 00-2 2v4a2 2 0 002 2h2m2 4h6a2 2 0 002-2v-4a2 2 0 00-2-2H9a2 2 0 00-2 2v4a2 2 0 002 2zm8-12V5a2 2 0 00-2-2H9a2 2 0 00-2 2v4h10z"/></svg>
                Print / Save PDF
            </button>
            <a href="CampusCrew_Modules_Presentation.pdf" download class="flex items-center gap-1.5 text-xs font-medium px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-200 transition border border-slate-700">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"/></svg>
                Direct PDF
            </a>
        </div>
    </header>

    <!-- Slide Deck Container -->
    <main class="w-full min-h-screen flex items-center justify-center">
        {"".join(slides_html)}
    </main>

    <!-- Bottom Keyboard Shortcut Hint -->
    <footer class="no-print fixed bottom-3 left-1/2 -translate-x-1/2 text-[11px] text-slate-500 bg-slate-900/60 backdrop-blur px-4 py-1 rounded-full border border-slate-800">
        Use <kbd class="px-1.5 py-0.5 rounded bg-slate-800 text-slate-300 font-mono text-[10px]">←</kbd> <kbd class="px-1.5 py-0.5 rounded bg-slate-800 text-slate-300 font-mono text-[10px]">→</kbd> arrow keys or <kbd class="px-1.5 py-0.5 rounded bg-slate-800 text-slate-300 font-mono text-[10px]">Space</kbd> to navigate slides
    </footer>

    <script>
        let currentSlide = 1;
        const totalSlides = {len(slides)};

        function showSlide(n) {{
            if (n < 1) n = 1;
            if (n > totalSlides) n = totalSlides;
            currentSlide = n;
            
            document.querySelectorAll('.slide-container').forEach(el => {{
                el.classList.remove('active');
            }});
            
            const activeEl = document.getElementById('slide-' + currentSlide);
            if (activeEl) {{
                activeEl.classList.add('active');
            }}
            
            document.getElementById('slideCounter').textContent = `Slide ${{currentSlide}} / ${{totalSlides}}`;
        }}

        function nextSlide() {{
            showSlide(currentSlide + 1);
        }}

        function prevSlide() {{
            showSlide(currentSlide - 1);
        }}

        document.addEventListener('keydown', (e) => {{
            if (e.key === 'ArrowRight' || e.key === ' ' || e.key === 'PageDown') {{
                nextSlide();
            }} else if (e.key === 'ArrowLeft' || e.key === 'PageUp') {{
                prevSlide();
            }} else if (e.key === 'Home') {{
                showSlide(1);
            }} else if (e.key === 'End') {{
                showSlide(totalSlides);
            }}
        }});
    </script>
</body>
</html>
"""
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_template)
    print(f"Generated HTML slide deck at: {output_path} ({os.path.getsize(output_path)} bytes)")

if __name__ == '__main__':
    out_dir = '/Users/ayushkumar/.gemini/antigravity/scratch/campuscrew'
    pdf_path = os.path.join(out_dir, 'CampusCrew_Modules_Presentation.pdf')
    html_path = os.path.join(out_dir, 'CampusCrew_Modules_Presentation.html')
    
    generate_pdf(slides_data, pdf_path)
    generate_html(slides_data, html_path)
    print("ALL FILES GENERATED SUCCESSFULLY!")
