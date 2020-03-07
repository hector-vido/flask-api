# Flask API

Site utilizado para testar os vários métodos de uma API REST com resultados fáceis de perceber.

## Iniciar

Para preparar a aplicação, iniciando o banco de dados e depois a própria aplicação, execute:

```bash
https://github.com/hector-vido/flask-api.git
cd flask-api
apt-get install -y sqlite3
sqlite3 data.db < migration/init.sql
python3 app.py
```

## Métodos

### - /api/items - GET

Retorna a lista completa dos ids de itens disponíveis com seus respectivos ids de subitens.

```bash
curl http://localhost:5000/api/items
```

```
[
  {
    "home_m1_boxes": [
      "m1_1"
    ]
  }, 
  "home_m1_h2"
]
```

### - /api/item/[id]/subitems - GET

Retorna a lista completa dos ids disponíveis dos subitens de um determinado item.

```bash
curl http://localhost:5000/api/item/home_m1_boxes/subitems
```

```json
[
  "m1_1", 
  "m1_2"
]
```

### - /api/item/[id] - PUT

Atualiza o conteúdo de um determinado item.

```
curl -X PUT -d '{"content" : "From API"}' -H 'Content-Type: application/json' localhost:5000/api/item/home_title
```

```
{"message": "Item home_title atualizado!"}
```

### - /api/item/[parent]/subitem - POST

Cria um item dentro de um determinado subitem.

```
curl -X POST -d '{"id" : "m1_0", "title" : "Shablau!", "icon" : "ti-dashboard", "content" : "Dolores officia et voluptatem et laboriosam nostrum."}' -H 'Content-Type: application/json' localhost:5000/api/item/home_m1_boxes/subitem
```

```
{"message": "Item m1_0 cadastrado com sucesso!"}
```

### - /api/item/[parent]/[id] - PUT

Atualiza um subitem de um determinado item.

```bash
curl -X PUT -d '{"title" : "Shablau!", "icon" : "ti-dashboard", "content" : "Lorem Ipsum"}' -H 'Content-Type: application/json' localhost:5000/api/item/home_m1_boxes/m1_1
```

```json
{"message": "Item m1_666 de home_m1_boxes atualizado!"}
```

### - /api/item/[parent]/[id] - DELETE

Remove um subitem de um determinado item.

```bash
curl -X DELETE localhost:5000/api/item/home_m1_boxes/m1_1
```

```
{"message": "Item m1_1 de home_m1_boxes removido!"}

```

## Ícones

Os ícones dos blocos podem ser alterados para qualquer um presente em [http://themify.me/themify-icons](http://themify.me/themify-icons).

## Renderizar HTML

Se deseja renderizar HTML gravado no banco através dos templates do Jinja, por questões de segurança, é necessário adicionar um modificador ao lado da variável:

	{{ c.nome|safe }}
