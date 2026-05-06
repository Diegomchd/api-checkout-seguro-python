#  Microsserviço de Checkout & Painel Administrativo

Este projeto demonstra uma integração completa de e-commerce focada em **Segurança de Dados** e **Arquitetura de Sistemas**.

##  Tecnologias Utilizadas
- **Backend:** Python + Flask (API REST)
- **Banco de Dados:** SQLite (Persistência de transações)
- **Frontend:** Vanilla JavaScript (Fetch API) & CSS3 Profissional
- **Auditoria:** Sistema de logs automático (`server_audit.log`)

##  Diferenciais Técnicos (Padrão ADS)
- **Validação Server-Side:** O preço é validado no servidor para evitar manipulações no HTML.
- **Segurança de Credenciais:** Uso de `.env.example` para proteção de chaves de API.
- **Feedback de Interface:** Botões com estado de carregamento para evitar duplicidade de pedidos.

##  Como testar
1. Instale as dependências: `pip install -r backend/requirements.txt`
2. Inicie o servidor: `python backend/app.py`
3. Acesse `index.html` para comprar e `admin.html` para ver o relatório.