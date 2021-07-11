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


class Values_CategoryView(APIView):

    def get(self, request, format=None):
        userId = request.GET.get('id')
        if userId:
            return Response(Values_CategorySerializer(get_object_or_404(Values_Category, id=userId), many=False).data,
                            status=status.HTTP_200_OK)

        serializer = Values_CategorySerializer(Values_Category.objects.all(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        try:
            serializer = Values_CategorySerializer(data=data)
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
            user = Values_Category.objects.get(id=userId)
        except Values_Category.DoesNotExist:
            return Response({"error": "Category ID not found", "status": False}, status=status.HTTP_400_BAD_REQUEST)
        serializer = Values_CategorySerializer(user, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data, status=status.HTTP_206_PARTIAL_CONTENT)

    def delete(self, request, format=None):
        if request.GET.get('id'):
            get_object_or_404(Values_Category, id=request.GET.get('id')).delete()
        else:
            get_object_or_404(Values_Category, id=request.data.get('id')).delete()
        return Response({"success": "Id related data deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

class Values_SubCategoryView(APIView):

    def get(self, request, format=None):
        response = {}
        userId = request.GET.get('id')
        if userId:
            qs = Values_SubCategory.objects.filter(id=userId)
        else:
            qs = Values_SubCategory.objects.all()

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
            serializer = Values_SubCategorySerializer(data=data)
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
            user = Values_SubCategory.objects.get(id=userId)
        except Values_SubCategory.SubCategory.DoesNotExist:
            return Response({"error": "Sub Category ID not found", "status": False}, status=status.HTTP_400_BAD_REQUEST)
        serializer = Values_SubCategorySerializer(user, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data, status=status.HTTP_206_PARTIAL_CONTENT)

    def delete(self, request, format=None):
        if request.GET.get('id'):
            get_object_or_404(Values_SubCategory, id=request.GET.get('id')).delete()
        else:
            get_object_or_404(Values_SubCategory, id=request.data.get('id')).delete()
        return Response({"success": "Id related data deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


class ICardsPDF_CategoryView(APIView):

    def get(self, request, format=None):
        userId = request.GET.get('id')
        if userId:
            return Response(ICardsPDF_CategorySerializer(get_object_or_404(ICardsPDF_Category, id=userId), many=False).data,
                            status=status.HTTP_200_OK)

        serializer = ICardsPDF_CategorySerializer(ICardsPDF_Category.objects.all(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        try:
            serializer = ICardsPDF_CategorySerializer(data=data)
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
            user = ICardsPDF_Category.objects.get(id=userId)
        except ICardsPDF_Category.DoesNotExist:
            return Response({"error": "Category ID not found", "status": False}, status=status.HTTP_400_BAD_REQUEST)
        serializer = ICardsPDF_CategorySerializer(user, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data, status=status.HTTP_206_PARTIAL_CONTENT)

    def delete(self, request, format=None):
        if request.GET.get('id'):
            get_object_or_404(ICardsPDF_Category, id=request.GET.get('id')).delete()
        else:
            get_object_or_404(ICardsPDF_Category, id=request.data.get('id')).delete()
        return Response({"success": "Id related data deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

class ICardsPDF_SubCategoryView(APIView):

    def get(self, request, format=None):
        response = {}
        userId = request.GET.get('id')
        if userId:
            qs = ICardsPDF_SubCategory.objects.filter(id=userId)
        else:
            qs = ICardsPDF_SubCategory.objects.all()

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
            serializer = ICardsPDF_SubCategorySerializer(data=data)
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
            user = ICardsPDF_SubCategory.objects.get(id=userId)
        except ICardsPDF_SubCategory.SubCategory.DoesNotExist:
            return Response({"error": "Sub Category ID not found", "status": False}, status=status.HTTP_400_BAD_REQUEST)
        serializer = ICardsPDF_SubCategorySerializer(user, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data, status=status.HTTP_206_PARTIAL_CONTENT)

    def delete(self, request, format=None):
        if request.GET.get('id'):
            get_object_or_404(ICardsPDF_SubCategory, id=request.GET.get('id')).delete()
        else:
            get_object_or_404(ICardsPDF_SubCategory, id=request.data.get('id')).delete()
        return Response({"success": "Id related data deleted successfully"}, status=status.HTTP_204_NO_CONTENT)   


class  ICardsAudio_CategoryView(APIView):

    def get(self, request, format=None):
        userId = request.GET.get('id')
        if userId:
            return Response(ICardsAudio_CategorySerializer(get_object_or_404(ICardsAudio_Category, id=userId), many=False).data,
                            status=status.HTTP_200_OK)

        serializer = ICardsAudio_CategorySerializer(Diff_Dig_Category.objects.all(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        try:
            serializer = ICardsAudio_CategorySerializer(data=data)
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
            user = ICardsAudio_Category.objects.get(id=userId)
        except ICardsAudio_Category.DoesNotExist:
            return Response({"error": "Category ID not found", "status": False}, status=status.HTTP_400_BAD_REQUEST)
        serializer = ICardsAudio_CategorySerializer(user, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data, status=status.HTTP_206_PARTIAL_CONTENT)

    def delete(self, request, format=None):
        if request.GET.get('id'):
            get_object_or_404(ICardsAudio_Category, id=request.GET.get('id')).delete()
        else:
            get_object_or_404(ICardsAudio_Category, id=request.data.get('id')).delete()
        return Response({"success": "Id related data deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

class ICardsAudio_SubCategoryView(APIView):

    def get(self, request, format=None):
        response = {}
        userId = request.GET.get('id')
        if userId:
            qs = ICardsAudio_SubCategory.objects.filter(id=userId)
        else:
            qs = ICardsAudio_SubCategory.objects.all()

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
            serializer = ICardsAudio_SubCategorySerializer(data=data)
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
            user = ICardsAudio_SubCategory.objects.get(id=userId)
        except ICardsAudio_SubCategory.SubCategory.DoesNotExist:
            return Response({"error": "Sub Category ID not found", "status": False}, status=status.HTTP_400_BAD_REQUEST)
        serializer = ICardsAudio_SubCategorySerializer(user, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data, status=status.HTTP_206_PARTIAL_CONTENT)

    def delete(self, request, format=None):
        if request.GET.get('id'):
            get_object_or_404(ICardsAudio_SubCategory, id=request.GET.get('id')).delete()
        else:
            get_object_or_404(ICardsAudio_SubCategory, id=request.data.get('id')).delete()
        return Response({"success": "Id related data deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


class ICardsVideo_CategoryView(APIView):

    def get(self, request, format=None):
        userId = request.GET.get('id')
        if userId:
            return Response(ICardsVideo_CategorySerializer(get_object_or_404(ICardsVideo_Category, id=userId), many=False).data,
                            status=status.HTTP_200_OK)

        serializer = ICardsVideo_CategorySerializer(ICardsVideo_Category.objects.all(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        try:
            serializer = ICardsVideo_CategorySerializer(data=data)
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
            user = ICardsVideo_Category.objects.get(id=userId)
        except ICardsVideo_Category.DoesNotExist:
            return Response({"error": "Category ID not found", "status": False}, status=status.HTTP_400_BAD_REQUEST)
        serializer = ICardsVideo_CategorySerializer(user, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data, status=status.HTTP_206_PARTIAL_CONTENT)

    def delete(self, request, format=None):
        if request.GET.get('id'):
            get_object_or_404(ICardsVideo_Category, id=request.GET.get('id')).delete()
        else:
            get_object_or_404(ICardsVideo_Category, id=request.data.get('id')).delete()
        return Response({"success": "Id related data deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

class ICardsVideo_SubCategoryView(APIView):

    def get(self, request, format=None):
        response = {}
        userId = request.GET.get('id')
        if userId:
            qs = ICardsVideo_SubCategory.objects.filter(id=userId)
        else:
            qs = ICardsVideo_SubCategory.objects.all()

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
            serializer = ICardsVideo_SubCategorySerializer(data=data)
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
            user = ICardsVideo_SubCategory.objects.get(id=userId)
        except ICardsVideo_SubCategory.SubCategory.DoesNotExist:
            return Response({"error": "Sub Category ID not found", "status": False}, status=status.HTTP_400_BAD_REQUEST)
        serializer = ICardsVideo_SubCategorySerializer(user, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data, status=status.HTTP_206_PARTIAL_CONTENT)

    def delete(self, request, format=None):
        if request.GET.get('id'):
            get_object_or_404(ICardsVideo_SubCategory, id=request.GET.get('id')).delete()
        else:
            get_object_or_404(ICardsVideo_SubCategory, id=request.data.get('id')).delete()
        return Response({"success": "Id related data deleted successfully"}, status=status.HTTP_204_NO_CONTENT)




class ImageBank_CategoryView(APIView):

    def get(self, request, format=None):
        userId = request.GET.get('id')
        if userId:
            return Response(ImageBank_CategorySerializer(get_object_or_404(ImageBank_Category, id=userId), many=False).data,
                            status=status.HTTP_200_OK)

        serializer = ImageBank_CategorySerializer(ImageBank_Category.objects.all(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        try:
            serializer = ImageBank_CategorySerializer(data=data)
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
            user = ImageBank_Category.objects.get(id=userId)
        except ImageBank_Category.DoesNotExist:
            return Response({"error": "Category ID not found", "status": False}, status=status.HTTP_400_BAD_REQUEST)
        serializer = ImageBank_CategorySerializer(user, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data, status=status.HTTP_206_PARTIAL_CONTENT)

    def delete(self, request, format=None):
        if request.GET.get('id'):
            get_object_or_404(ImageBank_Category, id=request.GET.get('id')).delete()
        else:
            get_object_or_404(ImageBank_Category, id=request.data.get('id')).delete()
        return Response({"success": "Id related data deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

class ImageBank_SubCategoryView(APIView):

    def get(self, request, format=None):
        response = {}
        userId = request.GET.get('id')
        if userId:
            qs =  ImageBank_SubCategory.objects.filter(id=userId)
        else:
            qs =  ImageBank_SubCategory.objects.all()

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
            serializer =  ImageBank_SubCategorySerializer(data=data)
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
            user =  ImageBank_SubCategory.objects.get(id=userId)
        except  ImageBank_SubCategory.SubCategory.DoesNotExist:
            return Response({"error": "Sub Category ID not found", "status": False}, status=status.HTTP_400_BAD_REQUEST)
        serializer =  ImageBank_SubCategorySerializer(user, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data, status=status.HTTP_206_PARTIAL_CONTENT)

    def delete(self, request, format=None):
        if request.GET.get('id'):
            get_object_or_404( ImageBank_SubCategory, id=request.GET.get('id')).delete()
        else:
            get_object_or_404(ImageBank_SubCategory, id=request.data.get('id')).delete()
        return Response({"success": "Id related data deleted successfully"}, status=status.HTTP_204_NO_CONTENT)




class WallPoster_CategoryView(APIView):

    def get(self, request, format=None):
        userId = request.GET.get('id')
        if userId:
            return Response(WallPoster_CategorySerializer(get_object_or_404(WallPoster_Category, id=userId), many=False).data,
                            status=status.HTTP_200_OK)

        serializer = WallPoster_CategorySerializer(WallPoster_Category.objects.all(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        try:
            serializer = WallPoster_CategorySerializer(data=data)
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
            user =WallPoster_Category.objects.get(id=userId)
        except WallPoster_Category.DoesNotExist:
            return Response({"error": "Category ID not found", "status": False}, status=status.HTTP_400_BAD_REQUEST)
        serializer = WallPoster_CategorySerializer(user, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data, status=status.HTTP_206_PARTIAL_CONTENT)

    def delete(self, request, format=None):
        if request.GET.get('id'):
            get_object_or_404WallPoster_Category, id=request.GET.get('id')).delete()
        else:
            get_object_or_404(WallPoster_Category, id=request.data.get('id')).delete()
        return Response({"success": "Id related data deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


class WallPoster_SubCategoryView(APIView):

    def get(self, request, format=None):
        userId = request.GET.get('id')
        if userId:
            return Response(WallPoster_SubCategorySerializer(get_object_or_404(WallPoster_SubCategory, id=userId), many=False).data,
                            status=status.HTTP_200_OK)

        serializer = WallPoster_SubCategorySerializer(WallPoster_Category.objects.all(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        try:
            serializer = WallPoster_SubCategorySerializer(data=data)
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
            user = WallPoster_SubCategory.objects.get(id=userId)
        except WallPoster_SubCategory.SubCategory.DoesNotExist:
            return Response({"error": "Sub Category ID not found", "status": False}, status=status.HTTP_400_BAD_REQUEST)
        serializer = WallPoster_SubCategorySerializer(user, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data, status=status.HTTP_206_PARTIAL_CONTENT)

    def delete(self, request, format=None):
        if request.GET.get('id'):
            get_object_or_404(WallPoster_SubCategory, id=request.GET.get('id')).delete()
        else:
            get_object_or_404(WallPoster_SubCategory, id=request.data.get('id')).delete()
        return Response({"success": "Id related data deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


# --------------------------------------------------- new changes shubham -------------------

class DailyBoostBannerView(APIView):

    def get(self, request, format=None):
        response = {}
        userId = request.GET.get('id')
        sub_id = request.GET.get('sub_id')
        if userId:
            qs = DailyBoostBanner.objects.filter(id=userId)
        elif sub_id:
            subid = get_object_or_404(SubCategory, id=sub_id)
            qs = subid.DailyBoostBanner_set.all().order_by('-id')
        else:
            qs = DailyBoostBanner.objects.all().order_by('-id')

        for data in qs:
            response[data.id] = {
                "id": data.id,
                "sub_category": data.sub_category.name,
                "sub_category_id": data.sub_category.id,
                "title": data.title,
                "banner": data.banner.url if data.banner else "no banner"
            }
        return Response(response.values(), status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        try:
            serializer = DailyBoostBannerSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
            return Response({"Status": True,
                             "Message": "Successfully Registered DailyBoostBanner"},
                            status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"Errors": "Some field miss check and enter", "exception": str(e), "status": False},
                            status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        userId = request.GET.get('id')
        data = request.data
        try:
            user = DailyBoostBanner.objects.get(id=userId)
        except Shots.DoesNotExist:
            return Response({"error": "DailyBoostBanner ID not found", "status": False}, status=status.HTTP_400_BAD_REQUEST)
        serializer = DailyBoostBannerSerializer(user, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data, status=status.HTTP_206_PARTIAL_CONTENT)

    def delete(self, request, format=None):
        if request.GET.get('id'):
            get_object_or_404(DailyBoostBanner, id=request.GET.get('id')).delete()
        else:
            get_object_or_404(DailyBoostBanner, id=request.data.get('id')).delete()
        return Response({"success": "Id related data deleted successfully"}, status=status.HTTP_204_NO_CONTENT)



class QuestionOfTheDayView(APIView):

    def get(self, request, format=None):
        response = {}
        userId = request.GET.get('id')
        sub_id = request.GET.get('sub_id')
        if userId:
            qs = QuestionOfTheDay.objects.filter(id=userId)
        elif sub_id:
            subid = get_object_or_404(SubCategory, id=sub_id)
            qs = subid.QuestionOfTheDay_set.all().order_by('-id')
        else:
            qs = QuestionOfTheDay.objects.all().order_by('-id')

        for data in qs:
            response[data.id] = {
                "id": data.id,
                "sub_category": data.sub_category.name,               
                "title": data.title,
                "banner": data.banner.url if data.banner else "no banner",
                "Question":data.Question,
                "Answer1":data.Answer1,
                "Answer2":data.Answer2,
                "Answer3":data.Answer3,
                "Answer4":data.Answer4,
                "CorrectAnswer":data.CorrectAnswer,
                "Explanation":data.Explanation,
                "image": data.image.url if data.image else "no image"               
            }
        return Response(response.values(), status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        try:
            serializer = QuestionOfTheDaySerializer(data=data)
            if serializer.is_valid():
                serializer.save()
            return Response({"Status": True,
                             "Message": "Successfully Registered QuestionOfTheDay"},
                            status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"Errors": "Some field miss check and enter", "exception": str(e), "status": False},
                            status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        userId = request.GET.get('id')
        data = request.data
        try:
            user = QuestionOfTheDay.objects.get(id=userId)
        except Shots.DoesNotExist:
            return Response({"error": "QuestionOfTheDay ID not found", "status": False}, status=status.HTTP_400_BAD_REQUEST)
        serializer = QuestionOfTheDaySerializer(user, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data, status=status.HTTP_206_PARTIAL_CONTENT)

    def delete(self, request, format=None):
        if request.GET.get('id'):
            get_object_or_404(QuestionOfTheDay, id=request.GET.get('id')).delete()
        else:
            get_object_or_404(QuestionOfTheDay, id=request.data.get('id')).delete()
        return Response({"success": "Id related data deleted successfully"}, status=status.HTTP_204_NO_CONTENT)