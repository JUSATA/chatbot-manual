``markdown
# Chatbot Manual de Convivencia - I.E. Atanasio Girardot

## 🏫 Descripción
Chatbot interactivo y animado para consultar el Manual de Convivencia de la Institución Educativa Atanasio Girardot. 
Desarrollado con Flask (Python) y una interfaz moderna con colores institucionales (verde, blanco y rojo).

## ✨ Características
- 🤖 Interfaz conversacional intuitiva
- 🎨 Diseño animado con colores institucionales
- 📱 Responsive design para móviles y desktop
- ⚡ Respuestas en tiempo real
- 🔍 Base de conocimientos completa del manual
- 📊 Tipeo animado y efectos visuales

## 🛠️ Instalación

### Requisitos Previos
- Python 3.8 o superior
- pip (gestor de paquetes de Python)

### Pasos de Instalación

1. **Clonar o descargar el proyecto:**
   ```bash
   git clone [url-del-proyecto]
   cd chatbot_atanasio_girardot
   ```

2. **Crear entorno virtual (recomendado):**
   ```bash
   python -m venv venv
   
   # En Windows:
   venv\Scripts\activate
   
   # En Mac/Linux:
   source venv/bin/activate
   ```

3. **Instalar dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Ejecutar la aplicación:**
   ```bash
   python run.py
   ```
   
   O alternativamente:
   ```bash
   python app.py
   ```

5. **Abrir en navegador:**
   - Ir a: `http://localhost:5000`

## 🌐 Despliegue en Producción

### Heroku
```bash
# Instalar Heroku CLI y ejecutar:
heroku create chatbot-atanasio-girardot
git push heroku main
```

### PythonAnywhere
1. Subir archivos al servidor
2. Configurar web app con Flask
3. Establecer app.py como archivo principal

## 💡 Uso del Chatbot

### Preguntas Frecuentes que Puedes Hacer:
- "¿Cuáles son mis derechos como estudiante?"
- "¿Qué uniformes debo usar?"
- "¿Qué es una situación tipo II?"
- "¿Cómo funciona el gobierno escolar?"
- "¿Qué servicios ofrece el colegio?"
- "¿Cómo es el debido proceso?"
- "¿Qué es el servicio social estudiantil?"

### Funcionalidades:
- ✅ Botones de respuesta rápida
- ✅ Escritura natural y conversacional
- ✅ Respuestas contextuales
- ✅ Animaciones y efectos visuales
- ✅ Interfaz responsiva

## 🔧 Personalización

### Modificar Base de Conocimientos:
Editar el diccionario `KNOWLEDGE_BASE` en `app.py` para añadir más temas o respuestas.

### Cambiar Colores:
Modificar las variables CSS en el archivo `templates/chatbot.html`:
```css
:root {
    --primary-green: #0d7f3c;
    --light-green: #28a745;
    --primary-red: #dc2626;
    /* ... más colores */
}
```

### Añadir Logo Personalizado:
Reemplazar el ícono Font Awesome en la clase `.logo` por una imagen:
```html
<div class="logo">
    <img src="/static/images/logo_atanasio.png" alt="Logo" style="width: 40px; height: 40px;">
</div>
```

## 📞 Soporte Técnico
- 🏫 Institución: I.E. Atanasio Girardot
- 📧 Email: [email institucional]
- 🌐 Web: [sitio web institucional]

## 📄 Licencia
Este proyecto está desarrollado para uso exclusivo de la I.E. Atanasio Girardot.

## 🎯 Próximas Mejoras
- [ ] Integración con base de datos
- [ ] Sistema de analytics
- [ ] Más animaciones interactivas
- [ ] Modo nocturno
- [ ] Soporte para archivos adjuntos
- [ ] Integración con WhatsApp Business API
```

## 🔥 Script de Inicio Rápido (start.bat para Windows)

```batch
@echo off
echo ========================================
echo   Iniciando Chatbot Atanasio Girardot
echo ========================================
echo.

echo Activando entorno virtual...
call venv\Scripts\activate

echo.
echo Instalando dependencias...
pip install -r requirements.txt

echo.
echo Iniciando servidor Flask...
echo.
echo Abre tu navegador en: http://localhost:5000
echo.
echo Presiona Ctrl+C para detener el servidor
echo ========================================
python app.py

pause
```

## 🍎 Script de Inicio para Mac/Linux (start.sh)

```bash
#!/bin/bash

echo "========================================"
echo "  Iniciando Chatbot Atanasio Girardot"
echo "========================================"
echo

echo "Activando entorno virtual..."
source venv/bin/activate

echo
echo "Instalando dependencias..."
pip install -r requirements.txt

echo
echo "Iniciando servidor Flask..."
echo
echo "Abre tu navegador en: http://localhost:5000"
echo
echo "Presiona Ctrl+C para detener el servidor"
echo "========================================"
python app.py