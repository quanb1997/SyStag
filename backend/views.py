import os
import requests

from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.decorators import api_view
from rest_framework.response import Response
# from rest_framework.views import APIView
from rest_framework import mixins, status
from rest_framework import generics, permissions, viewsets
import os
import requests

from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.decorators import api_view, detail_route, list_route
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.response import Response
# from rest_framework.views import APIView
from rest_framework import mixins, status, generics, permissions, viewsets, filters
from django.contrib.auth import get_user_model
from django.views.generic import View
from django.conf import settings
from operator import itemgetter
from collections import OrderedDict
import django.apps
from itertools import chain
import re

from backend.models import System, Group, Tag, User, GroupUsers, GroupSystems, \
    TagRelations, MEMBER, ADMIN, OWNER, MYSYSTEMS

from backend.serializers import SystemSerializer, UserSerializer, GroupSerializer
from backend.serializers import SystemTagSerializer, TagSerializer, GroupSystemTagSerializer
from backend.permissions import IsOwnerOrReadOnly
from backend import apps

# Create your views here.

# deals with retrieving systems from, adding systems to, and removing systems 
# from a group
class GroupSystemsViewSet(viewsets.GenericViewSet):
    queryset = Group.objects.all()
    serializer_class = SystemTagSerializer

    # def get_serializer_context(self):
    #     """
    #     Extra context provided to the serializer class.
    #     """
    #     context = super(GroupSystemsViewSet, self).get_serializer_context()
    #     context['group'] = self._group
    #     return context

    def list(self, request, *args, **kwargs):
        groupid = request.GET.get('id')
        self._group = self.queryset.get(pk=groupid)
        systems = System.objects.filter(groups=self._group)
        # serializer = self.get_serializer(systems)
        # group = self.get_serializer_context()['user']
        # return Response(UserSerializer(group).data)
        # time for brute force, from django rest framework
        group_info = []
        for system in systems:
            ret = OrderedDict()
            ret['groupid'] = self._group.groupid
            ret['groupname'] = self._group.groupname
            ret['serialnumber'] = system.serialnumber
            ret['companyname'] = system.companyname
            ret['systemname'] = system.systemname
            ret['osversion'] = system.osversion
            ret['productfamily'] = system.productfamily
            tagids = []
            tagnames = []
            tags = Tag.objects.filter(groups=self._group, systems=system)
            for tag in tags:
                tagids += [tag.tagid]
                tagnames += [tag.tagname]
            ret['tagids'] = tagids
            ret['tagnames'] = tagnames
            group_info += [ret] 
        return Response(group_info)

    def post(self, request, *args, **kwargs):
        groupid = request.data['GrpID']
        self._group = self.queryset.get(pk=groupid)
        if not GroupUsers.objects.filter(groupid=self._group,userid=request.user,\
            admin__in=[ADMIN, OWNER]):
            return Response({'message':\
                'You do not have permission to add systems to this group'},\
                status=status.HTTP_403_FORBIDDEN)
        sysids = request.data['SysIDList']
        systems = System.objects.filter(pk__in=sysids)
        GroupSystems.objects.bulk_create(\
            [GroupSystems(serialnumber=system, groupid=self._group) for system in systems])
        # serializer = self.get_serializer(self._group, many=True)
        # return Response(serializer.data)
        return Response()

    def delete(self, request, *args, **kwargs):
        groupid = request.data['GrpID']
        self._group = self.queryset.get(pk=groupid)
        if not GroupUsers.objects.filter(groupid=self._group,userid=request.user,\
            admin__in=[ADMIN, OWNER]):
            return Response({'message':\
                'You do not have permission to remove systems from this group'},\
                status=status.HTTP_403_FORBIDDEN)
        sysids = request.data['SysIDList']
        groupsystems = GroupSystems.objects.filter(serialnumber__in=sysids)\
            .filter(groupid=groupid)
        # might need this to get rid of excess tags in a group
        # tagrelations = TagRelations.objects.filter(userid=request.user,\
        #     serialnumber__pk__in=sysids,groupid=group)
        for groupsystem in groupsystems:
            groupsystem.delete()
        # serializer = self.get_serializer(self._group, many=True)
        # return Response(serializer.data)
        return Response()

# added this class based view instead of function based
class GroupViewSet(viewsets.GenericViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

    def list(self, request, *args, **kwargs):
        # need to change 'norsanar' back to request.user.username'
        usergroups = self.queryset.filter(users__username__exact=request.user.username)\
            .exclude(groupusers__admin__exact=MYSYSTEMS)
        serializer = self.get_serializer(usergroups, many=True)
        return Response(serializer.data)

    # request should put groupname in Name, users in UsrIDList,
    # and systems in SysIDList. Maybe the creator shouldn't be included in
    # UsrIDList, but instead we just group it from the authenticated request. 
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data={'groupname':request.data['Name']})
        if serializer.is_valid():
            group = serializer.create(serializer.validated_data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        # creator should be first user
        if 'UsrIDList' in request.data:
            users = User.objects.filter(pk__in=request.data['UsrIDList'])
            GroupUsers.objects.bulk_create(
                [GroupUsers(userid=users[0], groupid=group, admin=OWNER)] +
                [GroupUsers(userid=user, groupid=group, admin=MEMBER) for user in users[1:]])
        if 'SysIDList' in request.data:
            systems = System.objects.filter(pk__in=request.data['SysIDList'])
            GroupSystems.objects.bulk_create(
                [GroupSystems(serialnumber=system, groupid=group) for system in systems])
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    # group that we are editing in GrpID, new owner in newOwn
    def put(self, request, *args, **kwargs):
        group = self.queryset.get(pk=request.data['GrpID'])
        owner = GroupUsers.objects.filter(groupid__groupid__exact=request.data['GrpID'],
            userid__username__exact=request.user.username)
        newowner = GroupUsers.objects.filter(groupid__groupid__exact=request.data['GrpID'],
            userid__username__exact=request.data['NewOwn'])
        if len(owner) and owner[0].admin == OWNER:
            owner[0].admin = MEMBER
            owner[0].save()
            if not len(newowner):
                newowner = GroupUsers(groupid=group,userid=User.objects\
                    .filter(username=request.data['NewOwn'])[0],admin=OWNER)
            else:
                newowner = newowner[0]
                newowner.admin = OWNER
            newowner.save()
            return Response({'message':'owner changed'})
        else:
            return Response({'message':'user does not exist'},
                status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        groups = self.queryset.filter(pk__in=request.data['GrpIDList'],
            users__username__exact=request.user.username, groupusers__admin__exact=OWNER)
        if not len(groups):
            return Response({'message':'no groups were deleted'},
                status=status.HTTP_400_BAD_REQUEST)
        else:
            for group in groups:
                group.delete()
            return Response({'message':'groups deleted'})


# deals with creating, adding, and removing tags to/from a system
class GroupTagViewSet(viewsets.GenericViewSet):
    queryset = Tag.objects.all()
    serializer = TagSerializer

    def list(self, request, *args, **kwargs):
        groupid = request.GET.get('GrpID')
        tagname = self.request.GET.get('TagNm')
        sysid = self.request.GET.get('SysID')
        tag = self.queryset.filter(tagname=tagname, users=request.user, groups__pk=groupid)
        privacy = self.request.GET.get('Privacy')
        # if not GroupSystems.objects.filter(groupid__pk=groupid,serialnumber__pk=sysid)
        if len(tag)>1:
            return Response({'message':'there should not be multiple tags'+
                ' belonging to the same user and group'})
        elif not tag:
            tag = Tag(tagname=tagname,public=privacy)
            tag.save()
        elif not tag.exclude(systems__pk=sysid):
            return Response({'message':'the system is already tagged with that string'})
        else:
            tag = tag[0]
        group = Group.objects.get(pk=groupid)
        system = System.objects.get(pk=sysid)
        tagrelations = TagRelations(tagid=tag,serialnumber=system,groupid=group,\
            userid=request.user)
        tagrelations.save()
        return Response({'message':'system has been tagged'})

    def post(self, request, *args, **kwargs):
        groupid = request.data['GrpID']
        tagname = self.request.data['TagNm']
        sysid = self.request.data['SysID']
        tag = self.queryset.filter(tagname=tagname, users=request.user, groups__pk=groupid)
        privacy = self.request.data['Privacy']
        # if not GroupSystems.objects.filter(groupid__pk=groupid,serialnumber__pk=sysid)
        if len(tag)>1:
            return Response({'message':'there should not be multiple tags'+
                ' belonging to the same user and group'})
        elif not tag:
            tag = Tag(tagname=tagname,public=privacy)
            tag.save()
        elif not tag.exclude(systems__pk=sysid):
            return Response({'message':'the system is already tagged with that string'})
        else:
            tag = tag[0]
        group = Group.objects.get(pk=groupid)
        system = System.objects.get(pk=sysid)
        tagrelations = TagRelations(tagid=tag,serialnumber=system,groupid=group,\
            userid=request.user)
        tagrelations.save()
        return Response({'message':'system has been tagged'})

    def put(self, request, *args, **kwargs):
        groupid = request.data['GrpID']
        sysid = self.request.data['SysID']
        privacy = self.request.data['Privacy']
        tagids = self.request.data['TagIDList']
        tags = self.queryset.filter(groups__groupid=groupid,systems__serialnumber=sysid\
            ,users=request.user,pk__in=tagids).exclude(public=privacy)
        tags.public = privacy
        tags.save()
        return Response({'message':'tags privacy changed'})
        
    def delete(self, request, *args, **kwargs):
        groupid = request.data['GrpID']
        group = Group.objects.get(pk=groupid)
        sysid = self.request.data['SysID']
        tagids = self.request.data['TagIDList']
        tags = self.queryset.filter(groups__groupid=groupid,systems__serialnumber=sysid\
            ,users=request.user,pk__in=tagids)
        for tag in tags:
            tag.delete()
        return Response({'message':'tags deleted'})


# makes the delete request a get request instead (holds the delete method of the
# GroupTagViewset)
class GroupTagDeleteViewSet(viewsets.GenericViewSet):
    queryset = Tag.objects.all()
    serializer = TagSerializer
        
    def list(self, request, *args, **kwargs):
        groupid = request.GET.get('GrpID')
        group = Group.objects.get(pk=groupid)
        tagids = re.findall('&TagIDList\[\]=([0-9]+)',request.get_full_path())
        tagids = [int(tagid) for tagid in tagids]
        sysid = self.request.GET.get('SysID')
        tags = self.queryset.filter(groups__groupid=groupid,systems__serialnumber=sysid\
            ,users=request.user,pk__in=tagids)
        for tag in tags:
            tag.delete()
        return Response({'message':'tags deleted'})


# view that adds or removes users from a group. can also change admins or list systems
# might want to add a method to demote admins.
class GroupUserViewSet(viewsets.GenericViewSet):
    queryset = Group.objects.all()
    serializer_class = UserSerializer

    def list(self, request, *args, **kwargs):
        groupid = request.GET.get('GrpID')
        users = User.objects.filter(groups__groupid=groupid)
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        groupid = request.data['GrpID']
        usernames = request.data['UsrNmList']
        if not GroupUsers.objects.filter(groupid__groupid=groupid,userid=request.user,\
            admin__in=[ADMIN,OWNER]):
            return Response(\
                {'message':'you do not have permission to add users to this group'})
        users = User.objects.filter(username__in=usernames).exclude(groupid__groupid=groupid)
        if not users:
            return Response({'message':'all listed users already in group'})
        group = self.queryset.get(pk=groupid)
        GroupUsers.objects.bulk_create(
            [GroupUsers(userid=user, groupid=group, admin=MEMBER) for user in users])
        return Response({'message':'users successfully added to group'})

    def put(self, request, *args, **kwargs):
        groupid = request.data['GrpID']
        userids = request.data['UsrIDList']
        if not GroupUsers.objects.filter(groupid__groupid=groupid,userid=request.user,\
            admin__in=[ADMIN,OWNER]):
            return Response(\
                {'message':'you do not have permission to add admins to this group'})
        usersingroup = GroupUser.objects.filter(userid__pk__in=userids,groupid__pk=groupid)
        usersingroup.update(admin=ADMIN)
        group = self.queryset.get(pk=groupid)
        users = User.objects.filter(pk__in=userids).exclude(groups__pk=groupid)
        for user in users:
            GroupUsers.objects.bulk_create(
                [GroupUsers(userid=user, groupid=group, admin=ADMIN) for user in users])
        return Response({'message':'admins successfully added to group'})

    def delete(self, request, *args, **kwargs):
        groupid = request.data['GrpID']
        userids = request.data['UsrIDList']
        if not GroupUsers.objects.filter(groupid__groupid=groupid,userid=request.user,\
            admin__in=[ADMIN,OWNER]):
            return Response(\
                {'message':'you do not have permission to remove users from this group'})
        groupusers = GroupUsers.objects.filter(groupid__groupid=groupid,\
            userid__username__in=usernames).exclude(userid=user,admin=OWNER)
        for user in groupusers:
            user.delete()
        return Response({'message':'users successfully removed from group'})


# view that adds or removes systems to and from mysystems. It can also list the systems
class MySystemsViewSet(viewsets.GenericViewSet):
    queryset = System.objects.all()
    serializer_class = SystemTagSerializer

    def list(self, request, *args, **kwargs):
        self._group = Group.objects.filter(users=request.user,\
            groupusers__admin=MYSYSTEMS)[0]
        systems = self.queryset.filter(groups=self._group)
        # time for brute force, from django rest framework
        group_info = []
        for system in systems:
            ret = OrderedDict()
            ret['groupid'] = self._group.groupid
            ret['groupname'] = self._group.groupname
            ret['serialnumber'] = system.serialnumber
            ret['companyname'] = system.companyname
            ret['systemname'] = system.systemname
            ret['osversion'] = system.osversion
            ret['productfamily'] = system.productfamily
            tagids = []
            tagnames = []
            tags = Tag.objects.filter(groups=self._group, systems=system)
            for tag in tags:
                tagids += [tag.tagid]
                tagnames += [tag.tagname]
            ret['tagids'] = tagids
            ret['tagnames'] = tagnames
            group_info += [ret] 
        return Response(group_info)


    def post(self, request, *args, **kwargs):
        self._group = Group.objects.filter(users=request.user,\
            groupusers__admin=MYSYSTEMS)[0]
        sysids = request.data['SysIDList']
        systems = System.objects.filter(pk__in=sysids)
        GroupSystems.objects.bulk_create(\
            [GroupSystems(serialnumber=system, groupid=self._group) for system in systems])
        # serializer = self.get_serializer(self._group, many=True)
        # return Response(serializer.data)
        return Response()

    def delete(self, request, *args, **kwargs):
        self._group = Group.objects.filter(users=request.user,\
            groupusers__admin=MYSYSTEMS)[0]
        sysids = request.data['SysIDList']
        groupsystems = GroupSystems.objects.filter(serialnumber__in=sysids)\
            .filter(groupid=groupid)
        # might need this to get rid of excess tags in a group
        # tagrelations = TagRelations.objects.filter(userid=request.user,\
        #     serialnumber__pk__in=sysids,groupid=group)
        for groupsystem in groupsystems:
            groupsystem.delete()
        # serializer = self.get_serializer(self._group, many=True)
        # return Response(serializer.data)
        return Response()


# lists the field names of a model.
class FieldsViewSet(viewsets.GenericViewSet):
    queryset = System.objects.all()
    serializer_class = SystemSerializer

    def list(self, request, *args, **kwargs):
        modelname = request.GET.get('Model')
        models = []
        for model in django.apps.apps.get_models():
            if model.__name__ == modelname:
                models += [model]
        if len(models) > 1:
            return Response({'message':'more than one model matches your request'})
        elif len(models) < 1:
            return Response({'message':'no models match your request'})
        else:
            # from the django documentation:
            # https://docs.djangoproject.com/en/2.0/ref/models/meta/
            fieldnames = list(set(chain.from_iterable(
                (field.name, field.attname) if hasattr(field, 'attname') else (field.name,)
                for field in models[0]._meta.get_fields()
                # For complete backwards compatibility, you may want to exclude
                # GenericForeignKey from the results.
                if not (field.many_to_one and field.related_model is None)
            )))
            return Response({'fields':fieldnames})


# searches the database for the search term (q), searching by the attribute 'type'
class SearchViewSet(viewsets.GenericViewSet):
    queryset = System.objects.all()
    serializer_class = SystemSerializer

    def list(self, request, *args, **kwargs):
        searchterm = request.GET.get('SrchTerm')
        searchtype = request.GET.get('SrchType')
        if searchtype == 'tags':
            Systems = self.queryset.filter(tags__tagname=searchterm)
        else:
            Systems = self.queryset.filter(**{searchtype:searchterm})
        searchresult = self.get_serializer(instance=Systems, many=True).data
        return Response(searchresult)

# @api_view(['GET'])
# def search(request): #Nate
#     searchterm = request.GET.get('SrchTerm')
#     searchtype = request.GET.get('SrchType')
#     Systems = System.objects.filter(**{searchtype:searchterm})
#     searchresult = SystemSerializer(instance=Systems, many=True).data
#     return Response(searchresult)

# When passed a list of systems, will remove any systems that don't match filter,
# and will have the option to provide category to sort them by (Default None).
# Params: systems = list of systems (nested list)
# filt = specific value of a system to filter on
# category = index within the system list to be sorted by
def filter_systems(systems, filt, category=None): #Nate
    for s in systems:
        if not s.contains(filt):
            systems.remove(s)
    if(category != None):
        systems = sorted(systems, key=itemgetter(category))
    return systems

# Returns list of possible filters
def filters(): #Nate
    filters = apps.filterOptions.get_filters()
    #filters = System.objects
    return filters

def create_filter(new_filter): #Nate
    apps.filterOptions.create_filter(new_filter)

def group_users(request):
    pass

def group_tag(request):
    pass

def systems(request):
    pass

#Jacob's Method 3.1.19
def my_systems():
    #for s in 
    pass

    
#Jacob's Method  3.1.20
def add_my_system(request,SysIDList):
    if request.method == 'POST':
        pass
    if request.method == 'DELETE':
        rm_my_system(SysIDList)
    
#Jacob's Method 3.1.21
def rm_my_system(SysIDList):
    pass

'''3.1.7 Quan'''
def remove_group_system(GrpID, SysIDList):
    pass

'''3.1.8 Quan'''
def add_user(GrpID, SysIDList):
    pass

'''3.1.9 Quan'''
def remove_user(GrpID, UsrIDLIst):
    pass

def group_users(request):
    if request.method == 'POST' :
        add_user()
        return Response(status=status.HTTP_201_CREATED)
    elif request.method == 'DELETE' :
        remove_user()
        return Response(status=status.HTTP_205_RESET_CONTENT)

# Adds new tag to the Tag table of the database with the desired info
def create_tag(request):
    if request.method == 'POST':
        serializer = TagSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

'''3.1.11 Quan'''
def change_tag_privacy(GrpID, SysID, TagIDList):
    pass

#Deletes tag from the Tag table in database (if it exists).
def delete_tag(request, pk):
    try:
        tag = Tag.objects.get(pk=pk)
    except Tag.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'DELETE':
        tag.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

def group_tag(request):
    if request.method == 'POST':
        return create_tag(request)
    elif request.method == 'PUT':
        return change_tag_privacy(request)
    elif request.method == 'DELETE':
        return delete_tag(request)

def index(request):
    teapot = requests.get('http://httpbin.org/status/418')
    weather = requests.get('http://api.openweathermap.org/data/2.5/weather?q=Amherst&APPID=2487d20f1f2ff3551ff350b050285683')
    time = requests.get('https://now.httpbin.org')
    print(teapot.text)
    print(weather.text)
    times= int(os.environ.get('TIMES', 1))
    return HttpResponse(('                                   SyStag' +
'<pre>' + teapot.text + '</pre>' +
'</br> WEATHER: ' +
'<pre>' + weather.text + '</pre>' +
'</br> TIME: ' +
'<pre>' + time.text + '</pre>' +
'</br> Hello from Quan, Nate, Jacob, and Tristan @TuneSquad!!!') * times +
'<pre>' + '<form method="get" action="/mysys/">' +
'<button type="submit">To mysys</button>' + '</form>')
    #return render(request, 'index.html')

# I don't know what this does
# def db(request):
#
#     greeting = Greeting()
#     greeting.save()
#
#     greetings = Greeting.objects.all()
#
#     return render(request, 'db.html', {'greetings': greetings})

# serves the homepage from the REACT frontend
class ReactAppView(View):

    def get(self, request):
        try:

            with open(os.path.join(settings.REACT_APP, 'build', 'index.html')) as file:
                return HttpResponse(file.read())

        except :
            return HttpResponse(
                """
                index.html not found ! build your React app !!
                """,
                status=501,
            )

# searches the database for the search term (q), searching by the attribute 'type'
def mysys(request):
    searchterm = request.GET.get('q')
    searchtype = request.GET.get('type')
    searchresult = []
    try:
        Systems = System.objects.filter(**{searchtype:searchterm})
        searchresult = SystemSerializer(instance=Systems, many=True).data
    except:
        pass
    return render(request, 'mysys.html', {'system_list':searchresult,'search':searchterm,
        'model_fields':System._meta.get_fields(),'searchtype':searchtype})


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


# class UserList(generics.ListAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer


# class UserDetail(generics.RetrieveAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer


class SystemViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    Additionally we also provide an extra `highlight` action.
    """
    queryset = System.objects.all()
    serializer_class = SystemSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,)

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(SystemViewSet, self).dispatch(request, *args, **kwargs)
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


# these are class based views
#
# class SystemList(generics.ListCreateAPIView):
#     """
#     List all Systems, or create a new System.
#     """
#     permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
#     queryset = System.objects.all()
#     serializer_class = SystemSerializer
#     def perform_create(self, serializer):
#         serializer.save(owner=self.request.user)
#
#
# class SystemDetail(generics.RetrieveUpdateDestroyAPIView):
#     """
#     Retrieve, update or delete a system.
#     """
#     permission_classes = (permissions.IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly,)
#     queryset = System.objects.all()
#     serializer_class = SystemSerializer


# these are function based views, they do the same thing that the above views do
#
# @api_view(['GET', 'POST'])
# def system_list(request, format=None):
#     """
#     List all Systems, or create a new System.
#     """
#     if request.method == 'GET':
#         systems = System.objects.all()
#         serializer = SystemSerializer(systems, many=True)
#         return Response(serializer.data)
#
#     elif request.method == 'POST':
#         serializer = SystemSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
# @api_view(['GET', 'PUT', 'DELETE'])
# def system_detail(request, pk, format=None):
#     """
#     Retrieve, update or delete a system.
#     """
#     try:
#         system = System.objects.get(pk=pk)
#     except System.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)
#
#     if request.method == 'GET':
#         serializer = SystemSerializer(system)
#         return Response(serializer.data)
#
#     elif request.method == 'PUT':
#         serializer = SystemSerializer(system, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     elif request.method == 'DELETE':
#         system.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

# Create your views here.
