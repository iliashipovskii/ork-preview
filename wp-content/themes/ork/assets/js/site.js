/* Ванильный JS прототипа. Без зависимостей, всё опционально:
   при выключенном JS страница остаётся читаемой (видна первая модель,
   меню раскрыто ссылками, якоря работают обычным образом). */

(function () {
	'use strict';

	/* --- Бургер-меню на телефоне ---------------------------------------- */

	var header = document.getElementById('site-header');
	var toggle = document.getElementById('menu-toggle');

	if (header && toggle) {
		toggle.addEventListener('click', function () {
			var open = header.classList.toggle('is-open');
			toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
		});

		// Клик по пункту меню — закрыть панель.
		header.querySelectorAll('.site-nav a').forEach(function (link) {
			link.addEventListener('click', function () {
				header.classList.remove('is-open');
				toggle.setAttribute('aria-expanded', 'false');
			});
		});

		document.addEventListener('keydown', function (e) {
			if (e.key === 'Escape' && header.classList.contains('is-open')) {
				header.classList.remove('is-open');
				toggle.setAttribute('aria-expanded', 'false');
				toggle.focus();
			}
		});
	}

	/* --- Подсветка активной категории в липком подменю ------------------- */

	var subnavLinks = document.querySelectorAll('.subnav__list a');

	if (subnavLinks.length && 'IntersectionObserver' in window) {
		var byId = {};
		var sections = [];

		subnavLinks.forEach(function (link) {
			var id = link.getAttribute('href').slice(1);
			var section = document.getElementById(id);
			if (section) {
				byId[id] = link;
				sections.push(section);
			}
		});

		var visible = {};

		var setActive = function (id) {
			subnavLinks.forEach(function (link) {
				link.classList.toggle('is-active', link === byId[id]);
			});
			// Длинное подменю скроллим так, чтобы активный пункт был виден.
			var active = byId[id];
			var list = active && active.parentNode;
			if (active && list && list.scrollWidth > list.clientWidth) {
				var left = active.offsetLeft - list.clientWidth / 2 + active.offsetWidth / 2;
				list.scrollTo({ left: left, behavior: 'smooth' });
			}
		};

		var observer = new IntersectionObserver(function (entries) {
			entries.forEach(function (entry) {
				visible[entry.target.id] = entry.isIntersecting;
			});
			// Активна самая верхняя из видимых секций.
			for (var i = 0; i < sections.length; i++) {
				if (visible[sections[i].id]) {
					setActive(sections[i].id);
					break;
				}
			}
		}, { rootMargin: '-72px 0px -55% 0px' });

		sections.forEach(function (section) {
			observer.observe(section);
		});

		if (sections.length) {
			setActive(sections[0].id);
		}
	}

	/* --- Переключатель моделей внутри категории -------------------------- */

	document.querySelectorAll('.model-tabs').forEach(function (tablist) {
		var tabs = Array.prototype.slice.call(tablist.querySelectorAll('button[role="tab"]'));

		var select = function (index, moveFocus) {
			tabs.forEach(function (tab, i) {
				var panel = document.getElementById(tab.getAttribute('aria-controls'));
				var on = i === index;
				tab.setAttribute('aria-selected', on ? 'true' : 'false');
				tab.setAttribute('tabindex', on ? '0' : '-1');
				if (panel) {
					panel.hidden = !on;
				}
			});
			if (moveFocus) {
				tabs[index].focus();
			}
		};

		tabs.forEach(function (tab, i) {
			tab.setAttribute('tabindex', i === 0 ? '0' : '-1');
			tab.addEventListener('click', function () {
				select(i, false);
			});
		});

		// Стрелками — как положено для role="tablist".
		tablist.addEventListener('keydown', function (e) {
			var current = tabs.indexOf(document.activeElement);
			if (current < 0) {
				return;
			}
			var next = null;
			if (e.key === 'ArrowRight') {
				next = (current + 1) % tabs.length;
			} else if (e.key === 'ArrowLeft') {
				next = (current - 1 + tabs.length) % tabs.length;
			} else if (e.key === 'Home') {
				next = 0;
			} else if (e.key === 'End') {
				next = tabs.length - 1;
			}
			if (next !== null) {
				e.preventDefault();
				select(next, true);
			}
		});
	});

	/* --- Мягкое появление блоков при скролле ----------------------------- */

	var reveals = document.querySelectorAll('.reveal');
	var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

	if (reveals.length && 'IntersectionObserver' in window && !reduced) {
		var revealObserver = new IntersectionObserver(function (entries, obs) {
			entries.forEach(function (entry) {
				if (entry.isIntersecting) {
					entry.target.classList.add('is-visible');
					obs.unobserve(entry.target);
				}
			});
		}, { rootMargin: '0px 0px -10% 0px' });

		reveals.forEach(function (el) {
			revealObserver.observe(el);
		});
	} else {
		reveals.forEach(function (el) {
			el.classList.add('is-visible');
		});
	}
})();

/* =========================================================================
   Лайтбокс и слайдер.

   Своя реализация вместо Fancybox и Swiper: Fancybox тянет jQuery, Swiper
   весит под 150 КБ, а по требованиям проекта на фронте нет ни jQuery, ни
   тяжёлых библиотек, и нужен зелёный PageSpeed. Здесь ~4 КБ без зависимостей.
   ========================================================================= */

(function () {
	'use strict';

	var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

	/* --- Лайтбокс -------------------------------------------------------- */

	var box = null;
	var group = [];
	var index = 0;
	var lastFocused = null;

	var build = function () {
		if (box) { return box; }

		box = document.createElement('div');
		box.className = 'lightbox';
		box.setAttribute('role', 'dialog');
		box.setAttribute('aria-modal', 'true');
		box.setAttribute('aria-label', 'Просмотр изображения');
		box.hidden = true;
		box.innerHTML =
			'<button type="button" class="lightbox__close" aria-label="Закрыть">&times;</button>' +
			'<button type="button" class="lightbox__nav lightbox__nav--prev" aria-label="Предыдущее">&#8249;</button>' +
			'<figure class="lightbox__figure"><img alt=""><figcaption></figcaption></figure>' +
			'<button type="button" class="lightbox__nav lightbox__nav--next" aria-label="Следующее">&#8250;</button>';

		document.body.appendChild(box);

		box.querySelector('.lightbox__close').addEventListener('click', close);
		box.querySelector('.lightbox__nav--prev').addEventListener('click', function () { step(-1); });
		box.querySelector('.lightbox__nav--next').addEventListener('click', function () { step(1); });

		// Клик по подложке закрывает, по самой картинке — нет.
		box.addEventListener('click', function (e) {
			if (e.target === box || e.target.classList.contains('lightbox__figure')) { close(); }
		});

		return box;
	};

	var show = function () {
		var item = group[index];
		var img = box.querySelector('img');
		var cap = box.querySelector('figcaption');

		img.src = item.href;
		img.alt = item.alt || '';
		cap.textContent = item.caption || '';
		cap.hidden = !item.caption;

		var many = group.length > 1;
		box.querySelector('.lightbox__nav--prev').hidden = !many;
		box.querySelector('.lightbox__nav--next').hidden = !many;
	};

	var step = function (delta) {
		index = (index + delta + group.length) % group.length;
		show();
	};

	function close() {
		if (!box || box.hidden) { return; }
		box.hidden = true;
		document.documentElement.classList.remove('is-lightbox-open');
		if (lastFocused) { lastFocused.focus(); }
	}

	var open = function (items, start, trigger) {
		group = items;
		index = start;
		lastFocused = trigger || null;
		build();
		show();
		box.hidden = false;
		document.documentElement.classList.add('is-lightbox-open');
		box.querySelector('.lightbox__close').focus();
	};

	// Ссылки на изображения открываются в лайтбоксе. Группа — ближайший
	// контейнер с data-lightbox-group, иначе все ссылки страницы.
	document.addEventListener('click', function (e) {
		var link = e.target.closest ? e.target.closest('a[data-lightbox]') : null;
		if (!link || e.metaKey || e.ctrlKey || e.shiftKey || 1 === e.button) { return; }

		e.preventDefault();

		var scope = link.closest('[data-lightbox-group]') || document;
		var links = Array.prototype.slice.call(scope.querySelectorAll('a[data-lightbox]'));

		var items = links.map(function (a) {
			var img = a.querySelector('img');
			return {
				href: a.getAttribute('href'),
				alt: img ? img.getAttribute('alt') : '',
				caption: a.getAttribute('data-caption') || ''
			};
		});

		open(items, links.indexOf(link), link);
	});

	document.addEventListener('keydown', function (e) {
		if (!box || box.hidden) { return; }
		if (e.key === 'Escape') { close(); }
		if (e.key === 'ArrowLeft') { step(-1); }
		if (e.key === 'ArrowRight') { step(1); }
	});

	/* --- Слайдер --------------------------------------------------------- */

	document.querySelectorAll('.slider').forEach(function (slider) {
		var track = slider.querySelector('.slider__track');
		var slides = Array.prototype.slice.call(slider.querySelectorAll('.slider__slide'));
		if (!track || slides.length < 2) { return; }

		var dotsBox = slider.querySelector('.slider__dots');
		var dots = [];
		var active = 0;

		var scrollTo = function (i, smooth) {
			track.scrollTo({
				left: slides[i].offsetLeft - track.offsetLeft,
				behavior: smooth && !reduced ? 'smooth' : 'auto'
			});
		};

		if (dotsBox) {
			slides.forEach(function (_, i) {
				var dot = document.createElement('button');
				dot.type = 'button';
				dot.className = 'slider__dot';
				dot.setAttribute('aria-label', 'Слайд ' + (i + 1));
				dot.addEventListener('click', function () { stop(); scrollTo(i, true); });
				dotsBox.appendChild(dot);
				dots.push(dot);
			});
		}

		var mark = function (i) {
			active = i;
			dots.forEach(function (d, n) {
				d.classList.toggle('is-active', n === i);
				d.setAttribute('aria-current', n === i ? 'true' : 'false');
			});
		};

		mark(0);

		// Какой слайд ближе к левому краю трека — тот и активен.
		var ticking = false;
		track.addEventListener('scroll', function () {
			if (ticking) { return; }
			ticking = true;
			window.requestAnimationFrame(function () {
				var nearest = 0;
				var best = Infinity;
				slides.forEach(function (slide, i) {
					var d = Math.abs(slide.offsetLeft - track.offsetLeft - track.scrollLeft);
					if (d < best) { best = d; nearest = i; }
				});
				mark(nearest);
				ticking = false;
			});
		}, { passive: true });

		slider.querySelectorAll('.slider__arrow').forEach(function (btn) {
			btn.addEventListener('click', function () {
				stop();
				var dir = btn.classList.contains('slider__arrow--next') ? 1 : -1;
				scrollTo((active + dir + slides.length) % slides.length, true);
			});
		});

		/* Автопрокрутка: только если задана и пользователь не просил
		   уменьшить движение. Останавливается от любого вмешательства,
		   чтобы не выдёргивать слайд из-под руки. */
		var delay = parseInt(slider.getAttribute('data-autoplay') || '0', 10);
		var timer = null;

		function stop() {
			if (timer) { window.clearInterval(timer); timer = null; }
		}

		if (delay > 0 && !reduced) {
			timer = window.setInterval(function () {
				scrollTo((active + 1) % slides.length, true);
			}, delay);

			['mouseenter', 'focusin', 'touchstart', 'pointerdown'].forEach(function (ev) {
				slider.addEventListener(ev, stop, { passive: true });
			});

			// Невидимая вкладка не должна крутить слайды вхолостую.
			document.addEventListener('visibilitychange', function () {
				if (document.hidden) { stop(); }
			});
		}
	});
})();
