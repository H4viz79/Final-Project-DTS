import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from tkcalendar import DateEntry
import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Koneksi ke database
def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="data_perpustakaan"
    )

# Fungsi untuk menampilkan data
def fetch_data():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM books")
    rows = cursor.fetchall()
    update_treeview(rows)
    cursor.close()
    conn.close()

# Fungsi untuk memperbarui Treeview dengan data
def update_treeview(rows):
    for row in tree.get_children():
        tree.delete(row)
    for row in rows:
        tree.insert('', tk.END, values=row)

# Fungsi untuk menambah data
def add_data():
    title = entry_title.get()
    author = entry_author.get()
    year_published = entry_year_published.get()
    genre = entry_genre.get()
    date_added = entry_date_added.get_date()
    if title and author and year_published and genre and date_added:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO books (title, author, year_published, genre, date_added) VALUES (%s, %s, %s, %s, %s)",
            (title, author, year_published, genre, date_added)
        )
        conn.commit()
        cursor.close()
        conn.close()
        fetch_data()
        clear_entries()
    else:
        messagebox.showwarning("Input Error", "Please fill in all fields")

# Fungsi untuk membersihkan kolom input
def clear_entries():
    entry_title.delete(0, tk.END)
    entry_author.delete(0, tk.END)
    entry_year_published.delete(0, tk.END)
    entry_genre.delete(0, tk.END)
    entry_date_added.set_date("")

# Fungsi untuk menghapus data
def delete_data():
    selected_item = tree.selection()[0]
    item = tree.item(selected_item)
    book_id = item['values'][0]
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM books WHERE id=%s", (book_id,))
    conn.commit()
    cursor.close()
    conn.close()
    fetch_data()

# Fungsi untuk memperbarui data
def update_data():
    selected_item = tree.selection()[0]
    item = tree.item(selected_item)
    book_id = item['values'][0]

    title = entry_title.get()
    author = entry_author.get()
    year_published = entry_year_published.get()
    genre = entry_genre.get()
    date_added = entry_date_added.get_date()

    if title and author and year_published and genre and date_added:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute(
            """
            UPDATE books
            SET title=%s, author=%s, year_published=%s, genre=%s, date_added=%s
            WHERE id=%s
            """,
            (title, author, year_published, genre, date_added, book_id)
        )
        conn.commit()
        cursor.close()
        conn.close()
        fetch_data()
        clear_entries()
    else:
        messagebox.showwarning("Input Error", "Please fill in all fields")

# Fungsi untuk memilih data di Treeview
def select_data(event):
    selected_item = tree.selection()[0]
    item = tree.item(selected_item)

    entry_title.delete(0, tk.END)
    entry_title.insert(0, item['values'][1])

    entry_author.delete(0, tk.END)
    entry_author.insert(0, item['values'][2])

    entry_year_published.delete(0, tk.END)
    entry_year_published.insert(0, item['values'][3])

    entry_genre.delete(0, tk.END)
    entry_genre.insert(0, item['values'][4])

    entry_date_added.set_date(item['values'][5])

# Fungsi untuk melakukan analisis data menggunakan pandas
def analyze_data():
    conn = connect_db()
    query = "SELECT * FROM books"
    df = pd.read_sql(query, conn)
    conn.close()

    # Analisis sederhana: jumlah buku per genre
    analysis_result = df['genre'].value_counts().to_string()

    # Menampilkan hasil analisis
    messagebox.showinfo("Data Analysis", analysis_result)

# Fungsi untuk menyimpan data sebagai CSV
def save_as_csv():
    try:
        conn = connect_db()
        query = "SELECT * FROM books"
        df = pd.read_sql(query, conn)
        conn.close()

        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if file_path:
            df.to_csv(file_path, index=False)
            messagebox.showinfo("Save CSV", "Data has been saved to CSV file")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while saving to CSV: {str(e)}")

# Fungsi untuk menampilkan grafik buku per genre
def show_genre_distribution():
    try:
        conn = connect_db()
        query = "SELECT genre, COUNT(*) as count FROM books GROUP BY genre"
        df = pd.read_sql(query, conn)
        conn.close()

        fig, ax = plt.subplots()
        df.plot(kind='bar', x='genre', y='count', ax=ax, legend=False)
        ax.set_title('Distribution of Books by Genre')
        ax.set_xlabel('Genre')
        ax.set_ylabel('Number of Books')

        # Menampilkan grafik di Tkinter
        canvas = FigureCanvasTkAgg(fig, master=frame_chart)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while generating the chart: {str(e)}")

# Fungsi untuk keluar dari aplikasi
def exit_app():
    root.destroy()

# Setup GUI
root = tk.Tk()
root.title("Data Analisis Perpustakaan")

# Frame Input
frame_input = tk.Frame(root)
frame_input.pack(pady=10)

tk.Label(frame_input, text="Title").grid(row=0, column=0, padx=5, pady=5)
tk.Label(frame_input, text="Author").grid(row=0, column=1, padx=5, pady=5)
tk.Label(frame_input, text="Year Published").grid(row=0, column=2, padx=5, pady=5)
tk.Label(frame_input, text="Genre").grid(row=0, column=3, padx=5, pady=5)
tk.Label(frame_input, text="Date Added").grid(row=0, column=4, padx=5, pady=5)

entry_title = tk.Entry(frame_input)
entry_title.grid(row=1, column=0, padx=5, pady=5)
entry_author = tk.Entry(frame_input)
entry_author.grid(row=1, column=1, padx=5, pady=5)
entry_year_published = tk.Entry(frame_input)
entry_year_published.grid(row=1, column=2, padx=5, pady=5)
entry_genre = tk.Entry(frame_input)
entry_genre.grid(row=1, column=3, padx=5, pady=5)
entry_date_added = DateEntry(frame_input, date_pattern='yyyy-mm-dd')
entry_date_added.grid(row=1, column=4, padx=5, pady=5)

btn_add = tk.Button(frame_input, text="Add Book", command=add_data)
btn_add.grid(row=1, column=5, padx=5, pady=5)

btn_update = tk.Button(frame_input, text="Update Book", command=update_data)
btn_update.grid(row=1, column=6, padx=5, pady=5)

btn_delete = tk.Button(frame_input, text="Delete Book", command=delete_data)
btn_delete.grid(row=1, column=7, padx=5, pady=5)

btn_analyze = tk.Button(frame_input, text="Analyze Data", command=analyze_data)
btn_analyze.grid(row=1, column=8, padx=5, pady=5)

btn_save_csv = tk.Button(frame_input, text="Save as CSV", command=save_as_csv)
btn_save_csv.grid(row=1, column=9, padx=5, pady=5)

btn_show_chart = tk.Button(frame_input, text="Show Genre Distribution", command=show_genre_distribution)
btn_show_chart.grid(row=1, column=10, padx=5, pady=5)

btn_exit = tk.Button(frame_input, text="Exit", command=exit_app)
btn_exit.grid(row=1, column=11, padx=5, pady=5)

# Frame Treeview
frame_treeview = tk.Frame(root)
frame_treeview.pack(pady=10)

columns = ('ID', 'Title', 'Author', 'Year Published', 'Genre', 'Date Added')
tree = ttk.Treeview(frame_treeview, columns=columns, show='headings')

for col in columns:
    tree.heading(col, text=col)

tree.bind('<ButtonRelease-1>', select_data)
tree.pack()

# Frame Chart
frame_chart = tk.Frame(root)
frame_chart.pack(pady=10, fill=tk.BOTH, expand=True)

# Fetch data on startup
fetch_data()

root.mainloop()