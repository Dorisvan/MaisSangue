-- Inserts

-- Solicitantes:
INSERT INTO Solicitante (cpf, nome, cep, uf, cidade, telefone, email, bairro, rua)
VALUES ("713.867.104-07", "Juan Carlos Linhares de Almeida", "59780-000", "RN", "Caraúbas", "97023206", "juan.c@escolar.ifrn.edu.br", "Alto Boa Vista", "Rua Raimundo Nonato Bezerra"), 
	   ("715.874.320-02", "Paulo Victor de Carvalho Silva", "59700-000", "RN", "Apodi", "91816749", "silva.carvalho@escolar.ifrn.edu.br", "São Sebastião", "Rua Governador José Varela"),
       ("707.760.744-50", "Débora Maria Silva e Sena", "59780-000", "RN", "Caraúbas", "998998158", "maria.debora@escolar.ifrn.edu.br", "Leandro Bezerra", "Avenida Beijamin Constante"),
       ("707.125.024-32", "João Pedro Ferreira Mota", "59795-000", "RN", "Felipe Guerra", "996234295", "joao.mota@escolar.ifrn.edu.br", "Cidade Alta", "Rua Alcides Gurgel do Amaral"),
       ("153.174.234-30", "Brendo Emanuel de Morais Andrade", "59855-000", "RN", "Itaú", "99955-9752", "brendo.andrade@escolar.ifrn.edu.br", "Pinico Amassado", "Rua Monteiro Cavalcante");
     
     
-- Doadores:
INSERT INTO Doador (cpf, nome, idade, peso, tipo_sanguineo, estado, cidade, telefone, email)
VALUES ("706.504.004-61", "Dorisvan de Medeiros Jácome Filho", 18, "67 Kg", "O-", "RN", "Caraúbas", "999025206", "medeiros.jacome@escolar.ifrn.edu.br"),
       ("450.652.841-56", "Negreiros Silva Cunha", 18, "50 Kg", "O+", "RN", "Rodolfo Fernandes", "996857412", "negreiros.silva@escolar.ifrn.edu.br"),
       ("816.554.784-69", "Bruno Henrique Morais", 25, "85 Kg", "A-", "CE", "Russas", "999741256", "brunohenrique@hotmail.com"),
       ("254.963.102-11", "Erik Douglas Ferreira", 21, "72 Kg", "A+", "MG", "Ouro Preto", "985145798", "erik.douglas@gmail.com"),
       ("478.985.655-74", "Flávia Nycole Moreira", 18, "55 Kg", "AB-", "RN", "Apodi", "999741256", "moreira.nycole@escolar.ifrn.edu.br");
       

-- Histórico dos doadores:
INSERT INTO HistoricoDoador (doenca, Doador_codigo, Doador_cpf)
VALUES ("Asma", 4, "254.963.102-11"),
	   ("Osteoporose", 4, "254.963.102-11"),
       ("Osteoporose", 3, "816.554.784-69");    
       

-- Solicitações:
INSERT INTO Solicitacao (data, urgencia, tipo_sanguineo, local_internacao, Solicitante_codigo, Solicitante_cpf)
VALUES ("2022-03-17", 1, "A-", "Hospital Regional Dr.Aguinaldo Pereira", 1, "713.867.104-07"),
	   ("2022-03-12", 5, "B-", "Hospital Regional de Apodi", 2, "715.874.320-02"),
       ("2022-03-09", 3, "O-", "Hospital Regional Dr.Aguinaldo Pereira", 3, "707.760.744-50"),
       ("2022-03-07", 5, "AB-", "Hospital Municipal Dr. Eilson Gurgel", 4, "707.125.024-32"),
       ("2022-03-14", 2, "B-", "Hospital Municipal Marcolino Bessa", 5, "153.174.234-30"); 


-- Solicitações_Doadores N-N:
INSERT INTO SolicitacaoDoador (Solicitacao_codigo, Doador_codigo, Doador_cpf)
VALUES (1, 1, "706.504.004-61"),
	   (4, 5, "478.985.655-74");
       
       
-- Doações:
INSERT INTO Doacao (data, local_destino, doador_codigo, doador_cpf) 
VALUES ("2022-03-19", "Hospital Regional Dr. Aguinaldo Pereira", 1, "706.504.004-61"),
	   ("2022-03-10", "Hospital Municipal Dr. Eilson Gurgel", 5, "478.985.655-74");
       
INSERT INTO Doacao (data, local_destino, doador_codigo, doador_cpf)
VALUES ("2022-08-10", "Hospital Regional Dr. Aguinaldo Pereira", 1, "706.504.004-61");



-- Área para consultas da tabelas completas:
SELECT * FROM Solicitante;
SELECT * FROM Doador;
SELECT * FROM HistoricoDoador;
SELECT * FROM Solicitacao;
SELECT * FROM SolicitacaoDoador;
SELECT * FROM Doacao;