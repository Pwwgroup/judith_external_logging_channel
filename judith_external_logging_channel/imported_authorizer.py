"""Reference to an existing API Gateway authorizer by id.

No ``RequestAuthorizer.from_authorizer_id``/``from_authorizer_attributes``
factory exists on ``Authorizer``/``RequestAuthorizer``/``IAuthorizer`` in this
repo's pinned aws-cdk-lib version -- confirmed against the installed package
source, not assumed. ``apigateway.IAuthorizer`` is a plain two-property jsii
interface (``authorizer_id``, ``authorization_type``), so a minimal Python
object implementing it via ``@jsii.implements`` (the standard CDK pattern for
externally-referenced constructs -- the same one used for custom IVpc/
ISecurityGroup implementations) is a correct, lightweight substitute: it
creates no CloudFormation resource, it only carries the id across the jsii
boundary to whatever reads ``authorizer.authorizer_id`` when a Method is
attached to it.
"""

import jsii
from aws_cdk import aws_apigateway as apigateway


@jsii.implements(apigateway.IAuthorizer)
class ImportedAuthorizer:
    """A pre-existing API Gateway authorizer, referenced by id only."""

    def __init__(self, authorizer_id: str) -> None:
        self._authorizer_id = authorizer_id

    @property
    def authorizer_id(self) -> str:
        return self._authorizer_id

    @property
    def authorization_type(self) -> None:
        return None
