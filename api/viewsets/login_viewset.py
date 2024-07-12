import requests
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from api.constants import Constants


class LoginViewSet(viewsets.GenericViewSet):
    permission_classes = []
    authentication_classes = []

    @action(methods=['post'], detail=False, url_path='login', url_name='login')
    def login(self, request):
        headers = {
            'Content-Type': 'application/json'
        }
        try:
            login_token = requests.post(
                Constants.USUARIOS_URL + '/token/',
                json=request.data,
                headers=headers
            )
            login_token.raise_for_status()
            token_str = login_token.json().get('access')
            token_obj = AccessToken(token_str)
            role_id = token_obj['role']
            if role_id not in [2, 5]:
                return Response(
                    data={'detail': 'No tienes permisos para acceder a esta pagina'},
                    status=403
                )
            return Response(
                data=login_token.json(),
                status=login_token.status_code
            )
        except requests.exceptions.HTTPError as e:
            return e.response.json()
