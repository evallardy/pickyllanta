from django_cron import CronJobBase, Schedule
from core.views import leer

from core.views import leer

class LeerCron(CronJobBase):
    RUN_EVERY_MINS = 1  # Intervalo mínimo, no afecta a la programación de cron

    schedule = Schedule(run_at_times=['09:00', '11:00'])
    code = 'core.cron.leer_cron'  # Identificador único para el cron

    def do(self):
        leer()  # Llama a la función leer() de la aplicación core
