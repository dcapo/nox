from tastypie.exceptions import Unauthorized
from tastypie.authorization import Authorization
from nox.models import Event, Post
import re

class BaseAuthorization(Authorization):
    def get_id(self, resource_name, resource_uri):
        id = re.findall("/" + resource_name + "/(\d+)/", resource_uri)
        if not id:
            raise Unauthorized("Error: failed to parse resource URI.")
        return id[0]
    
    def create_list(self, object_list, bundle):
        raise Unauthorized("Sorry, creating an entire list is not allowed.")

    def update_list(self, object_list, bundle):
        raise Unauthorized("Sorry, updating an entire list is not allowed.")

    def delete_list(self, object_list, bundle):
        raise Unauthorized("Sorry, deleting an entire list is not allowed.")

class EventAuthorization(BaseAuthorization):
    def read_list(self, object_list, bundle):
        return object_list.filter(users__id__exact=bundle.request.user.id)

    def read_detail(self, object_list, bundle):
        return bundle.request.user in bundle.obj.users.all()

    def create_detail(self, object_list, bundle):
        return True
        
    def delete_detail(self, object_list, bundle):
        return bundle.request.user in bundle.obj.users.all()
        
    def update_detail(self, object_list, bundle):
        return bundle.request.user in bundle.obj.users.all()

class PostAuthorization(BaseAuthorization):
    def read_list(self, object_list, bundle):
        events = bundle.request.user.invite_set.values('event_id')
        return object_list.filter(event__id__in=events)

    def read_detail(self, object_list, bundle):
        return bundle.request.user in bundle.obj.event.users.all()

    def create_detail(self, object_list, bundle):
        event_id = super(PostAuthorization, self).get_id("event", bundle.data.get("event"))
        event = Event.objects.get(id=event_id)
        user = bundle.request.user
        return user in event.users.all() and user.invite_set.get(event=event).rsvp

    def delete_detail(self, object_list, bundle):
        return bundle.request.user == bundle.obj.user

    def update_detail(self, object_list, bundle):
        raise Unauthorized("Sorry, updating a post is not allowed.")

class InviteAuthorization(BaseAuthorization):
    def read_list(self, object_list, bundle):
        events = bundle.request.user.invite_set.values('event_id')
        return object_list.filter(event__id__in=events)

    def read_detail(self, object_list, bundle):
        return bundle.request.user in bundle.obj.event.users.all()

    def create_detail(self, object_list, bundle):
        event_id = super(InviteAuthorization, self).get_id("event", bundle.data.get("event"))
        event = Event.objects.get(id=event_id)
        user = bundle.request.user
        return user in event.users.all() and (user.invite_set.get(event=event).rsvp or not bundle.data.get('rsvp'))

    def delete_detail(self, object_list, bundle):
        return bundle.request.user in bundle.obj.event.users.all()

    def update_detail(self, object_list, bundle):
        return bundle.request.user in bundle.obj.event.users.all()

# SubPost = comment, like, dislike
class SubPostAuthorization(BaseAuthorization):
    def read_list(self, object_list, bundle):
        events = bundle.request.user.invite_set.values('event_id')
        return object_list.filter(post__event__id__in=events)
        
    def read_detail(self, object_list, bundle):
        return bundle.request.user in bundle.obj.post.event.users.all()

    def create_detail(self, object_list, bundle):
        post_id = super(SubPostAuthorization, self).get_id("post", bundle.data.get("post"))
        post = Post.objects.get(id=post_id)
        user = bundle.request.user
        return user in post.event.users.all()

    def delete_detail(self, object_list, bundle):
        return bundle.request.user == bundle.obj.user

    def update_detail(self, object_list, bundle):
        raise Unauthorized("Sorry, updating is not allowed on this resource.")

