from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class CustomPagination(PageNumberPagination):
    page_size = 10  # Set the number of items per page
    page_size_query_param = 'page_size'
    max_page_size = 100
    
    
    def get_paginated_response(self, data):
         return Response({
            'pagination': {
                'current_page': self.page.number,
                'next': self.get_next_link(),
                'previous': self.get_previous_link(),
                'total_pages': self.page.paginator.num_pages,
                'total_items': self.page.paginator.count,
            },
            'results': data, # The paginated data
            'status': True,   # Custom status field
            'code': 200,      # Custom code field
            'message': 'Data retrieved successfully',  # Custom message field
        })







# class CustomPagination(pagination.PageNumberPagination): # type: ignore
#     def get_paginated_response(self, data):
#         return Response({
#             'links': {
#                 'next': self.get_next_link(),
#                 'previous': self.get_previous_link()
#             },
#             'count': self.page.paginator.count,
#             'status':'Success',
#             'message':'user display successfully!',
#             'code':200,
#             'results': data
#         })    