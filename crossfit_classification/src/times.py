import tkinter as tk
from tkinter import ttk, messagebox

class TeamRegistrationTab(tk.Frame):
    def __init__(self, parent, teams, update_category_teams):
        super().__init__(parent)
        self.parent = parent
        self.teams = teams  # Dicionário contendo os times por categoria
        self.update_category_teams = update_category_teams

        # Interface de Cadastro de Times
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="Nome do Time").pack(pady=5)
        self.team_entry = tk.Entry(self)
        self.team_entry.pack(pady=5)

        tk.Label(self, text="Selecione a Categoria").pack(pady=5)
        self.category_var = tk.StringVar(self)
        categories = ["Rx Misto", "Amador Masculino", "Amador Feminino"]
        self.category_menu = ttk.Combobox(self, textvariable=self.category_var, values=categories)
        self.category_menu.pack(pady=5)

        tk.Button(self, text="Cadastrar Time", command=self.register_team).pack(pady=10)
        self.team_listbox = tk.Listbox(self, width=50, height=10)
        self.team_listbox.pack(pady=10)

    def register_team(self):
        team_name = self.team_entry.get()
        category = self.category_var.get()

        if not team_name or not category:
            messagebox.showerror("Erro", "Insira o nome do time e selecione uma categoria.")
            return

        # Adiciona o time à categoria correspondente
        self.teams[category].append(team_name)
        self.team_listbox.insert(tk.END, f"{team_name} ({category})")
        self.team_entry.delete(0, tk.END)

        # Atualiza as abas de categorias com os novos times
        self.update_category_teams(category, self.teams[category])
