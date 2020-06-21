from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.authentication import TokenAuthentication

from django.shortcuts import render
from rest_framework.permissions import( AllowAny, IsAdminUser,IsAuthenticatedOrReadOnly,
                                        DjangoModelPermissions,DjangoModelPermissionsOrAnonReadOnly)
from .models import Customer, DataSheet, Profession, Documents
from .serializers import( CustomerSerializer, DataSheetSerializer,
                          ProfessionSerializer, DocumentsSerializer)
from rest_framework import viewsets
# Create your views here.
class CustomerViewSet(viewsets.ModelViewSet):
    serializer_class = CustomerSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter,OrderingFilter]
    filter_fields = ('name',)
    search_fields =('name','address')
    ordering_fields= ('id','name')
    authentication_classes = [TokenAuthentication,]


    #queryset = Customer.objects.all()
    # print("THIS IS REPR:",repr(CustomerSerializer))

    def get_queryset(self):
        address= self.request.query_params.get('address',None)
        # status= True if self.request.query_params['active']== 'True' else False
        if self.request.query_params.get('active')=='False':
            status=False
        else:
            status=True
        if address:
            customers= Customer.objects.filter(address__icontains=address, active= status)
        else:

            customers= Customer.objects.filter(active= status)

        return customers
    # def list(self, request, *args, **kwargs):
    #     customers= self.get_queryset()     #.filter(id=2)
    #     context = {'request': request}
    #     serializer= CustomerSerializer(customers, many=True, context=context)
    #     return Response(serializer.data)
    def retrieve(self, request, *args, **kwargs):

        obj= self.get_object()
        context = {'request': request}
        serializer=CustomerSerializer(obj, context=context)
        return Response(serializer.data)
    # def create(self, request, *args, **kwargs):
    #     data=request.data
    #     context = {'request': request}
    #     customer=Customer.objects.create(
    #         name=data['name'], address=data['address'], data_sheet_id=data['data_sheet']
    #
    #     )
    #     profession= Profession.objects.get(id=data['professions'])
    #     customer.professions.add(profession)
    #     customer.save()
    #     serializer= CustomerSerializer(customer,context=context)
    #     return Response(serializer.data)
    def update(self, request, *args, **kwargs):
        customer=self.get_object()
        data=request.data
        context = {'request': request}
        customer.name=data['name']
        customer.address=data['address']
        customer.data_sheet_id=data['data_sheet']

        profession=Profession.objects.get(id=data['professions'])
        for p in customer.professions.all():
            customer.professions.remove(p)


        customer.professions.add(profession)

        customer.save()
        serializer=CustomerSerializer(customer,context=context)
        return Response(serializer.data)
    def partial_update(self, request, *args, **kwargs):
        customer = self.get_object()
        context = {'request': request}
        customer.name=request.data.get('name',customer.name)
        customer.address = request.data.get('address', customer.address)
        customer.data_sheet_id = request.data.get('data_sheet', customer.data_sheet_id)
        customer.save()
        serializer = CustomerSerializer(customer, context=context)
        return Response(serializer.data)
    def destroy(self, request, *args, **kwargs):
        customer=self.get_object()
        customer.delete()
        return Response('Object deleted.')
    @action(detail=True)
    def deactivate(self,request, **kwargs):
        customer=self.get_object()
        context = {'request': request}
        customer.active=False

        customer.save()
        serializer = CustomerSerializer(customer, context=context)
        return Response(serializer.data)


    @action(detail=False)
    def deactivate_all(self, request, **kwargs):
        customers = self.get_queryset()
        context = {'request': request}
        customers.update(active=False)
        context = {'request': request}

        serializer = CustomerSerializer(customers,many=True, context=context)
        return Response(serializer.data)

    @action(detail=False)
    def activate_all(self, request, **kwargs):
        customers = self.get_queryset()
        context = {'request': request}
        customers.update(active=True)
        context = {'request': request}

        serializer = CustomerSerializer(customers, many=True, context=context)
        return Response(serializer.data)

    @action(detail=False, methods=['POST'])
    def change_status(self, request, **kwargs):

        status=false if request.data['active'] =='false' else True
        context = {'request': request}
        customers=Customer.objects.all()
        customers.update(active= status)

        serializer= CustomerSerializer(customers, many=True, context=context)
        return Response(serializer.data)


class DataSheetViewSet(viewsets.ModelViewSet):
    queryset = DataSheet.objects.all()
    serializer_class = DataSheetSerializer
    permission_classes = [AllowAny, ]

class ProfessionViewSet(viewsets.ModelViewSet):
    queryset = Profession.objects.all()
    serializer_class = ProfessionSerializer
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAdminUser, ]
class DocumentsViewSet(viewsets.ModelViewSet):
    queryset = Documents.objects.all()
    serializer_class = DocumentsSerializer
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly, ]



# Create your views here.
