#map our urls to our view function
from django.urls import path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns


urlpatterns=[
    path('dynamic-form/<int:modelid>/', views.DynamicFormAPIView.as_view(), name='dynamic_form_view'),
    path('aimodels/', views.AIModelList.as_view(),name="aimodels"),
    path('dynamic-form/<int:modelid>/<int:query_id>/', views.ExplainAPIView.as_view(),name='explain_api'),
    path('chatbot/<int:modelid>',views.chatbot,name='chatbot'),
    path('feedback/<int:query_id>/', views.FeedbackView.as_view(), name='feedback-create'),
    path('explanation/<int:pk>/rate/', views.ExplanationRatingAPIView.as_view(), name='explanation-rate'),
    path('modelDetails/<int:model_id>/',views.model_feedback_view),
    path('chats/<int:query_id>/', views.ChatListView.as_view(), name='chat-list'),
    #path returns urlpattern opject
    #always end route with /
    # path('',views.home,name="home"),
    # path('create-aimodel',views.createAIModel,name="create-aimodel"),
    # path('create-query', views.query_view, name='create-query'),
    # path('explain_query/<int:query_id>/', views.explain_query, name='explain_query'),
    # path('visualise_query/<int:query_id>/', views.visualise_query, name='visualise_query'),
    # ############# API
    # path('queries/', views.QueryList.as_view()),
    # path('queries/<int:pk>/', views.QueryDetail.as_view()),
    # ############
    # # path('create_modelversion/', views.ModelVersionCreateView.as_view()),
    # path('create_Query/', views.QueryCreateView.as_view()),
    # # path('aimodels/<int:ai_model_id>/modelvs/', views.ModelVersionList.as_view()),
    # path('query-explanation/<int:query_id>/', views.QueryExplanationAPIView.as_view(), name='query-explanation'),
    # # path('aimodels/<int:ai_model_id>/modelvs/<int:model_version_id>/', views.DynamicFormView.as_view()),
    path('upload/', views.upload_model, name='upload_model'),
    path('user-queries/', views.UserQueryListView.as_view(), name='user-query-list'),
    # # path('success/', views.success, name='success'),  
    # # path('runcode/',views.run_code,name="runcode"),
]

urlpatterns = format_suffix_patterns(urlpatterns)
