from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def inicio():
    # Obtiene la dirección IP desde donde se hace la petición
    ip_cliente = request.remote_addr 
    
    return render_template(
        'index.html', 
        titulo="Centro de Biotecnología Agropecuaria",
        ip=ip_cliente
    )

@app.route('/version')
def version():
    return "<h2>Bienvenido - Deploy verificado: contenedor ha sido activado v2</h2>"

if __name__ == '__main__':
    # debug=False evita B201 | # nosec B104 evita la alerta de host 0.0.0.0
    app.run(debug=False, host='0.0.0.0', port=5000)  # nosec B104