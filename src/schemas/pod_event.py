from pydantic import BaseModel, Field

class ResponseModel(BaseModel):
    status: str
    message: str
    

class NamespaceModel(BaseModel):
    """
    Model for Kubernetes namespace input.
    """
    namespace: str = Field(
        ...,
        title="Namespace",
        description="The Kubernetes namespace to fetch pod events from.",
    )