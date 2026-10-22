import os
import sqlite3
from datetime import datetime
from pathlib import Path

from flask import Flask, abort, flash, redirect, render_template, request, url_for

BASE_DIR = Path(__file__).resolve().parent
DATABASE = Path(os.environ.get("GESTAO_DB", BASE_DIR / "instance" / "registros.db"))

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-chave-trocar-antes-de-publicar")
app.config["MAX_CONTENT_LENGTH"] = 1 * 1024 * 1024

CATEGORIAS = ["Doações", "Voluntariado", "Atividades", "Materiais", "Outros"]
STATUS = ["Ativo", "Inativo"]


def conectar_banco():
    DATABASE.parent.mkdir(parents=True, exist_ok=True)
    conexao = sqlite3.connect(DATABASE)
    conexao.row_factory = sqlite3.Row
    return conexao


def inicializar_banco():
    with conectar_banco() as conexao:
        conexao.execute("""
            CREATE TABLE IF NOT EXISTS registros (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titulo TEXT NOT NULL,
                descricao TEXT NOT NULL DEFAULT '',
                categoria TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'Ativo',
                data_cadastro TEXT NOT NULL
            )
        """)


inicializar_banco()


def validar_campos(form):
    titulo = form.get("titulo", "").strip()
    descricao = form.get("descricao", "").strip()
    categoria = form.get("categoria", "").strip()
    status = form.get("status", "Ativo").strip()

    erros = []
    if not titulo:
        erros.append("O título é obrigatório.")
    elif len(titulo) > 120:
        erros.append("O título deve ter no máximo 120 caracteres.")
    if len(descricao) > 1000:
        erros.append("A descrição deve ter no máximo 1.000 caracteres.")
    if categoria not in CATEGORIAS:
        erros.append("Selecione uma categoria válida.")
    if status not in STATUS:
        erros.append("Selecione um status válido.")
    return {"titulo": titulo, "descricao": descricao, "categoria": categoria, "status": status}, erros


@app.get("/")
def inicio():
    with conectar_banco() as conexao:
        total = conexao.execute("SELECT COUNT(*) FROM registros").fetchone()[0]
        ativos = conexao.execute("SELECT COUNT(*) FROM registros WHERE status = 'Ativo'").fetchone()[0]
        recentes = conexao.execute(
            "SELECT * FROM registros ORDER BY id DESC LIMIT 5"
        ).fetchall()
    return render_template("index.html", total=total, ativos=ativos, recentes=recentes)


@app.get("/registros")
def listar_registros():
    termo = request.args.get("q", "").strip()
    categoria = request.args.get("categoria", "").strip()
    sql = "SELECT * FROM registros WHERE 1=1"
    parametros = []
    if termo:
        sql += " AND (titulo LIKE ? OR descricao LIKE ?)"
        parametros.extend([f"%{termo}%", f"%{termo}%"])
    if categoria in CATEGORIAS:
        sql += " AND categoria = ?"
        parametros.append(categoria)
    sql += " ORDER BY id DESC"

    with conectar_banco() as conexao:
        registros = conexao.execute(sql, parametros).fetchall()
    return render_template(
        "registros.html", registros=registros, q=termo,
        categoria_selecionada=categoria, categorias=CATEGORIAS
    )


@app.route("/registros/novo", methods=["GET", "POST"])
def novo_registro():
    valores = {"titulo": "", "descricao": "", "categoria": "", "status": "Ativo"}
    if request.method == "POST":
        valores, erros = validar_campos(request.form)
        if not erros:
            with conectar_banco() as conexao:
                conexao.execute(
                    """INSERT INTO registros (titulo, descricao, categoria, status, data_cadastro)
                       VALUES (?, ?, ?, ?, ?)""",
                    (valores["titulo"], valores["descricao"], valores["categoria"],
                     valores["status"], datetime.now().strftime("%d/%m/%Y %H:%M"))
                )
            flash("Registro cadastrado com sucesso.", "success")
            return redirect(url_for("listar_registros"))
        for erro in erros:
            flash(erro, "error")
    return render_template("formulario.html", valores=valores, categorias=CATEGORIAS,
                           titulo_pagina="Novo registro", acao="Cadastrar")


@app.route("/registros/<int:registro_id>/editar", methods=["GET", "POST"])
def editar_registro(registro_id):
    with conectar_banco() as conexao:
        registro = conexao.execute(
            "SELECT * FROM registros WHERE id = ?", (registro_id,)
        ).fetchone()
    if registro is None:
        abort(404)

    valores = dict(registro)
    if request.method == "POST":
        valores, erros = validar_campos(request.form)
        if not erros:
            with conectar_banco() as conexao:
                conexao.execute(
                    """UPDATE registros SET titulo = ?, descricao = ?, categoria = ?, status = ?
                       WHERE id = ?""",
                    (valores["titulo"], valores["descricao"], valores["categoria"],
                     valores["status"], registro_id)
                )
            flash("Registro atualizado com sucesso.", "success")
            return redirect(url_for("listar_registros"))
        for erro in erros:
            flash(erro, "error")
    return render_template("formulario.html", valores=valores, categorias=CATEGORIAS,
                           titulo_pagina="Editar registro", acao="Salvar alterações")


@app.post("/registros/<int:registro_id>/excluir")
def excluir_registro(registro_id):
    with conectar_banco() as conexao:
        cursor = conexao.execute("DELETE FROM registros WHERE id = ?", (registro_id,))
        if cursor.rowcount == 0:
            abort(404)
    flash("Registro excluído com sucesso.", "success")
    return redirect(url_for("listar_registros"))


@app.errorhandler(404)
def pagina_nao_encontrada(_erro):
    return render_template("404.html"), 404


if __name__ == "__main__":
    app.run(debug=os.environ.get("FLASK_DEBUG") == "1")
