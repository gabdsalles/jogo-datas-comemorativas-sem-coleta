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

def salvar_dados_domino(clicks, clicks_peca, tempo, qtd_jogadas_jogador, qtd_jogadas_robo, qtd_pecas_esquerda, qtd_pecas_direita, qtd_pecas_tabuleiro, placar, ganhou,
                        qtd_compras_jogador, qtd_compras_robo, qtd_limpar_tabuleiro, tabuleiro_final, mao_final_jogador, mao_final_robo):
    
    print("Clicks: ", clicks)
    print("Clicks peça: ", clicks_peca)
    print("Tempo: ", tempo)
    print("Qtd jogadas jogador: ", qtd_jogadas_jogador)
    print("Qtd jogadas robo: ", qtd_jogadas_robo)
    print("Qtd peças esquerda: ", qtd_pecas_esquerda)
    print("Qtd peças direita: ", qtd_pecas_direita)
    print("Qtd peças tabuleiro: ", qtd_pecas_tabuleiro)
    print("Placar: ", placar)
    print("Ganhou: ", ganhou)
    print("Qtd compras jogador: ", qtd_compras_jogador)
    print("Qtd compras robo: ", qtd_compras_robo)
    print("Qtd limpar tabuleiro: ", qtd_limpar_tabuleiro)
    print("Tabuleiro final: ", list(tabuleiro_final))
    for peca in mao_final_jogador:
        print("Mão final jogador: ", peca.nome1, peca.nome2)
    
    for peca in mao_final_robo:
        print("Mão final robo: ", peca.nome1, peca.nome2)

    dados = {
        "Clicks": clicks,
        "Clicks_peca": clicks_peca,
        "Tempo": tempo,
        "Qtd_jogadas_jogador": qtd_jogadas_jogador,
        "Qtd_jogadas_robo": qtd_jogadas_robo,
        "Qtd_pecas_esquerda": qtd_pecas_esquerda,
        "Qtd_pecas_direita": qtd_pecas_direita,
        "Qtd_pecas_tabuleiro": qtd_pecas_tabuleiro,
        "Placar": str(placar),
        "Ganhou": ganhou,
        "Qtd_compras_jogador": qtd_compras_jogador,
        "Qtd_compras_robo": qtd_compras_robo,
        "Qtd_limpar_tabuleiro": qtd_limpar_tabuleiro,
        "Tabuleiro_final": str(list(tabuleiro_final)),
        "Mao_final_jogador": str([(peca.nome1, peca.nome2) for peca in mao_final_jogador]),
        "Mao_final_robo": str([(peca.nome1, peca.nome2) for peca in mao_final_robo])
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

    salvar_dados_domino_google_sheets(dados_list)

def salvar_dados_domino_google_sheets(dados):

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
        sheet = spreadsheet.worksheet("domino")
        sheet.append_row(dados)

    except Exception as e:
        print("Erro ao salvar dados no Google Sheets: ", e)
        traceback.print_exc()

    

    