# Корпус опубликованных списков

[Главная](../README.md) · [JSON-корпус](meta-corpus.json)

Всего 2027 записей; 1773 уникальных наборов после нормализации имён и количеств. Дубликаты сохранены с отдельными исходными IDs/credit/датами, но их нельзя считать независимыми матчами или доказательством популярности. Все 2027 записей проходят структурные проверки 40/классы/копии в этой нормализации.

Поле `eligible_heroes` вычисляется из классов карт. Если все карты одного класса, несколько героев легальны; герой не придумывается из имени списка. Поле `date` — дата записи источника, не дата испытания. Поле `video` — опубликованная ссылка, не подтверждение полного просмотра или матчевого аудита.

Исходный источник: [PvZH Vault JSON](https://pvzhvault.com/deck_database_final.json), получен 14.10.2026. Авторы указаны в каждом объекте; чужие редакторские тексты и изображения не копируются. Более свежий ориентир — [пост сообщества](https://www.reddit.com/r/PvZHeroes/comments/1sh6q47/the_best_decks_for_every_hero_a_continuation_of/), а не внутренний composite score базы.

## Разобранные исходные версии

| Герой | Колода | Исходный ID | Credit | Дата |
| --- | --- | --- | --- | --- |
| Green Shadow | Cartas Buenas | deck_8 | Pillowy | Jun 09, 2026 |
| Solar Flare | Valueflare | deck_13 | Xera | Apr 08, 2026 |
| Wall-Knight | Chemotherapy | deck_255 | Salt, The_Cute_Chick(TCC) | Jun 30, 2026 |
| Chompzilla | ApOTK | deck_44 | The_Cute_Chick(TCC), Cursed | Feb 18, 2026 |
| Spudow | Soteria | deck_-1205 | Xera | Jun 10, 2026 |
| Citron | Amphibious Momentus | deck_-860 | Sustainedx | Oct 03, 2026 |
| Grass Knuckles | Sensei | deck_74 | Xera, Durga | May 11, 2026 |
| Nightcap | Cyclecap | deck_1807 | MakeMeACoffee, Slewer | Jun 16, 2026 |
| Rose | Heal MidRose | deck_-271 | The_Cute_Chick(TCC), Salt | Aug 09, 2026 |
| Captain Combustible | Log Bait | deck_-270 | Xera, Salt, The_Cute_Chick(TCC) | May 24, 2026 |
| Beta-Carrotina | Sham Control — HeroDecks shell | author shell | HeroDecks | 2026-10-14 |
| Super Brainz | Limerence | deck_123 | Xera, Shortbow | Jun 11, 2026 |
| The Smash | Luminous | deck_16 | Seasons | Apr 03, 2026 |
| Impfinity | No-Hokai | deck_3 | The_Cute_Chick(TCC), Mono, Xera | Apr 19, 2026 |
| Rustbolt | Telepsterrazzi | deck_11 | The_Cute_Chick(TCC) | Apr 08, 2026 |
| Electric Boogaloo | Omani | deck_-461 | Bhb12 | Jun 22, 2026 |
| Brain Freeze | Lock the Bathroom | deck_-41 | Boris | Jul 03, 2026 |
| Professor Brainstorm | Trickstache | deck_122 | StarStormvZ | Nov 10, 2025 |
| Immorticia | Bestached | deck_108 | Xera, Shortbow | Sep 25, 2026 |
| Z-Mech | CGP Dark Ages | deck_-2255 | Sustainedx | Jul 13, 2026 |
| Neptuna | Midtomba | deck_12008 | Spand14, Xera, Shortbow | Jun 06, 2026 |
| Huge-Gigantacus | Telimps | deck_210 | Sushi | Aug 09, 2026 |
| Grass Knuckles | Redundancy | deck_2455 | stingray201 | Jun 24, 2026 |
| Captain Combustible | Comboss | deck_-42 | Xera | Jun 24, 2026 |
| Beta-Carrotina | Mirrtorcycle | deck_2555 | The Question Mark | Jun 24, 2026 |
| Chompzilla | Ringspresso | deck_45 | Xera, Slewer, MakeMeACoffee, First Hero | Aug 15, 2026 |
| Immorticia | Secret Swimmer Blob | deck_-124 | FryEmUp | Jun 09, 2026 |

## Расширенная выборка

В [портфеле](portfolio.md) добавлены 288 отдельных записей корпуса. Их `source_id`, исходное `source_name`, автор/credit, дата и точный численный состав сохраняются в [decks.json](../data/decks.json); опубликованные названия в навигации описывают основной и вспомогательный планы, а квадратный номер связывает вариант с источником. Исходные строки иногда имеют ошибки распознавания, поэтому не используются как уверенные имена архетипов. Каждая исходная карточная строка проверяется против нормализованного корпуса валидатором. Авторские 10 тем и прежние 5 tech-вариантов явно отделены статусами.
