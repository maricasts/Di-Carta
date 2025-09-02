from app import db
from datetime import datetime
from sqlalchemy import CheckConstraint

class Cliente(db.Model):
    __tablename__ = 'cliente'
    
    id = db.Column('id_cliente', db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    cpf = db.Column(db.String(11), unique=True, nullable=False)
    telefone = db.Column(db.String(15))
    email = db.Column(db.String(100))
    cep = db.Column(db.String(8))
    endereco = db.Column(db.String(150))

    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'cpf': self.cpf,
            'telefone': self.telefone,
            'email': self.email,
            'cep': self.cep,
            'endereco': self.endereco
        }

class Tecnico(db.Model):
    __tablename__ = 'tecnico'
    
    id = db.Column('id_tecnico', db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    cpf = db.Column(db.String(11), unique=True, nullable=False)
    status = db.Column(db.String(20), nullable=False)
    valor_hora = db.Column(db.Numeric(10, 2), nullable=False)
    carga_horaria = db.Column(db.Integer, nullable=False)

    __table_args__ = (
        CheckConstraint("status IN ('Contratado', 'Demitido')", name='check_status'),
    )

    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'cpf': self.cpf,
            'status': self.status,
            'valorHora': float(self.valor_hora),
            'cargaHoraria': self.carga_horaria
        }

class Livro(db.Model):
    __tablename__ = 'livro'
    
    id = db.Column('id_livro', db.Integer, primary_key=True)
    titulo = db.Column(db.String(150), nullable=False)
    autor = db.Column(db.String(100), nullable=False)
    editora = db.Column(db.String(100))
    ano = db.Column(db.Integer)
    genero = db.Column(db.String(50))
    preco = db.Column(db.Numeric(10, 2), nullable=False)
    estoque = db.Column(db.Integer, default=0)

    __table_args__ = (
        CheckConstraint('ano >= 1000 AND ano <= 2100', name='check_ano'),
        CheckConstraint('estoque >= 0', name='check_estoque'),
    )

    def to_dict(self):
        return {
            'id': self.id,
            'titulo': self.titulo,
            'autor': self.autor,
            'editora': self.editora,
            'ano': self.ano,
            'genero': self.genero,
            'preco': float(self.preco),
            'estoque': self.estoque
        }

class OrdemDeServico(db.Model):
    __tablename__ = 'ordem_de_servico'
    
    id = db.Column('id_ordem', db.Integer, primary_key=True)
    descricao = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default='ABERTA')
    data_abertura = db.Column(db.Date, default=datetime.utcnow)
    data_fechamento = db.Column(db.Date)

    def to_dict(self):
        return {
            'id': self.id,
            'descricao': self.descricao,
            'status': self.status,
            'dataAbertura': self.data_abertura.isoformat() if self.data_abertura else None,
            'dataFechamento': self.data_fechamento.isoformat() if self.data_fechamento else None
        }