# Minimum Spanning Tree (MST) - Kruskal Algorithm

Project Struktur Data menggunakan algoritma **Minimum Spanning Tree (MST)** dengan metode **Kruskal Algorithm** untuk studi kasus:

> Pemasangan Kabel Internet Antar Daerah

Program dibuat menggunakan Python dan menampilkan visualisasi graph menggunakan:

- NetworkX
- Matplotlib

---

# Features

- Implementasi algoritma Kruskal
- Visualisasi graph
- Highlight jalur MST
- Jalur non-MST ditampilkan dashed
- Input data custom via command line
- Validasi duplicate path
- Validasi self-loop
- Dynamic node naming
- Interactive command system
- Default demo graph

---

# Preview

## Jalur MST

- Edge MST: solid
- Edge non-MST: dashed

## Command System

```text
help
show
name 1 Jakarta
add 1 2 10
done
```

---

# Installation

## Clone Repository

```bash
git clone <repository-url>
cd <repository-folder>
```

## Install Dependency

```bash
pip install networkx matplotlib
```

---

# Run Program

```bash
python main.py
```

---

# Menu

Saat program dijalankan:

```text
1. Gunakan data default
2. Input data sendiri
```

---

# Custom Input System

## Help

```text
help
```

Menampilkan:

- jumlah node
- jumlah path
- daftar node
- daftar command

---

## Show Path

```text
show
```

Menampilkan seluruh kemungkinan path.

Contoh:

```text
1 (Jakarta) <--> 2 (Bandung) = 10
1 (Jakarta) <--> 3 (Bekasi) = AVAILABLE
```

`AVAILABLE` berarti path belum diregistrasi.

---

## Rename Node

```text
name <node> <label>
```

Contoh:

```text
name 1 Jakarta
name 2 Bandung
```

---

## Add Path

```text
add <node1> <node2> <distance>
```

Contoh:

```text
add 1 2 10
add 1 3 5
```

---

## Finish Input

```text
done
```

Input hanya dapat selesai jika minimal path terpenuhi:

```text
minimal path = total node - 1
```

---

# Validation

Program memiliki beberapa validasi:

- Node minimal 2
- Duplicate path tidak diperbolehkan
- `1 2` dan `2 1` dianggap sama
- Self-loop tidak diperbolehkan
- Distance harus lebih besar dari 0
- Minimal path harus terpenuhi

---

# Graph Visualization

Visualisasi graph menggunakan:

- `NetworkX`
- `Matplotlib`

## Visual Rules

- MST Edge → solid line
- Non-MST Edge → dashed gray line

---

# Algorithm

Project menggunakan:

## Kruskal Algorithm

Langkah:

1. Urutkan edge berdasarkan distance
2. Pilih edge terkecil
3. Hindari cycle
4. Ulangi sampai semua node terhubung

---

# Example

## Input

```text
name 1 Jakarta
name 2 Bandung
name 3 Bekasi

add 1 2 10
add 1 3 5
add 2 3 7
```

## Output

```text
Total Minimum Distance = 12
```

---

# Technologies

- Python
- NetworkX
- Matplotlib

---

# Author

Project Struktur Data - Minimum Spanning Tree (MST)
