from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect, jsonify
from urllib.parse import unquote

from sqlalchemy.exc import IntegrityError

from models import Session, Cliente, Servico
from logger import logger
from schemas import *
from flask_cors import CORS
import requests

info = Info(title="Cooperativa Service", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# definindo tags
home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
cliente_tag = Tag(name="Cliente", description="Adição, atualização, visualização e remoção de clientes")
servico_tag = Tag(name="Servico", description="Adição de um serviço solicitado por um cliente cadastrado na base")
cep_tag = Tag(name="Consulta CEP", description="Visualização dos dados referentes a um cep consultado")


@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi')


@app.post('/cliente', tags=[cliente_tag],
          responses={"200": ClienteViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_cliente(form: ClienteSchema):
    """Adiciona um novo Cliente à base de dados

    Retorna uma representação dos clientes e serviços associados.
    """
    print(form)
    cliente = Cliente(
        telefone=form.telefone,
        nome=form.nome,
        email=form.email,
        cep=form.cep,
        logradouro=form.logradouro,
        numero=form.numero,
        complemento=form.complemento,
        bairro=form.bairro,
        cidade=form.cidade,
        uf=form.uf
    )
    logger.info(f"Adicionando cliente: '{cliente.nome}'")
    try:
        # criando conexão com a base
        session = Session()
        # adicionando produto
        session.add(cliente)
        # efetivando o camando de adição de novo item na tabela
        session.commit()
        logger.info("Adicionado cliente: %s"% cliente)
        return apresenta_cliente(cliente), 200

    except IntegrityError as e:
        error_msg = "E-mail informado já cadastrado na base :/"
        logger.warning(f"Erro ao adicionar cliente '{cliente.nome}', {error_msg}")
        return {"mensagem": error_msg}, 409

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível salvar novo cliente :/"
        logger.warning(f"Erro ao adicionar cliente '{cliente.nome}', {error_msg}")
        return {"mensagem": error_msg}, 400


@app.put('/atualiza', tags=[cliente_tag],
        responses={"200": ClienteSchema, "400": ErrorSchema})
def upd_cliente(query: ClienteUpdSchema):
    """Atualiza os dados do Cliente a partir do telefone informado.

    """
    cliente_id = query.telefone
    
    #Verifica se foi informado o telefone
    if not cliente_id:
        error_msg = "Telefone não informado!"
        logger.warning("Erro: {error_msg}")
        return {"mensagem": error_msg}, 404
    else:
        logger.info(f"Atualizando dados do cliente com o telefone #{cliente_id}")

    # criando conexão com a base
    session = Session()
    # fazendo a busca
    reg_cliente = session.query(Cliente).filter(Cliente.telefone == cliente_id).first()

    if not reg_cliente:
        # se o telefone não foi encontrado
        error_msg = "Telefone não encontrado na base de dados"
        logger.warning(f"Erro ao buscar telefone '{cliente_id}', {error_msg}")
        return {"mensagem": error_msg}, 404
    else:
        logger.info("Telefone econtrado")
        # Atualiza o cadastro do cliente
        reg_cliente.nome = query.nome
        reg_cliente.email = query.email
        reg_cliente.cep = query.cep
        reg_cliente.logradouro = query.logradouro
        reg_cliente.numero = query.numero
        reg_cliente.complemento = query.complemento
        reg_cliente.bairro = query.bairro
        reg_cliente.cidade = query.cidade
        reg_cliente.uf = query.uf

        session.commit()

        return {"mensagem": "Cliente atualizado com sucesso!"}, 200


@app.delete('/cliente', tags=[cliente_tag],
            responses={"200": ClienteDelSchema, "404": ErrorSchema})
def del_cliente(query: ClienteBuscaPorTelefoneSchema):
    """Deleta um Cliente a partir do telefone informado

    Retorna uma mensagem de confirmação da remoção.
    """
    cliente_tel = query.id
    logger.info(f"Deletando o cliente com telefone #{cliente_tel}")
    # criando conexão com a base
    session = Session()
    # fazendo a remoção
    count = session.query(Cliente).filter(Cliente.telefone == cliente_tel).delete()
    session.commit()

    if count:
        # retorna a representação da mensagem de confirmação
        logger.info(f"Cliente com o telefone #{cliente_tel} deletado com sucesso!")
        return {"mensagem": "Cliente removido", "id": cliente_tel}
    else:
        # se o cliente não foi encontrado
        error_msg = "Telefone não encontrado na base :/"
        logger.warning(f"Erro ao deletar o cliente com o telefone #'{cliente_tel}', {error_msg}")
        return {"mensagem": error_msg}, 404


@app.get('/clientes', tags=[cliente_tag],
         responses={"200": ListagemClientesSchema, "404": ErrorSchema})
def get_clientes():
    """Faz a busca por todos os Clientes cadastrados

    Retorna uma representação da listagem de clientes.
    """
    logger.info(f"Coletando clientes")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    clientes = session.query(Cliente).all()

    if not clientes:
        # se não há clientes cadastrados
        return {"Clientes": []}, 200
    else:
        logger.info(f"%d clientes econtrados" % len(clientes))
        # retorna a representação do cliente
        return apresenta_clientes(clientes), 200


@app.get('/cliente', tags=[cliente_tag],
         responses={"200": ClienteViewSchema, "404": ErrorSchema})
def get_cliente(query: ClienteBuscaPorTelefoneSchema):
    """Faz a busca por um Cliente a partir do telefone do cliente

    Retorna uma representação do cliente e serviços associados.
    """
    cliente_id = query.id
    logger.info(f"Coletando dados sobre o telefone #{cliente_id}")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    telefone = session.query(Cliente).filter(Cliente.telefone == cliente_id).first()

    if not telefone:
        # se o telefone não foi encontrado
        error_msg = "Telefone não encontrado na base :/"
        logger.warning(f"Erro ao buscar telefone '{cliente_id}', {error_msg}")
        return {"mensagem": error_msg}, 404
    else:
        logger.info("Telefone econtrado: %s" % telefone)
        # retorna a representação de produto
        return apresenta_cliente(telefone), 200


@app.get('/busca_cliente', tags=[cliente_tag],
         responses={"200": ListagemClientesSchema, "404": ErrorSchema})
def busca_cliente(query: ClienteBuscaPorNomeSchema):
    """Faz a busca por cliente que contenha o termo informado

    Retorna uma representação dos clientes e serviços associados.
    """
    termo = unquote(query.termo)
    logger.info(f"Fazendo a busca por nome com o termo: {termo}")
    # criando conexão com a base
    session = Session()
    # fazendo a consulta
    clientes = session.query(Cliente).filter(Cliente.nome.ilike(f"%{termo}%")).all()
    
    if not clientes:
        # se não há clientes cadastrados com o termo pesquisado
        error_msg = f"Cliente com o termo >> {termo} << não encontrado"
        logger.warning(f"Erro ao buscar cliente com o termo '{termo}', {error_msg}")
        return {"mensagem": error_msg}, 404
    else:
        logger.info(f"%d clientes econtrados" % len(clientes))
        # retorna a representação de cliente
        return apresenta_clientes(clientes), 200


@app.post('/servico', tags=[servico_tag],
          responses={"200": ServicoSchema, "404": ErrorSchema})
def add_servico(form: ServicoSchema):
    """Adiciona um novo serviço solicitado por um cliente cadastrado na base identificado pelo id

    Retorna uma representação do cliente e serviços associados.
    """
    cliente_id  = form.cliente_tel
    logger.info(f"Adicionando serviço solicitado pelo cliente #{cliente_id}")
    # criando conexão com a base
    session = Session()
    # fazendo a busca pelo cliente
    cliente = session.query(Cliente).filter(Cliente.telefone == cliente_id).first()

    if not cliente:
        # se o cliente não for encontrado
        error_msg = "Cliente não encontrado na base :/"
        logger.warning(f"Erro ao adicionar serviço solicitado pelo cliente '{cliente_id}', {error_msg}")
        return {"mensagem": error_msg}, 404

    # criando o serviço
    tipo_servico = form.tipo_servico
    descricao = form.descricao
    servico = Servico(tipo_servico, descricao)

    # adicionando o serviço ao cliente
    cliente.adiciona_servico(servico)
    session.commit()

    logger.info(f"Serviço adicionado ao cliente #{cliente_id}")

    # retorna a representação do cliente
    return apresenta_cliente(cliente), 200


@app.delete('/servico', tags=[servico_tag],
            responses={"200": ServicoDelSchema, "404": ErrorSchema})
def del_servico(query: ServicoBuscaPorTelefoneSchema):
    """Deleta um Serviço a partir do telefone informado

    Retorna uma mensagem de confirmação da remoção.
    """
    cliente_tel = query.id
    logger.info(f"Deletando o serviço do cliente com telefone #{cliente_tel}")
    # criando conexão com a base
    session = Session()
    # fazendo a remoção
    count = session.query(Servico).filter(Servico.cliente == cliente_tel).delete()
    session.commit()

    if count:
        # retorna a representação da mensagem de confirmação
        logger.info(f"Serviço do cliente com o telefone #{cliente_tel} deletado com sucesso!")
        return {"mensagem": "Serviço removido", "cliente": cliente_tel}
    else:
        # se o serviço não foi encontrado
        error_msg = "Serviço não encontrado na base"
        logger.warning(f"Erro ao deletar o serviço do cliente com o telefone #'{cliente_tel}', {error_msg}")
        return {"mensagem": error_msg}, 404


@app.get('/servicos', tags=[servico_tag],
         responses={"200": ListagemServicosSchema, "404": ErrorSchema})
def get_servicos():
    """Faz a busca por todos os Serviços cadastrados

    Retorna uma representação da listagem de serviços.
    """
    logger.info(f"Coletando serviços")

    # criando conexão com a base
    session = Session()
    # fazendo a busca
    servicos = session.query(Servico).all()

    if not servicos:
        # se não há serviços cadastrados
        return {"Serviços": []}, 200
    else:
        logger.info(f"%d serviços econtrados" % len(servicos))
        # retorna a representação do serviço
        return apresenta_servicos(servicos), 200


@app.get('/cep', tags=[cep_tag],
         responses={"200": CepViewSchema, "404": ErrorSchema})
def get_dados_cep(query: CepBuscaDadosSchema):
    """Faz a busca pelos dados do CEP a partir de um CEP informado.

    Retorna uma representação dos dados associados.
    """
    cep_id = query.cep
    cep_api_url = "https://viacep.com.br/ws/"
    logger.info(f"Coletando dados sobre o cep #{cep_id}")
    
    try:
        #Faz a requisição à API externa
        response = requests.get(f"{cep_api_url}{cep_id}/json/")
        dados_ret = response.json()
    
        if "erro" in dados_ret:
            # se o cep não foi encontrado
            error_msg = "CEP informado não encontrado :/"
            logger.warning(f"Erro ao buscar cep '{cep_id}', {error_msg}")
            return {"mensagem": error_msg}, 404

        logger.info("CEP econtrado: %s" % cep_id)
        # retorna a representação dos dados do CEP
        dados_cep = {
            "cep": dados_ret["cep"],
            "logradouro": dados_ret["logradouro"],
            "complemento": dados_ret["complemento"],
            "bairro": dados_ret["bairro"],
            "localidade": dados_ret["localidade"],
            "uf": dados_ret["uf"],
            "ddd": dados_ret["ddd"],
        }
        
        return jsonify(dados_cep), 200
    
    except Exception as e:
        error_msg = "Erro ao consultar o CEP!"
        logger.warning(f"Erro ao consultar o CEP #'{cep_id}', {error_msg}")
        return {"mensagem": error_msg}, 500
        #return {"mensagem": e.args}, 500