import tkinter as tk
from tkinter import ttk
from categorias import Categorias
from ranqueamento import Ranqueamento
import csv

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Provas e Ranqueamento")
        self.geometry("800x600")  # Ajuste para permitir espaço suficiente na interface

        self.categorias = Categorias()
        self.ranqueamento = Ranqueamento()

        self.create_widgets()

    def create_widgets(self):
        # Criação das abas
        tab_control = ttk.Notebook(self)

        # Aba para cada categoria
        self.categorias.create_categoria_tabs(tab_control)

        # Aba para ranqueamento
        rank_tab = ttk.Frame(tab_control)
        tab_control.add(rank_tab, text="Classificação")
        self.create_ranking_frame(rank_tab)

        tab_control.pack(expand=1, fill="both")

    def create_ranking_frame(self, frame):
        # Combobox para seleção de categoria
        tk.Label(frame, text="Selecione a Categoria:").pack()
        self.categoria_combobox = ttk.Combobox(frame, values=list(self.categorias.get_categorias()), state="readonly")
        self.categoria_combobox.pack()

        # Combobox para seleção de prova
        tk.Label(frame, text="Selecione a Prova:").pack()
        self.prova_combobox = ttk.Combobox(frame, state="readonly")
        self.prova_combobox.pack()

        # Atualiza as provas quando a categoria muda
        self.categoria_combobox.bind("<<ComboboxSelected>>", self.update_provas)

        # Botão para calcular o ranqueamento
        rank_button = tk.Button(frame, text="Exibir Ranking", command=self.show_rankings)
        rank_button.pack(pady=10)

        self.rank_output = tk.Text(frame, height=20, width=80)
        self.rank_output.pack()

        # Botões para exportar CSV
        export_prova_button = tk.Button(frame, text="Exportar Classificação por Prova (CSV)", command=self.export_prova_csv)
        export_prova_button.pack(pady=10)

        export_geral_button = tk.Button(frame, text="Exportar Classificação Geral (CSV)", command=self.export_geral_csv)
        export_geral_button.pack(pady=10)

    def update_provas(self, event):
        """Atualiza a combobox de provas com base na categoria selecionada."""
        categoria = self.categoria_combobox.get()
        if categoria:
            provas = self.categorias.get_provas()
            self.prova_combobox.config(values=provas)
            self.prova_combobox.current(0)  # Seleciona a primeira prova por padrão

    def show_rankings(self):
        """Exibe o ranking com base na categoria e prova selecionadas."""
        categoria = self.categoria_combobox.get()  # Obtém a categoria selecionada
        prova = self.prova_combobox.get()  # Obtém a prova selecionada

        if categoria and prova:
            self.rank_output.delete(1.0, tk.END)

            # Ranking geral da categoria
            rankings = self.ranqueamento.calcular_rankings(self.categorias.get_all_scores())
            self.rank_output.insert(tk.END, f"{categoria} - Ranking Geral (Baseado nas posições nas provas):\n")
            for time, total_score in rankings[categoria]['geral'].items():
                self.rank_output.insert(tk.END, f"{time}: {total_score} pontos (Geral)\n")

            # Ranking por prova com score real apenas da prova e da categoria selecionada
            ranking_por_prova = self.ranqueamento.calcular_ranking_por_prova(self.categorias.get_all_scores(), categoria, prova)
            self.rank_output.insert(tk.END, f"\nRanking para a Prova {prova} da Categoria {categoria}:\n")

            # Exibe a colocação, nome do time, pontuação e o score real no formato especificado
            for posicao, resultado in enumerate(ranking_por_prova, start=1):
                time = resultado["time"]  # Nome do time
                pontos = resultado["pontos"]  # Pontos atribuídos com base na posição
                score_real = resultado["score_real"]  # Score real da prova
                self.rank_output.insert(tk.END, f"{posicao}º {time}: {pontos} pontos ({score_real})\n")
        else:
            self.rank_output.insert(tk.END, "Selecione uma categoria e uma prova.\n")

    def export_prova_csv(self):
        """Exporta a classificação por prova para CSV."""
        categoria = self.categoria_combobox.get()
        prova = self.prova_combobox.get()

        if categoria and prova:
            # Obtém os dados da classificação por prova
            ranking_por_prova = self.ranqueamento.calcular_ranking_por_prova(self.categorias.get_all_scores(), categoria, prova)

            # Nome do arquivo CSV
            filename = f"ranking_{categoria}_{prova}.csv"

            # Escreve os dados no arquivo CSV
            with open(filename, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Posição", "Time", "Pontuação", "Score Real"])
                
                for posicao, resultado in enumerate(ranking_por_prova, start=1):
                    time = resultado["time"]
                    pontos = resultado["pontos"]
                    score_real = resultado["score_real"]
                    # Escreve os valores separados por colunas (células diferentes)
                    writer.writerow([posicao, time, pontos, score_real])

            print(f"Classificação por Prova exportada para {filename}")

    def export_geral_csv(self):
        """Exporta a classificação geral para CSV."""
        categoria = self.categoria_combobox.get()

        if categoria:
            # Obtém os dados da classificação geral
            rankings = self.ranqueamento.calcular_rankings(self.categorias.get_all_scores())
            ranking_geral = rankings[categoria]['geral']

            # Nome do arquivo CSV
            filename = f"ranking_geral_{categoria}.csv"

            # Escreve os dados no arquivo CSV
            with open(filename, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Time", "Pontuação Total"])

                # Escreve os valores em colunas separadas (nome do time e pontuação)
                for time, total_score in ranking_geral.items():
                    writer.writerow([time, total_score])

            print(f"Classificação Geral exportada para {filename}")

if __name__ == "__main__":
    app = Application()
    app.mainloop()
