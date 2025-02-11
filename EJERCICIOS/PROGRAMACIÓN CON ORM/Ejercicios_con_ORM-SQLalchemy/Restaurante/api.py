from producto import Session
from pedido import Pedido


def consultar_pedido(cliente):
    session = Session()
    pedido = session.query(Pedido).filter_by(cliente=cliente).first()
    if pedido:
        return {
            "cliente": pedido.cliente,
            "productos": [pp.producto.nombre for pp in pedido.productos],
            "Total": pedido.total,
        }
    return {"error": "pedido no encontrado"}
