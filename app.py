from flask import Flask, render_template, request
import csv
import smtplib
from email.mime.text import MIMEText
import os

app = Flask(__name__)

# Função para buscar resposta no CSV
def buscar_resposta(categoria, subcategoria, motivo):
    with open("respostas.csv", encoding="utf-8") as arquivo:
        leitor = csv.DictReader(arquivo, delimiter=";")
        for linha in leitor:
            cat = linha["Categoria"].strip().lower()
            sub = linha["Subcategoria"].strip().lower()
            mot = linha["Motivo"].strip().lower()
            if cat != categoria.strip().lower():
                continue
            if subcategoria and sub != subcategoria.strip().lower():
                continue
            if motivo and mot != motivo.strip().lower():
                continue
            return linha["Resposta"]
    return "Nenhuma resposta encontrada para os dados fornecidos."

# Função para enviar e-mail
def enviar_email(destinatario, assunto, mensagem):
    remetente = os.getenv("peehhenriquee18@gmail.com")
    senha = os.getenv("fbsl xagv zklg wmrs")

    msg = MIMEText(mensagem)
    msg["Subject"] = assunto
    msg["From"] = remetente
    msg["To"] = destinatario

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(remetente, senha)
        smtp.send_message(msg)

@app.route("/", methods=["GET", "POST"])
def index():
    mensagem = ""
    resposta = ""
    email = ""
    if request.method == "POST":
        email = request.form["email"]
        categoria = request.form["categoria"]
        subcategoria = request.form["subcategoria"]
        motivo = request.form["motivo"]
        resposta = buscar_resposta(categoria, subcategoria, motivo)
        try:
            enviar_email(email, "Resposta do RH", resposta)
            mensagem = f"Sua pergunta foi enviada para {email}."
        except Exception as e:
            mensagem = f"Erro ao enviar e-mail: {e}"
    return render_template("index.html", mensagem=mensagem, resposta=resposta, email=email)


if __name__ == "__main__":
    app.run(debug=True, port=5001)
