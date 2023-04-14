SELECT * FROM Usuario;

SELECT * FROM Doacao;

SELECT * FROM Solicitacao;

SELECT * FROM UsuarioDoenca;

SELECT * FROM Doenca;

INSERT INTO Doacao(data, local_destino, urgencia, usuario_cpf, solicitacao_codigo)
VALUES ('20/04/2024', 'hospital', 2, 705, 1);

SELECT s.codigo, s.urgencia, s.local_internacao, u.tipo_sanguineo
FROM Solicitacao as s, Usuario as u
WHERE s.Usuario_cpf = u.cpf
GROUP BY u.tipo_sanguineo;

SELECT d.codigo, d.urgencia, d.local_internacao, u.tipo_sanguineo;

SELECT d.codigo, d.data, d.local_destino, u.tipo_sanguineo, 
CASE 
WHEN s.urgencia = 1 THEN  "Baixa" 
WHEN s.urgencia = 2 THEN  "Média"
WHEN s.urgencia = 3 THEN  "Alta" 
WHEN s.urgencia = 4 THEN  "Extrema"
END as urgencia
FROM Doacao as d, Usuario as u, Solicitacao as s
WHERE d.Usuario_cpf = u.cpf
GROUP BY u.tipo_sanguineo;

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


SELECT * FROM Doacao 
WHERE Usuario_cpf = Doacao.usuario_cpf
ORDER BY Doacao.data DESC;
