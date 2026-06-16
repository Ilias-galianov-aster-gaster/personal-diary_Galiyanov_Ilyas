from database import (
    init_db, add_entry, get_all_entries, get_entry,
    update_entry, delete_entry,
    get_entries_count, search_entries, delete_all_entries, get_last_week_entries
)

def print_entries(entries, title="Записи"):
    print(f"\n--- {title} ---")
    if not entries:
        print("(нет записей)")
        return
    for entry in entries:
        print(f"{entry['id']}. {entry['title']} ({entry['created_at']})")

def main():
    print("Инициализация базы данных...")
    init_db()
    print("База данных готова.\n")

    print("Добавляем 3 записи...")
    add_entry("Первая запись", "Содержимое первой записи.")
    add_entry("Вторая запись", "Текст второй записи.")
    add_entry("Третья запись", "И это третья запись.")
    print("Записи добавлены.\n")

    all_entries = get_all_entries()
    print_entries(all_entries, "Все записи (после добавления)")

    entry_2 = get_entry(2)
    if entry_2:
        print("\n--- Запись с id = 2 ---")
        print(f"Заголовок: {entry_2['title']}")
        print(f"Содержание: {entry_2['content']}")
        print(f"Дата: {entry_2['created_at']}")
    else:
        print("\nЗапись с id = 2 не найдена.")

    print("\nОбновляем запись с id = 2...")
    success = update_entry(2, "Обновлённый заголовок", "Новое содержание второй записи.")
    if success:
        print("Запись обновлена.")
    else:
        print("Ошибка: запись не найдена.")

    updated_entry = get_entry(2)
    if updated_entry:
        print("\n--- Обновлённая запись id=2 ---")
        print(f"Заголовок: {updated_entry['title']}")
        print(f"Содержание: {updated_entry['content']}")
        print(f"Дата: {updated_entry['created_at']}")

    print("\nУдаляем запись с id = 3...")
    deleted = delete_entry(3)
    if deleted:
        print("Запись удалена.")
    else:
        print("Запись не найдена.")

    remaining = get_all_entries()
    print_entries(remaining, "Оставшиеся записи после удаления")

    print("\n" + "="*50)
    print("Проверка самостоятельных функций:")

    count = get_entries_count()
    print(f"Количество записей в БД: {count}")

    results = search_entries("второй")
    print_entries(results, "Результаты поиска по слову 'второй'")

    week_entries = get_last_week_entries()
    print_entries(week_entries, "Записи за последнюю неделю")

    print("\nУдаляем все записи...")
    deleted_count = delete_all_entries()
    print(f"Удалено записей: {deleted_count}")
    print_entries(get_all_entries(), "После удаления всех")

if __name__ == "__main__":
    main()