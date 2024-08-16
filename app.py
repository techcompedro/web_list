from flask import Flask, render_template, request, redirect
from database import Lista, session, func, extract
import datetime as dt 
app = Flask(__name__)


@app.route('/')
def index ():
    if request.method == 'POST':
        data_str = request.form.get('data')  # Recebe a data do formulário como string
        data_obj = dt.strptime(data_str, '%Y-%m-%d').date()
    else:
        data_obj = None  # Defina um valor padrão se a data não for enviada

        # Total de tarefas
    all_items = session.query(Lista).all()
    total = len(all_items)

    # Tarefas pendentes e feitas
    contagem_feita_true = session.query(func.count(Lista.feita)).filter(Lista.feita == True).scalar()
    contagem_feita_false = session.query(func.count(Lista.feita)).filter(Lista.feita == False).scalar()

    return render_template('index.html', lista=all_items, total=total, feita_false=contagem_feita_false, feita_true=contagem_feita_true)



@app.route('/exibir_lista', methods=['GET', 'POST'])
def exibir_listaa():
    listas_hoje = session.query(Lista).filter(
        extract('day', Lista.data) == dt.date.today().day,
        extract('month', Lista.data) == dt.date.today().month,
        extract('year', Lista.data) == dt.date.today().year
    ).all()
    
    if request.method == 'POST':
        lista_selecionada = request.form.get('lista')  # Pegando o valor do dropdown
        
        if lista_selecionada == 'lista_hoje':
            lista = listas_hoje
        elif lista_selecionada == 'lista_mes':
            lista = session.query(Lista).filter(
                extract('month', Lista.data) == dt.date.today().month,
                extract('year', Lista.data) == dt.date.today().year
            ).all()
        elif lista_selecionada == 'lista_ano':
            lista = session.query(Lista).filter(
                extract('year', Lista.data) == dt.date.today().year
            ).all()
        else:
            lista = []

        return render_template('index.html', lista=lista)

    

@app.route('/adicionar_lista', methods=['POST'])
def addlista():
    data_str = request.form['data']
    data_obj = dt.strptime(data_str, '%Y-%m-%d').date()
    nova_lista = Lista(
        lista=request.form['lista'],
        descricao=request.form['descricao'],
        data=data_obj
    )
    session.add(nova_lista)
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