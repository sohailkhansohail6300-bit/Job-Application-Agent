import os

from weasyprint import HTML


def html_to_pdf(html_text, out_path):
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    HTML(string=html_text).write_pdf(out_path)
    return out_path


def markdown_to_html(markdown_text):
    text = markdown_text or ''
    lines = text.splitlines()
    html = []
    in_list = False
    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith('# '):
            if in_list:
                html.append('</ul>')
                in_list = False
            html.append(f'<h1>{stripped[2:]}</h1>')
        elif stripped.startswith('## '):
            if in_list:
                html.append('</ul>')
                in_list = False
            html.append(f'<h2>{stripped[3:]}</h2>')
        elif stripped.startswith('- '):
            if not in_list:
                html.append('<ul>')
                in_list = True
            html.append(f'<li>{stripped[2:]}</li>')
        else:
            if in_list:
                html.append('</ul>')
                in_list = False
            html.append(f'<p>{stripped}</p>')
    if in_list:
        html.append('</ul>')
    return '<html><head><meta charset="utf-8"></head><body>' + ''.join(html) + '</body></html>'
