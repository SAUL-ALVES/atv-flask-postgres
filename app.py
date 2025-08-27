import os
from typing import Optional, Tuple, List
from dotenv import load_dotenv
from flask import Flask, jsonify, request, render_template, redirect, url_for, flash
import bcrypt
import psycopg
from psycopg.rows import dict_row


try:
    from psycopg_pool import ConnectionPool
    HAS_POOL = True
except ImportError:
    HAS_POOL = False


load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:admin@localhost:5432/web1")

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET", "uma-chave-secreta-forte")
app.config["TEMPLATES_AUTO_RELOAD"] = True


if HAS_POOL:
    pool = ConnectionPool(conninfo=DATABASE_URL, min_size=1, max_size=5, timeout=10)
    def _conn():
        return pool.connection()
else:
    def _conn():
        return psycopg.connect(DATABASE_URL, row_factory=dict_row)


def db_query(sql: str, params: Optional[Tuple] = None) -> List[dict]:
    with _conn() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute(sql, params or ())
            return cur.fetchall()

def db_execute(sql: str, params: Optional[Tuple] = None, returning: bool = False):
    with _conn() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute(sql, params or ())
            rows = cur.fetchall() if returning else None
        conn.commit()
    return rows


def hash_password(plain: str) -> str:
    return bcrypt.hashpw(plain.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

@app.get("/")
def index():
    return redirect(url_for("users_page"))

@app.get("/users/new")
def users_new_form():
    """Renderiza o formulário de cadastro (HTML)."""
    return render_template("users_new.html")

@app.post("/users/form")
def users_create_from_form():
    try:
        nome = (request.form.get("nome") or "").strip()
        email = (request.form.get("email") or "").strip().lower()
        senha = request.form.get("senha") or ""

        if not all([nome, email, senha]):
            flash("Preencha nome, email e senha.", "error")
            return redirect(url_for("users_new_form"))

        senha_hash = hash_password(senha)

        row = db_execute(
            "INSERT INTO public.usuarios (nome, email, senha) VALUES (%s, %s, %s) RETURNING id, nome, email;",
            (nome, email, senha_hash),
            returning=True,
        )
        flash(f"Usuário {row[0]['email']} criado com sucesso!", "success")
        return redirect(url_for("users_page"))
    except psycopg.errors.UniqueViolation:
        flash("Email já cadastrado.", "error")
        return redirect(url_for("users_new_form"))
    except Exception as e:
        flash(f"Erro inesperado: {e}", "error")
        return redirect(url_for("users_new_form"))


@app.get("/users/page")
def users_page():
    try:
        q = (request.args.get("q") or "").strip()
        if q:
            like = f"%{q}%"
            rows = db_query(
                "SELECT id, nome, email FROM public.usuarios WHERE nome ILIKE %s OR email ILIKE %s ORDER BY id ASC;",
                (like, like),
            )
        else:
            rows = db_query("SELECT id, nome, email FROM public.usuarios ORDER BY id ASC;")
        return render_template("users_page.html", users=rows, q=q)
    except Exception as e:
        return f"<h3>Erro ao listar usuários:</h3><pre>{e}</pre>", 500


@app.get("/users/<int:user_id>/edit")
def users_edit_form(user_id: int):
    try:
        rows = db_query("SELECT id, nome, email FROM public.usuarios WHERE id = %s;", (user_id,))
        if not rows:
            flash("Usuário não encontrado.", "error")
            return redirect(url_for("users_page"))
        return render_template("users_edit.html", user=rows[0])
    except Exception as e:
        flash(f"Erro ao carregar formulário: {e}", "error")
        return redirect(url_for("users_page"))

@app.post("/users/<int:user_id>/edit")
def users_update_from_form(user_id: int):
    try:
        nome  = (request.form.get("nome") or "").strip()
        email = (request.form.get("email") or "").strip().lower()
        senha = request.form.get("senha")

        if not nome or not email:
            flash("Nome e email são obrigatórios.", "error")
            return redirect(url_for("users_edit_form", user_id=user_id))

        sets = ["nome = %s", "email = %s"]
        params = [nome, email]

        if senha:
            senha_hash = hash_password(senha)
            sets.append("senha = %s")
            params.append(senha_hash)

        params.append(user_id)
        sql = f"UPDATE public.usuarios SET {', '.join(sets)} WHERE id = %s RETURNING id;"
        rows = db_execute(sql, tuple(params), returning=True)
        if not rows:
            flash("Usuário não encontrado.", "error")
        else:
            flash("Usuário atualizado com sucesso.", "success")
        
        return redirect(url_for("users_page"))
    except psycopg.errors.UniqueViolation:
        flash("Email já cadastrado por outro usuário.", "error")
        return redirect(url_for("users_edit_form", user_id=user_id))
    except Exception as e:
        flash(f"Erro ao atualizar: {e}", "error")
        return redirect(url_for("users_edit_form", user_id=user_id))


@app.get("/users/<int:user_id>/confirm_delete")
def users_confirm_delete(user_id: int):
    try:
        rows = db_query("SELECT id, nome, email FROM public.usuarios WHERE id = %s;", (user_id,))
        if not rows:
            flash("Usuário não encontrado.", "error")
            return redirect(url_for("users_page"))
        return render_template("users_confirm_delete.html", user=rows[0])
    except Exception as e:
        flash(f"Erro: {e}", "error")
        return redirect(url_for("users_page"))

@app.post("/users/<int:user_id>/delete")
def users_delete_from_form(user_id: int):
    try:
        rows = db_execute("DELETE FROM public.usuarios WHERE id = %s RETURNING id;", (user_id,), returning=True)
        if not rows:
            flash("Usuário não encontrado.", "error")
        else:
            flash("Usuário excluído com sucesso.", "success")
        return redirect(url_for("users_page"))
    except Exception as e:
        flash(f"Erro ao excluir: {e}", "error")
        return redirect(url_for("users_page"))



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)