import urllib
import urlparse

from django.template import (Library, loader, TemplateSyntaxError, Node,
                             Variable, VariableDoesNotExist)
from django.template.defaultfilters import escapejs
from django.utils.encoding import smart_str
from django.utils.safestring import mark_safe
from django.utils.html import escape

import jinja2
from jingo import register, env

from utils.helpers import get_random_string

from django.template.defaultfilters import \
     (addslashes, escapejs, fix_ampersands,
      floatformat, iriencode, linenumbers,
      slugify, truncatewords, truncatewords_html,
      urlencode, cut, rjust, ljust, linebreaks,
      linebreaksbr, removetags, unordered_list,
      date, time, timesince, timeuntil, yesno,
      pluralize, phone2numeric, capfirst)


for func in (addslashes, escapejs, fix_ampersands,
             floatformat, iriencode, linenumbers, 
             slugify, truncatewords, truncatewords_html,
             urlencode, cut, rjust, ljust, linebreaks,
             linebreaksbr, removetags, unordered_list,
             date, time, timesince, timeuntil, yesno,
             pluralize, phone2numeric,capfirst):        
        register.filter(func)
        


@jinja2.contextfunction
@register.function
def querystring(context, query):
    """
    Add paramaters to a query string. New params will be appended, duplicates will
    be overwritten.
    """
    
    # separate querystring from route
    url_parts = context['request'].get_full_path().split('?')
    
    #collect all querystring params
    qs = url_parts[1].split('&') if len(url_parts) == 2 else []
    for i in query.split('&'):
        qs.append(i)
    
    #mash them together into a dictionary
    query_dictionary = {}
    for (i,v) in enumerate( qs ):    
        parts = v.split('=')
        if( len(parts) == 2 ):
            query_dictionary[parts[0]] = parts[1]
            
    #convert dictionary to querystring with all params that have values
    qs = []
    for (k,v) in query_dictionary.items():
        if len(v) > 0:
            qs.append( k+'='+urllib.quote(str(v)) )
            
    return '&'.join(sorted(qs))
    

@register.function
def replace(item, value):
    """Replaces first part of ``value`` with the second one

    :param: value (string) list of 2 items separated by comma
    :result: (string) ``item`` with the first string replaced by the other
    """
    items = value.split(',')
    if len(items) != 2:
        raise TemplateSyntaxError(
                "Replace filter argument is a comma separated list of 2 items")
    return item.replace(items[0], items[1])



@jinja2.contextfunction
@register.function
def escape_template(context, template):
    t = env.get_template(template).render(context)
    return jinja2.Markup(escapejs(t))


@jinja2.contextfunction
@register.function
def safe_csrf_token(context):
    csrf_token = context.get('csrf_token', None)
    if csrf_token:
        if csrf_token == 'NOTPROVIDED':
            return mark_safe(u"")
        else:
            return mark_safe(u"<div style='display:none'>"
                    "<input type='hidden' name='csrfmiddlewaretoken' "
                    "value='%s' /></div>" % escape(csrf_token))
    else:
        # It's very probable that the token is missing because of
        # misconfiguration, so we raise a warning
        from django.conf import settings
        if settings.DEBUG:
            import warnings
            warnings.warn("A {% csrf_token %} was used in a template, "
                    "but the context did not provide the value.  "
                    "This is usually caused by not using RequestContext.")
        return u''


@register.function
def hashtag(length=10):
    """ return random string """
    return get_random_string(length)
   

def urlparams(url_, **query):
    """
    Update the parameters of a url and return it.
    """
    url = urlparse.urlparse(url_)
    query_string = querystring(url.query, **query)
    new = urlparse.ParseResult(url.scheme, url.netloc, url.path, url.params,
                               query_string, url.fragment)
    return new.geturl()


def urlencode(items):
    """A Unicode-safe URLencoder."""
    try:
        return urllib.urlencode(items)
    except UnicodeEncodeError:
        return urllib.urlencode([(k, smart_str(v)) for k, v in items])