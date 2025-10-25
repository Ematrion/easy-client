from easy_client.types import QueryParams


GetParamsComments: QueryParams = {}

GetParamsPosts: QueryParams = {}

GetParamsAlbums: QueryParams = {}

GetParamsPhotos: QueryParams = {}

GetParamsUsers: QueryParams = {}

GetParamsTodos: QueryParams = {}



def get_default_params(endpoint: str) -> QueryParams:
    
    if endpoint == "comments":
        return GetParamsComments
    
    if endpoint == "posts":
        return GetParamsPosts
    
    if endpoint == "albums":
        return GetParamsAlbums
    
    if endpoint == "photos":
        return GetParamsPhotos
    
    if endpoint == "users":
        return GetParamsUsers
    
    if endpoint == "todos":
        return GetParamsTodos
    
    return {}