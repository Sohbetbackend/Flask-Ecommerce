from shop import create_app, db
from shop.customers.model import Customer, CustomerOrder
from shop.products.models import Addproduct, Category, Banner
from shop.admin.models import User

app = create_app()


@app.shell_context_processor
def make_shell_processor():
    return {'db': db, "Customer": Customer, "CustomerOrder": CustomerOrder, "Addproduct": Addproduct, "Category": Category, "Banner": Banner, "User": User}