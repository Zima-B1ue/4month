from django.contrib import admin
from django.urls import path
from products.views import main_page_view, products_view, product_detail_view, create_product_view
from onlinestore.settings import MEDIA_URL, MEDIA_ROOT
from django.conf.urls.static import static
from users.views import register_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', main_page_view),
    path('products/', products_view),
    path('products/<int:id>/', product_detail_view),
    path('products/create/', create_product_view),

    path('users/register/', register_view)
]
urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)