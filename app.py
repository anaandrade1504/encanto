from flask import Flask, request
app = Flask('instancia_flask')
import requests
#--------------------------------- rota para receber as informações do Webhook ------------------------------------
@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    event_type = data['event']
    payload = data['payload']
    process_event(event_type, payload)
    return "Webhook recebido"

#--------------------------------- Função que processa webhook  ------------------------------------  
def process_event(event_type,payload):
    # Dicionário com os casos possíveis de event_type e suas funções correspondentes
    cases = {
        "update_stock": update_stock_handler,
        "new_customer": new_customer_handler,
        "paid_sale": paid_sale_handler,
        "new_product": new_product_handler,
        "delete_product": delete_product_handler
    }

    # Verifica se event_type está presente nos casos
    if event_type in cases:
        # Obtém a função correspondente ao event_type
        handler = cases[event_type]
        # Chama a função correspondente passando o payload como parâmetro
        handler(payload)
    else:
        # Caso o event_type seja desconhecido
        print("Não foi possível indentificar o evento do webhook")

#--------------------------------- Função para lidar com o caso "update_stock" ------------------------------------
def update_stock_handler():
    print("Handling update_stock event")

#--------------------------------- Função para lidar com o caso "new_customer" ------------------------------------
def new_customer_handler():
    print("Handling new_customer event")

#--------------------------------- Função para lidar com o caso "paid_sale" ------------------------------------
def paid_sale_handler():
    print("Handling paid_sale event")

#--------------------------------- Função para lidar com o caso "new_product" ------------------------------------
def new_product_handler(payload):
    print("Handling new_product event")
    # Extrair as informações necessárias do payload
    product_data = payload['data']
    product_name = product_data['description']
    product_price = product_data['price']
    # !!!!!!!!!!!!!!!!!!!!!!! extrair outras informações necessárias do produto !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    
    # Montar o payload para a criação do produto na API da Nuvemshop
    POST_payload = {
        'name': product_name,
        'price': product_price,
        'description': product_data['description'], 
        'categories': product_data['category']['description'], 
        'stock': product_data['stock'], 
        'images': product_data['image_url'], 
        'barcode': product_data['barcode'], 
        'amount': product_data['amount'],
        'markup': product_data['markup'],
        'cost': product_data['cost'],
        'liquid': product_data['liquid'], 
        'discount': product_data['discount'],
        'discount_pct': product_data['discount_pct'],
        'status': product_data['status'],
        'environment': product_data['environment'],
        'partner_userid': product_data['partner_userid'],
        'text': product_data['text'],
        # ... adicionar outras informações necessárias para criar o produto na API
    }
    
    # Fazer o chamado para a API da Nuvemshop para inserir o novo produto
    api_url = 'https://api.nuvemshop.com.br/v1/products'
    api_headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer YOUR_API_TOKEN'  # Substitua pelo seu token de API válido
    }
    response = requests.post(api_url, json=POST_payload, headers=api_headers)

    
    # Verificar a resposta da API
    if response.status_code == 201:
        print("Novo produto inserido com sucesso")
    else:
        print("Falha ao inserir produto")
        print("Response:", response.json())

#--------------------------------- Função para lidar com o caso "delete_product" ------------------------------------
def delete_product_handler():
    print("Handling delete_product event")


