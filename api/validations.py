from pydantic import BaseModel


class SEOAgent(BaseModel):
     project_description: str
     customer_domain: str| None = None
     geographical_location:str

class CompetitorAgent(BaseModel):
     competitor1: str
     competitor2: str| None = None
     area:str

class CustomerAgent(BaseModel):
     company_name: str
     company_variations: list[str] | None = None
     geographical_location:str


class Characteristcs(BaseModel):
    industry:str|None=None
    risk_concern:str | None=None
    type: str |None=None
    interest: str |None=None
    type_of_entity: str |None=None
    specific_needs:str | None=None

class PersonalizedAgent(BaseModel):
     customer_name:str
     age_group:str
     customer_segment:str
     characteristics:Characteristcs

class UserAgent(BaseModel):
     email:str
     password:str

class MarketingAgent(BaseModel):
     customer_domain: str
     project_description: str
     geographical_location:str

class DigitalTwinAgentModel(BaseModel):
     area:str
     product_marketing_idea:str


class ChangePassModel(BaseModel):
     email:str
     password:str

class PolicyChatModel(BaseModel):
     pdf:str
     context:list[str]
     query:str

class EmergingRiskModel(BaseModel):
     area:str
     product_lines:str

class RefreshTokenModel(BaseModel):
     refreshToken:str

class PersonResearchModel(BaseModel):
     person:str

class CustomerReachModel(BaseModel):
     company_name:str

class VirtualChatModel(BaseModel):
     pdf:list[str]
     context:list[str]
     query:str

class DeleteFiles(BaseModel):
     files:list[str]

class OnboardingChatModel(BaseModel):
     pdf:str
     context:str
     query:str
