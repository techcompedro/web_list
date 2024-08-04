from flask import Flask, render_template, request, redirect
from database import Lista, session

app = Flask(__name__)

@app.route('/')
def lista():
    lista = session.query(Lista).all()
    return render_template('index.html', lista=lista)

@app.route('/salvar_lista', methods=['POST'])
def salvar_lista():
    nova_lista = Lista(
        lista = request.form['lista']
    )
    session.add(nova_lista)
    session.commit()
    return redirect('/')




@app.route('/editar_lista',  methods=['POST'])
def editar():
    lista_id  = request.form['id']
    list = session.query(Lista).get(lista_id)
    if list:
        list.lista = request.form['lista']
        session.commit()
    return redirect('/')

@app.route('/delete', methods=['POST'])
def delete():
    lista = request.form['lista']
    lista_id = session.query(Lista).filter_by(lista=lista).first()
    if  lista_id:
        session.delete(lista_id)
        session.commit()
    return redirect('/')
    
@app.route('/check', methods=['POST'])
def check():
    lista_id = request.form['id']
    list = session.query(Lista).get(lista_id)
    if list:
        list.feita = 'feita' in request.form
        session.commit()
   
    session.rollback()
    return redirect('/')

    
        







        


if __name__ == '__main__':
    app.run(debug=True)