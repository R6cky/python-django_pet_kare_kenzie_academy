from django.shortcuts import render
from rest_framework.views import APIView, Request, Response, status
from pets.models import Pet
from pets.serializers import PetSerializer
from groups.models import Group
from traits.models import Trait
from rest_framework.pagination import PageNumberPagination


class PetView(APIView, PageNumberPagination):

    def post(self, req):
            serializer = PetSerializer(data=req.data)
            serializer.is_valid(raise_exception=True)
            group_data = serializer.validated_data.pop('group')
            trait_list = serializer.validated_data.pop('traits')

            try:
                group = Group.objects.get(
                    scientific_name=group_data['scientific_name'])
            except Group.DoesNotExist:
                group = Group.objects.create(**group_data)

            pet = Pet.objects.create(**serializer.validated_data, group=group)

            for trait_data in trait_list:
                try:
                    trait = Trait.objects.get(name__iexact=trait_data['name'])

                except Trait.DoesNotExist:
                    trait = Trait.objects.create(**trait_data)

                pet.traits.add(trait)

            serializer = PetSerializer(pet)

            return Response(serializer.data, status.HTTP_201_CREATED)

    def get(self, req):
            trait_param = req.query_params.get('trait')

            if trait_param:
                pets = Pet.objects.filter(traits__name=trait_param).all()
                result_page = self.paginate_queryset(pets, req)
                serializer = PetSerializer(result_page, many=True)
                return self.get_paginated_response(serializer.data)

            pets = Pet.objects.all()
            result_page = self.paginate_queryset(pets, req)
            serializer = PetSerializer(result_page, many=True)
            return self.get_paginated_response(serializer.data)


class PetViewUnique(APIView):
    def get(self, req, pet_id):

        try:
            pet = Pet.objects.get(pk=pet_id)
        except Pet.DoesNotExist:
            return Response({"detail": "Not found."}, 404)

        serializer = PetSerializer(pet)
        return Response(serializer.data, 200)

    def delete(self, req, pet_id):
        try:
            pet = Pet.objects.get(pk=pet_id)
        except Pet.DoesNotExist:
            return Response({"detail": "Not found."}, 404)
        pet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def patch(self, req, pet_id: int):
        try:
            pet = Pet.objects.get(pk=pet_id)
        except Pet.DoesNotExist:
            return Response({"detail": "Not found."}, 404)

        serializer = PetSerializer(data=req.data, partial=True)
        serializer.is_valid(raise_exception=True)

        trait_data = serializer.validated_data.pop("traits", None)
        group_data = serializer.validated_data.pop("group", None)

        for key, value in serializer.validated_data.items():
            setattr(pet, key, value)

        new_traits_list = []

        if trait_data:
            for trait in trait_data:
                trait_true = Trait.objects.filter(name__icontains=trait["name"])

                trait_obj = (
                    trait_true.first()
                    if trait_true.exists()
                    else Trait.objects.create(name=trait["name"])
                )

                new_traits_list.append(trait_obj)

            pet.traits.set(new_traits_list)

        if group_data:
            group_exist = Group.objects.filter(
                scientific_name__icontains=group_data["scientific_name"]
            )

            group_obj = (
                group_exist.first()
                if group_exist.exists()
                else Group.objects.create(
                    scientific_name=group_data["scientific_name"]
                )
            )
            pet.group = group_obj
        pet.save()

        serializer = PetSerializer(pet)

        return Response(serializer.data, status=status.HTTP_200_OK)
