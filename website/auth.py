from flask import Blueprint, render_template, request, redirect, url_for, flash, session
import  requests
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
#from flask_login import login_user, logout_user, login_required, current_user

auth = Blueprint('auth', __name__)




url = 'https://apicrev3.azurewebsites.net/clientes'



@auth.route('/login', methods=["POST", "GET"])
def login():



    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        api=requests.get(url)


        user_exist=False

        for user in api.json():
            
            if user['emailCliente'] == email:
                user_exist = user
                break
            else:                        # se calhar esse else não é preciso
                user_exist = False   

        if user_exist:

            if user_exist['passwordCliente']== password:

                session["email"]=email
            
                requests.patch(url+'/'+email, json={})
                return redirect(url_for('views.home'))
            else:
                flash('Ver se palavra email ou palavra passe estão corretos', category='error')

        else:

            flash('Ver se palavra email ou palavra passe estão corretos', category='error')
            return render_template('login.html')

    else:
        if "email" in session:
            return redirect(url_for('views.home'))
        

    
  
    return render_template('login.html')


@auth.route("/signup", methods=["POST"])
def signup():


    nome = request.form.get('nome')
    email = request.form.get('email')
    password1 = request.form.get('password1')
    password2 = request.form.get('password2')
    #policy= request.form.get('policy')

    api=requests.get(url)

    user_exist=False

    for user in api.json():
        if user['emailCliente'] == email:
            user_exist = True
            break
        else:                        # se calhar esse else não é preciso
            user_exist = False

    

    if user_exist:
        flash('este email já foi usado!', category='error')

    else:
        dados={"nomeCliente": nome, "emailCliente": email,"passwordCliente": password1}

        if len(email)<7:
            flash('Email tem de ter pelo menos 7 caracteres!', category='error')
        elif len(password1)<6:
            flash('password tem de ter pelo menos 6 caracteres!', category='error')
        elif password1!=password2:
            flash('password tem de ser iguais!', category='error')
        # elif policy == None:
        #     flash(' Tem de aceitar termos e condições', category='error')
        else:
            api=requests.post(url, json=dados)
            flash('A conta fui criada com sucesso', category='success')
            session["email"]=email

            return redirect(url_for('views.home'))
    
    return redirect(url_for('views.login'))

   
    
@auth.route('/logout')
def logout():
    session.pop("email", None)
    return redirect(url_for('views.home'))

