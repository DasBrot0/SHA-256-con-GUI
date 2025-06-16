# Sistema de Verificación de Integridad de Archivos con SHA-256 y Sellado de Tiempo

Este proyecto implementa un sistema en Python para calcular y visualizar paso a paso el algoritmo criptográfico SHA-256, registrar la integridad de archivos y aplicar un sellado de tiempo básico para verificar la autenticidad de los datos.

---

## 🔍 Características principales

- ✅ Implementación del algoritmo **SHA-256 desde cero** (sin `hashlib`).
- 🔄 **Visualización paso a paso** del proceso interno del hash (registros a, b, c... h).
- 📂 Soporte para **archivos y texto** como entrada.
- 🕒 Registro de **timestamp** al momento de generar cada hash.
- 💾 Historial local de verificaciones (`history.json`).
- 🌐 Interfaz web simple usando **Flask**.

---

## 🧠 Estructura del proyecto

```
├── sha256.py             # Lógica principal con Flask e implementación manual del algoritmo SHA-256
├── templates/
│   └── index.html        # Interfaz web (Jinja2 + HTML)
├── static/
│   └── css/style.css     # Estilos personalizados
├── uploads/              # Carpeta para archivos temporales subidos
├── history.json          # Historial de entradas procesadas
└── README.md             # Este archivo
```

---

## 🚀 Cómo ejecutar

1. Clona el repositorio:
   ```bash
   git clone https://github.com/DasBrot0/SHA-256-con-GUI.git
   cd PROYECTO
   ```

2. Instala Flask (si aún no lo tienes):
   ```bash
   pip install flask
   ```

3. Ejecuta la aplicación:
   ```bash
   python sha256.py
   ```

4. Abre tu navegador y ve a:
   ```
   http://localhost:5000
   ```

---

## 🚀 Verificación

- Uso de la librería hashlib para verificar hash correcto:
   ```bash
   python sha256_verif.py
   ```
---

## 📦 Requisitos

- Python 3.7+
- Flask

---

## 📘 Referencia de algoritmo

El código base del algoritmo SHA-256 fue adaptado del repositorio de [Keanemind](https://github.com/keanemind/python-sha-256) bajo fines educativos. Se modificó para incluir soporte binario, visualización y registro de historial.

---