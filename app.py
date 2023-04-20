
from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from urllib.parse import unquote

from sqlalchemy.exc import IntegrityError

from model import Session, Produto, Comentario
from logger import logger
from schemas import *
from flask_cors import CORS

info = Info(title="Minha API", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# definindo tags
home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
produto_tag = Tag(name="Produto", description="Adição, visualização e remoção de produtos à base")
comentario_tag = Tag(name="Comentario", description="Adição de um comentário à um produtos cadastrado na base")


@app.get('/', tags=[home_tag])
def home():
    """#Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
"""

    return redirect('/openapi')


@app.post('/produto', tags=[produto_tag],
          responses={"200": ProdutoViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_produto(form: ProdutoSchema):
    """#Adiciona um novo Produto à base de dados
    #Retorna uma representação dos produtos e comentários associados.
"""
    produto = Produto(
        nome=form.nome,
        quantidade=form.quantidade,
        valor=form.valor)
    logger.debug(f"Adicionando produto de nome: '{produto.nome}'")
    try:
        # criando conexão com a base
        session = Session()
        # adicionando produto
        session.add(produto)
        # efetivando o camando de adição de novo item na tabela
        session.commit()
        logger.debug(f"Adicionado produto de nome: '{produto.nome}'")
        return apresenta_produto(produto), 200

    except IntegrityError as e:
        # como a duplicidade do nome é a provável razão do IntegrityError
        error_msg = "Produto de mesmo nome já salvo na base :/"
        logger.warning(f"Erro ao adicionar produto '{produto.nome}', {error_msg}")
        return {"mesage": error_msg}, 409

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível salvar novo item :/"
        logger.warning(f"Erro ao adicionar produto '{produto.nome}', {error_msg}")
        return {"mesage": error_msg}, 400


@app.get('/produtos', tags=[produto_tag],
         responses={"200": ListagemProdutosSchema, "404": ErrorSchema})
def get_produtos():
    """#Faz a busca por todos os Produto cadastrados
    #Retorna uma representação da listagem de produtos.
"""
    logger.debug(f"Coletando produtos ")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    produtos = session.query(Produto).all()

    if not produtos:
        # se não há produtos cadastrados
        return {"produtos": []}, 200
    else:
        logger.debug(f"%d rodutos econtrados" % len(produtos))
        # retorna a representação de produto
        print(produtos)
        return apresenta_produtos(produtos), 200


@app.get('/produto', tags=[produto_tag],
         responses={"200": ProdutoViewSchema, "404": ErrorSchema})
def get_produto(query: ProdutoBuscaSchema):
    """#Faz a busca por um Produto a partir do id do produto
    #Retorna uma representação dos produtos e comentários associados.
"""
    produto_id = query.id
    logger.debug(f"Coletando dados sobre produto #{produto_id}")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    produto = session.query(Produto).filter(Produto.id == produto_id).first()

    if not produto:
        # se o produto não foi encontrado
        error_msg = "Produto não encontrado na base :/"
        logger.warning(f"Erro ao buscar produto '{produto_id}', {error_msg}")
        return {"mesage": error_msg}, 404
    else:
        logger.debug(f"Produto econtrado: '{produto.nome}'")
        # retorna a representação de produto
        return apresenta_produto(produto), 200


@app.delete('/produto', tags=[produto_tag],
            responses={"200": ProdutoDelSchema, "404": ErrorSchema})
def del_produto(query: ProdutoBuscaSchema):
    """#Deleta um Produto a partir do nome de produto informado
    #Retorna uma mensagem de confirmação da remoção.
"""
    produto_nome = unquote(unquote(query.nome))
    print(produto_nome)
    logger.debug(f"Deletando dados sobre produto #{produto_nome}")
    # criando conexão com a base
    session = Session()
    # fazendo a remoção
    count = session.query(Produto).filter(Produto.nome == produto_nome).delete()
    session.commit()

    if count:
        # retorna a representação da mensagem de confirmação
        logger.debug(f"Deletado produto #{produto_nome}")
        return {"mesage": "Produto removido", "id": produto_nome}
    else:
        # se o produto não foi encontrado
        error_msg = "Produto não encontrado na base :/"
        logger.warning(f"Erro ao deletar produto #'{produto_nome}', {error_msg}")
        return {"mesage": error_msg}, 404


@app.post('/cometario', tags=[comentario_tag],
          responses={"200": ProdutoViewSchema, "404": ErrorSchema})
def add_comentario(form: ComentarioSchema):
    """#Adiciona de um novo comentário à um produtos cadastrado na base identificado pelo id
    #Retorna uma representação dos produtos e comentários associados.
"""
    produto_id  = form.produto_id
    logger.debug(f"Adicionando comentários ao produto #{produto_id}")
    # criando conexão com a base
    session = Session()
    # fazendo a busca pelo produto
    produto = session.query(Produto).filter(Produto.id == produto_id).first()

    if not produto:
        # se produto não encontrado
        error_msg = "Produto não encontrado na base :/"
        logger.warning(f"Erro ao adicionar comentário ao produto '{produto_id}', {error_msg}")
        return {"mesage": error_msg}, 404

    # criando o comentário
    texto = form.texto
    comentario = Comentario(texto)

    # adicionando o comentário ao produto
    produto.adiciona_comentario(comentario)
    session.commit()

    logger.debug(f"Adicionado comentário ao produto #{produto_id}")

    # retorna a representação de produto
    return apresenta_produto(produto), 200


"""
from flask import Flask, request, send_from_directory, render_template
from sqlalchemy.exc import IntegrityError

from model import Session, Service
from model.comentario import Comentario


app = Flask(__name__)
# app = Flask("abc")

@app.route('/')
def login():
    return render_template("login.html"), 200

@app.route('/home')
def home():
    return render_template("home.html"), 200

@app.route('/new_project')
def new_project():
    return render_template("new_project.html"), 200

@app.route('/open_project')
def open_project():
    return render_template("open_project.html"), 200

@app.route('/services')
def services():
    return render_template("services.html"), 200

@app.route('/units')
def units():
    return render_template("units.html"), 200

@app.route('/classification')
def classification():
    return render_template("classification.html"), 200

@app.route('/logout')
def logout():
    return render_template("login.html"), 200



@app.route('/favicon.ico')
def favicon():
    return send_from_directory('static', 'favicon.ico', mimetype='image/x-icon')
"""
@app.route('/service_new')
def service_new():
    return render_template("service_new.html"), 200


@app.route('/service_register', methods=['POST'])
def service_register():
    session = Session()
    service = Service(
        developer_code = request.form.get("developer_code"),
        base_description = request.form.get("base_description"),
        especification = request.form.get("especification"),
        manufactory_reference = request.form.get("manufactory_reference")
    )
        # adicionando service
    session.add(service)
        # efetivando o camando de adição de novo item na tabela
    session.commit()
    return render_template("service_register.html"), 200
"""

@app.route('/service_register', methods=['POST'])
def service_register():
    session = Session()
    service = Service(
        base_description = request.form.get("base_description"),
        especification_title = request.form.get("especification_title"),
        especification = request.form.get("especification"),
        manufactory_reference = request.form.get("manufactory_reference"),
        bim = request.form.get("bim"),
        developer_code = request.form.get("developer_code"),
        countable = request.form.get("countable"),
        schedule = request.form.get("schedule"),
        script = request.form.get("script"),
        ifc = request.form.get("ifc"),
        technical_approver = request.form.get("ifc"),
        bim_approver = request.form.get("bim_approver")
    )
    try:
        session.add(service)
        session.commit()
        return render_template("services.html",service=service), 200
    except IntegrityError as e:
        error_msg = "Service de mesmo nome já salvo na base :/"
        return render_template("error.html", error_code=409, error_msg=error_msg), 409
    except Exception as e:
        error_msg = "Não foi possível salvar novo item :/"
        print(str(e))
        return render_template("error.html", error_code=400, error_msg=error_msg), 400


@app.route('/unit_register', methods=['POST'])
def unit_register():
    session = Session()
    unit = Unit(
        unit = request.form.get("unit"),
        abbreviation = request.form.get("abbreviation"),
    )
    try:
        session.add(unit)
        session.commit()
        return render_template("units.html",unit=unit), 200
    except IntegrityError as e:
        error_msg = "Service de mesmo nome já salvo na base :/"
        return render_template("error.html", error_code=409, error_msg=error_msg), 409
    except Exception as e:
        error_msg = "Não foi possível salvar novo item :/"
        print(str(e))
        return render_template("error.html", error_code=400, error_msg=error_msg), 400
    

@app.route('/get_service', methods=['GET'])
def get_service():
    session = Session()
    service = session.query(Service).all
    print(service)
    return apresenta_service(service), 200
 

    """
    if not service:
        error_msg = "Service não encontrado na base :/"
        return render_template("error.html", error_code= 404, error_msg=error_msg), 404
    else:
        return render_template("service.html", service=service), 200
    """

@app.route('/get_service/<service_id>', methods=['GET'])
def get_service2(service_id):
    session = Session()
    service = session.query(Service).filter(Service.id == service_id).first()
    if not service:
        error_msg = "Service não encontrado na base :/"
        return render_template("error.html", error_code= 404, error_msg=error_msg), 404
    else:
        return render_template("service.html", service=service), 200


@app.route('/del_service/<service_id>', methods=['DELETE'])
def del_service(service_id):
    session = Session()
    count = session.query(Service).filter(Service.id == service_id).delete()
    session.commit()
    if count ==1:
        return render_template("deletado.html", service_id=service_id), 200
    else: 
        error_msg = "Service não encontrado na base :/"
        return render_template("error.html", error_code=404, error_msg=error_msg), 404


@app.route('/add_comentario/<service_id>', methods=['POST'])
def add_comentario(service_id):
    session = Session()
    service = session.query(Service).filter(Service.id == service_id).first()
    if not service:
        error_msg = "Service não encontrado na base :/"
        return render_template("error.html", error_code= 404, error_msg=error_msg), 404

    autor = request.form.get("autor")
    texto = request.form.get("texto")
    n_estrelas = request.form.get("n_estrela")
    if n_estrelas:
        n_estrelas = int(n_estrelas)

    comentario = Comentario(autor, texto, n_estrelas)
    service.adiciona_comentario(comentario)
    session.commit()
    return render_template("service.html", service=service), 200

    """