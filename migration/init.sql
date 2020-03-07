DROP TABLE IF EXISTS contents;
CREATE TABLE contents (
	id VARCHAR UNIQUE,
	content VARCHAR
);
CREATE INDEX id ON contents (id);

DROP TABLE IF EXISTS contents_childs;
CREATE TABLE contents_childs (
	parent VARCHAR,
	id VARCHAR,
	icon VARCHAR,
	title VARCHAR,
	content VARCHAR
);
CREATE UNIQUE INDEX parent_id ON contents_childs (parent, id);

INSERT INTO contents (id, content) VALUES
('home_title', 'Home'),
('home_top_h1', 'Python + Flask'),
('home_top_p', 'Uma página simples para testar requisições em APIs REST com python e requests ou qualquer outra linguagem de programação.'),
('home_m1_h2', 'Um Grade Microframework'),
('home_m1_p', 'Apesar da simplicidade e leveza, o flask é capaz de suportar aplicações extremamente complexas com a adição de módulos extras não presente no núcleo.'),
('home_m1_boxes', '[]');

INSERT INTO contents_childs (parent, id, icon, title, content) VALUES
('home_m1_boxes','m1_1','ti-package','Design Único','Sua arquitetura modular facilita escolher somente o necessário, evitando projetos inchados.'),
('home_m1_boxes','m1_2','ti-mouse-alt','Solução para Negócios','Microserviços estão em alta! O Flask é perfeito para criar microserviços!'),
('home_m1_boxes','m1_3','ti-headphone-alt','Suporte ao Usuário','Bem, podemos sempre ler a documentação online, certo? Qualquer coisa podemos contar com o professor!');
