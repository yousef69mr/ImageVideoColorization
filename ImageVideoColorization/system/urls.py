
from django.urls import path,include
from .views import(
    colorizationModelView,
    process_form_view
)
urlpatterns = [
    path('',colorizationModelView),
    path('process_form/',process_form_view)
]
