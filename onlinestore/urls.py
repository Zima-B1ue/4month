from django.contrib import admin
from django.urls import path
from products.views import MainPageCBV, ProductCBV, ProductDetailCBV, CreateProductCBV
from onlinestore.settings import MEDIA_URL, MEDIA_ROOT
from django.conf.urls.static import static
from users.views import register_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', MainPageCBV.as_view(template_name='layouts/index.html')),
    path('products/', ProductCBV.as_view()),
    path('products/<int:id>/', ProductDetailCBV.as_view()),
    path('products/create/', CreateProductCBV.as_view()),

    path('users/register/', register_view)
]
urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)