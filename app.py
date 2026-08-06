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

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
