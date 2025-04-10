-- Criação da tabela tbUser
CREATE TABLE IF NOT EXISTS tbUser (
    Id INT AUTO_INCREMENT PRIMARY KEY,
    Nome VARCHAR(255),
    Senha VARCHAR(255),
    Saldo DECIMAL(10,2)
);

CREATE TABLE IF NOT EXISTS tbTipoTransacao (
    Id INT AUTO_INCREMENT PRIMARY KEY,
    Tipo VARCHAR(50) NOT NULL
);

-- Criação da tabela tbTransacoes com campo Tipo
CREATE TABLE IF NOT EXISTS tbTransacoes (
    Id INT AUTO_INCREMENT PRIMARY KEY,
    RemetenteId INT NOT NULL,
    DestinatarioId INT, -- Pode ser NULL pra Depósito/Saque
    Quantia DECIMAL(10,2) NOT NULL,
    DataHora TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    Tipo VARCHAR(50) NOT NULL, -- Novo campo
    FOREIGN KEY (RemetenteId) REFERENCES tbUser(Id),
    FOREIGN KEY (DestinatarioId) REFERENCES tbUser(Id),
);

-- Inserindo 15 usuários na tabela tbUser (saldo inicial 0.00)
INSERT INTO tbUser (Nome, Senha, Saldo) VALUES 
    ('admin', 'admin', 0.00),
    ('João Silva', 'senha123', 0.00),
    ('Maria Santos', 'maria2024', 0.00),
    ('Carlos Oliveira', 'carOlive', 0.00),
    ('Ana Souza', 'ana_s123', 0.00),
    ('Pedro Lima', 'pedrolima', 0.00),
    ('Fernanda Costa', 'fernanda99', 0.00),
    ('Lucas Rocha', 'lucas_r', 0.00),
    ('Juliana Mendes', 'julim', 0.00),
    ('Rafael Duarte', 'rafaduarte', 0.00),
    ('Beatriz Almeida', 'beaalm', 0.00),
    ('Thiago Ferreira', 'thiago789', 0.00),
    ('Camila Dias', 'camila123', 0.00),
    ('Gabriel Barbosa', 'gab123', 0.00),
    ('Larissa Nunes', 'lari456', 0.00);

-- Simulando depósitos iniciais pra garantir saldo suficiente
UPDATE tbUser SET Saldo = 2000.00 WHERE Id = 2;     -- João Silva
UPDATE tbUser SET Saldo = 2500.00 WHERE Id = 3;     -- Maria Santos
UPDATE tbUser SET Saldo = 1000.00 WHERE Id = 4;     -- Carlos Oliveira
UPDATE tbUser SET Saldo = 2500.00 WHERE Id = 5;     -- Ana Souza
UPDATE tbUser SET Saldo = 1800.00 WHERE Id = 6;     -- Pedro Lima
UPDATE tbUser SET Saldo = 1200.00 WHERE Id = 7;     -- Fernanda Costa
UPDATE tbUser SET Saldo = 3000.00 WHERE Id = 8;     -- Lucas Rocha
UPDATE tbUser SET Saldo = 3000.00 WHERE Id = 9;     -- Juliana Mendes
UPDATE tbUser SET Saldo = 3200.00 WHERE Id = 10;    -- Rafael Duarte
UPDATE tbUser SET Saldo = 2000.00 WHERE Id = 11;     -- Beatriz Almeida
UPDATE tbUser SET Saldo = 1400.00 WHERE Id = 12;    -- Thiago Ferreira
UPDATE tbUser SET Saldo = 1700.00 WHERE Id = 13;    -- Camila Dias
UPDATE tbUser SET Saldo = 4100.00 WHERE Id = 14;    -- Gabriel Barbosa
UPDATE tbUser SET Saldo = 2800.00 WHERE Id = 15;    -- Larissa Nunes

-- Criando procedure ajustada para transferir dinheiro com Tipo
DROP PROCEDURE IF EXISTS TransferirDinheiro;

DELIMITER $$
CREATE PROCEDURE TransferirDinheiro(
    IN p_RemetenteId INT,
    IN p_DestinatarioId INT, -- Pode ser NULL pra Depósito/Saque
    IN p_Quantia DECIMAL(10,2),
    IN p_DataHora TIMESTAMP,
    IN p_Tipo VARCHAR(50)
)
BEGIN
    DECLARE v_SaldoRemetente DECIMAL(10,2);
    DECLARE v_SaldoDestinatario DECIMAL(10,2);

    START TRANSACTION;

    -- Verifica o remetente
    SELECT Saldo INTO v_SaldoRemetente 
      FROM tbUser 
     WHERE Id = p_RemetenteId 
     FOR UPDATE;

    IF v_SaldoRemetente IS NULL THEN
        ROLLBACK;
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Remetente não encontrado.';
    END IF;

    -- Verifica o destinatário (se não for NULL)
    IF p_DestinatarioId IS NOT NULL THEN
        SELECT Saldo INTO v_SaldoDestinatario 
          FROM tbUser 
         WHERE Id = p_DestinatarioId 
         FOR UPDATE;

        IF v_SaldoDestinatario IS NULL THEN
            ROLLBACK;
            SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Destinatário não encontrado.';
        END IF;
    END IF;

    -- Verifica saldo suficiente pro remetente (exceto pra Depósito)
    IF p_Tipo != 'Depósito' AND v_SaldoRemetente < p_Quantia THEN
        ROLLBACK;
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Saldo insuficiente.';
    END IF;

    -- Atualiza saldo do remetente
    IF p_Tipo = 'Depósito' THEN
        UPDATE tbUser 
          SET Saldo = Saldo + p_Quantia 
         WHERE Id = p_RemetenteId;
    ELSE
        UPDATE tbUser 
          SET Saldo = Saldo - p_Quantia 
         WHERE Id = p_RemetenteId;
    END IF;

    -- Atualiza saldo do destinatário (se houver)
    IF p_DestinatarioId IS NOT NULL THEN
        UPDATE tbUser 
          SET Saldo = Saldo + p_Quantia 
         WHERE Id = p_DestinatarioId;
    END IF;

    -- Registra a transação
    INSERT INTO tbTransacoes (RemetenteId, DestinatarioId, Quantia, DataHora, Tipo) 
     VALUES (p_RemetenteId, p_DestinatarioId, p_Quantia, p_DataHora, p_Tipo);

    COMMIT;
END $$
DELIMITER ;

-- Simulando 100 transações iniciais com tipos variados
CALL TransferirDinheiro(2, NULL, 500.00, '2024-01-05 10:30:00', 'Depósito');
CALL TransferirDinheiro(2, 3, 100.50, '2024-01-07 14:15:00', 'PIX');
CALL TransferirDinheiro(3, NULL, 200.00, '2024-01-10 09:45:00', 'Saque');
CALL TransferirDinheiro(4, 5, 300.75, '2024-01-12 16:20:00', 'Transferência');
CALL TransferirDinheiro(5, NULL, 150.00, '2024-01-15 11:00:00', 'Depósito');
CALL TransferirDinheiro(6, 7, 400.25, '2024-01-18 13:30:00', 'PIX');
CALL TransferirDinheiro(7, NULL, 250.60, '2024-02-01 08:00:00', 'Saque');
CALL TransferirDinheiro(8, 9, 500.00, '2024-02-03 17:10:00', 'Transferência');
CALL TransferirDinheiro(9, NULL, 300.30, '2024-02-05 12:45:00', 'Depósito');
CALL TransferirDinheiro(10, 11, 600.00, '2024-02-07 15:00:00', 'PIX');
CALL TransferirDinheiro(11, NULL, 200.50, '2024-02-10 09:15:00', 'Saque');
CALL TransferirDinheiro(12, 13, 700.75, '2024-02-12 14:30:00', 'Transferência');
CALL TransferirDinheiro(13, NULL, 400.00, '2024-02-15 10:00:00', 'Depósito');
CALL TransferirDinheiro(14, 15, 800.25, '2024-02-18 16:45:00', 'PIX');
CALL TransferirDinheiro(15, NULL, 150.60, '2024-03-01 11:30:00', 'Saque');
CALL TransferirDinheiro(2, 4, 300.00, '2024-03-03 13:15:00', 'Transferência');
CALL TransferirDinheiro(4, NULL, 500.50, '2024-03-05 09:00:00', 'Depósito');
CALL TransferirDinheiro(6, 8, 200.75, '2024-03-07 15:20:00', 'PIX');
CALL TransferirDinheiro(8, NULL, 600.00, '2024-03-10 10:45:00', 'Saque');
CALL TransferirDinheiro(10, 12, 400.25, '2024-03-12 12:00:00', 'Transferência');
CALL TransferirDinheiro(12, NULL, 700.60, '2024-03-15 14:00:00', 'Depósito');
CALL TransferirDinheiro(14, 2, 300.00, '2024-03-18 16:30:00', 'PIX');
CALL TransferirDinheiro(2, NULL, 800.50, '2024-04-01 08:30:00', 'Saque');
CALL TransferirDinheiro(5, 7, 150.75, '2024-04-03 11:15:00', 'Transferência');
CALL TransferirDinheiro(7, NULL, 400.00, '2024-04-05 09:45:00', 'Depósito');
CALL TransferirDinheiro(9, 11, 600.25, '2024-04-07 13:00:00', 'PIX');
CALL TransferirDinheiro(11, NULL, 200.60, '2024-04-10 10:15:00', 'Saque');
CALL TransferirDinheiro(13, 15, 500.00, '2024-04-12 15:30:00', 'Transferência');
CALL TransferirDinheiro(15, NULL, 300.50, '2024-04-15 12:00:00', 'Depósito');
CALL TransferirDinheiro(3, 6, 700.75, '2024-04-18 14:45:00', 'PIX');
CALL TransferirDinheiro(6, NULL, 400.00, '2024-05-01 09:00:00', 'Saque');
CALL TransferirDinheiro(9, 12, 800.25, '2024-05-03 11:30:00', 'Transferência');
CALL TransferirDinheiro(12, NULL, 150.60, '2024-05-05 10:15:00', 'Depósito');
CALL TransferirDinheiro(15, 2, 300.00, '2024-05-07 13:45:00', 'PIX');
CALL TransferirDinheiro(2, NULL, 500.50, '2024-05-10 08:30:00', 'Saque');
CALL TransferirDinheiro(5, 8, 200.75, '2024-05-12 16:00:00', 'Transferência');
CALL TransferirDinheiro(8, NULL, 600.00, '2024-06-01 09:45:00', 'Depósito');
CALL TransferirDinheiro(11, 14, 400.25, '2024-06-03 12:15:00', 'PIX');
CALL TransferirDinheiro(14, NULL, 700.60, '2024-06-05 11:00:00', 'Saque');
CALL TransferirDinheiro(3, 7, 300.00, '2024-06-07 14:30:00', 'Transferência');
CALL TransferirDinheiro(7, NULL, 800.50, '2024-06-10 10:00:00', 'Depósito');
CALL TransferirDinheiro(10, 13, 150.75, '2024-06-12 15:15:00', 'PIX');
CALL TransferirDinheiro(13, NULL, 400.00, '2024-07-01 08:00:00', 'Saque');
CALL TransferirDinheiro(2, 6, 600.25, '2024-07-03 13:45:00', 'Transferência');
CALL TransferirDinheiro(6, NULL, 200.60, '2024-07-05 09:30:00', 'Depósito');
CALL TransferirDinheiro(9, 12, 500.00, '2024-07-07 12:00:00', 'PIX');
CALL TransferirDinheiro(12, NULL, 300.50, '2024-07-10 10:45:00', 'Saque');
CALL TransferirDinheiro(15, 4, 700.75, '2024-07-12 14:15:00', 'Transferência');
CALL TransferirDinheiro(4, NULL, 400.00, '2024-08-01 11:00:00', 'Depósito');
CALL TransferirDinheiro(8, 11, 800.25, '2024-08-03 16:30:00', 'PIX');
CALL TransferirDinheiro(11, NULL, 150.60, '2024-08-05 09:15:00', 'Saque');
CALL TransferirDinheiro(14, 3, 300.00, '2024-08-07 13:00:00', 'Transferência');
CALL TransferirDinheiro(3, NULL, 500.50, '2024-08-10 10:30:00', 'Depósito');
CALL TransferirDinheiro(7, 10, 200.75, '2024-08-12 15:45:00', 'PIX');
CALL TransferirDinheiro(10, NULL, 600.00, '2024-09-01 08:45:00', 'Saque');
CALL TransferirDinheiro(13, 2, 400.25, '2024-09-03 11:30:00', 'Transferência');
CALL TransferirDinheiro(2, NULL, 700.60, '2024-09-05 09:00:00', 'Depósito');
CALL TransferirDinheiro(6, 9, 300.00, '2024-09-07 14:00:00', 'PIX');
CALL TransferirDinheiro(9, NULL, 800.50, '2024-09-10 10:15:00', 'Saque');
CALL TransferirDinheiro(12, 15, 150.75, '2024-09-12 12:45:00', 'Transferência');
CALL TransferirDinheiro(15, NULL, 400.00, '2024-10-01 09:30:00', 'Depósito');
CALL TransferirDinheiro(4, 8, 600.25, '2024-10-03 13:15:00', 'PIX');
CALL TransferirDinheiro(8, NULL, 200.60, '2024-10-05 10:00:00', 'Saque');
CALL TransferirDinheiro(11, 14, 500.00, '2024-10-07 15:30:00', 'Transferência');
CALL TransferirDinheiro(14, NULL, 300.50, '2024-10-10 11:45:00', 'Depósito');
CALL TransferirDinheiro(3, 7, 700.75, '2024-10-12 14:00:00', 'PIX');
CALL TransferirDinheiro(7, NULL, 400.00, '2024-11-01 08:15:00', 'Saque');
CALL TransferirDinheiro(10, 13, 800.25, '2024-11-03 12:30:00', 'Transferência');
CALL TransferirDinheiro(13, NULL, 150.60, '2024-11-05 09:45:00', 'Depósito');
CALL TransferirDinheiro(2, 6, 300.00, '2024-11-07 13:00:00', 'PIX');
CALL TransferirDinheiro(6, NULL, 500.50, '2024-11-10 10:30:00', 'Saque');
CALL TransferirDinheiro(9, 12, 200.75, '2024-11-12 15:15:00', 'Transferência');
CALL TransferirDinheiro(12, NULL, 600.00, '2024-12-01 08:00:00', 'Depósito');
CALL TransferirDinheiro(15, 4, 400.25, '2024-12-03 11:45:00', 'PIX');
CALL TransferirDinheiro(4, NULL, 700.60, '2024-12-05 09:15:00', 'Saque');
CALL TransferirDinheiro(8, 11, 300.00, '2024-12-07 14:30:00', 'Transferência');
CALL TransferirDinheiro(11, NULL, 800.50, '2024-12-10 10:00:00', 'Depósito');
CALL TransferirDinheiro(14, 3, 150.75, '2024-12-12 12:15:00', 'PIX');
CALL TransferirDinheiro(3, NULL, 400.00, '2025-01-01 09:30:00', 'Saque');
CALL TransferirDinheiro(7, 10, 600.25, '2025-01-03 13:45:00', 'Transferência');
CALL TransferirDinheiro(10, NULL, 200.60, '2025-01-05 10:15:00', 'Depósito');
CALL TransferirDinheiro(13, 2, 500.00, '2025-01-07 15:00:00', 'PIX');
CALL TransferirDinheiro(2, NULL, 300.50, '2025-01-10 08:45:00', 'Saque');
CALL TransferirDinheiro(6, 9, 700.75, '2025-01-12 11:30:00', 'Transferência');
CALL TransferirDinheiro(9, NULL, 400.00, '2025-02-01 09:00:00', 'Depósito');
CALL TransferirDinheiro(12, 15, 800.25, '2025-02-03 14:15:00', 'PIX');
CALL TransferirDinheiro(15, NULL, 150.60, '2025-02-05 10:30:00', 'Saque');
CALL TransferirDinheiro(4, 8, 300.00, '2025-02-07 12:00:00', 'Transferência');
CALL TransferirDinheiro(8, NULL, 500.50, '2025-02-10 09:45:00', 'Depósito');
CALL TransferirDinheiro(11, 14, 200.75, '2025-02-12 13:30:00', 'PIX');
CALL TransferirDinheiro(14, NULL, 600.00, '2025-03-01 08:15:00', 'Saque');
CALL TransferirDinheiro(3, 7, 400.25, '2025-03-03 11:00:00', 'Transferência');
CALL TransferirDinheiro(7, NULL, 700.60, '2025-03-05 09:30:00', 'Depósito');
CALL TransferirDinheiro(10, 13, 300.00, '2025-03-07 14:45:00', 'PIX');
CALL TransferirDinheiro(13, NULL, 800.50, '2025-03-10 10:00:00', 'Saque');
CALL TransferirDinheiro(2, 6, 150.75, '2025-03-12 12:15:00', 'Transferência');
CALL TransferirDinheiro(6, NULL, 400.00, '2025-04-01 08:30:00', 'Depósito');
CALL TransferirDinheiro(9, 12, 600.25, '2025-04-03 13:00:00', 'PIX');
CALL TransferirDinheiro(12, NULL, 200.60, '2025-04-05 09:15:00', 'Saque');
CALL TransferirDinheiro(15, 4, 500.00, '2025-04-07 14:30:00', 'Transferência');