from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class MyPagination(PageNumberPagination):
    def get_paginated_response(self, data):
        return Response({
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'num_pages': self.page.paginator.num_pages ,
            'count': self.page.paginator.count,
            'results': data
        })
