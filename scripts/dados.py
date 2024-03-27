import os
import traceback
import requests
import gspread
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

domino_spreadsheet_id = "1Doxuhdbr3nmXlrDycuhkzYeMaILpdlK3qfBZD5s-EAs"
api_key = "AIzaSyBHNpR6a0_7vjpjsWI2xtZTTYRwpCCrc38"

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

def converter_para_segundos(tempo):
    minutos, segundos = map(int, tempo.split(":"))
    return minutos * 60 + segundos

def converter_para_tempo_formatado(segundos):
    minutos, segundos = divmod(segundos, 60)
    return f"{minutos:02d}:{segundos:02d}"

def salvar_dados_domino(clicks, clicks_peca, tempo_narracao, tempo_jogo, tempo_ganhou_perdeu, qtd_jogadas_jogador, qtd_jogadas_robo, qtd_pecas_esquerda, qtd_pecas_direita, qtd_pecas_tabuleiro, placar, ganhou,
                        qtd_compras_jogador, qtd_compras_robo, qtd_pilha_compras, qtd_limpar_tabuleiro, tabuleiro_final, mao_final_jogador, mao_final_robo, mao_inicial_jogador, mao_inicial_robo, jogadas):
    
    segundos_narracao = converter_para_segundos(tempo_narracao)
    segundos_jogo = converter_para_segundos(tempo_jogo)
    segundos_ganhou_perdeu = converter_para_segundos(tempo_ganhou_perdeu)

    segundos_total = segundos_narracao + segundos_jogo + segundos_ganhou_perdeu
    tempo_total = converter_para_tempo_formatado(segundos_total)

    dados = {
        "Clicks": clicks,
        "Clicks_peca": clicks_peca,
        "Tempo_narracao": tempo_narracao,
        "Tempo_jogo": tempo_jogo,
        "Tempo_ganhou_perdeu": tempo_ganhou_perdeu,
        "Tempo_total": tempo_total,
        "Qtd_jogadas_jogador": qtd_jogadas_jogador,
        "Qtd_jogadas_robo": qtd_jogadas_robo,
        "Qtd_pecas_esquerda": qtd_pecas_esquerda,
        "Qtd_pecas_direita": qtd_pecas_direita,
        "Qtd_pecas_tabuleiro": qtd_pecas_tabuleiro,
        "Placar": str(placar),
        "Ganhou": ganhou,
        "Qtd_compras_jogador": qtd_compras_jogador,
        "Qtd_compras_robo": qtd_compras_robo,
        "Qtd_pilha_compras": qtd_pilha_compras,
        "Qtd_limpar_tabuleiro": qtd_limpar_tabuleiro,
        "Tabuleiro_final": str(list(tabuleiro_final)),
        "Mao_final_jogador": str([(peca.nome1, peca.nome2) for peca in mao_final_jogador]),
        "Mao_final_robo": str([(peca.nome1, peca.nome2) for peca in mao_final_robo]),
        "Mao_inicial_jogador": str([(peca.nome1, peca.nome2) for peca in mao_inicial_jogador]),
        "Mao_inicial_robo": str([(peca.nome1, peca.nome2) for peca in mao_inicial_robo]),
        "Jogadas": str(jogadas)
    }

    dados_list = list(dados.values())
    # print(dados_list)
    # for dado in dados_list:
    #     print(type(dado))

    # Salva em um arquivo json localmente.
    # dados_json = json.dumps(dados, indent=4)
    # print(type(dados_json))
    # with open("./data/domino.json", "w") as f:
    #     f.write(dados_json)

    salvar_dados_google_sheets(dados_list, "domino")

def salvar_dados_memoria(clicks, clicks_peca, tempo_narracao, tempo_jogo, tempo_ganhou_perdeu, qtd_jogadas_jogador,
                         qtd_jogadas_robo, pontos_jogador, pontos_robo, placar, ganhou, tabuleiro, cartas_jogador, cartas_robo, jogadas):

    tabuleiro_list = []

    for i, carta in enumerate(tabuleiro):
        carta_dict = {i: carta.nome}
        tabuleiro_list.append(carta_dict)
    
    segundos_narracao = converter_para_segundos(tempo_narracao)
    segundos_jogo = converter_para_segundos(tempo_jogo)
    segundos_ganhou_perdeu = converter_para_segundos(tempo_ganhou_perdeu)
    segundos_total = segundos_narracao + segundos_jogo + segundos_ganhou_perdeu
    tempo_total = converter_para_tempo_formatado(segundos_total)

    dados = {
        "Clicks": clicks,
        "Clicks_peca": clicks_peca,
        "Tempo_narracao": tempo_narracao,
        "Tempo_jogo": tempo_jogo,
        "Tempo_ganhou_perdeu": tempo_ganhou_perdeu,
        "Tempo_total": tempo_total,
        "Qtd_jogadas_jogador": qtd_jogadas_jogador,
        "Qtd_jogadas_robo": qtd_jogadas_robo,
        "Pontos_jogador": pontos_jogador,
        "Pontos_robo": pontos_robo,
        "Placar": str(placar),
        "Ganhou": ganhou,
        "Tabuleiro": str(tabuleiro_list),
        "Cartas_jogador": str([carta.nome for carta in cartas_jogador]),
        "Cartas_robo": str([carta.nome for carta in cartas_robo]),
        "Jogadas": str(jogadas)
    }

    dados_list = list(dados.values())

    salvar_dados_google_sheets(dados_list, "jogo_memoria")


def salvar_dados_google_sheets(dados, sheet_name):

    try:
        
        response = requests.get(f"https://sheets.googleapis.com/v4/spreadsheets/{domino_spreadsheet_id}?key={api_key}")
        if response.status_code == 200:
            print("Conexão com Google Sheets estabelecida")
            data = response.json()
        else:
            print("Erro ao conectar com Google Sheets")
            return

        creds = None

        if os.path.exists('./data/token.json'):
            creds = Credentials.from_authorized_user_file('./data/token.json', SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    './data/credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('./data/token.json', 'w') as token:
                token.write(creds.to_json())

        client = gspread.authorize(creds)
        spreadsheet = client.open_by_key(domino_spreadsheet_id)
        sheet = spreadsheet.worksheet(sheet_name)
        sheet.append_row(dados)

    except Exception as e:
        print("Erro ao salvar dados no Google Sheets: ", e)
        traceback.print_exc()

    

    