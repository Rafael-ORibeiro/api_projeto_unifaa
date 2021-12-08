from dns.rdatatype import NULL
from flask import Flask, Response, request
from flask.sessions import NullSession
from flask_pymongo import PyMongo
from bson import json_util
from bson.json_util import dumps
from flask_cors import CORS


    

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

app.config['MONGO_URI'] = "mongodb+srv://ror74559:12mm34@betcartoes.jbbi4.mongodb.net/cadastro?retryWrites=true&w=majority"

#collection produtos
mongo = PyMongo(app)

def retornarDados(resp):
    jsonResposta = []
    for dados in resp.json:
        jsonResposta.append({"codigo":dados["codigo"],
                             "produto":dados["produto"],
                             "quantidade":dados["quantidade"],
                             "valor":dados["valor"],
                             "data":dados["data"],
                             "descrição":dados["descrição"]
                             })
    return {"result": jsonResposta}

@app.route('/produtos',methods=['GET'])

def getProdutos():
    
    query_ = mongo.db.produtos.find()
    
    response = Response(json_util.dumps(query_),mimetype='application/json')
    
    return retornarDados(response)


@app.route('/produto/<codigo>',methods=['GET'])
def getProduto(codigo):
    
    query_ = mongo.db.produtos.find({"codigo":codigo})
    
    response = Response(json_util.dumps(query_),mimetype='application/json')
    
    return retornarDados(response)




@app.route('/produtos',methods=['POST'])

def postProdutos():
    
    print(request)
       
    duplicidade = dumps(mongo.db.produtos.find({"codigo":request.json[0]["codigo"]}))
    
    lista = eval(duplicidade)
    
    try:
        
        if lista == []:
                
            mongo.db.produtos.insert_one(request.json[0])
                
            return{"message":"Produto cadastrado com sucesso"}
            
        return{"message":"Já existe produto com esse código"}
    
    except:
        
        return{"message":"Erro ao tentar cadastrar produto."}
    
    
    
@app.route('/produtos/update',methods=['PUT'])

def updateProdutos():
    
    existeCodigo = dumps(mongo.db.produtos.find({"codigo":request.json[0]["codigo"]}))
    
    if existeCodigo != "[]": 
        
        novo = {"$set": {"codigo":request.json[0]["codigo"],
                            "produto":request.json[0]["produto"],
                            "quantidade":request.json[0]["quantidade"],
                            "valor":request.json[0]["valor"],
                            "data":request.json[0]["data"],
                            "descrição":request.json[0]["descrição"]
                            }}
        
        filtro ={"codigo":request.json[0]["codigo"]}
            
        try:
            mongo.db.produtos.update(filtro,novo)
            
            return{"message":"Produto atualizado!"}
        
        except:
            
            return{"message":"Erro ao tentar atualizar produto"}
    #response = Response(json_util.dumps(query_),mimetype='application/json')
        
    return {"message":"Esse produto não existe\n ou o produto já existe com a \nquantidade informada!"}



@app.route('/produtos/delete',methods=['DELETE'])

def deleteProdutos():
    
    produtoQueSeraDeletado = dumps(mongo.db.produtos.find({"codigo":request.json[0]["codigo"]}))
    
    if produtoQueSeraDeletado != "[]":
        try:
            filtro ={"codigo":request.json[0]["codigo"]}
            
            mongo.db.produtos.remove(filtro)
            
            return {"message":"Produto Deletado!"}
        
        except:
            
            return {"message":"Erro na tentativa de deletar"}
        
        #response =  Response(json_util.dumps(query_),mimetype='application/json')
    
    return{"message":"Produto não encontrado"}





if __name__ == "__main__":
    app.run(debug=True)