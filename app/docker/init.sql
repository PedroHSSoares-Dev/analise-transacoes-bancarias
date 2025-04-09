-- Criação da tabela tbUser
CREATE TABLE IF NOT EXISTS tbUser (
    Id INT AUTO_INCREMENT PRIMARY KEY,
    Nome VARCHAR(255),
    Senha VARCHAR(255),
    Saldo DECIMAL(10,2)
);

-- Criação da tabela tbTransacoes
CREATE TABLE IF NOT EXISTS tbTransacoes (
    Id INT AUTO_INCREMENT PRIMARY KEY,
    RemetenteId INT NOT NULL,
    DestinatarioId INT NOT NULL,
    Quantia DECIMAL(10,2) NOT NULL,
    DataHora TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (RemetenteId) REFERENCES tbUser(Id),
    FOREIGN KEY (DestinatarioId) REFERENCES tbUser(Id)
);

-- Inserindo alguns registros na tabela tbUser
INSERT INTO tbUser (Nome, Senha, Saldo) VALUES 
    ('admin', 'admin', 0.0),
    ('João Silva', 'senha123', 100.50),
    ('Maria Santos', 'maria2024', 250.75),
    ('Carlos Oliveira', 'carOlive', 500.00),
    ('Ana Souza', 'ana_s123', 750.30),
    ('Pedro Lima', 'pedrolima', 1200.00),
    ('Fernanda Costa', 'fernanda99', 430.25),
    ('Lucas Rocha', 'lucas_r', 890.60),
    ('Juliana Mendes', 'julim', 300.00),
    ('Rafael Duarte', 'rafaduarte', 2000.90),
    ('Beatriz Almeida', 'beaalm', 50.00);

-- Criando procedure para transferir dinheiro entre usuários
-- Remove a procedure, se ela existir
DROP PROCEDURE IF EXISTS TransferirDinheiro;

DELIMITER $$
CREATE PROCEDURE TransferirDinheiro(
    IN p_RemetenteId INT,
    IN p_DestinatarioId INT,
    IN p_Quantia DECIMAL(10,2)
)
BEGIN
    DECLARE v_SaldoRemetente DECIMAL(10,2);
    DECLARE v_SaldoDestinatario DECIMAL(10,2);

    START TRANSACTION;

    -- Bloqueia e obtém o saldo do remetente para atualização
    SELECT Saldo INTO v_SaldoRemetente 
      FROM tbUser 
     WHERE Id = p_RemetenteId 
     FOR UPDATE;

    IF v_SaldoRemetente IS NULL THEN
        ROLLBACK;
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Remetente não encontrado.';
    END IF;

    -- Bloqueia e obtém o saldo do destinatário para atualização
    SELECT Saldo INTO v_SaldoDestinatario 
      FROM tbUser 
     WHERE Id = p_DestinatarioId 
     FOR UPDATE;

    IF v_SaldoDestinatario IS NULL THEN
        ROLLBACK;
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Destinatário não encontrado.';
    END IF;

    -- Verifica se o remetente possui saldo suficiente
    IF v_SaldoRemetente < p_Quantia THEN
        ROLLBACK;
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Saldo insuficiente.';
    END IF;

    -- Atualiza os saldos dos usuários
    UPDATE tbUser 
      SET Saldo = Saldo - p_Quantia 
     WHERE Id = p_RemetenteId;

    UPDATE tbUser 
      SET Saldo = Saldo + p_Quantia 
     WHERE Id = p_DestinatarioId;

    -- Registra a transação na tabela de transações
    INSERT INTO tbTransacoes (RemetenteId, DestinatarioId, Quantia) 
     VALUES (p_RemetenteId, p_DestinatarioId, p_Quantia);

    COMMIT;
END $$
DELIMITER ;