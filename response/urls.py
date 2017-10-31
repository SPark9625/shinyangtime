from django.conf.urls import url
from response import views

app_name = "response"
urlpatterns = [
	url(r"^keyboard/", views.keyboard, name="keyboard"),
	url(r"^message", views.answer, name="answer"),
	url(r"^view/", views.view, name="view"),
	url(r"^proposal/", views.proposal, name="proposal"),
	# url(r"^thanks/", views.thanks, name="thanks")
]