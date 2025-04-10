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
        Tipo VARCHAR(50) NOT NULL,
        FOREIGN KEY (RemetenteId) REFERENCES tbUser(Id),
        FOREIGN KEY (DestinatarioId) REFERENCES tbUser(Id)
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