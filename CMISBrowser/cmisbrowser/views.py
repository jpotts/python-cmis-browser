from pyramid.view import view_config
from pyramid.events import NewRequest
from pyramid.events import subscriber
from cmislib.model import CmisClient
from pyramid.response import Response
from pyramid.httpexceptions import HTTPFound
import colander
from deform import Form, ValidationFailure
from deform.widget import TextAreaWidget, HiddenWidget
from pyramid.renderers import get_renderer

PAGE_SIZE = 20
FEED_SIZE = 100

def site_layout():
    renderer = get_renderer("templates/global_layout.pt")
    layout = renderer.implementation().macros['layout']
    return layout

@subscriber(NewRequest)
def new_request_subscriber(event):
    request = event.request
    settings = request.registry.settings
    client = CmisClient(settings['cmisbrowser.serviceUrl'],
                        settings['cmisbrowser.username'],
                        settings['cmisbrowser.password'])
    request.client = client

@view_config(route_name='home', renderer='templates/index.pt')
def home(request):
    return {'layout': site_layout(),
            'page_title': 'Home',
            'username': request.registry.settings['cmisbrowser.username']}

@view_config(route_name='about', renderer='templates/about.pt')
def about(request):
    return {'project':'CMISBrowser'}

@view_config(route_name='path', renderer='templates/path.pt')
def path(request):
    # set up the repository browser
    path = request.matchdict['path']
    path = '/' + path
    repo = request.client.defaultRepository
    folder = repo.getObjectByPath(path.encode('utf-8'))
    folderActions = folder.getAllowableActions()
    pageSize = PAGE_SIZE
    skipCount = 0
    if ('maxItems' in request.GET.keys() and
        'skipCount' in request.GET.keys()):
        pageSize = int(request.GET['maxItems'])
        skipCount = int(request.GET['skipCount'])
        if skipCount < 0:
            skipCount = 0

    rs = folder.getChildren(includeAllowableActions=True,
                                maxItems=pageSize,
                                skipCount=skipCount,
                                orderBy='cmis:name,ASC')
 
    # set up the new content form
    schema = NewContentForm()
    contentForm = Form(schema, action='/createContent' + path, buttons=('submit',))
    return {'layout': site_layout(),
            'page_title': 'Browse Repository',
            'page_size': pageSize,
            'skip_count': skipCount,
            'path': path,
            'canCreateDocument': folderActions['canCreateDocument'],
            'canCreateFolder': folderActions['canCreateFolder'],
            'children': rs,
            'form': contentForm.render()}

@view_config(route_name='feed', renderer='templates/feed.pt')
def feed(request):
    path = request.matchdict['path']
    path = '/' + path
    repo = request.client.defaultRepository
    folder = repo.getObjectByPath(path.encode('utf-8'))

    rs = folder.getChildren(includeAllowableActions=False,
                                maxItems=FEED_SIZE,
                                orderBy='cmis:lastModificationDate,DESC')

    return {'layout': site_layout(),
            'page_title': 'Recently Modified Documents in ' + folder.name,
            'page_size': FEED_SIZE,
            'path': path,
            'children': rs}

@view_config(route_name='details', renderer='templates/details.pt')
def details(request):
    path = request.matchdict['path']
    path = '/' + path
    repo = request.client.defaultRepository
    object = repo.getObjectByPath(path.encode('utf-8'))    
    return {'layout': site_layout(),
            'page_title': 'Details',
            'path': path,
            'object': object}

@view_config(route_name='file')
def get_file(request):
    path = request.matchdict['path']
    path = '/' + path
    repo = request.client.defaultRepository
    object = repo.getObjectByPath(path.encode('utf-8'))    
    return Response(body=object.getContentStream().read(), content_type=str(object.properties['cmis:contentStreamMimeType']))

@view_config(route_name='createFolder')
def create_folder(request):
    if 'Create' in request.POST:
        folderName = request.POST.items()[0][1]
        targetPath = request.POST.items()[1][1]
        targetFolder = request.client.defaultRepository.getObjectByPath(targetPath)
        newFolder = targetFolder.createFolder(folderName)
        #request.session.flash('Form was submitted successfully.')
        #url = request.route_url('home') 
        return HTTPFound(location="/path" + targetPath)

@view_config(route_name='createContent')
def create_content(request):
    schema = NewContentForm()
    myform = Form(schema, buttons=('submit',))
    
    if 'submit' in request.POST:
        targetPath = "/" + request.matchdict['path']
        controls = request.POST.items()
        try:
            appstruct = myform.validate(controls)  # call validate
            targetFolder = request.client.defaultRepository.getObjectByPath(targetPath)
            doc = targetFolder.createDocumentFromString(appstruct['name'], contentString=appstruct['content'], contentType='text/plain')          
        except ValidationFailure, e: # catch the exception
            return {'form':e.render()} # re-render the form with an exception
        return HTTPFound(location="/path" + targetPath)

@view_config(route_name='uploadFile')
def upload_file(request):
    if 'Upload' in request.POST:
        targetPath = "/" + request.matchdict['path']
        targetFolder = request.client.defaultRepository.getObjectByPath(targetPath)
        uploadedFile = request.POST.get('file')
        doc = targetFolder.createDocument(uploadedFile.filename, contentFile=uploadedFile.file)
        return HTTPFound(location="/path" + targetPath)

@view_config(route_name='delete')
def delete(request):
    targetPath = "/" + request.matchdict['path']
    targetObj = request.client.defaultRepository.getObjectByPath(targetPath)
    if hasattr(targetObj, "deleteTree"):
        targetObj.deleteTree()
    else:
        targetObj.delete()
    return HTTPFound(location="/path" + '/'.join(targetPath.split('/')[:-1]))

class NewContentForm(colander.MappingSchema):
    name = colander.SchemaNode(colander.String())
    content = colander.SchemaNode(colander.String(),
                                  widget=TextAreaWidget())
