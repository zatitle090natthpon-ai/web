from flask import Flask, render_template, request, redirect, url_for, flash
from models import db, CafeItem

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafe.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'matcha_secret_key_2026'

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/')
def home():
    featured = CafeItem.query.limit(3).all()
    return render_template('index.html', items=featured)

@app.route('/menu')
def menu_all():
    items = CafeItem.query.all()
    return render_template('menu.html', items=items, title="All Menu")

@app.route('/menu/beverages')
def menu_beverages():
    items = CafeItem.query.filter(CafeItem.category.in_(['Coffee', 'Tea'])).all()
    return render_template('menu.html', items=items, title="Beverages")

@app.route('/menu/bakery')
def menu_bakery():
    items = CafeItem.query.filter_by(category='Bakery').all()
    return render_template('menu.html', items=items, title="Bakery & Snacks")

@app.route('/item/<int:item_id>')
def item_detail(item_id):
    item = CafeItem.query.get_or_404(item_id)
    return render_template('detail.html', item=item)

@app.route('/about')
def about(): return render_template('about.html')

@app.route('/gallery')
def gallery(): return render_template('gallery.html')

@app.route('/contact')
def contact(): return render_template('contact.html')

@app.route('/promotions')
def promotions(): return render_template('promotions.html')

# --- ADMIN SECTION ---
@app.route('/admin/dashboard')
def admin_dashboard():
    total = CafeItem.query.count()
    coffee = CafeItem.query.filter_by(category='Coffee').count()
    tea = CafeItem.query.filter_by(category='Tea').count()
    bakery = CafeItem.query.filter_by(category='Bakery').count()
    recent = CafeItem.query.order_by(CafeItem.id.desc()).limit(5).all()
    return render_template('dashboard.html', total=total, coffee=coffee, tea=tea, bakery=bakery, recent=recent)

@app.route('/admin/manage')
def manage_menu():
    items = CafeItem.query.all()
    return render_template('manage.html', items=items)

@app.route('/admin/add', methods=['GET', 'POST'])
def add_item():
    if request.method == 'POST':
        new_item = CafeItem(
            name=request.form.get('name'),
            category=request.form.get('category'),
            price=request.form.get('price'),
            description=request.form.get('description'),
            image_url=request.form.get('image_url')
        )
        db.session.add(new_item)
        db.session.commit()
        flash('เพิ่มเมนูสำเร็จ!', 'success')
        return redirect(url_for('manage_menu'))
    return render_template('add_item.html')

@app.route('/admin/delete/<int:item_id>')
def delete_item(item_id):
    item = CafeItem.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    return redirect(url_for('manage_menu'))

if __name__ == '__main__':
    app.run(debug=True)