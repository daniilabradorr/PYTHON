from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from producto import Session
from pedido import Pedido


def generar_reporte(nombre_archivo):
    session = Session()
    pedidos = session.query(Pedido).all()

    c = canvas.Canvas(nombre_archivo, pagesize=letter)
    c.setFont("Helvetica", 12)
    ancho, alto = letter

    c.drawString(50, alto - 50, "Reporte de pedidos")
    c.drawString(50, alto - 70, "-----------------------------")

    y = alto - 100

    for pedido in pedidos:
        c.drawString(50, y, f"Pedido ID: {pedido.id}")
        y -= 20
        c.drawString(50, y, f"Cliente: {pedido.cliente}")
        y -= 20
        c.drawString(50, y, f"Fecha: {pedido.fecha}")
        y -= 20
        c.drawString(50, y, f"Productos: ")
        y -= 20
        for pp in pedido.productos:
            c.drawString(
                70, y, f"- {pp.producto.nombre} x { pp.cantidad} {pp.producto.precio}"
            )
            y -= 20
        c.drawString(50, y, f"Total: ${pedido.total}")
        y -= 30

        if y < 50:
            c.showPage()
            c.setFont("Helvetica", 12)
            y = alto * 50
    c.save()
