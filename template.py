from multiprocessing import Process, freeze_support, set_start_method

import psycopg2
import requests
from pymongo import MongoClient

# DB from
db_from_host = "localhost"
db_from_port = "5432"
db_from_name = "test_python"
db_from_user = "postgres"
db_from_password = "postgres"

# DB to
db_to_host = "localhost"
db_to_port = 27017
db_to_name = "test_python"
db_to_user = "mongo_user"
db_to_password = "mongo_pass"

# API
# token = ''

# Количество процессов
processes_number = 20


def main():
    print("Migration started", flush=True)

    page_number = 0
    page_size = 5000

    while True:
        book_uuids = get_book_uuids(page_number, page_size)

        if len(book_uuids) == 0:
            break

        processes = []
        for book_uuids_chunk in split_into_chunks(book_uuids, processes_number):
            if len(book_uuids_chunk) == 0:
                continue

            process = Process(target=migrate_books, args=[book_uuids_chunk])

            processes.append(process)

            process.start()

        for process in processes:
            process.join()

        page_number += 1

        # print("\n", flush=True)
        # print(f"Page {page_number} completed", flush=True)
        # print("\n\n\n", flush=True)

    print("Migration finished", flush=True)


def migrate_books(book_uuids):
    # print(f"Process {current_process().name} with PID {current_process().pid} started", flush=True)

    books = []
    for book_uuid in book_uuids:
        response = requests.post('http://localhost:8080/book/getByUuid',
                                 json={"uuid": book_uuid})
        response.raise_for_status()

        book = response.json()

        book_converted = convert(book)

        books.append(book_converted)

    save_books(books)


def convert(book):
    book["_id"] = book["uuid"]
    return book


def save_books(books):
    with MongoClient(host=db_to_host,
                     port=db_to_port,
                     username=db_to_user,
                     password=db_to_password) as client:
        db = client.get_database(db_to_name)
        collection = db.get_collection("book")
        collection.insert_many(books)


def get_book_uuids(page_number, page_size):
    connection = psycopg2.connect(host=db_from_host,
                                  port=db_from_port,
                                  database=db_from_name,
                                  user=db_from_user,
                                  password=db_from_password,
                                  sslmode="disable")
    cursor = connection.cursor()
    try:
        # print(cursor.mogrify("SELECT uuid FROM book OFFSET %s LIMIT %s", (page_number * page_size, page_size)))
        cursor.execute("SELECT uuid FROM book OFFSET %s LIMIT %s", (page_number * page_size, page_size))
        return [result[0] for result in cursor.fetchall()]
    finally:
        cursor.close()
        connection.close()


def split_into_chunks(lst, chunks_number):
    chunk_length = len(lst) // chunks_number
    if chunk_length == 0:
        chunk_length = 1
    return [lst[i:i + chunk_length] for i in range(0, len(lst), chunk_length)]


if __name__ == '__main__':
    freeze_support()
    set_start_method('spawn')
    main()
