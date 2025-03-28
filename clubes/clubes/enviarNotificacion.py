from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import environ
from pathlib import Path
import requests

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = str(Path(__file__).resolve().parent.parent) + "/clubes"


# ENV
env = environ.Env(
   HOST=(str, None),
)

environ.Env.read_env(f'{BASE_DIR}/.env')


def enviarEmailSocio(socio, msj):
    try:
        if socio.usa_email:
            mail_server = smtplib.SMTP(env('EMAIL_HOST'), env('EMAIL_PORT'))
            mail_server.ehlo()
            mail_server.starttls()
            mail_server.ehlo()
            mail_server.login(env('EMAIL_HOST_USER'), env('EMAIL_HOST_PASSWORD'))
            mensaje = MIMEMultipart()
            mensaje.attach(MIMEText(msj.texto, 'plain'))
            email = env('EMAIL_HOST_USER')
            mensaje['From'] = email
            mensaje['To'] = socio.email_socio
            mensaje['Subject'] = msj.referencia
            mail_server.sendmail(email, socio.email_socio, mensaje.as_string())

            msj.estado = 'E'
            msj.save()

    except Exception as error:
        pass


def enviarMensajeMail(obj):
    if(obj.categoria):
        socios =  obj.categoria.getSocios()
        for socio in socios:
            enviarEmailSocio(socio.socio, obj)
    elif(obj.disciplina):
        socios =  obj.disciplina.getSocios()
        for socio in socios:
            enviarEmailSocio(socio.socio, obj)
    else:
        socios =  obj.club.getSocios()
        for socio in socios:
            enviarEmailSocio(socio, obj)

'''def enviarMensajeT(obj):
    # Obtén el token de API del bot
    token = env('TELEGRAM_BOT_TOKEN')
    # Envía un mensaje de texto
    url = "https://api.telegram.org/bot{}/sendMessage".format(token)
    if(obj.disciplina):
        msj = obj.texto
        print(obj.disciplina.grupo_telegram, "Grupo TELEGRAM")
        data = {"chat_id": -1002405852068, "text": msj}
        response = requests.post(url, data=data)

        if response.status_code == 200:
            obj.estado = 'E'
            obj.save()
        # Imprime el resultado de la respuesta
        print(response.content)'''


def enviarMensajeT(obj):
    
    token = env('TELEGRAM_BOT_TOKEN')
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    grupos_telegram = []

    # Si se seleccionó una disciplina pero no una categoría específica
    if obj.disciplina and not obj.categoria:
        categorias = obj.disciplina.categoria_set.all()
        for categoria in categorias:
            if categoria.grupo_telegram:
                grupos_telegram.append(categoria.grupo_telegram)
    
    # Si se seleccionó una categoría específica
    elif obj.categoria:
        grupos_telegram.append(obj.categoria.grupo_telegram)
    
    msg_error = ""
    
    # Si hay grupos de Telegram para enviar
    for grupo_telegram in grupos_telegram:
        try:
            msj = obj.texto
            data = {
                "chat_id": grupo_telegram, 
                "text": msj
            }
            response = requests.post(url, data=data)
            
            if response.status_code != 200:
                msg_error += f"Error al enviar mensaje a {grupo_telegram}. Código de estado: {response.status_code} - "
        
        except Exception as error:
            msg_error += f"Error al enviar mensaje a {grupo_telegram} - "
    
    if msg_error == "":
        return "OK"
    else:
        return msg_error

def enviar(obj):

    if(obj.medio == 'T'):
        return enviarMensajeT(obj)
    elif(obj.medio == 'E'):
        return enviarMensajeMail(obj)
    else:
        env_t = enviarMensajeT(obj)
        env_e = enviarMensajeMail(obj)
        if env_t == "OK" and env_e == "OK":
            return "OK"
        elif env_t != "OK":
            return "ERROR Telefgram " + env_t
        else:
            return "ERROR Email " + env_e
