import json
import os


class Book:
    """Класс Книга"""

    next_id: int = 1

    def __init__(self, title: str, author: str, year: int) -> None:
        """
        Инициализирует объект Book.
        Параметры:
        * title - название книги
        * author - автор книги
        * year - год издания
        """
        self.id: int = Book.next_id
        Book.next_id += 1
        self.title: str = title
        self.author: str = author
        self.year: int = year
        self.status: str = "в наличии"

    def __str__(self) -> str:
        """Возвращает строковое представление книги"""
        return f"ID: {self.id}, Title: {self.title}, Author: {self.author}, Year: {self.year}, Status: {self.status}"


class Library:
    """Класс для управления библиотекой книг"""

    def __init__(self, filename: str = "library.json") -> None:
        """
        Параметры:
        * filename - путь до файла, где хранится библиотека в формате json
        """
        self.filename: str = filename
        self.books: list = self.load_books()

    def load_books(self) -> list[Book] | list:
        """
        Загружает книги из файла
        Возвращает:
        * books - list, список книг
        """
        if os.path.exists(self.filename):
            with open(self.filename, "r") as f:
                try:
                    data = json.load(f)
                    books: list = [
                        Book(book["title"], book["author"], book["year"])
                        for book in data
                    ]
                    Book.next_id = max(book.id for book in books) + 1 if books else 1
                    for book in books:
                        book.status = data[books.index(book)]["status"]
                    return books
                except json.JSONDecodeError:
                    print(
                        f"Не удалось загрузить библиотеку. Ошибка чтения файла {self.filename}. Может быть файл пустой?"
                    )
                    return []
        return []

    def save_books(self) -> None:
        """Сохраняет книги в файл"""
        data: list = [
            {
                "id": book.id,
                "title": book.title,
                "author": book.author,
                "year": book.year,
                "status": book.status,
            }
            for book in self.books
        ]
        with open(self.filename, "w") as f:
            json.dump(data, f, indent=4)

    def add_book(self, title: str, author: str, year: int) -> None:
        """Добавляет книгу в библиотеку"""
        book = Book(title, author, year)
        self.books.append(book)
        print(f"Книга '{title}' добавлена")

    def delete_book(self, book_id: int) -> None:
        """Удаляет книгу из библиотеки."""
        book: Book | None = next(
            (book for book in self.books if book.id == book_id), None
        )
        if book:
            self.books.remove(book)
            print(f"Книга с ID {book_id} удалена")
        else:
            print(f"Книга с ID={book_id} не найдена")

    def search_book(self, search_term: str) -> None:
        """Ищет книгу по названию, автору или году"""
        results = [
            book
            for book in self.books
            if search_term.lower() in book.title.lower()
            or search_term.lower() in book.author.lower()
            or (search_term.isdigit() and book.year == int(search_term))
        ]
        if results:
            print("Результаты поиска: ")
            for book in results:
                print(book)
            return results
        else:
            print("Книги не найдены.")

    def display_books(self) -> None:
        """Отображает все книги в библиотеке"""
        if self.books:
            print("Список всех книг: ")
            for book in self.books:
                print(book)
            return self.books
        else:
            print("Библиотека пуста")

    def change_book_status(self, book_id: int, new_status: str) -> None:
        """Изменяет статус книги"""
        book = next((book for book in self.books if book.id == book_id), None)
        if book:
            prev_status = book.status
            book.status = new_status
            print(
                f"Статус книги с ID {book_id} изменен c {prev_status} на '{new_status}'."
            )
        else:
            print("Книга с таким ID не найдена")

    def get_all_id(self) -> list:
        return [book.id for book in self.books]


def main() -> None:

    library = Library()

    while True:
        print("\nМеню:")
        print("1. Добавить книгу")
        print("2. Удалить книгу")
        print("3. Найти книгу")
        print("4. Отобразить все книги")
        print("5. Изменить статус книги")
        print("6. Выход")

        choice: str = input("Выберите действие: ")
        if choice == "1":
            title: str = input("Введите название книги: ")
            author: str = input("Введите автора книги: ")
            while True:
                try:
                    year_input: str = input("Введите год издания: ")
                    year: int = int(year_input)
                    if year < 0 or year > 2024:
                        print(
                            f"Неверный формат года, пожалуйста, введите действительный год"
                        )
                        continue
                    break
                except ValueError:
                    print(f"Неверный формат года, пожалуйста, введите целое число")
            library.add_book(title, author, year)
        elif choice == "2":
            while True:
                try:
                    book_id: int = int(input("Введите ID книги для удаления: "))
                    break
                except ValueError:
                    print("Неверный формат ID. Пожалуйста, введите целое число")
            library.delete_book(book_id)
        elif choice == "3":
            search_term: str = input(
                "Введите поисковый запрос (название, автор или год): "
            )
            library.search_book(search_term)
        elif choice == "4":
            library.display_books()
        elif choice == "5":
            while True:
                try:
                    book_id: int = int(
                        input("Введите ID книги для изменения статуса: ")
                    )
                    if book_id not in library.get_all_id():
                        print("Нет книги с таким ID")
                        continue
                    new_status: str = input(
                        "Введите новый статус ('в наличии' или 'выдана'): "
                    ).lower()
                    if new_status not in ["в наличии", "выдана"]:
                        print(
                            "Неверный статус. Пожалуйста, введите 'в наличии' или 'выдана'"
                        )
                        continue
                    break
                except ValueError:
                    print("Неверный формат ID. Пожалуйста, введите целое число")

            library.change_book_status(book_id, new_status)
        elif choice == "6":
            library.save_books()
            break
        else:
            print("Неверный выбор. Попробуйте еще раз.")


if __name__ == "__main__":
    main()
