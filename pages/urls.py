from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("informatii/", views.informatii, name="informatii"),
    path("calendar/", views.calendar_page, name="calendar"),
    path("parteneri/", views.parteneri, name="parteneri"),
    path("surse/", views.surse, name="surse"),
    path("subiecte/", views.subiecte, name="subiecte"),
    path("rezultate/", views.rezultate, name="rezultate"),
    path("arhiva/", views.arhiva, name="arhiva"),
    path("tematica/", views.tematica, name="tematica"),
    path("regulament/", views.regulament, name="regulament"),
    path("galerie/", views.galerie, name="galerie"),
]