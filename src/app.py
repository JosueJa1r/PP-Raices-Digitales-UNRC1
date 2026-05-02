import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_cors import CORS
from src.bd import registrar_productor, login_productor
from src.ia.bot import generar_respuesta_bot

# Cargar variables de entorno (API Keys)
load_dotenv()

# Inicializar Flask (sólo como API Backend)
app = Flask(__name__)
# Habilitar CORS para permitir peticiones desde el frontend (puerto 5501)
CORS(app)

@app.route('/api/chat', methods=['POST'])
def chat_bot_route():
    try:
        data = request.get_json()
        user_message = data.get('message', '')
        
        reply = generar_respuesta_bot(user_message)
        return jsonify({"reply": reply})
        
    except Exception as e:
        print("Error en RaícesBot IA:", e)
        return jsonify({"error": str(e) or "Hubo un problema al conectar con la IA. Intenta de nuevo más tarde."}), 500

@app.route('/api/register/productor', methods=['POST'])
def register_productor_route():
    try:
        data = request.get_json()
        nombre = data.get('nombre')
        correo = data.get('correo')
        password = data.get('password')
        hectareas = data.get('terreno')
        filtros = data.get('filtros')
        
        result = registrar_productor(nombre, correo, password, hectareas, filtros)
        
        if result['success']:
            return jsonify({"message": "Registro exitoso", "id_productor": result['id_productor']}), result['status']
        else:
            return jsonify({"error": result['error']}), result['status']
            
    except Exception as e:
        print("Error en ruta registro:", e)
        return jsonify({"error": "Error interno del servidor"}), 500

@app.route('/api/login/productor', methods=['POST'])
def login_productor_route():
    try:
        data = request.get_json()
        correo = data.get('correo')
        password = data.get('password')
        
        result = login_productor(correo, password)
        
        if result['success']:
            return jsonify({"message": "Login exitoso", "user": result['user']}), result['status']
        else:
            return jsonify({"error": result['error']}), result['status']
            
    except Exception as e:
        print("Error en ruta login:", e)
        return jsonify({"error": "Error interno del servidor"}), 500

if __name__ == '__main__':
    # Inicia el servidor local en el puerto 5000
    app.run(debug=True, port=5000)

