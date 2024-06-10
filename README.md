
# WhatsApp Bot para Coleta de Leads e Envio de Informações

Este projeto é um bot para WhatsApp, desenvolvido com Flask e Twilio, que coleta informações de leads e envia essas informações para um número de WhatsApp pessoal, além de armazenar os dados em uma planilha e enviar essa planilha por e-mail. O bot é configurado para interagir com usuários e coletar informações sobre seus interesses e necessidades.

## Funcionalidades

- Coleta informações de usuários através do WhatsApp.
- Armazena as informações em um banco de dados SQLite.
- Atualiza uma planilha Excel com os dados coletados.
- Envia a planilha atualizada por e-mail.
- Notifica o WhatsApp pessoal com os detalhes do lead coletado.

## Tecnologias Utilizadas

- Python
- Flask
- Twilio API
- SQLite
- Openpyxl
- SMTP (para envio de e-mail)

## Pré-requisitos

- Conta no Twilio
- Credenciais da API do Twilio
- Conta no Gmail para envio de e-mails
- Python 3.6+ instalado
- Ngrok (para expor o servidor local)

## Configuração

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/LeonardoRFragoso/ChatBot-WhatsApp
   cd seu-repositorio
   ```

2. **Crie e ative um ambiente virtual (opcional, mas recomendado):**
   ```bash
   python -m venv venv
   source venv/bin/activate   # No Windows, use `venv\Scripts\activate`
   ```

3. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure suas credenciais do Twilio e do Gmail no código:**
   - No arquivo `wpp.py`, atualize as variáveis `account_sid`, `auth_token`, `twilio_whatsapp_number`, `personal_whatsapp_number`, `email_user`, `email_password`, `email_send_list`.

5. **Configure o webhook do Twilio:**
   - Use o [Ngrok](https://ngrok.com/) para expor seu servidor local:
     ```bash
     ngrok http 5000
     ```
   - Configure o URL do webhook no console do Twilio com a URL gerada pelo Ngrok (ex: `https://seu-url-ngrok.ngrok.io/whatsapp`).

6. **Execute o servidor Flask:**
   ```bash
   python wpp.py
   ```

## Uso

1. Envie uma mensagem "start" para o número do WhatsApp configurado no Twilio.
2. Siga as instruções do bot para fornecer seu nome, sobrenome, interesse e uma breve descrição.
3. As informações coletadas serão armazenadas e enviadas conforme configurado.

## Estrutura do Projeto

```
├── leads.db              # Banco de dados SQLite
├── leads.xlsx            # Planilha Excel com dados coletados
├── wpp.py                # Código principal do bot
├── requirements.txt      # Dependências do projeto
└── README.md             # Este arquivo
```

## Considerações Finais

Este bot foi desenvolvido para facilitar a coleta de leads e a comunicação com potenciais clientes. Certifique-se de configurar corretamente todas as variáveis e credenciais para garantir o funcionamento adequado do bot.

## Licença

Este projeto está licenciado sob a [MIT License](LICENSE).

## Contato

Para mais informações, entre em contato:

- Email: [leonardorfragoso@gmail.com](mailto:leonardorfragoso@gmail.com)
- Website: [PyScript.Tech](https://www.pyscript.tech/)
