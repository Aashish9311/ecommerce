from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'stock', 'image']
        
    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price <= 0:
            raise forms.ValidationError("Price must be greater than zero.")
        return price
    
    def clean_stock(self):
        stock = self.cleaned_data.get('stock')
        if stock < 0:
            raise forms.ValidationError("Stock cannot be negative.")
        return stock
    
    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            # Check file size
            if image.size > 5 * 1024 * 1024:  # 5MB
                raise forms.ValidationError("Image file size should not exceed 5MB.")
            
            # Check file extension
            valid_extensions = ['jpg', 'jpeg', 'png', 'gif']
            import os
            ext = os.path.splitext(image.name)[1][1:].lower()
            if ext not in valid_extensions:
                raise forms.ValidationError(f"Unsupported file extension. Allowed extensions: {', '.join(valid_extensions)}")
        return image