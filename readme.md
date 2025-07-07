# Sistema de Verificación de Integridad de Archivos con SHA-256 y Sellado de Tiempo

Este proyecto implementa un sistema en Python con interfaz web para calcular y visualizar paso a paso el algoritmo criptográfico **SHA-256** hecho desde cero, registrar la integridad de archivos y aplicar un sellado de tiempo básico para verificar la autenticidad de los datos.
---

## 🔍 Características principales

- ✅ Implementación del algoritmo **SHA-256 desde cero** (sin usar `hashlib`).
- 🔄 **Visualización paso a paso** del proceso interno del hash (valores a, b, c... h).
- 📂 Soporte para entrada de **texto y archivos**.
- 🕒 Registro de **timestamp** al generar cada hash.
- 🌐 Interfaz web moderna y responsiva usando **Flask** y **Bootstrap 5.3** con navegación entre pasos.
- 💾 Validación de tamaño máximo para archivos en modo paso a paso **(500 KB)**.

---

## 🧠 Estructura del proyecto

```
├── sha256.py             # Código principal con Flask y SHA-256 manual
├── templates/
│   └── index.html        # Interfaz web (Jinja2 + HTML + Bootstrap 5.3)
├── uploads/              # Carpeta para archivos temporales subidos
├── history.json          # Historial de entradas procesadas
└── README.md             # Este archivo
```

---

## 📦 Requisitos

- Python 3.7+
- Flask (`pip install flask`)

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
   pip install flask-session
   ```

3. Ejecuta la aplicación:
   ```bash
   python sha256.py
   ```

4. Abre tu navegador y visita:
   ```
   http://localhost:5000
   ```

---

## Uso

- Ingresa texto o selecciona un archivo para calcular su hash SHA-256.
- Activa el **modo visual paso a paso** para ver el proceso interno del algoritmo.
- En modo paso a paso el tamaño máximo permitido es 500 KB.
- Consulta el historial de hashes calculados con timestamps.

---

## Notas

- El modo oscuro está activado por defecto y puedes alternarlo con el botón en la interfaz, gracias al soporte nativo de Bootstrap 5.3.
- El sistema guarda el historial localmente en `history.json` para consultas posteriores.
- El algoritmo SHA-256 está implementado manualmente para fines educativos y visualización detallada.

---

## 🚀 Verificación

- Uso de la librería hashlib para verificar hash correcto:
   ```bash
   python sha256_verif.py
   ```

---

## 📘 Referencia de algoritmo

El algoritmo base fue adaptado del repositorio [Keanemind/python-sha-256](https://github.com/keanemind/python-sha-256) con modificaciones para soporte binario, visualización y registro.

Si quieres contribuir o reportar errores, ¡bienvenido!  
Para dudas o sugerencias, abre un issue en el repositorio.

---
