import tkinter as tk
from tkinter import messagebox, scrolledtext
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import Image, ImageTk
import os

# ------------------ PODACI ------------------
data = {
    "characters": [
        {"id": "hero", "name": "Glavni Lik", "img": "hero.png", "bio": "Vođa grupe, odlučan i hrabar."},
        {"id": "anna", "name": "Ana", "img": "anna.png", "bio": "Medicinska sestra koja pomaže ranjenima."},
        {"id": "boris", "name": "Boris", "img": "boris.png", "bio": "Opasni švercer sa mutnom prošlošću."},
        {"id": "clara", "name": "Klara", "img": "clara.png", "bio": "Idealistična borbena novinarka."},
        {"id": "david", "name": "David", "img": "david.png", "bio": "Bivši političar, sada oportunista."},
        {"id": "elena", "name": "Elena", "img": "elena.png", "bio": "Misteriozna informantkinja."},
        {"id": "fikret", "name": "Fikret", "img": "fikret.png", "bio": "Veteran rata sa mnogo trauma."},
        {"id": "goran", "name": "Goran", "img": "goran.png", "bio": "Naivni ali snažni seljak."},
        {"id": "hana", "name": "Hana", "img": "hana.png", "bio": "Briljantna ali paranoična matematičarka."},
        {"id": "igor", "name": "Igor", "img": "igor.png", "bio": "Iskusni mehaničar i lojalan saborac."},
        {"id": "jovana", "name": "Jovana", "img": "jovana.png", "bio": "Mladi špijun s dvostrukom lojalnošću."}
    ],
    "relationships": [
        {"from": "hero", "to": "anna", "type": "friend", "strength": 5, "context": "ratni saborci i saveznici na terenu"},
        {"from": "hero", "to": "boris", "type": "enemy", "strength": -7, "context": "zavist, izdaja i pređašnje razmirice"},
        {"from": "anna", "to": "clara", "type": "friend", "strength": 4, "context": "prijateljstvo iz studentskih dana"},
        {"from": "boris", "to": "david", "type": "enemy", "strength": -5, "context": "sukobi interesa u trgovačkom lancu"},
        {"from": "clara", "to": "david", "type": "friend", "strength": 3, "context": "političko partnerstvo"},
        {"from": "hero", "to": "elena", "type": "friend", "strength": 2, "context": "tajni savez preko obaveštajaca"},
        {"from": "elena", "to": "fikret", "type": "enemy", "strength": -4, "context": "nesuglasice iz vremena službe"},
        {"from": "fikret", "to": "goran", "type": "friend", "strength": 6, "context": "suborci iz bitke kod mosta"},
        {"from": "goran", "to": "hana", "type": "friend", "strength": 5, "context": "rodbinske veze - brat i sestra"},
        {"from": "hana", "to": "hero", "type": "enemy", "strength": -3, "context": "nerazrešeni dug iz prošlosti"},
        {"from": "igor", "to": "hero", "type": "friend", "strength": 5, "context": "popravljao vozila za misije"},
        {"from": "igor", "to": "anna", "type": "friend", "strength": 4, "context": "saradnja u hitnim evakuacijama"},
        {"from": "igor", "to": "boris", "type": "enemy", "strength": -6, "context": "sukob oko neispravne opreme"},
        {"from": "jovana", "to": "hero", "type": "friend", "strength": 3, "context": "tajni zadaci pod njegovim vođstvom"},
        {"from": "jovana", "to": "elena", "type": "enemy", "strength": -4, "context": "takmičenje u obaveštajnim podacima"},
        {"from": "jovana", "to": "clara", "type": "friend", "strength": 2, "context": "zajednička misija spašavanja civila"},
        {"from": "hero", "to": "clara", "type": "friend", "strength": 1, "context": "poznavanje preko Ane"},
        {"from": "hero", "to": "david", "type": "neutral", "strength": 0, "context": "neodređeni politički kontakti"},
        {"from": "hero", "to": "fikret", "type": "neutral", "strength": 0, "context": "međusobno poštovanje iz daljine"},
        {"from": "hero", "to": "goran", "type": "friend", "strength": 1, "context": "deljenje resursa za preživljavanje"}
    ]
}

# ------------------ SCENE DATA ------------------
scenes = [
    {"text": "Ana te moli za pomoć u misiji. Hoćeš li joj pomoći?", "lik1": "hero", "lik2": "anna", "yes_change": 3, "no_change": 0},
    {"text": "Boris ti nudi sumnjiv savez. Hoćeš li ga prihvatiti?", "lik1": "hero", "lik2": "boris", "yes_change": 5, "no_change": -2},
    {"text": "Klara je oklevetana od strane Davida. Staješ li na njenu stranu?", "lik1": "clara", "lik2": "david", "yes_change": -3, "no_change": 0},
    {"text": "Elena ti nudi informacije o Fikretu. Hoćeš li ih uzeti?", "lik1": "hero", "lik2": "elena", "yes_change": 2, "no_change": 0},
    {"text": "Hana te optužuje za prošle greške. Priznaješ li ih?", "lik1": "hero", "lik2": "hana", "yes_change": 4, "no_change": -2},
    {"text": "Igor te pita da li ćeš učestvovati u popravci vozila. Hoćeš li pomoći?", "lik1": "hero", "lik2": "igor", "yes_change": 3, "no_change": 0},
    {"text": "Jovana predlaže zajedničku misiju. Prihvataš li?", "lik1": "hero", "lik2": "jovana", "yes_change": 3, "no_change": -1},
    {"text": "Elena sumnja u Jovanine namere. Da li joj veruješ?", "lik1": "jovana", "lik2": "elena", "yes_change": -3, "no_change": 0},
    {"text": "Clara ti nudi pomoć u zamenu za poverljive informacije. Da li ih deliš?", "lik1": "hero", "lik2": "clara", "yes_change": 2, "no_change": -1},
    {"text": "David ti nudi političku zaštitu. Da li prihvataš?", "lik1": "hero", "lik2": "david", "yes_change": 3, "no_change": 0},
    {"text": "Fikret sumnja u Elenu i traži tvoj stav. Da li staješ uz njega?", "lik1": "hero", "lik2": "fikret", "yes_change": 2, "no_change": -2},
    {"text": "Goran traži pomoć u organizovanju sela. Da li ga podržavaš?", "lik1": "hero", "lik2": "goran", "yes_change": 3, "no_change": 0},
    {"text": "Hana te testira pitanjem lojalnosti. Da li ostaješ dosledan sebi?", "lik1": "hero", "lik2": "hana", "yes_change": 2, "no_change": -2}
]

# ------------------ DOMINO EFEKAT ------------------
def primeni_domino_efekat(scenarij, odgovor_da):
    efekti = []
    log_efekata = []

    if scenarij["lik1"] == "hero" and scenarij["lik2"] == "boris" and odgovor_da:
        efekti.append(("hero", "jovana", -2))
        efekti.append(("hero", "igor", -2))
        log_efekata.append("Jovana i Igor gube poverenje jer ne odobravaju saradnju s Borisom.")
    elif scenarij["lik1"] == "hero" and scenarij["lik2"] == "anna" and odgovor_da:
        efekti.append(("hero", "clara", 2))
        log_efekata.append("Clara poštuje tvoju brigu za Anu.")
    elif scenarij["lik1"] == "hero" and scenarij["lik2"] == "igor" and not odgovor_da:
        efekti.append(("hero", "goran", -2))
        log_efekata.append("Goran je razočaran jer nisi podržao Igora.")
    elif scenarij["lik1"] == "hero" and scenarij["lik2"] == "jovana" and odgovor_da:
        efekti.append(("hero", "elena", -2))
        log_efekata.append("Elena sumnja u tvoju odluku da sarađuješ s Jovanom.")
    elif scenarij["lik1"] == "hero" and scenarij["lik2"] == "hana" and odgovor_da:
        efekti.append(("hero", "david", 2))
        log_efekata.append("David ceni tvoju iskrenost prema Hani.")
    elif scenarij["lik1"] == "hero" and scenarij["lik2"] == "elena" and odgovor_da:
        efekti.append(("hero", "fikret", -2))
        log_efekata.append("Fikret se ljuti jer deliš informacije s Elenom.")

    for a, b, delta in efekti:
        izmeni_odnos(a, b, delta)

    return log_efekata

# ------------------ FUNKCIJE ------------------
def izmeni_odnos(lik1, lik2, iznos):
    for rel in data["relationships"]:
        if (rel["from"] == lik1 and rel["to"] == lik2) or (rel["from"] == lik2 and rel["to"] == lik1):
            rel["strength"] += iznos
            if rel["strength"] > 0:
                rel["type"] = "friend"
            elif rel["strength"] < 0:
                rel["type"] = "enemy"
            else:
                rel["type"] = "neutral"
            break

# ------------------ APLIKACIJA ------------------
class StoryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Interaktivna priča")
        self.scene_index = 0

        self.text_label = tk.Label(root, text="", wraplength=500, font=("Helvetica", 14))
        self.text_label.pack(pady=10)

        self.button_frame = tk.Frame(root)
        self.button_frame.pack()
        self.yes_button = tk.Button(self.button_frame, text="DA", width=15, command=lambda: self.odgovori(True))
        self.yes_button.grid(row=0, column=0, padx=10)
        self.no_button = tk.Button(self.button_frame, text="NE", width=15, command=lambda: self.odgovori(False))
        self.no_button.grid(row=0, column=1, padx=10)

        self.canvas_frame = tk.Frame(root)
        self.canvas_frame.pack(pady=10)

        self.history_box = scrolledtext.ScrolledText(root, height=10, width=70, wrap=tk.WORD, font=("Consolas", 10))
        self.history_box.pack(padx=10, pady=10)
        self.history_box.insert(tk.END, "📜 Istorija odluka:")
        self.history_box.config(state='disabled')

        self.prikazi_scenu()

    def prikazi_scenu(self):
        if self.scene_index < len(scenes):
            scena = scenes[self.scene_index]
            self.text_label.config(text=scena['text'])
            prikazi_graf(self.canvas_frame)
        else:
            self.text_label.config(text="🏁 Kraj priče. Hvala na igranju!")
            self.yes_button.config(state="disabled")
            self.no_button.config(state="disabled")
            prikazi_graf(self.canvas_frame)

    def odgovori(self, odgovor_da):
        scena = scenes[self.scene_index]
        change = scena["yes_change"] if odgovor_da else scena["no_change"]
        izmeni_odnos(scena["lik1"], scena["lik2"], change)

        akcija = "DA" if odgovor_da else "NE"
        tekst = f"✔ {scena['text']} → {akcija} (promena odnosa: {change}"

        self.history_box.config(state='normal')
        self.history_box.insert(tk.END, tekst)

        efekti = primeni_domino_efekat(scena, odgovor_da)
        for e in efekti:
            self.history_box.insert(tk.END, f"↳ {e}")

        self.history_box.config(state='disabled')
        self.history_box.see(tk.END)

        self.scene_index += 1
        self.prikazi_scenu()

# ------------------ PRIKAZ GRAFA ------------------
def prikazi_graf(canvas_frame):
    for widget in canvas_frame.winfo_children():
        widget.destroy()

    G = nx.Graph()
    for char in data["characters"]:
        G.add_node(char["id"], label=char["name"])
    for rel in data["relationships"]:
        boja = 'green' if rel["type"] == "friend" else ('red' if rel["type"] == "enemy" else 'gray')
        G.add_edge(rel["from"], rel["to"], weight=abs(rel["strength"]), color=boja, context=rel["context"])

    pos = nx.spring_layout(G, seed=42, k=15)
    fig = plt.figure(figsize=(6, 5))
    colors = [d["color"] for u, v, d in G.edges(data=True)]
    weights = [d["weight"] for u, v, d in G.edges(data=True)]
    labels = nx.get_node_attributes(G, 'label')
    
    nx.draw(G, pos, with_labels=True, labels=labels, edge_color=colors,
            width=weights, node_size=1200, node_color='lightblue', font_size=9)
    
    edge_labels = {(u, v): d["context"] for u, v, d in G.edges(data=True)}  # Corrected line
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=7,
                                bbox=dict(boxstyle="round,pad=0.2", edgecolor='none', facecolor='white', alpha=0.7))
    plt.axis('off')

    canvas = FigureCanvasTkAgg(fig, master=canvas_frame)
    canvas.draw()
    canvas.get_tk_widget().pack()

# ------------------ POKRETANJE ------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = StoryApp(root)
    root.mainloop()
