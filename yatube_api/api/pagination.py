from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response


class CustomLimitOffsetPagination(LimitOffsetPagination):
    """
    Класс для настройки собственной пагинации.

    Параметры:
        default_limit -- количество элементов на странице по умолчанию.
        max_limit -- максимальное количество элементов на странице.
    """

    def paginate_queryset(self, queryset, request, view=None):
        no_pagination = ('limit' not in request.query_params
                         and 'offset' not in request.query_params)
        if no_pagination:
            return None
        return super().paginate_queryset(queryset, request, view)

    def get_paginated_response(self, data):
        if self.limit is None and self.offset is None:
            return Response(data)
        return super().get_paginated_response(data)
