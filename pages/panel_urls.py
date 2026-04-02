from django.urls import path

from . import panel_views

urlpatterns = [
    path("", panel_views.panel_login_view, name="panel_root"),
    path("login/", panel_views.panel_login_view, name="panel_login"),
    path("logout/", panel_views.panel_logout_view, name="panel_logout"),
    path("dashboard/", panel_views.panel_dashboard, name="panel_dashboard"),

    # Rezultate
    path("rezultate/", panel_views.panel_rezultate, name="panel_rezultate"),
    path("rezultate/<int:year_id>/", panel_views.panel_rezultate_year, name="panel_rezultate_year"),
    path("rezultate/<int:year_id>/delete/", panel_views.panel_rezultate_year_delete, name="panel_rezultate_year_delete"),
    path("rezultate/<int:year_id>/<int:judet_id>/", panel_views.panel_rezultate_judet, name="panel_rezultate_judet"),
    path("rezultate/<int:year_id>/<int:judet_id>/delete/", panel_views.panel_rezultate_judet_delete, name="panel_rezultate_judet_delete"),
    path("rezultate/<int:year_id>/<int:judet_id>/<int:etapa_id>/", panel_views.panel_rezultate_etapa, name="panel_rezultate_etapa"),
    path("rezultate/<int:year_id>/<int:judet_id>/<int:etapa_id>/delete/", panel_views.panel_rezultate_etapa_delete, name="panel_rezultate_etapa_delete"),
    path("rezultate/<int:year_id>/<int:judet_id>/<int:etapa_id>/<int:doc_id>/delete/", panel_views.panel_rezultate_doc_delete, name="panel_rezultate_doc_delete"),

    # Config
    path("config/", panel_views.panel_config, name="panel_config"),

    # Arhiva
    path("arhiva/", panel_views.panel_arhiva, name="panel_arhiva"),
    path("arhiva/<int:folder_id>/", panel_views.panel_arhiva_folder, name="panel_arhiva_folder"),
    path("arhiva/<int:folder_id>/delete/", panel_views.panel_arhiva_folder_delete, name="panel_arhiva_folder_delete"),
    path("arhiva/<int:folder_id>/<int:doc_id>/delete/", panel_views.panel_arhiva_doc_delete, name="panel_arhiva_doc_delete"),
]
