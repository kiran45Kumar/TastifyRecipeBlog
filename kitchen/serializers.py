from rest_framework import serializers
from kitchen.models import Kitchen, CookingCategory

class KitchenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kitchen
        fields = '__all__'
        def validate(self, attrs):
            kitchen_name = attrs.get('kitchen_name')
            website_url = attrs.get('website_url')
            business_email = attrs.get('business_email')
            qs = Kitchen.objects.all()
            if self.instance:
                qs = qs.exclude(pk=self.instance.pk)

            if qs.filter(kitchen_name__iexact=kitchen_name).exists():
                raise serializers.ValidationError({'kitchen_name': 'Kitchen name already exists'})
            if website_url and qs.filter(website_url__iexact=website_url).exists():
                raise serializers.ValidationError({'website_url': 'Website URL already exists'})
            if business_email and qs.filter(business_email__iexact=business_email).exists():
                raise serializers.ValidationError({'business_email': 'Business email already exists'})

            return attrs
        
class CookingCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CookingCategory
        fields = '__all__'