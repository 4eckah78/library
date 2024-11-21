import os
import unittest

from app.main import Book, Library


class TestBook(unittest.TestCase):
    def setUp(self) -> None:
        Book.next_id = 1

    def test_initialization(self) -> None:
        book = Book("Test Title", "Test Author", 2023)
        self.assertEqual(book.id, 1)
        self.assertEqual(book.title, "Test Title")
        self.assertEqual(book.author, "Test Author")
        self.assertEqual(book.year, 2023)
        self.assertEqual(book.status, "в наличии")

    def test_str_representation(self) -> None:
        book = Book("Test Title", "Test Author", 2023)
        self.assertEqual(
            str(book),
            "ID: 1, Title: Test Title, Author: Test Author, Year: 2023, Status: в наличии",
        )


class TestLibrary(unittest.TestCase):
    def setUp(self) -> None:
        self.test_file = "test_library.json"
        self.library = Library(self.test_file)

    def tearDown(self) -> None:
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_add_book(self) -> None:
        self.library.add_book("Test Title", "Test Author", 2023)
        self.assertEqual(len(self.library.books), 1)
        self.assertEqual(self.library.books[0].title, "Test Title")

    def test_save_and_load_books(self) -> None:
        self.library.add_book("Test Title", "Test Author", 2023)
        self.library.save_books()

        new_library = Library(self.test_file)
        self.assertEqual(len(new_library.books), 1)
        self.assertEqual(new_library.books[0].title, "Test Title")

    def test_delete_book(self) -> None:
        self.library.add_book("Test Title", "Test Author", 2023)
        book_id = self.library.books[0].id
        self.library.delete_book(book_id)
        self.assertEqual(len(self.library.books), 0)

    def test_search_book(self) -> None:
        self.library.add_book("Test Title", "Test Author", 2023)
        self.library.add_book("Another Book", "Another Author", 2022)

        res = self.library.search_book("Test")
        self.assertEqual(len(self.library.books), 2)
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0].title, "Test Title")

    def test_change_book_status(self) -> None:
        self.library.add_book("Test Title", "Test Author", 2023)
        book_id = self.library.books[0].id
        self.library.change_book_status(book_id, "выдана")
        self.assertEqual(self.library.books[0].status, "выдана")


if __name__ == "__main__":
    unittest.main()
