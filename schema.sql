-- Arquivo: schema.sql

-- Recrie a estrutura das suas tabelas aqui
CREATE TABLE TblServico (
    Empresa NVARCHAR(100),
    DataViagem DATETIME,
    NroServico NVARCHAR(100),
    HoraViagem NVARCHAR(10),
    ASK NUMERIC(10, 4),
    IdLinha INT,
    LinhaClasse NVARCHAR(100),
    Status NVARCHAR(50),
    KmRodado NUMERIC(10, 2),
    IdServico INT PRIMARY KEY
);

CREATE TABLE TblLinha (
    NomeLinha NVARCHAR(100),
    NroLinha NVARCHAR(50),
    SubGrupo NVARCHAR(50),
    LinhaClasse NVARCHAR(100),
    IdLinha INT
);

CREATE TABLE TblBilhete (
    IdServico INT,
    IdTipoPassagem INT,
    IdStatus INT,
    Distancia NUMERIC(10, 2),
    Total NUMERIC(10, 2)
);

-- (Opcional, mas recomendado) Insira algumas linhas de dados para teste
INSERT INTO TblLinha (NomeLinha, NroLinha, SubGrupo, IdLinha, LinhaClasse) VALUES ('LINHA TESTE', '1234', 'GRUPO A', 1, 'CLASSE_X');
INSERT INTO TblServico (Empresa, DataViagem, NroServico, ASK, IdLinha, LinhaClasse, Status, IdServico) VALUES ('VIACAO MOTTA', '2025-09-18', '5000', 100.0, 1, 'CLASSE_X', 'ABERTO', 100);
INSERT INTO TblBilhete (IdServico, IdTipoPassagem, IdStatus, Distancia, Total) VALUES (100, 1, 1, 50.0, 75.50);

