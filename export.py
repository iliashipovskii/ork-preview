# -*- coding: utf-8 -*-
"""
Снимок работающего WordPress в статические файлы для GitHub Pages.

Зачем так, а не второй генератор: раньше прототип собирался отдельным
скриптом, и после переезда на WordPress две версии начали расходиться —
на Pages не было ни нового меню, ни «Новостей», ни «О компании».
Поддерживать две копии одного сайта смысла нет, поэтому прототип теперь
просто снимается с боевой сборки и всегда ей соответствует.

Что делает:
  1. обходит все публичные адреса локального WordPress;
  2. складывает страницы как <путь>/index.html;
  3. тащит за собой стили, скрипты, шрифты и картинки из медиатеки;
  4. переписывает абсолютные ссылки на относительные — чтобы сайт жил
     в подпапке /ork-preview/ на GitHub Pages;
  5. дописывает в подвал строчку о том, что это демоверсия.

Запуск (WordPress должен быть поднят):
    python preview/export.py
    python preview/export.py --site http://localhost:8080
"""

import argparse
import os
import re
import shutil
import sys
import urllib.parse
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))

# Файлы прототипа, которые не относятся к снимку и должны пережить очистку.
KEEP = {'export.py', '.nojekyll', 'robots.txt', 'CNAME'}

NOINDEX = '<meta name="robots" content="noindex, nofollow">'

DEMO_NOTE = (
    '<div class="demo-note-footer">Демоверсия. Фотографии временные, '
    'тексты, телефон и адрес — рыба: заменим на настоящие.</div>'
)

DEMO_CSS = """
.demo-note-footer {
	max-width: 1240px;
	margin: 24px auto 0;
	padding: 14px 32px 0;
	border-top: 1px solid rgba(255, 255, 255, 0.15);
	font-size: 13px;
	line-height: 1.5;
	color: #8fa79a;
}

@media (max-width: 900px) {
	.demo-note-footer {
		padding: 14px 20px 0;
	}
}
"""


# В окружении разработчика задан системный HTTP-прокси, и запросы к
# localhost уходили через него — WordPress отвечал 502. Ходим напрямую.
_opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))


def fetch(url):
    """Содержимое по адресу и его content-type."""
    req = urllib.request.Request(url, headers={'User-Agent': 'ork-export/1.0'})
    with _opener.open(req, timeout=60) as r:
        return r.read(), r.headers.get('Content-Type', '')


# Ссылки, которые WordPress ставит в <head> для себя: на статике за ними
# ничего нет, а браузер и проверялки ссылок на них спотыкаются.
CRUFT = re.compile(
    r'<link[^>]*rel=[^>]*(?:alternate|EditURI|wlwmanifest|pingback|api\.w\.org)[^>]*>'
    r'|<link[^>]*(?:/feed/|wp-json|xmlrpc)[^>]*>'
)


def strip_wp_cruft(html):
    """Выкусывает из <head> ссылки на RSS, REST API и xmlrpc."""
    return CRUFT.sub('', html)


def page_path(site, url):
    """Адрес страницы → путь файла внутри preview/."""
    rel = urllib.parse.urlparse(url).path.strip('/')

    return 'index.html' if '' == rel else rel + '/index.html'


def depth_of(path):
    """Сколько уровней вложенности у файла — столько же ../ в ссылках."""
    return path.count('/')


def rewrite(text, site, depth):
    """Абсолютные ссылки на сайт → относительные."""
    up = '../' * depth

    def repl(m):
        tail = m.group(1).lstrip('/')

        # Ссылка на главную из корня должна остаться непустой.
        return (up + tail) if (tail or up) else './'

    # И http, и https, и протокол-относительный вид.
    for prefix in (site, site.replace('http://', 'https://'), site.replace('http://', '//')):
        text = re.sub(re.escape(prefix) + r'([^"\'\s)>]*)', repl, text)

    return text


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--site', default='http://localhost:8080')
    parser.add_argument('--urls', default=None, help='файл со списком адресов')
    parser.add_argument('--base', default='/ork-preview/',
                        help='корень сайта на хостинге — нужен только для 404.html')
    args = parser.parse_args()

    site = args.site.rstrip('/')

    if args.urls:
        urls = [u.strip() for u in open(args.urls, encoding='utf-8') if u.strip().startswith('http')]
    else:
        urls = [site + '/']

    # Главная всегда первой, дубли убираем, но порядок сохраняем.
    seen = set()
    pages = []

    for u in [site + '/'] + urls:
        key = urllib.parse.urlparse(u).path.rstrip('/') or '/'

        if key in seen:
            continue

        seen.add(key)
        pages.append(site + (urllib.parse.urlparse(u).path or '/'))

    # Чистим прошлый снимок.
    for name in os.listdir(HERE):
        if name in KEEP:
            continue

        path = os.path.join(HERE, name)
        shutil.rmtree(path) if os.path.isdir(path) else os.remove(path)

    assets = set()
    saved = 0
    queue_pages = list(pages)

    # Служебное WordPress на статике не нужно и только ломает обход.
    skip = re.compile(r'/(wp-admin|wp-json|wp-login|feed|comments|xmlrpc)')

    while queue_pages:
        url = queue_pages.pop(0)

        try:
            body, ctype = fetch(url)
        except Exception as exc:  # адрес мог исчезнуть между выборкой и обходом
            print('пропуск %s — %s' % (url, exc))
            continue

        if 'text/html' not in ctype:
            continue

        html = body.decode('utf-8', 'replace')

        # Идём по внутренним ссылкам: так подхватываются страницы
        # постраничной навигации, которых нет в списке из wp-cli.
        for m in re.finditer(r'href="' + re.escape(site) + r'([^"#?]*)"', html):
            path = m.group(1) or '/'

            if skip.search(path) or '.' in path.rsplit('/', 1)[-1]:
                continue

            key = path.rstrip('/') or '/'

            if key in seen:
                continue

            seen.add(key)
            queue_pages.append(site + path)

        # Собираем всё, что страница тянет с этого же сайта.
        for m in re.finditer(re.escape(site) + r'(/wp-content/[^"\'\s)>]+)', html):
            assets.add(m.group(1))

        rel = page_path(site, url)
        depth = depth_of(rel)

        html = strip_wp_cruft(html)

        if NOINDEX not in html:
            html = html.replace('</title>', '</title>\n' + NOINDEX, 1)

        if '</footer>' in html:
            html = html.replace('</footer>', DEMO_NOTE + '</footer>', 1)

        html = rewrite(html, site, depth)

        out = os.path.join(HERE, rel)
        os.makedirs(os.path.dirname(out), exist_ok=True)

        with open(out, 'w', encoding='utf-8', newline='\n') as f:
            f.write(html)

        saved += 1

    # Страница 404: GitHub Pages сам отдаёт 404.html.
    try:
        body, _ = fetch(site + '/stranica-kotoroy-net-404/')
    except urllib.error.HTTPError as exc:
        body = exc.read()
    except Exception:
        body = b''

    if body:
        html = body.decode('utf-8', 'replace')

        for m in re.finditer(re.escape(site) + r'(/wp-content/[^"\'\s)>]+)', html):
            assets.add(m.group(1))

        # 404.html лежит в корне, но открывается с любого уровня —
        # поэтому ссылки в нём должны быть от корня сайта Pages.
        base = '/' + args.base.strip('/') + '/' if args.base.strip('/') else '/'
        html = strip_wp_cruft(html)
        html = html.replace('</footer>', DEMO_NOTE + '</footer>', 1)
        html = rewrite(html, site, 0)

        # 404 открывается с любого уровня вложенности, поэтому относительные
        # ссылки в ней не годятся — переводим их в абсолютные от корня сайта.
        for attr in ('href', 'src'):
            html = html.replace(attr + '="', attr + '="' + base)
            html = html.replace(attr + '="' + base + 'http', attr + '="http')
            html = html.replace(attr + '="' + base + '#', attr + '="#')
            html = html.replace(attr + '="' + base + 'mailto:', attr + '="mailto:')
            html = html.replace(attr + '="' + base + 'tel:', attr + '="tel:')
            html = html.replace(attr + '="' + base + './', attr + '="' + base)

        with open(os.path.join(HERE, '404.html'), 'w', encoding='utf-8', newline='\n') as f:
            f.write(html)

    # Ассеты: стили, скрипты, шрифты, картинки. CSS может тянуть ещё шрифты.
    queue = list(assets)
    done = set()

    while queue:
        rel = queue.pop()

        if rel in done:
            continue

        done.add(rel)
        clean = rel.split('?')[0].split('#')[0]
        out = os.path.join(HERE, clean.lstrip('/'))

        try:
            data, ctype = fetch(site + rel)
        except Exception as exc:
            print('нет ассета %s — %s' % (rel, exc))
            continue

        os.makedirs(os.path.dirname(out), exist_ok=True)

        if 'css' in ctype:
            text = data.decode('utf-8', 'replace')

            for m in re.finditer(r'url\(\s*[\'"]?([^\'")]+)', text):
                ref = m.group(1)

                if ref.startswith('data:'):
                    continue

                absolute = urllib.parse.urljoin(site + clean, ref)

                if absolute.startswith(site + '/wp-content/'):
                    queue.append(absolute[len(site):])

            data = rewrite(text, site, depth_of(clean.lstrip('/'))).encode('utf-8')

        with open(out, 'wb') as f:
            f.write(data)

    # Полоска «это демо» — дописываем в тему, чтобы не плодить отдельный файл.
    theme_css = os.path.join(HERE, 'wp-content', 'themes', 'ork', 'assets', 'css', 'site.css')

    if os.path.exists(theme_css) and 'demo-note-footer' not in open(theme_css, encoding='utf-8').read():
        with open(theme_css, 'a', encoding='utf-8', newline='\n') as f:
            f.write(DEMO_CSS)

    open(os.path.join(HERE, '.nojekyll'), 'w').close()

    with open(os.path.join(HERE, 'robots.txt'), 'w', encoding='utf-8', newline='\n') as f:
        f.write('# Демо-прототип, в поиске ему делать нечего.\nUser-agent: *\nDisallow: /\n')

    print('страниц: %d, файлов-ассетов: %d' % (saved, len(done)))


if __name__ == '__main__':
    sys.exit(main())
