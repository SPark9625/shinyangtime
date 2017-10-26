from django.conf.urls import url
from response import views

app_name = "response"
urlpatterns = [
	url(r"^keyboard/", views.keyboard),
	url(r"^message", views.answer),
]