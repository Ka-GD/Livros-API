import sqlite3  
from flask import Flask, request, jsonify  

app = Flask(__name__) 

@app.route("/")
def home():
    return "<h2>Bem-vindo à API de Livros!</h2>"

@app.route("/livro")
def manda_o_pix():
    return "<h2>doação</h2>" 
# toda api tem endpoint
# comando pra criar a conexão com db conn e coon.execute é pra executar a tabela init_db é pra iniciar
def init_db():
    with sqlite3.connect("database.db") as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS LIVROS (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titulo TEXT NOT NULL,
                categoria TEXT NOT NULL,
                autor TEXT NOT NULL,
                image_url TEXT NOT NULL
            )
        """)  
# create table é pra criar a tabela if not exists é pra criar só se não tiver a tabela já criada

init_db()

# route cria as rotas como no react só q aq é endpoint é como a gente se comunica com a api
@app.route("/doar", methods=["POST"])
def doar():
    dados = request.get_json()

#    o erro 400 é do lado do cliente não tem haver com o 500 erro de servidor
    if not all(key in dados for key in ["titulo", "categoria", "autor", "image_url"]):
        return jsonify({"erro": "Todos os campos são obrigatórios"}), 400  

    titulo = dados["titulo"]
    categoria = dados["categoria"]
    autor = dados["autor"]
    image_url = dados["image_url"]

    # erro 200 é quando da tudo certo
    with sqlite3.connect("database.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO LIVROS (titulo, categoria, autor, image_url) 
            VALUES (?, ?, ?, ?)
        """, (titulo, categoria, autor, image_url))
        conn.commit() 
    return jsonify({"mensagem": "Livro cadastrado com sucesso"}), 201


if __name__ == "__main__":
    app.run(debug=True)
# app.run é pra rodar todas as  rotas ou endpoint dentro