from datetime import datetime
import random
from django.http import JsonResponse
from django.shortcuts import render
from club.models.club import Club
from club.models.personal import Personal
from clubes.validators import validar_cuit
from disciplinas.models import Categoria, Disciplina, SocioCategoria
from socios.models import Socio

from parametros.models.alergia import Alergia
from parametros.models.ciudad import Ciudad
from parametros.models.dificultad import Dificultad
from parametros.models.enfermedad_cronica import EnfermedadCronica
from parametros.models.enfermedad_infancia import EnfermedadInfancia
from parametros.models.escuela import Escuela
from parametros.models.genero import Genero
from parametros.models.grupo_sanguineo import GrupoSanguineo
from parametros.models.medicacion import Medicacion
from parametros.models.tipo_documento import TipoDocumento
from parametros.models.tipo_socio import TipoSocio
from parametros.models.vacuna import Vacuna


def asociarme(request):
    error = ""
    mi_club = Club.objects.filter(id=1)
    mis_disciplinas = Disciplina.objects.filter(club=mi_club[0])
    nuestras_personas = Personal.objects.filter(club=mi_club[0])
    tipos_doc = TipoDocumento.objects.all()
    generos = Genero.objects.all()
    ciudades = Ciudad.objects.all()
    tipos_socios = TipoSocio.objects.all()
    grupos_sanguineos = GrupoSanguineo.objects.all()
    enf_cronicas = EnfermedadCronica.objects.all()
    enf_infancia = EnfermedadInfancia.objects.all()
    vacunas = Vacuna.objects.all()
    dificultades = Dificultad.objects.all()
    alergias = Alergia.objects.all()
    medicamentos = Medicacion.objects.all()
    escuelas = Escuela.objects.all()
    
    data = {
        'club' : mi_club[0],
        'disciplinas' : mis_disciplinas,
        'personas' : nuestras_personas,
        'tipos_doc': tipos_doc,
        'generos': generos,
        'ciudades': ciudades,
        'tipos_socios': tipos_socios,
        'grupos_sanguineos': grupos_sanguineos,
        'enf_cronicas': enf_cronicas,
        'enf_infancia': enf_infancia,
        'vacunas': vacunas,
        'dificultades': dificultades,
        'alergias': alergias,
        'medicamentos': medicamentos,
        'escuelas': escuelas,
        'error': error
    }
    if request.method == 'POST':
        submitForm(request)
    return render(request, 'asociarme.html', data)

def submitForm(request):
    nombre = request.POST.get('nombre')
    apellido = request.POST.get('apellido')
    fecha_nac = request.POST.get('fecha_nac')
    tipo_doc = request.POST.get('tipo_doc') #
    nro_doc = request.POST.get('nro_doc')
    CUIL = request.POST.get('CUIL')
    genero = request.POST.get('genero')#
    ciudad = request.POST.get('ciudad')#
    direccion = request.POST.get('direccion')
    nro_tel = request.POST.get('nro_tel')
    email = request.POST.get('email')
    usa_email = request.POST.get('usa_email')#
    fecha_ingreso = request.POST.get('fecha_ingreso')
    nombre_responsable = request.POST.get('nombre_responsable')
    nro_tel_responsable = request.POST.get('nro_tel_responsable')
    email_responsable = request.POST.get('email_responsable')
    if not email_responsable:
        email_responsable = None
    cobertura = request.POST.get('cobertura')
    nro_cobertura = request.POST.get('nro_cobertura')
    medico = request.POST.get('medico')
    grupo_sanguineo = request.POST.get('grupo_sanguineo')#
    peso = request.POST.get('peso')
    altura = request.POST.get('altura')
    enf_cronica = request.POST.getlist('enf_cronica')#
    enf_infancia = request.POST.getlist('enf_infancia')#
    enf_de_huesos = request.POST.get('enf_huesos')#
    enf_nerviosas = request.POST.get('enf_nerviosas')#
    enf_digestivas = request.POST.get('enf_digestivas')#
    vacunas = request.POST.getlist('vacunas')#
    alergias = request.POST.getlist('alergias')#
    dificultades = request.POST.getlist('dificultades')#
    medicamentos = request.POST.getlist('medicamentos')#
    escuela = request.POST.get('escuela')#
    anio_escolar = request.POST.get('anio_escolar')
    turno_escolar = request.POST.get('turno_escolar')
    tipo_contacto_escolar = request.POST.get('tipo_contacto_escolar')
    nombre_contacto_escolar = request.POST.get('nombre_contacto_escolar')
    tel_contacto_escolar = request.POST.get('tel_contacto_escolar')
    email_contacto_escolar = request.POST.get('email_contacto_escolar')
    if not email_contacto_escolar:
        email_contacto_escolar = None
    
    tipo_docu = TipoDocumento.objects.get(id=tipo_doc)
    gen = Genero.objects.get(id=genero)
    ciu = Ciudad.objects.get(id=ciudad)
    grupo_san = GrupoSanguineo.objects.get(id=grupo_sanguineo)

    disciplinas = request.POST.getlist('disciplinas')
    
    if escuela:
        esc = Escuela.objects.get(id=escuela)
    else:
        esc = None
    if anio_escolar:
        anio_escolar = int(anio_escolar)
    else:
        anio_escolar = None
    
    tiene_email = usa_email == '1'
    enf_huesos = enf_de_huesos == '1'
    enf_diges = enf_digestivas == '1'
    enf_nervi = enf_nerviosas == '1'

    
    try:
        nro_inscripcion = random.randint(1, 1000000) 
        socio = Socio(
            nombre=nombre,
            apellido = apellido,
            fecha_nacimiento = fecha_nac,
            tipo_documento = tipo_docu,
            nro_documento = nro_doc,
            genero = gen,
            CUIL = CUIL,
            ciudad = ciu,
            direccion = direccion,
            nro_telefono = nro_tel,
            email_socio = email,
            usa_email = tiene_email,
            fecha_ingreso = fecha_ingreso,
            responsable = nombre_responsable,
            tel_responsable = nro_tel_responsable,
            email_responsable = email_responsable,
            cobertura = cobertura,
            nro_cobertura = nro_cobertura,
            medico = medico,
            grupo_sanguineo = grupo_san,
            peso = peso,
            altura = altura,
            enfermedades_huesos = enf_huesos,
            enfermedades_nerviosas = enf_nervi,
            enfermedades_digestivas = enf_diges,
            escuela = esc,
            año_escolar = anio_escolar,
            turno_escolar = turno_escolar,
            tipo_contacto_escolar = tipo_contacto_escolar,
            nombre_contacto_escolar = nombre_contacto_escolar,
            telefono_contacto_escolar = tel_contacto_escolar,
            email_contacto_escolar = email_contacto_escolar,
            nro_inscripcion = nro_inscripcion
        )
        socio.save()

        for disciplina in disciplinas:
            # Obtener la categoría que corresponde a la edad del socio y crear el registro
            edad = datetime.now().year - int(socio.fecha_nacimiento[0:4])
            cats = Categoria.objects.filter(disciplina=disciplina).filter(edad_desde__lte=edad).filter(edad_hasta__gte=edad)
            for cat in cats:
                alta_cat = SocioCategoria(socio=socio, categoria=cat, estado=True, club=socio.club)
                alta_cat.save()
        
        if enf_cronica != 0:
            enfermedades_cronicas = EnfermedadCronica.objects.filter(id__in=enf_cronica)
            socio.enfermedades_cronicas.set(enfermedades_cronicas)
        else: 
            pass

        if enf_infancia != 0:
            enfermedades_infancia = EnfermedadInfancia.objects.filter(id__in=enf_infancia)
            socio.enfermedades_infancia.set(enfermedades_infancia)
        else: 
            pass
        
        if vacunas != 0:
            lista_vacunas = Vacuna.objects.filter(id__in=vacunas)
            socio.vacunas.set(lista_vacunas)
        else: 
            pass

        if alergias != 0:
            lista_alergias = Alergia.objects.filter(id__in=alergias)
            socio.alergias.set(lista_alergias)
        else: 
            pass
        if dificultades != 0:
            lista_dificultades = Dificultad.objects.filter(id__in=dificultades)
            socio.dificultades.set(lista_dificultades)
        else: 
            pass
        if medicamentos != 0:
            lista_medicamentos = Medicacion.objects.filter(id__in=medicamentos)
            socio.medicaciones.set(lista_medicamentos)
        else: 
            pass
        # messages.success(request, "Socio registrado con éxito.")
        return JsonResponse( { "success": True, "mensaje": "Socio registrado con éxito. Diríjase a secretaría con el siguiente código: " + str(nro_inscripcion) }, status=200)
    except Exception as e:
        return JsonResponse({ "error": str(e) }, status=400)


def verificar_cuil(request, cuil):
    try:
        validar_cuit(cuil)
    except:
        return JsonResponse({'invalido': True})    
    cuil_existente = Socio.objects.filter(CUIL=cuil).exists()
    return JsonResponse({'registrado': cuil_existente})

def verificar_dni(request, dni):  
    dni_existente = Socio.objects.filter(nro_documento=dni).exists()

    return JsonResponse({'registrado': dni_existente})

def verificar_email(request, email):  
    email_existente = Socio.objects.filter(email_socio=email).exists()

    return JsonResponse({'registrado': email_existente})


