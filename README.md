# SA Descritores API

API REST desacoplada para gestão e acompanhamento de descritores pedagógicos por área, turno, série e turma.

## Stack

- Python 3.12+
- Flask
- SQLAlchemy + Flask-Migrate
- Flask-JWT-Extended
- Marshmallow
- Flask-Smorest com Swagger/OpenAPI
- Flask-CORS
- python-dotenv
- SQLite inicial, com configuração via `DATABASE_URL` preparada para PostgreSQL

## Executando localmente

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
flask --app app:create_app db init
flask --app app:create_app db migrate -m "initial schema"
flask --app app:create_app db upgrade
flask --app app:create_app run
```

A documentação Swagger fica em `/api/docs/swagger-ui`.

## Principais endpoints

Todos os recursos ficam sob `/api/v1`.

- `POST /api/v1/auth/login`
- `POST /api/v1/auth/refresh`
- `GET /api/v1/auth/me`
- `POST /api/v1/auth/logout`
- CRUD administrativo: `/areas`, `/shifts`, `/grades`, `/classes`, `/users`, `/descriptors`, `/questions`
- Operacional: `/applications`, `/answers`, `/alerts`
- Dashboards: `/dashboard/pca` e `/dashboard/admin`

## Segurança e escopo PCA

O controle RBAC separa Administrador e PCA. Administradores possuem acesso total. PCAs só podem alterar aplicações de descritores pertencentes simultaneamente à própria área de conhecimento e ao próprio turno.

## Solução de conflitos no GitHub

Se aparecer um erro como `NameError: name 'codex' is not defined` em `app/extensions.py`, o arquivo ficou com texto de conflito do Git dentro do código. Remova qualquer linha parecida com nome de branch (`codex/...`) e qualquer marcador `<<<<<<<`, `=======` ou `>>>>>>>`.

A versão correta de `app/extensions.py` é:

```python
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_smorest import Api
from flask_cors import CORS

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
smorest_api = Api()
cors = CORS()
```

A versão correta de `app/__init__.py` deve importar e usar `smorest_api`, não `api`:

```python
from app.extensions import db, migrate, jwt, smorest_api, cors
# ...
smorest_api.init_app(app)
register_blueprints(smorest_api)
```
