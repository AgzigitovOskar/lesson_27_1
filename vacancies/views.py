import json

from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Count, Avg
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView

from hunting import settings
from vacancies.models import Vacancy, Skill
from vacancies.serializers import VacancyListSerializer, VacancyDetailSerializer, VacancyCreateSerializer, \
    VacancyUpdateSerializer, VacancyDestroySerializer


def hello(request):
    return HttpResponse("Hello world")


class VacancyListView(ListAPIView):
    queryset = Vacancy.objects.all()
    serializer_class = VacancyListSerializer

    # def get(self, request, *args, **kwargs):
    #     super().get(request, *args, **kwargs)
    #
    #     search_text = request.GET.get("text", None)
    #     if search_text:
    #         self.object_list = self.object_list.filter(text=search_text)
    #
    #     self.object_list = self.object_list.select_related("user").prefetch_related("skills").order_by("text")
    #
    #     # response =[]
    #     # for vacancy in self.object_list:
    #     #     response.append({
    #     #         "id": vacancy.id,
    #     #         "text": vacancy.text
    #     #     })
    #
    #     paginator = Paginator(self.object_list, settings.TOTAL_ON_PAGE)
    #     page_number = request.GET.get("page")
    #     page_obj = paginator.get_page(page_number)
    #
    #     # vacancies = []
    #     # for vacancy in page_obj:
    #     #     vacancies.append({
    #     #         "id": vacancy.id,
    #     #         "text": vacancy.text,
    #     #         "slug": vacancy.slug,
    #     #         "status": vacancy.status,
    #     #         "created": vacancy.created,
    #     #         "username": vacancy.user.username,
    #     #         "skills": list(map(str, vacancy.skills.all())),
    #     #     })
    #     list(map(lambda x: setattr(x, "username", x.user.username if x.user else None), page_obj))
    #
    #     response = {
    #         "items": VacancyListSerializer(page_obj, many=True).data,
    #         "num_pages": paginator.num_pages,
    #         "total": paginator.count
    #     }
    #
    #     return JsonResponse(response, safe=False)


class VacancyDetailView(RetrieveAPIView):
    # model = Vacancy
    queryset = Vacancy.objects.all()
    serializer_class = VacancyDetailSerializer

    # def get(self, request, *args, **kwargs):
    #     vacancy = self.get_object()
    #
    #     return JsonResponse(VacancyDetailSerializer(vacancy).data)


# @method_decorator(csrf_exempt, name="dispatch")
class VacancyCreateView(CreateAPIView):
    queryset = Vacancy.objects.all()
    serializer_class = VacancyCreateSerializer

    # def post(self, request, *args, **kwargs):
    #     vacancy_data = VacancyCreateSerializer(data=json.loads(request.body))
    #     if vacancy_data.is_valid():
    #         vacancy_data.save()
    #     else:
    #         return JsonResponse(vacancy_data.errors)
    #
    #     # vacancy = Vacancy.objects.create(
    #     #     # user_id = vacancy_data["user_id"],
    #     #     slug=vacancy_data["slug"],
    #     #     text=vacancy_data["text"],
    #     #     status=vacancy_data["status"]
    #     # )
    #     #
    #     # vacancy.user = get_object_or_404(User, pk=vacancy_data["user_id"])
    #
    #     # for skill in vacancy_data["skills"]:
    #     #     try:
    #     #         skill_obj = Skill.objects.get(name=skill)
    #     #     except Skill.DoesNotExist:
    #     #         skill_obj = Skill.objects.create(name=skill)
    #     #     vacancy.skills.add(skill_obj)
    #     # vacancy.save()
    #
    #        # тоже самое
    #     # for skill in vacancy_data["skills"]:
    #     #     skill_obj, created = Skill.objects.get_or_create(
    #     #         name=skill,
    #     #         defaults={
    #     #             "is_active": True
    #     #         }
    #     #     )
    #     #     vacancy.skills.add(skill_obj)
    #     # vacancy.save()
    #
    #     return JsonResponse(vacancy_data.data)
    #     #     "id": vacancy.id,
    #     #     "text": vacancy.text,
    #     #     "slug": vacancy.slug,
    #     #     "status": vacancy.status,
    #     #     "created": vacancy.created,
    #     #     "user": vacancy.user_id
    #     # })


class VacancyUpdateView(UpdateAPIView):
    queryset = Vacancy.objects.all()
    serializer_class = VacancyUpdateSerializer

    # def patch(self, request, *args, **kwargs):
    #     super().post(request, *args, **kwargs)
    #
    #     vacancy_data = json.loads(request.body)
    #     self.object.slug = vacancy_data["slug"]
    #     self.object.text = vacancy_data["text"]
    #     self.object.status = vacancy_data["status"]
    #
    #     for skill in vacancy_data["skills"]:
    #         try:
    #             skill_obj = Skill.objects.get(name=skill)
    #         except Skill.DoesNotExist:
    #             return JsonResponse({"error": "Skill not found"}, status=404)
    #         self.object.skills.add(skill_obj)
    #
    #     self.object.save()
    #
    #     return JsonResponse({
    #         "id": self.object.id,
    #         "text": self.object.text,
    #         "slug": self.object.slug,
    #         "status": self.object.status,
    #         "created": self.object.created,
    #         "user": self.object.user_id,
    #         # "skills": list(self.object.skills.all().values_list("name", flat=True)),
    #     })
    #


class VacancyDeleteView(DestroyAPIView):
    queryset = Vacancy.objects.all()
    serializer_class = VacancyDestroySerializer

    # def delete(self, request, *args, **kwargs):
    #     super().delete(request, *args, **kwargs)
    #
    #     return JsonResponse({"status": "ok"}, status=200)


class UserVacancyDetailView(View):
    def get(self, request):
        user_qs = User.objects.annotate(vacancies=Count('vacancy'))

        paginator = Paginator(user_qs, settings.TOTAL_ON_PAGE)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        users = []
        for user in page_obj:
            users.append({
                "id": user.id,
                "name": user.username,
                "vacancies": user.vacancies
            })

        response ={
            "items": users,
            "total": paginator.count,
            "num_pages": paginator.num_pages,
            "avg": user_qs.aggregate(avg=Avg('vacancies'))["avg"]
        }

        return JsonResponse(response)



