from rest_framework import serializers
from backend.models import System, User, Group, Tag, TagRelations

from collections import OrderedDict
# Non-field imports, but public API
from rest_framework.fields import (  # NOQA # isort:skip
    CreateOnlyDefault, CurrentUserDefault, SkipField, empty
)
from rest_framework.relations import PKOnlyObject  # NOQA # isort:skip

# all of these class serialize database data, so it can be returned to the frontend
# as JSON or other formats

# for serializing a system. only sends some of the system fields,
# will probably change later
class SystemSerializer(serializers.ModelSerializer):

    class Meta:
        model = System
        fields = ('serialnumber', 'companyname', 'systemname', 'osversion',
            'productfamily',)


# for serializing a user. does not send the password
class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('userid', 'username')


# for serializing a group
class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = ('groupid', 'groupname',)


# for serializing a tag
class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ('tagid', 'tagname',)

# class SystemTagListSerializer(serializers.ListSerializer):

#     def __init__(self, *args, **kwargs):
#         self.child = kwargs.pop('child', copy.deepcopy(self.child))
#         self.allow_empty = kwargs.pop('allow_empty', True)
#         assert self.child is not None, '`child` is a required argument.'
#         assert not inspect.isclass(self.child), '`child` has not been instantiated.'
#         super(ListSerializer, self).__init__(*args, **kwargs)
#         self.child.bind(field_name='', parent=self)


# for serializing all of a systems tags (plus the system info)
class SystemTagSerializer(serializers.ModelSerializer):
    groupid = serializers.SerializerMethodField()
    groupname = serializers.SerializerMethodField()
    tagids = serializers.SerializerMethodField()
    tagnames = serializers.SerializerMethodField()

    def __init__(self, instance=None, data=empty, **kwargs):
        self._group = kwargs.get('context').get('group')
        self._tags = Tag.objects.filter(groups=self._group, systems=instance)
        super(SystemTagSerializer, self).__init__(**kwargs)

    def get_groupid(self, obj):
        return self._group.groupid

    def get_groupname(self, obj):
        return self._group.groupname

    def get_tagids(self, obj):
        tagids = []
        for tag in self._tags:
            tagids = tagids + [tag.tagid]
        return tagids

    def get_tagnames(self, obj):
        tagnames = []
        for tag in self._tags:
            tagnames = tagnames + [tag.tagname]
        return tagnames

    def to_representation(self, instance):
        # ret = super(SystemTagSerializer, self).to_representation(instance)
        ret = OrderedDict()
        ret['groupid'] = 2
        return ret
    
    class Meta:
        model = System
        # list_serializer_class = SystemTagListSerializer
        fields = ('groupid','groupname','serialnumber', 'companyname', 'systemname',\
            'osversion', 'productfamily','tagids','tagnames')

# for serailizing all of a group's systems' tags. Serializes the information of
# each object
class GroupSystemTagSerializer(serializers.ModelSerializer):
    pass
#     systems = SystemTagSerializer(many=True, read_only=True)

#     class Meta:
#         model = Group
#         fields = ('groupid', 'groupname', 'systems',)
