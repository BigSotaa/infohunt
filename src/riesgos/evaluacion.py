import json, random, requests, time

def getAlexaRank(domain:str,similar_web_api_key:str):
    try:
        url = "https://similarweb12.p.rapidapi.com/v1/website-analytics/"
        querystring = {"domain":domain}
        headers = {
            "X-RapidAPI-Key": similar_web_api_key,
            "X-RapidAPI-Host": "similarweb12.p.rapidapi.com"
        }

        response = requests.get(url, headers=headers, params=querystring)
        response=response.json()
        rank_global = response['overview']['globalRank']
        aux=asignar_nivel_criticidad(rank_global)
        return aux
    except:
        return "Medio"

def generar_evaluacion_y_recomendaciones(data,similar_web_api_key):
    evaluacion = []
    
    #print(data)
    
    # Definir recomendaciones basadas en la evaluación
    recomendaciones_data_leak = [
        {"recomendacion": "Change the password of the affected account immediately.", "impacto": "High"},
        {"recomendacion": "Enable two-factor authentication (2FA) to improve the security of your account.", "impacto": "Medium"},
        {"recomendacion": "Check all your accounts for reused passwords and change them.", "impacto": "High"},
        {"recomendacion": "Monitor your bank and financial accounts for unauthorized activity.", "impacto": "High"},
        {"recomendacion": "Be skeptical of suspicious emails or messages and avoid clicking on unverified links.", "impacto": "Medium"},
        {"recomendacion": "Report to the relevant authorities and platforms in case of fraud or identity theft.", "impacto": "High"},
        {"recomendacion": "Use a password management solution to create and store secure passwords.", "impacto": "Medium"},
        {"recomendacion": "Keep your systems and software updated to protect against known vulnerabilities.", "impacto": "High"},
        {"recomendacion": "Review the privacy settings of your online accounts and clear unnecessary personal information.", "impacto": "Medium"},
        {"recomendacion": "Educate your contacts about online threats and promote safe practices.", "impacto": "Low"},

    ]

    for entry in data:
        aux=entry['sources'][0]
        aux= aux.strip("[]'")
        aux=str(aux)
        nivel_critico=getAlexaRank(aux,similar_web_api_key)
        
        email = entry['line'].split(':')[0]
        breaches = entry['sources']
        last_breach = entry['last_breach']
        password = entry['line'].split(':')[1]

        evaluacion.append({
            'Email': email,
            'Breaches': breaches,
            'Password': password,
            'Last Breach': last_breach,
            'Nivel de Criticidad': nivel_critico,
            'Recomendaciones': random.sample(recomendaciones_data_leak, 2)
        })
    #Debug
    #print(evaluacion)
    
    return evaluacion

def asignar_nivel_criticidad(alexa_rank):
    if alexa_rank is None:
        return 'Unknown'  # Or any other default you want to return
    if alexa_rank < 1000:
        return 'Critical'  # Changed to English
    elif alexa_rank < 10000:
        return 'High'  # Changed to English
    elif alexa_rank < 100000:
        return 'Medium'  # Changed to English
    else:
        return 'Low'  # Changed to English

    
def identificar_riesgos_username(username: str):
    # Leer los datos de redes sociales del archivo JSON
    file_path = f"output/report_{username}_simple.json"
    with open(file_path, "r") as file:
        datos_redes_sociales = json.load(file)

    # Crear una variable para almacenar los datos importantes
    datos_importantes = {}

    # Lista de recomendaciones para nivel crítico medio
    recomendaciones_medio = [
        {"recomendacion": "Review your privacy settings carefully and adjust the visibility of your profile and posts as necessary.", "impacto": "Low"},
        {"recomendacion": "Be cautious when accepting friend requests or following unknown people.", "impacto": "Medium"},
        {"recomendacion": "Regularly review your activity and adjust notification settings to maintain greater control over your account.", "impacto": "High"},
        {"recomendacion": "Avoid sharing personal or sensitive data in your posts.", "impacto": "Medium"},
        {"recomendacion": "Use two-factor authentication (2FA) if available to improve the security of your account.", "impacto": "High"},
        {"recomendacion": "Keep your passwords secure and regularly change the passwords of your accounts.", "impacto": "High"},
        {"recomendacion": "Disable geographic locations in your posts to protect your privacy.", "impacto": "Medium"},
        {"recomendacion": "Do not share confidential information, such as phone numbers or addresses, in your public profile.", "impacto": "Medium"},
        {"recomendacion": "Be skeptical of suspicious offers or links you receive through direct messages.", "impacto": "Medium"},
        {"recomendacion": "Periodically review the applications and services linked to your account and remove those you no longer use or trust.", "impacto": "Low"},
        {"recomendacion": "Immediately report any suspicious activity or account to the social media platform.", "impacto": "High"},
        {"recomendacion": "Do not reveal your real-time location through social media, especially if you are away from home.", "impacto": "Medium"},
        {"recomendacion": "Be careful with third-party applications and make sure they have good ratings and reviews before authorizing them.", "impacto": "Medium"},
    ]

    # Extraer los datos importantes y almacenarlos en la variable
    for red_social, detalles in datos_redes_sociales.items():
        # Check if 'site' key exists in 'detalles'
        if 'site' in detalles and 'alexaRank' in detalles['site']:
            alexa_rank = detalles['site']['alexaRank']
        else:
            alexa_rank = None  # or some default value

        nivel_criticidad = asignar_nivel_criticidad(alexa_rank)

        datos_importantes[red_social] = {
            "status": detalles["status"],
            "url_user": detalles["url_user"],
            "critical_level": nivel_criticidad,
            "recommendations":random.sample(recomendaciones_medio, 2)
        }

    #Debug    
    #print(datos_importantes)

    return datos_importantes

