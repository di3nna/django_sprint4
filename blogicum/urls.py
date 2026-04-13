from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    # 🔥 ИЗМЕНЕНО: сначала свои пути users, потом стандартные auth
    path('auth/', include('users.urls')),
    path('auth/', include('django.contrib.auth.urls')),
    path('', include('blog.urls')),
    path('pages/', include('pages.urls')),
]

# 🔥 ДОБАВЛЕНО: обработчики ошибок
handler404 = 'pages.views.page_not_found'
handler500 = 'pages.views.server_error'

# 🔥 ДОБАВЛЕНО: для разработки (медиафайлы и debug_toolbar)
if settings.DEBUG:
    import debug_toolbar
    urlpatterns += (path('__debug__/', include(debug_toolbar.urls)),)
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
