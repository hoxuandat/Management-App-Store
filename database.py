import sqlalchemy as sa
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Float, DateTime
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql import func


### Tao doi tuong engine ket noi voi database SQLite supermarket.db####
engine = sa.create_engine('sqlite:///supermarket.db')


### Tao base class cho cac model####
Base = declarative_base()



                        ############## DINH NGHIA CAC MODEL################

#### Dinh nghia model cho Product
class Product(Base):
    __tablename__ = 'products'
    id = sa.Column(sa.Integer, primary_key = True)
    name = sa.Column(sa.String(100), nullable = False )
    price = sa.Column(sa.Integer, nullable = False)
    quantity = sa.Column(sa.Integer, nullable = False, default = 1)
    ### Quan he voi bang OrderItem
    order_items = relationship("OrderItem", back_populates = "product")

#### Dinh nghia model cho Customer
class Customer(Base):
    __tablename__ = 'customers'
    id =sa.Column(sa.Integer, primary_key = True)
    name = sa.Column(sa.String(100), nullable = False )
    phone = sa.Column(sa.String(20), nullable = False )
    address = sa.Column(sa.String(100), nullable = False)
    total_purchase = sa.Column(sa.Integer, nullable = False, default = 0)
    order_count = sa.Column(sa.Integer, nullable = False, default = 0)
    ### Quan he voi bang Order
    order = relationship("Order", back_populates = "customer")

### Dinh nghia model cho Order
class Order(Base):
    __tablename__ = 'orders'
    id = sa.Column(sa.Integer, primary_key = True)
    customer_id = sa.Column(sa.Integer, sa.ForeignKey('customers.id'), nullable = False)
    total = sa.Column(sa.Integer, nullable = False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    ### Quan he voi bang Customer va OrderItem
    customer = relationship("Customer", back_populates = "order")
    order_items = relationship("OrderItem", back_populates = "order")



### Dinh nghia model cho Staff
class Staff(Base):
    __tablename__ = 'staff'
    id = sa.Column(sa.Integer, primary_key = True)
    name = sa.Column(sa.String(100), unique = True, nullable = False)
    password = sa.Column(sa.String(100), nullable = False)



###Dinh nghia model cho OrderItem
class OrderItem(Base):
    __tablename__ = 'order_items'
    id = sa.Column(sa.Integer, primary_key = True)
    order_id = sa.Column(sa.Integer, sa.ForeignKey('orders.id'), nullable = False)
    product_id = sa.Column(sa.Integer, sa.ForeignKey('products.id'), nullable = False)
    quantity = sa.Column(sa.Integer, nullable = False, default = 1)
    ### Quan he voi bang Order va bang Product
    order = relationship("Order", back_populates = "order_items")
    product = relationship("Product", back_populates = "order_items")




### Tao cac bang trong database
Base.metadata.create_all(engine)


### Tao session factory
Session = sessionmaker(bind = engine)

# --- Hàm get_session ---
def get_session():
    """Trả về một session SQLAlchemy."""
    return Session()



    session.commit()
    session.close()
