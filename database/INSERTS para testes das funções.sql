INSERT INTO Doenca (nome)
VALUES ("HIV"),
("Hepatite pós 10 anos de idade"),
("Malária"),
("Chagas"),
("Enxerto de duramater"),
("Câncer gerais ou Leucemia"),
("Problemas de pulmão, coração, rins ou fígado"),
("Diabético com complicações vasculares ou em uso de insulina"),
("Tuberculose extra-pulmonar"),
("Elefantíase"),
("Hanseníase"),
("Calazar (leishmaniose visceral)"),
("Leishmaniose tegumentar ou cutânea"),
("Esquistossomose hepatoesplênica"),
("Doenças que gerem inimputabilidade jurídica"),
("Brucelose"),
("Transplante de órgãos ou de medula"),
("Mal de Parkinson");

# Usuários

# Administrador
INSERT INTO Usuario(cpf, nome, dt_nasc, peso, tipo_sanguineo, cep, cidade, email, senha, telefone, opcao_doacao, estado_sessao, nivel_usuario) 
VALUES ('70294976489', 'Brendo Emanuel', '2005-10-20', '73', 'A+', '5070006', 'Itaú', 'Brendoemanuel@gmail.com', '123','979026478', 'Sim', 0, 1);


# Usuários comuns

INSERT INTO Usuario(cpf, nome, dt_nasc, peso, tipo_sanguineo, cep, cidade, email, senha, telefone, opcao_doacao, estado_sessao, nivel_usuario) 
VALUES 
('70293246513', 'Dorisvan Jácome', '2004-09-29', '50', 'O-', '5070006', 'Caraúbas', 'dorisvanjacome@gmail.com', '123','999026254', 'Sim', 0, 0),
('70294976512', 'Ívisson Marlos', '2005-03-10', '70', 'O-', '5070006', 'Caraúbas', 'ivissonmarlos@gmail.com', '123','979026456', 'Sim', 0, 0),
 ('70293230253', 'João Pedro', '2004-02-19', '70', 'A+', '5070006', 'Sítio Felipe Guerra', 'joao.mota@escolar.ifrn.edu.br', '123','99900323', 'Sim', 0, 1);

SELECT * FROM Usuario;

INSERT INTO Solicitacao(data, urgencia, local_internacao, situacao, Usuario_codigo) 
VALUES
('2023-06-01', 'Baixa', 'hospital x', 'Pendente', 2),
('2023-06-02', 'Alta', 'hospital x', 'Pendente', 3),
('2023-06-02', 'Média', 'hospital x', 'Pendente', 4);

SELECT * FROM Solicitacao
