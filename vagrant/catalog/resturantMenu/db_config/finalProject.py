import logging
from flask import Flask,render_template,request,flash,redirect,url_for,jsonify
app = Flask(__name__)

##mock database

#Fake Restaurants
restaurant = {'name': 'The CRUDdy Crab', 'id': '1'}

restaurants = [{'name': 'The CRUDdy Crab', 'id': '1'}, {'name':'Blue Burgers', 'id':'2'},{'name':'Taco Hut', 'id':'3'}]


#Fake Menu Items
items = [ {'name':'Cheese Pizza', 'description':'made with fresh cheese', 'price':'$5.99','course' :'Entree', 'id':'1'}, {'name':'Chocolate Cake','description':'made with Dutch Chocolate', 'price':'$3.99', 'course':'Dessert','id':'2'},{'name':'Caesar Salad', 'description':'with fresh organic vegetables','price':'$5.99', 'course':'Entree','id':'3'},{'name':'Iced Tea', 'description':'with lemon','price':'$.99', 'course':'Beverage','id':'4'},{'name':'Spinach Dip', 'description':'creamy dip with fresh spinach','price':'$1.99', 'course':'Appetizer','id':'5'} ]
item =  {'name':'Cheese Pizza','description':'made with fresh cheese','price':'$5.99','course' :'Entree','id':'1'}

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Restaurant, Base, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/restaurants/JSON')
def restaurantsJSON():
    restaurants = session.query(Restaurant).all()
    return jsonify(Restaurant=[restaurant.serialize for restaurant in restaurants])

@app.route('/restaurant/<int:restaurant_id>/menu/JSON')
def restaurantMenuJSON(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(
        restaurant_id=restaurant_id).all()
    return jsonify(MenuItems=[i.serialize for i in items])

@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/JSON')
def restaurantMenuItemJSON(restaurant_id,menu_id):
    menuItem = session.query(MenuItem).filter_by(
        id=menu_id).one()
    return jsonify(MenuItems=menuItem.serialize)

@app.route('/')
@app.route('/restaurants/')
def showRestaurants():
	#return "This page will show all my restaurants"
    restaurants = session.query(Restaurant).all()
    return render_template("restaurants.html",restaurants = restaurants)

@app.route('/restaurant/new',methods=['GET', 'POST'])
def newRestaurant():
    #return "This page will be for makeing newrestaurants"
    if request.method == 'POST':
        newRestaurant = Restaurant(name=request.form['name'])
        session.add(newRestaurant)
        session.commit()
        flash("new restaurant created")
        return redirect(url_for('showRestaurants'))
    else:
        return render_template('newRestaurant.html')

@app.route('/restaurant/<int:restaurant_id>/edit',methods=['GET', 'POST'])
def editRestaurant(restaurant_id):
    app.logger.warning("came in edit restaurant")
    editedRestaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    if request.method == 'POST':
        app.logger.warning("came in post edit restaurant")
        if(request.form['name']):
           editedRestaurant.name = request.form['name']
        session.add(editedRestaurant)
        session.commit()
        flash("restaurant details edited")
        return redirect(url_for('showRestaurants'))
    else:
        return render_template('editRestaurant.html',restaurant = editedRestaurant)

@app.route('/restaurant/<int:restaurant_id>/delete',methods=['GET', 'POST'])
def deleteRestaurant(restaurant_id): 
    #return "This page is for deleting restaurant %s" % restaurant_id
    #restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    if request.method == 'POST':
        newRestaurant = Restaurant(name=request.form['name'])
        session.delete(newRestaurant)
        session.commit()
        flash("restaurant deleted")
        return redirect(url_for('showRestaurants'))
    else:
        return render_template('deleteRestaurant.html',restaurant = restaurant)    

@app.route('/restaurant/<int:restaurant_id>')
@app.route('/restaurant/<int:restaurant_id>/menu')
def showMenu(restaurant_id):
    #return "This page is for viewing restaurant %s all menu items"% restaurant_id 
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id = restaurant.id).all()
    app.logger.warning(items)
    return render_template('menu.html',restaurant=restaurant,items=items)

@app.route('/restaurant/<int:restaurant_id>/menu/new',methods=['GET', 'POST'])
def newMenuItem(restaurant_id):
    #return "This is to add new menu item to restaurant %s" % restaurant_id
    if request.method == 'POST':
        newItem = MenuItem(name=request.form['name'], description=request.form[
                           'description'], price=request.form['price'], course=request.form['course'], restaurant_id=restaurant_id)
        session.add(newItem)
        session.commit()
        flash("new menu item created")
        return redirect(url_for('showMenu', restaurant_id=restaurant_id))
    else:
        return render_template('newmenuitem.html', restaurant_id=restaurant_id)    

@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/edit',methods=['GET', 'POST'])
def editMenuItem(restaurant_id,menu_id):
    #return "This is to edit a menu item %s in %s restaurant" % (menu_id,restaurant_id)
    editedItem = session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method == 'POST':
        oldName = editedItem.name
        if request.form['name']:
            editedItem.name = request.form['name']
        session.add(editedItem)
        session.commit()
        flash("menu item %s was updated to %s" % (oldName,editedItem.name))
        return redirect(url_for('showMenu', restaurant_id=restaurant_id))
    else:
        # USE THE RENDER_TEMPLATE FUNCTION BELOW TO SEE THE VARIABLES YOU
        # SHOULD USE IN YOUR EDITMENUITEM TEMPLATE
        return render_template(
            'editmenuitem.html', restaurant_id=restaurant_id, MenuID= menu_id, item=editedItem)    

@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete',methods=['GET', 'POST'])
def deleteMenuItem(restaurant_id,menu_id):
    #return "This page is to delete a menu item %s from restaurant %s" % (menu_id,restaurant_id)
    #if we dont specify one it returns a list of objects instead of one.
    itemToDelete = session.query(MenuItem).filter_by(id = menu_id).one()
    if request.method == 'POST':
        session.delete(itemToDelete)
        session.commit()
        flash("menu item %s was deleted" % itemToDelete.name)
        return redirect(url_for('showMenu', restaurant_id=restaurant_id))
    else:
        # USE THE RENDER_TEMPLATE FUNCTION BELOW TO SEE THE VARIABLES YOU
        # SHOULD USE IN YOUR EDITMENUITEM TEMPLATE
        return render_template('deleteMenuItem.html', restaurant_id=restaurant_id, item=itemToDelete)    

if __name__ == '__main__':
    app.secret_key = 'super secret key'
	#this reloads  flask everytime it detects code change
    app.debug = True
	#host = '0.0.0.0' this signifies to listen on all ip address not only localhost
    app.run(host = '0.0.0.0',port = 5000)