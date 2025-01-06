class Ranqueamento:
    def __init__(self):
        pass

    def calcular_rankings(self, scores):
        """
        Calcula o ranking geral somando os pontos de todas as provas.
        Cada time acumula pontos com base na posição em todas as provas.
        """
        rankings = {}
        for categoria, times_scores in scores.items():
            geral = self.calcular_ranking_geral(times_scores)
            rankings[categoria] = {"geral": geral}
        return rankings

    def calcular_ranking_geral(self, times_scores):
        """
        Calcula o ranking geral somando os pontos das posições de todas as provas.
        Apenas soma as provas que têm pontuação atribuída.
        """
        pontuacao_total = {time: 0 for time in times_scores}

        # Lista de provas que seguem a lógica inversa (quanto maior o score, melhor a pontuação)
        provas_inversas = ["3a PR SNATCH (CargaLibras)", "3b PR CLEAN JERK (CargaLibras)", "1d TODOS (Repetições)",
                           "2a (Repetições)", "2b (Repetições)", "FINAL 4b (Repetições)", "FINAL 4c (Repetições)"]

        # Itera sobre todas as provas
        for prova in self.get_provas(times_scores):
            # Para cada prova, classificamos os times de acordo com o score real
            if prova in provas_inversas:
                # Para provas inversas, quanto maior o score, melhor a posição
                ranking_por_prova = sorted(times_scores.items(), key=lambda x: x[1].get(prova, 0), reverse=True)
            else:
                # Para todas as outras provas, quanto menor o score, melhor a posição
                ranking_por_prova = sorted(times_scores.items(), key=lambda x: x[1].get(prova, 0))

            # Calcula a pontuação para cada posição, mas somente se o score for maior que 0
            for posicao, (time, provas) in enumerate(ranking_por_prova):
                if provas.get(prova, 0) > 0:  # Soma apenas se a pontuação da prova for maior que 0
                    pontos = 100 - posicao * 10
                    pontos = max(pontos, 0)  # Garante que a pontuação mínima seja 0
                    pontuacao_total[time] += pontos

        # Ordena os times com base na pontuação total, do maior para o menor
        return dict(sorted(pontuacao_total.items(), key=lambda item: item[1], reverse=True))

    def calcular_ranking_por_prova(self, scores, categoria_selecionada, prova_selecionada):
        """
        Calcula o ranking por uma prova específica, exibindo o score da prova selecionada.
        Se dois ou mais times tiverem o mesmo score, eles recebem a mesma pontuação.
        """
        ranking_por_prova = []

        # Verifica se a categoria selecionada existe nos scores
        if categoria_selecionada in scores:
            times = scores[categoria_selecionada]  # Obtem os times da categoria selecionada

            # Itera sobre os times dentro da categoria
            for time, provas in times.items():
                score_real = provas.get(prova_selecionada, 0)

                # Adiciona o time e seus detalhes no ranking
                ranking_por_prova.append({
                    "time": time,  # Nome do time
                    "score_real": score_real
                })

            # Lista de provas que seguem a lógica inversa
            provas_inversas = ["3a PR SNATCH (CargaLibras)", "3b PR CLEAN JERK (CargaLibras)", "1d TODOS (Repetições)",
                               "2a (Repetições)", "2b (Repetições)", "FINAL 4b (Repetições)", "FINAL 4c (Repetições)"]

            # Ordena o ranking com base no score da prova
            if prova_selecionada in provas_inversas:
                # Para provas inversas, quanto maior o score, melhor a posição
                ranking_por_prova = sorted(ranking_por_prova, key=lambda x: x['score_real'], reverse=True)
            else:
                # Para todas as outras provas, quanto menor o score, melhor a posição
                ranking_por_prova = sorted(ranking_por_prova, key=lambda x: x['score_real'])

            # Atribui pontuações com base nas posições e trata scores iguais
            pontos_atual = 100
            for i, resultado in enumerate(ranking_por_prova):
                if i == 0 or resultado["score_real"] != ranking_por_prova[i - 1]["score_real"]:
                    # Calcula os pontos para a posição
                    pontos_atual = 100 - (i * 10)
                    pontos_atual = max(pontos_atual, 0)  # Garante que a pontuação mínima seja 0

                resultado["pontos"] = pontos_atual

        return ranking_por_prova

    def get_provas(self, times_scores):
        """
        Obtém a lista de provas a partir dos times (todos os times têm as mesmas provas).
        """
        return times_scores[next(iter(times_scores))].keys()
