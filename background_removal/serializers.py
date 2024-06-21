from rest_framework import serializers

class ImageUploadSerializer(serializers.Serializer):
    image_file = serializers.ImageField()
    bg_option = serializers.ChoiceField(choices=['none', 'white', 'color', 'image','prompt'], required=False)
    bg_color = serializers.CharField(max_length=7, required=False)  # Hex color code
    bg_image = serializers.ImageField(required=False)
    bg_prompt = serializers.CharField(max_length=30,required=False)
    
