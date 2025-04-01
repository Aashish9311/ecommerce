from django import forms

class ShippingAddressForm(forms.Form):
    full_name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(required=True)
    phone = forms.CharField(max_length=15, required=True)
    address_line1 = forms.CharField(max_length=100, required=True)
    address_line2 = forms.CharField(max_length=100, required=False)
    city = forms.CharField(max_length=100, required=True)
    state = forms.CharField(max_length=100, required=True)
    postal_code = forms.CharField(max_length=20, required=True)
    country = forms.CharField(max_length=100, required=True)
    shipping_notes = forms.CharField(widget=forms.Textarea, required=False)
    
    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        # Basic phone number validation
        if not phone.isdigit():
            raise forms.ValidationError("Phone number should contain only digits.")
        if len(phone) < 10:
            raise forms.ValidationError("Phone number should be at least 10 digits.")
        return phone
    
    def clean_postal_code(self):
        postal_code = self.cleaned_data.get('postal_code')
        # Basic postal code validation
        if not postal_code.isalnum():
            raise forms.ValidationError("Postal code should contain only letters and numbers.")
        return postal_code
    
    def get_shipping_address(self):
        """Format the shipping address as a string"""
        data = self.cleaned_data
        address_parts = [
            data['full_name'],
            data['address_line1']
        ]
        
        if data.get('address_line2'):
            address_parts.append(data['address_line2'])
            
        address_parts.extend([
            f"{data['city']}, {data['state']} {data['postal_code']}",
            data['country'],
            f"Phone: {data['phone']}",
            f"Email: {data['email']}"
        ])
        
        if data.get('shipping_notes'):
            address_parts.append(f"Notes: {data['shipping_notes']}")
            
        return "\n".join(address_parts)