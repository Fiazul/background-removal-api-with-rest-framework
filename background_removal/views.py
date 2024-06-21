from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse
from .serializers import ImageUploadSerializer
from .utils import remove_background, add_background
from .tests import generate_and_save_image
import os

class BackgroundRemovalAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = ImageUploadSerializer(data=request.data)
        if serializer.is_valid():
            image_file = serializer.validated_data['image_file']
            bg_option = serializer.validated_data.get('bg_option', 'none')
            bg_color = serializer.validated_data.get('bg_color')
            bg_image = serializer.validated_data.get('bg_image')
            prompt = serializer.validated_data.get('bg_prompt')
            output_folder = r"D:\bgremove\myproject\background_removal\temp"
            
            bg_prompt = generate_and_save_image(prompt, output_folder)
            print('image',bg_prompt)
            print('bg',bg_image)
        
            
            

            processed_image = remove_background(image_file)

            if processed_image:
                print("imagep",bg_prompt)
                if bg_option in ['white', 'color', 'image', 'prompt']:
                    processed_image = add_background(processed_image, bg_option, bg_color, bg_image,bg_prompt)

                response = HttpResponse(processed_image, content_type='image/png')
                response['Content-Disposition'] = 'attachment; filename="processed_image.png"'
                if bg_option == 'prompt': 
                    os.remove(bg_prompt)
                return HttpResponse(processed_image, content_type='image/png')
            
            else:
                return Response({'error': 'Background removal failed.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        
def upload_form(request):
        return render(request, 'templates/upload.html')

