from django.urls import path, re_path, include
from . import views
from django.views.generic import TemplateView

# urlpatterns = [
#     path("", views.homepageview, name="home"),
#     path("index/", views.index, name="index"),
#     re_path(r"^about/contacts", views.contacts, name="contacts"),
#     re_path(r"^about/", views.about, name="about", kwargs={"name": "Egor", "age": 99}),
#     re_path(r"^user/(?P<name>\D+)/(?P<age>\d+)/", views.user, name="user"),
#     re_path(r"^user/(?P<name>\D+)/", views.user),
#     re_path(r"^user/", views.user),
#     path("message/<str:category>/<str:subcategory>/<str:theme>/<int:number>/", views.message)
#     # path("user/<str:name>/<int:age>/", views.user, name="user_full"),
#     # path("user/<str:name>/", views.user, name="user_name"),
#     # path("user/", views.user, name="user_default")
# ]




product_patterns = [
    path("", views.products),
    path("comments/", views.comments),
    path("questions/", views.questions),
]

urlpatterns = [
    path("", views.index, name="home"),
    path("products/<int:id>/", include(product_patterns)),
    path("user/", views.user),
    path("contacts/", views.contacts),
    path("direct/", views.direct),
    path("info/", views.info, name="info")
    # path("info/", TemplateView.as_view(template_name="blog/info.html", extra_context={"header": "ABOUT SITE"}),
    #      name="info"),
]

