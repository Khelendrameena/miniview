from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.shortcuts import redirect
from django.conf import settings

class MySocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        # Automatically proceed to the provider login
        if not sociallogin.is_existing:
            return redirect(settings.SOCIALACCOUNT_PROVIDERS['google']['APP']['login_url'])
