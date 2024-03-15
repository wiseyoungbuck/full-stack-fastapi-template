from app.models import Organization, OrganizationCreate, Email


from sqlmodel import Session

from app.core.db import engine


def create_organization(name, email) -> tuple[Organization, Email]:
    """
    Create new organization.
    """
    with Session(engine) as session:
        organization = Organization(name=name, owner_id=70)
        session.add(organization)
        session.commit()
        print(organization.id)
        email = Email(email_address=email, is_primary=True, organization_id=organization.id)
        
        
        session.add(email)
        session.commit()
        session.refresh(organization)
        session.refresh(email)
    return organization, email

def read_organization(org_id: int):
    with Session(engine) as session:
        org: Organization = session.get(Organization, org_id)
        print(org.emails)
        
    return org

if __name__ == "__main__":
    org, email = create_organization("Tes6t Org", "tes6t@test.com")
    
    print(org.model_dump_json())
    print(email.model_dump_json())
    org= read_organization(org.id)
    print(org.model_dump_json())
    print(email.model_dump_json())
#    print([e.model_dump_json() for e in emails])