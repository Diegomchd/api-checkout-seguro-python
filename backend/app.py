import os
import sqlite3
import logging
from datetime import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS

# --- CORREÇÃO DE CAMINHOS ABSOLUTOS ---
# Isso garante que o DB e o Log fiquem exatamente dentro da pasta 'backend'
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, 'vendas.db')
LOG_PATH = os.path.join(BASE_DIR, 'server_audit.log')

logging.basicConfig(filename=LOG_PATH, level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)
# Permite que o Live Server (porta 5500) converse com o Flask (porta 5000)
CORS(app)

def conectar_db():
    return sqlite3.connect(DB_PATH)

def init_db():
    try:
        conn = conectar_db()
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS transacoes 
                          (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                           cliente TEXT, produto_id TEXT, valor REAL, status TEXT, data TEXT)''')
        conn.commit()
        conn.close()
        print("✅ Banco de dados carregado com sucesso!")
    except Exception as e:
        print(f"❌ Erro ao criar banco: {e}")

CATALOGO = {
    "PROD-001": {"nome": "Curso Python", "preco": 297.00},
    "PROD-002": {"nome": "Mentoria ADS", "preco": 500.00}
}

@app.route('/api/pagamento', methods=['POST'])
def processar_pagamento():
    dados = request.json
    p_id = dados.get('produto_id')
    nome = dados.get('nome', 'Visitante')

    if p_id not in CATALOGO:
        return jsonify({"erro": "Produto inválido"}), 400

    produto = CATALOGO[p_id]
    data_formatada = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    try:
        conn = conectar_db()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO transacoes (cliente, produto_id, valor, status, data) VALUES (?, ?, ?, ?, ?)",
                       (nome, p_id, produto['preco'], 'APROVADO', data_formatada))
        conn.commit()
        conn.close()
        logging.info(f"Venda Sucesso: {nome} - {p_id}")
        return jsonify({"checkout_url": "https://sandbox.infinitypay.com.br/pay/sucesso"}), 200
    except Exception as e:
        logging.error(f"Erro DB: {e}")
        return jsonify({"erro": "Falha no servidor"}), 500

@app.route('/api/admin/vendas', methods=['GET'])
def listar_vendas():
    try:
        conn = conectar_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM transacoes ORDER BY id DESC")
        linhas = cursor.fetchall()
        conn.close()

        vendas = [{"id": l[0], "cliente": l[1], "produto": l[2], "valor": l[3], "status": l[4], "data": l[5]} for l in linhas]
        return jsonify(vendas), 200
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

if __name__ == '__main__':
    init_db()
    # O debug=True reinicia o servidor sozinho se você salvar o arquivo
    app.run(port=5000, debug=True)