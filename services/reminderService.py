from datetime import datetime, timedelta
from config.connection import db
from models.recoleccionModel import Recoleccion
from models.userModel import User
from services.whatsappService import whatsapp_service
from sqlalchemy.exc import SQLAlchemyError
from services.notificationService import NotificationService
import threading
import time
from apscheduler.schedulers.background import BackgroundScheduler

class ReminderService:
    def __init__(self):
        self.scheduler = BackgroundScheduler()
        self.app = None  # Referencia a la aplicación Flask
        
    def init_app(self, app):
        """Inicializar con la aplicación Flask"""
        self.app = app
        
    def schedule_individual_reminders(self):
        """
        Programa un job individual para cada recolección futura
        """
        if not self.app:
            print("Error: Aplicación Flask no inicializada")
            return
            
        try:
            with self.app.app_context():
                # Limpiar jobs existentes primero
                self.clear_existing_reminder_jobs()
                
                # Buscar recolecciones futuras (próximas 48 horas)
                ahora = datetime.now()
                limite_futuro = ahora + timedelta(hours=48)
                
                print(f"Buscando recolecciones futuras desde {ahora} hasta {limite_futuro}")
                
                recolecciones_futuras = Recoleccion.query.filter(
                    Recoleccion.fechaRecoleccion >= ahora.date(),
                    Recoleccion.fechaRecoleccion <= limite_futuro.date(),
                    Recoleccion.cumplimiento == 0,
                    Recoleccion.notificado == 0  # SOLO las que no han sido notificadas
                ).all()
                
                print(f"Encontradas {len(recolecciones_futuras)} recolecciones futuras sin notificar")
                
                recolecciones_programadas = 0
                recolecciones_por_lote = {}
                
                # Agrupar por NoRecoleccion para evitar duplicados
                for recoleccion in recolecciones_futuras:
                    if recoleccion.NoRecoleccion:
                        if recoleccion.NoRecoleccion not in recolecciones_por_lote:
                            recolecciones_por_lote[recoleccion.NoRecoleccion] = recoleccion
                    else:
                        # Recolección individual
                        self.schedule_single_reminder(recoleccion)
                        recolecciones_programadas += 1
                
                # Programar una por lote 
                for no_recoleccion, recoleccion in recolecciones_por_lote.items():
                    self.schedule_single_reminder(recoleccion)
                    recolecciones_programadas += 1
                
                print(f"Programados {recolecciones_programadas} recordatorios individuales")
                
        except Exception as e:
            print(f"Error programando recordatorios individuales: {str(e)}")
    
    def schedule_single_reminder(self, recoleccion):
        """
        Programa un recordatorio individual para una recolección
        """
        try:
            # Calcular cuándo enviar el recordatorio (1 hora antes)
            fecha_hora_recoleccion = datetime.combine(
                recoleccion.fechaRecoleccion, 
                recoleccion.horaRecoleccion
            )
            tiempo_recordatorio = fecha_hora_recoleccion - timedelta(hours=1)
            
            # Si el recordatorio es en el futuro, programarlo
            if tiempo_recordatorio > datetime.now():
                # Usar NoRecoleccion como identificador único
                job_id = f"reminder_{recoleccion.NoRecoleccion}"
                
                self.scheduler.add_job(
                    self.send_single_reminder,
                    'date',
                    run_date=tiempo_recordatorio,
                    args=[recoleccion.NoRecoleccion], 
                    id=job_id
                )
                
                print(f"Recordatorio programado para {tiempo_recordatorio} (recolección {recoleccion.NoRecoleccion})")
            else:
                print(f"Recolección {recoleccion.NoRecoleccion} ya pasó o el recordatorio sería en el pasado")
                
        except Exception as e:
            print(f"Error programando recordatorio individual: {str(e)}")
    
    def send_single_reminder(self, no_recoleccion):
        """
        Envía un recordatorio para una recolección específica
        """
        if not self.app:
            print("Error: Aplicación Flask no inicializada")
            return
            
        try:
            with self.app.app_context():
                # Buscar la recolección por NoRecoleccion
                recoleccion = Recoleccion.query.filter_by(
                    NoRecoleccion=no_recoleccion,
                    cumplimiento=0,
                    notificado=0  # si no ha sido notificada
                ).first()
                
                if recoleccion:
                    print(f"Enviando recordatorio programado para recolección {recoleccion.NoRecoleccion}")
                    exito = self.send_reminder_for_recoleccion(recoleccion)
                    if exito:
                        # MARCAR COMO NOTIFICADO
                        recoleccion.notificado = 1
                        db.session.commit()
                        print(f"Recordatorio enviado y marcado (notificado=1) para recolección {recoleccion.NoRecoleccion}")
                    else:
                        print(f"Error enviando recordatorio para recolección {recoleccion.NoRecoleccion}")
                        # No marcamos como notificado si falló, para reintentar después
                else:
                    print(f"Recolección {no_recoleccion} no encontrada, ya cumplida o YA NOTIFICADA (notificado=1)")
                    
        except Exception as e:
            print(f"Error enviando recordatorio individual: {str(e)}")
            try:
                with self.app.app_context():
                    db.session.rollback()
            except:
                pass
    
    def clear_existing_reminder_jobs(self):
        """
        Limpia todos los jobs de recordatorios existentes
        """
        try:
            jobs = self.scheduler.get_jobs()
            jobs_eliminados = 0
            for job in jobs:
                if job.id.startswith('reminder_'):
                    job.remove()
                    jobs_eliminados += 1
            print(f"Jobs de recordatorios anteriores eliminados: {jobs_eliminados}")
        except Exception as e:
            print(f"Error limpiando jobs: {str(e)}")
    
    def send_reminder_for_recoleccion(self, recoleccion):
        """
        Envía recordatorio para una recolección específica
        """
        try:
            # Obtener información del usuario
            usuario = User.query.get(recoleccion.id_usuario)
            if not usuario or not usuario.telefono:
                print(f"Usuario {recoleccion.id_usuario} no encontrado o sin teléfono")
                return False
            
            # Formatear teléfono
            telefono = NotificationService.formatear_telefono_whatsapp(usuario.telefono)
            if not telefono:
                print(f"Teléfono no válido para usuario {usuario.id}")
                return False
            
            # Obtener todos los medicamentos de esta recolección (por si es batch)
            if recoleccion.NoRecoleccion:
                # Es una recolección batch, obtener todos los medicamentos
                recolecciones_batch = Recoleccion.query.filter_by(
                    NoRecoleccion=recoleccion.NoRecoleccion
                ).all()
                
                medicamentos = []
                for rec in recolecciones_batch:
                    if rec.medicamento:
                        medicamentos.append(rec.medicamento.nombreMedicamento)
            else:
                # Recolección individual
                medicamentos = [recoleccion.medicamento.nombreMedicamento] if recoleccion.medicamento else ["Medicamento no especificado"]
            
            # Formatear fecha y hora
            fecha_str = recoleccion.fechaRecoleccion.strftime("%d/%m/%Y")
            hora_str = recoleccion.horaRecoleccion.strftime("%I:%M %p")
            
            # Enviar recordatorio por WhatsApp
            exito = whatsapp_service.send_recoleccion_reminder(
                to_number=telefono,
                nombre_paciente=f"{usuario.nombre} {usuario.apellidos}",
                no_recoleccion=recoleccion.NoRecoleccion,
                fecha_recoleccion=fecha_str,
                hora_recoleccion=hora_str,
                sede=recoleccion.sede.nombreSede if recoleccion.sede else "Sede no especificada",
                medicamentos=medicamentos
            )
            
            if exito:
                print(f"Recordatorio enviado a {usuario.nombre} para recolección {recoleccion.NoRecoleccion}")
                print(f"   Fecha: {fecha_str} Hora: {hora_str}")
                return True
            else:
                print(f"Error enviando recordatorio a {usuario.nombre}")
                return False
            
        except Exception as e:
            print(f"Error en send_reminder_for_recoleccion: {str(e)}")
            return False
    
    def check_pending_reminders_backup(self):
        """
        Verificación de respaldo por si algún job falló
        Busca recolecciones que deberían haberse notificado pero aún tienen notificado=0
        """
        if not self.app:
            print("Error: Aplicación Flask no inicializada")
            return 0
            
        try:
            with self.app.app_context():
                ahora = datetime.now()
                print(f"🔍 Verificación de respaldo - {ahora}")
                
                # Buscar recolecciones que:
                # - Son para hoy o pasado
                # - La hora de recolección ya pasó (o está muy próxima)
                # - cumplimiento = 0 (no cumplidas)
                # - notificado = 0 (no notificadas)
                # - En un rango de hasta 2 horas atrás (por si algún job falló)
                
                tiempo_limite_inferior = ahora - timedelta(hours=2)
                tiempo_limite_superior = ahora + timedelta(minutes=15)  # Incluir las próximas 15 min
                
                recolecciones_pendientes = Recoleccion.query.filter(
                    Recoleccion.fechaRecoleccion >= tiempo_limite_inferior.date(),
                    Recoleccion.fechaRecoleccion <= ahora.date(),
                    Recoleccion.cumplimiento == 0,
                    Recoleccion.notificado == 0  # SOLO las no notificadas
                ).all()
                
                # Filtrar por hora también
                recolecciones_filtradas = []
                for rec in recolecciones_pendientes:
                    fecha_hora_recoleccion = datetime.combine(rec.fechaRecoleccion, rec.horaRecoleccion)
                    # Si la recolección fue en las últimas 2 horas o en los próximos 15 minutos
                    if tiempo_limite_inferior <= fecha_hora_recoleccion <= tiempo_limite_superior:
                        recolecciones_filtradas.append(rec)
                
                print(f"Encontradas {len(recolecciones_filtradas)} recolecciones pendientes en verificación de respaldo")
                
                recordatorios_enviados = 0
                for recoleccion in recolecciones_filtradas:
                    exito = self.send_reminder_for_recoleccion(recoleccion)
                    if exito:
                        # MARCAR COMO NOTIFICADO = 1
                        recoleccion.notificado = 1
                        db.session.commit()
                        recordatorios_enviados += 1
                        print(f"Recordatorio de respaldo enviado y marcado (notificado=1) para recolección {recoleccion.NoRecoleccion}")
                    else:
                        print(f"Error en recordatorio de respaldo para recolección {recoleccion.NoRecoleccion}")
                
                return recordatorios_enviados
                
        except Exception as e:
            print(f"Error en check_pending_reminders_backup: {str(e)}")
            return 0
    
    def start_daily_reminders(self):
        """
        Inicia el sistema de recordatorios con jobs individuales
        """
        if not self.app:
            print("Error: Aplicación Flask no inicializada")
            return
            
        try:
            # Iniciar el scheduler solo si no está ya corriendo
            if not self.scheduler.running:
                self.scheduler.start()
                print("Scheduler iniciado")
            
            # 1. Programar recordatorios individuales al iniciar
            self.schedule_individual_reminders()
            
            # 2. Verificación de respaldo cada 30 minutos
            self.scheduler.add_job(
                self.check_pending_reminders_backup,
                'interval',
                minutes=30,
                id='backup_check'
            )
            
            # 3. Actualizar jobs individuales cada 6 horas (para nuevas recolecciones)
            self.scheduler.add_job(
                self.schedule_individual_reminders,
                'interval',
                hours=6,
                id='refresh_schedule'
            )
            
            # 4. También actualizar a medianoche para el día siguiente
            self.scheduler.add_job(
                self.schedule_individual_reminders,
                'cron',
                hour=0,
                minute=1,
                id='midnight_refresh'
            )
            
            print(" Sistema de recordatorios individuales iniciado")
            print("   - Jobs individuales programados para cada recolección")
            print("   - Verificación de respaldo cada 30 minutos")
            print("   - Actualización de schedule cada 6 horas y a medianoche")
            print("   - NOTIFICADO=0 → Envía mensaje y marca NOTIFICADO=1")
            print("   - NOTIFICADO=1 → No envía mensaje (ya fue notificado)")
            
        except Exception as e:
            print(f"Error iniciando sistema de recordatorios: {str(e)}")
    
    def stop_reminders(self):
        """
        Detiene el scheduler de recordatorios
        """
        try:
            if self.scheduler.running:
                self.scheduler.shutdown()
            print("Scheduler de recordatorios detenido")
        except Exception as e:
            print(f"Error deteniendo scheduler: {str(e)}")
    
    def get_scheduled_reminders(self):
        """
        Obtiene la lista de recordatorios programados (para debugging)
        """
        try:
            jobs = self.scheduler.get_jobs()
            reminder_jobs = [job for job in jobs if job.id.startswith('reminder_')]
            
            print(f"Recordatorios programados: {len(reminder_jobs)}")
            for job in reminder_jobs:
                print(f"   - {job.id} -> {job.next_run_time}")
            
            return reminder_jobs
        except Exception as e:
            print(f"Error obteniendo recordatorios programados: {str(e)}")
            return []

# Instancia global del servicio
reminder_service = ReminderService()