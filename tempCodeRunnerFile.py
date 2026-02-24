from flask import Flask, render_template, request, redirect, url_for, flash
from models import db, CafeItem

app = Flask(__name__)

# --- Configuration ---
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafe.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'cafe_secret_key_2026'

db.init_app(app)

# สร้างตารางใน Database อัตโนมัติ (จะสร้างไฟล์ cafe.db ในโฟลเดอร์ instance)
with app.app_context():
    db.create_all()

# --- ROUTES (10+ Pages) ---

@app.route('/')
def home():
    # หน้าที่ 1: Home - แสดงเมนูแนะนำ 3 อย่าง
    featured = CafeItem.query.limit(3).all()
    return render_template('index.html', items=featured)

@app.route('/menu')
def menu_all():
    # หน้าที่ 2: All Menu
    items = CafeItem.query.all()
    return render_template('menu.html', items=items, title="All Menu")

@app.route('/menu/beverages')
def menu_beverages():
    # หน้าที่ 3: Beverages
    items = CafeItem.query.filter(CafeItem.category.in_(['Coffee', 'Tea', 'Non-Coffee'])).all()
    return render_template('menu.html', items=items, title="Beverages")

@app.route('/menu/bakery')
def menu_bakery():
    # หน้าที่ 4: Bakery & Snacks
    items = CafeItem.query.filter_by(category='Bakery').all()
    return render_template('menu.html', items=items, title="Bakery & Snacks")

@app.route('/menu/<int:item_id>')
def item_detail(item_id):
    # หน้าที่ 5: Product Detail (Dynamic Route)
    item = CafeItem.query.get_or_404(item_id)
    return render_template('detail.html', item=item)

@app.route('/about')
def about():
    # หน้าที่ 6: About Us
    return render_template('about.html')

@app.route('/gallery')
def gallery():
    # หน้าที่ 7: Gallery
    return render_template('gallery.html')

@app.route('/contact')
def contact():
    # หน้าที่ 8: Contact
    return render_template('contact.html')

@app.route('/promotions')
def promotions():
    # หน้าที่ 9: Promotions
    return render_template('promotions.html')

# --- ADMIN SECTION ---

@app.route('/admin/add', methods=['GET', 'POST'])
def add_item():
    # หน้าที่ 10: Admin Add Item
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
        flash(f'เพิ่มเมนู "{new_item.name}" สำเร็จแล้ว!', 'success')
        return redirect(url_for('manage_menu'))
    return render_template('add_item.html')

@app.route('/admin/manage')
def manage_menu():
    # หน้าที่ 11 (แถม): Admin Manage Dashboard
    items = CafeItem.query.all()
    return render_template('manage.html', items=items)

@app.route('/admin/delete/<int:item_id>')
def delete_item(item_id):
    # ฟังก์ชันเสริม: Delete Item
    item = CafeItem.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    flash(f'ลบรายการ "{item.name}" เรียบร้อยแล้ว', 'danger')
    return redirect(url_for('manage_menu'))

if __name__ == '__main__':
    app.run(debug=True)