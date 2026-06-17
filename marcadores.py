# marcadores.py
# Tabla de referencia clínica fija. Esto NO lo genera la IA: los rangos y las
# preguntas son fijos para que el semáforo sea siempre consistente entre corridas.
# Fuente: rangos estándar de referencia general (Mayo Clinic / MedlinePlus).
# IMPORTANTE: antes de la entrega final, verificar 3-4 de estos rangos contra
# una fuente citable para la documentación del proyecto.

MARCADORES = {
    "Hemoglobina": {
        "unidad": "g/dL",
        "explicacion": "Mide la proteína de los glóbulos rojos que transporta oxígeno por tu cuerpo.",
        "rango": {"hombre": (13.5, 17.5), "mujer": (12.0, 15.5)},
        "preguntas_bajo": [
            "¿Mi nivel bajo de hemoglobina podría ser anemia?",
            "¿Qué tipo de anemia sospecha y qué prueba lo confirmaría?",
            "¿Debo cambiar mi dieta antes de la próxima revisión?",
        ],
        "preguntas_alto": [
            "¿Qué podría estar causando que mi hemoglobina esté alta?",
            "¿Esto está relacionado con hidratación o con otra condición?",
            "¿Necesito algún estudio adicional?",
        ],
    },
    "Hematocrito": {
        "unidad": "%",
        "explicacion": "Mide qué porcentaje de tu sangre está compuesto por glóbulos rojos.",
        "rango": {"hombre": (38.8, 50.0), "mujer": (34.9, 44.5)},
        "preguntas_bajo": [
            "¿Este resultado está relacionado con mi hemoglobina?",
            "¿Podría deberse a algo puntual como deshidratación?",
            "¿Necesito repetir el estudio en otras condiciones?",
        ],
        "preguntas_alto": [
            "¿Qué podría causar un hematocrito elevado?",
            "¿Esto se relaciona con mi nivel de oxígeno o hidratación?",
            "¿Debo preocuparme por la viscosidad de mi sangre?",
        ],
    },
    "Glóbulos blancos": {
        "unidad": "/µL",
        "explicacion": "Mide tus células de defensa contra infecciones.",
        "rango": {"hombre": (4500, 11000), "mujer": (4500, 11000)},
        "preguntas_bajo": [
            "¿Un nivel bajo de glóbulos blancos me pone en riesgo de infecciones?",
            "¿Debo evitar algo en particular mientras esto se aclara?",
            "¿Necesito repetir el estudio pronto?",
        ],
        "preguntas_alto": [
            "¿Este nivel sugiere una infección activa o inflamación?",
            "¿Debo repetir el estudio si me sentí enfermo recientemente?",
            "¿Hay algún medicamento que pueda estar afectando este valor?",
        ],
    },
    "Plaquetas": {
        "unidad": "/µL",
        "explicacion": "Mide tu capacidad de coagulación de la sangre.",
        "rango": {"hombre": (150000, 450000), "mujer": (150000, 450000)},
        "preguntas_bajo": [
            "¿Este nivel aumenta mi riesgo de sangrado?",
            "¿Debo evitar algún medicamento como aspirina?",
            "¿Cuándo debo repetir este estudio?",
        ],
        "preguntas_alto": [
            "¿Este nivel aumenta mi riesgo de coágulos?",
            "¿Debo evitar algún medicamento o actividad?",
            "¿Cuándo debo repetir este estudio?",
        ],
    },
    "Hierro sérico": {
        "unidad": "µg/dL",
        "explicacion": "Mide el hierro disponible en tu sangre, necesario para transportar oxígeno.",
        "rango": {"hombre": (65, 175), "mujer": (50, 170)},
        "preguntas_bajo": [
            "¿Mi nivel bajo de hierro está relacionado con mi hemoglobina?",
            "¿Debo tomar un suplemento de hierro o solo ajustar mi dieta?",
            "¿Qué alimentos me recomienda priorizar?",
        ],
        "preguntas_alto": [
            "¿Qué podría causar que mi hierro esté alto?",
            "¿Debo dejar de tomar suplementos de hierro si los uso?",
            "¿Necesito algún estudio adicional?",
        ],
    },
    "Glucosa": {
        "unidad": "mg/dL",
        "explicacion": "Mide el nivel de azúcar en tu sangre.",
        "rango": {"hombre": (70, 99), "mujer": (70, 99)},
        "preguntas_bajo": [
            "¿Este nivel bajo de glucosa es motivo de preocupación?",
            "¿Debo ajustar mis horarios de comida?",
            "¿Necesito repetir el estudio en otras condiciones?",
        ],
        "preguntas_alto": [
            "¿Este nivel me pone en riesgo de prediabetes?",
            "¿Necesito una prueba de hemoglobina glucosilada (A1C) para confirmar?",
            "¿Qué cambios en mi dieta sugiere primero?",
        ],
    },
    "Colesterol total": {
        "unidad": "mg/dL",
        "explicacion": "Mide la cantidad total de grasa (colesterol) en tu sangre.",
        "rango": {"hombre": (0, 200), "mujer": (0, 200)},
        "preguntas_bajo": [],
        "preguntas_alto": [
            "¿Qué tan alto es mi riesgo cardiovascular con este resultado?",
            "¿Debo enfocarme primero en LDL o en triglicéridos?",
            "¿Necesito medicamento o basta con cambios de estilo de vida?",
        ],
    },
    "Colesterol LDL": {
        "unidad": "mg/dL",
        "explicacion": "Mide el colesterol que puede acumularse y obstruir tus arterias.",
        "rango": {"hombre": (0, 100), "mujer": (0, 100)},
        "preguntas_bajo": [],
        "preguntas_alto": [
            "¿Qué tan urgente es bajar este número?",
            "¿Qué alimentos específicos debo reducir primero?",
            "¿En cuánto tiempo debo repetir el estudio para ver progreso?",
        ],
    },
    "Colesterol HDL": {
        "unidad": "mg/dL",
        "explicacion": "Mide el colesterol que ayuda a proteger tus arterias.",
        "rango": {"hombre": (40, 999), "mujer": (50, 999)},
        "preguntas_bajo": [
            "¿Qué puedo hacer para subir mi HDL de forma natural?",
            "¿El ejercicio que hago actualmente es suficiente?",
            "¿Este nivel bajo aumenta mi riesgo aunque mi LDL esté bien?",
        ],
        "preguntas_alto": [],
    },
    "Triglicéridos": {
        "unidad": "mg/dL",
        "explicacion": "Mide la grasa que tu cuerpo usa como fuente de energía.",
        "rango": {"hombre": (0, 150), "mujer": (0, 150)},
        "preguntas_bajo": [],
        "preguntas_alto": [
            "¿Esto está relacionado con mi consumo de azúcar o alcohol?",
            "¿Debo preocuparme por mi páncreas con este nivel?",
            "¿Cuándo debo repetir el estudio?",
        ],
    },
    "Creatinina": {
        "unidad": "mg/dL",
        "explicacion": "Mide qué tan bien están filtrando tus riñones.",
        "rango": {"hombre": (0.7, 1.3), "mujer": (0.6, 1.1)},
        "preguntas_bajo": [],
        "preguntas_alto": [
            "¿Esto indica un problema en mis riñones?",
            "¿Necesito una prueba adicional como la tasa de filtración glomerular (TFG)?",
            "¿Algún medicamento que tomo puede estar afectando este valor?",
        ],
    },
    "Ácido úrico": {
        "unidad": "mg/dL",
        "explicacion": "Mide un desecho que tu cuerpo produce al procesar ciertos alimentos.",
        "rango": {"hombre": (3.4, 7.0), "mujer": (2.4, 6.0)},
        "preguntas_bajo": [],
        "preguntas_alto": [
            "¿Este nivel me pone en riesgo de gota?",
            "¿Qué alimentos específicos debo evitar?",
            "¿Es necesario tratamiento aunque no tenga síntomas?",
        ],
    },
    "ALT (TGP)": {
        "unidad": "U/L",
        "explicacion": "Mide una enzima del hígado que indica si hay daño en sus células.",
        "rango": {"hombre": (7, 56), "mujer": (7, 56)},
        "preguntas_bajo": [],
        "preguntas_alto": [
            "¿Qué tan preocupante es esta elevación?",
            "¿Podría estar relacionada con algún medicamento o suplemento que tomo?",
            "¿Necesito un ultrasonido hepático?",
        ],
    },
    "AST (TGO)": {
        "unidad": "U/L",
        "explicacion": "Mide otra enzima relacionada con el hígado, aunque también puede venir de músculo o corazón.",
        "rango": {"hombre": (10, 40), "mujer": (10, 40)},
        "preguntas_bajo": [],
        "preguntas_alto": [
            "¿Esto confirma un problema hepático o podría ser otra causa?",
            "¿Debo evitar el alcohol mientras esto se aclara?",
            "¿Cuándo debo repetir el estudio?",
        ],
    },
}


def evaluar_semaforo(nombre_marcador: str, valor: float, sexo: str) -> str:
    """
    Compara un valor contra el rango fijo del marcador y regresa el color
    del semáforo. Esto es lógica de Python pura -- NO se le pide a Gemini --
    para que el resultado sea siempre el mismo dado el mismo valor.

    Regresa: "verde", "amarillo", "rojo", o "desconocido" si el marcador no existe.
    """
    if nombre_marcador not in MARCADORES:
        return "desconocido"

    sexo_key = "hombre" if sexo.lower().startswith("h") else "mujer"
    minimo, maximo = MARCADORES[nombre_marcador]["rango"][sexo_key]

    if minimo <= valor <= maximo:
        return "verde"

    # Qué tan lejos está del rango determina amarillo vs rojo.
    # Margen de 15% fuera de rango = amarillo; más allá = rojo.
    rango_total = maximo - minimo if maximo - minimo > 0 else maximo
    margen = rango_total * 0.15

    if minimo - margen <= valor < minimo or maximo < valor <= maximo + margen:
        return "amarillo"

    return "rojo"


def obtener_preguntas(nombre_marcador: str, valor: float, sexo: str) -> list:
    """Regresa las preguntas sugeridas según si el valor cayó alto o bajo."""
    if nombre_marcador not in MARCADORES:
        return []

    sexo_key = "hombre" if sexo.lower().startswith("h") else "mujer"
    minimo, maximo = MARCADORES[nombre_marcador]["rango"][sexo_key]

    if valor < minimo:
        return MARCADORES[nombre_marcador].get("preguntas_bajo", [])
    elif valor > maximo:
        return MARCADORES[nombre_marcador].get("preguntas_alto", [])
    return []