from termaid import render_rich

# Representasi hasil akhir pohon merentang minimum (MST)
# Menghubungkan semua node dengan total bobot terkecil tanpa membentuk loop
mermaid_mst = """
graph TD
    %% Tepi tebal (==>) menandakan jalur MST terpilih
    A((Node A)) == 2 ==> B((Node B))
    B((Node B)) == 3 ==> C((Node C))
    A((Node A)) == 1 ==> D((Node D))
    
    %% Tepi biasa (-->) untuk jalur graf asli yang tidak dipilih dalam MST
    B -->|7| D
    C -->|5| D
"""

# Render langsung ke terminal dengan Rich Text berwarna
try:
    # Menggunakan tema 'neon' agar teks dan garis terlihat kontras
    print(render_rich(mermaid_mst, theme="neon"))
except Exception as e:
    print(f"Error: {e}")