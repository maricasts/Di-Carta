-- Criação do Banco de Dados (executar como superuser se necessário)
-- CREATE DATABASE dicarta_livraria;

-- Tabela: TECNICO
CREATE TABLE IF NOT EXISTS tecnico (
    id_tecnico SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    cpf CHAR(11) UNIQUE NOT NULL,
    status VARCHAR(20) CHECK (status IN ('Contratado', 'Demitido')) NOT NULL,
    valor_hora NUMERIC(10, 2) NOT NULL,
    carga_horaria INTEGER NOT NULL
);

-- Tabela: LIVRO
CREATE TABLE IF NOT EXISTS livro (
    id_livro SERIAL PRIMARY KEY,
    titulo VARCHAR(150) NOT NULL,
    autor VARCHAR(100) NOT NULL,
    editora VARCHAR(100),
    ano INTEGER CHECK (ano >= 1000 AND ano <= 2100),
    genero VARCHAR(50),
    preco NUMERIC(10, 2) NOT NULL,
    estoque INTEGER DEFAULT 0 CHECK (estoque >= 0)
);

-- Tabela: CLIENTE
CREATE TABLE IF NOT EXISTS cliente (
    id_cliente SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    cpf CHAR(11) UNIQUE NOT NULL,
    telefone VARCHAR(15),
    email VARCHAR(100),
    cep CHAR(8),
    endereco VARCHAR(150)
);

-- Tabela: VENDA
CREATE TABLE IF NOT EXISTS venda (
    id_venda SERIAL PRIMARY KEY,
    data DATE NOT NULL,
    total NUMERIC(10, 2) NOT NULL,
    id_tecnico INTEGER NOT NULL,
    id_cliente INTEGER NOT NULL,
    CONSTRAINT fk_venda_tecnico FOREIGN KEY (id_tecnico) REFERENCES tecnico (id_tecnico),
    CONSTRAINT fk_venda_cliente FOREIGN KEY (id_cliente) REFERENCES cliente (id_cliente)
);

-- Tabela: ITEMVENDA
CREATE TABLE IF NOT EXISTS itemvenda (
    id_item SERIAL PRIMARY KEY,
    id_venda INTEGER NOT NULL,
    id_livro INTEGER NOT NULL,
    quantidade INTEGER NOT NULL CHECK (quantidade > 0),
    preco_unitario NUMERIC(10, 2) NOT NULL,
    CONSTRAINT fk_item_venda FOREIGN KEY (id_venda) REFERENCES venda (id_venda) ON DELETE CASCADE,
    CONSTRAINT fk_item_livro FOREIGN KEY (id_livro) REFERENCES livro (id_livro)
);
