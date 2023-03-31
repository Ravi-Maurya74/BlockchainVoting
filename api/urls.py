from django.urls import path
from api import views

urlpatterns = [
    # path("test/", views.test),
    path("createVoter/", views.NewVoter.as_view()),
    path("createNewElection/", views.newElection),
    path("getElectionResult/", views.getElectionResult),
    path("castVote/", views.castVote),
    path("verifyVote/", views.verifyVote),
]
