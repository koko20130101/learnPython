from django.conf.urls import url, include
from .views import LoginView

urlpatterns = [
    url('login/', LoginView.as_view())
]
