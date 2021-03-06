import commonware

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models

from amo.helpers import fetch_amo_user
from person.managers import ProfileManager

log = commonware.log.getLogger('f.profile.models')


class Limit(models.Model):
    email = models.CharField(max_length=255)


class Profile(models.Model):
    user = models.ForeignKey(User, unique=True)
    nickname = models.CharField(max_length=255, blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    occupation = models.CharField(max_length=255, blank=True, null=True)
    homepage = models.CharField(max_length=255, blank=True, null=True)
    photo = models.CharField(max_length=255, blank=True, null=True)

    objects = ProfileManager()

    def get_name(self):
        if not (self.user.first_name or self.user.last_name or self.nickname):
            return self.user.username
        return self.get_fullname()

    def get_fullname(self):
        name = self.user.first_name if self.user.first_name else None
        if self.user.last_name:
            name = '%s %s' % (name, self.user.last_name) \
                    if name else self.user.last_name
        if not name and self.nickname:
            return self.nickname
        return name

    def get_nickname(self):
        " return nickname or username if no nickname "
        return self.nickname or self.user.username

    def __unicode__(self):
        return self.get_name()

    def get_addons_url(self):
        #return reverse('jp_browser_user_addons', args=[self.get_nickname()])
        return reverse('jp_browser_user_addons', args=[self.user.username])

    def get_libraries_url(self):
        #return reverse('jp_browser_user_libraries', args=[self.get_nickname()])
        return reverse('jp_browser_user_libraries', args=[self.user.username])

    def get_profile_url(self):
        #if self.nickname and not '?' in self.nickname:
        #    return reverse('person_public_profile', args=[self.nickname])
        return reverse('person_public_profile', args=[self.user.username])

    def update_from_AMO(self, data=None):
        if not data:
            data = fetch_amo_user(self.user.email)

        if 'email' in data and self.user.email != data['email']:
            log.info('User (%s) updated email (%s)' % (
                self.user.username, self.user.email))
            self.user.email = data['email']
            self.user.save()

        if 'display_name' in data:
            if data['display_name']:
                names = data['display_name'].split(' ')
                self.user.firstname = names[0]
                if len(names) > 1:
                    self.user.lastname = names[-1]
                self.user.save()

        if 'username' in data:
            self.nickname = data['username']
            log.debug('nickname updated from AMO by id (%s)' % self.user.username)
        if 'homepage' in data:
            self.homepage = data['homepage']

        self.save()
