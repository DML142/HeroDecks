#!/usr/bin/env python3
"""Build readable Markdown from the frozen factual and editorial datasets."""
import json,pathlib,re,math,collections,urllib.parse,os
R=pathlib.Path(__file__).resolve().parents[1]
load=lambda p:json.loads((R/p).read_text())
C={x['id']:x for x in load('data/cards.json')};H={x['id']:x for x in load('data/heroes.json')};D=load('data/decks.json');A=load('data/deck-analysis.json');P=load('data/card-analysis.json')
def write(path,text):
 p=R/path;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text.rstrip()+'\n')
def slug(s):return re.sub('[^a-z0-9]+','_',s.lower()).strip('_')
def cardpath(c):return f"cards/{c['faction']}/{slug(c['class'])}/{slug(c['name'])}.md"
def deckpath(d):return f"decks/{H[d['hero']]['faction']}/{d['hero']}/{d['slug']}.md"
def link(label,path,base):return f'[{label}]({os.path.relpath(R/path,(R/base).parent)})'
def cardlink(c,base):return link(c['name'],cardpath(c),base)
def stats(c):return f"{c['strength']}/{c['health']}" if c['strength'] is not None else '—'
def prob(n,draws):return (1-math.comb(40-n,draws)/math.comb(40,draws))*100
def clean(s):return s.replace('|',' / ').replace('\u200b','').replace('\ufeff','')
qreasons={1:'Ситуационный дополнительный ответ или финишер: его редко хотят видеть дважды, а основной план работает без него.',2:'Вспомогательный пакет: достаточно для доступа в длинной игре, но меньше риск получить несколько условных карт в начале.',3:'Часто нужный компонент, который делит место с другой ролью; четвёртая копия увеличила бы перекос руки.',4:'Максимальная плотность повторяемого основного действия/двигателя; ранняя или последовательная доступность важнее разнообразия.'}
counts=collections.Counter(c['evidence'] for c in C.values())
for c in C.values():
 path=cardpath(c);used=[d for d in D if any(x['card']==c['id'] for x in d['cards'])]
 text=f"# {c['name']}\n\n[Карты](../../README.md) · [Общий индекс](../../../README.md)\n\n| Поле | Значение |\n| --- | --- |\n| Сторона | {c['faction']} |\n| Класс | {c['class']} |\n| Стоимость | {c['cost']} |\n| Атака / здоровье | {stats(c)} |\n| Типы | {c['type']} |\n| Редкость / набор | {c['rarity']} / {c['set']} |\n| Допустима в обычной колоде | {'Да' if c['deckable'] else 'Нет / архивная недоступная запись'} |\n| Уровень источника | {c['evidence']} |\n\n## Что делает\n\n{clean(c['effect'])}\n\nТекст правил приведён на английском, чтобы не скрывать неоднозначность неофициального перевода. Числа и краткое правило — фактическая карточная запись; стратегическая оценка ниже — авторский разбор.\n\n"
 if c['id'] in P:text+='## Применение и цена альтернативы\n\n'+P[c['id']]['role']+'\n\n'+P[c['id']]['alternative']+'\n\n'
 if used:text+='## Разобранные колоды\n\n'+'\n'.join('- '+link(H[d['hero']]['name']+' — '+d['name'],deckpath(d),path) for d in used)+'\n\n'
 text+=f"## Источник\n\n[Индивидуальная статья вики]({c['wiki_url']}). Получено 2026-10-14. {c['source_note']}\n\nОбщая исходная структурная база: [PvZH Vault](https://pvzhvault.com/card_data.json); индивидуальная вики имеет приоритет при обнаруженном расхождении. Полная проверка в клиенте игры не выполнялась. Атрибуция и лицензия: [SOURCES](../../../SOURCES.md)."
 write(path,text)
for d in D:
 h=H[d['hero']];a=A[d['id']];path=deckpath(d);curve=collections.Counter();avg=0
 for x in d['cards']:curve[C[x['card']]['cost']]+=x['count'];avg+=C[x['card']]['cost']*x['count']
 text=f"# {h['name']} — {d['name']}\n\n[Колоды](../../README.md) · [Герой](../../../heroes/{h['faction']}/{h['id']}.md) · [Карты](../../../cards/README.md) · [Правила](../../../rules/README.md)\n\nДата исследования: **14 октября 2026**. Статус: **{d['category']}**. Состав: **40 карт**, классы **{' + '.join(h['classes'])}**. Средняя стоимость без скидок/ramp: **{avg/40:.2f}**.\n\n"
 if d['source_id']:text+=f"Исходный автор/credit: **{d['credit']}**; дата записи источника: **{d['source_date']}**; ID корпуса: `{d['source_id']}`. Название в корпусе может отличаться регистром/орфографией. Источник численного состава — [корпус](../../../research/meta-corpus.json), перенесённый из [базы опубликованных списков](https://pvzhvault.com/deck_database_final.json). Причины выбора/числа копий ниже — наша интерпретация, а не цитата намерений автора.\n\n"
 else:text+='Авторский кандидат HeroDecks по проверенным механикам. Не заявляется точной копией чужой рекомендованной колоды.\n\n'
 text+='Текст анализирует сильный кандидат под указанный план; оптимальность и винрейт не доказаны. Контрматчапы — механические гипотезы. [Метод исследования](../../../research/methodology.md).\n\n## Мышление при создании\n\n'+a['construction']+'\n\n## Почему именно этот герой\n\n'+a['hero_reason']+'\n\n'
 text+=f"Сигнатура: **{h['signature']}**. Другие силы: **{', '.join(h['powers'])}**. Они не входят в 40 карт, не выбираются как гарантированная стартовая сила и не существуют в четырёх копиях. Подробности: [все силы](../../../heroes/powers.md).\n\n"
 if d.get('changes'):
  text+='## Изменения относительно основы\n\n| Карта | Изменение |\n| --- | --- |\n'+'\n'.join(f"| {cardlink(C[x['card']],path)} | {x['delta']:+d} |" for x in d['changes'])+'\n\n'+a.get('variant_tradeoff','')+'\n\n'
 text+='## Каждая карта: правило, роль, альтернативы и количество\n\n'
 for x in d['cards']:
  c=C[x['card']];n=x['count'];p=P[c['id']]
  text+=f"### {n}× {c['name']}\n\n**Цена {c['cost']}; {stats(c)}; {c['class']}; {c['type']}.** [Карточная запись]({os.path.relpath(R/cardpath(c),(R/path).parent)}).\n\n**Правило:** {clean(c['effect'])}\n\n**Работа в плане:** {p['role']}\n\n**Почему эта карта, а не замена:** {p['alternative']}\n\n**Почему {n}×:** {a['notes'].get(c['id'],qreasons[n])} Вероятность увидеть хотя бы одну в исходных четырёх картах — **{prob(n,4):.1f}%**, в первых десяти обычных выборках — **{prob(n,10):.1f}%**. Это расчёт без mulligan, Conjure и изменения состава колоды; он показывает цену количества, но не доказывает оптимальность.\n\n"
 text+='## Mulligan и старт\n\n'+a['mulligan']+'\n\n## Как играть\n\n### Начало\n\n'+a['early']+'\n\n### Средняя игра\n\n'+a['mid']+'\n\n### Завершение\n\n'+a['late']+'\n\n## Проверенная последовательность и ограничения\n\n'+a['combo']+'\n\n'
 text+='Проверка здесь означает соответствие приведённым правилам, ресурсам, типам и фазам. Это не воспроизведение в клиенте. Если wiki-excerpt у нужной карты отличается от клиентского текста, пересчитайте последовательность по клиенту.\n\n## Контрколоды и реакция\n\n| Противник | Почему опасен и как менять решение |\n| --- | --- |\n'
 for name,why in a['counters']:
  match=next((v for v in D if v['name'].lower()==name.lower()),None);label=link(name,deckpath(match),path) if match else name
  text+=f'| {label} | {why} |\n'
 text+='\nНе указан процент побед: открытого актуального матчевого массива для этих конкретных 40-карточных версий нет. Смысл таблицы — какие механики обходят ваш план, а не обещание автоматической победы соперника.\n\n## Ошибки, которые ломают план\n\n'+'\n'.join('- '+m for m in a['mistakes'])+'\n\n## Кривая стоимости\n\n| Цена | Количество |\n| --- | --- |\n'+'\n'.join(f'| {k} | {v} |' for k,v in sorted(curve.items()))+'\n\n'
 text+='Кривая учитывает напечатанную текущую цену. Не включает скидки Teacher/Waxer/Terror-Former, расход эволюционного основания, Conjure-карты и вероятные непредсказуемые токены.\n\n## Итоговый список для сборки\n\n| Количество | Карта | Цена | Класс |\n| --- | --- | --- | --- |\n'
 text+='\n'.join(f"| {x['count']}× | {cardlink(C[x['card']],path)} | {C[x['card']]['cost']} | {C[x['card']]['class']} |" for x in d['cards'])+'\n\n**Всего: 40.**\n\n```text\n'+'\n'.join(f"{x['count']}x {C[x['card']]['name']}" for x in d['cards'])+'\n```\n\n'
 text+='## Логическая проверка\n\n- 40 карт, от одной до четырёх каждого имени.\n- Только сторона и два класса героя; токены и суперсилы не добавлены в основной список.\n- Для Evolution/Fusion в тексте указаны основания; событие получения карты не подменено подмешиванием в колоду.\n- Поздние удары учитывают ресурс, линию, блок и возможность ответа.\n- Изменение контрмета-версии сохраняет ровно 40 карт.\n\n[Общий журнал исправлений](../../../research/audit.md) · [Справочник синергий](../../../synergies/README.md).'
 write(path,text)
for h in H.values():
 hd=[d for d in D if d['hero']==h['id']];path=f"heroes/{h['faction']}/{h['id']}.md";a=A[hd[0]['id']]
 text=f"# {h['name']}\n\n[Все герои](../README.md) · [Главная](../../README.md)\n\nСторона: **{h['faction']}**. Классы: **{' + '.join(h['classes'])}**. Можно включать обычные доступные карты только этих классов и этой стороны. Совпадение классов у двух героев не даёт им одинаковые суперсилы.\n\n## Механический план героя\n\n{a['hero_reason']}\n\n## Четыре суперсилы\n\n- Сигнатура: **{h['signature']}**.\n"+'\n'.join('- '+v for v in h['powers'])+f"\n\n[Правила и эффекты всех сил](../powers.md). В начале приходит одна случайная сила; остальные получают через блок. Это отдельный набор от 40 карточек.\n\n## Колоды\n\n"+'\n'.join('- '+link(d['name']+' — '+d['category'],deckpath(d),path) for d in hd)+f"\n\n## Источник\n\n[Вики героя]({urllib.parse.quote(h['wiki_url'],safe=':/_-')}). Проверено по доступным индексированным материалам 2026-10-14; актуальная версия клиента отдельно не снималась. [Источники](../../SOURCES.md)."
 write(path,text)
write('cards/README.md','# Карты\n\n[Главная](../README.md) · [Герои](../heroes/README.md) · [Правила](../rules/README.md)\n\n503 записи основной базы, включая отдельные архивные/недоступные записи. Жетоны и суперсилы индексируются отдельно. `wiki-infobox` означает извлечение карточного блока, `wiki-search-excerpt` — неполную индексированную выдержку, `wiki-reviewed` — ручное исправление выявленного расхождения. Ни один статус не означает клиентскую проверку.\n\n| Класс | Карты |\n| --- | --- |\n'+'\n'.join(f'| {cl} | '+', '.join(link(c['name'],cardpath(c),'cards/README.md') for c in sorted(C.values(),key=lambda v:(v['cost'],v['name'])) if c['class']==cl)+' |' for cl in ['Guardian','Kabloom','Mega-Grow','Smarty','Solar','Beastly','Brainy','Crazy','Hearty','Sneaky'])+'\n\n[JSON-каталог](../data/cards.json) · [жетоны](tokens.md) · [суперсилы](../heroes/powers.md).')
write('heroes/README.md','# Все 22 героя\n\n[Главная](../README.md) · [Все колоды](../decks/README.md) · [Все суперсилы](powers.md)\n\n| Герой | Сторона | Классы | Сигнатура |\n| --- | --- | --- | --- |\n'+'\n'.join(f"| {link(h['name'],'heroes/'+h['faction']+'/'+h['id']+'.md','heroes/README.md')} | {h['faction']} | {' + '.join(h['classes'])} | {h['signature']} |" for h in H.values()))
write('decks/README.md','# Все 32 разобранные колоды\n\n[Главная](../README.md) · [Герои](../heroes/README.md) · [Техника построения](../research/deckbuilding.md)\n\n`source-based` и `source-based-alt` — численный состав найденного источника с нашим разбором. `theorycraft` — авторская конструкция. `countermeta-theorycraft` — проверенный по механикам кандидат против указанного плана; победы над метой не измерены.\n\n| Герой | Колода | Статус | Дата состава |\n| --- | --- | --- | --- |\n'+'\n'.join(f"| {H[d['hero']]['name']} | {link(d['name'],deckpath(d),'decks/README.md')} | {d['category']} | {d['source_date']} |" for d in D))
write('README.md',f'''# HeroDecks

Исследовательская база PvZ Heroes на русском: **22 героя · 32 подробных разбора колод · 503 карточные записи · корпус 2027 опубликованных списков**. Дата среза: **14 октября 2026 года**.

| Раздел | Что внутри |
| --- | --- |
| [Колоды](decks/README.md) | `decks/plants-or-zombies/hero_name/deck_name.md`: мышление, роль каждой карты, количества, альтернативы, mulligan, игра, контры и итоговые 40 карт |
| [Карты](cards/README.md) | Отдельные карточные файлы по стороне и классу; характеристики, правила, ссылки на колоды и источники |
| [Герои](heroes/README.md) | Классы, четыре силы, особенности плана и колоды каждого героя |
| [Суперсилы](heroes/powers.md) | Эффекты и ограничения отдельного набора сил |
| [Правила](rules/README.md) | Фазы, поле, ресурс, рука, победа и блок |
| [Механики](mechanics/README.md) | Traits, Evolution, Fusion, Freeze, Draw/Conjure и timing |
| [Синергии](synergies/README.md) | Условия, стоимость, смысл и способы разорвать комбинацию |
| [Построение колод](research/deckbuilding.md) | Роли, кривая, вероятность копий, mulligan и контроль неоптимальных замен |
| [Мета](research/meta.md) | Свежие рекомендации отдельно от исторических/видеосписков и авторских контрмета-кандидатов |
| [Корпус](research/corpus-index.md) | 2027 исходных записей, фильтрация и дубликаты; это не массив матчей |
| [Аудит](research/audit.md) | Исправления ошибок источников и границы проверки |
| [Источники](SOURCES.md) | Происхождение, атрибуция, лицензии и надёжность |

## Как читать силу колод

Подбор стремится к сильным согласованным планам. «Максимально сильная» версия зависит от состава противников, пилотирования и патча; без актуального матчевого массива глобальная оптимальность не доказана. Контрматчапы в разборе — вывод из механик, а не придуманный винрейт.

Последняя найденная явная правка рекомендательного поста сообщества — 25.09.2026. Не все её составы удалось получить напрямую из Tbot; устаревшие численные версии и авторские конструкции помечены. Поиск нашёл вики-источник каждой карточной записи, но {counts.get('wiki-search-excerpt',0)} записей имеют только неполную поисковую выдержку. Полный клиентский аудит не выполнялся.

## Проверка и обновление

```bash
python3 scripts/generate.py
python3 scripts/validate.py
```

Python 3, только стандартная библиотека. Редактируйте `data/*.json`, затем пересобирайте Markdown. Не меняйте сгенерированные составы отдельно от JSON: это создаёт расхождение между анализом и списком.

[Методология](research/methodology.md). Авторский разбор и адаптированные wiki-сведения: CC BY-SA 4.0 с оговорками [SOURCES](SOURCES.md). Игровые персонажи, изображения и оригинальные тексты принадлежат правообладателям; изображения в пакет не включены.
''')
print('Generated',len(list(R.rglob('*.md'))),'Markdown files')
