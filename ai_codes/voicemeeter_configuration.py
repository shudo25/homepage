import matplotlib.pyplot as plt
plt.rcParams['font.family'] = ["Meiryo", "MS Gothic", "Yu Gothic", "MS Mincho"]  # 優先順で複数指定
import networkx as nx

# ノードとラベル（改訂版）
nodes = {
    "UserMic": "物理マイク（あなた専用）",
    "UserSpk": "物理スピーカー/ヘッドホン（あなた専用）",
    "Zoom": "Zoom",
    "SasaraMic": "Zoomマイク（ささらさん）",
    "SasaraSpk": "Zoomスピーカー（ささらさん）",
    "CeVIO": "CeVIO（Zoom経由で発声）",
    "Py": "Pythonスクリプト（Zoom経由で認識）"
}

# エッジ（接続）
edges = [
    ("UserMic", "Zoom"),
    ("Zoom", "UserSpk"),
    ("CeVIO", "SasaraMic"),
    ("SasaraMic", "Zoom"),
    ("Zoom", "SasaraSpk"),
    ("SasaraSpk", "Py"),
    ("Py", "CeVIO")  # 音声認識→LLM→CeVIO発声の経路
]

G = nx.DiGraph()
G.add_nodes_from(nodes)
G.add_edges_from(edges)

# レイアウト（改訂版）
pos = {
    "UserMic": (-2, 2),
    "UserSpk": (2, 2),
    "Zoom": (0, 2),
    "CeVIO": (-2, 0),
    "SasaraMic": (-0.5, 0),
    "SasaraSpk": (0.8, 0),   # 少し左へ
    "Py": (2, 0)           # 少し左へ
}

plt.figure(figsize=(10, 6))
nx.draw_networkx_nodes(G, pos, node_color='lightblue', node_size=2500)
nx.draw_networkx_labels(G, pos, labels=nodes, font_size=10, font_family='Meiryo')
# 通常のエッジ（("Py", "CeVIO")以外）
normal_edges = [e for e in edges if e != ("Py", "CeVIO")]
nx.draw_networkx_edges(G, pos, edgelist=normal_edges, arrows=True, arrowstyle='-|>', arrowsize=20, width=2)

# 曲線エッジ（("Py", "CeVIO")のみ）
import matplotlib.patches as mpatches
ax = plt.gca()
start = pos["Py"]
end = pos["CeVIO"]
arrow = mpatches.FancyArrowPatch(
    start, end,
    connectionstyle="arc3,rad=-0.5",  # 曲線の度合い
    arrowstyle='-|>',
    mutation_scale=20,
    color='orange',
    linewidth=2
)
ax.add_patch(arrow)

# y軸範囲を調整してカーブが見切れないようにする
plt.ylim(-2, 3)
plt.xlim(-3, 3)  # 右側の余白を多めに取る
plt.axis('off')
plt.title('物理デバイス分離・Zoom経由ルーティング図', fontsize=14, fontname='Meiryo')
plt.tight_layout()
plt.show()