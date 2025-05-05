from django.urls import path
from myapp import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views




urlpatterns = [
    # path('', views.index, name='index'),
    path('',views.data_overview_view, name='overview'),
    # path('upload/', views.upload_file, name='upload_file'),
    path('overview/', views.data_overview_view, name='overview'),
    path('plot/', views.plot_selection_view, name='plot'),
    path('feature_selection/', views.feature_selection_view, name='feature_selection'),    #path('modeling/', views.modeling_view, name='modeling'),
    #path('data-treatment/', views.data_treatment_view, name='data_treatment'),
    #path('scoring/', views.scoring_view, name='scoring'),
    #path('change_data_type/', views.change_data_type, name='change_data_type'),
    #path('remove_column/', views.remove_column, name='remove_column'),
    #path('feature-engineering/', views.feature_engineering, name='feature_engineering'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    #path('accounts/login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    #path('accounts/logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('pd/', views.pd_view, name='pd'),
    path('lgd/', views.lgd_view, name='lgd'),  # Ensure this line exists
    path('ead/', views.ead_view, name='ead'),  # Ensure this line exists
    path('evaluation/', views.evaluation_view, name='evaluation'),
    
    # Vision 360°
    path('vision360/', views.vision360_view, name='vision360'),
    
    # Fiche Client
    path('fiche_client/', views.fiche_client_view, name='fiche_client'),



]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
