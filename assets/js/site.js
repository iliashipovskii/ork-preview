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
