from twilio.rest import Client
from flask import Flask, request
import sqlite3
import logging
import openpyxl
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import os

app = Flask(__name__)

# Configurar logging
logging.basicConfig(level=logging.DEBUG)

# Insira suas credenciais corretas aqui
account_sid = 'ACd622a932f08478adf9a1b8a94bdb166d'
auth_token = '6fa763c04318ac9074e18b13c1e7909d'
client = Client(account_sid, auth_token)

# Número de telefone do Twilio para WhatsApp
twilio_whatsapp_number = 'whatsapp:+14155238886'
personal_whatsapp_number = 'whatsapp:+5521980292791'

# URL do site da PyScript.Tech
url = "https://www.pyscript.tech/"

# Dicionário para armazenar estados dos usuários
user_states = {}

# Função para inserir um registro de lead no banco de dados
def registrar_lead(user_id, user_name, user_last_name, user_username, interesse, descricao):
    # Cria uma conexão separada para garantir que cada operação ocorra na mesma thread
    conn = sqlite3.connect('leads.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS leads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            user_name TEXT NOT NULL,
            user_last_name TEXT,
            user_username TEXT,
            interesse TEXT NOT NULL,
            descricao TEXT
        )
    ''')
    conn.commit()

    cursor.execute('''
        INSERT INTO leads (user_id, user_name, user_last_name, user_username, interesse, descricao)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (user_id, user_name, user_last_name, user_username, interesse, descricao))
    conn.commit()
    conn.close()

    enviar_mensagem_pessoal(user_name, user_last_name, user_username, interesse, descricao)
    atualizar_planilha(user_name, user_last_name, user_username, interesse, descricao)
    enviar_email()

# Função para enviar mensagem para o WhatsApp pessoal
def enviar_mensagem_pessoal(user_name, user_last_name, user_username, interesse, descricao):
    mensagem = f"Novo lead:\nNome: {user_name} {user_last_name}\nUsername: {user_username}\nInteresse: {interesse}\nDescrição: {descricao}"
    client.messages.create(
        body=mensagem,
        from_=twilio_whatsapp_number,
        to=personal_whatsapp_number
    )

# Função para atualizar a planilha
def atualizar_planilha(user_name, user_last_name, user_username, interesse, descricao):
    file_path = 'leads.xlsx'
    
    if not os.path.exists(file_path):
        workbook = openpyxl.Workbook()
        sheet = workbook.active
        sheet.append(['Nome', 'Sobrenome', 'Username', 'Interesse', 'Descrição'])
    else:
        workbook = openpyxl.load_workbook(file_path)
        sheet = workbook.active

    sheet.append([user_name, user_last_name, user_username, interesse, descricao])
    workbook.save(file_path)

# Função para enviar a planilha por e-mail
def enviar_email():
    email_user = 'leonardorfragoso@gmail.com'
    email_password = 'ofanteltgansbxju'
    email_send_list = ['leonardorfragoso@gmail.com', 'pyscript.tech@gmail.com']

    subject = 'Novos Leads'

    msg = MIMEMultipart()
    msg['From'] = email_user
    msg['To'] = ', '.join(email_send_list)
    msg['Subject'] = subject

    body = 'Segue em anexo a planilha atualizada com os novos leads.'
    msg.attach(MIMEText(body, 'plain'))

    filename = 'leads.xlsx'
    attachment = open(filename, 'rb')

    part = MIMEApplication(attachment.read(), Name=filename)
    part['Content-Disposition'] = f'attachment; filename={filename}'
    msg.attach(part)

    attachment.close()

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(email_user, email_password)
    text = msg.as_string()
    server.sendmail(email_user, email_send_list, text)
    server.quit()

# Função para manipular as mensagens recebidas
@app.route("/whatsapp", methods=['POST'])
def whatsapp():
    global user_states

    try:
        logging.debug("Recebendo requisição do Twilio")
        user_id = request.form['From']
        message_text = request.form['Body'].strip()
        user_first_name = user_id  # No WhatsApp, não há informações de nome no número, então usamos o ID

        logging.debug(f"Mensagem recebida: {message_text} de {user_id}")

        # Inicializa o estado do usuário se não existir
        if user_id not in user_states:
            user_states[user_id] = {'state': 'start'}

        state = user_states[user_id]['state']

        if state == 'start':
            if message_text.lower() == 'start':
                send_message(user_id, "Olá! Bem-vindo à PyScript.Tech! Qual é o seu nome?")
                user_states[user_id]['state'] = 'perguntando_nome'

        elif state == 'perguntando_nome':
            user_states[user_id]['user_name'] = message_text
            send_message(user_id, f"Obrigado, {message_text}! Qual é o seu sobrenome?")
            user_states[user_id]['state'] = 'perguntando_sobrenome'

        elif state == 'perguntando_sobrenome':
            user_states[user_id]['user_last_name'] = message_text
            user_name = user_states[user_id]['user_name']
            user_last_name = user_states[user_id]['user_last_name']
            send_message(user_id, f"Perfeito, {user_name} {user_last_name}! Aqui estão alguns dos serviços que oferecemos:")
            send_message(user_id, "1. Desenvolvimento Web\n2. Criação de Bots\n3. Automação com Python\n\nPara mais informações, visite nosso site: " + url)
            send_message(user_id, "Você está interessado em algum serviço específico? (Desenvolvimento Web/Criação de Bots/Automação com Python)")
            user_states[user_id]['state'] = 'confirmando_interesse'

        elif state == 'confirmando_interesse':
            user_states[user_id]['interesse'] = message_text
            send_message(user_id, "Por favor, descreva brevemente sua necessidade:")
            user_states[user_id]['state'] = 'perguntando_descricao'

        elif state == 'perguntando_descricao':
            descricao = message_text
            user_name = user_states[user_id]['user_name']
            user_last_name = user_states[user_id]['user_last_name']
            interesse = user_states[user_id]['interesse']

            registrar_lead(user_id, user_name, user_last_name, user_first_name, interesse, descricao)
            send_message(user_id, "Obrigado pelo seu interesse! Nossa equipe entrará em contato com você em breve.")
            send_message(user_id, f"Enquanto isso, você pode explorar mais sobre nossos serviços em nosso site: {url}")

            # Reseta o estado do usuário para permitir um novo início
            user_states[user_id]['state'] = 'start'

        return "OK", 200
    except Exception as e:
        logging.error(f"Erro no webhook do WhatsApp: {e}")
        return "Erro no servidor", 500

# Função para enviar mensagem via Twilio
def send_message(to, body):
    client.messages.create(
        body=body,
        from_=twilio_whatsapp_number,
        to=to
    )

if __name__ == "__main__":
    app.run(debug=True, port=5000)
