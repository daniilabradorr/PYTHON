#ENLAZAR LOS PEDIDOS CON LOS PRODUCTOS.

#Importación de todo lo necesario.
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from datetime import datetime
from producto import Base, engine

# Definición del modelo de la clase 'Pedido'
class Pedido(Base):
    __tablename__ = "pedidos"
    id = Column(Integer, primary_key=True, autoincrement=True)
    cliente = Column(String(255), nullable=False)
    fecha = Column(DateTime, default=datetime.utcnow)
    productos = relationship("PedidoProducto", back_populates= "pedido")
    total = Column(Float, nullable=False, default= 0.0)

    def calculartotal(self):
        self.total = sum(pp.producto.precio * pp.cantidad for pp in self.productos)

class PedidoProducto(Base):
    __tablename__ = "pedido_producto"
    id = Column(Integer, primary_key=True, autoincrement=True)
    pedido_id = Column(Integer, ForeignKey("pedidos.id"))
    producto_id = Column(Integer, ForeignKey("productos.id"))
    cantidad = Column(Integer, nullable=False, default=1)

    pedido = relationship("Pedido", back_populates="productos")
    producto = relationship("Producto", back_populates="pedidos")

Base.metadata.create_all(engine)