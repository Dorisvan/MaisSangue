SELECT u.email FROM Usuario as u, Solicitacao as s
WHERE u.codigo = s.Usuario_codigo and s.codigo = 1; 

SELECT u.email FROM Usuario as u, Solicitacao as s 
WHERE s.codigo = %s AND u.codigo = s.Usuario_codigo;

SELECT * FROM USUARIO;

SELECT * FROM solicitacao;

SELECT s.codigo, s.data, s.urgencia, s.local_internacao, u.tipo_sanguineo, s.situacao 
FROM Solicitacao as s, Usuario as u 
WHERE s.Usuario_codigo = 6 AND s.Usuario_codigo = u.codigo
GROUP BY s.codigo, u.tipo_sanguineo, s.situacao;


INSERT INTO Usuario(cpf, nome, dt_nasc, peso, tipo_sanguineo, cep, cidade, email, senha, telefone, opcao_doacao, estado_sessao, nivel_usuario) 
VALUES ('702.932.302-53', 'João Pedro', '2004-04-19', '70', 'A+', '5070006', 'Caraúbas', 'joao.mota@escolar.ifrn.edu.br', '123','99900323', 'Sim', 0, 1);


INSERT INTO Solicitacao(data, urgencia, local_internacao, situacao, Usuario_codigo) 
VALUES('2023-06-01', 'Baixa', 'hospital x', 'Pendente', 6);


SELECT * FROM Doacao;

SELECT u.codigo 
FROM Usuario as u, UsuarioDoenca as ud, Doacao as d, Solicitacao as s
WHERE u.codigo = %s AND u.tipo_sanguineo = %s AND u.codigo NOT IN ud.codigo_usuario AND (SELECT Solicitacao WHERE s.codigo = %s AND s.situacao ="Pendente");

SELECT u.codigo, d.Solicitacao_codigo, d.data
FROM Usuario as u, Doacao as d
WHERE u.codigo = d.Usuario_codigo AND CURDATE()>DATE_ADD((SELECT MAX(d.data) ORDER BY MAX(d.data) DESC LIMIT 1), INTERVAL 120 DAY)
GROUP BY u.codigo;

SELECT d.Usuario_codigo
FROM Doacao as d
WHERE CURDATE()> (MAX(d.data), INTERVAL 4 MONTH);

SELECT d.Usuario_codigo
FROM Doacao AS d, Usuario as u
WHERE d.Usuario_codigo = u.codigo AND CURDATE() > (SELECT DATE_ADD(MAX(data), INTERVAL 4 MONTH) FROM Doacao)
GROUP BY d.Usuario_codigo;

SELECT *
FROM Doacao
WHERE codigo = 5 AND CURDATE() > DATE_ADD((SELECT MAX(data) FROM Doacao WHERE codigo = 5 GROUP BY codigo), INTERVAL 120 DAY);

SELECT *
FROM Doacao
WHERE SELECT



SELECT *
FROM Doacao
WHERE CURDATE() > DATE_SUB(NOW(), INTERVAL 120 DAY);

SELECT * FROM Doacao 
WHERE MAX(Doacao.data) ORDER BY MAX(d.data) DESC LIMIT 1;

SELECT d.codigo, d.data, d.local_destino, u.tipo_sanguineo, solicitacao_codigo 
FROM Doacao as d, Usuario as u
WHERE d.Usuario_codigo = u.codigo
ORDER BY u.tipo_sanguineo;


INSERT INTO Doacao(data, local_destino, solicitacao_codigo, usuario_codigo) 
VALUES ('2022-03-03', 'Hopistal x', 2, 6);

SELECT DISTINCT *
FROM Usuario as u 
WHERE u.codigo LIKE 'A+' OR u.cpf LIKE 'A+' OR u.nome LIKE 'A+' OR u.dt_nasc LIKE 'A+' OR u.peso LIKE 'A+' OR u.tipo_sanguineo LIKE 'A+' OR u.cep LIKE 'A+' OR u.cidade LIKE 'A+' OR u.email LIKE 'A+' OR u.senha LIKE 'A+' OR u.telefone LIKE 'A+' OR u.opcao_doacao LIKE 'A+' OR u.estado_doacao LIKE 'A+' OR u.nivel_usuario LIKE 'A+';

SELECT DISTINCT s.codigo, s.data, s.urgencia, s.local_internacao, u.tipo_sanguineo, s.situacao 
FROM Solicitacao as s, Usuario as u 
WHERE s.Usuario_codigo = u.codigo AND s.codigo LIKE 'Baixa' OR s.data LIKE 'Baixa' OR s.urgencia LIKE 'Baixa' OR s.local_internacao LIKE 'Baixa' OR u.tipo_sanguineo LIKE 'Baixa' OR s.situacao LIKE 'Baixa'
GROUP BY s.codigo, u.tipo_sanguineo, s.situacao, s.urgencia;

SELECT DISTINCT d.codigo, d.data, d.local_destino, d.Solicitacao_codigo, u.tipo_sanguineo
FROM Doacao as d, Usuario as u
WHERE d.Usuario_codigo = u.codigo AND d.codigo LIKE 2 OR d.data LIKE 2 OR d.local_destino LIKE 2 OR d.Solicitacao_codigo LIKE 2 OR d.Usuario_codigo LIKE 2
GROUP BY d.codigo;

SELECT ud.Usuario_codigo, u.nome, d.id, d.nome
FROM UsuarioDoenca as ud, Usuario as u, Doenca as d
WHERE ud.Usuario_codigo = u.codigo AND ud.Doenca_id = d.id;

INSERT INTO UsuarioDoenca(Doenca_id, Usuario_codigo) VALUES (1, 2);

SELECT * FROM UsuarioDoenca;


SELECT s.codigo, s.data, s.urgencia, s.local_internacao, u.tipo_sanguineo, s.situacao 
FROM Solicitacao as s, Usuario as u 
WHERE s.Usuario_codigo = u.codigo AND s.codigo = 2
GROUP BY s.codigo, u.tipo_sanguineo, s.situacao;

SELECT u.codigo FROM Usuario as u, Doacao as d 
WHERE u.codigo = d.Usuario_codigo AND CURDATE() > DATE_ADD((SELECT MAX(d.data) ORDER BY MAX(d.data) DESC LIMIT 1), INTERVAL 120DAY);

SELECT u.codigo
FROM Usuario as u, Doacao as d 
WHERE 2 NOT IN(SELECT d.Usuario_codigo FROM Doacao as d)
GROUP BY u.codigo;

SELECT d.Usuario_codigo FROM Doacao as d;

SELECT DISTINCT s.codigo, s.data, s.urgencia, s.local_internacao, u.tipo_sanguineo, s.situacao 
FROM Solicitacao as s, Usuario as u 
WHERE s.Usuario_codigo = u.codigo AND s.Usuario_codigo = 2 AND s.codigo LIKE 'Extrema' OR s.data LIKE 'Extrema' OR s.urgencia LIKE 'Extrema' OR s.local_internacao LIKE 'Extrema' OR u.tipo_sanguineo LIKE 'Extrema' OR s.situacao LIKE 'Extrema' 
GROUP BY s.codigo;

SELECT DISTINCT d.usuario_codigo, d.data, d.local_destino, u.tipo_sanguineo, d.Solicitacao_codigo 
FROM Doacao AS d, Usuario AS u, Solicitacao as s
WHERE d.Usuario_codigo = 2 AND (d.codigo = 3 OR d.data = 3 OR d.local_destino = 3 OR d.Solicitacao_codigo = 3 OR d.Usuario_codigo = 3)
GROUP BY d.Solicitacao_codigo;


SELECT DISTINCT d.usuario_codigo, d.data, d.local_destino, u.tipo_sanguineo, d.Solicitacao_codigo 
FROM Doacao as d, Usuario as u 
WHERE d.codigo LIKE 1 OR d.data LIKE 1 OR d.local_destino LIKE 1 OR d.Solicitacao_codigo LIKE 1 OR d.Usuario_codigo LIKE 1 OR u.tipo_sanguineo LIKE 1;


SELECT DISTINCT d.usuario_codigo, d.data, d.local_destino, u.tipo_sanguineo, d.Solicitacao_codigo 
FROM Doacao as d, Usuario as u
WHERE d.Usuario_codigo = u.codigo AND d.Usuario_codigo = 3 AND (d.codigo LIKE 1 OR d.data LIKE 1 OR d.local_destino LIKE 1 OR d.Solicitacao_codigo LIKE 1 OR d.Usuario_codigo LIKE 1);

UPDATE Usuario 
SET cpf="504", nome="Dorisvan", dt_nasc='2004-04-21', peso=50, tipo_sanguineo="A+", cep="123", cidade="Caraúbas", email="Dorisvan@gmail.com", senha="123", telefone="903232", opcao_doacao="Sim"
WHERE codigo=1;