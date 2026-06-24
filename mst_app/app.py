import subprocess

import matplotlib.pyplot as plt

from .cli import input_custom_data
from .graph_data import Path, load_default_data, reset_data
from .mermaid_renderer import render_mermaid
from .mst import draw_graph2, kruskal
from .ui import print_error, print_info


def main():
    print("PROJECT MST")
    print("Pemasangan Kabel Internet Antar Daerah")

    print("\n1. Gunakan data default")
    print("2. Input data sendiri")

    choice = input("\nPilih: ")

    reset_data()

    if choice == "2":
        input_custom_data()
    else:
        load_default_data()

    print("\n=== DAFTAR SEMUA JALUR ===\n")

    for path in Path.get_sorted_paths():
        print(
            f"Node {path._path[0]} "
            f"<--> Node {path._path[1]} "
            f"= {path.distance}"
        )

    mst, steps = kruskal()

    print("\n=== PILIH RENDERER ===\n")
    print("1. Pyplot")
    print("2. Mermaid / termaid")

    renderer_choice = input("\nPilih renderer: ").strip()

    if renderer_choice == "2":
        print("\n=== PILIH OUTPUT MERMAID ===\n")
        print("1. Hasil MST saja")
        print("2. Seluruh proses Kruskal")
        mermaid_choice = input("\nPilih mode: ").strip()
        mode = "process" if mermaid_choice == "2" else "result"
        try:
            mmd_path, svg_path = render_mermaid(mst, steps, mode=mode)
        except FileNotFoundError as exc:
            print_error(str(exc))
            print_info("Pastikan Mermaid CLI dapat dijalankan dari terminal ini.")
            return
        except subprocess.CalledProcessError as exc:
            print_error(f"Failed to render Mermaid output: {exc}")
            return
        print(f"\nMermaid source: {mmd_path}")
        print(f"SVG result    : {svg_path}")
        return

    draw_graph2(mst)
    plt.show()
