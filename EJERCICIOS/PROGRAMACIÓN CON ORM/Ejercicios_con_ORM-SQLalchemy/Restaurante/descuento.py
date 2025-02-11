def aplicar_descuento(pedido, porcentaje_descuento):
    descuento = pedido.total * (porcentaje_descuento / 100)
    pedido.total -= descuento
    return pedido.total
