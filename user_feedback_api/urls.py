from django.urls import include, path
from rest_framework import routers
from .views import FeedbackViewSet, UserViewSet, get_user_feedbacks, new_feedback, user_login, user_logout, user_signup, delete_user
from django.contrib.auth import views as auth_views

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="User Feedback API",
      default_version='v1',
      description="User Feedback API for Nortal home assingment",
      terms_of_service="",
      contact=openapi.Contact(email="jere@sikstus.com"),
      license=openapi.License(name="Opensource"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

router = routers.DefaultRouter()
router.register(r'feedbacks', FeedbackViewSet, 'feedbacks')
router.register(r'users', UserViewSet, 'users')

urlpatterns = [
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),

    path('', include(router.urls)),
    path('users/<pk>/feedbacks', get_user_feedbacks, name='get_user_feedbacks'),
    path('new_feedback/', new_feedback, name='new_feedback'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('signup/', user_signup, name='signup'),
    path('delete_user/', delete_user, name='delete_user'),
]