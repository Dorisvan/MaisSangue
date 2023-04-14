-- Consultas

-- 1. Liste os doadores do tipo de sangue O (O- ou O+).

SELECT d.codigo, d.nome, d.cpf, d.tipo_sanguineo, d.telefone, d.email, d.cidade 
FROM Doador as d
WHERE d.tipo_sanguineo = "O-" or d.tipo_sanguineo = "O+";


-- 2. Separe o número de doadores por idade.

SELECT d.idade, COUNT(d.idade) as quantidade_de_doadores
FROM Doador as d
GROUP BY d.idade
ORDER BY d.idade;


-- 3. Liste as solicitações que estão pendentes.

SELECT * 
FROM Solicitacao as s
WHERE s.codigo NOT IN (SELECT so.solicitacao_codigo FROM SolicitacaoDoador as so);


-- 4. Liste o total de doadores por tipo_sanguineo.

SELECT d.tipo_sanguineo, COUNT(d.tipo_sanguineo) as quantidade_de_doadores
FROM Doador as d
GROUP BY d.tipo_sanguineo;


-- 5. Liste os solicitantes e doadores que estão no mesmo estado, incluindo a cidade de cada um.

SELECT s.codigo as solicitante_codigo, s.nome as solicitante_nome, s.cidade as solicitante_cidade, s.uf as solicitante_estado, so.tipo_sanguineo as solicitante_tipo_sanguineo, d.codigo as doador_codigo, d.nome as doador_nome, d.cidade as doador_cidade, d.estado as doador_estado, d.tipo_sanguineo as doador_tipo_sanguineo
FROM Solicitante as s, Solicitacao as so, Doador as d
WHERE s.codigo = so.Solicitante_codigo and s.uf = d.estado 
ORDER BY s.uf, s.cidade; 


-- 6. Liste os tipos de doenças mais comuns, com base na ordem decrescente.

SELECT hd.doenca, COUNT(hd.doenca) as numero_de_casos
FROM HistoricoDoador as hd
GROUP BY hd.doenca
ORDER BY numero_de_casos DESC;

-- 7. Liste o histórico de doenças de cada doador e teste se nenhuma doença impede que seja um doador.

SELECT d.codigo, d.nome, hd.doenca,
CASE 
	WHEN hd.doenca NOT IN ("HIV","Doença de Chagas","Sífilis") THEN  "Ok"
    WHEN hd.doenca IN ("HIV","Doença de Chagas","Sífilis") THEN  "Not Ok"
END as situacao
FROM HistoricoDoador as hd, doador as d
WHERE d.codigo = hd.Doador_codigo
ORDER BY d.codigo;


-- 8. Liste as solicitações com maiores graus de urgência no momento.

SELECT s.codigo, s.data, s.tipo_sanguineo, s.local_internacao, s.Solicitante_codigo, s.Solicitante_cpf,
CASE 
	WHEN s.urgencia = 1 THEN  "Extrema"
	WHEN s.urgencia = 2 THEN  "Muito alta"
	WHEN s.urgencia = 3 THEN  "Alta"
	WHEN s.urgencia = 4 THEN  "Média"
	WHEN s.urgencia = 5 THEN  "Baixa"
END as "urgencia"
FROM Solicitacao as s
WHERE s.urgencia in (1, 2, 3)
ORDER BY s.urgencia; 


-- 9. Liste os doadores que já doaram pelo menos uma vez, se for o caso, mostre a última solicitação que cada um atendeu.

SELECT d.codigo as codigo_doador, d.nome as nome_doador, d.cpf as cpf_doador, MAX(doa.data) as ultima_doacao, sd.Solicitacao_codigo
FROM Doador as d, Doacao as doa, SolicitacaoDoador as sd
WHERE d.codigo = doa.Doador_codigo AND d.codigo = sd.Doador_codigo AND doa.data = (SELECT doa.data ORDER BY doa.data DESC LIMIT 1)
GROUP BY d.codigo
ORDER BY d.codigo;


-- 10. Liste os doadores aptos a doar novamente, considerando seu peso e a data da última doação.

SELECT d.codigo, d.cpf, d.nome, d.idade, d.peso, d.tipo_sanguineo, d.estado, d.cidade, d.telefone, d.email, MAX(doa.data) as ultima_doacao,
CASE 
	WHEN d.codigo = doa.Doador_codigo AND CURDATE()>DATE_ADD((SELECT MAX(doa.data) ORDER BY MAX(doa.data) DESC LIMIT 1), INTERVAL 120 DAY) AND d.peso > 50 THEN  "Ok"
END as "Situacao"
FROM Doacao as doa, Doador as d, historicodoador as hd
WHERE doa.data = (SELECT MAX(doa.data) ORDER BY MAX(doa.data) DESC LIMIT 1 ) AND d.codigo = doa.Doador_codigo
GROUP BY d.codigo;

