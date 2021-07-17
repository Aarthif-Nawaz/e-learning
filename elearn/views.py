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
import uuid
from django.db.models import Q
from operator import itemgetter
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.authtoken.models import Token
from django.core import serializers
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from django.contrib.sessions.backends.db import SessionStore


class RegistrationView(APIView):

    def get(self, request):
        response = {}
        userId = request.GET.get('id')
        if userId:
            qs = User.objects.filter(id=userId)
        else:
            qs = User.objects.all().order_by('id')

        for data in qs:
            response[data.id] = {
                "id": data.id,
                "user_name": data.name,
                "mobile": data.mobile,
                "email": data.email,
                "collegue": data.college,
                "location": data.location,
                "is_blocked": data.is_blocked
            }
        return Response(response.values(), status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        if data.get('mobile'):
            finding_exising_user_detail = User.objects.filter(mobile__iexact=data.get('mobile'))

            if finding_exising_user_detail.exists():
                return Response({"message": "Mobile Already Exists"},
                                status=status.HTTP_200_OK)
        if data.get('email'):
            finding_exising_user_detail = User.objects.filter(email__iexact=data.get('email'))
            if finding_exising_user_detail.exists():
                return Response({"message": "Email Already Exists"},
                                status=status.HTTP_200_OK)
        try:
            serializer = UserSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                id = serializer.data['id']
                return Response({"Status": True,
                                 "Message": "Successfully Registered User", "User ID": id},
                                status=status.HTTP_201_CREATED)
            return Response({"Status": True,
                             "Message": f" : Unable to register"},
                            status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"Errors": "Some field miss check and enter", "exception": str(e), "status": False},
                            status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        userId = request.GET.get('id')
        data = request.data
        try:
            user = User.objects.get(id=userId)
        except User.DoesNotExist:
            return Response({"error": "User ID not found", "status": False}, status=status.HTTP_400_BAD_REQUEST)
        serializer = UserSerializer(user, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data, status=status.HTTP_206_PARTIAL_CONTENT)

    def delete(self, request, format=None):
        if request.GET.get('id'):
            get_object_or_404(User, id=request.GET.get('id')).delete()
        else:
            get_object_or_404(User, id=request.data.get('id')).delete()
        return Response({"success": "Id related data deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


class Login(APIView):

    def post(self, request):
        data = request.data
        finding_exising_user = User.objects.filter(mobile__exact=data.get('mobile'))
        if finding_exising_user.exists():
            for data in finding_exising_user:
                if not data.is_blocked:
                    return Response({"user_id": data.id, "user_name": data.name, "mobile": data.mobile, "email": data.email},
                                    status=status.HTTP_200_OK)
                else:
                    return Response({"message": "User Blocked"},
                                    status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response({'message': 'No Such mobile exists'}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        userId = request.GET.get('id')
        try:
            user = User.objects.get(id=userId)
        except User.DoesNotExist:
            return Response({"error": "User ID not found", "status": False}, status=status.HTTP_400_BAD_REQUEST)

        data = {"is_blocked": request.data.get('is_blocked')}
        serializer = UserBlockedSerializer(user, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data, status=status.HTTP_206_PARTIAL_CONTENT)


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
            print(data)
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
        cat_Id = request.GET.get('cat_id')
        if userId:
            qs = ShotsSubCategory.objects.filter(id=userId)
        elif cat_Id:
            subid = get_object_or_404(ShotsCategory, id=cat_Id)
            qs = subid.shotssubcategory_set.all().order_by('id')
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
        cat_Id = request.GET.get('cat_id')
        if userId:
            qs = Diff_Dig_SubCategory.objects.filter(id=userId)
        elif cat_Id:
            subid = get_object_or_404(Diff_Dig_Category, id=cat_Id)
            qs = subid.diff_dig_subcategory_set.all().order_by('id')
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
        if data.get('sub_category'):
            finding_exising_sub_category_detail = Diff_Dig.objects.filter(sub_category_id=data.get('sub_category'))
            if finding_exising_sub_category_detail.exists():
                return Response({"message": "Sub Category Already Exists"},
                                status=status.HTTP_400_BAD_REQUEST)
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
                             "Message": "Successfully Registered Recent Updates Category"},
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
            return Response({"error": "Recent Category ID not found", "status": False},
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
        cat_Id = request.GET.get('cat_id')
        if userId:
            qs = Recent_Updates_SubCategory.objects.filter(id=userId)
        elif cat_Id:
            subid = get_object_or_404(Recent_Updates_Category, id=cat_Id)
            qs = subid.recent_updates_subcategory_set.all().order_by('id')
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
                             "Message": "Successfully Registered Recent Updates SubCategory"},
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
            return Response({"error": "Recent Updates Sub Category ID not found", "status": False},
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
        if data.get('sub_category'):
            finding_exising_sub_category_detail = recent_updates.objects.filter(
                sub_category_id=data.get('sub_category'))
            if finding_exising_sub_category_detail.exists():
                return Response({"message": "Sub Category Already Exists"},
                                status=status.HTTP_400_BAD_REQUEST)
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
        cat_Id = request.GET.get('cat_id')
        if userId:
            qs = Values_SubCategory.objects.filter(id=userId)
        elif cat_Id:
            subid = get_object_or_404(Values_Category, id=cat_Id)
            qs = subid.values_subcategory_set.all().order_by('id')
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
        if data.get('sub_category'):
            finding_exising_sub_category_detail = Values.objects.filter(sub_category_id=data.get('sub_category'))
            if finding_exising_sub_category_detail.exists():
                return Response({"message": "Sub Category Already Exists"},
                                status=status.HTTP_400_BAD_REQUEST)
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
        cat_Id = request.GET.get('cat_id')
        if userId:
            qs = ICardsPDF_SubCategory.objects.filter(id=userId)
        elif cat_Id:
            subid = get_object_or_404(ICardsPDF_Category, id=cat_Id)
            qs = subid.icardspdf_subcategory_set.all().order_by('id')
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
        if data.get('sub_category'):
            finding_exising_sub_category_detail = ICardsPDF.objects.filter(sub_category_id=data.get('sub_category'))
            if finding_exising_sub_category_detail.exists():
                return Response({"message": "Sub Category Already Exists"},
                                status=status.HTTP_400_BAD_REQUEST)
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
        cat_Id = request.GET.get('cat_id')
        if userId:
            qs = ICardsVideo_SubCategory.objects.filter(id=userId)
        elif cat_Id:
            subid = get_object_or_404(ICardsVideo_Category, id=cat_Id)
            qs = subid.icardsvideo_subcategory_set.all().order_by('id')
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
        cat_Id = request.GET.get('cat_id')
        if userId:
            qs = ICardsAudio_SubCategory.objects.filter(id=userId)
        elif cat_Id:
            subid = get_object_or_404(ICardsAudio_Category, id=cat_Id)
            qs = subid.icardsaudio_subcategory_set.all().order_by('id')
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
        cat_Id = request.GET.get('cat_id')
        if userId:
            qs = ImageBank_SubCategory.objects.filter(id=userId)
        elif cat_Id:
            subid = get_object_or_404(ImageBank_Category, id=cat_Id)
            qs = subid.imagebank_subcategory_set.all().order_by('id')
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
        if data.get('sub_category'):
            finding_exising_sub_category_detail = ImageBank.objects.filter(sub_category_id=data.get('sub_category'))
            if finding_exising_sub_category_detail.exists():
                return Response({"message": "Sub Category Already Exists"},
                                status=status.HTTP_400_BAD_REQUEST)
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
        cat_Id = request.GET.get('cat_id')
        if userId:
            qs = WallPoster_SubCategory.objects.filter(id=userId)
        elif cat_Id:
            subid = get_object_or_404(WallPoster_Category, id=cat_Id)
            qs = subid.wallposter_subcategory_set.all().order_by('id')
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
        if data.get('sub_category'):
            finding_exising_sub_category_detail = WallPosters.objects.filter(sub_category_id=data.get('sub_category'))
            if finding_exising_sub_category_detail.exists():
                return Response({"message": "Sub Category Already Exists"},
                                status=status.HTTP_400_BAD_REQUEST)
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
            qs = QuestionOfTheDay.objects.all().order_by('id').first()

        try:
            response[qs.id] = {
                "id": qs.id,
                "Question": qs.Question,
                "Answer1": qs.Answer1,
                "Answer2": qs.Answer2,
                "Answer3": qs.Answer3,
                "Answer4": qs.Answer4,
                "CorrectAnswer": qs.CorrectAnswer,
                "Explanation": qs.Explanation,
                "image": qs.Image.url if qs.Image else "no image"

            }
            return Response(response.values(), status=status.HTTP_200_OK)
        except:
            return Response({'message': 'No Data'}, status=status.HTTP_400_BAD_REQUEST)

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
            QuestionOfTheDay.objects.all().delete()
        return Response({"success": "Id related data deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


class DailyBoosterMainView(APIView):

    def get(self, request, format=None):
        response = {}
        userId = request.GET.get('id')
        if userId:
            qs = DailyBoosterMain.objects.filter(id=userId)
        else:
            qs = DailyBoosterMain.objects.all().order_by('id')
        for data in qs:
            response[data.id] = {
                "id": data.id,
                "bannerImage": data.banner.banner.url,
                "title": data.title,
                "banner_id": data.banner.id,
                "timer": data.timer,
                "no_of_questions": data.no_of_mcq,
            }
        return Response(response.values(), status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        try:
            serializer = DailyBoosterMainSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response({"Status": True,
                                 "Message": "Successfully Registered DailyBoosterMainQuiz"},
                                status=status.HTTP_201_CREATED)
            return Response({"Status": False,
                             "Message": "Not Successfully Registered DailyBoosterMainQuiz"},
                            status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"Errors": "Some field miss check and enter", "exception": str(e), "status": False},
                            status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        userId = request.GET.get('id')
        data = request.data
        try:
            user = DailyBoosterMain.objects.get(id=userId)
        except DailyBoosterMain.DoesNotExist:
            return Response({"error": "DailyBoosterQuiz ID not found", "status": False},
                            status=status.HTTP_400_BAD_REQUEST)
        serializer = DailyBoosterMainSerializer(user, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data, status=status.HTTP_206_PARTIAL_CONTENT)

    def delete(self, request, format=None):
        if request.GET.get('id'):
            get_object_or_404(DailyBoosterMain, id=request.GET.get('id')).delete()
        else:
            get_object_or_404(DailyBoosterMain, id=request.data.get('id')).delete()
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
                "banner_image": data.dailyboostdetail.banner.banner.url,
                "banner_id": data.dailyboostdetail.banner.banner.id,
                "banner_title": data.dailyboostdetail.banner.title,
                "timer": data.dailyboostdetail.timer,
                "no_of_mcq": data.dailyboostdetail.no_of_mcq,
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
            DailyBoosterQuiz.objects.all().delete()
        return Response({"success": "Id related data deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


class DailyBoosterTimerQuizView(APIView):
    def get(self, request, format=None):
        response = {}
        date = request.GET.get('date')
        user_id = request.GET.get('user_id')
        if date and user_id:
            qs = DailyBoosterQuizTimer.objects.filter(date__exact=date, user_id=user_id).order_by('date')
        else:
            qs = DailyBoosterQuizTimer.objects.filter(date__exact=date).order_by('date')
        for data in qs:
            response[data.id] = {
                "id": data.id,
                "date": data.date,
                "timer": data.timer,
                "user_id": data.user.id
            }
        return Response(response.values(), status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        user_id = request.GET.get('user_id')
        if data.get('date') and user_id:
            finding_exising_date_detail = DailyBoosterQuizTimer.objects.filter(date__exact=data.get('date'),
                                                                               user_id=user_id)
            if finding_exising_date_detail.exists():
                return Response({"message": "Date Already Exists"},
                                status=status.HTTP_400_BAD_REQUEST)

        try:
            serializer = DailyBoosterQuizTimeSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
            return Response({"Status": True,
                             "Message": "Successfully Registered DailyBoosterQuizTimer"},
                            status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"Errors": "Some field miss check and enter", "exception": str(e), "status": False},
                            status=status.HTTP_400_BAD_REQUEST)


class DailyBoosterCompletedQuizView(APIView):

    def get(self, request, format=None):
        response = {}
        date = request.GET.get('date')
        user_id = request.GET.get('user_id')
        if date and user_id:
            qs = DailyBoosterCompleted.objects.filter(date__exact=date, user_id=user_id).order_by('date')
        else:
            qs = DailyBoosterCompleted.objects.filter(date__exact=date).order_by('date')
        for data in qs:
            response[data.id] = {
                "id": data.id,
                "date": data.date,
                "correct": data.correct,
                "wrong": data.wrong,
                "user_id": data.user.id
            }
        return Response(response.values(), status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        user_id = request.GET.get('user_id')
        if data.get('date') and user_id:
            finding_exising_date_detail = DailyBoosterCompleted.objects.filter(date__exact=data.get('date'),
                                                                               user_id=user_id)
            if finding_exising_date_detail.exists():
                return Response({"message": "Date Already Exists"},
                                status=status.HTTP_400_BAD_REQUEST)

        try:
            serializer = DailyBoosterQuizCompletedSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
            return Response({"Status": True,
                             "Message": "Successfully Registered DailyBoosterQuizCompleted"},
                            status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"Errors": "Some field miss check and enter", "exception": str(e), "status": False},
                            status=status.HTTP_400_BAD_REQUEST)


class QuestionBank_CategoryView(APIView):

    def get(self, request, format=None):
        userId = request.GET.get('id')
        if userId:
            return Response(
                QuestionBank_CategorySerializer(get_object_or_404(QuestionBank_Category, id=userId), many=False).data,
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
        cat_Id = request.GET.get('cat_id')
        if userId:
            qs = QuestionBank_SubCategory.objects.filter(id=userId)
        elif cat_Id:
            subid = get_object_or_404(QuestionBank_Category, id=cat_Id)
            qs = subid.questionbank_subcategory_set.all().order_by('id')
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
        Id = request.GET.get('id')
        user_id = request.GET.get('user_id')
        if Id:
            qs = QuestionBank.objects.filter(id=Id)
        elif user_id:
            userId = get_object_or_404(User, id=user_id)
            qs = userId.questionbank_set.all().order_by('id')
        else:
            qs = QuestionBank.objects.all()

        for data in qs:
            print(data)
            response[data.id] = {
                "id": data.id,
                "category_id": data.category.id,
                "category_name": data.category.name,
                "sub_category_id": data.sub_category.id,
                "sub_category_name": data.sub_category.name,
                "examtype": data.examtype,
                "numberofmcqs": data.numberofmcqs,
                "exam_mode": data.exam_mode,
                "user_id": data.user.id,
                "user_name": data.user.name
            }
        return Response(response.values(), status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        try:
            serializer = QuestionBank_Serializer(data=data)
            if serializer.is_valid():
                serializer.save()
            return Response({"Status": True,
                             "Message": "Successfully Registered QuestionBank User"},
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


class QuestionBankModeView(APIView):
    def get(self, request, format=None):
        response = {}
        Id = request.GET.get('id')
        level = request.GET.get('level')
        sub_cat = request.GET.get('sub_cat')
        type = request.GET.get('type')
        if Id:
            qs = QuestionBankMode.objects.filter(id=Id)
        elif level and sub_cat and type:
            qs = QuestionBankMode.objects.filter(level__exact=level, sub_category_id=sub_cat,
                                                 examtype__exact=type).order_by('id')
        elif level:
            qs = QuestionBankMode.objects.filter(level__exact=level).order_by('id')
        elif sub_cat:
            qs = QuestionBankMode.objects.filter(sub_category_id=sub_cat).order_by('id')
        elif type:
            qs = QuestionBankMode.objects.filter(examtype__exact=type).order_by('id')
        else:
            qs = QuestionBank.objects.all().order_by('id')

        for data in qs:
            print(data)
            response[data.id] = {
                "id": data.id,
                "sub_category_id": data.sub_category.id,
                "sub_category_name": data.sub_category.name,
                "examtype": data.examtype,
                "level": data.level,
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
            serializer = QuestionBankModeSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
            return Response({"Status": True,
                             "Message": "Successfully Registered QuestionBankMode Questions"},
                            status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"Errors": "Some field miss check and enter", "exception": str(e), "status": False},
                            status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        userId = request.GET.get('id')
        data = request.data
        try:
            user = QuestionBankMode.objects.get(id=userId)
        except QuestionBankMode.DoesNotExist:
            return Response({"error": "QuestionBank Mode ID not found", "status": False},
                            status=status.HTTP_400_BAD_REQUEST)
        serializer = QuestionBankModeSerializer(user, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data, status=status.HTTP_206_PARTIAL_CONTENT)

    def delete(self, request, format=None):
        if request.GET.get('id'):
            get_object_or_404(QuestionBankMode, id=request.GET.get('id')).delete()
        else:
            get_object_or_404(QuestionBankMode, id=request.data.get('id')).delete()
        return Response({"success": "Id related data deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


class QuestionBankTestModeView(APIView):

    def get(self, request, format=None):
        response = {}
        Id = request.GET.get('id')
        level = request.GET.get('level')
        sub_cat = request.GET.get('sub_cat')
        type = request.GET.get('type')
        if Id:
            qs = QuestionBankTestMode.objects.filter(id=Id)
        elif level and sub_cat and type:
            qs = QuestionBankTestMode.objects.filter(level__exact=level, sub_category_id=sub_cat,
                                                     examtype__exact=type).order_by('id')
        elif level:
            qs = QuestionBankTestMode.objects.filter(level__exact=level).order_by('id')
        elif sub_cat:
            qs = QuestionBankTestMode.objects.filter(sub_category_id=sub_cat).order_by('id')
        elif type:
            qs = QuestionBankTestMode.objects.filter(examtype__exact=type).order_by('id')
        else:
            qs = QuestionBankTestMode.objects.all().order_by('id')

        for data in qs:
            print(data)
            response[data.id] = {
                "id": data.id,
                "sub_category_id": data.sub_category.id,
                "sub_category_name": data.sub_category.name,
                "examtype": data.examtype,
                "level": data.level,
                "question": data.question,
                "answer1": data.answer1,
                "answer2": data.answer2,
                "answer3": data.answer3,
                "answer4": data.answer4,
                "correctanswer": data.correctanswer,
                "timer": data.timer,
            }
        return Response(response.values(), status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        try:
            serializer = QuestionBankTestModeSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
            return Response({"Status": True,
                             "Message": "Successfully Registered QuestionBankTestMode Questions"},
                            status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"Errors": "Some field miss check and enter", "exception": str(e), "status": False},
                            status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        userId = request.GET.get('id')
        data = request.data
        try:
            user = QuestionBankTestMode.objects.get(id=userId)
        except QuestionBankTestMode.DoesNotExist:
            return Response({"error": "QuestionBank TestMode ID not found", "status": False},
                            status=status.HTTP_400_BAD_REQUEST)
        serializer = QuestionBankTestModeSerializer(user, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data, status=status.HTTP_206_PARTIAL_CONTENT)

    def delete(self, request, format=None):
        if request.GET.get('id'):
            get_object_or_404(QuestionBankTestMode, id=request.GET.get('id')).delete()
        else:
            get_object_or_404(QuestionBankTestMode, id=request.data.get('id')).delete()
        return Response({"success": "Id related data deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


class QuestionBankTimerQuizView(APIView):
    def get(self, request, format=None):
        response = {}
        date = request.GET.get('date')
        timer = request.GET.get('timer')
        user_id = request.GET.get('user_id')
        mode = request.GET.get('mode')
        if date and user_id and mode and timer:
            qs = QuestionBankQuizTimer.objects.filter(date__exact=date, question_bank__user_id=user_id,
                                                      question_bank__exam_mode__exact=mode,
                                                      timer__exact=timer).order_by('date')
        elif date and user_id and mode:
            qs = QuestionBankQuizTimer.objects.filter(date__exact=date, question_bank__user_id=user_id,
                                                      question_bank__exam_mode__exact=mode).order_by('date')
        elif user_id and mode:
            qs = QuestionBankQuizTimer.objects.filter(question_bank__user_id=user_id,
                                                      question_bank__exam_mode__exact=mode).order_by('user_id')
        else:
            qs = QuestionBankQuizTimer.objects.filter(date__exact=date).order_by('date')
        for data in qs:
            response[data.id] = {
                "id": data.id,
                "mode": data.question_bank.exam_mode,
                "type": data.question_bank.examtype,
                "date": data.date,
                "timer": data.timer,
                "user_id": data.question_bank.user.id
            }
        return Response(response.values(), status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        try:
            serializer = QuestionBankQuizTimerSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
            return Response({"Status": True,
                             "Message": "Successfully Registered QuestionBankQuiz Timer"},
                            status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"Errors": "Some field miss check and enter", "exception": str(e), "status": False},
                            status=status.HTTP_400_BAD_REQUEST)


class QuestionBankCompletedQuizView(APIView):

    def get(self, request, format=None):
        response = {}
        date = request.GET.get('date')
        user_id = request.GET.get('user_id')
        mode = request.GET.get('mode')
        if date and user_id and mode:
            qs = QuestionBankCompleted.objects.filter(date__exact=date, question_bank__user_id=user_id,
                                                      question_bank__exam_mode__exact=mode).order_by('date')
        elif user_id and mode:
            qs = QuestionBankCompleted.objects.filter(question_bank__user_id=user_id,
                                                      question_bank__exam_mode__exact=mode).order_by('date')
        else:
            qs = QuestionBankCompleted.objects.filter(date__exact=date).order_by('date')
        for data in qs:
            response[data.id] = {
                "id": data.id,
                "mode": data.question_bank.exam_mode,
                "type": data.question_bank.examtype,
                "date": data.date,
                "correct": data.correct,
                "wrong": data.wrong,
                "user_id": data.question_bank.user.id
            }
        return Response(response.values(), status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data

        try:
            serializer = QuestionBankCompletedSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
            return Response({"Status": True,
                             "Message": "Successfully Registered QuestionBankCompleted"},
                            status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"Errors": "Some field miss check and enter", "exception": str(e), "status": False},
                            status=status.HTTP_400_BAD_REQUEST)


class PrimeClassVideo_CategoryView(APIView):

    def get(self, request, format=None):
        userId = request.GET.get('id')
        if userId:
            return Response(PrimeClassVideo_CategorySerializer(get_object_or_404(PrimeClassVideo_Category, id=userId),
                                                               many=False).data,
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
        cat_Id = request.GET.get('cat_id')
        if userId:
            qs = PrimeClassVideo_SubCategory.objects.filter(id=userId)
        elif cat_Id:
            subid = get_object_or_404(PrimeClassVideo_Category, id=cat_Id)
            qs = subid.primeclassvideo_subcategory_set.all().order_by('id')
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
        sub_id = request.GET.get('sub_id')
        if userId:
            qs = PrimeClassVideo.objects.filter(id=userId)
        elif sub_id:
            qs = PrimeClassVideo.objects.filter(sub_category_id=sub_id)
        else:
            qs = PrimeClassVideo.objects.all()

        for data in qs:
            response[data.id] = {
                "id": data.id,
                "sub_category_id": data.sub_category.id,
                "sub_category_name": data.sub_category.name,
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
            return Response(PrimeClassAudio_CategorySerializer(get_object_or_404(PrimeClassAudio_Category, id=userId),
                                                               many=False).data,
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
        cat_Id = request.GET.get('cat_id')
        if userId:
            qs = PrimeClassAudio_SubCategory.objects.filter(id=userId)
        elif cat_Id:
            subid = get_object_or_404(PrimeClassAudio_Category, id=cat_Id)
            qs = subid.primeclassaudio_subcategory_set.all().order_by('id')
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
        sub_id = request.GET.get('sub_id')
        if userId:
            qs = PrimeClassAudio.objects.filter(id=userId)
        elif sub_id:
            qs = PrimeClassAudio.objects.filter(sub_category_id=sub_id)
        else:
            qs = PrimeClassAudio.objects.all()

        for data in qs:
            print(data)
            response[data.id] = {
                "id": data.id,
                "sub_category_id": data.sub_category.id,
                "sub_category_name": data.sub_category.name,
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
            return Response(PrimeClassNotes_CategorySerializer(get_object_or_404(PrimeClassNotes_Category, id=userId),
                                                               many=False).data,
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
        cat_Id = request.GET.get('cat_id')
        if userId:
            qs = PrimeClassNotes_SubCategory.objects.filter(id=userId)
        elif cat_Id:
            subid = get_object_or_404(PrimeClassNotes_Category, id=cat_Id)
            qs = subid.primeclassnotes_subcategory_set.all().order_by('id')
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
        sub_id = request.GET.get('sub_id')
        if userId:
            qs = PrimeClassNotes.objects.filter(id=userId)
        elif sub_id:
            qs = PrimeClassNotes.objects.filter(sub_category_id=sub_id)
        else:
            qs = PrimeClassNotes.objects.all()

        for data in qs:
            print(data)
            response[data.id] = {
                "id": data.id,
                "sub_category_id": data.sub_category.id,
                "sub_category_name": data.sub_category.name,
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
            PrimeClassNotes.objects.all().delete()
        return Response({"success": "Id related data deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


# -------------Live class ------------------

class LiveClass_CategoryView(APIView):

    def get(self, request, format=None):
        userId = request.GET.get('id')
        if userId:
            return Response(
                LiveClass_CategorySerializer(get_object_or_404(LiveClass_Category, id=userId), many=False).data,
                status=status.HTTP_200_OK)

        serializer = LiveClass_CategorySerializer(LiveClass_Category.objects.all(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        try:
            serializer = LiveClass_CategorySerializer(data=data)
            if serializer.is_valid():
                serializer.save()
            return Response({"Status": True,
                             "Message": "Successfully Registered LiveClass_Category"},
                            status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"Errors": "Some field miss check and enter", "exception": str(e), "status": False},
                            status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        userId = request.GET.get('id')
        data = request.data
        try:
            user = LiveClass_Category.objects.get(id=userId)
        except LiveClass_Category.DoesNotExist:
            return Response({"error": "LiveClass_Category ID not found", "status": False},
                            status=status.HTTP_400_BAD_REQUEST)
        serializer = LiveClass_CategorySerializer(user, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data, status=status.HTTP_206_PARTIAL_CONTENT)

    def delete(self, request, format=None):
        if request.GET.get('id'):
            get_object_or_404(LiveClass_Category, id=request.GET.get('id')).delete()
        else:
            get_object_or_404(LiveClass_Category, id=request.data.get('id')).delete()
        return Response({"success": "Id related data deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


class LiveClass_SubCategoryView(APIView):

    def get(self, request, format=None):
        response = {}
        userId = request.GET.get('id')
        cat_Id = request.GET.get('cat_id')
        if userId:
            qs = LiveClass_SubCategory.objects.filter(id=userId)
        elif cat_Id:
            subid = get_object_or_404(LiveClass_Category, id=cat_Id)
            qs = subid.liveclass_subcategory_set.all().order_by('id')
        else:
            qs = LiveClass_SubCategory.objects.all()

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
            serializer = LiveClass_SubCategorySerializer(data=data)
            if serializer.is_valid():
                serializer.save()
            return Response({"Status": True,
                             "Message": "Successfully Registered LiveClass_SubCategory"},
                            status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"Errors": "Some field miss check and enter", "exception": str(e), "status": False},
                            status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        userId = request.GET.get('id')
        data = request.data
        try:
            user = LiveClass_SubCategory.objects.get(id=userId)
        except LiveClass_SubCategory.DoesNotExist:
            return Response({"error": "LiveClass_SubCategory ID not found", "status": False},
                            status=status.HTTP_400_BAD_REQUEST)
        serializer = LiveClass_SubCategorySerializer(user, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data, status=status.HTTP_206_PARTIAL_CONTENT)

    def delete(self, request, format=None):
        if request.GET.get('id'):
            get_object_or_404(LiveClass_SubCategory, id=request.GET.get('id')).delete()
        else:
            get_object_or_404(LiveClass_SubCategory, id=request.data.get('id')).delete()
        return Response({"success": "Id related data deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


class LiveClassView(APIView):

    def get(self, request, format=None):
        response = {}
        userId = request.GET.get('id')
        sub_id = request.GET.get('sub_id')
        if userId:
            qs = LiveClass.objects.filter(id=userId)
        elif sub_id:
            qs = LiveClass.objects.filter(sub_category_id=sub_id)
        else:
            qs = LiveClass.objects.all()

        for data in qs:
            print(data)
            response[data.id] = {
                "id": data.id,
                "sub_category_id": data.sub_category.id,
                "sub_category_name": data.sub_category.name,
                "banner_id": data.banner.id,
                "banner": data.banner.bannerimage.url,
                "title": data.title,
                "video": data.video,
            }
        return Response(response.values(), status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        try:
            serializer = LiveClass_Serializer(data=data)
            if serializer.is_valid():
                serializer.save()
            return Response({"Status": True,
                             "Message": "Successfully Registered LiveClass"},
                            status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"Errors": "Some field miss check and enter", "exception": str(e), "status": False},
                            status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        userId = request.GET.get('id')
        data = request.data
        try:
            user = LiveClass.objects.get(id=userId)
        except LiveClass.DoesNotExist:
            return Response({"error": "LiveClass ID not found", "status": False},
                            status=status.HTTP_400_BAD_REQUEST)
        serializer = LiveClass_Serializer(user, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data, status=status.HTTP_206_PARTIAL_CONTENT)

    def delete(self, request, format=None):
        if request.GET.get('id'):
            get_object_or_404(LiveClass, id=request.GET.get('id')).delete()
        else:
            get_object_or_404(LiveClass, id=request.data.get('id')).delete()
        return Response({"success": "Id related data deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


class LiveClassBannerImageView(APIView):

    def get(self, request, format=None):
        response = {}
        userId = request.GET.get('id')
        if userId:
            qs = LiveClassBannerImage.objects.filter(id=userId)
        else:
            qs = LiveClassBannerImage.objects.all().order_by('id')

        for data in qs:
            response[data.id] = {
                "id": data.id,
                "title": data.title,
                "banner": data.bannerimage.url if data.bannerimage else "no image"
            }
        return Response(response.values(), status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        try:
            serializer = LiveClassBannerImage_Serializer(data=data)
            if serializer.is_valid():
                serializer.save()
            return Response({"Status": True,
                             "Message": "Successfully Registered LiveClassBannerImage"},
                            status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"Errors": "Some field miss check and enter", "exception": str(e), "status": False},
                            status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        userId = request.GET.get('id')
        data = request.data
        try:
            user = LiveClassBannerImage.objects.get(id=userId)
        except LiveClassBannerImage.DoesNotExist:
            return Response({"error": "LiveClassBannerImage ID not found", "status": False},
                            status=status.HTTP_400_BAD_REQUEST)
        serializer = LiveClassBannerImage_Serializer(user, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data, status=status.HTTP_206_PARTIAL_CONTENT)

    def delete(self, request, format=None):
        if request.GET.get('id'):
            get_object_or_404(LiveClassBannerImage, id=request.GET.get('id')).delete()
        else:
            get_object_or_404(LiveClassBannerImage, id=request.data.get('id')).delete()
        return Response({"success": "Id related data deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


# ---------------------QuestionBankPreviousQuestions------


class QuestionBankPreviousQuestions_CategoryView(APIView):

    def get(self, request, format=None):
        userId = request.GET.get('id')
        if userId:
            return Response(
                QuestionBankPreviousQuestions_CategorySerializer(
                    get_object_or_404(QuestionBankPreviousQuestions_Category, id=userId),
                    many=False).data,
                status=status.HTTP_200_OK)

        serializer = QuestionBankPreviousQuestions_CategorySerializer(
            QuestionBankPreviousQuestions_Category.objects.all(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        try:
            serializer = QuestionBankPreviousQuestions_CategorySerializer(data=data)
            if serializer.is_valid():
                serializer.save()
            return Response({"Status": True,
                             "Message": "Successfully Registered QuestionBankPreviousQuestions_Category"},
                            status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"Errors": "Some field miss check and enter", "exception": str(e), "status": False},
                            status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        userId = request.GET.get('id')
        data = request.data
        try:
            user = QuestionBankPreviousQuestions_Category.objects.get(id=userId)
        except QuestionBankPreviousQuestions_Category.DoesNotExist:
            return Response({"error": "Question Bank ID not found", "status": False},
                            status=status.HTTP_400_BAD_REQUEST)
        serializer = QuestionBankPreviousQuestions_CategorySerializer(user, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data, status=status.HTTP_206_PARTIAL_CONTENT)

    def delete(self, request, format=None):
        if request.GET.get('id'):
            get_object_or_404(QuestionBankPreviousQuestions_Category, id=request.GET.get('id')).delete()
        else:
            QuestionBankPreviousQuestions_Category.objects.all().delete()
        return Response({"success": "Id related data deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


class QuestionBankPreviousQuestions_SubCategoryView(APIView):

    def get(self, request, format=None):
        response = {}
        userId = request.GET.get('id')
        cat_Id = request.GET.get('cat_id')
        if userId:
            qs = QuestionBankPreviousQuestions_SubCategory.objects.filter(id=userId)
        elif cat_Id:
            subid = get_object_or_404(QuestionBankPreviousQuestions_Category, id=cat_Id)
            qs = subid.questionbankpreviousquestions_subcategory_set.all().order_by('id')
        else:
            qs = QuestionBankPreviousQuestions_SubCategory.objects.all()

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
            serializer = QuestionBankPreviousQuestions_SubCategorySerializer(data=data)
            if serializer.is_valid():
                serializer.save()
            return Response({"Status": True,
                             "Message": "Successfully Registered QuestionBankPreviousQuestions_SubCategory"},
                            status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"Errors": "Some field miss check and enter", "exception": str(e), "status": False},
                            status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        userId = request.GET.get('id')
        data = request.data
        try:
            user = QuestionBankPreviousQuestions_SubCategory.objects.get(id=userId)
        except QuestionBankPreviousQuestions_SubCategory.DoesNotExist:
            return Response({"error": "QuestionBankPreviousQuestions_SubCategory ID not found", "status": False},
                            status=status.HTTP_400_BAD_REQUEST)
        serializer = QuestionBankPreviousQuestions_SubCategorySerializer(user, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data, status=status.HTTP_206_PARTIAL_CONTENT)

    def delete(self, request, format=None):
        if request.GET.get('id'):
            get_object_or_404(QuestionBankPreviousQuestions_SubCategory, id=request.GET.get('id')).delete()
        else:
            QuestionBankPreviousQuestions_SubCategory.objects.all().delete()
        return Response({"success": "Id related data deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


class QuestionBankPreviousQuestionsView(APIView):

    def get(self, request, format=None):
        response = {}
        userId = request.GET.get('id')
        sub_id = request.GET.get('sub_id')
        if userId:
            qs = QuestionBankPreviousQuestions.objects.filter(id=userId)
        elif sub_id:
            qs = QuestionBankPreviousQuestions.objects.filter(sub_category_id=sub_id)
        else:
            qs = QuestionBankPreviousQuestions.objects.all()

        for data in qs:
            print(data)
            response[data.id] = {
                "id": data.id,
                "sub_category_id": data.sub_category.id,
                "sub_category_name": data.sub_category.name,
                "title": data.title,
                "pdf": data.pdf.url if data.pdf else "no pdf"
            }
        return Response(response.values(), status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        try:
            serializer = QuestionBankPreviousQuestions_Serializer(data=data)
            if serializer.is_valid():
                serializer.save()
            return Response({"Status": True,
                             "Message": "Successfully Registered QuestionBankPreviousQuestions"},
                            status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"Errors": "Some field miss check and enter", "exception": str(e), "status": False},
                            status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        userId = request.GET.get('id')
        data = request.data
        try:
            user = QuestionBankPreviousQuestions.objects.get(id=userId)
        except QuestionBankPreviousQuestions.DoesNotExist:
            return Response({"error": "Question Bank Previous Questions ID not found", "status": False},
                            status=status.HTTP_400_BAD_REQUEST)
        serializer = QuestionBankPreviousQuestions_Serializer(user, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data, status=status.HTTP_206_PARTIAL_CONTENT)

    def delete(self, request, format=None):
        if request.GET.get('id'):
            get_object_or_404(QuestionBankPreviousQuestions, id=request.GET.get('id')).delete()
        else:
            QuestionBankPreviousQuestions.objects.all().delete()
        return Response({"success": "Id related data deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


class QuestionDiscussionView(APIView):

    def get(self, request, format=None):
        response = {}
        userId = request.GET.get('id')
        if userId:
            qs = QuestionDiscussion.objects.filter(id=userId)
        else:
            qs = QuestionDiscussion.objects.all()

        for data in qs:
            print(data)
            response[data.id] = {
                "id": data.id,
                "title": data.title,
                "video": data.video.url,
            }
        return Response(response.values(), status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        try:
            serializer = QuestionDiscussion_Serializer(data=data)
            if serializer.is_valid():
                serializer.save()
            return Response({"Status": True,
                             "Message": "Successfully Registered QuestionDiscussion"},
                            status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"Errors": "Some field miss check and enter", "exception": str(e), "status": False},
                            status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        userId = request.GET.get('id')
        data = request.data
        try:
            user = QuestionDiscussion.objects.get(id=userId)
        except QuestionDiscussion.DoesNotExist:
            return Response({"error": "Question Discussion ID not found", "status": False},
                            status=status.HTTP_400_BAD_REQUEST)
        serializer = QuestionDiscussion_Serializer(user, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data, status=status.HTTP_206_PARTIAL_CONTENT)

    def delete(self, request):
        if request.GET.get('id'):
            get_object_or_404(QuestionDiscussion, id=request.GET.get('id')).delete()
        else:
            QuestionDiscussion.objects.all().delete()
        return Response({"success": "Id related data deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


class ShotsbookMarkView(APIView):

    def get(self, request, format=None):
        response = {}
        userId = request.GET.get('id')
        if userId:
            qs = ShotsbookMark.objects.filter(id=userId)
        else:
            qs = ShotsbookMark.objects.all()

        for data in qs:
            print(data)
            response[data.id] = {
                "id": data.id,
                "shots_title": data.shots.title,
                "Shots_id": data.shots.id,
                "user_id": data.user.id,
                "boookmark_status": data.bookmark_status
            }
        return Response(response.values(), status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        try:
            serializer = ShotsbookMark_Serializer(data=data)
            if serializer.is_valid():
                serializer.save()
            return Response({"Status": True,
                             "Message": "Successfully Registered ShotsbookMark"},
                            status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"Errors": "Some field miss check and enter", "exception": str(e), "status": False},
                            status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        userId = request.GET.get('id')
        data = request.data
        try:
            user = ShotsbookMark.objects.get(id=userId)
        except ShotsbookMark.DoesNotExist:
            return Response({"error": "ShotsbookMark ID not found", "status": False},
                            status=status.HTTP_400_BAD_REQUEST)
        serializer = ShotsbookMark_Serializer(user, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data, status=status.HTTP_206_PARTIAL_CONTENT)

    def delete(self, request):
        if request.GET.get('id'):
            get_object_or_404(ShotsbookMark, id=request.GET.get('id')).delete()
        else:
            get_object_or_404(ShotsbookMark, id=request.data.get('id')).delete()
        return Response({"success": "Id related data deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


class ShotsLikedView(APIView):

    def get(self, request, format=None):
        response = {}
        userId = request.GET.get('id')
        if userId:
            qs = ShotsLiked.objects.filter(id=userId)
        else:
            qs = ShotsLiked.objects.all()

        for data in qs:
            print(data)
            response[data.id] = {
                "id": data.id,
                "shots_title": data.shots.title,
                "Shots_id": data.shots.id,
                "user_id": data.user.id,
                "liked_status": data.liked_status
            }
        return Response(response.values(), status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        try:
            serializer = ShotsLiked_Serializer(data=data)
            if serializer.is_valid():
                serializer.save()
            return Response({"Status": True,
                             "Message": "Successfully Registered ShotsLiked"},
                            status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"Errors": "Some field miss check and enter", "exception": str(e), "status": False},
                            status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        userId = request.GET.get('id')
        data = request.data
        try:
            user = ShotsLiked.objects.get(id=userId)
        except ShotsLiked.DoesNotExist:
            return Response({"error": "ShotsLiked ID not found", "status": False},
                            status=status.HTTP_400_BAD_REQUEST)
        serializer = ShotsLiked_Serializer(user, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data, status=status.HTTP_206_PARTIAL_CONTENT)

    def delete(self, request):
        if request.GET.get('id'):
            get_object_or_404(ShotsLiked, id=request.GET.get('id')).delete()
        else:
            get_object_or_404(ShotsLiked, id=request.data.get('id')).delete()
        return Response({"success": "Id related data deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


class Diff_DigbookMarkView(APIView):

    def get(self, request, format=None):
        response = {}
        userId = request.GET.get('id')
        if userId:
            qs = Diff_DigbookMark.objects.filter(id=userId)
        else:
            qs = Diff_DigbookMark.objects.all()

        for data in qs:
            print(data)
            response[data.id] = {
                "id": data.id,
                "Diff_Dig_title": data.Diff_Dig.title,
                "Diff_Dig_id": data.Diff_Dig.id,
                "user_id": data.user.id,
                "boookmark_status": data.bookmark_status
            }
        return Response(response.values(), status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        try:
            serializer = Diff_DigbookMark_Serializer(data=data)
            if serializer.is_valid():
                serializer.save()
            return Response({"Status": True,
                             "Message": "Successfully Registered Diff_DigbookMark"},
                            status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"Errors": "Some field miss check and enter", "exception": str(e), "status": False},
                            status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        userId = request.GET.get('id')
        data = request.data
        try:
            user = Diff_DigbookMark.objects.get(id=userId)
        except Diff_DigbookMark.DoesNotExist:
            return Response({"error": "Diff_DigbookMark ID not found", "status": False},
                            status=status.HTTP_400_BAD_REQUEST)
        serializer = Diff_DigbookMark_Serializer(user, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data, status=status.HTTP_206_PARTIAL_CONTENT)

    def delete(self, request):
        if request.GET.get('id'):
            get_object_or_404(Diff_DigbookMark, id=request.GET.get('id')).delete()
        else:
            get_object_or_404(Diff_DigbookMark, id=request.data.get('id')).delete()
        return Response({"success": "Id related data deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


class Diff_DigLikedView(APIView):

    def get(self, request, format=None):
        response = {}
        userId = request.GET.get('id')
        if userId:
            qs = Diff_DigLiked.objects.filter(id=userId)
        else:
            qs = Diff_DigLiked.objects.all()

        for data in qs:
            print(data)
            response[data.id] = {
                "id": data.id,
                "Diff_Dig_title": data.Diff_Dig.title,
                "Diff_Dig_id": data.Diff_Dig.id,
                "user_id": data.user.id,
                "liked_status": data.liked_status
            }
        return Response(response.values(), status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        try:
            serializer = Diff_DigLiked_Serializer(data=data)
            if serializer.is_valid():
                serializer.save()
            return Response({"Status": True,
                             "Message": "Successfully Registered Diff_DigLiked"},
                            status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"Errors": "Some field miss check and enter", "exception": str(e), "status": False},
                            status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        userId = request.GET.get('id')
        data = request.data
        try:
            user = Diff_DigLiked.objects.get(id=userId)
        except Diff_DigLiked.DoesNotExist:
            return Response({"error": "Diff_DigLiked ID not found", "status": False},
                            status=status.HTTP_400_BAD_REQUEST)
        serializer = Diff_DigLiked_Serializer(user, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data, status=status.HTTP_206_PARTIAL_CONTENT)

    def delete(self, request):
        if request.GET.get('id'):
            get_object_or_404(Diff_DigLiked, id=request.GET.get('id')).delete()
        else:
            get_object_or_404(Diff_DigLiked, id=request.data.get('id')).delete()
        return Response({"success": "Id related data deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


class Recent_UpdatesbookMarkView(APIView):

    def get(self, request, format=None):
        response = {}
        userId = request.GET.get('id')
        if userId:
            qs = Recent_UpdatesbookMark.objects.filter(id=userId)
        else:
            qs = Recent_UpdatesbookMark.objects.all()

        for data in qs:
            print(data)
            response[data.id] = {
                "id": data.id,
                "Recent_Updates_title": data.Recent_Updates.title,
                "Recent_Updates_id": data.Recent_Updates.id,
                "user_id": data.user.id,
                "boookmark_status": data.bookmark_status
            }
        return Response(response.values(), status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        try:
            serializer = Recent_UpdatesbookMark_Serializer(data=data)
            if serializer.is_valid():
                serializer.save()
            return Response({"Status": True,
                             "Message": "Successfully Registered Recent_UpdatesbookMark"},
                            status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"Errors": "Some field miss check and enter", "exception": str(e), "status": False},
                            status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        userId = request.GET.get('id')
        data = request.data
        try:
            user = Recent_UpdatesbookMark.objects.get(id=userId)
        except Recent_UpdatesbookMark.DoesNotExist:
            return Response({"error": "Recent_UpdatesbookMark ID not found", "status": False},
                            status=status.HTTP_400_BAD_REQUEST)
        serializer = Recent_UpdatesbookMark_Serializer(user, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data, status=status.HTTP_206_PARTIAL_CONTENT)

    def delete(self, request):
        if request.GET.get('id'):
            get_object_or_404(Recent_UpdatesbookMark, id=request.GET.get('id')).delete()
        else:
            get_object_or_404(Recent_UpdatesbookMark, id=request.data.get('id')).delete()
        return Response({"success": "Id related data deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


class Recent_UpdatesLikedView(APIView):

    def get(self, request, format=None):
        response = {}
        userId = request.GET.get('id')
        if userId:
            qs = Recent_UpdatesLiked.objects.filter(id=userId)
        else:
            qs = Recent_UpdatesLiked.objects.all()

        for data in qs:
            print(data)
            response[data.id] = {
                "id": data.id,
                "Recent_Updates_title": data.Recent_Updates.title,
                "Recent_Updates_id": data.Recent_Updates.id,
                "user_id": data.user.id,
                "liked_status": data.liked_status
            }
        return Response(response.values(), status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        try:
            serializer = Recent_UpdatesLiked_Serializer(data=data)
            if serializer.is_valid():
                serializer.save()
            return Response({"Status": True,
                             "Message": "Successfully Registered Recent_UpdatesLiked"},
                            status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"Errors": "Some field miss check and enter", "exception": str(e), "status": False},
                            status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        userId = request.GET.get('id')
        data = request.data
        try:
            user = Recent_UpdatesLiked.objects.get(id=userId)
        except Recent_UpdatesLiked.DoesNotExist:
            return Response({"error": "Recent_UpdatesLiked ID not found", "status": False},
                            status=status.HTTP_400_BAD_REQUEST)
        serializer = Recent_UpdatesLiked_Serializer(user, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data, status=status.HTTP_206_PARTIAL_CONTENT)

    def delete(self, request):
        if request.GET.get('id'):
            get_object_or_404(Recent_UpdatesLiked, id=request.GET.get('id')).delete()
        else:
            get_object_or_404(Recent_UpdatesLiked, id=request.data.get('id')).delete()
        return Response({"success": "Id related data deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


class ValuesbookMarkView(APIView):

    def get(self, request, format=None):
        response = {}
        userId = request.GET.get('id')
        if userId:
            qs = ValuesbookMark.objects.filter(id=userId)
        else:
            qs = ValuesbookMark.objects.all()

        for data in qs:
            print(data)
            response[data.id] = {
                "id": data.id,
                "Values_title": data.Values.title,
                "Values_id": data.Values.id,
                "user_id": data.user.id,
                "boookmark_status": data.bookmark_status
            }
        return Response(response.values(), status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        try:
            serializer = ValuesbookMark_Serializer(data=data)
            if serializer.is_valid():
                serializer.save()
            return Response({"Status": True,
                             "Message": "Successfully Registered ValuesbookMark"},
                            status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"Errors": "Some field miss check and enter", "exception": str(e), "status": False},
                            status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        userId = request.GET.get('id')
        data = request.data
        try:
            user = ValuesbookMark.objects.get(id=userId)
        except ValuesbookMark.DoesNotExist:
            return Response({"error": "ValuesbookMark ID not found", "status": False},
                            status=status.HTTP_400_BAD_REQUEST)
        serializer = ValuesbookMark_Serializer(user, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data, status=status.HTTP_206_PARTIAL_CONTENT)

    def delete(self, request):
        if request.GET.get('id'):
            get_object_or_404(ValuesbookMark, id=request.GET.get('id')).delete()
        else:
            get_object_or_404(ValuesbookMark, id=request.data.get('id')).delete()
        return Response({"success": "Id related data deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


class ValuesLikedView(APIView):

    def get(self, request, format=None):
        response = {}
        userId = request.GET.get('id')
        if userId:
            qs = ValuesLiked.objects.filter(id=userId)
        else:
            qs = ValuesLiked.objects.all()

        for data in qs:
            print(data)
            response[data.id] = {
                "id": data.id,
                "Values_title": data.Values.title,
                "Values_id": data.Values.id,
                "user_id": data.user.id,
                "liked_status": data.liked_status
            }
        return Response(response.values(), status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        try:
            serializer = ValuesLiked_Serializer(data=data)
            if serializer.is_valid():
                serializer.save()
            return Response({"Status": True,
                             "Message": "Successfully Registered ValuesLiked"},
                            status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"Errors": "Some field miss check and enter", "exception": str(e), "status": False},
                            status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        userId = request.GET.get('id')
        data = request.data
        try:
            user = ValuesLiked.objects.get(id=userId)
        except ValuesLiked.DoesNotExist:
            return Response({"error": "ValuesLiked ID not found", "status": False},
                            status=status.HTTP_400_BAD_REQUEST)
        serializer = ValuesLiked_Serializer(user, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data, status=status.HTTP_206_PARTIAL_CONTENT)

    def delete(self, request):
        if request.GET.get('id'):
            get_object_or_404(ValuesLiked, id=request.GET.get('id')).delete()
        else:
            get_object_or_404(ValuesLiked, id=request.data.get('id')).delete()
        return Response({"success": "Id related data deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


class ICardsPDFbookMarkView(APIView):

    def get(self, request, format=None):
        response = {}
        userId = request.GET.get('id')
        if userId:
            qs = ICardsPDFbookMark.objects.filter(id=userId)
        else:
            qs = ICardsPDFbookMark.objects.all()

        for data in qs:
            print(data)
            response[data.id] = {
                "id": data.id,
                "ICardsPDF_title": data.ICardsPDF.title,
                "ICardsPDF_id": data.ICardsPDF.id,
                "user_id": data.user.id,
                "boookmark_status": data.bookmark_status
            }
        return Response(response.values(), status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        try:
            serializer = ICardsPDFbookMark_Serializer(data=data)
            if serializer.is_valid():
                serializer.save()
            return Response({"Status": True,
                             "Message": "Successfully Registered ICardsPDFbookMark"},
                            status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"Errors": "Some field miss check and enter", "exception": str(e), "status": False},
                            status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        userId = request.GET.get('id')
        data = request.data
        try:
            user = ICardsPDFbookMark.objects.get(id=userId)
        except ICardsPDFbookMark.DoesNotExist:
            return Response({"error": "ICardsPDFbookMark ID not found", "status": False},
                            status=status.HTTP_400_BAD_REQUEST)
        serializer = ICardsPDFbookMark_Serializer(user, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data, status=status.HTTP_206_PARTIAL_CONTENT)

    def delete(self, request):
        if request.GET.get('id'):
            get_object_or_404(ICardsPDFbookMark, id=request.GET.get('id')).delete()
        else:
            get_object_or_404(ICardsPDFbookMark, id=request.data.get('id')).delete()
        return Response({"success": "Id related data deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


class ICardsPDFLikedView(APIView):

    def get(self, request, format=None):
        response = {}
        userId = request.GET.get('id')
        if userId:
            qs = ICardsPDFLiked.objects.filter(id=userId)
        else:
            qs = ICardsPDFLiked.objects.all()

        for data in qs:
            print(data)
            response[data.id] = {
                "id": data.id,
                "ICardsPDF_title": data.ICardsPDF.title,
                "ICardsPDF_id": data.ICardsPDF.id,
                "user_id": data.user.id,
                "liked_status": data.liked_status
            }
        return Response(response.values(), status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        try:
            serializer = ICardsPDFLiked_Serializer(data=data)
            if serializer.is_valid():
                serializer.save()
            return Response({"Status": True,
                             "Message": "Successfully Registered ICardsPDFLiked"},
                            status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"Errors": "Some field miss check and enter", "exception": str(e), "status": False},
                            status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        userId = request.GET.get('id')
        data = request.data
        try:
            user = ICardsPDFLiked.objects.get(id=userId)
        except ICardsPDFLiked.DoesNotExist:
            return Response({"error": "ICardsPDFLiked ID not found", "status": False},
                            status=status.HTTP_400_BAD_REQUEST)
        serializer = ICardsPDFLiked_Serializer(user, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data, status=status.HTTP_206_PARTIAL_CONTENT)

    def delete(self, request):
        if request.GET.get('id'):
            get_object_or_404(ICardsPDFLiked, id=request.GET.get('id')).delete()
        else:
            get_object_or_404(ICardsPDFLiked, id=request.data.get('id')).delete()
        return Response({"success": "Id related data deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


class ICardsAudiobookMarkView(APIView):

    def get(self, request, format=None):
        response = {}
        userId = request.GET.get('id')
        if userId:
            qs = ICardsAudiobookMark.objects.filter(id=userId)
        else:
            qs = ICardsAudiobookMark.objects.all()

        for data in qs:
            print(data)
            response[data.id] = {
                "id": data.id,
                "ICardsAudio_title": data.ICardsAudio.title,
                "ICardsAudio_id": data.ICardsAudio.id,
                "user_id": data.user.id,
                "boookmark_status": data.bookmark_status
            }
        return Response(response.values(), status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        try:
            serializer = ICardsAudiobookMark_Serializer(data=data)
            if serializer.is_valid():
                serializer.save()
            return Response({"Status": True,
                             "Message": "Successfully Registered ICardsAudiobookMark"},
                            status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"Errors": "Some field miss check and enter", "exception": str(e), "status": False},
                            status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        userId = request.GET.get('id')
        data = request.data
        try:
            user = ICardsAudiobookMark.objects.get(id=userId)
        except ICardsAudiobookMark.DoesNotExist:
            return Response({"error": "ICardsAudiobookMark ID not found", "status": False},
                            status=status.HTTP_400_BAD_REQUEST)
        serializer = ICardsAudiobookMark_Serializer(user, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data, status=status.HTTP_206_PARTIAL_CONTENT)

    def delete(self, request):
        if request.GET.get('id'):
            get_object_or_404(ICardsAudiobookMark, id=request.GET.get('id')).delete()
        else:
            get_object_or_404(ICardsAudiobookMark, id=request.data.get('id')).delete()
        return Response({"success": "Id related data deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


class ICardsAudioLikedView(APIView):

    def get(self, request, format=None):
        response = {}
        userId = request.GET.get('id')
        if userId:
            qs = ICardsAudioLiked.objects.filter(id=userId)
        else:
            qs = ICardsAudioLiked.objects.all()

        for data in qs:
            print(data)
            response[data.id] = {
                "id": data.id,
                "ICardsAudio_title": data.ICardsAudio.title,
                "ICardsAudio_id": data.ICardsAudio.id,
                "user_id": data.user.id,
                "liked_status": data.liked_status
            }
        return Response(response.values(), status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        try:
            serializer = ICardsAudioLiked_Serializer(data=data)
            if serializer.is_valid():
                serializer.save()
            return Response({"Status": True,
                             "Message": "Successfully Registered ICardsAudioLiked"},
                            status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"Errors": "Some field miss check and enter", "exception": str(e), "status": False},
                            status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        userId = request.GET.get('id')
        data = request.data
        try:
            user = ICardsAudioLiked.objects.get(id=userId)
        except ICardsAudioLiked.DoesNotExist:
            return Response({"error": "ICardsAudioLiked ID not found", "status": False},
                            status=status.HTTP_400_BAD_REQUEST)
        serializer = ICardsAudioLiked_Serializer(user, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data, status=status.HTTP_206_PARTIAL_CONTENT)

    def delete(self, request):
        if request.GET.get('id'):
            get_object_or_404(ICardsAudioLiked, id=request.GET.get('id')).delete()
        else:
            get_object_or_404(ICardsAudioLiked, id=request.data.get('id')).delete()
        return Response({"success": "Id related data deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


class ICardsVideobookMarkView(APIView):

    def get(self, request, format=None):
        response = {}
        userId = request.GET.get('id')
        if userId:
            qs = ICardsVideobookMark.objects.filter(id=userId)
        else:
            qs = ICardsVideobookMark.objects.all()

        for data in qs:
            print(data)
            response[data.id] = {
                "id": data.id,
                "ICardsVideo_title": data.ICardsVideo.title,
                "ICardsVideo_id": data.ICardsVideo.id,
                "user_id": data.user.id,
                "boookmark_status": data.bookmark_status
            }
        return Response(response.values(), status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        try:
            serializer = ICardsVideobookMark_Serializer(data=data)
            if serializer.is_valid():
                serializer.save()
            return Response({"Status": True,
                             "Message": "Successfully Registered ICardsVideobookMark"},
                            status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"Errors": "Some field miss check and enter", "exception": str(e), "status": False},
                            status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        userId = request.GET.get('id')
        data = request.data
        try:
            user = ICardsVideobookMark.objects.get(id=userId)
        except ICardsVideobookMark.DoesNotExist:
            return Response({"error": "ICardsVideobookMark ID not found", "status": False},
                            status=status.HTTP_400_BAD_REQUEST)
        serializer = ICardsVideobookMark_Serializer(user, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data, status=status.HTTP_206_PARTIAL_CONTENT)

    def delete(self, request):
        if request.GET.get('id'):
            get_object_or_404(ICardsVideobookMark, id=request.GET.get('id')).delete()
        else:
            get_object_or_404(ICardsVideobookMark, id=request.data.get('id')).delete()
        return Response({"success": "Id related data deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


class ICardsVideoLikedView(APIView):

    def get(self, request, format=None):
        response = {}
        userId = request.GET.get('id')
        if userId:
            qs = ICardsVideoLiked.objects.filter(id=userId)
        else:
            qs = ICardsVideoLiked.objects.all()

        for data in qs:
            print(data)
            response[data.id] = {
                "id": data.id,
                "ICardsVideo_title": data.ICardsVideo.title,
                "ICardsVideo_id": data.ICardsVideo.id,
                "user_id": data.user.id,
                "liked_status": data.liked_status
            }
        return Response(response.values(), status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        try:
            serializer = ICardsVideoLiked_Serializer(data=data)
            if serializer.is_valid():
                serializer.save()
            return Response({"Status": True,
                             "Message": "Successfully Registered ICardsVideoLiked"},
                            status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"Errors": "Some field miss check and enter", "exception": str(e), "status": False},
                            status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        userId = request.GET.get('id')
        data = request.data
        try:
            user = ICardsVideoLiked.objects.get(id=userId)
        except ICardsVideoLiked.DoesNotExist:
            return Response({"error": "ICardsVideoLiked ID not found", "status": False},
                            status=status.HTTP_400_BAD_REQUEST)
        serializer = ICardsVideoLiked_Serializer(user, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data, status=status.HTTP_206_PARTIAL_CONTENT)

    def delete(self, request):
        if request.GET.get('id'):
            get_object_or_404(ICardsVideoLiked, id=request.GET.get('id')).delete()
        else:
            get_object_or_404(ICardsVideoLiked, id=request.data.get('id')).delete()
        return Response({"success": "Id related data deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


class ImageBankbookMarkView(APIView):

    def get(self, request, format=None):
        response = {}
        userId = request.GET.get('id')
        if userId:
            qs = ImageBankbookMark.objects.filter(id=userId)
        else:
            qs = ImageBankbookMark.objects.all()

        for data in qs:
            print(data)
            response[data.id] = {
                "id": data.id,
                "ImageBank_title": data.ImageBank.title,
                "ImageBank_id": data.ImageBank.id,
                "user_id": data.user.id,
                "boookmark_status": data.bookmark_status
            }
        return Response(response.values(), status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        try:
            serializer = ImageBankbookMark_Serializer(data=data)
            if serializer.is_valid():
                serializer.save()
            return Response({"Status": True,
                             "Message": "Successfully Registered ImageBankbookMark"},
                            status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"Errors": "Some field miss check and enter", "exception": str(e), "status": False},
                            status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        userId = request.GET.get('id')
        data = request.data
        try:
            user = ImageBankbookMark.objects.get(id=userId)
        except ImageBankbookMark.DoesNotExist:
            return Response({"error": "ImageBankbookMark ID not found", "status": False},
                            status=status.HTTP_400_BAD_REQUEST)
        serializer = ImageBankbookMark_Serializer(user, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data, status=status.HTTP_206_PARTIAL_CONTENT)

    def delete(self, request):
        if request.GET.get('id'):
            get_object_or_404(ImageBankbookMark, id=request.GET.get('id')).delete()
        else:
            get_object_or_404(ImageBankbookMark, id=request.data.get('id')).delete()
        return Response({"success": "Id related data deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


class ImageBankLikedView(APIView):

    def get(self, request, format=None):
        response = {}
        userId = request.GET.get('id')
        if userId:
            qs = ImageBankLiked.objects.filter(id=userId)
        else:
            qs = ImageBankLiked.objects.all()

        for data in qs:
            print(data)
            response[data.id] = {
                "id": data.id,
                "ImageBank_title": data.ImageBank.title,
                "ImageBank_id": data.ImageBank.id,
                "user_id": data.user.id,
                "liked_status": data.liked_status
            }
        return Response(response.values(), status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        try:
            serializer = ImageBankLiked_Serializer(data=data)
            if serializer.is_valid():
                serializer.save()
            return Response({"Status": True,
                             "Message": "Successfully Registered ImageBankLiked"},
                            status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"Errors": "Some field miss check and enter", "exception": str(e), "status": False},
                            status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        userId = request.GET.get('id')
        data = request.data
        try:
            user = ImageBankLiked.objects.get(id=userId)
        except ImageBankLiked.DoesNotExist:
            return Response({"error": "ImageBankLiked ID not found", "status": False},
                            status=status.HTTP_400_BAD_REQUEST)
        serializer = ImageBankLiked_Serializer(user, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data, status=status.HTTP_206_PARTIAL_CONTENT)

    def delete(self, request):
        if request.GET.get('id'):
            get_object_or_404(ImageBankLiked, id=request.GET.get('id')).delete()
        else:
            get_object_or_404(ImageBankLiked, id=request.data.get('id')).delete()
        return Response({"success": "Id related data deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


class WallPostersbookMarkView(APIView):

    def get(self, request, format=None):
        response = {}
        userId = request.GET.get('id')
        if userId:
            qs = WallPostersbookMark.objects.filter(id=userId)
        else:
            qs = WallPostersbookMark.objects.all()

        for data in qs:
            print(data)
            response[data.id] = {
                "id": data.id,
                "WallPosters_title": data.WallPosters.title,
                "WallPosters_id": data.WallPosters.id,
                "user_id": data.user.id,
                "boookmark_status": data.bookmark_status
            }
        return Response(response.values(), status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        try:
            serializer = WallPostersbookMark_Serializer(data=data)
            if serializer.is_valid():
                serializer.save()
            return Response({"Status": True,
                             "Message": "Successfully Registered WallPostersbookMark"},
                            status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"Errors": "Some field miss check and enter", "exception": str(e), "status": False},
                            status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        userId = request.GET.get('id')
        data = request.data
        try:
            user = WallPostersbookMark.objects.get(id=userId)
        except WallPostersbookMark.DoesNotExist:
            return Response({"error": "WallPostersbookMark ID not found", "status": False},
                            status=status.HTTP_400_BAD_REQUEST)
        serializer = WallPostersbookMark_Serializer(user, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data, status=status.HTTP_206_PARTIAL_CONTENT)

    def delete(self, request):
        if request.GET.get('id'):
            get_object_or_404(WallPostersbookMark, id=request.GET.get('id')).delete()
        else:
            get_object_or_404(WallPostersbookMark, id=request.data.get('id')).delete()
        return Response({"success": "Id related data deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


class WallPostersLikedView(APIView):

    def get(self, request, format=None):
        response = {}
        userId = request.GET.get('id')
        if userId:
            qs = WallPostersLiked.objects.filter(id=userId)
        else:
            qs = WallPostersLiked.objects.all()

        for data in qs:
            print(data)
            response[data.id] = {
                "id": data.id,
                "WallPosters_title": data.WallPosters.title,
                "WallPosters_id": data.WallPosters.id,
                "user_id": data.user.id,
                "liked_status": data.liked_status
            }
        return Response(response.values(), status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        try:
            serializer = WallPostersLiked_Serializer(data=data)
            if serializer.is_valid():
                serializer.save()
            return Response({"Status": True,
                             "Message": "Successfully Registered WallPostersLiked"},
                            status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"Errors": "Some field miss check and enter", "exception": str(e), "status": False},
                            status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        userId = request.GET.get('id')
        data = request.data
        try:
            user = WallPostersLiked.objects.get(id=userId)
        except WallPostersLiked.DoesNotExist:
            return Response({"error": "WallPostersLiked ID not found", "status": False},
                            status=status.HTTP_400_BAD_REQUEST)
        serializer = WallPostersLiked_Serializer(user, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data, status=status.HTTP_206_PARTIAL_CONTENT)

    def delete(self, request):
        if request.GET.get('id'):
            get_object_or_404(WallPostersLiked, id=request.GET.get('id')).delete()
        else:
            get_object_or_404(WallPostersLiked, id=request.data.get('id')).delete()
        return Response({"success": "Id related data deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


class PrimeClassVideobookMarkView(APIView):

    def get(self, request, format=None):
        response = {}
        userId = request.GET.get('id')
        if userId:
            qs = PrimeClassVideobookMark.objects.filter(id=userId)
        else:
            qs = PrimeClassVideobookMark.objects.all()

        for data in qs:
            print(data)
            response[data.id] = {
                "id": data.id,
                "PrimeClassVideo_title": data.PrimeClassVideo.title,
                "PrimeClassVideo_id": data.PrimeClassVideo.id,
                "user_id": data.user.id,
                "boookmark_status": data.bookmark_status
            }
        return Response(response.values(), status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        try:
            serializer = PrimeClassVideobookMark_Serializer(data=data)
            if serializer.is_valid():
                serializer.save()
            return Response({"Status": True,
                             "Message": "Successfully Registered PrimeClassVideobookMark"},
                            status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"Errors": "Some field miss check and enter", "exception": str(e), "status": False},
                            status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        userId = request.GET.get('id')
        data = request.data
        try:
            user = PrimeClassVideobookMark.objects.get(id=userId)
        except PrimeClassVideobookMark.DoesNotExist:
            return Response({"error": "PrimeClassVideobookMark ID not found", "status": False},
                            status=status.HTTP_400_BAD_REQUEST)
        serializer = PrimeClassVideobookMark_Serializer(user, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data, status=status.HTTP_206_PARTIAL_CONTENT)

    def delete(self, request):
        if request.GET.get('id'):
            get_object_or_404(PrimeClassVideobookMark, id=request.GET.get('id')).delete()
        else:
            get_object_or_404(PrimeClassVideobookMark, id=request.data.get('id')).delete()
        return Response({"success": "Id related data deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


class PrimeClassAudiobookMarkView(APIView):

    def get(self, request, format=None):
        response = {}
        userId = request.GET.get('id')
        if userId:
            qs = PrimeClassAudiobookMark.objects.filter(id=userId)
        else:
            qs = PrimeClassAudiobookMark.objects.all()

        for data in qs:
            print(data)
            response[data.id] = {
                "id": data.id,
                "PrimeClassAudio_title": data.PrimeClassAudio.title,
                "PrimeClassAudio_id": data.PrimeClassAudio.id,
                "user_id": data.user.id,
                "boookmark_status": data.bookmark_status
            }
        return Response(response.values(), status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        try:
            serializer = PrimeClassAudiobookMark_Serializer(data=data)
            if serializer.is_valid():
                serializer.save()
            return Response({"Status": True,
                             "Message": "Successfully Registered PrimeClassAudiobookMark"},
                            status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"Errors": "Some field miss check and enter", "exception": str(e), "status": False},
                            status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        userId = request.GET.get('id')
        data = request.data
        try:
            user = PrimeClassAudiobookMark.objects.get(id=userId)
        except PrimeClassAudiobookMark.DoesNotExist:
            return Response({"error": "PrimeClassAudiobookMark ID not found", "status": False},
                            status=status.HTTP_400_BAD_REQUEST)
        serializer = PrimeClassAudiobookMark_Serializer(user, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data, status=status.HTTP_206_PARTIAL_CONTENT)

    def delete(self, request):
        if request.GET.get('id'):
            get_object_or_404(PrimeClassAudiobookMark, id=request.GET.get('id')).delete()
        else:
            get_object_or_404(PrimeClassAudiobookMark, id=request.data.get('id')).delete()
        return Response({"success": "Id related data deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


class PrimeClassNotesbookMarkView(APIView):

    def get(self, request, format=None):
        response = {}
        userId = request.GET.get('id')
        if userId:
            qs = PrimeClassNotesbookMark.objects.filter(id=userId)
        else:
            qs = PrimeClassNotesbookMark.objects.all()

        for data in qs:
            print(data)
            response[data.id] = {
                "id": data.id,
                "PrimeClassNotes_title": data.PrimeClassNotes.title,
                "PrimeClassNotes_id": data.PrimeClassNotes.id,
                "user_id": data.user.id,
                "boookmark_status": data.bookmark_status
            }
        return Response(response.values(), status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        try:
            serializer = PrimeClassNotesbookMark_Serializer(data=data)
            if serializer.is_valid():
                serializer.save()
            return Response({"Status": True,
                             "Message": "Successfully Registered PrimeClassNotesbookMark"},
                            status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"Errors": "Some field miss check and enter", "exception": str(e), "status": False},
                            status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        userId = request.GET.get('id')
        data = request.data
        try:
            user = PrimeClassNotesbookMark.objects.get(id=userId)
        except PrimeClassNotesbookMark.DoesNotExist:
            return Response({"error": "PrimeClassNotesbookMark ID not found", "status": False},
                            status=status.HTTP_400_BAD_REQUEST)
        serializer = PrimeClassNotesbookMark_Serializer(user, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data, status=status.HTTP_206_PARTIAL_CONTENT)

    def delete(self, request):
        if request.GET.get('id'):
            get_object_or_404(PrimeClassNotesbookMark, id=request.GET.get('id')).delete()
        else:
            get_object_or_404(PrimeClassNotesbookMark, id=request.data.get('id')).delete()
        return Response({"success": "Id related data deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


class LiveClassbookMarkView(APIView):

    def get(self, request, format=None):
        response = {}
        userId = request.GET.get('id')
        sub_id = request.GET.get('sub_id')
        if userId:
            qs = LiveClassbookMark.objects.filter(id=userId)
        elif sub_id:
            qs = LiveClassbookMark.objects.filter(liveClass__sub_category__category_id=sub_id)
        else:
            qs = LiveClassbookMark.objects.all()

        for data in qs:
            print(data)
            response[data.id] = {
                "id": data.id,
                "LiveClass_sub_category_id": data.liveClass.sub_category.id,
                "LiveClass_title": data.liveClass.title,
                "LiveClass_id": data.liveClass.id,
                "user_id": data.user.id,
                "boookmark_status": data.bookmark_status
            }
        return Response(response.values(), status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        try:
            serializer = LiveClassbookMark_Serializer(data=data)
            if serializer.is_valid():
                serializer.save()
            return Response({"Status": True,
                             "Message": "Successfully Registered LiveClassbookMark"},
                            status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"Errors": "Some field miss check and enter", "exception": str(e), "status": False},
                            status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        userId = request.GET.get('id')
        data = request.data
        try:
            user = LiveClassbookMark.objects.get(id=userId)
        except LiveClassbookMark.DoesNotExist:
            return Response({"error": "LiveClassbookMark ID not found", "status": False},
                            status=status.HTTP_400_BAD_REQUEST)
        serializer = LiveClassbookMark_Serializer(user, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data, status=status.HTTP_206_PARTIAL_CONTENT)

    def delete(self, request):
        if request.GET.get('id'):
            get_object_or_404(LiveClassbookMark, id=request.GET.get('id')).delete()
        else:
            get_object_or_404(LiveClassbookMark, id=request.data.get('id')).delete()
        return Response({"success": "Id related data deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


class QuestionDiscussionbookMarkView(APIView):

    def get(self, request, format=None):
        response = {}
        userId = request.GET.get('id')
        if userId:
            qs = QuestionDiscussionbookMark.objects.filter(id=userId)
        else:
            qs = QuestionDiscussionbookMark.objects.all()

        for data in qs:
            print(data)
            response[data.id] = {
                "id": data.id,
                "QuestionDiscussion_title": data.QuestionDiscussion.title,
                "QuestionDiscussion_id": data.QuestionDiscussion.id,
                "user_id": data.user.id,
                "boookmark_status": data.bookmark_status
            }
        return Response(response.values(), status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        try:
            serializer = QuestionDiscussionbookMark_Serializer(data=data)
            if serializer.is_valid():
                serializer.save()
            return Response({"Status": True,
                             "Message": "Successfully Registered QuestionDiscussionbookMark"},
                            status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"Errors": "Some field miss check and enter", "exception": str(e), "status": False},
                            status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        userId = request.GET.get('id')
        data = request.data
        try:
            user = QuestionDiscussionbookMark.objects.get(id=userId)
        except QuestionDiscussionbookMark.DoesNotExist:
            return Response({"error": "QuestionDiscussionbookMark ID not found", "status": False},
                            status=status.HTTP_400_BAD_REQUEST)
        serializer = QuestionDiscussionbookMark_Serializer(user, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data, status=status.HTTP_206_PARTIAL_CONTENT)

    def delete(self, request):
        if request.GET.get('id'):
            get_object_or_404(QuestionDiscussionbookMark, id=request.GET.get('id')).delete()
        else:
            get_object_or_404(QuestionDiscussionbookMark, id=request.data.get('id')).delete()
        return Response({"success": "Id related data deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


class ICardsPastPaper_CategoryView(APIView):

    def get(self, request, format=None):
        userId = request.GET.get('id')
        if userId:
            return Response(
                ICardsPastPaper_CategorySerializer(get_object_or_404(ICardsPastPaper_Category, id=userId),
                                                   many=False).data,
                status=status.HTTP_200_OK)

        serializer = ICardsPastPaper_CategorySerializer(ICardsPastPaper_Category.objects.all(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        try:
            serializer = ICardsPastPaper_CategorySerializer(data=data)
            if serializer.is_valid():
                serializer.save()
            return Response({"Status": True,
                             "Message": "Successfully Registered PastPaper Category"},
                            status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"Errors": "Some field miss check and enter", "exception": str(e), "status": False},
                            status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        userId = request.GET.get('id')
        data = request.data
        try:
            user = ICardsPastPaper_Category.objects.get(id=userId)
        except ICardsPastPaper_Category.DoesNotExist:
            return Response({"error": "Category ID not found", "status": False}, status=status.HTTP_400_BAD_REQUEST)
        serializer = ICardsPastPaper_CategorySerializer(user, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data, status=status.HTTP_206_PARTIAL_CONTENT)

    def delete(self, request, format=None):
        if request.GET.get('id'):
            get_object_or_404(ICardsPastPaper_Category, id=request.GET.get('id')).delete()
        else:
            get_object_or_404(ICardsPastPaper_Category, id=request.data.get('id')).delete()
        return Response({"success": "Id related data deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


class ICardsPastPaper_SubCategoryView(APIView):

    def get(self, request, format=None):
        response = {}
        userId = request.GET.get('id')
        cat_Id = request.GET.get('cat_id')
        if userId:
            qs = ICardsPastPaper_SubCategory.objects.filter(id=userId)
        elif cat_Id:
            subid = get_object_or_404(ICardsPastPaper_Category, id=cat_Id)
            qs = subid.icardspastpaper_subcategory_set.all().order_by('id')
        else:
            qs = ICardsPastPaper_SubCategory.objects.all()

        for data in qs:
            print(data)
            response[data.id] = {
                "id": data.id,
                "category_id": data.category.id,
                "category_name": data.category.name,
                "sub_category_name": data.name
            }
        return Response(response.values(), status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        try:
            serializer = ICardsPastPaper_SubCategorySerializer(data=data)
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
            user = ICardsPastPaper_SubCategory.objects.get(id=userId)
        except ICardsPastPaper_SubCategory.DoesNotExist:
            return Response({"error": "Sub Category ID not found", "status": False}, status=status.HTTP_400_BAD_REQUEST)
        serializer = ICardsPastPaper_SubCategorySerializer(user, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data, status=status.HTTP_206_PARTIAL_CONTENT)

    def delete(self, request, format=None):
        if request.GET.get('id'):
            get_object_or_404(ICardsPastPaper_SubCategory, id=request.GET.get('id')).delete()
        else:
            get_object_or_404(ICardsPastPaper_SubCategory, id=request.data.get('id')).delete()
        return Response({"success": "Id related data deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


class ICardsPastPaperView(APIView):

    def get(self, request, format=None):
        response = {}
        userId = request.GET.get('id')
        sub_id = request.GET.get('sub_id')
        if userId:
            qs = ICardsPastPaper.objects.filter(id=userId)
        elif sub_id:
            subid = get_object_or_404(ICardsPastPaper_SubCategory, id=sub_id)
            qs = subid.icardspastpaper_set.all().order_by('id')
        else:
            qs = ICardsPastPaper.objects.all().order_by('id')

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
            serializer = ICardsPastPaperSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
            return Response({"Status": True,
                             "Message": "Successfully Registered ICARDS pdf"},
                            status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"Errors": "Some field miss check and enter", "exception": str(e), "status": False},
                            status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        userId = request.GET.get('id')
        data = request.data
        try:
            user = ICardsPastPaper.objects.get(id=userId)
        except ICardsPastPaper.DoesNotExist:
            return Response({"error": "Icards video ID not found", "status": False}, status=status.HTTP_400_BAD_REQUEST)
        serializer = ICardsPastPaperSerializer(user, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data, status=status.HTTP_206_PARTIAL_CONTENT)

    def delete(self, request, format=None):
        if request.GET.get('id'):
            get_object_or_404(ICardsPastPaper, id=request.GET.get('id')).delete()
        else:
            get_object_or_404(ICardsPastPaper, id=request.data.get('id')).delete()
        return Response({"success": "Id related data deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


# --------------------17 july 


class Test_CategoryView(APIView):

    def get(self, request, format=None):
        userId = request.GET.get('id')
        if userId:
            return Response(
                Test_CategorySerializer(get_object_or_404(Test_Category, id=userId),
                                                   many=False).data,
                status=status.HTTP_200_OK)

        serializer = Test_CategorySerializer(Test_Category.objects.all(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        try:
            serializer = Test_CategorySerializer(data=data)
            if serializer.is_valid():
                serializer.save()
            return Response({"Status": True,
                             "Message": "Successfully Registered Test Category"},
                            status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"Errors": "Some field miss check and enter", "exception": str(e), "status": False},
                            status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        userId = request.GET.get('id')
        data = request.data
        try:
            user = Test_Category.objects.get(id=userId)
        except Test_Category.DoesNotExist:
            return Response({"error": "Category ID not found", "status": False}, status=status.HTTP_400_BAD_REQUEST)
        serializer = Test_CategorySerializer(user, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data, status=status.HTTP_206_PARTIAL_CONTENT)

    def delete(self, request, format=None):
        if request.GET.get('id'):
            get_object_or_404(Test_Category, id=request.GET.get('id')).delete()
        else:
            get_object_or_404(Test_Category, id=request.data.get('id')).delete()
        return Response({"success": "Id related data deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


class Test_SubCategoryView(APIView):

    def get(self, request, format=None):
        response = {}
        userId = request.GET.get('id')
        cat_Id = request.GET.get('cat_id')
        if userId:
            qs = Test_SubCategory.objects.filter(id=userId)
        elif cat_Id:
            subid = get_object_or_404(Test_Category, id=cat_Id)
            qs = subid.Test_subcategory_set.all().order_by('id')
        else:
            qs = Test_SubCategory.objects.all()

        for data in qs:
            print(data)
            response[data.id] = {
                "id": data.id,
                "category_id": data.category.id,            
                "sub_category_title": data.category.title,            
                "title": data.title,
                "no_of_mcq": data.no_of_mcq,
                "timer": data.timer,
                "result_date": data.result_date
            }
        return Response(response.values(), status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        try:
            serializer = Test_SubCategorySerializer(data=data)
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
            user = Test_SubCategory.objects.get(id=userId)
        except Test_SubCategory.DoesNotExist:
            return Response({"error": "Sub Category ID not found", "status": False}, status=status.HTTP_400_BAD_REQUEST)
        serializer = Test_SubCategorySerializer(user, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data, status=status.HTTP_206_PARTIAL_CONTENT)

    def delete(self, request, format=None):
        if request.GET.get('id'):
            get_object_or_404(Test_SubCategory, id=request.GET.get('id')).delete()
        else:
            get_object_or_404(Test_SubCategory, id=request.data.get('id')).delete()
        return Response({"success": "Id related data deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


class TestQuestionsView(APIView):

    def get(self, request, format=None):
        response = {}
        userId = request.GET.get('id')
        sub_id = request.GET.get('sub_id')
        if userId:
            qs = TestQuestions.objects.filter(id=userId)
        elif sub_id:
            subid = get_object_or_404(Test_SubCategory, id=sub_id)
            qs = subid.TestQuestions_set.all().order_by('id')
        else:
            qs = TestQuestions.objects.all().order_by('id')

        for data in qs:
            response[data.id] = {
                "id": data.id,           
                "test_sub_category_id": data.test_sub_category.id,          
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
            serializer = TestQuestionsSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
            return Response({"Status": True,
                             "Message": "Successfully Registered TestQuestions"},
                            status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"Errors": "Some field miss check and enter", "exception": str(e), "status": False},
                            status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        userId = request.GET.get('id')
        data = request.data
        try:
            user = TestQuestions.objects.get(id=userId)
        except TestQuestions.DoesNotExist:
            return Response({"error": "Icards video ID not found", "status": False}, status=status.HTTP_400_BAD_REQUEST)
        serializer = TestQuestionsSerializer(user, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data, status=status.HTTP_206_PARTIAL_CONTENT)

    def delete(self, request, format=None):
        if request.GET.get('id'):
            get_object_or_404(TestQuestions, id=request.GET.get('id')).delete()
        else:
            get_object_or_404(TestQuestions, id=request.data.get('id')).delete()
        return Response({"success": "Id related data deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


class TestQuestionStatisticsView(APIView):

    def get(self, request, format=None):
        response = {}
        userId = request.GET.get('id')
        sub_id = request.GET.get('sub_id')
        if userId:
            qs = TestQuestionStatistics.objects.filter(id=userId)
        elif sub_id:
            subid = get_object_or_404(Test_SubCategory, id=sub_id)
            qs = subid.TestQuestionStatistics_set.all().order_by('id')
        else:
            qs = TestQuestionStatistics.objects.all().order_by('id')

        for data in qs:
            response[data.id] = {
                "id": data.id,              
                "test_sub_category_id": data.test_sub_category.id,          
                "skipped": data.skipped,
                "wrong": data.wrong,
                "correct": data.correct,
                "not_viewed": data.not_viewed    
            }
        return Response(response.values(), status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        try:
            serializer = TestQuestionStatisticsSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
            return Response({"Status": True,
                             "Message": "Successfully Registered TestQuestionStatistics"},
                            status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"Errors": "Some field miss check and enter", "exception": str(e), "status": False},
                            status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        userId = request.GET.get('id')
        data = request.data
        try:
            user = TestQuestionStatistics.objects.get(id=userId)
        except TestQuestionStatistics.DoesNotExist:
            return Response({"error": "Icards video ID not found", "status": False}, status=status.HTTP_400_BAD_REQUEST)
        serializer = TestQuestionStatisticsSerializer(user, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data, status=status.HTTP_206_PARTIAL_CONTENT)

    def delete(self, request, format=None):
        if request.GET.get('id'):
            get_object_or_404(TestQuestionStatistics, id=request.GET.get('id')).delete()
        else:
            get_object_or_404(TestQuestionStatistics, id=request.data.get('id')).delete()
        return Response({"success": "Id related data deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
class TestQuestionDiscussionView(APIView):

    def get(self, request, format=None):
        response = {}
        userId = request.GET.get('id')
        sub_id = request.GET.get('sub_id')
        if userId:
            qs = TestQuestionDiscussion.objects.filter(id=userId)
        elif sub_id:
            subid = get_object_or_404(Test_SubCategory, id=sub_id)
            qs = subid.TestQuestionDiscussion_set.all().order_by('id')
        else:
            qs = TestQuestionDiscussion.objects.all().order_by('id')

        for data in qs:
            response[data.id] = {
                "id": data.id,              
                "test_sub_category_id": data.test_sub_category.id,          
                "video": data.video.url if data.video else "no video",
                "question": data.question,
                "question_time": data.question_time,  
                "image": data.image.url if data.image else "no image",        
                "notes": data.notes.url if data.notes else "no notes",
                "bookmark": data.bookmark   
            }
        return Response(response.values(), status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        try:
            serializer = TestQuestionDiscussionSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
            return Response({"Status": True,
                             "Message": "Successfully Registered TestQuestionDiscussion"},
                            status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"Errors": "Some field miss check and enter", "exception": str(e), "status": False},
                            status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        userId = request.GET.get('id')
        data = request.data
        try:
            user = TestQuestionDiscussion.objects.get(id=userId)
        except TestQuestionDiscussion.DoesNotExist:
            return Response({"error": "Icards video ID not found", "status": False}, status=status.HTTP_400_BAD_REQUEST)
        serializer = TestQuestionDiscussionSerializer(user, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data, status=status.HTTP_206_PARTIAL_CONTENT)

    def delete(self, request, format=None):
        if request.GET.get('id'):
            get_object_or_404(TestQuestionDiscussion, id=request.GET.get('id')).delete()
        else:
            get_object_or_404(TestQuestionDiscussion, id=request.data.get('id')).delete()
        return Response({"success": "Id related data deleted successfully"}, status=status.HTTP_204_NO_CONTENT)



class TestDiscussionView(APIView):

    def get(self, request, format=None):
        response = {}
        userId = request.GET.get('id')
        if userId:
            qs = TestDiscussion.objects.filter(id=userId)
        else:
            qs = TestDiscussion.objects.all().order_by('id').first()

        try:
            response[qs.id] = {
                "id": qs.id,
                "question": qs.question,
                "answer1": qs.answer1,
                "answer2": qs.answer2,
                "answer3": qs.answer3,
                "answer4": qs.answer4,
                "correctanswer": qs.correctanswer,
                "explanation": qs.explanation,
                "image": qs.image.url if qs.image else "no image"
            }
            return Response(response.values(), status=status.HTTP_200_OK)
        except:
            return Response({'message': 'No Data'}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        data = request.data
        try:
            serializer = TestDiscussionSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
            return Response({"Status": True,
                             "Message": "Successfully Registered TestDiscussion"},
                            status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"Errors": "Some field miss check and enter", "exception": str(e), "status": False},
                            status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        userId = request.GET.get('id')
        data = request.data
        try:
            user = TestDiscussion.objects.get(id=userId)
        except TestDiscussion.DoesNotExist:
            return Response({"error": "TestDiscussion ID not found", "status": False},
                            status=status.HTTP_400_BAD_REQUEST)
        serializer = TestDiscussionSerializer(user, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data, status=status.HTTP_206_PARTIAL_CONTENT)

    def delete(self, request, format=None):
        if request.GET.get('id'):
            get_object_or_404(TestDiscussion, id=request.GET.get('id')).delete()
        else:
            TestDiscussion.objects.all().delete()
        return Response({"success": "Id related data deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

class DiscussionView(APIView):

    def get(self, request, format=None):
        response = {}
        userId = request.GET.get('id')
        if userId:
            qs = Discussion.objects.filter(id=userId)
        else:
            qs = Discussion.objects.all().order_by('id').first()

        try:
            response[qs.id] = {
                "id": qs.id,                   
                "video": qs.video.url if qs.video else "no video",
                "question": qs.question,
                "question_time": qs.question_time,  
                "notes": qs.notes.url if qs.notes else "no notes",
                "image": qs.image.url if qs.image else "no image",        
                "bookmark": qs.bookmark   
            }
            return Response(response.values(), status=status.HTTP_200_OK)
        except:
            return Response({'message': 'No Data'}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        data = request.data
        try:
            serializer = DiscussionSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
            return Response({"Status": True,
                             "Message": "Successfully Registered Discussion"},
                            status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"Errors": "Some field miss check and enter", "exception": str(e), "status": False},
                            status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        userId = request.GET.get('id')
        data = request.data
        try:
            user = Discussion.objects.get(id=userId)
        except Discussion.DoesNotExist:
            return Response({"error": "Discussion ID not found", "status": False},
                            status=status.HTTP_400_BAD_REQUEST)
        serializer = DiscussionSerializer(user, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data, status=status.HTTP_206_PARTIAL_CONTENT)

    def delete(self, request, format=None):
        if request.GET.get('id'):
            get_object_or_404(Discussion, id=request.GET.get('id')).delete()
        else:
            Discussion.objects.all().delete()
        return Response({"success": "Id related data deleted successfully"}, status=status.HTTP_204_NO_CONTENT)




class GroupDiscussionAdminView(APIView):

    def get(self, request, format=None):
        response = {}
        userId = request.GET.get('id')
        if userId:
            qs = GroupDiscussionAdmin.objects.filter(id=userId)
        else:
            qs = GroupDiscussionAdmin.objects.all()

        for data in qs:
            print(data)
            response[data.id] = {
                "id": data.id,
                "groupname": data.groupname
            }
        return Response(response.values(), status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        try:
            serializer = GroupDiscussionAdminSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
            return Response({"Status": True,
                             "Message": "Successfully Registered GroupDiscussionAdmin"},
                            status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"Errors": "Some field miss check and enter", "exception": str(e), "status": False},
                            status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        userId = request.GET.get('id')
        data = request.data
        try:
            user = GroupDiscussionAdmin.objects.get(id=userId)
        except GroupDiscussionAdmin.DoesNotExist:
            return Response({"error": "Question Discussion ID not found", "status": False},
                            status=status.HTTP_400_BAD_REQUEST)
        serializer = GroupDiscussionAdminSerializer(user, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data, status=status.HTTP_206_PARTIAL_CONTENT)

    def delete(self, request):
        if request.GET.get('id'):
            get_object_or_404(GroupDiscussionAdmin, id=request.GET.get('id')).delete()
        else:
            GroupDiscussionAdmin.objects.all().delete()
        return Response({"success": "Id related data deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


class GroupDiscussionUserView(APIView):

    def get(self, request, format=None):
        response = {}
        userId = request.GET.get('id')
        if userId:
            qs = GroupDiscussionUser.objects.filter(id=userId)
        else:
            qs = GroupDiscussionUser.objects.all()

        for data in qs:
            print(data)
            response[data.id] = {
                "id": data.id,           
                "user_id": data.user.id,        
                "group_id": data.group.id,        
                "question": data.question,
                "file": data.file.url if data.file else "no file",
                "answer1": data.answer1,
                "answer2": data.answer2,
                "answer3": data.answer3,
                "answer4": data.answer4,
                "correctanswer": data.correctanswer           
            }
        return Response(response.values(), status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        try:
            serializer = GroupDiscussionUserSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
            return Response({"Status": True,
                             "Message": "Successfully Registered GroupDiscussionUser"},
                            status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"Errors": "Some field miss check and enter", "exception": str(e), "status": False},
                            status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        userId = request.GET.get('id')
        data = request.data
        try:
            user = GroupDiscussionUser.objects.get(id=userId)
        except QuestionDiscussionbookMark.DoesNotExist:
            return Response({"error": "GroupDiscussionUser ID not found", "status": False},
                            status=status.HTTP_400_BAD_REQUEST)
        serializer = GroupDiscussionUserSerializer(user, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data, status=status.HTTP_206_PARTIAL_CONTENT)

    def delete(self, request):
        if request.GET.get('id'):
            get_object_or_404(GroupDiscussionUser, id=request.GET.get('id')).delete()
        else:
            get_object_or_404(GroupDiscussionUser, id=request.data.get('id')).delete()
        return Response({"success": "Id related data deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


class DailyBoosterBookMarkView(APIView):

    def get(self, request, format=None):
        response = {}
        userId = request.GET.get('id')
        if userId:
            qs = DailyBoosterBookMark.objects.filter(id=userId)
        else:
            qs = DailyBoosterBookMark.objects.all()

        for data in qs:
            print(data)
            response[data.id] = {
                "id": data.id,
                "DailyBoostermain_title": data.DailyBoostermain.title,
                "DailyBoostermain_id": data.DailyBoostermain.id,
                "user_id": data.user.id,
                "boookmark_status": data.bookmark_status
            }
        return Response(response.values(), status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        try:
            serializer = DailyBoosterBookMarkSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
            return Response({"Status": True,
                             "Message": "Successfully Registered DailyBoosterBookMark"},
                            status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"Errors": "Some field miss check and enter", "exception": str(e), "status": False},
                            status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        userId = request.GET.get('id')
        data = request.data
        try:
            user = DailyBoosterBookMark.objects.get(id=userId)
        except DailyBoosterBookMark.DoesNotExist:
            return Response({"error": "DailyBoosterBookMark ID not found", "status": False},
                            status=status.HTTP_400_BAD_REQUEST)
        serializer = DailyBoosterBookMarkSerializer(user, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data, status=status.HTTP_206_PARTIAL_CONTENT)

    def delete(self, request):
        if request.GET.get('id'):
            get_object_or_404(DailyBoosterBookMark, id=request.GET.get('id')).delete()
        else:
            get_object_or_404(DailyBoosterBookMark, id=request.data.get('id')).delete()
        return Response({"success": "Id related data deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


class LeaderBoardView(APIView):

    def get(self, request, format=None):
        response = {}
        userId = request.GET.get('id')
        if userId:
            qs = LeaderBoard.objects.filter(id=userId)
        else:
            qs = LeaderBoard.objects.all()

        for data in qs:
            print(data)
            response[data.id] = {
                "id": data.id,
                "Test_SubCategory_title": data.Test_SubCategory.title,
                "Test_SubCategory_id": data.Test_SubCategory.id,
                "user_id": data.user.id,
                "score": data.score,
                "accuracy": data.accuracy
            }
        return Response(response.values(), status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        try:
            serializer = LeaderBoardSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
            return Response({"Status": True,
                             "Message": "Successfully Registered LeaderBoard"},
                            status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"Errors": "Some field miss check and enter", "exception": str(e), "status": False},
                            status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        userId = request.GET.get('id')
        data = request.data
        try:
            user = LeaderBoard.objects.get(id=userId)
        except LeaderBoard.DoesNotExist:
            return Response({"error": "LeaderBoard ID not found", "status": False},
                            status=status.HTTP_400_BAD_REQUEST)
        serializer = LeaderBoardSerializer(user, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data, status=status.HTTP_206_PARTIAL_CONTENT)

    def delete(self, request):
        if request.GET.get('id'):
            get_object_or_404(LeaderBoard, id=request.GET.get('id')).delete()
        else:
            get_object_or_404(LeaderBoard, id=request.data.get('id')).delete()
        return Response({"success": "Id related data deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

