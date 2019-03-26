TEMASG = ["sucesos", "infraestructura y transportes", "entretenimiento", "política", 
          "deportes", "ciencia y ambiente", "asuntos internacionales", "otros", "economía",
         "asuntos sociales"]
TEMAS = []

TEMAS.append(["accidente", "asalto", "asesinato", "crimenes", "delitos sexuales", "desapariciones",
        "eventos naturales", "femicidio", "incendio", "juicios", "narcotrafico y crimen organizado", 
         "peleas", "suicidios", "estafa y/o fraude", "intervencion policial", "amenazas"])

TEMAS.append(["infraestructura", "infraestructura vial", "telecomunicaciones", "transito", "transporte",
              "uber", "combustible"])

TEMAS.append(["baile", "cine", "farandula", "moda", "musica", "ocio", "redes sociales", "streaming", 
              "television", "toros", "teatro"])

TEMAS.append(["asamblea legislativa", "candidatos politicos", "ciudadania", "corrupcion", "debates electorales",
             "huelga", "electorales", "ex-presidentes", "funcionarios publicos", "gobierno", "poder judicial",
             "instituciones publicas y autonomas", "medicion opinion publica", "partidos politicos", "presidencia",
             "sindicatos", "colegios profesionales", "cemento", "yanber", "municipalidades"])

TEMAS.append(["alpinismo", "atletismo", "boxeo", "ciclismo", "futbol", "golf", "natacion", "olimpiadas",
             "surf", "tennis", "triatlon", "mma"])

TEMAS.append(["ambiente", "animales", "arqueologia", "clima", "combustibles", "energia", "medicina", "naturaleza",
             "tecnologia", "sotenibilidad"])

TEMAS.append(["china", "estados unidos", "españa", "francia", "guerra", "italia", "nicaragua", "siria",
             "terrorismo", "onu", "venezuela", "corea del norte", "palestina"])

TEMAS.append(["cartas a la columna", "curiosidades", "feriados/efemerides", "historias de vida", "medios", 
              "salud", "condolencias", "loteria", "caridad", "quices"])

TEMAS.append(["banca", "fiscales", "gasto publico", "negocios", "pensiones", "pobreza", "trabajo", "crecimiento economico"])

TEMAS.append(["adultos mayores", "comunicacion", "cultura", "educacion", "genero", "historia", 
              "indigenas", "juventud", "lgbtiq", "literatura", "migracion", "niñez", "religion",
             "salud", "seguridad", "urbanismo", "vivienda", "servicio militar", "servicios publicos",
             "turismo"])

## Temas generales

temas_dic = {}
for i in range(len(TEMASG)):
    temas_dic[TEMASG[i]] = i

# sinónimos
temas_dic["infraestructura vial y transportes"] = temas_dic["infraestructura y transportes"]
temas_dic["infraestructura vial y transporte"] = temas_dic["infraestructura y transportes"]
temas_dic["mundo"] = temas_dic["asuntos internacionales"]
temas_dic["nacionales"] = temas_dic["política"]
temas_dic["asuntos"] = temas_dic["asuntos sociales"]
temas_dic["ambiente"] = temas_dic["ciencia y ambiente"]

## Temas específicos

temase_dics = []
for i in range(len(TEMASG)):
    dic = {}
    for j in range(len(TEMAS[i])):
        dic[TEMAS[i][j]] = j
    temase_dics.append(dic)

# sinonimos
temase_dics[0]["judiciales"] = temase_dics[0]["juicios"]
temase_dics[0]["accidentes"] = temase_dics[0]["accidente"]
temase_dics[0]["femicidios"] = temase_dics[0]["femicidio"]
temase_dics[0]["desaparecido"] = temase_dics[0]["desapariciones"]
temase_dics[0]["asaltos"] = temase_dics[0]["asalto"]
temase_dics[0]["narcotráfico y crimen organizado"] = temase_dics[0]["narcotrafico y crimen organizado"]
temase_dics[0]["desaparecida"] = temase_dics[0]["desapariciones"]

