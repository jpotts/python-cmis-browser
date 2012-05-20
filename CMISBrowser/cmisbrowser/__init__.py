from pyramid.config import Configurator

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_static_view('deform_static', 'deform:static')
    config.add_route('home', '/')
    config.add_route('about', '/about')    
    config.add_route('path', '/path/{path:.*}')
    config.add_route('details', '/details/{path:.*}')
    config.add_route('file', '/file/{path:.*}')
    config.add_route('createFolder', '/createFolder/{path:.*}')
    config.add_route('createContent', '/createContent/{path:.*}')
    config.add_route('uploadFile', '/uploadFile/{path:.*}')
    config.add_route('delete', '/delete/{path:.*}')                
    config.scan()
    return config.make_wsgi_app()
