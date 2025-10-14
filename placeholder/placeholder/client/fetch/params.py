from easy_client.types import QueryParams


GetParamsPosts: QueryParams = {}

GetParamsComments: QueryParams = {}

GetParamsAlbums: QueryParams = {}

GetParamsPhotos: QueryParams = {}

GetParamsTodos: QueryParams = {}

GetParamsUsers: QueryParams = {}



def get_default_params(endpoint: str) -> QueryParams:
    
    if endpoint == "posts":
        return GetParamsPosts
    
    if endpoint == "comments":
        return GetParamsComments
    
    if endpoint == "albums":
        return GetParamsAlbums
    
    if endpoint == "photos":
        return GetParamsPhotos
    
    if endpoint == "todos":
        return GetParamsTodos
    
    if endpoint == "users":
        return GetParamsUsers
    
    return {}