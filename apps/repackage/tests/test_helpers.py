"""
repackage.tests.test_models
---------------------------
"""
import commonware
import os
import tempfile
import urllib2
import zipfile

#from mock import Mock
from nose.tools import eq_
from nose import SkipTest
from utils.test import TestCase

from django.conf import settings

from base.templatetags.base_helpers import hashtag
from repackage.helpers import Repackage, increment_version

log = commonware.log.getLogger('f.tests')


class RepackageTest(TestCase):

    def setUp(self):
        self.hashtag = hashtag()
        self.file_prefix = os.path.join(settings.ROOT,
                'apps/xpi/tests/sample_addons/')
        self.xpi_file_prefix = "file://%s" % self.file_prefix
        self.sample_addons = [
                "sample_add-on-1.0b3.xpi",
                "sample_add-on-1.0b4.xpi",
                "sample_add-on-1.0rc2.xpi",
                "repackage-special_name.xpi"]
        self.sdk_source_dir = settings.REPACKAGE_SDK_SOURCE or os.path.join(
                settings.ROOT, 'lib/addon-sdk-1.0rc2')

    def tearDown(self):
        target_xpi = '%s.xpi' % os.path.join(
                tempfile.gettempdir(), self.hashtag)
        target_json = '%s.json' % os.path.join(
                tempfile.gettempdir(), self.hashtag)
        if os.path.isfile(target_xpi):
            os.remove(target_xpi)
        if os.path.isfile(target_json):
            os.remove(target_json)

    # mock self.sdk.get_source_dir()
    def test_repackage(self):
        for sample in self.sample_addons:
            rep = Repackage()
            rep.download(os.path.join(self.xpi_file_prefix, sample))
            response = rep.rebuild(self.sdk_source_dir, self.hashtag)
            assert not response[1]

    def test_not_existing_location(self):
        rep = Repackage()
        self.assertRaises(urllib2.HTTPError,
                rep.download,
                'http://builder.addons.mozilla.org/wrong_file.xpi')

    def test_forcing_version(self):
        for sample in self.sample_addons:
            rep = Repackage()
            rep.download(os.path.join(self.xpi_file_prefix, sample))
            rep.get_manifest({'version': 'force.version'})
        eq_(rep.manifest['version'], 'force.version')

    def test_main_dir_files_existence(self):
        rep = Repackage()
        xpi_path = os.path.join(
            self.xpi_file_prefix, 'infocon10sdk11icons.xpi')
        rep.download(xpi_path)
        response = rep.rebuild(self.sdk_source_dir, self.hashtag)
        assert not response[1]
        with open(os.path.join(settings.XPI_TARGETDIR,
                               "%s.xpi" % self.hashtag)) as xpi_file:
            xpi = zipfile.ZipFile(xpi_file)
            filenames = xpi.namelist()
            xpi.close()
        assert 'icon.png' in filenames
        assert 'icon64.png' in filenames
        raise SkipTest()
        # I've got no idea how to copy icon16.png to main dir of the XPI
        assert 'icon16.png' in filenames

    def test_version_increment(self):
        eq_('2.1.1', increment_version('2.1'))
        eq_('abc.0.1', increment_version('abc'))
        eq_('1.0.1', increment_version('1'))
        eq_('1.2pre.1', increment_version('1.2pre'))
        eq_('1.2.3pre.1', increment_version('1.2.3pre'))
        eq_('2.1.2', increment_version('2.1.1'))
        eq_('2.1.2.3', increment_version('2.1.2.2'))
        eq_('1.2.3pre.2', increment_version('1.2.3pre.1'))
