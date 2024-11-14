from django.shortcuts import render

# Create your views here.
from rest_framework import generics

from new_app.models import Enquiry


#
# class SnippetList(generics.ListCreateAPIView):
#     queryset = Enquiry.objects.all()
#     serializer_class = Enquiry_serializer


# views.py
import gspread
from google.oauth2.service_account import Credentials
from rest_framework.response import Response
from rest_framework import status, views

from django.conf import settings

from new_app.serializer import EnquirySerializer

import gspread
from google.oauth2.service_account import Credentials
from rest_framework.response import Response
from rest_framework import status, views

from django.conf import settings


class EnquiryToGoogleSheetView(views.APIView):
    def post(self, request):
        # Serialize data
        serializer = EnquirySerializer(data=request.data)
        if serializer.is_valid():
            # Define the Google Sheets API scope
            SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

            # Authenticate with the correct scope and open Google Sheet
            creds = Credentials.from_service_account_file(
                settings.GOOGLE_SHEETS_CREDS, scopes=SCOPES
            )
            client = gspread.authorize(creds)
            sheet = client.open_by_key(settings.GOOGLE_SHEET_ID).sheet1  # or specify sheet name if not sheet1

            # Extract data from the validated serializer
            name = serializer.validated_data['name']
            phone = serializer.validated_data['phone']
            email = serializer.validated_data['email']

            # Append row to Google Sheet
            sheet.append_row([name, phone, email])

            return Response({"message": "Enquiry saved to Google Sheet"}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

