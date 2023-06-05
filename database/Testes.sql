SELECT u.email FROM Usuario as u, Solicitacao as s
WHERE u.codigo = s.Usuario_codigo and s.codigo = 1; 

SELECT u.email FROM Usuario as u, Solicitacao as s 
WHERE s.codigo = %s AND u.codigo = s.Usuario_codigo;

SELECT * FROM USUARIO;

SELECT * FROM solicitacao;

INSERT INTO Usuario(cpf, nome, dt_nasc, peso, tipo_sanguineo, cep, cidade, email, senha, telefone, opcao_doacao, estado_sessao) 
VALUES ('605', 'João Pedro', '2004-04-19', '50kg', 'A+', '5070006', 'Caraúbas', 'joao.mota@escolar.ifrn.edu.br', '123','99900323', 'Sim', 0);


INSERT INTO Solicitacao(data, urgencia, local_internacao, situacao, Usuario_codigo) 
VALUES('2023-06-01', 'Baixa', 'hospital x', 'Pendente', 1);


SELECT * FROM Doacao;


INSERT INTO Doacao(data, local_destino, solicitacao_codigo, usuario_codigo) 
VALUES ('2023-02-02', 'Hopistal x', 1, 1);

SELECT DISTINCT *
FROM Usuario as u 
WHERE u.codigo LIKE 1 OR u.cpf LIKE 1 OR u.nome LIKE 1 OR u.dt_nasc LIKE 1 OR u.peso LIKE 1 OR u.tipo_sanguineo LIKE 1 OR u.cep LIKE 1 OR u.cidade LIKE 1 OR u.email LIKE 1 OR u.senha LIKE 1 OR u.telefone LIKE 1 OR u.opcao_doacao LIKE 1 OR u.estado_doacao LIKE 1 OR u.nivel_usuario LIKE 1;

