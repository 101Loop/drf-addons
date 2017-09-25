from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from .add_ons import JsonResponse, paginate_data


class ValidateAndPerformView(APIView):
    renderer_classes = (JSONRenderer, )
    permission_classes = (AllowAny, )
    serializer_class = None
    show_serializer = None
    model = None

    def validated(self, serialized_data, *args, **kwargs):
        """
        This method should return data and HTTP Status Code of the operation that is needed to be performed.
        Parameters
        ----------
        serialized_data: serializer_class
            This is the serialized data that has been validated.
        args: tuple
            This contains extra positional arguments that can be sent upon call.
        kwargs: dict
            This contains key-value paired arguments that can be sent upon call.

        Returns
        -------
        data: dict
            This contains relevant information that will be returned after the operation has been performed
        status_code: int
            This will reflect the status code of the operation that has been performed.

        """
        raise NotImplementedError('The abstract method needs to be implemented')

    @csrf_exempt
    def post(self, request):
        serialized_data = self.serializer_class(data=request.data)
        if serialized_data.is_valid():
            data, status_code = self.validated(serialized_data=serialized_data)
            return JsonResponse(data, status=status_code)
        else:
            return JsonResponse(serialized_data.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    class Meta:
        abstract = True


class AddObjectView(ValidateAndPerformView):
    permission_classes = (IsAuthenticated, )

    def validated(self, serialized_data, *args, **kwargs):
        serialized_data = self.show_serializer(serialized_data.save(created_by=self.request.user))
        return serialized_data.data, status.HTTP_201_CREATED


class PaginatedSearchView(ValidateAndPerformView):
    renderer_classes = (JSONRenderer, )
    permission_classes = (IsAuthenticated, )

    def validated(self, serialized_data, *args, **kwargs):
        searched_data = self.show_serializer(self.model.objects.extra(where=serialized_data.data['where'],
                                                                      order_by=serialized_data.data['order_by']),
                                             many=True)
        return paginate_data(searched_data=searched_data, request_data=serialized_data), status.HTTP_202_ACCEPTED
