# Vampire Survivors: Student Edition

![Vampire Survivors: Student Edition](/photoToReadme/menu.png)

## Opis projektu

**Vampire Survivors: Student Edition** to prosta gra oparta na mechanice znanej z gier typu "vampire survivors". Gracz ma możliwość wyboru postaci spośród różnych dostępnych opcji oraz eksplorowania dwóch różnych map, starając się przetrwać ataki dwóch bossów i siedmiu różnych przeciwników. Dodatkowo, gracz może zdobywać i wykorzystywać różne umiejętności (perki), takie jak zwiększenie życia czy szybkości poruszania się.

## GamePlay

![Pierwsza mapa](/photoToReadme/map1.png)
![Druga mapa](/photoToReadme/map2.png)

## Wątki i ich znaczenie

1. **spawn_enemy_thread**: Wątek odpowiedzialny za pojawianie się przeciwników na mapie co określony czas.
2. **spawn_perk_thread**: Wątek generujący perki na mapie co pewien okres czasu.
3. **spawn_shoot_thread**: Wątek obsługujący strzały gracza.
4. **reload_thread**: Wątek służący do przeładowania broni gracza, blokujący możliwość strzelania na określony czas, gdy gracz nie ma już amunicji.
5. **_is_near_player**: Wątek zatrzymujący bossa w miejscu na okresłony czas.
6. **shoot_thread**: Wątek sprawdzający, czy gracz nie otrzymał obrażeń od strzałów przeciwników.
7. **spawn_boss**: Wątek odpowiedzialny za pojawienie się bossa na mapie.
8. **set_immortality**: Wątek aktywujący tryb nieśmiertelności dla gracza na określony czas.
9. **boost_thread**: Wątek aktywujący perk dla gracza na określony czas.

## Sekcje krytyczne

1. **lock_hit**: Sekcja krytyczna, która sprawdza, czy gracz nie jest w trybie nieśmiertelności i obsługuje kolizje gracza z przeciwnikami lub bossem.
2. **activate_perk**: Sekcja krytyczna odpowiedzialna za aktywację perka przez gracza w momencie kiedy żaden inny perk nie jest aktywowany.
3. **move_bullets**: Sekcja krytyczna odpowiedzialna za poruszanie się pocisków przeciwników oraz ich kolizje z graczem.

