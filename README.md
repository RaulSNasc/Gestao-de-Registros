# Gestão de Registros

MVP acadêmico de uma aplicação web para organizar informações de uma organização comunitária, permitindo cadastrar, consultar, editar e excluir registros em uma interface responsiva.

## Funcionalidades

- Cadastro de registros com título, categoria, descrição e status.
- Listagem e busca por título ou descrição.
- Filtro por categoria.
- Edição de registros existentes.
- Exclusão com confirmação.
- Validação dos dados no servidor.
- Armazenamento persistente em SQLite.
- Mensagens de sucesso e erro.
- Interface adaptável a celular e computador, com foco visível e navegação por teclado.

## Tecnologias

- Python 3.12+
- Flask
- SQLite
- HTML5 e CSS3
- Jinja2
- pytest

## Executar localmente

1. Instale Python 3.12 ou superior.
2. Abra um terminal na pasta do projeto.
3. Crie e ative um ambiente virtual:

   **Windows (PowerShell):**
   ```powershell
   py -m venv .venv
   .venv\\Scripts\\Activate.ps1
   ```

   **Linux/macOS:**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

4. Instale as dependências:

   ```bash
   pip install -r requirements.txt
   ```

5. Defina uma chave secreta para a sessão antes de executar (recomendado):

   **Windows PowerShell:**
   ```powershell
   $env:SECRET_KEY="substitua-por-uma-chave-aleatoria"
   ```

   **Linux/macOS:**
   ```bash
   export SECRET_KEY="substitua-por-uma-chave-aleatoria"
   ```

6. Inicie a aplicação:

   ```bash
   python app.py
   ```

7. Abra no navegador o endereço `http://127.0.0.1:5000`.

O banco `instance/registros.db` será criado automaticamente na primeira execução. Faça backup do banco se houver dados que precisem ser preservados.

## Executar testes

```bash
pytest -q
```

## Estrutura

```text
gestao-de-registros/
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── formulario.html
│   ├── registros.html
│   └── 404.html
├── static/
│   └── css/
│       └── style.css
└── tests/
    └── test_app.py
```

## Escopo e limitações

Este é um MVP para demonstração e avaliação acadêmica. A versão atual não implementa autenticação de usuários, perfis de acesso, proteção CSRF via token nem limitação de tentativas. Antes de disponibilizar publicamente para uso real, implemente esses controles, configure `SECRET_KEY` segura, use HTTPS, revise os testes de segurança e defina uma política de backup e retenção dos dados.

Use apenas dados fictícios durante a demonstração. Não publique o banco SQLite nem segredos no repositório.
