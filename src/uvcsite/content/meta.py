import martian
import grokcore.component
import uvcsite.content.components
import uvcsite.content.directive
import uvcsite.content.interfaces
import zope.component.zcml

from martian.error import GrokError


def default_name(factory, module=None, **data):
    return factory.__name__.lower()


class ProductFolderGrokker(martian.ClassGrokker):
    martian.component(uvcsite.content.components.ProductFolder)
    martian.directive(uvcsite.content.directive.contenttype)
    martian.directive(grokcore.component.name, get_default=default_name)

    def execute(self, factory, config, contenttype, name):
        print(name)
        if not contenttype:
            raise GrokError("%r must specify which contenttype should "
                            "go into this ProductFolder. Please use the"
                            "direcitve 'contenttype' for it."
                            % factory, factory)

        name = name.capitalize()
        config.action(
            discriminator=(
                'utility', uvcsite.content.interfaces.IProductFolder, name),
            callable=zope.component.zcml.handler,
            args=('registerUtility', factory,
                  uvcsite.content.interfaces.IProductFolder, name),
            )

        return True
