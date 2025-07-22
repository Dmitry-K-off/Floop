from django.urls import path
from .views import SubmitDataView, SubmitDataDetailView, SubmitDataUpdateView, SubmitDataListByUserView

urlpatterns = [
    path('submitData/', SubmitDataView.as_view(), name='submit-data'),
    path('submitData/<int:id>/', SubmitDataDetailView.as_view(), name='submit-data-detail'), # GET по ID
    path('submitData/<int:id>/edit/', SubmitDataUpdateView.as_view(), name='submit-data-update'), # PATCH
    path('submitData/user/', SubmitDataListByUserView.as_view(), name='submit-data-list-by-user') # GET по email
]
