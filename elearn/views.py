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
            subid = get_object_or_404(ShotsSubCategory, id=sub_id)
            qs = subid.shots_set.all().order_by('id')
        else:
            qs = Shots.objects.all().order_by('id')

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


class ShotsCategoryView(APIView):

    def get(self, request, format=None):
        userId = request.GET.get('id')
        if userId:
            return Response(ShotsCategorySerializer(get_object_or_404(ShotsCategory, id=userId), many=False).data,
                            status=status.HTTP_200_OK)

        serializer = ShotsCategorySerializer(ShotsCategory.objects.all(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        try:
            serializer = ShotsCategorySerializer(data=data)
            if serializer.is_valid():
                serializer.save()
            return Response({"Status": True,
                             "Message": "Successfully Registered Shots Category"},
                            status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"Errors": "Some field miss check and enter", "exception": str(e), "status": False},
                            status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        userId = request.GET.get('id')
        data = request.data
        try:
            user = ShotsCategory.objects.get(id=userId)
        except ShotsCategory.DoesNotExist:
            return Response({"error": "Shots Category ID not found", "status": False},
                            status=status.HTTP_400_BAD_REQUEST)
        serializer = ShotsCategorySerializer(user, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data, status=status.HTTP_206_PARTIAL_CONTENT)

    def delete(self, request, format=None):
        if request.GET.get('id'):
            get_object_or_404(ShotsCategory, id=request.GET.get('id')).delete()
        else:
            get_object_or_404(ShotsCategory, id=request.data.get('id')).delete()
        return Response({"success": "Id related data deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


class ShotsSubCategoryView(APIView):

    def get(self, request, format=None):
        response = {}
        userId = request.GET.get('id')
        if userId:
            qs = ShotsSubCategory.objects.filter(id=userId)
        else:
            qs = ShotsSubCategory.objects.all()

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
            serializer = ShotsSubCategorySerializer(data=data)
            if serializer.is_valid():
                serializer.save()
            return Response({"Status": True,
                             "Message": "Successfully Registered Shots SubCategory"},
                            status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"Errors": "Some field miss check and enter", "exception": str(e), "status": False},
                            status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        userId = request.GET.get('id')
        data = request.data
        try:
            user = ShotsSubCategory.objects.get(id=userId)
        except ShotsSubCategory.DoesNotExist:
            return Response({"error": "Shots Sub Category ID not found", "status": False},
                            status=status.HTTP_400_BAD_REQUEST)
        serializer = ShotsSubCategorySerializer(user, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data, status=status.HTTP_206_PARTIAL_CONTENT)

    def delete(self, request, format=None):
        if request.GET.get('id'):
            get_object_or_404(ShotsSubCategory, id=request.GET.get('id')).delete()
        else:
            get_object_or_404(ShotsSubCategory, id=request.data.get('id')).delete()
        return Response({"success": "Id related data deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


class Diff_Dig_CategoryView(APIView):

    def get(self, request, format=None):
        userId = request.GET.get('id')
        if userId:
            return Response(
                Diff_Dig_CategorySerializer(get_object_or_404(Diff_Dig_Category, id=userId), many=False).data,
                status=status.HTTP_200_OK)

        serializer = Diff_Dig_CategorySerializer(Diff_Dig_Category.objects.all(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        try:
            serializer = Diff_Dig_CategorySerializer(data=data)
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
            user = Diff_Dig_Category.objects.get(id=userId)
        except Diff_Dig_Category.DoesNotExist:
            return Response({"error": "Category ID not found", "status": False}, status=status.HTTP_400_BAD_REQUEST)
        serializer = Diff_Dig_CategorySerializer(user, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data, status=status.HTTP_206_PARTIAL_CONTENT)

    def delete(self, request, format=None):
        if request.GET.get('id'):
            get_object_or_404(Diff_Dig_Category, id=request.GET.get('id')).delete()
        else:
            get_object_or_404(Diff_Dig_Category, id=request.data.get('id')).delete()
        return Response({"success": "Id related data deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


class Diff_Dig_SubCategoryView(APIView):

    def get(self, request, format=None):
        response = {}
        userId = request.GET.get('id')
        if userId:
            qs = Diff_Dig_SubCategory.objects.filter(id=userId)
        else:
            qs = Diff_Dig_SubCategory.objects.all()

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
            serializer = Diff_Dig_SubCategorySerializer(data=data)
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
            user = Diff_Dig_SubCategory.objects.get(id=userId)
        except Diff_Dig_SubCategory.DoesNotExist:
            return Response({"error": "Sub Category ID not found", "status": False}, status=status.HTTP_400_BAD_REQUEST)
        serializer = Diff_Dig_SubCategorySerializer(user, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data, status=status.HTTP_206_PARTIAL_CONTENT)

    def delete(self, request, format=None):
        if request.GET.get('id'):
            get_object_or_404(Diff_Dig_SubCategory, id=request.GET.get('id')).delete()
        else:
            get_object_or_404(Diff_Dig_SubCategory, id=request.data.get('id')).delete()
        return Response({"success": "Id related data deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


class Diff_DigView(APIView):

    def get(self, request, format=None):
        response = {}
        userId = request.GET.get('id')
        sub_id = request.GET.get('sub_id')
        if userId:
            qs = Diff_Dig.objects.filter(id=userId)
        elif sub_id:
            subid = get_object_or_404(Diff_Dig_SubCategory, id=sub_id)
            qs = subid.diff_dig_set.all().order_by('id')
        else:
            qs = Diff_Dig.objects.all().order_by('id')

        for data in qs:
            response[data.id] = {
                "id": data.id,
                "sub_category": data.sub_category.name,
                "sub_category_id": data.sub_category.id,
                "title": data.title,
                "pdf": data.pdf.url if data.pdf else "no pdf"
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


class RecentUpdatesCategoryView(APIView):

    def get(self, request, format=None):
        userId = request.GET.get('id')
        if userId:
            return Response(Recent_Updates_CategorySerializer(get_object_or_404(Recent_Updates_Category, id=userId),
                                                              many=False).data,
                            status=status.HTTP_200_OK)

        serializer = Recent_Updates_CategorySerializer(Recent_Updates_Category.objects.all(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        try:
            serializer = Recent_Updates_CategorySerializer(data=data)
            if serializer.is_valid():
                serializer.save()
            return Response({"Status": True,
                             "Message": "Successfully Registered Shots Category"},
                            status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"Errors": "Some field miss check and enter", "exception": str(e), "status": False},
                            status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        userId = request.GET.get('id')
        data = request.data
        try:
            user = Recent_Updates_Category.objects.get(id=userId)
        except Recent_Updates_Category.DoesNotExist:
            return Response({"error": "Shots Category ID not found", "status": False},
                            status=status.HTTP_400_BAD_REQUEST)
        serializer = Recent_Updates_CategorySerializer(user, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data, status=status.HTTP_206_PARTIAL_CONTENT)

    def delete(self, request, format=None):
        if request.GET.get('id'):
            get_object_or_404(Recent_Updates_Category, id=request.GET.get('id')).delete()
        else:
            get_object_or_404(Recent_Updates_Category, id=request.data.get('id')).delete()
        return Response({"success": "Id related data deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


class RecentUpdatesSubCategoryView(APIView):

    def get(self, request, format=None):
        response = {}
        userId = request.GET.get('id')
        if userId:
            qs = Recent_Updates_SubCategory.objects.filter(id=userId)
        else:
            qs = Recent_Updates_SubCategory.objects.all()

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
            serializer = Recent_Updates_SubCategorySerializer(data=data)
            if serializer.is_valid():
                serializer.save()
            return Response({"Status": True,
                             "Message": "Successfully Registered Shots SubCategory"},
                            status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"Errors": "Some field miss check and enter", "exception": str(e), "status": False},
                            status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        userId = request.GET.get('id')
        data = request.data
        try:
            user = Recent_Updates_SubCategory.objects.get(id=userId)
        except Recent_Updates_SubCategory.DoesNotExist:
            return Response({"error": "Shots Sub Category ID not found", "status": False},
                            status=status.HTTP_400_BAD_REQUEST)
        serializer = Recent_Updates_SubCategorySerializer(user, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data, status=status.HTTP_206_PARTIAL_CONTENT)

    def delete(self, request, format=None):
        if request.GET.get('id'):
            get_object_or_404(Recent_Updates_SubCategory, id=request.GET.get('id')).delete()
        else:
            get_object_or_404(Recent_Updates_SubCategory, id=request.data.get('id')).delete()
        return Response({"success": "Id related data deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


class RecentUpdatesView(APIView):

    def get(self, request, format=None):
        response = {}
        userId = request.GET.get('id')
        sub_id = request.GET.get('sub_id')
        if userId:
            qs = recent_updates.objects.filter(id=userId)
        elif sub_id:
            subid = get_object_or_404(Recent_Updates_SubCategory, id=sub_id)
            qs = subid.recent_updates_set.all().order_by('id')
        else:
            qs = recent_updates.objects.all().order_by('id')
        for data in qs:
            response[data.id] = {
                "id": data.id,
                "sub_category": data.sub_category.name,
                "sub_category_id": data.sub_category.id,
                "title": data.title,
                "pdf": data.pdf.url if data.pdf else "no pdf"
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
                             "Message": "Successfully Registered Values Category"},
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
            return Response({"error": "Values Category ID not found", "status": False},
                            status=status.HTTP_400_BAD_REQUEST)
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
        except Values_SubCategory.DoesNotExist:
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


class ValuesView(APIView):

    def get(self, request, format=None):
        response = {}
        userId = request.GET.get('id')
        sub_id = request.GET.get('sub_id')
        if userId:
            qs = Values.objects.filter(id=userId)
        elif sub_id:
            subid = get_object_or_404(Values_SubCategory, id=sub_id)
            qs = subid.values_set.all().order_by('id')
        else:
            qs = Values.objects.all().order_by('id')

        for data in qs:
            response[data.id] = {
                "id": data.id,
                "sub_category": data.sub_category.name,
                "sub_category_id": data.sub_category.id,
                "title": data.title,
                "pdf": data.pdf.url if data.pdf else "no pdf"
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


class ICardsPDF_CategoryView(APIView):

    def get(self, request, format=None):
        userId = request.GET.get('id')
        if userId:
            return Response(
                ICardsPDF_CategorySerializer(get_object_or_404(ICardsPDF_Category, id=userId), many=False).data,
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
        except ICardsPDF_SubCategory.DoesNotExist:
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


class ICardsPDFView(APIView):
    def get(self, request, format=None):
        response = {}
        userId = request.GET.get('id')
        sub_id = request.GET.get('sub_id')
        if userId:
            qs = ICardsPDF.objects.filter(id=userId)
        elif sub_id:
            subid = get_object_or_404(ICardsPDF_SubCategory, id=sub_id)
            qs = subid.icardspdf_set.all().order_by('id')
        else:
            qs = ICardsPDF.objects.all().order_by('id')

        for data in qs:
            response[data.id] = {
                "id": data.id,
                "sub_category": data.sub_category.name,
                "sub_category_id": data.sub_category.id,
                "title": data.title,
                "pdf": data.pdf.url if data.pdf else "no pdf"
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


class ICardsVideo_CategoryView(APIView):

    def get(self, request, format=None):
        userId = request.GET.get('id')
        if userId:
            return Response(
                ICardsVideo_CategorySerializer(get_object_or_404(ICardsVideo_Category, id=userId), many=False).data,
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
        except ICardsVideo_SubCategory.DoesNotExist:
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


class ICardsVideoView(APIView):

    def get(self, request, format=None):
        response = {}
        userId = request.GET.get('id')
        sub_id = request.GET.get('sub_id')
        if userId:
            qs = ICardsVideo.objects.filter(id=userId)
        elif sub_id:
            subid = get_object_or_404(ICardsVideo_SubCategory, id=sub_id)
            qs = subid.icardsvideo_set.all().order_by('id')
        else:
            qs = ICardsVideo.objects.all().order_by('id')

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


class ICardsAudio_CategoryView(APIView):

    def get(self, request, format=None):
        userId = request.GET.get('id')
        if userId:
            return Response(
                ICardsAudio_CategorySerializer(get_object_or_404(ICardsAudio_Category, id=userId), many=False).data,
                status=status.HTTP_200_OK)

        serializer = ICardsAudio_CategorySerializer(ICardsAudio_Category.objects.all(), many=True)
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
        except ICardsAudio_SubCategory.DoesNotExist:
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


class ICardsAudioView(APIView):

    def get(self, request, format=None):
        response = {}
        userId = request.GET.get('id')
        sub_id = request.GET.get('sub_id')
        if userId:
            qs = ICardsAudio.objects.filter(id=userId)
        elif sub_id:
            subid = get_object_or_404(ICardsAudio_SubCategory, id=sub_id)
            qs = subid.icardsaudio_set.all().order_by('id')
        else:
            qs = ICardsAudio.objects.all().order_by('id')

        for data in qs:
            response[data.id] = {
                "id": data.id,
                "sub_category": data.sub_category.name,
                "sub_category_id": data.sub_category.id,
                "title": data.title,
                "audio": data.audio.url if data.audio else "no audio"
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


class ImageBank_CategoryView(APIView):

    def get(self, request, format=None):
        userId = request.GET.get('id')
        if userId:
            return Response(
                ImageBank_CategorySerializerr(get_object_or_404(ImageBank_Category, id=userId), many=False).data,
                status=status.HTTP_200_OK)

        serializer = ImageBank_CategorySerializerr(ImageBank_Category.objects.all(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        try:
            serializer = ImageBank_CategorySerializerr(data=data)
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
        serializer = ImageBank_CategorySerializerr(user, data=data, partial=True)
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
            qs = ImageBank_SubCategory.objects.filter(id=userId)
        else:
            qs = ImageBank_SubCategory.objects.all()

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
            serializer = ImageBank_SubCategorySerializer(data=data)
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
            user = ImageBank_SubCategory.objects.get(id=userId)
        except  ImageBank_SubCategory.DoesNotExist:
            return Response({"error": "Sub Category ID not found", "status": False}, status=status.HTTP_400_BAD_REQUEST)
        serializer = ImageBank_SubCategorySerializer(user, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data, status=status.HTTP_206_PARTIAL_CONTENT)

    def delete(self, request, format=None):
        if request.GET.get('id'):
            get_object_or_404(ImageBank_SubCategory, id=request.GET.get('id')).delete()
        else:
            get_object_or_404(ImageBank_SubCategory, id=request.data.get('id')).delete()
        return Response({"success": "Id related data deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


class ImageBankView(APIView):

    def get(self, request, format=None):
        response = {}
        userId = request.GET.get('id')
        sub_id = request.GET.get('sub_id')
        if userId:
            qs = ImageBank.objects.filter(id=userId)
        elif sub_id:
            subid = get_object_or_404(ImageBank_SubCategory, id=sub_id)
            qs = subid.imagebank_set.all().order_by('id')
        else:
            qs = ImageBank.objects.all().order_by('id')

        for data in qs:
            response[data.id] = {
                "id": data.id,
                "sub_category": data.sub_category.name,
                "sub_category_id": data.sub_category.id,
                "title": data.title,
                "pdf": data.pdf.url if data.pdf else "no pdf"
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


class WallPoster_CategoryView(APIView):

    def get(self, request, format=None):
        userId = request.GET.get('id')
        if userId:
            return Response(
                WallPoster_CategorySerializer(get_object_or_404(WallPoster_Category, id=userId), many=False).data,
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
            user = WallPoster_Category.objects.get(id=userId)
        except WallPoster_Category.DoesNotExist:
            return Response({"error": "Category ID not found", "status": False}, status=status.HTTP_400_BAD_REQUEST)
        serializer = WallPoster_CategorySerializer(user, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data, status=status.HTTP_206_PARTIAL_CONTENT)

    def delete(self, request, format=None):
        if request.GET.get('id'):
            get_object_or_404(WallPoster_Category, id=request.GET.get('id')).delete()
        else:
            get_object_or_404(WallPoster_Category, id=request.data.get('id')).delete()
        return Response({"success": "Id related data deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


class WallPoster_SubCategoryView(APIView):

    def get(self, request, format=None):
        response = {}
        userId = request.GET.get('id')
        if userId:
            qs = WallPoster_SubCategory.objects.filter(id=userId)
        else:
            qs = WallPoster_SubCategory.objects.all()

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
        except WallPoster_SubCategory.DoesNotExist:
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


class WallPosterView(APIView):
    def get(self, request, format=None):
        response = {}
        userId = request.GET.get('id')
        sub_id = request.GET.get('sub_id')
        if userId:
            qs = WallPosters.objects.filter(id=userId)
        elif sub_id:
            subid = get_object_or_404(WallPoster_SubCategory, id=sub_id)
            qs = subid.wallposters_set.all().order_by('id')
        else:
            qs = WallPosters.objects.all().order_by('id')

        for data in qs:
            response[data.id] = {
                "id": data.id,
                "sub_category": data.sub_category.name,
                "sub_category_id": data.sub_category.id,
                "title": data.title,
                "pdf": data.pdf.url if data.pdf else "no pdf"
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


class DailyBoostBannerView(APIView):

    def get(self, request, format=None):
        response = {}
        userId = request.GET.get('id')
        if userId:
            qs = DailyBoostBanner.objects.filter(id=userId)
        else:
            qs = DailyBoostBanner.objects.all().order_by('id')

        for data in qs:
            response[data.id] = {
                "id": data.id,
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
        except DailyBoostBanner.DoesNotExist:
            return Response({"error": "DailyBoostBanner ID not found", "status": False},
                            status=status.HTTP_400_BAD_REQUEST)
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
        if userId:
            qs = QuestionOfTheDay.objects.filter(id=userId)
        else:
            qs = QuestionOfTheDay.objects.all().order_by('id')
        for data in qs:
            response[data.id] = {
                "id": data.id,
                "Question": data.Question,
                "Answer1": data.Answer1,
                "Answer2": data.Answer2,
                "Answer3": data.Answer3,
                "Answer4": data.Answer4,
                "CorrectAnswer": data.CorrectAnswer,
                "Explanation": data.Explanation,
                "image": data.Image.url if data.Image else "no image"

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
        except QuestionOfTheDay.DoesNotExist:
            return Response({"error": "QuestionOfTheDay ID not found", "status": False},
                            status=status.HTTP_400_BAD_REQUEST)
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


class DailyBoosterQuizView(APIView):

    def get(self, request, format=None):
        response = {}
        userId = request.GET.get('id')
        if userId:
            qs = DailyBoosterQuiz.objects.filter(id=userId)
        else:
            qs = DailyBoosterQuiz.objects.all().order_by('id')
        for data in qs:
            response[data.id] = {
                "id": data.id,
                "banner_id": data.banner.id,
                "bannerImage": data.banner.banner,
                "bannerTitle":data.banner.title,
                "question": data.question,
                "answer1": data.answer1,
                "answer2": data.answer2,
                "answer3": data.answer3,
                "answer4": data.answer4,
                "correctanswer": data.correctanswer,
                "explanation": data.explanation,
                "timer": data.timer,
                "image": data.image.url if data.image else "no image"
            }
        return Response(response.values(), status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        try:
            serializer = DailyBoosterQuizSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
            return Response({"Status": True,
                             "Message": "Successfully Registered DailyBoosterQuiz"},
                            status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"Errors": "Some field miss check and enter", "exception": str(e), "status": False},
                            status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        userId = request.GET.get('id')
        data = request.data
        try:
            user = DailyBoosterQuiz.objects.get(id=userId)
        except DailyBoosterQuiz.DoesNotExist:
            return Response({"error": "DailyBoosterQuiz ID not found", "status": False},
                            status=status.HTTP_400_BAD_REQUEST)
        serializer = DailyBoosterQuizSerializer(user, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data, status=status.HTTP_206_PARTIAL_CONTENT)

    def delete(self, request, format=None):
        if request.GET.get('id'):
            get_object_or_404(DailyBoosterQuiz, id=request.GET.get('id')).delete()
        else:
            get_object_or_404(DailyBoosterQuiz, id=request.data.get('id')).delete()
        return Response({"success": "Id related data deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


class QuestionBank_CategoryView(APIView):

    def get(self, request, format=None):
        userId = request.GET.get('id')
        if userId:
            return Response(QuestionBank_CategorySerializer(get_object_or_404(QuestionBank_Category, id=userId), many=False).data,
                            status=status.HTTP_200_OK)

        serializer = QuestionBank_CategorySerializer(QuestionBank_Category.objects.all(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        try:
            serializer = QuestionBank_CategorySerializer(data=data)
            if serializer.is_valid():
                serializer.save()
            return Response({"Status": True,
                             "Message": "Successfully Registered QuestionBank_Category"},
                            status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"Errors": "Some field miss check and enter", "exception": str(e), "status": False},
                            status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        userId = request.GET.get('id')
        data = request.data
        try:
            user = QuestionBank_Category.objects.get(id=userId)
        except QuestionBank_Category.DoesNotExist:
            return Response({"error": "QuestionBank_Category ID not found", "status": False},
                            status=status.HTTP_400_BAD_REQUEST)
        serializer = QuestionBank_CategorySerializer(user, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data, status=status.HTTP_206_PARTIAL_CONTENT)

    def delete(self, request, format=None):
        if request.GET.get('id'):
            get_object_or_404(QuestionBank_Category, id=request.GET.get('id')).delete()
        else:
            get_object_or_404(QuestionBank_Category, id=request.data.get('id')).delete()
        return Response({"success": "Id related data deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


class QuestionBank_SubCategoryView(APIView):

    def get(self, request, format=None):
        response = {}
        userId = request.GET.get('id')
        if userId:
            qs = QuestionBank_SubCategory.objects.filter(id=userId)
        else:
            qs = QuestionBank_SubCategory.objects.all()

        for data in qs:
            print(data)
            response[data.id] = {
                "id": data.id,
                "category_id": data.category.id,
                "category_name": data.category.name,
                "name": data.name
            }
        return Response(response.values(), status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        try:
            serializer = QuestionBank_SubCategorySerializer(data=data)
            if serializer.is_valid():
                serializer.save()
            return Response({"Status": True,
                             "Message": "Successfully Registered QuestionBank_SubCategory"},
                            status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"Errors": "Some field miss check and enter", "exception": str(e), "status": False},
                            status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        userId = request.GET.get('id')
        data = request.data
        try:
            user = QuestionBank_SubCategory.objects.get(id=userId)
        except QuestionBank_SubCategory.DoesNotExist:
            return Response({"error": "QuestionBank_SubCategory ID not found", "status": False},
                            status=status.HTTP_400_BAD_REQUEST)
        serializer = QuestionBank_SubCategorySerializer(user, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data, status=status.HTTP_206_PARTIAL_CONTENT)

    def delete(self, request, format=None):
        if request.GET.get('id'):
            get_object_or_404(QuestionBank_SubCategory, id=request.GET.get('id')).delete()
        else:
            get_object_or_404(QuestionBank_SubCategory, id=request.data.get('id')).delete()
        return Response({"success": "Id related data deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

class QuestionBankView(APIView):

    def get(self, request, format=None):
        response = {}
        userId = request.GET.get('id')
        if userId:
            qs = QuestionBank.objects.filter(id=userId)
        else:
            qs = QuestionBank.objects.all()

        for data in qs:
            print(data)
            response[data.id] = {
                "id": data.id,
                "sub_category_id": data.category.id,
                "sub_category_name": data.category.name,
                "examtype": data.examtype,
                "numberofmcqs": data.numberofmcqs,
                "question": data.question,
                "answer1": data.answer1,
                "answer2": data.answer2,
                "answer3": data.answer3,
                "answer4": data.answer4,
                "correctanswer": data.correctanswer,
                "explanation": data.explanation,
                "image": data.image.url if data.image else "no image"
            }
        return Response(response.values(), status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        try:
            serializer = QuestionBank_Serializer(data=data)
            if serializer.is_valid():
                serializer.save()
            return Response({"Status": True,
                             "Message": "Successfully Registered QuestionBank"},
                            status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"Errors": "Some field miss check and enter", "exception": str(e), "status": False},
                            status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        userId = request.GET.get('id')
        data = request.data
        try:
            user = QuestionBank.objects.get(id=userId)
        except QuestionBank.DoesNotExist:
            return Response({"error": "QuestionBank ID not found", "status": False},
                            status=status.HTTP_400_BAD_REQUEST)
        serializer = QuestionBank_Serializer(user, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data, status=status.HTTP_206_PARTIAL_CONTENT)

    def delete(self, request, format=None):
        if request.GET.get('id'):
            get_object_or_404(QuestionBank, id=request.GET.get('id')).delete()
        else:
            get_object_or_404(QuestionBank, id=request.data.get('id')).delete()
        return Response({"success": "Id related data deleted successfully"}, status=status.HTTP_204_NO_CONTENT)



class PrimeClassVideo_CategoryView(APIView):

    def get(self, request, format=None):
        userId = request.GET.get('id')
        if userId:
            return Response(PrimeClassVideo_CategorySerializer(get_object_or_404(PrimeClassVideo_Category, id=userId), many=False).data,
                            status=status.HTTP_200_OK)

        serializer = PrimeClassVideo_CategorySerializer(PrimeClassVideo_Category.objects.all(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        try:
            serializer = PrimeClassVideo_CategorySerializer(data=data)
            if serializer.is_valid():
                serializer.save()
            return Response({"Status": True,
                             "Message": "Successfully Registered PrimeClassVideo_Category"},
                            status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"Errors": "Some field miss check and enter", "exception": str(e), "status": False},
                            status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        userId = request.GET.get('id')
        data = request.data
        try:
            user = PrimeClassVideo_Category.objects.get(id=userId)
        except PrimeClassVideo_Category.DoesNotExist:
            return Response({"error": "PrimeClassVideo_Category ID not found", "status": False},
                            status=status.HTTP_400_BAD_REQUEST)
        serializer = PrimeClassVideo_CategorySerializer(user, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data, status=status.HTTP_206_PARTIAL_CONTENT)

    def delete(self, request, format=None):
        if request.GET.get('id'):
            get_object_or_404(PrimeClassVideo_Category, id=request.GET.get('id')).delete()
        else:
            get_object_or_404(PrimeClassVideo_Category, id=request.data.get('id')).delete()
        return Response({"success": "Id related data deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


class PrimeClassVideo_SubCategoryView(APIView):

    def get(self, request, format=None):
        response = {}
        userId = request.GET.get('id')
        if userId:
            qs = PrimeClassVideo_SubCategory.objects.filter(id=userId)
        else:
            qs = PrimeClassVideo_SubCategory.objects.all()

        for data in qs:
            print(data)
            response[data.id] = {
                "id": data.id,
                "category_id": data.category.id,
                "category_name": data.category.name,
                "name": data.name
            }
        return Response(response.values(), status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        try:
            serializer = PrimeClassVideo_SubCategorySerializer(data=data)
            if serializer.is_valid():
                serializer.save()
            return Response({"Status": True,
                             "Message": "Successfully Registered PrimeClassVideo_SubCategory"},
                            status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"Errors": "Some field miss check and enter", "exception": str(e), "status": False},
                            status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        userId = request.GET.get('id')
        data = request.data
        try:
            user = PrimeClassVideo_SubCategory.objects.get(id=userId)
        except PrimeClassVideo_SubCategory.DoesNotExist:
            return Response({"error": "PrimeClassVideo_SubCategory ID not found", "status": False},
                            status=status.HTTP_400_BAD_REQUEST)
        serializer = PrimeClassVideo_SubCategorySerializer(user, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data, status=status.HTTP_206_PARTIAL_CONTENT)

    def delete(self, request, format=None):
        if request.GET.get('id'):
            get_object_or_404(PrimeClassVideo_SubCategory, id=request.GET.get('id')).delete()
        else:
            get_object_or_404(PrimeClassVideo_SubCategory, id=request.data.get('id')).delete()
        return Response({"success": "Id related data deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

class PrimeClassVideoView(APIView):

    def get(self, request, format=None):
        response = {}
        userId = request.GET.get('id')
        if userId:
            qs = PrimeClassVideo.objects.filter(id=userId)
        else:
            qs = PrimeClassVideo.objects.all()

        for data in qs:
            print(data)
            response[data.id] = {
                "id": data.id,
                "sub_category_id": data.category.id,
                "sub_category_name": data.category.name,
                "title": data.title,        
                "video": data.video.url if data.video else "no video"
            }
        return Response(response.values(), status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        try:
            serializer = PrimeClassVideo_Serializer(data=data)
            if serializer.is_valid():
                serializer.save()
            return Response({"Status": True,
                             "Message": "Successfully Registered PrimeClassVideo"},
                            status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"Errors": "Some field miss check and enter", "exception": str(e), "status": False},
                            status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        userId = request.GET.get('id')
        data = request.data
        try:
            user = PrimeClassVideo.objects.get(id=userId)
        except PrimeClassVideo.DoesNotExist:
            return Response({"error": "PrimeClassVideo ID not found", "status": False},
                            status=status.HTTP_400_BAD_REQUEST)
        serializer = PrimeClassVideo_Serializer(user, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data, status=status.HTTP_206_PARTIAL_CONTENT)

    def delete(self, request, format=None):
        if request.GET.get('id'):
            get_object_or_404(PrimeClassVideo, id=request.GET.get('id')).delete()
        else:
            get_object_or_404(PrimeClassVideo, id=request.data.get('id')).delete()
        return Response({"success": "Id related data deleted successfully"}, status=status.HTTP_204_NO_CONTENT)



class PrimeClassAudio_CategoryView(APIView):

    def get(self, request, format=None):
        userId = request.GET.get('id')
        if userId:
            return Response(PrimeClassAudio_CategorySerializer(get_object_or_404(PrimeClassAudio_Category, id=userId), many=False).data,
                            status=status.HTTP_200_OK)

        serializer = PrimeClassAudio_CategorySerializer(PrimeClassAudio_Category.objects.all(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        try:
            serializer = PrimeClassAudio_CategorySerializer(data=data)
            if serializer.is_valid():
                serializer.save()
            return Response({"Status": True,
                             "Message": "Successfully Registered PrimeClassAudio_Category"},
                            status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"Errors": "Some field miss check and enter", "exception": str(e), "status": False},
                            status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        userId = request.GET.get('id')
        data = request.data
        try:
            user = PrimeClassAudio_Category.objects.get(id=userId)
        except PrimeClassAudio_Category.DoesNotExist:
            return Response({"error": "PrimeClassAudio_Category ID not found", "status": False},
                            status=status.HTTP_400_BAD_REQUEST)
        serializer = PrimeClassAudio_CategorySerializer(user, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data, status=status.HTTP_206_PARTIAL_CONTENT)

    def delete(self, request, format=None):
        if request.GET.get('id'):
            get_object_or_404(PrimeClassAudio_Category, id=request.GET.get('id')).delete()
        else:
            get_object_or_404(PrimeClassAudio_Category, id=request.data.get('id')).delete()
        return Response({"success": "Id related data deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


class PrimeClassAudio_SubCategoryView(APIView):

    def get(self, request, format=None):
        response = {}
        userId = request.GET.get('id')
        if userId:
            qs = PrimeClassAudio_SubCategory.objects.filter(id=userId)
        else:
            qs = PrimeClassAudio_SubCategory.objects.all()

        for data in qs:
            print(data)
            response[data.id] = {
                "id": data.id,
                "category_id": data.category.id,
                "category_name": data.category.name,
                "name": data.name
            }
        return Response(response.values(), status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        try:
            serializer = PrimeClassAudio_SubCategorySerializer(data=data)
            if serializer.is_valid():
                serializer.save()
            return Response({"Status": True,
                             "Message": "Successfully Registered PrimeClassAudio_SubCategory"},
                            status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"Errors": "Some field miss check and enter", "exception": str(e), "status": False},
                            status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        userId = request.GET.get('id')
        data = request.data
        try:
            user = PrimeClassAudio_SubCategory.objects.get(id=userId)
        except PrimeClassAudio_SubCategory.DoesNotExist:
            return Response({"error": "PrimeClassAudio_SubCategory ID not found", "status": False},
                            status=status.HTTP_400_BAD_REQUEST)
        serializer = PrimeClassAudio_SubCategorySerializer(user, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data, status=status.HTTP_206_PARTIAL_CONTENT)

    def delete(self, request, format=None):
        if request.GET.get('id'):
            get_object_or_404(PrimeClassAudio_SubCategory, id=request.GET.get('id')).delete()
        else:
            get_object_or_404(PrimeClassAudio_SubCategory, id=request.data.get('id')).delete()
        return Response({"success": "Id related data deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

class PrimeClassAudioView(APIView):

    def get(self, request, format=None):
        response = {}
        userId = request.GET.get('id')
        if userId:
            qs = PrimeClassAudio.objects.filter(id=userId)
        else:
            qs = PrimeClassAudio.objects.all()

        for data in qs:
            print(data)
            response[data.id] = {
                "id": data.id,
                "sub_category_id": data.category.id,
                "sub_category_name": data.category.name,
                "title": data.title,        
                "audio": data.audio.url if data.audio else "no audio"
            }
        return Response(response.values(), status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        try:
            serializer = PrimeClassAudio_Serializer(data=data)
            if serializer.is_valid():
                serializer.save()
            return Response({"Status": True,
                             "Message": "Successfully Registered PrimeClassAudio"},
                            status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"Errors": "Some field miss check and enter", "exception": str(e), "status": False},
                            status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        userId = request.GET.get('id')
        data = request.data
        try:
            user = PrimeClassAudio.objects.get(id=userId)
        except PrimeClassAudio.DoesNotExist:
            return Response({"error": "PrimeClassAudio ID not found", "status": False},
                            status=status.HTTP_400_BAD_REQUEST)
        serializer = PrimeClassAudio_Serializer(user, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data, status=status.HTTP_206_PARTIAL_CONTENT)

    def delete(self, request, format=None):
        if request.GET.get('id'):
            get_object_or_404(PrimeClassAudio, id=request.GET.get('id')).delete()
        else:
            get_object_or_404(PrimeClassAudio, id=request.data.get('id')).delete()
        return Response({"success": "Id related data deleted successfully"}, status=status.HTTP_204_NO_CONTENT)




class PrimeClassNotes_CategoryView(APIView):

    def get(self, request, format=None):
        userId = request.GET.get('id')
        if userId:
            return Response(PrimeClassNotes_CategorySerializer(get_object_or_404(PrimeClassNotes_Category, id=userId), many=False).data,
                            status=status.HTTP_200_OK)

        serializer = PrimeClassNotes_CategorySerializer(PrimeClassNotes_Category.objects.all(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        try:
            serializer = PrimeClassNotes_CategorySerializer(data=data)
            if serializer.is_valid():
                serializer.save()
            return Response({"Status": True,
                             "Message": "Successfully Registered PrimeClassNotes_Category"},
                            status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"Errors": "Some field miss check and enter", "exception": str(e), "status": False},
                            status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        userId = request.GET.get('id')
        data = request.data
        try:
            user = PrimeClassNotes_Category.objects.get(id=userId)
        except PrimeClassNotes_Category.DoesNotExist:
            return Response({"error": "PrimeClassNotes_Category ID not found", "status": False},
                            status=status.HTTP_400_BAD_REQUEST)
        serializer = PrimeClassNotes_CategorySerializer(user, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data, status=status.HTTP_206_PARTIAL_CONTENT)

    def delete(self, request, format=None):
        if request.GET.get('id'):
            get_object_or_404(PrimeClassNotes_Category, id=request.GET.get('id')).delete()
        else:
            get_object_or_404(PrimeClassNotes_Category, id=request.data.get('id')).delete()
        return Response({"success": "Id related data deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


class PrimeClassNotes_SubCategoryView(APIView):

    def get(self, request, format=None):
        response = {}
        userId = request.GET.get('id')
        if userId:
            qs = PrimeClassNotes_SubCategory.objects.filter(id=userId)
        else:
            qs = PrimeClassNotes_SubCategory.objects.all()

        for data in qs:
            print(data)
            response[data.id] = {
                "id": data.id,
                "category_id": data.category.id,
                "category_name": data.category.name,
                "name": data.name
            }
        return Response(response.values(), status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        try:
            serializer = PrimeClassNotes_SubCategorySerializer(data=data)
            if serializer.is_valid():
                serializer.save()
            return Response({"Status": True,
                             "Message": "Successfully Registered PrimeClassNotes_SubCategory"},
                            status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"Errors": "Some field miss check and enter", "exception": str(e), "status": False},
                            status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        userId = request.GET.get('id')
        data = request.data
        try:
            user = PrimeClassNotes_SubCategory.objects.get(id=userId)
        except PrimeClassNotes_SubCategory.DoesNotExist:
            return Response({"error": "PrimeClassNotes_SubCategory ID not found", "status": False},
                            status=status.HTTP_400_BAD_REQUEST)
        serializer = PrimeClassNotes_SubCategorySerializer(user, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data, status=status.HTTP_206_PARTIAL_CONTENT)

    def delete(self, request, format=None):
        if request.GET.get('id'):
            get_object_or_404(PrimeClassNotes_SubCategory, id=request.GET.get('id')).delete()
        else:
            get_object_or_404(PrimeClassNotes_SubCategory, id=request.data.get('id')).delete()
        return Response({"success": "Id related data deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

class PrimeClassNotesView(APIView):
    
    def get(self, request, format=None):
        response = {}
        userId = request.GET.get('id')
        if userId:
            qs = PrimeClassNotes.objects.filter(id=userId)
        else:
            qs = PrimeClassNotes.objects.all()

        for data in qs:
            print(data)
            response[data.id] = {
                "id": data.id,
                "sub_category_id": data.category.id,
                "sub_category_name": data.category.name,
                "title": data.title,        
                "pdf": data.pdf.url if data.pdf else "no pdf"
            }
        return Response(response.values(), status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        try:
            serializer = PrimeClassNotes_Serializer(data=data)
            if serializer.is_valid():
                serializer.save()
            return Response({"Status": True,
                             "Message": "Successfully Registered PrimeClassNotes"},
                            status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"Errors": "Some field miss check and enter", "exception": str(e), "status": False},
                            status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        userId = request.GET.get('id')
        data = request.data
        try:
            user = PrimeClassNotes.objects.get(id=userId)
        except PrimeClassNotes.DoesNotExist:
            return Response({"error": "PrimeClassNotes ID not found", "status": False},
                            status=status.HTTP_400_BAD_REQUEST)
        serializer = PrimeClassNotes_Serializer(user, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data, status=status.HTTP_206_PARTIAL_CONTENT)

    def delete(self, request, format=None):
        if request.GET.get('id'):
            get_object_or_404(PrimeClassNotes, id=request.GET.get('id')).delete()
        else:
            get_object_or_404(PrimeClassNotes, id=request.data.get('id')).delete()
        return Response({"success": "Id related data deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


