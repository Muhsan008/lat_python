from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Fungsi untuk membuat tabel jika belum ada
def create_table():
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS mahasiswa (
            id INTEGER PRIMARY KEY,
            nama TEXT NOT NULL,
            nim TEXT NOT NULL
        )
    ''')

    connection.commit()
    connection.close()

# Fungsi untuk menambahkan data
def tambah_mahasiswa(nama, nim):
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()

    cursor.execute('INSERT INTO mahasiswa (nama, nim) VALUES (?, ?)', (nama, nim))

    connection.commit()
    connection.close()

# Fungsi untuk mendapatkan semua data
def get_all_mahasiswa():
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()

    cursor.execute('SELECT * FROM mahasiswa')
    data = cursor.fetchall()

    connection.close()
    return data

# Fungsi untuk mendapatkan data berdasarkan ID
def get_mahasiswa_by_id(id):
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()

    cursor.execute('SELECT * FROM mahasiswa WHERE id = ?', (id,))
    data = cursor.fetchone()

    connection.close()
    return data

# Fungsi untuk memperbarui data
def update_mahasiswa(id, nama, nim):
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()

    cursor.execute('UPDATE mahasiswa SET nama = ?, nim = ? WHERE id = ?', (nama, nim, id))

    connection.commit()
    connection.close()

# Fungsi untuk menghapus data
def hapus_mahasiswa(id):
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()

    cursor.execute('DELETE FROM mahasiswa WHERE id = ?', (id,))

    connection.commit()
    connection.close()

# Route untuk halaman utama
@app.route('/')
def index():
    create_table()
    data = get_all_mahasiswa()
    return render_template('index.html', data=data)

# Route untuk tambah data
@app.route('/tambah', methods=['POST'])
def tambah():
    if request.method == 'POST':
        nama = request.form['nama']
        nim = request.form['nim']

        tambah_mahasiswa(nama, nim)

    return redirect(url_for('index'))

# Route untuk edit data
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    data = get_mahasiswa_by_id(id)

    if request.method == 'POST':
        nama = request.form['nama']
        nim = request.form['nim']

        update_mahasiswa(id, nama, nim)
        return redirect(url_for('index'))

    return render_template('edit.html', data=data)

# Route untuk hapus data
@app.route('/hapus/<int:id>')
def hapus(id):
    hapus_mahasiswa(id)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
