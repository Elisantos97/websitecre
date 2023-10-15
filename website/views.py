from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
import requests
from datetime import datetime
from website import auth
import base64
import time

views = Blueprint('views', __name__)




url ='https://elisandroapicre.azurewebsites.net/clientes'
url1='https://elisandroapicre.azurewebsites.net/produtos'
url2='https://elisandroapicre.azurewebsites.net/categorias'
url3='https://elisandroapicre.azurewebsites.net/subcategorias'
url4='https://elisandroapicre.azurewebsites.net/imagens'
url5='https://elisandroapicre.azurewebsites.net/produto_relacionado'
url6='https://elisandroapicre.azurewebsites.net/carrinho'
url7='https://elisandroapicre.azurewebsites.net/conta'
url8='https://elisandroapicre.azurewebsites.net/vendas'
url9='https://elisandroapicre.azurewebsites.net/alterar'
url10='https://elisandroapicre.azurewebsites.net/resposta'
url11='https://elisandroapicre.azurewebsites.net/desafio'
url12='https://elisandroapicre.azurewebsites.net/foto'
url13='https://elisandroapicre.azurewebsites.net/respostafotos'


@views.route("/",methods=['GET'])
def home():



    idCliente=0

    if "email" in session:
        clientes=requests.get(url)
        for cliente in clientes.json():
            if cliente.get("emailCliente")==session.get("email"):
                idCliente=cliente.get("idCliente")
    


    produtos = requests.get(url1)
    categorias = requests.get(url2)
    subcategorias = requests.get(url3)
    

    exibir_header=True
    return render_template('produtos.html', exibir_header=exibir_header, produtos=produtos.json(), categorias=categorias.json(), subcategorias=subcategorias.json(), idCliente=idCliente)


@views.route("/subcategoria/<nome>",methods=['GET'])
def subcategoria(nome):

    idCliente=0

    if "email" in session:
        clientes=requests.get(url)
        for cliente in clientes.json():
            if cliente.get("emailCliente")==session.get("email"):
                idCliente=cliente.get("idCliente")

    produtos = requests.get(url1+'/subcategoria/'+nome)
    categorias = requests.get(url2)
    subcategorias = requests.get(url3)
    

    
    return render_template('produtos.html', produtos=produtos.json(), categorias=categorias.json(), subcategorias=subcategorias.json(), idCliente=idCliente)


@views.route("/categoria/<nome>",methods=['GET'])
def categoria(nome):

    idCliente=0

    if "email" in session:
        clientes=requests.get(url)
        for cliente in clientes.json():
            if cliente.get("emailCliente")==session.get("email"):
                idCliente=cliente.get("idCliente")

    produtos = requests.get(url1+'/categoria/'+nome)
    categorias = requests.get(url2)
    subcategorias = requests.get(url3)
    

    
    return render_template('produtos.html', produtos=produtos.json(), categorias=categorias.json(), subcategorias=subcategorias.json(),idCliente=idCliente)


@views.route("/<nome>",methods=['GET'])
def nome(nome):
        
    idCliente=0

    if "email" in session:
        clientes=requests.get(url)
        for cliente in clientes.json():
            if cliente.get("emailCliente")==session.get("email"):
                idCliente=cliente.get("idCliente")

    produtos = requests.get(url1+'/'+nome)
    categorias = requests.get(url2)
    subcategorias = requests.get(url3)


    return render_template('produtos.html', produtos=produtos.json(), categorias=categorias.json(), subcategorias=subcategorias.json(), idCliente=idCliente)

    

@views.route("/produto/<int:id>",methods=['GET'])
def produto(id):

    idCliente=0

    if "email" in session:
        clientes=requests.get(url)
        for cliente in clientes.json():
            if cliente.get("emailCliente")==session.get("email"):
                idCliente=cliente.get("idCliente")

    produtos = requests.get(url1)
    produto = requests.get(url1+'/'+str(id))
    categorias = requests.get(url2)
    subcategorias = requests.get(url3)
    imagens=requests.get(url4+'/produto/'+str(id))
    prod_relacionado=requests.get(url5+'/produto/'+str(id))
    



    imagens=imagens.json()

    num_imagens=len(imagens)

    s=0
    for i in range(num_imagens):
        imagens[i]['ind']=2+s
        s=s+1


    return render_template('produto.html', produto=produto.json(),produtos=produtos.json(), imagens=imagens, prod_relacionado=prod_relacionado.json(), \
                           categorias=categorias.json(), subcategorias=subcategorias.json(), idCliente=idCliente)   


@views.route('/adicionar_carrinho', methods=["POST"])
def adicionar_carrinho():


    if "email" in session:

        clientes=requests.get(url)
        for cliente in clientes.json():
            if cliente.get("emailCliente")==session.get("email"):
                idCliente=cliente.get("idCliente")
             

        idProduto = request.form.get('idProduto')
        quantidade = request.form.get('quantidade')
        precoUnitario = request.form.get('precoUnitario')
        precoTotal = request.form.get('precoTotal')

        print(idProduto)




        dados = {"idProduto": int(idProduto),"idCliente": idCliente, "quantidade": int(quantidade), "precoUnitario": float(precoUnitario), "precoTotal": float(precoTotal)}
        print(dados)
        api=requests.post(url6, json=dados)

        return redirect(url_for("views.produto", id=idProduto))

    else:

        return redirect(url_for("auth.login"))




@views.route('/api/submit', methods=['GET'])
def submit_data():
    idCliente= request.args.get('idCliente')
    print(idCliente)

    

    count = requests.get('https://elisandroapicre.azurewebsites.net/soma_produto/'+str(idCliente))
        
    print(count.json())
    return str(count.json())
    
    
  


@views.route('/carrinho', methods=['GET'])
def carrinho():

    if "email" in session:

        clientes=requests.get(url)
        for cliente in clientes.json():
            if cliente.get("emailCliente")==session.get("email"):
                idCliente=cliente.get("idCliente")
    
        produtos = requests.get(url1)
        categorias = requests.get(url2)
        subcategorias = requests.get(url3)


        lista_produtos=requests.get(url6+'/cliente/'+str(idCliente))
        lista_produtos=lista_produtos.json()

        lista_carrinho=[]
        valor_total = []

        for produto1 in produtos.json():
            for produto2 in lista_produtos:
                if produto1.get("idProduto")==produto2.get("idProduto"):
                    produto2["imagemProduto"]=produto1.get("imagemProduto")
                    lista_carrinho.append(produto2)

        for produto in lista_produtos:
            valor_total.append(produto.get("precoTotal"))


        return render_template("carrinho.html", lista_carrinho=lista_carrinho, categorias=categorias.json(), subcategorias=subcategorias.json(), valor_total=("%.2f" %sum(valor_total)), idCliente=idCliente)
    
    return redirect(url_for("auth.login"))


@views.route('/apagar_produto/<id>', methods=['GET', 'POST'])
def apagar_produto(id):

    api = requests.delete(url6+'/'+str(id))

    return redirect(url_for("views.carrinho"))


@views.route('/finalizar_compra', methods=['GET', 'POST'])
def finalizar_compra():


    categorias = requests.get(url2)
    subcategorias = requests.get(url3)
    valor_total=request.form.get("valor_total")

    return render_template("finalizar_compra.html", valor_total=valor_total, categorias=categorias.json(), subcategorias=subcategorias.json())


@views.route('/pagamento', methods=['GET', 'POST'])
def pagamento():

    if "email" in session:

        clientes=requests.get(url)
        for cliente in clientes.json():
            if cliente.get("emailCliente")==session.get("email"):
                idCliente=cliente.get("idCliente")


    numeroCartao = request.form.get('numeroCartao')
    ccv = request.form.get('ccv')
    valor_total = request.form.get('valor_total')
    nome = request.form.get('nome')
    morada = request.form.get('morada')
    nif = request.form.get('nif')
    codigopostal = request.form.get('codigopostal')
    cidade = request.form.get('cidade')

    




    contas=requests.get(url7)
    

    for conta_bancaria in contas.json():
        print(numeroCartao==conta_bancaria.get("numeroCartao"))
        print(int(ccv)==conta_bancaria.get("ccv"))
        print(conta_bancaria.get("saldo")>= float(valor_total))
        if numeroCartao==conta_bancaria.get("numeroCartao") and int(ccv)==conta_bancaria.get("ccv") and conta_bancaria.get("saldo")>= float(valor_total):

            lista_produtos=requests.get(url6+'/cliente/'+str(idCliente))
            lista_produtos=lista_produtos.json()

            for produto in lista_produtos:
                api = requests.delete(url6+'/'+str(produto.get("idCarrinho")))

                idProduto=produto.get("idProduto")
                idCliente=produto.get("idCliente")
                quantidade=produto.get("quantidade")
                precoTotal=produto.get("precoTotal")
                iva=0

                dados={"idProduto":idProduto, "idCliente":idCliente, "quantidade":quantidade, "precototal":precoTotal, "iva":iva, "nomeEntrega": nome, "moradaEntrega": morada,"nifEntrega": nif,"codigopostalEntrega": codigopostal,"cidadeEntrega": cidade}
                print(dados)



                vendas = requests.post(url8, json=dados)

            flash('Compra feita com sucesso', category='success')
            return redirect(url_for("views.home"))
  
    flash('Erro de pagamento', category='error')
    return redirect(url_for("views.carrinho"))


@views.route('/area_pessoal', methods=['GET', 'POST'])
def area_pessoal():

    if "email" in session:
        
        return redirect(url_for("views.dados"))
    
    return redirect(url_for("auth.login"))



@views.route('/dados', methods=['GET', 'POST'])
def dados():

    if "email" in session:

        dados={}

        clientes=requests.get(url)
        for cliente in clientes.json():
            if cliente.get("emailCliente")==session.get("email"):
                dados["nome"]=cliente.get("nomeCliente")
                dados["email"]=cliente.get("emailCliente")
                dados["telefone"]=cliente.get("telefoneCliente")
                dados["telemovel"]=cliente.get("telemovelCliente")
                dados["nif"]=cliente.get("nifCliente")
                dados["morada"]=cliente.get("moradaCliente")
                dados["codigopostal"]=cliente.get("codigopostalCliente")
                dados["cidade"]=cliente.get("cidadeCliente")

        print(dados)

        
        return render_template("dados.html", dados=dados)
    
    return redirect(url_for("auth.login"))

@views.route('/historico', methods=['GET', 'POST'])
def historico():

    if "email" in session:

        clientes=requests.get(url)
        for cliente in clientes.json():
            if cliente.get("emailCliente")==session.get("email"):
                idCliente=cliente.get("idCliente")
    
        produtos = requests.get(url1)


        lista_produtos=requests.get(url8+'/cliente/'+str(idCliente))
        lista_produtos=lista_produtos.json()

        lista_compra=[]

        for produto1 in produtos.json():
            for produto2 in lista_produtos:
                if produto1.get("idProduto")==produto2.get("idProduto"):
                    produto2["imagemProduto"]=produto1.get("imagemProduto")
                    lista_compra.append(produto2)


    
    return render_template("historico.html", compras=lista_compra)


@views.route('/password', methods=['GET', 'POST'])
def password():

    clientes=requests.get(url)
    for cliente in clientes.json():
        if cliente.get("emailCliente")==session.get("email"):
            idCliente=cliente.get("idCliente")
            

    clientes=requests.get(url+'/'+str(idCliente))
    cliente=clientes.json()


    if request.method == 'POST':
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        password3 = request.form.get('password3')

        if cliente.get("passwordCliente")==password1 and password2==password3:
            dados={"passwordCliente": password2}
            api=requests.patch(url9+'/'+str(idCliente), json=dados)

            flash('Palavra-passe alterada com sucesso!', category='Success')
            return render_template("password.html")
            

        else:
            flash('Ocorreu algum erro!', category='error')
            return render_template("password.html")
        
    return render_template("password.html")



##############################################################################




@views.route('/desafio', methods=['GET'])
def desafio():
        
    if "email" in session:

        categorias = requests.get(url2)
        subcategorias = requests.get(url3)

        try:

            lista_desafios=requests.get(url11)

            data_atual = datetime.now().strftime('%Y-%m-%d')

            for desafio in lista_desafios.json():

                if data_atual==desafio.get("dataDesafio"):


            
    
            
                    desafios=requests.get(url11+'/'+str(desafio.get("idDesafio")))


                    return render_template("desafio.html",desafio=desafios.json(), categorias=categorias.json(), subcategorias=subcategorias.json())
                
        
        except:
        
            return redirect(url_for("views.home"))
        
        return redirect(url_for("views.home"))

    else:
        return redirect(url_for("auth.login"))

@views.route('/resposta', methods=['POST'])
def resposta():
    


    clientes=requests.get(url)
    for cliente in clientes.json():
        if cliente.get("emailCliente")==session.get("email"):
            idCliente=cliente.get("idCliente")

    email=session["email"]
    resposta = request.form.get('resposta')
    idDesafio = request.form.get('idDesafio')
    imagemProduto= request.form.get('imagem')

    if resposta=="opcao1":
        nota="correta"
        flash('Resposta correta!', category='success')

    else:
        nota="incorreta"
        flash('Resposta erraada!', category='error')      

    
    dados={"respostaCliente":resposta, "emailCliente":email, "idDesafio":idDesafio, "imagemProduto":imagemProduto,"nota":nota}
    respostacliente=requests.post(url10, json=dados)
    

    return redirect(url_for("views.home"))
    



@views.route('/partilha', methods=['GET','POST'])
def partilha():

    if "email" in session:

        api=requests.get(url12)

        

        fotos=api.json()

        


        categorias = requests.get(url2)
        subcategorias = requests.get(url3)

        return render_template("partilhadefotos.html", categorias=categorias.json(), subcategorias=subcategorias.json(), fotos=fotos)
    
    else:
        return redirect(url_for("auth.login"))


@views.route('/partilhar_foto', methods=['POST'])
def partilhar_foto():

    clientes=requests.get(url)
    for cliente in clientes.json():
        if cliente.get("emailCliente")==session.get("email"):
            idCliente=cliente.get("idCliente")

    imagem = request.form.get('imagemProduto')

    dados={"foto":imagem, "idCliente":idCliente}

    api=requests.post(url12, json=dados)


    return redirect(url_for("views.partilha"))



@views.route('/resposta_foto', methods=['POST'])
def resposta_foto():

    clientes=requests.get(url)
    for cliente in clientes.json():
        if cliente.get("emailCliente")==session.get("email"):
            idCliente=cliente.get("idCliente")

    resposta = request.form.get('resposta')
    idFoto = request.form.get('idFoto')


    dados={"resposta":resposta, "idCliente":idCliente, "idFoto":idFoto}

    api=requests.post(url13, json=dados)


    return redirect(url_for("views.partilha"))


@views.route('/respostas/<int:id>', methods=['GET'])
def respostas(id):


    
    respostas=requests.get(url13)

    fotos=requests.get(url12+'/'+str(id))
    foto=fotos.json()


    lista_respostas=[]

    for resposta in respostas.json():
        if resposta.get("idFoto")== foto.get("idFoto"):
            lista_respostas.append(resposta.get("resposta"))
        


    return render_template("listarespostas.html", foto=foto, lista_respostas=lista_respostas)