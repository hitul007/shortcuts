# =================================================================================================
# Verify OTP
# =================================================================================================
import secrets

# URL
# path("verify-phone/", jc.VerifyOTP.as_view()),

class OTPVerification(jcb_models.BaseModel):
    otp = models.CharField(max_length=10)
    user = models.ForeignKey(auth_models.User, on_delete=models.PROTECT)
    is_verified = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        # Generate Crypto OTP.
        secret_generator = secrets.SystemRandom()
        if not self.otp:
            self.otp = str(secret_generator.randrange(1000, 9999))

        super().save(*args, **kwargs)

        # TODO: Send OTP.


class OTPVerificationSerializer(serializers.Serializer):
    mobile = serializers.CharField(max_length=20)
    otp = serializers.CharField(max_length=10)

    def validate_mobile(self, value):
        owner_profile_instance = jc_backend_models.UserProfile.objects.filter(
            is_deleted=False, contact_number=value
        ).last()
        if not owner_profile_instance:
            raise serializers.ValidationError("Invalid mobile")

        return owner_profile_instance


class VerifyOTP(View):
    def post(self, request):
        serializer_instance = jcb_serializers.OTPVerificationSerializer(
            data=request.data
        )
        if not serializer_instance.is_valid():
            return jc_utils.create_response(
                serializer_instance.errors, 400, message="Bad request"
            )

        otp = serializer_instance.validated_data.get("otp")
        owner_profile_instance = serializer_instance.validated_data.get("mobile")
        jc_models.OTPVerification.objects.filter(
            otp=otp,
            user=owner_profile_instance.user,
            created_at__gte=timezone.now() - datetime.timedelta(minutes=2),
        ).count()

        owner_profile_instance.is_phone_verified = True
        owner_profile_instance.save(update_fields=["is_phone_verified"])

        return jc_utils.create_response({}, 200, message="Success")



# =================================================================================================
# Email verify
# =================================================================================================

# URL
# path(
#        "verify-email/<uuid:token>/", jc.VerifyEmailViewset.as_view()
#    )
from django.shortcuts import Http404


class VerifyEmailViewset(View):
    def get(self, request, token):
        if not token:
            raise Http404

        verification_token = jc_models.EmailVerification.objects.filter(
            token=token, is_verified=False
        ).last()

        if verification_token:
            verification_token.is_verified = True
            verification_token.save(update_fields=["is_verified"])
        else:
            raise Http404

        return HttpResponse("Email has been verified.")


class EmailVerification(jcb_models.BaseModel):
    user = models.ForeignKey(auth_models.User, on_delete=models.PROTECT)
    token = models.UUIDField(max_length=100, default=uuid.uuid4)
    is_verified = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.is_verified:
            profile_instance = self.user.user_profile.filter(is_deleted=False).last()
            if profile_instance:
                profile_instance.is_email_verified = True
                profile_instance.save(update_fields=["is_email_verified"])


# =================================================================================================
# Login Token based
# =================================================================================================
# URL
# path("login/", jc.LoginViewset.as_view()),

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length=100)
    device_id = serializers.CharField(max_length=300)
    device_type = serializers.CharField(max_length=20)


class UserDeviceId(jcb_models.BaseModel):
    device_id = models.CharField(max_length=300)
    device_type = models.CharField(max_length=20)
    user = models.ForeignKey(auth_models.User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("device_id", "user", "is_deleted")


class LoginViewset(APIView):
    def post(self, request):
        """
        View to do login
        """
        serializer_instance = jcb_serializers.LoginSerializer(data=request.data)
        if not serializer_instance.is_valid():
            return jc_utils.create_response(
                serializer_instance.errors, 400, message="Bad request"
            )

        user = authenticate(
            username=serializer_instance.validated_data.get("email"),
            password=serializer_instance.validated_data.get("password"),
        )

        user_device_instance = jc_models.UserDeviceId.objects.filter(
            device_id=serializer_instance.validated_data.get("device_id"),
            device_type=serializer_instance.validated_data.get("device_type"),
            user=user,
        ).last()

        if user_device_instance:
            if user_device_instance.is_deleted:
                user_device_instance.is_deleted = False
                user_device_instance.save(update_fields=["is_deleted"])
        else:
            try:
                jc_models.UserDeviceId.objects.create(
                    device_id=serializer_instance.validated_data.get("device_id"),
                    device_type=serializer_instance.validated_data.get("device_type"),
                    user=user,
                )
            except Exception:
                pass

        if user:
            token_instance, _ = Token.objects.get_or_create(user=user)
            return jc_utils.create_response(
                {"token": token_instance.key}, 200, message="Success"
            )
        else:
            return jc_utils.create_response({}, 403, message="Unauthorized")



# =================================================================================================
# Logout Token based
# =================================================================================================
# URL
# path("logout/", jc.Logout.as_view()),

class LogoutSerializer(serializers.Serializer):
    device_id = serializers.CharField(max_length=300)

class Logout(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer_instance = jcb_serializers.LogoutSerializer(data=request.data)

        if not serializer_instance.is_valid():
            return jc_utils.create_response(
                serializer_instance.errors, 400, message="Bad request"
            )

        # TODO: Remove token afterwards.

        jc_models.UserDeviceId.objects.filter(
            device_id=serializer_instance.validated_data.get("device_id"),
            user=request.user,
        ).update(is_deleted=True)

        return jc_utils.create_response({}, 200, message="Success")


# =================================================================================================
# Signup
# =================================================================================================
class SignupViewset(APIView):
    def post(self, request):
        """
        View to do signup.
        """
        serializer_instance = jcb_serializers.SignupSerializer(data=request.data)
        if not serializer_instance.is_valid():
            return jc_utils.create_response(
                serializer_instance.errors, 400, message="Bad request"
            )

        _, user_instance = serializer_instance.save()

        # TODO: Send OTP.
        jc_models.OTPVerification.objects.create(user=user_instance)
        # TODO: Send notification to jay with email.

        return jc_utils.create_response(
            {},
            200,
            message="Account created successfully. We will verify and get back to you.",
        )

class SignupSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=30)
    last_name = serializers.CharField(max_length=30)
    email = serializers.EmailField()
    password = serializers.CharField(max_length=100)
    gstin_no = serializers.CharField(max_length=30)
    company_name = serializers.CharField(max_length=30)
    contact_number = serializers.CharField(max_length=20)
    address = serializers.CharField(max_length=250)
    usertype = serializers.CharField(max_length=200)

    def validate_email(self, value):
        emails = dj_models.User.objects.filter(email=value).count()
        if emails:
            raise serializers.ValidationError("Email already exists")

        return value

    def validate_contact_number(self, value):
        if jc_backend_models.OwnerProfile.objects.filter(
            contact_number=value, is_deleted=False
        ).count():
            raise serializers.ValidationError("Contact number already exists")

    def save(self):
        validated_data = self.validated_data
        user_instance = dj_models.User.objects.create_user(
            username=validated_data.get("email"),
            email=validated_data.get("email"),
            first_name=validated_data.get("first_name"),
            last_name=validated_data.get("last_name"),
            password=validated_data.get("password"),
        )
        user_instance.is_active = False
        user_instance.save()

        owner_profile_instance = jc_backend_models.OwnerProfile.objects.create(
            company_name=validated_data.get("company_name"),
            contact_number=validated_data.get("contact_number"),
            address=validated_data.get("address"),
            gstin_no=validated_data.get("gstin_no"),
            user=user_instance,
        )


        # Send email verification email.
        send_mail(
            "Team: Verify your email",
            html_message="""
            <p>Hi {name},</p>

            <p>To serve you better, please verify the email address by clicking below link.</p>

            <p>Link - <a href="{link}">Link</a> </p>
            """.format(
                name="%s %s" % (user_instance.first_name, user_instance.last_name),
                link=dj_settings.BASE_URL + reverse(),
            ),
        )


        return owner_profile_instance, user_instance

