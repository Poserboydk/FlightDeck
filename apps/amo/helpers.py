import commonware.log
import urllib2

from django.conf import settings
from lxml import etree

from utils.amo import AMOOAuth

log = commonware.log.getLogger('f.amo')


def get_addon_amo_api_url(id, file_id):
    """provides URL for AMO addon info API

    :attr: id (int) add-on's id in AMO
    :attr: file_id (int) version identified by file id in AMO
    """
    url = "%s://%s/api/%s/addon/%d" % (
        settings.AMOAPI_PROTOCOL, settings.AMOAPI_DOMAIN,
        settings.AMOAPI_VERSION, id)
    # XXX: wait until this will be supported by AMO API
    # BUG 690336
    #if file_id:
    #    url = "%s/%d" % (url, file_id)
    return url


def get_addon_details(amo_id, amo_file_id=None):
    """Pull metadata from AMO using `generic AMO API
    <https://developer.mozilla.org/en/addons.mozilla.org_%28AMO%29_API_Developers%27_Guide/The_generic_AMO_API>`_

    :attr: amo_id (int) id of the add-on in AMO
    :attr: amo_file_id (int) id of the file uploaded to AMO
    :returns: dict
    """
    url = get_addon_amo_api_url(amo_id, amo_file_id)
    log.debug("AMOAPI: receiving add-on info from \"%s\"" % url)
    req = urllib2.Request(url)
    try:
        page = urllib2.urlopen(req, timeout=settings.URLOPEN_TIMEOUT)
    except urllib2.HTTPError, error:
        if '404' in str(error):
            return {'deleted': True}
    except Exception, error:
        msg = "AMOAPI: ERROR receiving add-on info from \"%s\"%s%s"
        log.critical(msg % (url, '\n', str(error)))
        return {'error': msg % (url, ' : ', str(error))}
    amo_xml = etree.fromstring(page.read())
    amo_data = {}
    for element in amo_xml.iter():
        if element.tag in ('status', 'rating', 'version', 'slug'):
            amo_data[element.tag] = element.text
        if element.tag == 'status':
            amo_data['status_code'] = int(element.get('id'))
    # return dict
    return amo_data


def fetch_amo_user(email):
    log.debug('#'*80)
    amo = AMOOAuth(domain=settings.AMOOAUTH_DOMAIN,
                   port=settings.AMOOAUTH_PORT,
                   protocol=settings.AMOOAUTH_PROTOCOL,
                   prefix=settings.AMOOAUTH_PREFIX)
    amo.set_consumer(consumer_key=settings.AMOOAUTH_CONSUMERKEY,
                     consumer_secret=settings.AMOOAUTH_CONSUMERSECRET)
    return amo.get_user_by_email(email) or None
