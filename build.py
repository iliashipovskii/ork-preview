# -*- coding: utf-8 -*-
"""
Сборка статического прототипа сайта ООО «ОРК».

Зачем генератор, а не руками сверстанные файлы: шапка, подвал и блок категории
повторяются на всех страницах, а данные каталога ниже устроены ровно так, как
потом будут лежать в WordPress (разделы = термины ork_category верхнего уровня,
категории = дочерние термины, модели = записи ork_model). Когда дойдём до темы,
структура переедет один в один, а HTML станет шаблоном блока.

Запуск:  python preview/build.py
"""

import os
from datetime import date

HERE = os.path.dirname(os.path.abspath(__file__))

PHONE = '+7 (473) 250-41-17'
PHONE_HREF = 'tel:+74732504117'
MAIL = 'sale@ork-zavod.ru'
ADDRESS = 'Воронеж, ул. Остужева, 52Б'
HOURS = 'Пн–Пт 8:00–17:00'

# Пункты меню: (slug папки, подпись). slug '' — главная.
MENU = [
    ('stoylovoe-oborudovanie', 'Стойловое оборудование'),
    ('navozoudalenie', 'Навозоудаление'),
    ('ohlazhdenie-moloka', 'Охлаждение молока'),
    ('zapchasti', 'Запчасти'),
    ('kontakty', 'Контакты'),
]

# --- Данные каталога -------------------------------------------------------
# cats: id якоря, название, описание, картинка (или None → заглушка),
#       models: список моделей; у модели label для вкладки, title и specs.

STALL = [
    {
        'id': 'ograzhdeniya-kormovogo-stola',
        'name': 'Ограждения кормового стола',
        'desc': 'Самофиксирующиеся решётки вдоль кормового прохода: корова сама заходит в ячейку, '
                'оператор фиксирует всю секцию одним рычагом.',
        'img': ('feed.svg', 'Кормовая решётка'),
        'specs': [('Длина секции', '3 000 мм, 5 мест'), ('Шаг ячейки', '600 мм'), ('Фиксация', 'групповая, рычагом')],
    },
    {
        'id': 'razdelitelnye-sekcii',
        'name': 'Разделительные секции',
        'desc': 'Боксы для отдыха коров. Изогнутая форма не мешает животному вставать и ложиться, '
                'а нижняя дуга задаёт правильное положение в стойле.',
        'img': ('stall.svg', 'Стойловые разделители'),
        'specs': [('Труба', 'Ø 48 × 2,5 мм, Ст3'), ('Покрытие', 'горячее цинкование, 80 мкм'),
                  ('Длина бокса', '2 000 / 2 200 / 2 400 мм')],
    },
    {
        'id': 'kalitki-i-zabory',
        'name': 'Калитки и заборы',
        'desc': 'Секционные ограждения для загонов и проходов. Телескопические калитки подгоняются '
                'по месту без резки и сварки.',
        'img': ('gate.svg', 'Калитка'),
        'specs': [('Ширина калитки', '1 000 – 6 000 мм'), ('Высота', '1 200 мм'),
                  ('Крепление', 'на стойку Ø 108 мм')],
    },
    {
        'id': 'ograzhdenie-poilok',
        'name': 'Ограждение поилок',
        'desc': 'Защитные рамы вокруг групповых поилок: коровы не толкаются и не опрокидывают поилку, '
                'а оператор легко подходит для мойки.',
        'img': ('drinker.svg', 'Групповая поилка'),
        'specs': [('Труба', 'Ø 48 × 2,5 мм'), ('Размер', 'под поилки 1,5 – 3 м'),
                  ('Покрытие', 'горячее цинкование')],
    },
]

MANURE = [
    {
        'id': 'nasosy',
        'name': 'Насосы',
        'desc': 'Перекачивают жидкий навоз из приямков в лагуну или цистерну. Погружные — для каналов, '
                'шнековые — для густой массы.',
        'img': None,
        'models': [
            {'label': 'НЦ-30', 'title': 'Погружной насос НЦ-30',
             'specs': [('Производительность', '30 м³/ч'), ('Мощность', '5,5 кВт'), ('Напор', '12 м')]},
            {'label': 'НЦ-55', 'title': 'Погружной насос НЦ-55',
             'specs': [('Производительность', '55 м³/ч'), ('Мощность', '11 кВт'), ('Напор', '15 м')]},
            {'label': 'НШ-80', 'title': 'Шнековый насос НШ-80',
             'specs': [('Производительность', '80 м³/ч'), ('Мощность', '15 кВт'), ('Напор', '20 м')]},
        ],
    },
    {
        'id': 'meshalki',
        'name': 'Мешалки',
        'desc': 'Перемешивают навоз в хранилище перед откачкой, чтобы не оседала корка и не забивались насосы.',
        'img': None,
        'models': [
            {'label': 'ММ-7,5', 'title': 'Мешалка ММ-7,5',
             'specs': [('Мощность', '7,5 кВт'), ('Длина вала', '4 м'), ('Объём хранилища', 'до 800 м³')]},
            {'label': 'ММ-15', 'title': 'Мешалка ММ-15',
             'specs': [('Мощность', '15 кВт'), ('Длина вала', '6 м'), ('Объём хранилища', 'до 2 000 м³')]},
        ],
    },
    {
        'id': 'skrepery',
        'name': 'Скреперы',
        'desc': 'Дельта-скреперы для проходов с решётчатым и сплошным полом. Складываются на обратном ходу '
                'и не мешают коровам.',
        'img': ('scraper.svg', 'Скрепер'),
        'models': [
            {'label': 'Дельта-скрепер', 'title': 'Дельта-скрепер',
             'specs': [('Ширина прохода', '2 – 4 м'), ('Нож', 'сталь + полиуретан'), ('Привод', 'тросовый')]},
            {'label': 'Для решётчатого пола', 'title': 'Скрепер для решётчатого пола',
             'specs': [('Ширина прохода', '1,8 – 3,6 м'), ('Нож', 'сталь, складной'), ('Привод', 'цепной')]},
        ],
    },
    {
        'id': 'skrepernye-stancii',
        'name': 'Скреперные станции',
        'desc': 'Приводят скреперы в движение по расписанию. Один привод обслуживает до двух проходов.',
        'img': None,
        'models': [
            {'label': '', 'title': 'Приводная станция',
             'specs': [('Мощность', '1,5 кВт'), ('Скорость', '3 м/мин'), ('Длина канала', 'до 150 м')]},
        ],
    },
    {
        'id': 'separatory',
        'name': 'Сепараторы',
        'desc': 'Разделяют навоз на жидкую и твёрдую фракции. Твёрдая идёт на подстилку или компост, '
                'жидкая — на поля.',
        'img': None,
        'models': [
            {'label': '', 'title': 'Шнековый сепаратор СШ-20',
             'specs': [('Производительность', '20 м³/ч'), ('Мощность', '5,5 кВт'), ('Влажность фракции', '70 %')]},
        ],
    },
    {
        'id': 'transportery',
        'name': 'Транспортёры',
        'desc': 'Скребковые транспортёры для привязного содержания: убирают навоз из каналов и грузят в прицеп.',
        'img': None,
        'models': [
            {'label': '', 'title': 'Скребковый транспортёр',
             'specs': [('Длина цепи', 'до 160 м'), ('Скорость', '0,19 м/с'), ('Мощность', '4 кВт')]},
        ],
    },
]

COOLING = [
    {
        'id': 'om-1000',
        'kicker': 'Открытого типа',
        'name': 'ОМ-1000',
        'desc': 'Горизонтальный танк для ферм на 40–80 коров. Откидная крышка, мешалка и пульт '
                'с контролем температуры.',
        'img': ('tank.svg', 'Охладитель ОМ-1000'),
        'pdf': 'Паспорт (PDF, 1,2 МБ)',
        'specs': [('Объём', '1 000 л'), ('Охлаждение', 'с +35 до +4 °C за 3 ч'),
                  ('Ёмкость', 'AISI 304, 2 мм'), ('Мощность', '2,2 кВт, 380 В')],
    },
    {
        'id': 'oz-3000',
        'kicker': 'Закрытого типа',
        'name': 'ОЗ-3000',
        'desc': 'Вертикальный герметичный танк с двойной стенкой для ферм на 100–200 коров. '
                'Встроенная автомойка и журнал температур для молокозавода.',
        'img': ('tank2.svg', 'Охладитель ОЗ-3000'),
        'pdf': 'Паспорт (PDF, 1,8 МБ)',
        'specs': [('Объём', '3 000 л'), ('Охлаждение', 'с +35 до +4 °C за 2,5 ч'),
                  ('Ёмкость', 'AISI 304, двойная стенка'), ('Мощность', '5,5 кВт, 380 В')],
    },
]


# --- Кусочки разметки -------------------------------------------------------

LOGO_SVG = (
    '<svg class="logo__symbol" viewBox="0 0 439.7 140.46" fill="currentColor" fill-rule="evenodd" '
    'aria-hidden="true" focusable="false">'
    '<path d="M0 0H140.4624V140.4607H0Z M12.2145 12.2156H128.2479V128.2476H12.2145Z"/>'
    '<path d="M149.6217 0H290.0841V140.4607H149.6217Z M161.8362 12.2156H277.8696V128.2476H161.8362Z"/>'
    '<path d="M299.2394 0H439.6989V140.4607H299.2394Z M311.4511 12.2156H427.4844V128.2476H311.4511Z"/>'
    '<circle cx="70.2304" cy="70.2318" r="24.3082"/>'
    '<path d="M224.0618 75.4231H265.6511V117.0122H224.0618Z"/>'
    '<path d="M366.6564 70.2318L415.27 42.5602V97.9005Z"/>'
    '</svg>'
)

ICON_PHONE = ('<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
              'stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
              '<path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 '
              '2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1.9.4 1.8.7 2.7a2 2 0 0 1-.5 2.1L8 9.8a16 16 0 0 0 6 '
              '6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.7.7a2 2 0 0 1 1.7 2z"/></svg>')

ICON_BURGER = ('<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
               'stroke-width="2" stroke-linecap="round" aria-hidden="true">'
               '<line x1="4" y1="7" x2="20" y2="7"/><line x1="4" y1="12" x2="20" y2="12"/>'
               '<line x1="4" y1="17" x2="20" y2="17"/></svg>')


def head(title, root, description):
    return f'''<!doctype html>
<html lang="ru">
<head>
<script>document.documentElement.classList.add('js')</script>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} — ООО «ОРК»</title>
<meta name="description" content="{description}">
<!-- Прототип: в поиске ему делать нечего. -->
<meta name="robots" content="noindex, nofollow">
<meta name="theme-color" content="#0f2a21">
<link rel="icon" href="{root}assets/img/logo.svg" type="image/svg+xml">
<link rel="preload" href="{root}assets/fonts/onest-cyrillic-var.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="{root}assets/fonts/unbounded-cyrillic-var.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{root}assets/css/fonts.css">
<link rel="stylesheet" href="{root}assets/css/site.css">
</head>
<body>
<div class="demo-note">
<b>Демонстрационная версия.</b> Тексты, цифры, названия моделей и картинки — заглушки, их заменим на настоящие.
</div>
'''


def header(root, current):
    links = []
    for slug, label in MENU:
        href = f'{root}{slug}/'
        cur = ' aria-current="page"' if slug == current else ''
        links.append(f'<a href="{href}"{cur}>{label}</a>')
    nav = '\n'.join(links)
    return f'''<header class="site-header container" id="site-header">
<a class="logo" href="{root}">
{LOGO_SVG}
<span class="logo__mark">ОРК</span>
<span class="logo__tagline">завод фермерского оборудования</span>
</a>
<nav class="site-nav" id="site-nav" aria-label="Основное меню">
{nav}
<div class="site-nav__contacts">
<a href="{PHONE_HREF}">{PHONE}</a>
<a href="mailto:{MAIL}">{MAIL}</a>
</div>
</nav>
<a class="header-phone" href="{PHONE_HREF}">{PHONE}</a>
<div class="header-actions">
<a href="{PHONE_HREF}" aria-label="Позвонить">{ICON_PHONE}</a>
<button type="button" id="menu-toggle" aria-label="Меню" aria-expanded="false" aria-controls="site-nav">{ICON_BURGER}</button>
</div>
</header>'''


def footer(root):
    return f'''<footer class="site-footer">
<div class="container site-footer__inner">
<div class="site-footer__brand">
<span class="site-footer__logo">{LOGO_SVG}<span class="site-footer__mark">ОРК</span></span>
<span>© {date.today().year} ООО «ОРК»</span>
</div>
<div>{ADDRESS}<br>{HOURS}</div>
<div><a href="{PHONE_HREF}">{PHONE}</a><br><a href="mailto:{MAIL}">{MAIL}</a></div>
</div>
</footer>
<script src="{root}assets/js/site.js" defer></script>
</body>
</html>
'''


def page_hero(root, current, title, lead):
    label = dict(MENU)[current]
    return f'''<section class="site-hero page-hero">
<img class="site-hero__image" src="{root}assets/img/hero.svg" alt="">
<div class="site-hero__scrim"></div>
<div class="site-hero__inner">
{header(root, current)}
<div class="container page-hero__body">
<div class="breadcrumbs"><a href="{root}">Главная</a> / {label}</div>
<h1>{title}</h1>
<p class="page-hero__lead">{lead}</p>
</div>
</div>
</section>'''


def subnav(cats):
    items = '\n'.join(f'<a href="#{c["id"]}">{c["name"]}</a>' for c in cats)
    return f'''<nav class="subnav" aria-label="Категории раздела">
<div class="container subnav__list">
{items}
</div>
</nav>'''


def specs_block(specs):
    cls = 'specs specs--4' if len(specs) == 4 else 'specs'
    items = '\n'.join(
        f'<div class="specs__item"><span class="specs__key">{k}</span>'
        f'<span class="specs__value">{v}</span></div>' for k, v in specs)
    return f'<div class="{cls}">\n{items}\n</div>'


def media_block(root, img, fallback_title, height_note=''):
    if img:
        src, alt = img
        return f'<div class="media"><img src="{root}assets/img/{src}" alt="{alt}" loading="lazy"></div>'
    # Обёртка нужна: прямые текстовые узлы во flex-контейнере становятся
    # отдельными flex-элементами, и <br> между ними не срабатывает.
    return (f'<div class="media media--placeholder"><span>Фото: {fallback_title}'
            f'<em>заменим на настоящее</em></span></div>')


def links_block(pdf_label='Паспорт изделия (PDF) ›'):
    return (f'<div class="inline-links">'
            f'<a href="mailto:{MAIL}">Узнать цену ›</a>'
            f'<a href="#" onclick="return false">{pdf_label}</a>'
            f'</div>')


def simple_category(root, cat, alt_bg):
    """Категория без переключателя: заголовок → фото → характеристики."""
    bg = ' is-alt' if alt_bg else ''
    return f'''<section class="catalog-section{bg}" id="{cat['id']}">
<div class="container catalog-section__inner reveal">
<div class="catalog-section__head">
<h2>{cat['name']}</h2>
<p class="catalog-section__desc">{cat['desc']}</p>
{links_block()}
</div>
{media_block(root, cat.get('img'), cat['name'])}
{specs_block(cat['specs'])}
</div>
</section>'''


def tabbed_category(root, cat, alt_bg):
    """Категория с несколькими моделями: вкладки переключают содержимое.
    Без JS виден первый вариант — это нормальная деградация."""
    bg = ' is-alt' if alt_bg else ''
    models = cat['models']
    tabs = ''
    if len(models) > 1:
        buttons = '\n'.join(
            f'<button type="button" role="tab" id="tab-{cat["id"]}-{i}" '
            f'aria-controls="panel-{cat["id"]}-{i}" aria-selected="{"true" if i == 0 else "false"}">'
            f'{m["label"]}</button>' for i, m in enumerate(models))
        tabs = f'<div class="model-tabs" role="tablist" aria-label="Модели: {cat["name"]}">\n{buttons}\n</div>'

    panels = []
    for i, m in enumerate(models):
        hidden = '' if i == 0 else ' hidden'
        panels.append(f'''<div class="model" role="tabpanel" id="panel-{cat['id']}-{i}"
aria-labelledby="tab-{cat['id']}-{i}"{hidden}>
<div class="model__head">
<div class="model__title">{m['title']}</div>
{links_block('Паспорт (PDF) ›')}
</div>
{media_block(root, cat.get('img'), m['title'])}
{specs_block(m['specs'])}
</div>''')

    return f'''<section class="catalog-section{bg}" id="{cat['id']}">
<div class="container catalog-section__inner reveal">
<div class="catalog-section__head">
<h2>{cat['name']}</h2>
<p class="catalog-section__desc">{cat['desc']}</p>
</div>
{tabs}
{chr(10).join(panels)}
</div>
</section>'''


def cta(title, text=None, show_phone=False, slim=False):
    cls = 'cta cta--slim' if slim else 'cta'
    body = f'<p>{text}</p>' if text else ''
    phone = f'<a class="cta__phone" href="{PHONE_HREF}">{PHONE}</a>' if show_phone else ''
    return f'''<section class="{cls}">
<div class="container cta__inner">
<div class="cta__text">
<h2>{title}</h2>
{body}
</div>
<div class="cta__contacts">
{phone}
<a class="cta__mail" href="mailto:{MAIL}">{MAIL}</a>
</div>
</div>
</section>'''


# --- Страницы ---------------------------------------------------------------

def build_index():
    root = ''
    cards = [
        ('stoylovoe-oborudovanie', 'stall.svg', 'Стойловое оборудование',
         'Ограждения кормового стола, разделительные секции, калитки'),
        ('navozoudalenie', 'scraper.svg', 'Навозоудаление', 'Насосы, мешалки, скреперы, сепараторы'),
        ('ohlazhdenie-moloka', 'tank.svg', 'Охлаждение молока', 'Танки-охладители от 1 000 до 3 000 л'),
        ('zapchasti', 'parts.svg', 'Запчасти', 'Звёздочки, хомуты, крепёж, комплектующие'),
    ]
    cards_html = '\n'.join(f'''<a class="product-card" href="{root}{slug}/">
<img src="{root}assets/img/{img}" alt="{title}" loading="lazy">
<div class="product-card__body">
<span class="product-card__title">{title}</span>
<span class="product-card__desc">{desc}</span>
<span class="product-card__more">Подробнее ›</span>
</div>
</a>''' for slug, img, title, desc in cards)

    facts = [('18 лет', 'на рынке'), ('1 400+', 'ферм оснащено'),
             ('34', 'региона России и СНГ'), ('5 лет', 'гарантия на металлоконструкции')]
    facts_html = '\n'.join(
        f'<div class="facts__item"><span class="facts__value">{v}</span>'
        f'<span class="facts__label">{l}</span></div>' for v, l in facts)

    return (head('Оборудование для молочных ферм', root,
                 'ООО «ОРК» — производство стойлового оборудования, систем навозоудаления '
                 'и охлаждения молока. Воронеж.')
            + f'''<section class="site-hero">
<img class="site-hero__image" src="{root}assets/img/hero.svg" alt="">
<div class="site-hero__scrim"></div>
<div class="site-hero__inner">
{header(root, None)}
<div class="container hero-body">
<h1>Оборудование для молочных ферм</h1>
<p class="hero-body__lead">Стойловое оборудование, навозоудаление и охлаждение молока.
Производим в Воронеже с 2008 года.</p>
<div class="hero-links">
<a href="{root}stoylovoe-oborudovanie/">Каталог ›</a>
<a class="is-secondary" href="{root}kontakty/">Связаться ›</a>
</div>
<div class="hero-cta">
<a class="hero-cta__call" href="{PHONE_HREF}">{PHONE}</a>
<a class="hero-cta__mail" href="mailto:{MAIL}">{MAIL}</a>
</div>
</div>
</div>
</section>

<section class="facts">
<div class="container facts__grid">
{facts_html}
</div>
</section>

<section class="products">
<div class="container">
<h2 class="products__head">Продукция</h2>
<div class="products__grid reveal">
{cards_html}
</div>
</div>
</section>

<section class="production">
<img class="production__image" src="{root}assets/img/workshop.svg" alt="Цех" loading="lazy">
<div class="production__scrim"></div>
<div class="container production__body">
<h2>Своё производство полного цикла</h2>
<p>Цех 12 000 м². Режем, гнём и варим трубу на своём оборудовании, цинкуем горячим способом.
Поэтому стойла не ржавеют годами, а сроки не зависят от подрядчиков.</p>
<div class="production__facts">
<div><strong>80 мкм</strong>слой цинка</div>
<div><strong>Бесплатно</strong>проект коровника</div>
<div><strong>Свои бригады</strong>монтаж под ключ</div>
</div>
</div>
</section>

'''
            + cta('Посчитаем оборудование под вашу ферму',
                  'Напишите, сколько голов и какой коровник, — пришлём расчёт за 1 рабочий день.',
                  show_phone=True)
            + footer(root))


def build_stall():
    root, slug = '../', 'stoylovoe-oborudovanie'
    sections = '\n\n'.join(simple_category(root, c, i % 2 == 1) for i, c in enumerate(STALL))
    return (head('Стойловое оборудование', root,
                 'Ограждения кормового стола, разделительные секции, калитки и ограждения поилок.')
            + page_hero(root, slug, 'Стойловое оборудование',
                        'Для беспривязного и привязного содержания, от 50 до 2 000 голов. '
                        'Труба Ст3, горячее цинкование, сборка на болтах без сварки на месте.')
            + '\n' + subnav(STALL) + '\n\n' + sections + '\n\n'
            + cta('Пришлите план коровника — подберём комплект', slim=True)
            + footer(root))


def build_manure():
    root, slug = '../', 'navozoudalenie'
    sections = '\n\n'.join(tabbed_category(root, c, i % 2 == 1) for i, c in enumerate(MANURE))
    return (head('Навозоудаление', root,
                 'Насосы, мешалки, скреперы, скреперные станции, сепараторы и транспортёры.')
            + page_hero(root, slug, 'Навозоудаление',
                        'Полная цепочка: уборка из проходов, перекачка, перемешивание '
                        'и разделение навоза на фракции.')
            + '\n' + subnav(MANURE) + '\n\n' + sections + '\n\n'
            + cta('Подберём систему навозоудаления под ваш коровник', slim=True)
            + footer(root))


def build_cooling():
    root, slug = '../', 'ohlazhdenie-moloka'
    blocks = []
    for i, m in enumerate(COOLING):
        bg = ' is-alt' if i % 2 == 1 else ''
        blocks.append(f'''<section class="catalog-section{bg}" id="{m['id']}">
<div class="container catalog-section__inner reveal">
<div class="catalog-section__head">
<span class="kicker">{m['kicker']}</span>
<h2>{m['name']}</h2>
<p class="catalog-section__desc">{m['desc']}</p>
{links_block(m['pdf'] + ' ›')}
</div>
{media_block(root, m['img'], m['name'])}
{specs_block(m['specs'])}
</div>
</section>''')
    return (head('Охлаждение молока', root,
                 'Танки-охладители молока из нержавеющей стали AISI 304, от 1 000 до 3 000 литров.')
            + page_hero(root, slug, 'Охлаждение молока',
                        'Танки-охладители из пищевой нержавейки AISI 304. Молоко остывает до +4 °C '
                        'за 3 часа и сохраняет сорт «высший».')
            + '\n\n' + '\n\n'.join(blocks) + '\n\n'
            + cta('Подберём объём танка под ваш удой', slim=True)
            + footer(root))


def build_parts():
    root, slug = '../', 'zapchasti'
    return (head('Запчасти', root, 'Запчасти и комплектующие к оборудованию ООО «ОРК».')
            + page_hero(root, slug, 'Запчасти',
                        'Комплектующие к нашему оборудованию и расходники: звёздочки, цепи, '
                        'ножи скреперов, крепёж.')
            + f'''
<section class="catalog-section">
<div class="container catalog-section__inner reveal">
{media_block(root, ('parts.svg', 'Запчасти и комплектующие'), 'Запчасти')}
</div>
</section>

<section class="empty-section is-alt">
<div class="container empty-section__inner reveal">
<h2>Раздел наполним по вашему списку</h2>
<p>Страница работает на том же шаблоне, что «Стойловое оборудование»: категории идут блоками
подряд, внутри категории — переключатель моделей. Как только пришлёте перечень запчастей
с характеристиками, раздел соберётся за вечер.</p>
</div>
</section>

'''
            + cta('Нужна запчасть — напишите модель и год выпуска', slim=True)
            + footer(root))


def build_contacts():
    root, slug = '../', 'kontakty'
    return (head('Контакты', root, 'ООО «ОРК», Воронеж, ул. Остужева, 52Б. Телефон и почта отдела продаж.')
            + f'''<section class="site-hero">
<div class="site-hero__inner">
{header(root, slug)}
<div class="container page-hero__body page-hero__body--short">
<h1>Контакты</h1>
</div>
</div>
</section>

<section class="contacts">
<div class="container contacts__grid">
<div class="contacts__card">
<p class="contacts__lead">Напишите, сколько голов и какой коровник, — ответим с ценой и сроками
за 1 рабочий день.</p>
<div class="contacts__field">
<span class="contacts__label">Отдел продаж</span>
<a class="contacts__phone" href="{PHONE_HREF}">{PHONE}</a>
</div>
<div class="contacts__field">
<span class="contacts__label">Почта</span>
<a class="contacts__mail" href="mailto:{MAIL}">{MAIL}</a>
</div>
<div class="contacts__pair">
<div class="contacts__field">
<span class="contacts__label">Адрес</span>
<span class="contacts__value">Воронеж,<br>ул. Остужева, 52Б</span>
</div>
<div class="contacts__field">
<span class="contacts__label">Режим работы</span>
<span class="contacts__value">Пн–Пт<br>8:00–17:00</span>
</div>
</div>
<div class="contacts__legal">ООО «ОРК» · ИНН 3662123456 · ОГРН 1083668012345</div>
</div>
<div class="map" role="img" aria-label="Схема проезда, здесь будет Яндекс.Карта">
<div class="map__road"></div>
<div class="map__road map__road--v"></div>
<div class="map__park"></div>
<div class="map__pin">
<div class="map__pin-label">ОРК, производство</div>
<svg width="48" height="60" viewBox="0 0 24 30" fill="#1E5945" stroke="#FFFFFF" stroke-width="1.5" aria-hidden="true">
<path d="M12 1C6.5 1 2 5.3 2 10.7 2 18 12 29 12 29s10-11 10-18.3C22 5.3 17.5 1 12 1z"/>
<circle cx="12" cy="11" r="3.5" fill="#FFFFFF" stroke="none"/>
</svg>
</div>
<div class="map__note">здесь будет Яндекс.Карта</div>
</div>
</div>
</section>

'''
            + footer(root))


PAGES = {
    'index.html': build_index,
    'stoylovoe-oborudovanie/index.html': build_stall,
    'navozoudalenie/index.html': build_manure,
    'ohlazhdenie-moloka/index.html': build_cooling,
    'zapchasti/index.html': build_parts,
    'kontakty/index.html': build_contacts,
}


def main():
    for rel, fn in PAGES.items():
        path = os.path.join(HERE, rel)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        html = fn()
        with open(path, 'w', encoding='utf-8', newline='\n') as f:
            f.write(html)
        print('%-40s %6d b' % (rel, len(html.encode('utf-8'))))
    # Пустой .nojekyll: GitHub Pages иначе прогоняет всё через Jekyll
    # и выкидывает папки/файлы, начинающиеся с подчёркивания.
    open(os.path.join(HERE, '.nojekyll'), 'w').close()

    # Демо не должно попасть в поиск: и robots.txt, и meta robots на каждой странице.
    with open(os.path.join(HERE, 'robots.txt'), 'w', encoding='utf-8', newline='\n') as f:
        f.write('# Демо-прототип, в поиске ему делать нечего.\n'
                'User-agent: *\n'
                'Disallow: /\n')
    print('готово')


if __name__ == '__main__':
    main()
