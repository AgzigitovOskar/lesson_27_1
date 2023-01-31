from rest_framework import serializers

from vacancies.models import Vacancy


# Сериализаторы модели
class VacancyListSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    skills = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field="name"
    )

    class Meta:
        model = Vacancy
        fields = ["id", "text", "slug", "status", "created", "username", "skills"]


class VacancyDetailSerializer(serializers.ModelSerializer):
    skills = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field="name"
    )

    class Meta:
        model = Vacancy
        fields = '__all__'


class VacancyCreateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = Vacancy
        exclude = ["skills"]


# Простые сериализаторы
# class VacancySerializer(serializers.Serializer):
#     id = serializers.IntegerField()
#     text = serializers.CharField(max_length=2000)
#     slug = serializers.CharField(max_length=50)
#     status = serializers.CharField(max_length=6)
#     created = serializers.DateTimeField()
#     username = serializers.CharField(max_length=100)

