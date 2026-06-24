from termaid import render_rich

# Representasi hasil akhir pohon merentang minimum (MST)
# Menghubungkan semua node dengan total bobot terkecil tanpa membentuk loop
mermaid_mst = """
flowchart TD

subgraph a["Base Rooute"]
a_n1((a))
a_n2((b))
a_n3((c))
a_n4((d))
a_n5((e))

a_n1 -.-|10| a_n2
a_n1 -.-|7| a_n4
a_n2 -.-|6| a_n3
a_n2 -.-|5| a_n5
a_n4 -.-|4| a_n3
a_n3 -.-|8| a_n5
a_n4 -.-|9| a_n5
end

subgraph c["KRUSKAL - step 1"]
c_n1((a))
c_n2((b))
c_n3((c))
c_n4((d))
c_n5((e))

c_n1 -.-|10| c_n2
c_n1 -.-|7| c_n4
c_n2 -.-|6| c_n3
c_n2 -.-|5| c_n5
c_n4 ---|4| c_n3
c_n3 -.-|8| c_n5
c_n4 -.-|9| c_n5
end

subgraph d["KRUSKAL - step 2"]
d_n1((a))
d_n2((b))
d_n3((c))
d_n4((d))
d_n5((e))

d_n1 -.-|10| d_n2
d_n1 -.-|7| d_n4
d_n2 -.-|6| d_n3
d_n2 ---|5| d_n5
d_n4 ---|4| d_n3
d_n3 -.-|8| d_n5
d_n4 -.-|9| d_n5
end

subgraph e["KRUSKAL - step 3"]
e_n1((a))
e_n2((b))
e_n3((c))
e_n4((d))
e_n5((e))

e_n1 -.-|10| e_n2
e_n1 -.-|7| e_n4
e_n2 ---|6| e_n3
e_n2 ---|5| e_n5
e_n4 ---|4| e_n3
e_n3 -.-|8| e_n5
e_n4 -.-|9| e_n5
end

subgraph f["KRUSKAL - step 4"]
f_n1((a))
f_n2((b))
f_n3((c))
f_n4((d))
f_n5((e))

f_n1 -.-|10| f_n2
f_n1 ---|7| f_n4
f_n2 ---|6| f_n3
f_n2 ---|5| f_n5
f_n4 ---|4| f_n3
f_n3 -.-|8| f_n5
f_n4 -.-|9| f_n5
end



a --> c --> d --> e --> f
"""

# Render langsung ke terminal dengan Rich Text berwarna
try:
    # Menggunakan tema 'neon' agar teks dan garis terlihat kontras
    print(render_rich(mermaid_mst, theme="neon"))
except Exception as e:
    print(f"Error: {e}")