from plone.app.testing import PloneSandboxLayer
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import IntegrationTesting
from plone.app.testing import applyProfile
from plone.testing import z2
from zope.configuration import xmlconfig


class TutkaUtils(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load ZCML
        import jyu.datautils
        #self.loadZCML(package=jyu.tutka.utils)
        xmlconfig.file('configure.zcml', jyu.datautils, context=configurationContext)

        # Install product and call its initialize() function
        z2.installProduct(app, 'jyu.datautils')

        # Note: you can skip this if my.product is not a Zope 2-style
        # product, i.e. it is not in the Products.* namespace and it
        # does not have a <five:registerPackage /> directive in its
        # configure.zcml.

    def setUpPloneSite(self, portal):
        # Install into Plone site using portal_setup
        applyProfile(portal, 'jyu.datautils:default')

    def tearDownZope(self, app):
        # Uninstall product
        z2.uninstallProduct(app, 'jyu.datautils')

TUTKA_UTILS_FIXTURE = TutkaUtils()
TUTKA_UTILS_INTEGRATION_TESTING = IntegrationTesting(bases=(TUTKA_UTILS_FIXTURE,), name="DataUtilsTests:Integration")
