from flask import Flask, render_template, request, redirect
import csv

app = Flask(__name__)
FILENAME = "books.csv"

# Ensure CSV has headers
with open(FILENAME, "a", newline="") as file:
    writer = csv.writer(file)
    if file.tell() == 0:
        writer.writerow(["ID", "Title", "Author", "Status"])

@app.route("/")
def index():
    books = []
    with open(FILENAME, "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            books.append(row)
    return render_template("index.html", books=books)

@app.route("/add", methods=["POST"])
def add_book():
    book_id = request.form["id"]
    title = request.form["title"]
    author = request.form["author"]

    with open(FILENAME, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([book_id, title, author, "Available"])

    return redirect("/")

@app.route("/borrow/<book_id>")
def borrow_book(book_id):
    books = []
    with open(FILENAME, "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row["ID"] == book_id:
                row["Status"] = "Borrowed"
            books.append(row)

    with open(FILENAME, "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["ID", "Title", "Author", "Status"])
        writer.writeheader()
        writer.writerows(books)

    return redirect("/")

@app.route("/return/<book_id>")
def return_book(book_id):
    books = []
    with open(FILENAME, "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row["ID"] == book_id:
                row["Status"] = "Available"
            books.append(row)

    with open(FILENAME, "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["ID", "Title", "Author", "Status"])
        writer.writeheader()
        writer.writerows(books)

    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
