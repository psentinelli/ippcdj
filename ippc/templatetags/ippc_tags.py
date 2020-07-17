from django import template  
#from django.template import Library, Node

#from django.db.models import get_model
#from django.apps import get_model 
from .translate_tags import get_object_translation
from django.shortcuts import get_object_or_404

import os.path
from ippc.models import CommentFile,CountryPage,IppcUserProfile
from django.utils.html import format_html
 
from django.contrib.auth.models import User
from myzzz.settings import   MEDIA_URL 

register = template.Library()

@register.simple_tag
def get_comment_file(id):
      print(id)
      file = CommentFile.objects.filter(comment_id=id)
      if file.count()>0:
        for f in file:
            return format_html( '<i class="icon-file">&#160;</i><a href="'+MEDIA_URL+f.file.name+'">'+os.path.basename(f.file.name)+'</a>')
      else:
        return   ''






def _render_nodelist_items(nodelist, context, result=None):
    if result is None:
        result = []
    for node in nodelist:
        if not isinstance(node, template.Node):
            result.append(node)
        else:
            try:
                result.append(nodelist.render_node(node, context))
            except:
                # get the wrapped exception if settings.DEBUG is True
                #if hasattr(ex, 'exc_info'):
                #    ex = ex.exc_info[1]
                # let every exception other than StopLoopException propagate
               # if not isinstance(ex, StopLoopException):
                #    raise
                # reraise the StopLoopException with the updated nodelist
                #if ex.nodelist:
                  #  result.extend(ex.nodelist)
                #ex.nodelist = result
                #raise StopLoopException
                print()
    return result

# http://www.b-list.org/weblog/2006/jun/07/django-tips-write-better-template-tags/     
class LatestContentNode(template.Node):
    """
    Template tag, which lets us fetch any number of objects 
    from any installed model and store them in any 
    context variable we want. 
     
    Call it like this:

    {% get_latest ApplicationName.ModelName 5 as some_variable_name %}

    Eg1:

    {% get_latest weblog.Entry 10 as latest_entries %}

    Eg2:

    {% get_latest comments.Comment 5 as recent_comments %}
    
    """
    def __init__(self, model, num, varname):
        self.num, self.varname = num, varname
        #self.model = get_model(*model.split('.'))
    
    def render(self, context):
        # status=2 means only show entries that are not marked as draft in Mezzanine Displayable core model
          
        context[self.varname] = self.model._default_manager.filter(status=2)[:self.num]
        return ''
 
def get_latest(parser, token):
    bits = token.contents.split()
    if len(bits) != 5:
        raise TemplateSyntaxError#, "get_latest tag takes exactly four arguments"
    if bits[3] != 'as':
        raise TemplateSyntaxError#, "third argument to get_latest tag must be 'as'"
    return LatestContentNode(bits[1], bits[2], bits[4])
    
get_latest = register.tag(get_latest)



from mezzanine.pages.models import Page, RichTextPage
from mezzanine.core.templatetags.mezzanine_tags import richtext_filters
from ippc.templatetags.ippc_tags import get_object_translation
from ippc.models import TransRichTextPage
# http://stackoverflow.com/a/13927772
# show specific page in template
@register.simple_tag
def get_page(slug, attr):
    # page = richtext_filter(get_object_translation(getattr(RichTextPage.objects.get(pk=int(pk)), attr)))
    page = get_object_translation(RichTextPage.objects.get(slug=slug))
    return richtext_filters(page.content)

# https://groups.google.com/forum/#!topic/mezzanine-users/UJsHUtv8FUg
# http://stackoverflow.com/questions/4577513/how-do-i-change-a-django-template-based-on-the-users-group#answer-8826722
# https://github.com/lukaszb/django-guardian
# @register.filter
# def can_view(user, page):
#     content_model = page.get_content_model()
#     return user.has_perm('can_view', content_model)

@register.simple_tag
def get_latest_cns():
    """
    Put a list of recently published get_latest_cns   into the template
    context. 

    Usage::

        {% get_latest_cns 5 as cns %}
     
    """
    latestcns = CountryPage.objects.filter(status=2)
    return list(latestcns)

@register.simple_tag
def get_profile_usr(id):
    user_obj=User.objects.get(id=id)
    useprofile=get_object_or_404(IppcUserProfile,user_id=user_obj.id)
    return  useprofile

