from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import login_required, login_user, logout_user, current_user
from grocery_app.extensions import bcrypt
from grocery_app.models import GroceryStore, GroceryItem, User
from grocery_app.forms import GroceryStoreForm, GroceryItemForm, SignUpForm, LoginForm, DeleteForm

# Import app and db from events_app package so that we can run app
from grocery_app.extensions import app, db

main = Blueprint("main", __name__)

auth = Blueprint("auth", __name__)

##########################################
#           Routes                       #
##########################################

@main.route('/')
def homepage():
    all_stores = GroceryStore.query.all()
    return render_template('home.html', all_stores=all_stores)

@main.route('/new_store', methods=['GET', 'POST'])
@login_required
def new_store():
    form = GroceryStoreForm()
    
    if form.validate_on_submit():
        new_store = GroceryStore(
            title=form.title.data,
            address=form.address.data,
            created_by=current_user
        )
        db.session.add(new_store)
        db.session.commit()

        flash('New store created!')
        return redirect(f'/store/{new_store.id}')

    return render_template('new_store.html', form=form)

@main.route('/new_item', methods=['GET', 'POST'])
@login_required
def new_item():
    form = GroceryItemForm()
    
    if form.validate_on_submit():
        new_item = GroceryItem(
            name=form.name.data,
            price=form.price.data,
            category=form.category.data,
            photo_url=form.photo_url.data,
            store_id=form.store.data.id,
            created_by=current_user
        )
        db.session.add(new_item)
        db.session.commit()

        flash('New item added succesfully.')

    return render_template('new_item.html', form=form)

@main.route('/store/<store_id>', methods=['GET', 'POST'])
@login_required
def store_detail(store_id):
    store = GroceryStore.query.get(store_id)
    form = GroceryStoreForm(obj=store)

    if form.delete.data:
        GroceryStore.query.filter_by(id=store_id).delete()
        db.session.commit()
        return redirect('/')

    if form.validate_on_submit():
        store.title = form.title.data
        store.address = form.address.data
        
        db.session.add(store)
        db.session.commit()

        flash('Store information updated succesfully.')

    return render_template('store_detail.html', store=store, form=form)

@main.route('/item/<item_id>', methods=['GET', 'POST'])
@login_required
def item_detail(item_id):
    item = GroceryItem.query.get(item_id)
    form = GroceryItemForm(obj=item)
    
    if form.delete.data:
        GroceryItem.query.filter_by(id=item_id).delete()
        db.session.commit()
        return redirect('/')
    
    if form.validate_on_submit():
        item.name = form.name.data
        item.price = form.price.data
        item.category = form.category.data
        item.photo_url = form.photo_url.data
        item.store_id = form.store.data.id
        
        db.session.add(item)
        db.session.commit()

        flash('Item edited succesfully')
 
    return render_template('item_detail.html', item=item, form=form)

@main.route('/add_to_shopping_list/<item_id>', methods=['POST'])
def add_to_shopping_list(item_id):
    user = current_user
    item = GroceryItem.query.get(item_id)
    user.shopping_list_items.append(item)
    
    db.session.add(user)
    db.session.commit()

    return redirect(url_for('main.shopping_list'))

@main.route('/shopping_list', methods=['GET', 'POST'])
@login_required
def shopping_list():
    user = current_user
    user_item_list = user.shopping_list_items
    forms = {}
    for item in user_item_list:
        forms[f'{item.id}'] = DeleteForm()

    for form in forms.values():
        if form.delete.data:
            item_id = int(form.item_id.data)
            item = GroceryItem.query.get(item_id)
        
            user.shopping_list_items.remove(item)
            db.session.add(user)
            db.session.commit()

            return render_template('shopping_list.html', user=current_user, forms=forms)

    return render_template('shopping_list.html', user=current_user, forms=forms)

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()
    
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(
            username=form.username.data,
            password=hashed_password
        )
        db.session.add(user)
        db.session.commit()
        flash('Account Created.')
        print('created')
        return redirect(url_for('auth.login'))
    
    return render_template('signup.html', form=form)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        login_user(user, remember=True)
        next_page = request.args.get('next')
        return redirect(next_page if next_page else url_for('main.homepage'))
    return render_template('login.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.homepage'))
