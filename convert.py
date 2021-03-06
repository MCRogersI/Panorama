import unicodedata
from fuzzywuzzy import process
from pkg_resources import resource_filename # For the right filename

def remove_accents(input_str):
    '''
    Removes accents and special characters
    Input:  string
    Output: Modified string
    '''

    nfkd_form = unicodedata.normalize('NFKD', input_str)
    return u"".join([c for c in nfkd_form if not unicodedata.combining(c)])

def comunas_dict():
    '''
    Returns a dictionary with Comuna_name : code
    Reads it from a file comunas.csv on the 'data' directory
    '''
    
    comunas = {"LUMACO": 9207, 
"LOTA": 8106, 
"LAUTARO": 9108, 
"COMBARBALA": 4302, 
"PIRQUE": 13202, 
"JUAN FERNANDEZ": 5104, 
"LAGUNA BLANCA": 12102, 
"SAN CARLOS": 8416, 
"LAGO VERDE": 11102, 
"ANGOL": 9201, 
"CHAITEN": 10401, 
"QUINTA NORMAL": 13126, 
"COPIAPO": 3101, 
"CALBUCO": 10102, 
"MACHALI": 6108, 
"DIEGO DE ALMAGRO": 3202, 
"EMPEDRADO": 7104, 
"VICTORIA": 9211, 
"YERBAS BUENAS": 7408, 
"PUERTO OCTAY": 10302, 
"RIO HURTADO": 4305, 
"SAN MIGUEL": 13130, 
"PELARCO": 7106, 
"COINCO": 6103, 
"TIMAUKEL": 12303, 
"ALTO HOSPICIO": 1107, 
"MELIPEUCO": 9110, 
"MARIA PINTO": 13504, 
"PAINE": 13404, 
"ESTACION CENTRAL": 13106, 
"LANCO": 14103, 
"QUILICURA": 13125, 
"TEODORO SCHMIDT": 9117, 
"SAN FERNANDO": 6301, 
"COLINA": 13301, 
"CHONCHI": 10203, 
"CASTRO": 10201, 
"CABO DE HORNOS": 12201, 
"FREIRE": 9105, 
"COLLIPULLI": 9202, 
"CONTULMO": 8204, 
"NIQUEN": 8409, 
"MOSTAZAL": 6110, 
"SAN JOAQUIN": 13129, 
"EL BOSQUE": 13105, 
"CERRILLOS": 13102, 
"CORONEL": 8102, 
"LAJA": 8304, 
"PUREN": 9208, 
"RENAICO": 9209, 
"SAN FABIAN": 8417, 
"HUALPEN": 8112, 
"PICHIDEGUA": 6113, 
"PINTO": 8411, 
"VICHUQUEN": 7309, 
"CHANCO": 7202, 
"PENCO": 8107, 
"PAIGUANO": 4105, 
"PAIHUANO": 4105, 
"LOS ANGELES": 8301, 
"LO BARNECHEA": 13115, 
"OSORNO": 10301, 
"HUALAIHUE": 10403, 
"COLCHANE": 1403, 
"PUTRE": 15201, 
"LA UNION": 14201, 
"CABILDO": 5402, 
"PUERTO VARAS": 10109, 
"NATALES": 12401, 
"MARIQUINA": 14106, 
"FUTALEUFU": 10402, 
"LA HIGUERA": 4104, 
"LONCOCHE": 9109, 
"LEBU": 8201, 
"TENO": 7308, 
"RENGO": 6115, 
"MAULLIN": 10108, 
"TALAGANTE": 13601, 
"CHILE CHICO": 11401, 
"HUASCO": 3304, 
"FLORIDA": 8104, 
"CUREPTO": 7103, 
"TEMUCO": 9101, 
"EL MONTE": 13602, 
"VITACURA": 13132, 
"MEJILLONES": 2102, 
"SAN JAVIER": 7406, 
"PUDAHUEL": 13124, 
"QUEMCHI": 10209, 
"CURACAVI": 13503, 
"HUARA": 1404, 
"HUECHURABA": 13107, 
"TALCAHUANO": 8110, 
"CALERA DE TANGO": 13403, 
"SAN ANTONIO": 5601, 
"ALHUE": 13502, 
"EL CARMEN": 8407, 
"MAULE": 7105, 
"PUMANQUE": 6309, 
"LLAILLAY": 5703, 
"CURARREHUE": 9104, 
"CAUQUENES": 7201, 
"LINARES": 7401, 
"VILLA ALEMANA": 5804, 
"COLBUN": 7402, 
"RETIRO": 7405, 
"MACUL": 13118, 
"PURRANQUE": 10303, 
"PALMILLA": 6306, 
"VINA DEL MAR": 5109, 
"RANQUIL": 8415, 
"OVALLE": 4301, 
"CHILLAN": 8401, 
"LOLOL": 6304, 
"PALENA": 10404, 
"TALCA": 7101, 
"TORRES DEL PAINE": 12402, 
"ANDACOLLO": 4103, 
"PERQUENCO": 9113, 
"TOCOPILLA": 2301, 
"LA GRANJA": 13111, 
"LICANTEN": 7303, 
"QUILACO": 8308, 
"GENERAL LAGOS": 15202, 
"LA FLORIDA": 13110, 
"CHEPICA": 6302, 
"GUAITECAS": 11203, 
"ISLA DE PASCUA": 5201, 
"PLACILLA": 6308, 
"SAN GREGORIO": 12104, 
"PORVENIR": 12301, 
"LO PRADO": 13117, 
"SANTA CRUZ": 6310, 
"YUNGAY": 8421, 
"TOLTEN": 9118, 
"PICHILEMU": 6201, 
"COBQUECURA": 8403, 
"QUELLON": 10208, 
"RIO IBANEZ": 11402, 
"SAN PABLO": 10307, 
"VILLARRICA": 9120, 
"TRAIGUEN": 9210, 
"PANGUIPULLI": 14108, 
"VALLENAR": 3301, 
"LOS LAGOS": 14104, 
"PROVIDENCIA": 13123, 
"PAREDONES": 6206, 
"ERCILLA": 9204, 
"PEUMO": 6112, 
"TOME": 8111, 
"CATEMU": 5702, 
"PRIMAVERA": 12302, 
"DONIHUE": 6105, 
"SAN PEDRO": 13505, 
"TORTEL": 11303, 
"CHOLCHOL": 9121, 
"CONCON": 5103, 
"ALTO DEL CARMEN": 3302, 
"SIERRA GORDA": 2103, 
"TALTAL": 2104, 
"PARRAL": 7404, 
"NINHUE": 8408, 
"CHILLAN VIEJO": 8406, 
"NANCAGUA": 6305, 
"ANTUCO": 8302, 
"SAN RAMON": 13131, 
"HIJUELAS": 5503, 
"PORTEZUELO": 8412, 
"SAN ESTEBAN": 5304, 
"AISEN": 11201, 
"AYSEN": 11201, 
"QUILLECO": 8309, 
"NEGRETE": 8307, 
"CONSTITUCION": 7102, 
"CANELA": 4202, 
"IQUIQUE": 1101, 
"ALTO BIOBIO": 8314, 
"SAGRADA FAMILIA": 7307, 
"SANTO DOMINGO": 5606, 
"LAMPA": 13302, 
"SAAVEDRA": 9116, 
"CERRO NAVIA": 13103, 
"COCHAMO": 10103, 
"SAN CLEMENTE": 7109, 
"PANQUEHUE": 5704, 
"LOS VILOS": 4203, 
"CARAHUE": 9102, 
"CHIMBARONGO": 6303, 
"EL QUISCO": 5604, 
"CONCHALI": 13104, 
"QUIRIHUE": 8414, 
"QUINCHAO": 10210, 
"NAVIDAD": 6205, 
"BULNES": 8402, 
"FUTRONO": 14202, 
"PADRE LAS CASAS": 9112, 
"RAUCO": 7305, 
"ANTARTICA": 12202, 
"SAN JUAN DE LA COSTA": 10306, 
"QUILPUE": 5801, 
"RENCA": 13128, 
"CISNES": 11202, 
"TUCAPEL": 8312, 
"MARIA ELENA": 2302, 
"LA SERENA": 4101, 
"CURANILAHUE": 8205, 
"GORBEA": 9107, 
"O'HIGGINS": 11302, 
"PETORCA": 5404, 
"SANTIAGO": 13101, 
"VILLA ALEGRE": 7407, 
"COIHAIQUE": 11101, 
"COYHAIQUE": 11101, 
"CALERA": 5502, 
"LA CALERA": 5502, 
"CALLE LARGA": 5302, 
"LITUECHE": 6203, 
"RINCONADA": 5303, 
"PENCAHUE": 7107, 
"LOS SAUCES": 9206, 
"CODEGUA": 6102, 
"OLIVAR": 6111, 
"RIO NEGRO": 10305, 
"CURICO": 7301, 
"RECOLETA": 13127, 
"MULCHEN": 8305, 
"MELIPILLA": 13501, 
"ALGARROBO": 5602, 
"PUCON": 9115, 
"PERALILLO": 6307, 
"FRESIA": 10104, 
"BUIN": 13402, 
"TIERRA AMARILLA": 3103, 
"PUERTO MONTT": 10101, 
"QUEILEN": 10207, 
"FRUTILLAR": 10105, 
"MAFIL": 14105, 
"CURACO DE VELEZ": 10204, 
"DALCAHUE": 10205, 
"PEMUCO": 8410, 
"PELLUHUE": 7203, 
"LAGO RANCO": 14203, 
"PADRE HURTADO": 13604, 
"ARICA": 15101, 
"ISLA DE MAIPO": 13603, 
"PAILLACO": 14107, 
"LA PINTANA": 13112, 
"LONGAVI": 7403, 
"MOLINA": 7304, 
"CAMINA": 1402, 
"HUALQUI": 8105, 
"ANCUD": 10202, 
"VALDIVIA": 14101, 
"CHANARAL": 3201, 
"LONQUIMAY": 9205, 
"SAN IGNACIO": 8418, 
"ROMERAL": 7306, 
"SAN NICOLAS": 8419, 
"COLTAUCO": 6104, 
"VALPARAISO": 5101, 
"COIHUECO": 8405, 
"COQUIMBO": 4102, 
"COCHRANE": 11301, 
"LOS ALAMOS": 8206, 
"QUINTA DE TILCOCO": 6114, 
"CHIGUAYANTE": 8103, 
"YUMBEL": 8313, 
"LA LIGUA": 5401, 
"NOGALES": 5506, 
"SANTA BARBARA": 8311, 
"PENALOLEN": 13122, 
"CARTAGENA": 5603, 
"LA REINA": 13113, 
"CABRERO": 8303, 
"CABO DE HORNOS (EX NAVARINO)": 12201, 
"FREIRINA": 3303, 
"SANTA JUANA": 8109, 
"RIO VERDE": 12103, 
"CALDERA": 3102, 
"CALAMA": 2201, 
"CANETE": 8203, 
"PICA": 1405, 
"EL TABO": 5605, 
"SAN BERNARDO": 13401, 
"INDEPENDENCIA": 13108, 
"LAS CONDES": 13114, 
"RIO BUENO": 14204, 
"PENAFLOR": 13605, 
"RANCAGUA": 6101, 
"OLMUE": 5803, 
"PUENTE ALTO": 13201, 
"SAN PEDRO DE LA PAZ": 8108, 
"OLLAGUE": 2202, 
"LA CISTERNA": 13109, 
"SAN FELIPE": 5701, 
"MAIPU": 13119, 
"PUNTA ARENAS": 12101, 
"PAPUDO": 5403, 
"LO ESPEJO": 13116, 
"ARAUCO": 8202, 
"PUNITAQUI": 4304, 
"NAVARINO": 12201, 
"TIRUA": 8207, 
"QUILLOTA": 5501, 
"PUYEHUE": 10304, 
"QUINTERO": 5107, 
"PITRUFQUEN": 9114, 
"MALLOA": 6109, 
"CASABLANCA": 5102, 
"GRANEROS": 6106, 
"LOS MUERMOS": 10106, 
"CORRAL": 14102, 
"POZO ALMONTE": 1401, 
"LA ESTRELLA": 6202, 
"NUEVA IMPERIAL": 9111, 
"HUALANE": 7302, 
"REQUINOA": 6116, 
"ILLAPEL": 4201, 
"SANTA MARIA": 5706, 
"CURACAUTIN": 9203, 
"ZAPALLAR": 5405, 
"PUTAENDO": 5705, 
"MARCHIHUE": 6204, 
"LLANQUIHUE": 10107, 
"SAN PEDRO DE ATACAMA": 2203, 
"ANTOFAGASTA": 2101, 
"PUQUELDON": 10206, 
"TREGUACO": 8420, 
"LA CRUZ": 5504, 
"NUNOA": 13120, 
"SAN VICENTE": 6117, 
"SAN VICENTE DE TAGUA TAGUA": 6117, 
"CAMARONES": 15102, 
"SAN JOSE DE MAIPO": 13203, 
"SALAMANCA": 4204, 
"LAS CABRAS": 6107, 
"QUILLON": 8413, 
"LOS ANDES": 5301, 
"VICUNA": 4106, 
"LIMACHE": 5802, 
"TILTIL": 13303, 
"PEDRO AGUIRRE CERDA": 13121, 
"MONTE PATRIA": 4303, 
"NACIMIENTO": 8306, 
"PUCHUNCAVI": 5105, 
"GALVARINO": 9106, 
"CONCEPCION": 8101, 
"SAN ROSENDO": 8310, 
"SAN RAFAEL": 7110, 
"RIO CLARO": 7108, 
"COELEMU": 8404, 
"CUNCO": 9103, 
"VILCUN": 9119}
    
    return comunas

    # This is so it gets the correct path+filename and
    # it actually works
    # filename = resource_filename(__name__, '../data/comunas.csv')

    # with open(filename, newline='') as csvfile:
        # data = csv.reader(csvfile, delimiter=',')
        # for row in data:
            # comunas[row[0]] = row[1]
    # return comunas

def get_code(name):
    '''
    Given the name of a comuna, returns the code of that comuna
    Input:  string
    Output: string
    '''

    comuna = remove_accents(name).upper()
    comunas = comunas_dict()

    try:
        return comunas[comuna]
    except Exception as e:
        print ("Could not find code for: ", comuna)

def get_fuzzy(name, show=False, threshold=False):
    '''
    Returns the most similar comuna name.
    Uses the fuzzywuzzy package
    Returns the name (string)
    '''

    comuna = remove_accents(name).upper()
    comunas = comunas_dict()

    comunas_names = list(comunas.keys())    # List of comunas names (choioces)

    best_match = process.extractOne(comuna, comunas_names)

    if show:    #prints the name of the comuna and the score it got
        print (best_match)
    if threshold:   #if the user specifies a threshold
        if best_match[1]<threshold:
            print ("Score lower than minimum threshold for comuna: {0} - {1}".format(comuna, best_match[0]))
            return None
    return best_match[0]    # The name

def get_steps(name, show=False, threshold=False):
    '''
    A wrapper mtehod that uses the 'get_code' function first
    and if it fails, it tries the 'get_fuzzy method'
    Returns the code
    '''

    comuna = get_code(name)
    if comuna==None:
        comuna = get_fuzzy(name, show, threshold)
        if comuna:
            comuna = get_code(comuna)
    return comuna
