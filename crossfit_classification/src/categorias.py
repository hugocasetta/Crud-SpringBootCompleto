import tkinter as tk
from tkinter import ttk
import json
import os

class Categorias:
    def __init__(self):
        self.categorias = {
            "Rx Misto": ["Hugo/Bigode/Elaine", "Wesley/Lorena/Vitinho", "Breno/Tellini/Vini Japa","Vini Wesley/Amanda/Paulo","kaike/Andressa/Rogerio","Kao/Andre/Pauka","Hauari/Guilher/Maju"],
            "Amador Masculino": ["Guilherme/Rodrigo/Matheus", "Lucas/Pedro/Cleiton", "Marco/Diego/Cassio","Rau/Caio/Matheus","Bola/Du/Gabriel"],
            "Amador Feminino": ["Gabriela/Japa/Fernanda", "Fernanda/Patricia/Camila", "Marcela/Mari/Karime","Thaynara/Natalia/Jaque"]
        }
        # Nomes das provas atualizados para corresponder com os nomes no código de ranqueamento
        self.provas = ["1a ATLETA 1 (segundos)", "1b ATLETA 2 (segundos)", "1c ATLETA 3 (segundos)", "1d TODOS (Repetições)", 
                       "2a (Repetições)", "2b (Repetições)", "3a PR SNATCH (CargaLibras)", "3b PR CLEAN JERK (CargaLibras)", 
                       "FINAL 4a (segundos)", "FINAL 4b (Repetições)", "FINAL 4c (Repetições)", "SURPRESA"]
        self.scores_file = "pontuacoes.json"
        self.scores = self.load_scores()  # Carregar pontuações do arquivo

    def get_categorias(self):
        return self.categorias.keys()

    def get_times(self, categoria):
        return self.categorias[categoria]

    def get_provas(self):
        return self.provas

    def set_scores(self, categoria, time, scores):
        # Garantir que o time tenha todas as provas inicializadas
        if categoria not in self.scores:
            self.scores[categoria] = {}

        if time not in self.scores[categoria]:
            self.scores[categoria][time] = {prova: 0 for prova in self.provas}

        # Atualiza as pontuações
        for prova, score in scores.items():
            self.scores[categoria][time][prova] = score
        
        self.save_scores()  # Salva as pontuações no arquivo

    def get_all_scores(self):
        return self.scores

    def save_scores(self):
        """Salva as pontuações no arquivo JSON."""
        with open(self.scores_file, 'w') as f:
            json.dump(self.scores, f, indent=4)

    def load_scores(self):
        """Carrega as pontuações do arquivo JSON."""
        if os.path.exists(self.scores_file):
            with open(self.scores_file, 'r') as f:
                return json.load(f)
        else:
            return {}

    def create_categoria_tabs(self, tab_control):
        """Cria as abas de cada categoria dinamicamente com a interface Tkinter"""
        for categoria in self.get_categorias():
            tab = ttk.Frame(tab_control)
            tab_control.add(tab, text=categoria)
            self.create_categoria_frame(tab, categoria)

    def create_categoria_frame(self, frame, categoria):
        times = self.get_times(categoria)
        provas = self.get_provas()

        # Combobox de Times
        combobox_label = tk.Label(frame, text="Times")
        combobox_label.pack()

        combobox = ttk.Combobox(frame, values=times, state="readonly")
        combobox.pack()

        # Entradas de pontuação das provas
        scores_frame = tk.Frame(frame)
        scores_frame.pack(pady=10)

        prova_scores = {}
        prova_labels = {}  # Dicionário para armazenar os labels de último score

        for prova in provas:
            prova_label = tk.Label(scores_frame, text=prova)
            prova_label.grid(row=provas.index(prova), column=0)

            # Campo de entrada para novo score
            score_entry = tk.Entry(scores_frame)
            score_entry.grid(row=provas.index(prova), column=1)
            prova_scores[prova] = score_entry

            # Label para mostrar o último score
            last_score_label = tk.Label(scores_frame, text="Último Score: 0")
            last_score_label.grid(row=provas.index(prova), column=2)
            prova_labels[prova] = last_score_label

        # Botão para carregar os scores
        load_button = tk.Button(frame, text="Carregar Pontuações", 
                                command=lambda: self.load_scores_for_team_and_update_labels(categoria, combobox.get(), prova_labels))
        load_button.pack(pady=10)

        # Botão para salvar pontuações
        save_button = tk.Button(frame, text="Salvar Pontuações", 
                                command=lambda: self.save_scores_and_clear(categoria, combobox, prova_scores))
        save_button.pack(pady=10)

    def load_scores_for_team_and_update_labels(self, categoria, time, prova_labels):
        """Carrega os scores e atualiza os labels com o último score registrado."""
        if not time:
            print("Selecione um time.")
            return

        scores = self.load_scores_for_team(categoria, time)

        # Atualiza os labels com os últimos scores
        for prova, label in prova_labels.items():
            last_score = scores.get(prova, 0)
            label.config(text=f"Último Score: {last_score}")

    def load_scores_for_team(self, categoria, time):
        """Carrega os scores existentes para um time em uma categoria."""
        if categoria in self.scores and time in self.scores[categoria]:
            return self.scores[categoria][time]
        return {prova: 0 for prova in self.provas}  # Retorna pontuações vazias se não houver dados

    def save_scores_and_clear(self, categoria, combobox, prova_scores):
        """Salva as pontuações e limpa os campos de entrada."""
        time = combobox.get()
        if not time:
            print("Selecione um time.")
            return

        scores = {prova: int(entry.get()) for prova, entry in prova_scores.items() if entry.get().isdigit()}

        if scores:
            self.set_scores(categoria, time, scores)
            print(f"Pontuações salvas para {time} na categoria {categoria}.")

            # Limpa os campos após salvar
            combobox.set("")
            for entry in prova_scores.values():
                entry.delete(0, tk.END)
        else:
            print("Pontuações inválidas.")
