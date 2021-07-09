from django.shortcuts import render, get_object_or_404
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
import requests
import pytz
import json
from django.contrib.sessions.models import Session
from elearn.models import *
from elearn.serializers import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
import uuid
from django.db.models import Q
from operator import itemgetter
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.authtoken.models import Token
from django.core import serializers
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from django.contrib.sessions.backends.db import SessionStore


class ShotsView(APIView):

    def get(self, request, format=None):
        response = {}
        userId = request.GET.get('id')
        sub_id = request.GET.get('sub_id')
        if userId:
            qs = Shots.objects.filter(id=userId)
        elif sub_id:
            subid = get_object_or_404(SubCategory, id=sub_id)
            qs = subid.shots_set.all().order_by('-id')
        else:
            qs = Shots.objects.all().order_by('-id')

        for data in qs:
            response[data.id] = {
                "id": data.id,
                "sub_category": data.sub_category.name,
                "sub_category_id": data.sub_category.id,
                "title": data.title,
                "video": data.video.url if data.video else "no video"
            }
        return Response(response.values(), status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        try:
            serializer = ShotsSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
            return Response({"Status": True,
                             "Message": "Successfully Registered Shots"},
                            status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"Errors": "Some field miss check and enter", "exception": str(e), "status": False},
                            status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        userId = request.GET.get('id')
        data = request.data
        try:
            user = Shots.objects.get(id=userId)
        except Shots.DoesNotExist:
            return Response({"error": "Shots ID not found", "status": False}, status=status.HTTP_400_BAD_REQUEST)
        serializer = ShotsSerializer(user, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data, status=status.HTTP_206_PARTIAL_CONTENT)

    def delete(self, request, format=None):
        if request.GET.get('id'):
            get_object_or_404(Shots, id=request.GET.get('id')).delete()
        else:
            get_object_or_404(Shots, id=request.data.get('id')).delete()
        return Response({"success": "Id related data deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


class CategoryView(APIView):

    def get(self, request, format=None):
        userId = request.GET.get('id')
        if userId:
            return Response(CategorySerializer(get_object_or_404(Category, id=userId), many=False).data,
                            status=status.HTTP_200_OK)

        serializer = CategorySerializer(Category.objects.all(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        try:
            serializer = CategorySerializer(data=data)
            if serializer.is_valid():
                serializer.save()
            return Response({"Status": True,
                             "Message": "Successfully Registered Category"},
                            status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"Errors": "Some field miss check and enter", "exception": str(e), "status": False},
                            status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        userId = request.GET.get('id')
        data = request.data
        try:
            user = Category.objects.get(id=userId)
        except Category.DoesNotExist:
            return Response({"error": "Category ID not found", "status": False}, status=status.HTTP_400_BAD_REQUEST)
        serializer = CategorySerializer(user, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data, status=status.HTTP_206_PARTIAL_CONTENT)

    def delete(self, request, format=None):
        if request.GET.get('id'):
            get_object_or_404(Category, id=request.GET.get('id')).delete()
        else:
            get_object_or_404(Category, id=request.data.get('id')).delete()
        return Response({"success": "Id related data deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


class SubCategoryView(APIView):

    def get(self, request, format=None):
        response = {}
        userId = request.GET.get('id')
        if userId:
            qs = SubCategory.objects.filter(id=userId)
        else:
            qs = SubCategory.objects.all()

        for data in qs:
            print(data)
            response[data.id] = {
                "id": data.id,
                "category": data.category.name,
                "sub_category": data.name,
            }
        return Response(response.values(), status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        try:
            serializer = SubCategorySerializer(data=data)
            if serializer.is_valid():
                serializer.save()
            return Response({"Status": True,
                             "Message": "Successfully Registered SubCategory"},
                            status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"Errors": "Some field miss check and enter", "exception": str(e), "status": False},
                            status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        userId = request.GET.get('id')
        data = request.data
        try:
            user = SubCategory.objects.get(id=userId)
        except SubCategory.DoesNotExist:
            return Response({"error": "Sub Category ID not found", "status": False}, status=status.HTTP_400_BAD_REQUEST)
        serializer = SubCategorySerializer(user, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data, status=status.HTTP_206_PARTIAL_CONTENT)

    def delete(self, request, format=None):
        if request.GET.get('id'):
            get_object_or_404(SubCategory, id=request.GET.get('id')).delete()
        else:
            get_object_or_404(SubCategory, id=request.data.get('id')).delete()
        return Response({"success": "Id related data deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


class Diff_DigView(APIView):

    def get(self, request, format=None):
        response = {}
        userId = request.GET.get('id')
        sub_id = request.GET.get('sub_id')
        if userId:
            qs = Diff_Dig.objects.filter(id=userId)
        elif sub_id:
            subid = get_object_or_404(SubCategory, id=sub_id)
            qs = subid.diff_dig_set.all().order_by('-id')
        else:
            qs = Diff_Dig.objects.all().order_by('-id')

        for data in qs:
            response[data.id] = {
                "id": data.id,
                "sub_category": data.sub_category.name,
                "sub_category_id": data.sub_category.id,
                "title": data.title,
                "video": data.video.url if data.video else "no video"
            }
        return Response(response.values(), status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        try:
            serializer = DiffDigSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
            return Response({"Status": True,
                             "Message": "Successfully Registered Diff Dig"},
                            status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"Errors": "Some field miss check and enter", "exception": str(e), "status": False},
                            status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        userId = request.GET.get('id')
        data = request.data
        try:
            user = Diff_Dig.objects.get(id=userId)
        except Diff_Dig.DoesNotExist:
            return Response({"error": "Diff Dig ID not found", "status": False}, status=status.HTTP_400_BAD_REQUEST)
        serializer = DiffDigSerializer(user, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data, status=status.HTTP_206_PARTIAL_CONTENT)

    def delete(self, request, format=None):
        if request.GET.get('id'):
            get_object_or_404(Diff_Dig, id=request.GET.get('id')).delete()
        else:
            get_object_or_404(Diff_Dig, id=request.data.get('id')).delete()
        return Response({"success": "Id related data deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


class RecentUpdatesView(APIView):

    def get(self, request, format=None):
        response = {}
        userId = request.GET.get('id')
        sub_id = request.GET.get('sub_id')
        if userId:
            qs = recent_updates.objects.filter(id=userId)
        elif sub_id:
            subid = get_object_or_404(SubCategory, id=sub_id)
            qs = subid.recent_updates_set.all().order_by('-id')
        else:
            qs = recent_updates.objects.all().order_by('-id')
        for data in qs:
            response[data.id] = {
                "id": data.id,
                "sub_category": data.sub_category.name,
                "sub_category_id": data.sub_category.id,
                "title": data.title,
                "video": data.video.url if data.video else "no video"
            }
        return Response(response.values(), status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        try:
            serializer = RecentUpdatesSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
            return Response({"Status": True,
                             "Message": "Successfully Registered Recent Updates"},
                            status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"Errors": "Some field miss check and enter", "exception": str(e), "status": False},
                            status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        userId = request.GET.get('id')
        data = request.data
        try:
            user = recent_updates.objects.get(id=userId)
        except recent_updates.DoesNotExist:
            return Response({"error": "Recent Updates ID not found", "status": False},
                            status=status.HTTP_400_BAD_REQUEST)
        serializer = RecentUpdatesSerializer(user, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data, status=status.HTTP_206_PARTIAL_CONTENT)

    def delete(self, request, format=None):
        if request.GET.get('id'):
            get_object_or_404(recent_updates, id=request.GET.get('id')).delete()
        else:
            get_object_or_404(recent_updates, id=request.data.get('id')).delete()
        return Response({"success": "Id related data deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


class ValuesView(APIView):

    def get(self, request, format=None):
        response = {}
        userId = request.GET.get('id')
        sub_id = request.GET.get('sub_id')
        if userId:
            qs = Values.objects.filter(id=userId)
        elif sub_id:
            subid = get_object_or_404(SubCategory, id=sub_id)
            qs = subid.values_set.all().order_by('-id')
        else:
            qs = Values.objects.all().order_by('-id')

        for data in qs:
            response[data.id] = {
                "id": data.id,
                "sub_category": data.sub_category.name,
                "sub_category_id": data.sub_category.id,
                "title": data.title,
                "video": data.video.url if data.video else "no video"
            }
        return Response(response.values(), status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        try:
            serializer = ValuesSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
            return Response({"Status": True,
                             "Message": "Successfully Registered Values"},
                            status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"Errors": "Some field miss check and enter", "exception": str(e), "status": False},
                            status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        userId = request.GET.get('id')
        data = request.data
        try:
            user = Values.objects.get(id=userId)
        except Values.DoesNotExist:
            return Response({"error": "Values ID not found", "status": False}, status=status.HTTP_400_BAD_REQUEST)
        serializer = ValuesSerializer(user, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data, status=status.HTTP_206_PARTIAL_CONTENT)

    def delete(self, request, format=None):
        if request.GET.get('id'):
            get_object_or_404(Values, id=request.GET.get('id')).delete()
        else:
            get_object_or_404(Values, id=request.data.get('id')).delete()
        return Response({"success": "Id related data deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


class ICardsPDFView(APIView):
    def get(self, request, format=None):
        response = {}
        userId = request.GET.get('id')
        sub_id = request.GET.get('sub_id')
        if userId:
            qs = ICardsPDF.objects.filter(id=userId)
        elif sub_id:
            subid = get_object_or_404(SubCategory, id=sub_id)
            qs = subid.icardspdf_set.all().order_by('-id')
        else:
            qs = ICardsPDF.objects.all().order_by('-id')

        for data in qs:
            response[data.id] = {
                "id": data.id,
                "sub_category": data.sub_category.name,
                "sub_category_id": data.sub_category.id,
                "title": data.title,
                "video": data.video.url if data.video else "no video"
            }
        return Response(response.values(), status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        try:
            serializer = ICardsPDFSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
            return Response({"Status": True,
                             "Message": "Successfully Registered ICARDS PDF"},
                            status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"Errors": "Some field miss check and enter", "exception": str(e), "status": False},
                            status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        userId = request.GET.get('id')
        data = request.data
        try:
            user = ICardsPDF.objects.get(id=userId)
        except ICardsPDF.DoesNotExist:
            return Response({"error": "Icards pdf ID not found", "status": False}, status=status.HTTP_400_BAD_REQUEST)
        serializer = ICardsPDFSerializer(user, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data, status=status.HTTP_206_PARTIAL_CONTENT)

    def delete(self, request, format=None):
        if request.GET.get('id'):
            get_object_or_404(ICardsPDF, id=request.GET.get('id')).delete()
        else:
            get_object_or_404(ICardsPDF, id=request.data.get('id')).delete()
        return Response({"success": "Id related data deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


class ICardsVideoView(APIView):

    def get(self, request, format=None):
        response = {}
        userId = request.GET.get('id')
        sub_id = request.GET.get('sub_id')
        if userId:
            qs = ICardsVideo.objects.filter(id=userId)
        elif sub_id:
            subid = get_object_or_404(SubCategory, id=sub_id)
            qs = subid.icardsvideo_set.all().order_by('-id')
        else:
            qs = ICardsVideo.objects.all().order_by('-id')

        for data in qs:
            response[data.id] = {
                "id": data.id,
                "sub_category": data.sub_category.name,
                "sub_category_id": data.sub_category.id,
                "title": data.title,
                "video": data.video.url if data.video else "no video"
            }
        return Response(response.values(), status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        try:
            serializer = ICardsVideoSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
            return Response({"Status": True,
                             "Message": "Successfully Registered ICARDS Video"},
                            status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"Errors": "Some field miss check and enter", "exception": str(e), "status": False},
                            status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        userId = request.GET.get('id')
        data = request.data
        try:
            user = ICardsVideo.objects.get(id=userId)
        except ICardsVideo.DoesNotExist:
            return Response({"error": "Icards video ID not found", "status": False}, status=status.HTTP_400_BAD_REQUEST)
        serializer = ICardsVideoSerializer(user, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data, status=status.HTTP_206_PARTIAL_CONTENT)

    def delete(self, request, format=None):
        if request.GET.get('id'):
            get_object_or_404(ICardsVideo, id=request.GET.get('id')).delete()
        else:
            get_object_or_404(ICardsVideo, id=request.data.get('id')).delete()
        return Response({"success": "Id related data deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

class ICardsAudioView(APIView):

    def get(self, request, format=None):
        response = {}
        userId = request.GET.get('id')
        sub_id = request.GET.get('sub_id')
        if userId:
            qs = ICardsAudio.objects.filter(id=userId)
        elif sub_id:
            subid = get_object_or_404(SubCategory, id=sub_id)
            qs = subid.icardsaudio_set.all().order_by('-id')
        else:
            qs = ICardsAudio.objects.all().order_by('-id')

        for data in qs:
            response[data.id] = {
                "id": data.id,
                "sub_category": data.sub_category.name,
                "sub_category_id": data.sub_category.id,
                "title": data.title,
                "video": data.video.url if data.video else "no video"
            }
        return Response(response.values(), status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        try:
            serializer = ICardsAudioSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
            return Response({"Status": True,
                             "Message": "Successfully Registered ICARDS Audio"},
                            status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"Errors": "Some field miss check and enter", "exception": str(e), "status": False},
                            status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        userId = request.GET.get('id')
        data = request.data
        try:
            user = ICardsAudio.objects.get(id=userId)
        except ICardsAudio.DoesNotExist:
            return Response({"error": "Icards audio ID not found", "status": False}, status=status.HTTP_400_BAD_REQUEST)
        serializer = ICardsAudioSerializer(user, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data, status=status.HTTP_206_PARTIAL_CONTENT)

    def delete(self, request, format=None):
        if request.GET.get('id'):
            get_object_or_404(ICardsAudio, id=request.GET.get('id')).delete()
        else:
            get_object_or_404(ICardsAudio, id=request.data.get('id')).delete()
        return Response({"success": "Id related data deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


class ImageBankView(APIView):

    def get(self, request, format=None):
        response = {}
        userId = request.GET.get('id')
        sub_id = request.GET.get('sub_id')
        if userId:
            qs = ImageBank.objects.filter(id=userId)
        elif sub_id:
            subid = get_object_or_404(SubCategory, id=sub_id)
            qs = subid.imagebank_set.all().order_by('-id')
        else:
            qs = ImageBank.objects.all().order_by('-id')

        for data in qs:
            response[data.id] = {
                "id": data.id,
                "sub_category": data.sub_category.name,
                "sub_category_id": data.sub_category.id,
                "title": data.title,
                "video": data.video.url if data.video else "no video"
            }
        return Response(response.values(), status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        try:
            serializer = ImageBankSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
            return Response({"Status": True,
                             "Message": "Successfully Registered Image Bank"},
                            status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"Errors": "Some field miss check and enter", "exception": str(e), "status": False},
                            status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        userId = request.GET.get('id')
        data = request.data
        try:
            user = ImageBank.objects.get(id=userId)
        except ImageBank.DoesNotExist:
            return Response({"error": "Image Bank ID not found", "status": False}, status=status.HTTP_400_BAD_REQUEST)
        serializer = ImageBankSerializer(user, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data, status=status.HTTP_206_PARTIAL_CONTENT)

    def delete(self, request, format=None):
        if request.GET.get('id'):
            get_object_or_404(ImageBank, id=request.GET.get('id')).delete()
        else:
            get_object_or_404(ImageBank, id=request.data.get('id')).delete()
        return Response({"success": "Id related data deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


class WallPosterView(APIView):
    def get(self, request, format=None):
        response = {}
        userId = request.GET.get('id')
        sub_id = request.GET.get('sub_id')
        if userId:
            qs = WallPosters.objects.filter(id=userId)
        elif sub_id:
            subid = get_object_or_404(SubCategory, id=sub_id)
            qs = subid.wallposters_set.all().order_by('-id')
        else:
            qs = WallPosters.objects.all().order_by('-id')

        for data in qs:
            response[data.id] = {
                "id": data.id,
                "sub_category": data.sub_category.name,
                "sub_category_id": data.sub_category.id,
                "title": data.title,
                "video": data.video.url if data.video else "no video"
            }
        return Response(response.values(), status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        try:
            serializer = WallPosterSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
            return Response({"Status": True,
                             "Message": "Successfully Registered Wall Posters"},
                            status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"Errors": "Some field miss check and enter", "exception": str(e), "status": False},
                            status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        userId = request.GET.get('id')
        data = request.data
        try:
            user = WallPosters.objects.get(id=userId)
        except WallPosters.DoesNotExist:
            return Response({"error": "Wall Posters ID not found", "status": False}, status=status.HTTP_400_BAD_REQUEST)
        serializer = WallPosterSerializer(user, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data, status=status.HTTP_206_PARTIAL_CONTENT)

    def delete(self, request, format=None):
        if request.GET.get('id'):
            get_object_or_404(WallPosters, id=request.GET.get('id')).delete()
        else:
            get_object_or_404(WallPosters, id=request.data.get('id')).delete()
        return Response({"success": "Id related data deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
