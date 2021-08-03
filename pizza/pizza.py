from flask import Flask, render_template,request,jsonify

app = Flask(__name__)

class Item:
    def __init__(self,title,name,type,value=''):
        self.title = title
        self.name=name
        self.type=type
        self.value = title.lower() if  value == '' else value
class Order:
    def __init__(self,membership,size,drink,topping,subtotal,gst,total):
        self.membership = membership
        self.size = size
        self.drink=drink
        self.topping = topping
        self.subtotal = subtotal
        self.gst = gst
        self.total = total
    price = {
        'member':0.8,
        'non-member':1,
        'topping':3,
        'drink':5,
        'size':{
            'large':15,
            'medium':12,
            'small':10
        }
    }
    def calPrice(self):
        drinkOrder = len(self.drink)*self.price['drink'] 
        toppingOrder = len(self.topping)*self.price['topping'] 
        size = self.size[0] if self.size else 0
        pizzaOrder = self.price['size'].get(size) if size!=0 else 0
        membership = self.membership[0] if self.membership else 'non-member'
        subtotal = (drinkOrder + toppingOrder + pizzaOrder) * self.price.get(membership)
        self.subtotal = subtotal
        self.gst = subtotal*0.13
        self.total = self.subtotal+self.gst

CATEGORIES = ['membership','size','drink','topping','subtotal','gst','total']
def getOrderObj(alist):
    orderList=[]
    for i in alist:
        data =  request.form.getlist(i)
        orderList.append(data)
    orderObj = Order(*orderList)
    return orderObj

@app.route('/', methods=['POST','GET'])
def pizza():
    memberShipList = [['Member','membership','radio'],['Non-Member','membership','radio']]
    sizeList = [['Large','size','radio'],['Medium','size','radio'],['Small','size','radio']]
    drinkList = [['Fizzy Drink','drink','checkbox'],['Regular Coffee','drink','checkbox'],
                ['Cappuccino','drink','checkbox'],['Tea','drink','checkbox']]
    toppingList = [['Extra Cheese','topping','checkbox'],['Pepperoni','topping','checkbox'],
                ['Bacon','topping','checkbox'],['Seafood','topping','checkbox'],['Vegetables','topping','checkbox']]
    priceList = [['Subtotal','subtotal','text',0],['GST','gst','text',0],['Total','total','text',0]]
    formData={
        'MemberShip':[Item(*i) for i in memberShipList],
        'Pick Your Size':[Item(*i) for i in sizeList],
        'Pick Your Drink':[Item(*i) for i in drinkList],
        'Pick Your Toppings':[Item(*i) for i in toppingList],
        'Price':[Item(*i) for i in priceList]
    }  
    if request.method=='POST':
        order = getOrderObj(CATEGORIES)
        print(order)
        return "The other page for payment."

    return render_template('pizza.html',formData = formData )

@app.route('/price',methods=['POST'])
def price():
    order = getOrderObj(CATEGORIES)
    order.calPrice()
    price =  {'Subtotal':order.subtotal,'GST':order.gst,'Total':order.total}
    return jsonify(price)

if __name__ == '__main__':
    app.run(debug=True)