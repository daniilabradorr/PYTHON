def generar_factura(pedido):
    factura = f"Factura: \nCliente: {pedido.cliente}:\n"
    for pp in pedido.productos:
        factura += f"1. {pp.producto.nombre}: {pp.producto.precio} * {pp.cantidad}\n"

    factura += f"Total: {pedido.total}"
    return factura
