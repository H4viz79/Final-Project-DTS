# Aplikasi Analisis Data Perpustakaan

Ini adalah aplikasi manajemen dan analisis data perpustakaan sederhana yang dibangun menggunakan Python, Tkinter, dan MySQL. Aplikasi ini memungkinkan pengguna untuk mengelola catatan buku, menganalisis data, dan mengekspor data ke file CSV.

## Fitur

- **Add Book**: Menambahkan catatan buku baru ke basis data perpustakaan dengan menambahkan kolom untuk judul, pengarang, tahun, dan tanggal.
- **View Books**: Menampilkan semua buku yang tersimpan dalam basis data dalam format tabel.
- **Update Book**: Memodifikasi catatan buku yang ada secara langsung dari aplikasi.
- **Delete Book**: Menghapus buku dari database perpustakaan.
- **Save as CSV**: Mengekspor daftar buku saat ini ke file CSV.
- **Analyze Books**: Visualisasikan jumlah buku yang ditambahkan setiap tahun dengan diagram batang.
- **Exit Application**: Menutup aplikasi secara aman.

## Dependencies

- **Python 3.10.0**
- **Tkinter**: Paket GUI standar dari Python.
- **mysql-connector-python**: Konektor MySQL untuk Python.
- **pandas**: Library manipulasi dan analisis data.
- **matplotlib**: Library plotting untuk visualisasi data.
- **tkcalendar**: Widget DateEntry untuk Tkinter.

Anda dapat menginstal paket Python yang diperlukan menggunakan `pip`:

```bash
pip install mysql-connector-python pandas matplotlib tkcalendar
