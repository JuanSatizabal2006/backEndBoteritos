from django.urls import path

from .views.trimestreViews import TrimestresView, TrimestresList
from .views.logrosViews import LogrosViews, ListLogrosAdmin, ListLogrosProfesor
from .views.calificarViews import CalificarList, CalificarSave, CalificarSend
from .views.informeViews import InformeList, CreateInforme, InformesEstudiantesList, InformeEstudianteOne

urlpatterns= [
    path('trimestre/', TrimestresView),
    path('trimestre/<str:fecha>/', TrimestresList),
    path('logro/', LogrosViews), #CREAR Y ACTUALIZAR LOGROS
    path('listlogros/admin/<int:idtrim>/', ListLogrosAdmin), #LISTADO DE LOGROS PARA QUE EL ADMIN LO VISUALICE
    path('listlogros/profesor/<int:idtrim>/<int:idprof>/', ListLogrosProfesor), #LISTAR LOGROS PARA QUE EL PROFESOR VISUALICE LO QUE HA CREADO
    path('calificar/<int:idtrim>/<int:idprof>/<int:idestud>/', CalificarList), #LISTAR LOGROS PARA QUE LOS PROFESORES PUEDAN CALIFICAR, ESTO ESTA RELACIONADO CON LA TABLA LOGROSESTUDIANTE
    path('calificar/guardar/', CalificarSave),
    path('calificar/enviar/', CalificarSend),
    
    path('informe/list/<int:idtrim>/<int:idarea>/<int:idestud>/', InformeList),
    path('informe/create/', CreateInforme),
    path('informe/estudiante/<int:idstud>/', InformesEstudiantesList),
    path('informe/estudiante/one/<int:idinform>/', InformeEstudianteOne)
]