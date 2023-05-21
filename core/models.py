from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db import models

ESTATUS_MENSAJE = (
    (0, 'Terminado'),
    (1, 'Activo'),
)

class MensajePicky(models.Model, PermissionRequiredMixin):
    token = models.CharField("Token", max_length=255, null=True, blank=True)
    number = models.CharField("Number", max_length=50)                                 # Number
    message_in = models.CharField("Mensage in", max_length=255)                        # Message_in
    message_in_raw = models.CharField("Mensaje in raw", max_length=255)                # Message_in_raw
    message = models.CharField("Mensaje", max_length=255, null=True, blank=True)
    application = models.CharField("Aplicación", max_length=255, null=True, blank=True)# Application
    tipo = models.CharField("Type", max_length=255, default=2)                         # Tipo 
    unique_id = models.CharField("Unique id", max_length=255, null=True, blank=True)
    quoted = models.CharField("Quoted", max_length=255, null=True, blank=True)
    estatus_mensaje = models.IntegerField("Estatus del mensaje", choices=ESTATUS_MENSAJE, default=1)
    fecha_alta = models.DateTimeField("Fecha alta", auto_now_add=True)                 # fecha alta
    nivel = models.IntegerField("Nivel de pregunta", default=1)
    opcion1 = models.JSONField("Acción", null=True, blank=True)
    opcion2 = models.JSONField("Bien", null=True, blank=True)
    opcion3 = models.JSONField("Estado", null=True, blank=True)
    opcion4 = models.JSONField("Municipio", null=True, blank=True)
    opcion5 = models.JSONField("Bien seleccionado", null=True, blank=True)

    class Meta:
        verbose_name = 'Mensaje picky'
        verbose_name_plural = 'Mensajes picky'
        ordering = ['number','-fecha_alta',]
        db_table = 'MensajePicky'

class Bitacora(models.Model, PermissionRequiredMixin):
    descripcion = models.CharField("Descripción", max_length=255)
    fecha = models.DateTimeField("Fecha", auto_now_add=True)
    
    class Meta:
        verbose_name = 'Registro'
        verbose_name_plural = 'Registros'
        ordering = ['-fecha']
        db_table = 'Bitcora'
    
    def __str__(self):
        return '%s - %s' % (self.fecha, self.descripcion)

class Llanta(models.Model, PermissionRequiredMixin):
    # Datos extraídos
    producto_clave = models.CharField("Producto/Clave",max_length=100, blank=True, null=True)
    descripcion = models.CharField("Descripción", max_length=255, blank=True, null=True)
    existencia = models.IntegerField("Existencia", default=0)
    costo_promedio_pesos = models.DecimalField("Costo Promedio Pesos", decimal_places=2, max_digits=10, default=0)
    tipo = models.CharField("Tipo",max_length=50, blank=True, null=True)
    subtipo = models.CharField("Subtipo",max_length=50, blank=True, null=True)
    capas = models.IntegerField("Capas", default=0)
    precio_especia_llantashop_pago_efectivo = models.DecimalField("Precio Especia LLANTASHOP pago Efectivo", decimal_places=2, max_digits=10, default=0)
    msi_3 = models.DecimalField("3 MSI", decimal_places=2, max_digits=10, default=0)
    msi_6 = models.DecimalField("6 MSI", decimal_places=2, max_digits=10, default=0)
    msi_9 = models.DecimalField("9 MSI", decimal_places=2, max_digits=10, default=0)
    msi_12 = models.DecimalField("12 MSI", decimal_places=2, max_digits=10, default=0)
    msi_18 = models.DecimalField("18 MSI", decimal_places=2, max_digits=10, default=0)
    envio = models.DecimalField("Envio", decimal_places=2, max_digits=10, default=0)
    utilidad = models.DecimalField("Utilidad", decimal_places=2, max_digits=10, default=0)
    afiliado = models.DecimalField("Afiliado", decimal_places=2, max_digits=10, default=0)
    actualizado = models.IntegerField("Actualizado en el proceso de extracción", default=1)
    # Datos separados
    ancho = models.CharField("Ancho",max_length=10, blank=True, null=True)
    alto = models.CharField("Alto",max_length=10, blank=True, null=True)
    rin = models.CharField("Rin",max_length=10, blank=True, null=True)
    radial = models.IntegerField("Radial", default=0)
    marca = models.CharField("Marca",max_length=100, blank=True, null=True)
    # Bitácora
    creado = models.DateTimeField("Creado", auto_now_add=True)
    modificado = models.DateTimeField("Actualizado", auto_now=True)


    class Meta:
        verbose_name = 'Llanta' 
        verbose_name_plural = 'Llantas' 
        ordering = ['producto_clave']
        db_table = 'Llanta'
