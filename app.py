from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import json
import re
from difflib import get_close_matches
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Base de conocimiento extraída del manual de convivencia
KNOWLEDGE_BASE = {
    "derechos_estudiantes": {
        "keywords": ["derechos", "derecho", "estudiante", "estudiantes", "tengo derecho"],
        "response": """**Derechos de los Estudiantes** 🎓

Los estudiantes de la I.E. Atanasio Girardot tienen derecho a:

• Recibir una educación integral que responda a las demandas del contexto
• Al respeto de su identidad, integridad y dignidad personal
• A no ser discriminado por orientación sexual, religiosa o ideológica
• A participar en la vida democrática de la institución
• Al debido proceso
• A conocer el sistema de evaluación institucional
• A ser evaluados objetivamente
• A solicitar un segundo evaluador si considera vulnerados sus derechos
• Conocer los resultados parciales y finales de cada asignatura
• Beneficiarse de todos los recursos y servicios institucionales

¿Te gustaría conocer más sobre algún derecho específico?"""
    },
    
    "deberes_estudiantes": {
        "keywords": ["deberes", "deber", "obligaciones", "responsabilidades", "que debo hacer"],
        "response": """**Deberes de los Estudiantes** 📋

Son deberes de los estudiantes:

• Acatar las disposiciones del manual de convivencia y PEI
• Respetar a las demás personas sin importar sus diferencias
• Seguir el conducto regular y debido proceso
• Evitar la violencia para solucionar conflictos
• Cuidar el medio ambiente y recursos institucionales
• Esforzarse por alcanzar la excelencia académica
• Presentar justificaciones oportunas por permisos o ausencias
• Entregar información institucional a padres o acudientes
• Asumir un comportamiento ético en todas sus actuaciones

¿Necesitas información sobre algún deber específico?"""
    },
    
    "uniformes": {
        "keywords": ["uniforme", "uniformes", "vestimenta", "ropa", "presentacion personal"],
        "response": """**Uniformes Institucionales** 👔👗

**Uniforme de Gala Masculino:**
• Pantalón clásico azul oscuro en lino
• Camisa colegial blanca (camiseta blanca por debajo)
• Correa negra en cuero
• Zapatos negros de cordones
• Medias azules oscuras
• Saco o chaqueta azul oscuro

**Uniforme de Gala Femenino:**
• Camisa blanca colegial de cuello sport
• Jomber a cuadros según modelo
• Short azul oscuro
• Medias blancas a la rodilla
• Zapatos negros de atadura
• Saco o chaqueta azul oscuro

**Uniforme de Educación Física:**
• Pantalón de sudadera azul oscuro con nombre de la institución
• Camiseta blanca con escudo institucional
• Tenis completamente blancos
• Medias blancas (no tobilleras)

¿Necesitas más detalles sobre algún uniforme?"""
    },
    
    "situaciones_tipo_1": {
        "keywords": ["situacion tipo 1", "tipo i", "falta leve", "conflicto", "problemas menores"],
        "response": """**Situaciones Tipo I** ⚠️

Corresponden a conflictos manejados inadecuadamente y situaciones esporádicas que afectan negativamente el clima escolar, sin generar daños al cuerpo o salud.

**Ejemplos:**
• Llegar tarde al aula de clase
• Interrumpir el desarrollo normal de las clases
• No atender orientaciones del docente
• Consumir alimentos en espacios no permitidos
• Usar aparatos electrónicos sin autorización
• Descuido en presentación personal

**Medidas Pedagógicas:**
• Diálogo con personas implicadas
• Registro en observador del alumno
• Actividades reflexivas
• Acciones de servicio social
• Presentar excusas a personas ofendidas
• Compromiso escrito de no reincidir

¿Te interesa conocer sobre situaciones Tipo II o III?"""
    },
    
    "situaciones_tipo_2": {
        "keywords": ["situacion tipo 2", "tipo ii", "falta grave", "agresion", "acoso", "bullying"],
        "response": """**Situaciones Tipo II** 🚨

Son situaciones de agresión escolar, acoso escolar (bullying) y ciberacoso que no constituyen delito pero que:
• Se presentan de manera repetida o sistemática
• Causan daños al cuerpo o salud sin generar incapacidad

**Ejemplos:**
• Intimidación o degradación con tecnologías
• Agresión verbal sistemática
• Acoso o provocación sexual
• Deteriorar bienes institucionales
• Comercializar trabajos académicos

**Medidas Pedagógicas:**
• Reporte al comité de convivencia
• Citación a padres de familia
• Trabajos reflexivos con orientación
• Suspensión entre 3 a 5 días hábiles
• Reparación de daños causados
• Posible temporalización asistida

¿Quieres información sobre el protocolo específico?"""
    },
    
    "situaciones_tipo_3": {
        "keywords": ["situacion tipo 3", "tipo iii", "delito", "grave", "violencia sexual", "armas"],
        "response": """**Situaciones Tipo III** 🆘

Situaciones de agresión escolar constitutivas de presuntos delitos contra la libertad, integridad y formación sexual, o cualquier otro delito del código penal.

**Ejemplos:**
• Portar armas de cualquier tipo
• Violencia sexual
• Tráfico de sustancias psicoactivas
• Amenazas graves
• Lesiones personales

**Protocolo Inmediato:**
• Atención en salud física y mental
• Información inmediata a padres/acudientes
• Reporte a Policía Nacional
• Medidas de protección a víctimas
• Reporte al Sistema de Información Unificado
• Posible cancelación de matrícula

**IMPORTANTE:** Estas situaciones requieren intervención de autoridades competentes.

¿Necesitas información sobre el debido proceso?"""
    },
    
    "gobierno_escolar": {
        "keywords": ["gobierno escolar", "consejo directivo", "consejo academico", "personero", "representante"],
        "response": """**Gobierno Escolar** 🏛️

El gobierno escolar es un sistema de participación democrática que incluye:

**Consejo Directivo:**
• Rector (presidente)
• 2 representantes docentes
• 2 representantes de padres
• 1 representante estudiantil (grado 11)
• 1 representante de exalumnos
• 1 representante del sector productivo

**Consejo Académico:**
• Rector (presidente)
• Directivos docentes
• Un docente por área

**Representación Estudiantil:**
• Consejo de estudiantes
• Personero estudiantil
• Representante al consejo directivo
• Contralor estudiantil

¿Te interesa conocer las funciones específicas de algún órgano?"""
    },
    
    "debido_proceso": {
        "keywords": ["debido proceso", "proceso disciplinario", "como se investiga", "procedimiento"],
        "response": """**Debido Proceso** ⚖️

Etapas del proceso disciplinario:

**1. Queja o Conocimiento de Oficio**
• Presentación formal de la situación
• Documentación de hechos

**2. Indagación Preliminar**
• Verificación de hechos
• Identificación de involucrados

**3. Mediación (si aplica)**
• Búsqueda de acuerdos amigables
• Justicia restaurativa

**4. Apertura del Proceso**
• Resolución rectoral
• Notificación al estudiante

**5. Pruebas y Descargos**
• Recolección de evidencias
• Derecho a defensa

**6. Decisión Primera Instancia**
• Resolución rectoral con sanción

**7. Recursos**
• Apelación y reposición
• 3 días hábiles para presentar

**8. Segunda Instancia**
• Revisión por Jefe de Núcleo

¿Quieres detalles sobre alguna etapa específica?"""
    },
    
    "servicios": {
        "keywords": ["servicios", "biblioteca", "restaurante", "laboratorio", "orientacion"],
        "response": """**Servicios Institucionales** 🏢

La I.E. Atanasio Girardot ofrece:

**Alimentación:**
• Restaurante escolar (refrigerio/almuerzo)
• Prioridad para preescolar y primaria

**Biblioteca Escolar:**
• Préstamo de libros (8 días)
• Hasta 3 materiales por usuario
• Horario: descansos y horas programadas

**Apoyo Pedagógico:**
• Orientación escolar
• Atención psicopedagógica
• Remisiones externas

**Tecnológicos:**
• Laboratorios de informática
• Aulas digitales
• Equipos audiovisuales

**Comunicación:**
• Emisora institucional
• Periódico mural
• Carteleras informativas

¿Te interesa información detallada sobre algún servicio?"""
    },

    "servicio_social": {
        "keywords": ["servicio social", "horas sociales", "comunidad", "grado 10", "grado 11"],
        "response": """**Servicio Social Estudiantil** 🤝

**Requisitos:**
• Estudiantes de grados 10° y 11°
• Mínimo 80 horas
• En horario contrario a clases
• Actividades sin ánimo de lucro

**Instituciones Participantes:**
• Alcaldía Municipal
• Hospital y Cruz Roja
• Bibliotecas
• Hogares Infantiles
• Casa de la Cultura
• INDER
• Bomberos
• Organizaciones comunitarias

**Responsabilidades:**
• Dedicar mínimo 2 horas diarias
• Ser respetuoso y discreto
• Cuidar recursos asignados
• Cumplir horarios establecidos

**Coordinación:**
• Un coordinador institucional
• Seguimiento y evaluación
• Certificación de cumplimiento

¿Necesitas información sobre instituciones específicas?"""
    },

    "contacto_ayuda": {
        "keywords": ["ayuda", "contacto", "quien me ayuda", "donde acudir", "apoyo"],
        "response": """**¿Necesitas Ayuda?** 🆘

**Conducto Regular Académico:**
1. Docente de la asignatura
2. Padre de familia/acudiente
3. Director de grupo
4. Coordinación
5. Rectoría
6. Consejo Directivo

**Conducto Regular Convivencial:**
1. Docente
2. Director de grupo
3. Coordinación
4. Rectoría
5. Comité Escolar de Convivencia
6. Consejo Directivo

**Apoyo Especializado:**
• Docente Orientador
• Personero Estudiantil
• Jueces de Paz Escolar
• Representante Estudiantil

**Recuerda:** Siempre puedes solicitar acompañamiento del personero estudiantil para garantizar tus derechos.

¿Te puedo ayudar con algo más específico?"""
    }
}

def find_best_match(user_input):
    user_input = user_input.lower()
    best_match = None
    best_score = 0
    
    for topic, data in KNOWLEDGE_BASE.items():
        for keyword in data["keywords"]:
            if keyword in user_input:
                # Simple scoring based on keyword presence
                score = len(keyword) / len(user_input) + (user_input.count(keyword) * 0.1)
                if score > best_score:
                    best_score = score
                    best_match = topic
    
    return best_match if best_score > 0.1 else None

@app.route('/')
def home():
    return render_template('chatbot.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_message = data.get('message', '').strip()
        
        if not user_message:
            return jsonify({
                'response': "Por favor, escribe tu pregunta sobre el Manual de Convivencia.",
                'timestamp': datetime.now().strftime("%H:%M")
            })
        
        # Saludos
        if any(greeting in user_message.lower() for greeting in ['hola', 'buenos días', 'buenas tardes', 'buenas noches', 'hey']):
            return jsonify({
                'response': """¡Hola! Soy el asistente virtual de la I.E. Atanasio Girardot 🏫

Estoy aquí para ayudarte con información sobre nuestro Manual de Convivencia. Puedo ayudarte con:

• **Derechos y deberes** de los estudiantes
• **Uniformes** institucionales  
• **Situaciones disciplinarias** (Tipos I, II, III)
• **Gobierno escolar** y representación
• **Servicios** institucionales
• **Debido proceso**
• **Servicio social estudiantil**

¿Sobre qué te gustaría saber más?""",
                'timestamp': datetime.now().strftime("%H:%M")
            })
        
        # Despedidas
        if any(farewell in user_message.lower() for farewell in ['adiós', 'bye', 'hasta luego', 'gracias', 'chao']):
            return jsonify({
                'response': "¡Hasta pronto! Recuerda que siempre puedes consultarme sobre el Manual de Convivencia. ¡Que tengas un excelente día! 👋",
                'timestamp': datetime.now().strftime("%H:%M")
            })
        
        # Buscar respuesta en la base de conocimiento
        best_match = find_best_match(user_message)
        
        if best_match:
            response = KNOWLEDGE_BASE[best_match]["response"]
        else:
            # Respuesta por defecto con sugerencias
            response = """No encontré información específica sobre tu consulta. 🤔

Puedes preguntarme sobre:

• **"¿Cuáles son mis derechos como estudiante?"**
• **"¿Qué uniforme debo usar?"**
• **"¿Qué es una situación tipo II?"**
• **"¿Cómo funciona el gobierno escolar?"**
• **"¿Qué servicios ofrece el colegio?"**
• **"¿Cómo es el debido proceso?"**

¿Podrías reformular tu pregunta con alguno de estos temas?"""
        
        return jsonify({
            'response': response,
            'timestamp': datetime.now().strftime("%H:%M")
        })
        
    except Exception as e:
        return jsonify({
            'response': "Disculpa, hubo un error procesando tu consulta. Por favor intenta nuevamente.",
            'timestamp': datetime.now().strftime("%H:%M")
        }), 500

@app.route('/health')
def health():
    return jsonify({'status': 'OK', 'service': 'Chatbot Atanasio Girardot'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)