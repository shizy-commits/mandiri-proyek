#include <iostream>
#include <vector>
#include <iomanip>
#include <string>

using namespace std;

struct Barang {
    string kodeBarang;
    string namaBarang;
    double harga;
    int stok;
};

vector<Barang> inventaris;

void tambahBarang() {
    Barang b;

    cout << "\n=== TAMBAH BARANG ===\n";

    cout << "Kode Barang : ";
    cin >> b.kodeBarang;

    cin.ignore();

    cout << "Nama Barang : ";
    getline(cin, b.namaBarang);

    do {
        cout << "Harga Barang : ";
        cin >> b.harga;

        if (b.harga < 0) {
            cout << "Error! Harga tidak boleh negatif.\n";
        }

    } while (b.harga < 0);

    do {
        cout << "Stok Barang : ";
        cin >> b.stok;

        if (b.stok < 0) {
            cout << "Error! Stok tidak boleh negatif.\n";
        }

    } while (b.stok < 0);

    inventaris.push_back(b);

    cout << "\nBarang berhasil ditambahkan!\n";
}

void tampilkanBarang() {

    cout << "\n=== DAFTAR BARANG ===\n";

    if (inventaris.empty()) {
        cout << "Belum ada data barang.\n";
        return;
    }

    cout << left
         << setw(15) << "Kode"
         << setw(25) << "Nama"
         << setw(15) << "Harga"
         << setw(10) << "Stok"
         << endl;

    cout << string(65, '-') << endl;

    for (int i = 0; i < inventaris.size(); i++) {

        cout << left
             << setw(15) << inventaris[i].kodeBarang
             << setw(25) << inventaris[i].namaBarang
             << setw(15) << inventaris[i].harga
             << setw(10) << inventaris[i].stok
             << endl;
    }
}

void cariBarangTermahal() {

    if (inventaris.empty()) {
        cout << "Inventaris kosong.\n";
        return;
    }

    int indexTermahal = 0;

    for (int i = 1; i < inventaris.size(); i++) {

        if (inventaris[i].harga >
            inventaris[indexTermahal].harga) {

            indexTermahal = i;
        }
    }

    cout << "\n=== BARANG TERMAHAL ===\n";

    cout << "Kode  : "
         << inventaris[indexTermahal].kodeBarang
         << endl;

    cout << "Nama  : "
         << inventaris[indexTermahal].namaBarang
         << endl;

    cout << "Harga : "
         << inventaris[indexTermahal].harga
         << endl;

    cout << "Stok  : "
         << inventaris[indexTermahal].stok
         << endl;
}

void hitungTotalNilaiInventaris() {

    double total = 0;

    for (int i = 0; i < inventaris.size(); i++) {

        total += inventaris[i].harga *
                 inventaris[i].stok;
    }

    cout << "\nTotal Nilai Inventaris = Rp "
         << total << endl;
}

void cekRestock() {

    bool ditemukan = false;

    cout << "\n=== BARANG PERLU RESTOCK ===\n";

    for (int i = 0; i < inventaris.size(); i++) {

        if (inventaris[i].stok < 5) {

            ditemukan = true;

            cout << inventaris[i].kodeBarang
                 << " | "
                 << inventaris[i].namaBarang
                 << " | Stok : "
                 << inventaris[i].stok
                 << endl;
        }
    }

    if (!ditemukan) {
        cout << "Tidak ada barang yang perlu restock.\n";
    }
}

void updateStok() {

    if (inventaris.empty()) {
        cout << "Inventaris kosong.\n";
        return;
    }

    string kode;

    cout << "\nMasukkan kode barang : ";
    cin >> kode;

    bool ditemukan = false;

    for (int i = 0; i < inventaris.size(); i++) {

        if (inventaris[i].kodeBarang == kode) {

            ditemukan = true;

            int *ptrStok = &inventaris[i].stok;

            cout << "Stok saat ini : "
                 << *ptrStok << endl;

            int perubahan;

            cout << "Masukkan perubahan stok (contoh: 5 untuk tambah, -5 untuk kurangi) : ";
            cin >> perubahan;

            *ptrStok += perubahan;

            if (*ptrStok < 0) {
                *ptrStok = 0;
            }

            cout << "Stok berhasil diperbarui.\n";
            cout << "Stok terbaru : "
                 << *ptrStok << endl;

            break;
        }
    }

    if (!ditemukan) {
        cout << "Kode barang tidak ditemukan.\n";
    }
}

int main() {

    int pilihan;

    do {

        cout << "\n====================================\n";
        cout << " SISTEM MANAJEMEN INVENTARIS TOKO\n";
        cout << "====================================\n";

        cout << "1. Tambah Barang\n";
        cout << "2. Tampilkan Semua Barang\n";
        cout << "3. Cari Barang Termahal\n";
        cout << "4. Hitung Total Nilai Inventaris\n";
        cout << "5. Cek Restock\n";
        cout << "6. Update Stok\n";
        cout << "7. Keluar\n";

        cout << "Pilihan : ";
        cin >> pilihan;

        switch (pilihan) {

            case 1:
                tambahBarang();
                break;

            case 2:
                tampilkanBarang();
                break;

            case 3:
                cariBarangTermahal();
                break;

            case 4:
                hitungTotalNilaiInventaris();
                break;

            case 5:
                cekRestock();
                break;

            case 6:
                updateStok();
                break;

            case 7:
                cout << "\nHave a nice day!\n";
                break;

            default:
                cout << "\nPilihan tidak valid!\n";
        }

    } while (pilihan != 7);

    return 0;
}

