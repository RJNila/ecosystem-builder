from pydantic import ValidationError
from app.dtos.organization import OrganizationCreate, OrganizationOut
import uuid


def test_organization_create_valid():
    dto = OrganizationCreate(name="Acme Corp", code="ACME", description="Test org")
    assert dto.name == "Acme Corp"
    assert dto.code == "ACME"


def test_organization_create_invalid():
    try:
        OrganizationCreate(name="A", code="X", description="d" * 600)
        assert False, "ValidationError expected"
    except ValidationError:
        pass


def test_organization_out_from_model_attrs():
    # OrganizationOut uses from_attributes option; simulate with attribute object
    class Obj:
        def __init__(self):
            self.id = uuid.uuid4()
            self.name = "Name"
            self.code = "C"
            self.description = None

    out = OrganizationOut.model_validate(Obj())
    assert out.name == "Name"
    assert out.code == "C"
