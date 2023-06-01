SELECT u.email FROM Usuario as u, Solicitacao as s
WHERE u.codigo = s.Usuario_codigo and s.codigo = 5; 

SELECT * FROM USUARIO;

SELECT * FROM solicitacao;

INSERT INTO Usuario(cpf, nome, dt_nasc, peso, tipo_sanguineo, cep, cidade, email, senha, telefone, opcao_doacao, estado_sessao) 
VALUES ('704', 'Marlos', '2004-04-19', '50kg', 'A+', '5070006', 'Caraúbas', 'dorisvanjacome@gmail.com', '123','99900323', 'Sim', 0);


INSERT INTO Solicitacao(data, urgencia, local_internacao, situacao, Usuario_codigo) 
VALUES('2023-06-01', 1, 'hospital x', 'Pendente', 2);


