from django import forms
from .models import UserProfile
from django.core.exceptions import ValidationError
from os.path import splitext

class ProfilePhotoForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profile_photo']

    def clean_profile_photo(self):
        photo = self.cleaned_data.get('profile_photo')

        if photo:
            max_size = 2 * 1024 * 1024  # 2MB
            if photo.size > max_size:
                raise ValidationError("Image file too large ( > 2MB )")

            valid_extensions = ['.jpg', '.jpeg', '.png', '.webp']
            ext = splitext(photo.name)[1].lower()
            if ext not in valid_extensions:
                raise ValidationError("Only JPEG, PNG, and WebP formats are allowed.")
        
        return photo
