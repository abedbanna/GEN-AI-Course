from django.urls import path

from . import views

urlpatterns = [
    path("translate", views.translate_text_view, name="translate"),
    path("feedback", views.email_response_view, name="feedback"),
    path("review", views.customer_review_view, name="review"),
    path("", views.index, name="index"),
]