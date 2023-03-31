from rest_framework import serializers
import json
from .models import Voter, Election, Choice


class VoterSerialzer(serializers.ModelSerializer):
    class Meta:
        model = Voter
        fields = [
            "name",
            "user_email",
            "password",
            "admin",
            "voted_in",
        ]


class ElectionSerializer(serializers.ModelSerializer):
    choices_name = serializers.SerializerMethodField()

    def get_choices_name(self, instance):
        result = []
        for choice in instance.choices.all():
            result.append(choice.name)
        return result

    class Meta:
        model = Election
        fields = [
            "id",
            "title",
            "number_of_choices",
            "choices",
            "choices_name",
        ]


class ChoiceSerialzer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = [
            "name",
            "choice_id",
        ]
