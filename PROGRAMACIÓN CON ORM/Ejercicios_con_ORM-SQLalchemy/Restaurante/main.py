from producto import Producto, Session
from pedido import Pedido, PedidoProducto
from descuento import aplicar_descuento
from factura import generar_factura
from api import consultar_pedido
from reporte import generar_reporte


def main():
    session = Session()

    # Crear productos
    producto1 = Producto(nombre="Pizza margarita", tipo="plato", precio="8.5")
    producto2 = Producto(nombre="Coca Cola", tipo="bebida", precio="1.5")

    session.add_all([producto1, producto2])
    session.commit()

    # Crear pedido
    pedido = Pedido(cliente="Raquel Martinez")
    session.add(pedido)
    session.commit()

    # Agregar productos al pedido
    pedido_producto1 = PedidoProducto(
        pedido_id=pedido.id, producto_id=producto1.id, cantidad=1
    )
    pedido_producto2 = PedidoProducto(
        pedido_id=pedido.id, producto_id=producto2.id, cantidad=2
    )
    session.add_all([pedido_producto1, pedido_producto2])
    pedido.calcularTotal()
    session.commit()

    # Aplicar descuento
    aplicar_descuento(pedido, 10)
    session.commit()

    # Generar factura
    print(generar_factura(pedido))

    # COnsultar pedido via API
    print(consultar_pedido("Raquel Martinez"))

    # Generar el reporte PDF
    generar_reporte("reporte_pedidos.pdf")
    print("Reporte generado ")


if __name__ == "__main__":
    main()
