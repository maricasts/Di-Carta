import os
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.middleware.proxy_fix import ProxyFix
from sqlalchemy.orm import DeclarativeBase
import logging
from datetime import datetime, date

# Configure logging for debugging
logging.basicConfig(level=logging.DEBUG)

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

# Create the Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dicarta-livraria-secret-key")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Configure the database
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}

# Initialize the app with the extension
db.init_app(app)

# Import models at module level
from models import Cliente, Tecnico, Livro, OrdemDeServico

with app.app_context():
    # Create all tables
    db.create_all()

@app.route('/')
def index():
    """Main landing page with user type selection"""
    return render_template('index.html')

@app.route('/cliente/register', methods=['GET', 'POST'])
def cliente_register():
    """Cliente registration page"""
    if request.method == 'POST':
        try:
            # Verificar se CPF já existe
            cpf = request.form['cpf'].replace('.', '').replace('-', '')
            existing_cliente = Cliente.query.filter_by(cpf=cpf).first()
            if existing_cliente:
                flash('CPF já cadastrado no sistema.', 'error')
                return render_template('cliente_register.html')
            
            cliente = Cliente(
                nome=request.form['nome'],
                cpf=cpf,
                telefone=request.form.get('telefone', ''),
                email=request.form.get('email', ''),
                cep=request.form.get('cep', ''),
                endereco=request.form.get('endereco', '')
            )
            
            db.session.add(cliente)
            db.session.commit()
            
            session['user_id'] = cliente.id
            session['user_type'] = 'cliente'
            session['user_name'] = cliente.nome
            flash('Cadastro realizado com sucesso!', 'success')
            return redirect(url_for('cliente_dashboard'))
        except Exception as e:
            db.session.rollback()
            app.logger.error(f"Erro ao cadastrar cliente: {str(e)}")
            flash('Erro ao realizar cadastro. Verifique os dados.', 'error')
    
    return render_template('cliente_register.html')

@app.route('/tecnico/register', methods=['GET', 'POST'])
def tecnico_register():
    """Tecnico registration page"""
    if request.method == 'POST':
        try:
            # Verificar se CPF já existe
            cpf = request.form['cpf'].replace('.', '').replace('-', '')
            existing_tecnico = Tecnico.query.filter_by(cpf=cpf).first()
            if existing_tecnico:
                flash('CPF já cadastrado no sistema.', 'error')
                return render_template('tecnico_register.html')
            
            tecnico = Tecnico(
                nome=request.form['nome'],
                cpf=cpf,
                status=request.form.get('status', 'Contratado'),
                valor_hora=float(request.form['valorHora']),
                carga_horaria=int(request.form['cargaHoraria'])
            )
            
            db.session.add(tecnico)
            db.session.commit()
            
            session['user_id'] = tecnico.id
            session['user_type'] = 'tecnico'
            session['user_name'] = tecnico.nome
            flash('Cadastro realizado com sucesso!', 'success')
            return redirect(url_for('tecnico_dashboard'))
        except Exception as e:
            db.session.rollback()
            app.logger.error(f"Erro ao cadastrar técnico: {str(e)}")
            flash('Erro ao realizar cadastro. Verifique os dados.', 'error')
    
    return render_template('tecnico_register.html')

@app.route('/cliente/dashboard')
def cliente_dashboard():
    """Cliente dashboard with book catalog"""
    if session.get('user_type') != 'cliente':
        return redirect(url_for('index'))
    
    books = [book.to_dict() for book in Livro.query.all()]
    return render_template('cliente_dashboard.html', books=books)

@app.route('/tecnico/dashboard')
def tecnico_dashboard():
    """Tecnico dashboard with management options"""
    if session.get('user_type') != 'tecnico':
        return redirect(url_for('index'))
    
    books = [book.to_dict() for book in Livro.query.all()]
    orders = [order.to_dict() for order in OrdemDeServico.query.all()]
    
    # Calculate sales statistics
    total_books = len(books)
    total_stock = sum(book.get('estoque', 0) for book in books)
    
    stats = {
        'total_books': total_books,
        'total_stock': total_stock,
        'total_orders': len(orders)
    }
    
    return render_template('tecnico_dashboard.html', stats=stats, books=books[:5], orders=orders[:5])

@app.route('/books')
def books_catalog():
    """Books catalog page for customers"""
    if session.get('user_type') != 'cliente':
        return redirect(url_for('index'))
    
    books = [book.to_dict() for book in Livro.query.all()]
    return render_template('books_catalog.html', books=books)

@app.route('/tecnico/books')
def book_management():
    """Book management page for technicians"""
    if session.get('user_type') != 'tecnico':
        return redirect(url_for('index'))
    
    books = [book.to_dict() for book in Livro.query.all()]
    return render_template('book_management.html', books=books)

@app.route('/tecnico/books/add', methods=['POST'])
def add_book():
    """Add a new book"""
    if session.get('user_type') != 'tecnico':
        return redirect(url_for('index'))
    
    try:
        livro = Livro(
            titulo=request.form['titulo'],
            autor=request.form['autor'],
            editora=request.form.get('editora', ''),
            ano=int(request.form['ano']) if request.form.get('ano') else None,
            genero=request.form.get('genero', ''),
            preco=float(request.form['preco']),
            estoque=int(request.form.get('estoque', 0))
        )
        
        db.session.add(livro)
        db.session.commit()
        flash('Livro adicionado com sucesso!', 'success')
    except Exception as e:
        db.session.rollback()
        app.logger.error(f"Erro ao adicionar livro: {str(e)}")
        flash('Erro ao adicionar livro.', 'error')
    
    return redirect(url_for('book_management'))

@app.route('/tecnico/books/update/<int:book_id>', methods=['POST'])
def update_book(book_id):
    """Update a book"""
    if session.get('user_type') != 'tecnico':
        return redirect(url_for('index'))
    
    try:
        livro = Livro.query.get_or_404(book_id)
        
        livro.titulo = request.form['titulo']
        livro.autor = request.form['autor']
        livro.editora = request.form.get('editora', '')
        livro.ano = int(request.form['ano']) if request.form.get('ano') else None
        livro.genero = request.form.get('genero', '')
        livro.preco = float(request.form['preco'])
        livro.estoque = int(request.form.get('estoque', 0))
        
        db.session.commit()
        flash('Livro atualizado com sucesso!', 'success')
    except Exception as e:
        db.session.rollback()
        app.logger.error(f"Erro ao atualizar livro: {str(e)}")
        flash('Erro ao atualizar livro.', 'error')
    
    return redirect(url_for('book_management'))

@app.route('/tecnico/books/delete/<int:book_id>', methods=['POST'])
def delete_book(book_id):
    """Delete a book"""
    if session.get('user_type') != 'tecnico':
        return redirect(url_for('index'))
    
    try:
        livro = Livro.query.get_or_404(book_id)
        db.session.delete(livro)
        db.session.commit()
        flash('Livro excluído com sucesso!', 'success')
    except Exception as e:
        db.session.rollback()
        app.logger.error(f"Erro ao excluir livro: {str(e)}")
        flash('Erro ao excluir livro.', 'error')
    
    return redirect(url_for('book_management'))

@app.route('/tecnico/orders')
def orders_management():
    """Orders management page for technicians"""
    if session.get('user_type') != 'tecnico':
        return redirect(url_for('index'))
    
    orders = [order.to_dict() for order in OrdemDeServico.query.all()]
    return render_template('orders_management.html', orders=orders)

@app.route('/tecnico/orders/add', methods=['POST'])
def add_order():
    """Add a new service order"""
    if session.get('user_type') != 'tecnico':
        return redirect(url_for('index'))
    
    try:
        ordem = OrdemDeServico(
            descricao=request.form['descricao'],
            status='ABERTA',
            data_abertura=datetime.now().date()
        )
        
        db.session.add(ordem)
        db.session.commit()
        flash('Ordem de serviço criada com sucesso!', 'success')
    except Exception as e:
        db.session.rollback()
        app.logger.error(f"Erro ao criar ordem de serviço: {str(e)}")
        flash('Erro ao criar ordem de serviço.', 'error')
    
    return redirect(url_for('orders_management'))

@app.route('/tecnico/orders/update/<int:order_id>', methods=['POST'])
def update_order(order_id):
    """Update a service order"""
    if session.get('user_type') != 'tecnico':
        return redirect(url_for('index'))
    
    try:
        ordem = OrdemDeServico.query.get_or_404(order_id)
        
        ordem.descricao = request.form['descricao']
        ordem.status = request.form['status']
        
        if request.form.get('dataFechamento'):
            ordem.data_fechamento = datetime.strptime(request.form['dataFechamento'], '%Y-%m-%d').date()
        
        db.session.commit()
        flash('Ordem de serviço atualizada com sucesso!', 'success')
    except Exception as e:
        db.session.rollback()
        app.logger.error(f"Erro ao atualizar ordem de serviço: {str(e)}")
        flash('Erro ao atualizar ordem de serviço.', 'error')
    
    return redirect(url_for('orders_management'))

@app.route('/cart')
def shopping_cart():
    """Shopping cart page"""
    if session.get('user_type') != 'cliente':
        return redirect(url_for('index'))
    
    cart_items = session.get('cart', [])
    total = sum(item['preco'] * item['quantity'] for item in cart_items)
    
    return render_template('shopping_cart.html', cart_items=cart_items, total=total)

@app.route('/cart/add/<int:book_id>')
def add_to_cart(book_id):
    """Add book to shopping cart"""
    if session.get('user_type') != 'cliente':
        return redirect(url_for('index'))
    
    # Get book details
    book = Livro.query.get(book_id)
    if book and book.estoque > 0:
        cart = session.get('cart', [])
        
        # Check if book already in cart
        for item in cart:
            if item['id'] == book_id:
                item['quantity'] += 1
                break
        else:
            cart.append({
                'id': book_id,
                'titulo': book.titulo,
                'autor': book.autor,
                'preco': float(book.preco),
                'quantity': 1
            })
        
        session['cart'] = cart
        flash(f'"{book.titulo}" adicionado ao carrinho!', 'success')
    else:
        flash('Livro indisponível no estoque.', 'error')
    
    return redirect(url_for('books_catalog'))

@app.route('/cart/remove/<int:book_id>')
def remove_from_cart(book_id):
    """Remove book from shopping cart"""
    if session.get('user_type') != 'cliente':
        return redirect(url_for('index'))
    
    cart = session.get('cart', [])
    cart = [item for item in cart if item['id'] != book_id]
    session['cart'] = cart
    
    flash('Item removido do carrinho!', 'success')
    return redirect(url_for('shopping_cart'))

@app.route('/logout')
def logout():
    """Logout user"""
    session.clear()
    flash('Logout realizado com sucesso!', 'success')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
