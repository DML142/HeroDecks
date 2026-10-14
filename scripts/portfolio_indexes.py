#!/usr/bin/env python3
import json,pathlib,collections,os,re,math
R=pathlib.Path(__file__).resolve().parents[1]
from data_io import read_data,save_analysis
read=lambda p:read_data(R,p)
C={x['id']:x for x in read('data/cards.json')};H={x['id']:x for x in read('data/heroes.json')};D=read('data/decks.json');A=read('data/deck-analysis.json');E=read('data/archetypes.json');MET=read('data/rating-metrics.json')
def path(d):return f"decks/{H[d['hero']]['faction']}/{d['hero']}/{d['slug']}.md"
def link(d):return f"[{d['name']}](../{path(d)})"
def write(p,s):(R/p).write_text(s.rstrip()+'\n')
text='# Портфель: по 15 колод на каждого героя\n\n[Главная](../README.md) · [Все разборы](../decks/README.md) · [Тематические пожелания](themes.md) · [Оценки](ratings.md)\n\n330 различных численных составов. 32 прежних разбора сохранены, добавлены 288 опубликованных списков и 10 авторских тематических вариантов. Небольшие прежние контрмета-адаптации помечены статусом; остальные новые опубликованные варианты отбирались с минимумом 9 замен относительно уже выбранных колод своего героя. Разные планы важнее максимума одной оценки.\n\nСила, стабильность и веселье здесь — авторские ориентиры; RNG и сложность растут в сторону большей зависимости и трудности. Колоды с одинаковыми классами распределены между Citron/Beta и SB/HG без полного повторения 40 карт. Исторические источники не объявлены свежей метой.\n\n'
for hid,h in H.items():
 ds=[d for d in D if d['hero']==hid]
 text+=f"## {h['name']}\n\nКлассы: {' + '.join(h['classes'])}. **15 колод**.\n\n| Колода | План | Потенциал | Стабильность | RNG | Веселье | Агрессия | Контроль | Сложность | Дата источника |\n| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |\n"
 for d in ds:
  v=A[d['id']]['ratings'];text+='| '+link(d)+' | '+E[d['family']]['title']+' | '+' | '.join(str(v[k]['score']) for k in ['competitive_potential','consistency','rng_dependence','fun','aggression','control','pilot_difficulty'])+' | '+str(d['source_date'])+' |\n'
 text+='\n'
write('research/portfolio.md',text)
scale={
 'competitive_potential':('Вероятность реализовать конкурентный план по механикам','слабый/медленный план','согласованный конкурентный кандидат'),
 'consistency':('Повторяемость доступа и развития','много условных рук','плотный повторяемый план'),
 'rng_dependence':('Зависимость от случайных результатов','почти всё предсказуемо','результат сильно определяется выпадением'),
 'strategic_depth':('Количество значимых решений','простой линейный маршрут','много развилок и решений по фазам'),
 'fun':('Субъективная яркость и разнообразие','малое разнообразие','яркие развилки и payoff'),
 'aggression':('Раннее давление и гонка','пассивное начало','максимальная ранняя гонка'),
 'control':('Способность тормозить/снимать поле','мало ответов','много способов удержать игру'),
 'unpredictability':('Разброс доступных продолжений','линейный план','много неожиданных маршрутов'),
 'speed':('Темп реализации','долгая подготовка','ранний самостоятельный clock'),
 'resilience':('Сохранение плана после ответов','один ответ ломает всё','несколько устойчивых угроз и резерв'),
 'card_advantage':('Поддержка руки','быстро исчерпывается','много условного/постоянного ресурса'),
 'combo_ceiling':('Потолок подготовленного payoff','обычный бой','несколько сильных связанных действий'),
 'pilot_difficulty':('Цена ошибки и сложность расчёта','легко освоить','много фазовых ловушек'),
 'budget_accessibility':('Приблизительная доступность по редкости','много Legendary','меньше Legendary-слотов'),
 'hero_identity':('Уместность класса и сил','слабое использование особенностей','план явно использует особенности героя')}
text='# Оценки: 15 шкал от 1 до 10\n\n[Портфель](portfolio.md) · [Колоды](../decks/README.md)\n\nОценки — редакционные ориентиры для выбора стиля, а не результат турнира, симулятора или рассчитанный винрейт. Они не сравнимы с реальными процентами побед. Два числа с разницей в 1 не доказывают превосходства. Максимумы всех шкал одновременно не являются целью: большое RNG и высокая сложность — свойства, которые нравятся не всем; агрессия и контроль могут конфликтовать по слотам.\n\n| Параметр | Что оценивает | 1 | 10 |\n| --- | --- | --- | --- |\n'
for m in MET:text+=f"| {m['label']} | {' | '.join(scale[m['id']])} |\n"
text+='''
## Как получены числа

База — профиль архетипа из [archetypes.json](../data/archetypes.json), затем простые поправки по **конкретным 40 картам**: ранние ≤2, поздние ≥5, средняя напечатанная цена, слоты в четырёх копиях и признаки Draw/Conjure, защиты, удаления, случайных результатов и редкости. Значения округляются и ограничиваются диапазоном 1–10. Поиск признаков по тексту — грубое приближение: условный Draw не равен гарантированному, damage может иметь ограниченную цель, а защитная способность не защищает от всех видов удаления.

Точные воспроизводимые формулы находятся в функции `ratings` [expand_portfolio.py](../scripts/expand_portfolio.py); исходные признаки, значение и объяснение каждой шкалы — в [deck-analysis.json](../data/deck-analysis.json). «Веселье» и «глубина» — субъективные редакционные прокси. Доступность отражает плотность Legendary, не полную цену sparks. Выраженность героя — категория уместности плана (7 у обычных вариантов, 8 у специально подстроенных тем), поэтому не изображает измеренную разницу между всеми 330 колодами.

Потенциал конкуренции начинается с экспертной гипотезы архетипа и уменьшается за особенно тяжёлую кривую, недостаток ранних слотов и высокий RNG. Эта модель не знает реальную частоту оппонентов, личный уровень пилота или состав коллекции. Для эмпирического пересмотра нужны версии клиента, журналы партий с точными списками и оппонентами, количество игр и интервал неопределённости.

## Как выбирать

Для лестницы сначала смотрите на потенциал, стабильность и скорость, затем проверьте контрматчапы конкретного списка. Для необычных партий смотрите на веселье, глубину, комбо-потолок и допустимый для вас RNG. Для освоения героя начинайте с меньшей сложности. Сумма всех 15 чисел намеренно не используется: она наградила бы одновременно риск, стоимость ошибок и противоположные стили.
'''
write('research/ratings.md',text)
text='''# Bad Moon Rising и Force Field + Soul Patch

[Портфель](portfolio.md) · [Все колоды](../decks/README.md)

Это специальные авторские варианты под запрос: по одному для **каждого из пяти Brainy** и **каждого из пяти Guardian**. Остальные герои не могут положить соответствующие карты в исходную колоду. Получение чужого класса через Conjure не разрешает его в основном списке.

## Blood Moon: пять способов сохранить основания

BMR — Brainy Trick за 7, превращает все ваши живые Zombies в случайных стоимостью **5 и выше**. Ключевой ресурс — несколько тел, переживших Plants Play; дорогая исходная атака не увеличивает гарантированно качество выпадения. Новые результаты имеют собственные правила и могут оказаться неудобными: например, Ra в Tricks приходит после уже потраченного солнца Plants. Не рассчитываем стабильный летал на баги Binary или на обязательный Zombot.

Medulla за 3 даёт +2 Brain при розыгрыше Zombie в её линии, Brain Vendor за 3 возвращает 3. При заранее установленной среде и свободном месте один Vendor на обычном четвёртом ходу оставляет **6**, не 7: 4−3+3+2. Для раннего Moon нужен дополнительный источник, скидка либо другой ход. Teleportation Zombie должен оставаться живым для ввода новых оснований в Tricks.

| Герой / колода | Адаптация | Запасной способ победить |
| --- | --- | --- |
'''
bmr_notes={
'super_brainz':('Pogo + MUG, повторные раскрытия Vendor, поздний вход через TZ','Bounce и атаки обычного поля, условный Carried Away'),
'huge_gigantacus':('Cryo/Station, Swabbie в воде, скидки на текущую руку от Terror-Former','Leap-прогрессия и обычные атаки; сигнатура не гарантирована'),
'rustbolt':('Flag удешевляет Zombies, Teacher — Tricks; эти эффекты нельзя смешивать','Going Viral на сохранённой широкой доске'),
'professor_brainstorm':('Barrel/Final Mission и Crazy-removal очищают поле до сборки оснований','Темп Con Man/случайные силы Quazard, без жертвы всего своего swarm'),
'immorticia':('Cheese/Cyborg, Extinction и Area 22; копирование чисел Swimmer','Beastly-размены и Frenzy в Area, без обязательного Moon')}
for d in D:
 if d.get('theme') and d['family']=='bmr':text+=f"| {H[d['hero']]['name']} — {link(d)} | {' | '.join(bmr_notes[d['hero']])} |\n"
text+='''
### Пример повторного Vendor

На пятом ходу при **трёх уже живых Brain Vendor** можно оплатить MUG за 5. Если все три раскрытия Vendor успешно состоялись после Plants Play, они возвращают 9 Brain, и остаётся возможность оплатить BMR за 7. Это условная ресурсная последовательность, не надёжный стандартный пятый ход: нужны три выживших Vendor, MUG, Moon, допустимые позиции и отсутствие anti-grave/налога. Не закладываем дополнительные возвраты Medulla при повторном скрытии как гарантированные.

## Sanctuary: пять разных защитных оболочек

Soul Patch — Guardian, **6 солнца, 5/10, Armored 1**, принимает повреждение вместо героя. Force Field — Guardian Environment за **4**, Plants в этой ground-линии не могут получить повреждение. Поэтому перенаправленный урон предотвращается; Patch защищает от урона герою даже из других линий, но сам должен оставаться в поле.

**Связка не является полной неуязвимостью.** Rocket Science уничтожает Patch с атакой 5, Pogo возвращает его, Sumo/другие переносы отделяют от среды, вражеский ландшафт заменяет Force. Debuff/transform и уничтожающие способности существ тоже требуют внимания. Вызов Zombot по текущему тексту очищает растения здесь и рядом при раскрытии, а не гарантированно всю доску.

| Герой / колода | Чем поддерживает защиту | Как завершает |
| --- | --- | --- |
'''
patch_notes={
'wall_knight':('Primal Sunflower, Ketchup/Pepper, Buddy/Cob и условный Uncrackable','Astrocado и сохранённые усиленные тела'),
'spudow':('Berry/Launcher, anti-grave, быстрые тела','Pecan превращает 10 Health Patch в атакующее число 10; усиливает и Zombies'),
'citron':('Bounce/splash/Freeze и условный Peel Shield на один ход','Tricarrotops, Lima-поле, окно Brainana'),
'beta_carrotina':('Параллельное водное поле и защитный ground, помощь токенов сил','Cattail/Rotobaga и Dino-рост; постоянного Peel Shield нет'),
'grass_knuckles':('Umbrella, налог, ранние Peas и Root Wall при наличии','Gatling Pea/Plant Food и условный Time to Shine')}
for d in D:
 if d.get('theme') and d['family']=='force_patch':text+=f"| {H[d['hero']]['name']} — {link(d)} | {' | '.join(patch_notes[d['hero']])} |\n"
text+='''
### Практические окна установки

- Wall-Knight: живой Primal Sunflower даёт возможность оплатить Patch за 6 на обычном пятом ходу с дополнительным солнцем; Force должен быть установлен ранее либо оплачен другим ходом. Потерянный Sunflower не учитывается.
- Grass Knuckles: заранее установленный Force, на седьмом ходу Patch 6 + Umbrella 1 = 7. Общая инвестиция вместе с ранее оплаченным Force — **11**. Umbrella делает Untrickable **другие** растения здесь/рядом, не себя. Замена среды остаётся разрешённой.
- Citron: сохранённый Peel Shield за 1 может купить один бой после замены среды. Patch 6 + сила 1 требуют 7 при совместной оплате; следующая игра всё равно требует восстановить защиту или закончить партию.
- Spudow: Force 4 + Patch 6 + Pecan 5 = 15 суммарно, обычно по разным ходам. Перед Pecan сравните Health обеих сторон — большое здоровье Zombie превращается в большую атаку тоже.
- Beta: водная армия создаёт clock, пока Patch принимает повреждение героя в защищённой ground-линии. Force в воду ставить нельзя.

## Источники механических проверок

[Bad Moon Rising](https://plantsvszombies.wiki.gg/wiki/Bad_Moon_Rising), [Brain Vendor](https://plantsvszombies.wiki.gg/wiki/Brain_Vendor), [Medulla Nebula](https://plantsvszombies.wiki.gg/wiki/Medulla_Nebula), [MUG](https://plantsvszombies.wiki.gg/wiki/Mixed-Up_Gravedigger), [Soul Patch](https://plantsvszombies.wiki.gg/wiki/Soul_Patch), [Force Field](https://plantsvszombies.wiki.gg/wiki/Force_Field_%28PvZH%29), [Umbrella Leaf](https://plantsvszombies.wiki.gg/wiki/Umbrella_Leaf). Вики проверена по доступным индексированным материалам 14.10.2026; старые примеры стратегии могут описывать прежние версии, поэтому арифметика пересчитана по текущему каталогу.
'''
write('research/themes.md',text)
text='# 59 профилей архетипов\n\n[Синергии](README.md) · [Портфель](../research/portfolio.md)\n\nПрофили описывают механизм, а не присваивают турнирный tier. Наличие одной карты не гарантирует полный пакет; поддержку конкретных 40 проверяет таблица в каждом разборе.\n\n'
for k,e in E.items():
 cards=', '.join(f"[{C[c]['name']}]({C[c]['wiki_url']})" for c in e['core'])
 text+=f"## {e['title']}\n\nЯкорные карты: {cards}.\n\n{e['plan']}\n\n**Почему работает и при каких условиях:** {e['sequence']}\n\n**Чем разрывается:** {e['weak']}\n\n"
write('synergies/archetypes.md',text)
# Frozen record of how the portfolio was chosen, independent of subjective scores.
counts=collections.Counter(d['category'] for d in D)
report={'date':'2026-10-14','decks':len(D),'per_hero':{hid:sum(d['hero']==hid for d in D) for hid in H},'categories':dict(counts),'distinct_lists':len({tuple(sorted((x['card'],x['count']) for x in d['cards'])) for d in D}),'new_source_minimum_replacements':min(d['selection_distance'] for d in D if d['category']=='source-portfolio'),'families_per_hero':{hid:len({d['family'] for d in D if d['hero']==hid}) for hid in H},'ratings_per_deck':len(MET),'limits':'Source diversity and semantic premises; not empirical win rates or complete client simulation.'}
write('research/portfolio-summary.json',json.dumps(report,ensure_ascii=False,indent=2))
print('Indexes written:',len(D),'lists, categories',dict(counts))
