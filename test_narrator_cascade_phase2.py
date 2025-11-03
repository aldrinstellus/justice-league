#!/usr/bin/env python3
"""
Test Narrator Cascade Phase 2 - All 11 Heroes Integration

Verifies that all heroes successfully receive narrator from Superman coordinator.
"""

import sys

print('Testing narrator cascade to all Justice League heroes...\n')

try:
    from core.justice_league import SupermanCoordinator
    print('✅ Superman imports successfully')

    # Initialize Superman (which initializes all heroes with narrator)
    superman = SupermanCoordinator()

    # Check that all 16 heroes have narrator instances
    heroes_to_check = [
        ('Oracle', superman.oracle),
        ('Batman', superman.batman),
        ('Artemis', superman.artemis),
        ('Green Arrow', superman.green_arrow),
        ('Green Lantern', superman.green_lantern),
        ('Wonder Woman', superman.wonder_woman),
        ('Flash', superman.flash),
        ('Aquaman', superman.aquaman),
        ('Cyborg', superman.cyborg),
        ('Atom', superman.atom),
        ('Martian Manhunter', superman.martian_manhunter),
        ('Plastic Man', superman.plastic_man),
        ('Zatanna', superman.zatanna),
        ('Litty', superman.litty),
        ('Hawkman', superman.hawkman),
    ]

    print('\nChecking narrator instances in all heroes:\n')

    success_count = 0
    failed_heroes = []

    for hero_name, hero_instance in heroes_to_check:
        if hero_instance and hasattr(hero_instance, 'narrator'):
            if hero_instance.narrator is not None:
                print(f'  ✅ {hero_name}: Has narrator instance')
                success_count += 1
            else:
                print(f'  ⚠️  {hero_name}: narrator attribute exists but is None')
                failed_heroes.append(hero_name)
        else:
            print(f'  ❌ {hero_name}: No narrator attribute')
            failed_heroes.append(hero_name)

    print(f'\n{"=" * 60}')
    print(f'📊 NARRATOR CASCADE PHASE 2 TEST RESULTS')
    print(f'{"=" * 60}')
    print(f'  Total Heroes: {len(heroes_to_check)}')
    print(f'  ✅ Success: {success_count}')
    print(f'  ❌ Failed: {len(failed_heroes)}')
    print(f'  Success Rate: {(success_count/len(heroes_to_check)*100):.1f}%')
    print(f'{"=" * 60}')

    if success_count == len(heroes_to_check):
        print('\n✅ Phase 2 Complete: All heroes successfully integrated with narrator!')
        sys.exit(0)
    else:
        print(f'\n⚠️ {len(failed_heroes)} heroes still need narrator integration:')
        for hero in failed_heroes:
            print(f'   - {hero}')
        sys.exit(1)

except Exception as e:
    print(f'\n❌ Error during test: {e}')
    import traceback
    traceback.print_exc()
    sys.exit(1)
