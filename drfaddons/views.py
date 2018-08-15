from rest_framework.views import APIView


def get_user(email: str, mobile: str, name: str=None):
    """
    This function will return the user with the given mobile number and
    if no such user exists then it will return the user with the given email address
    and even if no such user exists then it will create a new user with the provided details and will return it.
    Parameters
    ----------
    email: str
        EMail of the user
    mobile: str
        Mobile number of the user
    name: str
        Name of the user
        Default value is None
    """
    from django.contrib.auth import get_user_model

    User = get_user_model()

    try:
        user = User.objects.get(mobile=mobile)
    except User.DoesNotExist:
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user = User.objects.create_user(username=mobile, email=email, mobile=mobile, name=name, is_active=True,
                                            password=User.objects.make_random_password())
    return user


class ValidateAndPerformView(APIView):
    """
    An abstract class that provides a APIView in various projects for easily doing certain tasks.
    Checks the validation with serializer_class and calls validated.
    Was created by me not knowing about GenericAPIView.
    May be labelled as deprecated and get removed in future versions.

    Source: Himanshu Shankar (https://github.com/iamhssingh)
    """
    from django.views.decorators.csrf import csrf_exempt
    from rest_framework.permissions import AllowAny
    from rest_framework.renderers import JSONRenderer

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
        from .add_ons import JsonResponse
        from rest_framework import status

        serialized_data = self.serializer_class(data=request.data)
        if serialized_data.is_valid():
            data, status_code = self.validated(serialized_data=serialized_data)
            return JsonResponse(data, status=status_code)
        else:
            return JsonResponse(serialized_data.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    class Meta:
        abstract = True


class AddObjectView(ValidateAndPerformView):
    """
    Creates or updates an object.
    Used in various projects by only specifying a few variables.
    Was created by me not knowing about GenericAPIView.
    May be labelled as deprecated and get removed in future versions.

    Source: Himanshu Shankar (https://github.com/iamhssingh)
    """
    from django.views.decorators.csrf import csrf_exempt
    from rest_framework.permissions import IsAuthenticated

    permission_classes = (IsAuthenticated,)

    def validated(self, serialized_data, *args, **kwargs):
        from rest_framework import status

        serialized_data = self.show_serializer(serialized_data.save(created_by=self.request.user))
        return serialized_data.data, status.HTTP_201_CREATED

    @csrf_exempt
    def post(self, request):
        from .add_ons import JsonResponse
        from rest_framework import status

        if 'id' in request.data.keys():
            try:
                serialized_data = self.serializer_class(self.model.objects.get(pk=request.data['id']),
                                                        data=request.data)
            except self.model.DoesNotExist:
                data = {'id': ["Object with provided ID does not exists"]}
                return JsonResponse(data, status=status.HTTP_404_NOT_FOUND)
        else:
            serialized_data = self.serializer_class(data=request.data)
        if serialized_data.is_valid():
            data, status_code = self.validated(serialized_data=serialized_data)
            return JsonResponse(data, status=status_code)
        else:
            return JsonResponse(serialized_data.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    class Meta:
        abstract = True


class PaginatedSearchView(ValidateAndPerformView):
    """
    Provides querying via POST method along with Paginated View.
    Used in various projects by only specifying a few variables.
    Was created by me not knowing about GenericAPIView.
    May be labelled as deprecated and get removed in future versions.

    Source: Himanshu Shankar (https://github.com/iamhssingh)
    """
    from rest_framework.permissions import IsAuthenticated

    permission_classes = (IsAuthenticated, )

    def fetch_data(self, serialized_data):
        raise NotImplementedError('Implement Fetch Data')

    def validated(self, serialized_data, *args, **kwargs):
        from .add_ons import paginate_data
        from rest_framework import status

        searched_data = self.show_serializer(
            self.fetch_data(serialized_data).order_by(serialized_data.data['order_by'][0]), many=True)
        return paginate_data(searched_data=searched_data, request_data=serialized_data), status.HTTP_202_ACCEPTED

    class Meta:
        abstract = True
