# utils/email_notificaciones.py
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import List
from datetime import datetime

from config.settings import settings
from models.citas import Cita
from sqlalchemy.orm import Session
from models.ninos import Nino
from models.tutores import Tutor
from models.personal import Personal
from models.usuarios import Usuario
from models.terapias import Terapia
# al inicio
from models.ninos_prospecto import NinoProspecto


def _enviar_correo(subject: str, body_html: str, destinatarios: List[str]):
    if not destinatarios:
        return

    msg = MIMEMultipart("alternative")
    msg["From"] = f"{settings.SMTP_FROM_NAME} <{settings.SMTP_FROM_EMAIL}>"
    msg["To"] = ", ".join(destinatarios)
    msg["Subject"] = subject

    msg.attach(MIMEText(body_html, "html", "utf-8"))

    with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
        server.starttls()
        server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
        server.sendmail(settings.SMTP_FROM_EMAIL, destinatarios, msg.as_string())


def _formatear_fecha_hora(fecha, hora) -> str:
    if not fecha or not hora:
        return "sin fecha/hora"
    dt = datetime.combine(fecha, hora)
    # Ej: Lunes 17 de Noviembre 2025, 10:00 AM
    return dt.strftime("%A %d de %B de %Y, %H:%M").capitalize()


def obtener_correos_tutor_y_terapeuta(cita: Cita, db: Session) -> list[str]:
    correos: list[str] = []

    # Terapeuta -> personal -> usuarios
    if cita.id_personal:
        personal = db.query(Personal).filter(Personal.id_personal == cita.id_personal).first()
        if personal and personal.id_usuario:
            u = db.query(Usuario).filter(Usuario.id_usuario == personal.id_usuario).first()
            if u and u.correo:
                correos.append(u.correo)

    # Tutor -> ninos -> tutores -> usuarios
    if cita.id_nino:
        nino = db.query(Nino).filter(Nino.id_nino == cita.id_nino).first()
        if nino and nino.id_tutor:
            tutor = db.query(Tutor).filter(Tutor.id_tutor == nino.id_tutor).first()
            if tutor and tutor.id_usuario:
                u = db.query(Usuario).filter(Usuario.id_usuario == tutor.id_usuario).first()
                if u and u.correo:
                    correos.append(u.correo)

    # Si no hay niño formal pero sí prospecto
    if not cita.id_nino and cita.id_nino_prospecto:
        prospecto = db.query(NinoProspecto).filter(
            NinoProspecto.id_nino_prospecto == cita.id_nino_prospecto
        ).first()
        if prospecto and prospecto.correo_contacto:
            correos.append(prospecto.correo_contacto)

    # evitar repetidos
    return list(set(correos))


def obtener_nombres_relacionados(cita: Cita, db: Session):
    nombre_nino = None
    nombre_terapeuta = None
    nombre_terapia = None

    if cita.id_nino:
        nino = db.query(Nino).filter(Nino.id_nino == cita.id_nino).first()
        if nino:
            nombre_nino = f"{nino.nombre} {nino.apellido_paterno or ''} {nino.apellido_materno or ''}".strip()

    if cita.id_personal:
        personal = db.query(Personal).filter(Personal.id_personal == cita.id_personal).first()
        if personal and personal.id_usuario:
            u = db.query(Usuario).filter(Usuario.id_usuario == personal.id_usuario).first()
            if u:
                nombre_terapeuta = f"{u.nombre} {u.apellido_paterno or ''} {u.apellido_materno or ''}".strip()

    if cita.id_terapia:
        terapia = db.query(Terapia).filter(Terapia.id_terapia == cita.id_terapia).first()
        if terapia:
            nombre_terapia = terapia.nombre_terapia

    return nombre_nino, nombre_terapeuta, nombre_terapia


def enviar_notificacion_cita_creada(cita: Cita, db: Session):
    correos = obtener_correos_tutor_y_terapeuta(cita, db)
    if not correos:
        return

    nombre_nino, nombre_terapeuta, nombre_terapia = obtener_nombres_relacionados(cita, db)
    fecha_hora = _formatear_fecha_hora(cita.fecha, cita.hora)

    subject = "📅 Nueva cita programada - Autismo Mochis IA"

    body = f"""
    <h2>Nueva cita programada</h2>
    <p><strong>Paciente:</strong> {nombre_nino or 'No asignado'}</p>
    <p><strong>Terapeuta:</strong> {nombre_terapeuta or 'No asignado'}</p>
    <p><strong>Servicio:</strong> {nombre_terapia or 'No especificado'}</p>
    <p><strong>Fecha y hora:</strong> {fecha_hora}</p>
    <p><strong>Tipo:</strong> {cita.tipo or 'Individual'}</p>
    <p><strong>Notas:</strong> {cita.notas or 'Sin notas adicionales'}</p>
    <hr>
    <p>Este mensaje fue enviado automáticamente por el sistema Autismo Mochis IA.</p>
    """

    _enviar_correo(subject, body, correos)


def enviar_notificacion_cita_cancelada(cita: Cita, db: Session):
    correos = obtener_correos_tutor_y_terapeuta(cita, db)
    if not correos:
        return

    nombre_nino, nombre_terapeuta, nombre_terapia = obtener_nombres_relacionados(cita, db)
    fecha_hora = _formatear_fecha_hora(cita.fecha, cita.hora)

    subject = "❌ Cita cancelada - Autismo Mochis IA"

    body = f"""
    <h2>Cita cancelada</h2>
    <p><strong>Paciente:</strong> {nombre_nino or 'No asignado'}</p>
    <p><strong>Terapeuta:</strong> {nombre_terapeuta or 'No asignado'}</p>
    <p><strong>Servicio:</strong> {nombre_terapia or 'No especificado'}</p>
    <p><strong>Fecha y hora original:</strong> {fecha_hora}</p>
    <p>Si tienes dudas, comunícate con el centro.</p>
    <hr>
    <p>Este mensaje fue enviado automáticamente por el sistema Autismo Mochis IA.</p>
    """

    _enviar_correo(subject, body, correos)
