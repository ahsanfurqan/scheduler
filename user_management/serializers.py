from rest_framework import serializers
from .models import CustomUser, Patient, Counsellor
import django.contrib.auth.password_validation as validators
from django.core import exceptions

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username','first_name','last_name','email','is_counsellor','is_patient',"password"]
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        is_patient = validated_data.get('is_patient', False)
        is_counsellor = validated_data.get('is_counsellor', False)
        
        # Check atleast one Should Be true
        if not is_patient and not is_counsellor:
            raise serializers.ValidationError('Patient or Councellor at least one must be selected')
        # get the password from the data
        password = validated_data.get('password', '')
         
        errors = dict() 
        try:
            # validate the password and catch the exception
            validators.validate_password(password=password, user=self.instance)
         
        # the exception raised here is different than serializers.ValidationError
        except exceptions.ValidationError as e:
            errors['password'] = list(e.messages)        
        
        if errors:
            raise serializers.ValidationError(errors)
        
        user = CustomUser.objects.create_user(**validated_data)
        
        # Create associated Patient or Counsellor
        if is_patient:
            Patient.objects.create(user=user)

        if is_counsellor:
            Counsellor.objects.create(user=user)

        return user
    
class UpdateUserSearilizer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['first_name','last_name','is_counsellor','is_patient']
        extra_kwargs = {'password': {'write_only': True}}

class PatientUpdateSerializer(serializers.ModelSerializer):
    user = UpdateUserSearilizer(required=False,partial=True)

    class Meta:
        model = Patient
        fields = '__all__'
        
    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', {})
        user_instance = instance.user
        # Check if is_counsellor field has been modified
        is_counsellor_changed = user_instance.is_counsellor != user_data.get('is_counsellor', user_instance.is_counsellor)
        # Update user fields only if data is provided
        if user_data:
            for attr, value in user_data.items():
                setattr(user_instance, attr, value)
            user_instance.save()

        # Check and update associated Counsellor instance
        if is_counsellor_changed:
            is_counsellor = user_data.get('is_counsellor', user_instance.is_counsellor)
            
            if is_counsellor:
                # Check if a Counsellor instance already exists
                counsellor_instance, created = Counsellor.objects.get_or_create(user=user_instance)

                # Activate or deactivate the Counsellor instance
                counsellor_instance.is_active = instance.is_active
                counsellor_instance.save()
            else:
                # Deactivate the associated Counsellor instance
                Counsellor.objects.filter(user=instance.user).update(is_active=False)
        

        # Continue with the update for the Counsellor model
        return super().update(instance, validated_data)
    
class PatientSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()

    class Meta:
        model = Patient
        fields = '__all__'
    

class CounsellorSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()

    class Meta:
        model = Counsellor
        fields = '__all__'
            
class CounsellorUpdateSerializer(serializers.ModelSerializer):
    user = UpdateUserSearilizer(required=False,partial=True)

    class Meta:
        model = Counsellor
        fields = '__all__'
    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', {})
        user_instance = instance.user

         # Check if is_patient field has been modified
        is_patient_changed = user_instance.is_patient != user_data.get('is_patient', user_instance.is_patient)
        # Update user fields only if data is provided
        if user_data:
            for attr, value in user_data.items():
                setattr(user_instance, attr, value)
            user_instance.save()

        # Check and update associated Patient instance
        if is_patient_changed:
            is_patient = user_data.get('is_patient', user_instance.is_patient)
            
            if is_patient:
                # Check if a Patient instance already exists
                pateint_instance, created = Patient.objects.get_or_create(user=user_instance)

                # Activate or deactivate the Patient instance
                pateint_instance.is_active = instance.is_active
                pateint_instance.save()
            else:
                # Deactivate the associated Patient instance
                Patient.objects.filter(user=instance.user).update(is_active=False)
        

        # Continue with the update for the Counsellor model
        return super().update(instance, validated_data)
