from fastapi import APIRouter, FastAPI,HTTPException,Depends,Request,UploadFile,Form
from dotenv import load_dotenv
from validations import SEOAgent,CompetitorAgent,CustomerAgent,PersonalizedAgent,UserAgent,MarketingAgent,DigitalTwinAgentModel,ChangePassModel,PolicyChatModel,RefreshTokenModel,EmergingRiskModel,PersonResearchModel,CustomerReachModel,VirtualChatModel,DeleteFiles,OnboardingChatModel
from agents.seo_agent.crew import SeoAgent
from agents.competitor_analysis_agent.crew import CompetitorAnalysisAgent
from agents.customer_sentiment_agent.crew import CustomerSentimentCrew
from agents.personalized_recommendation_agent.crew import PersonalizedRecommendationCrew
from agents.digital_twin_agent.crew import DigitalTwinAgent
from agents.marketing_agent.crew import MarketingPostsCrew
from fastapi.middleware.cors import CORSMiddleware
from passlib.context import CryptContext
from agents.user_id_agent.crew import IDReaderCrew
from utils.index import get_password_hash,get_user,create_token,verify_password,create_user,change_password,decode_token,updateRefreshToken,verifyRefreshMatchToken,load_document,retreiveUsers
from utils.jwtbearer import JWTBearer
from agents.policy_word_explainer_agent.crew import PolicyCrew
from agents.emerging_risk_agent.crew import EmergingRiskAgent
from agents.person_research_agent.crew import PersonResearchAgent
from agents.customer_reach_agent.crew import CustomerResearchCrew
from agents.contract_optimization_agent.crew import ContractOptimizationCrew
from agents.automated_budget_agent.crew import AutomatedBudgetingAgent
from agents.user_stories_agent.crew import UserStoryCrew
from agents.contract_summarizer_agent.crew import ContractSummarizer
from agents.document_processor.crew import DocumentProcessor
from agents.claims_processor.crew import ClaimsProcessor
from agents.onboarding_chatbot.crew import OnboardingChatbot
from PyPDF2 import PdfMerger
from agents.virtual_assistant_agent.crew import ChatCrew
from pathlib import Path
import os
from typing import Annotated,List
from nanoid import generate
import asyncio
import uvicorn

app = FastAPI()
load_dotenv()
uri = os.getenv('MONGO_URI')
model = os.getenv("MODEL")
api_key = os.getenv("OPENAI_API_KEY")
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins='*',
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
agent_router = APIRouter(prefix="/agent",tags=['Agent'])
auth_router = APIRouter(prefix="/auth",tags=['Auth'])
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

#agents
@agent_router.post('/{agentId}',dependencies=[Depends(JWTBearer())])
async def agents(agentId,agent:SEOAgent|CompetitorAgent|CustomerAgent|PersonalizedAgent|MarketingAgent|DigitalTwinAgentModel|EmergingRiskModel|PersonResearchModel|CustomerReachModel):
    if(agentId=='0'):        
        result= await asyncio.to_thread(SeoAgent().crew().kickoff,agent.dict())
        return {"result":result}
    elif(agentId=='2'):
        result= await asyncio.to_thread(CompetitorAnalysisAgent().crew().kickoff,agent.dict())
        return {"result":result}
    elif(agentId=='9'):
        result=  await asyncio.to_thread(CustomerSentimentCrew().crew().kickoff,agent.dict())
        return {"result":result}
    elif(agentId=='10'):
        result=  await asyncio.to_thread(PersonalizedRecommendationCrew().crew().kickoff,agent.dict())
        return {"result":result}
    elif(agentId=='1'):
        result =  await asyncio.to_thread(MarketingPostsCrew().crew().kickoff,agent.dict())
        return {"result":result}
    elif(agentId=='3'):
        result= await asyncio.to_thread(DigitalTwinAgent().crew().kickoff,agent.dict())
        return {'result':result}
    elif(agentId=='7'):
        result =  await asyncio.to_thread(EmergingRiskAgent().crew().kickoff,agent.dict())
        return {"result":result}
    elif(agentId=='8'):
        result =  await asyncio.to_thread(PersonResearchAgent().crew().kickoff,agent.dict())
        return {"result":result}
    elif(agentId=='11'):
        result =  await asyncio.to_thread(CustomerResearchCrew().crew().kickoff,agent.dict())
        return {"result":result}

@agent_router.post('/file/{agentId}',dependencies=[Depends(JWTBearer())])
async def agentsFile(agentId,file:UploadFile=None,file2:UploadFile=None,files:List[UploadFile]=None,region:Annotated[str, Form()]=None,functionality:Annotated[str ,Form()]=None):
    if(agentId=='4'):
        if(agentId not in os.listdir('uploads')):
            os.mkdir(f"uploads/{agentId}")
        file_name=generate(size=10)
        audio_path = f'./uploads/{agentId}/{file_name}.png'
        with open(audio_path, "wb") as f:
            f.write(file.file.read())
        id_reader_crew = IDReaderCrew(image_path=audio_path)
        inputs = {
            "image_path": audio_path,
        }
        response = await asyncio.to_thread(id_reader_crew.crew().kickoff,inputs)
        os.remove(audio_path)
        return {"result":response}
    elif(agentId=='12'):
        if(agentId not in os.listdir('uploads')):
            os.mkdir(f"uploads/{agentId}")
        file_name=generate(size=10)
        if('.docx' in file.filename):
            audio_path = f'./uploads/{agentId}/{file_name}.docx'
            with open(audio_path, "wb") as f:
                f.write(file.file.read())
        if('.pdf' in file.filename):
            audio_path = f'./uploads/{agentId}/{file_name}.pdf'
            with open(audio_path, "wb") as f:
                f.write(file.file.read())
        if('.txt' in file.filename):
            audio_path = f'./uploads/{agentId}/{file_name}.txt'
            with open(audio_path, "wb") as f:
                f.write(file.file.read())

        contract_text = load_document(audio_path)
        # Initialize and run the agent
        inputs = {"contract_text": contract_text}
        response = await asyncio.to_thread(ContractOptimizationCrew().crew().kickoff,inputs)
        os.remove(audio_path)
        return {"result":response}
    elif(agentId=='13'):
        file_name=generate(size=10)
        if(agentId not in os.listdir('uploads')):
            os.mkdir(f"uploads/{agentId}")
        audio_path = f'./uploads/{agentId}/{file_name}.csv'
        with open(audio_path, "wb") as f:
            data=await asyncio.to_thread(file.file.read)
            await asyncio.to_thread(f.write,data)
        inputs = {
            "file_path": audio_path,
            "region": region,
        }
        result = await asyncio.to_thread(AutomatedBudgetingAgent(inputs=inputs).crew().kickoff,inputs)
        os.remove(audio_path)
        return {"result":result}
    elif(agentId=='15'):
        user_story_crew = UserStoryCrew()
        response_audio_files = []
        for i in files:
            fileName=generate(size=10)
            audio_path=f'./uploads/audios/{fileName}.wav'
            response_audio_files.append(audio_path)
            with open(audio_path,'wb') as f:
                data=await asyncio.to_thread(i.file.read)
                await asyncio.to_thread(f.write,data)
        functionalities = []
        functionalities.append(response_audio_files)

        response = await asyncio.to_thread(user_story_crew.crew().kickoff,{"audio_responses": functionalities})
        for i in response_audio_files:
            await asyncio.to_thread(os.remove,i)
        return {"result":response}
    elif(agentId=='16'):
        file_name= f'./uploads/{agentId}/{generate(size=10)}.pdf'
        if(agentId not in os.listdir('uploads')):
            os.mkdir(f"uploads/{agentId}")
        with open(file_name,'wb') as f:
            data=await asyncio.to_thread(file.file.read)
            await asyncio.to_thread(f.write,data)
        inputs = {
            'contract_file': file_name  # Use the absolute path here
        }
        response=await asyncio.to_thread(ContractSummarizer().crew().kickoff,inputs)
        await asyncio.to_thread(os.remove,file_name)
        return {"result":response}
    elif(agentId=='17'):
        if(agentId not in os.listdir('uploads')):
            os.mkdir(f"uploads/{agentId}")
        file_name=generate(size=10)
        if('.docx' in file.filename):
            audio_path = f'./uploads/{agentId}/{file_name}.docx'
            with open(audio_path, "wb") as f:
                f.write(file.file.read())
        if('.pdf' in file.filename):
            audio_path = f'./uploads/{agentId}/{file_name}.pdf'
            with open(audio_path, "wb") as f:
                f.write(file.file.read())
        if('.txt' in file.filename):
            audio_path = f'./uploads/{agentId}/{file_name}.txt'
            with open(audio_path, "wb") as f:
                f.write(file.file.read())
        inputs = {
            'document_file': audio_path  # Replace with the path to your document
        }
        response=await asyncio.to_thread(DocumentProcessor().crew().kickoff,inputs)
        await asyncio.to_thread(os.remove,audio_path)
        return {"result":response}
    elif(agentId=='18'):
        print('im hereee')
        file_name1= f'./uploads/{agentId}/{generate(size=10)}.pdf'
        file_name2= f'./uploads/{agentId}/{generate(size=10)}.pdf'
        if(agentId not in os.listdir('uploads')):
            os.mkdir(f"uploads/{agentId}")
        with open(file_name1,'wb') as f:
            data=await asyncio.to_thread(file.file.read)
            await asyncio.to_thread(f.write,data)
        with open(file_name2,'wb') as f:
            data=await asyncio.to_thread(file2.file.read)
            await asyncio.to_thread(f.write,data)

        inputs = {
            'rules_document': file_name1,
            'claims_document': file_name2
        }
        response=await asyncio.to_thread(ClaimsProcessor().crew().kickoff,inputs)
        await asyncio.to_thread(os.remove,file_name1)
        await asyncio.to_thread(os.remove,file_name2)
        return {"result":response}

@auth_router.post('/login')
async def login(user:UserAgent):
    retrieveUser=get_user({"email":user.email})
    if(retrieveUser):
        if(verify_password(user.password,retrieveUser['password'])):
            accessToken=create_token(user.dict(),'accessToken')
            refreshToken=create_token(user.dict(),'refreshToken')
            newUser={"email":retrieveUser['email'],"tokens":{"access_token":accessToken,"refresh_token":refreshToken}}
            updateRefreshToken(newUser['email'],refreshToken)
            return newUser
        raise HTTPException(status_code=404, detail="Invalid Credentials")
    raise HTTPException(status_code=404, detail="Invalid Credentials")
    
@auth_router.post('/register')
async def register(user:UserAgent):
    retrieveUser=get_user({'email':user.email})
    if(retrieveUser):
        raise HTTPException(status_code=404, detail="User Already Exist")
    accessToken=create_token(user.dict(),'accessToken')
    refreshToken=create_token(user.dict(),'refreshToken')
    passwordHash=get_password_hash(user.password)
    newUser={"email":user.email,"password":passwordHash}
    createdUser=create_user(newUser,refreshToken)
    createdUser['tokens']={"accessToken":accessToken,"refreshToken":refreshToken}
    del createdUser['password']
    return createdUser

@auth_router.post('/forgot-password')
async def forgotPass(email:str):
    user={"email":email}
    retrieveUser=get_user(user)
    if(not retrieveUser):
        raise HTTPException(status_code=404, detail="User Doesnt Exist")
    return user

@auth_router.post('/change-password')
async def changePass(newPass:ChangePassModel):
    newPassword=newPass.password
    user={"email":newPass.email}
    retrieveUser=get_user(user)
    if(not retrieveUser):
        raise HTTPException(status_code=404, detail="User Doesnt Exist")
    change_password(user,newPassword)
    return 'done'

@auth_router.post('/tokens')
async def newTokens(request:RefreshTokenModel):
    try:
        refreshToken=request.refreshToken
        print('refresh',refreshToken)
        data=decode_token(refreshToken)
        if(verifyRefreshMatchToken(data['email'],refreshToken)):
            newRefreshToken=create_token(data,'refreshToken')
            updateRefreshToken(data['email'],newRefreshToken)
            newTokens={"access_token":create_token(data,'accessToken'),"refresh_token":newRefreshToken}
            return newTokens
        else:
            print('they dont match')
            raise HTTPException(status_code=404, detail="Unauthorized")
    except Exception as e:
        print('error',e)
        raise HTTPException(status_code=404, detail="Unauthorized")

@app.post('/logout', dependencies=[Depends(JWTBearer())])
async def logout(request:Request):
    token = request.headers['authorization'].split()[1]
    try:
        data=decode_token(token)
        updateRefreshToken(data['email'],'')
        return 'Success'
    except:
        raise HTTPException(status_code=403, detail="Invalid Access Token")

@app.get('/user',dependencies=[Depends(JWTBearer())])
async def getUser(request:Request):
    token = request.headers['authorization'].split()[1]
    try:
        data=decode_token(token)
        return data
    except:
        raise HTTPException(status_code=403, detail="Invalid Access Token")
    
@app.delete('/file',dependencies=[Depends(JWTBearer())])
async def deleteFile(file:str):
    audio_path = f'./uploads/{file}'
    await asyncio.to_thread(os.remove,audio_path)
    print('deleted File Sucessfully')
    return 'Success'

@app.post('/files',dependencies=[Depends(JWTBearer())])
async def deleteFile(file:DeleteFiles):
    for i in file.files:
        audio_path = f'./uploads/{i}'
        await asyncio.to_thread(os.remove,audio_path)
    print('deleted File Sucessfully')
    return 'Success'

@app.post('/start/policy-chat',dependencies=[Depends(JWTBearer())])
async def policyStart(file:UploadFile):
        file_name=generate(size=10)
        audio_path = f'./uploads/{file_name}.pdf'
        with open(audio_path, "wb") as f:
            data=await asyncio.to_thread(file.file.read)
            await asyncio.to_thread(f.write,data)
        # response = id_reader_crew.crew().kickoff(inputs=inputs)
        # os.remove(audio_path)
        
        return {"result":f"{file_name}.pdf"}

@app.post('/policy-chat/chat',dependencies=[Depends(JWTBearer())])
async def policyChat(chat:PolicyChatModel):    
    pdf_path=f'./uploads/{chat.pdf}'
    policy_crew =  PolicyCrew(pdf_path=pdf_path)
    context=' | '.join(chat.context)
    inputs={
        "query": chat.query,
        "context": context,
    }
    result=await asyncio.to_thread(policy_crew.crew().kickoff,inputs)
    result=result.dict()
    result['type']=2
    return {'result':result}

@app.post('/start/chatbot',dependencies=[Depends(JWTBearer())])
async def chatBotStart(file:UploadFile):
        file_name=generate(size=10)
        audio_path = f'./uploads/{file_name}.pdf'
        with open(audio_path, "wb") as f:
            data=await asyncio.to_thread(file.file.read)
            await asyncio.to_thread(f.write,data)
        # response = id_reader_crew.crew().kickoff(inputs=inputs)
        # os.remove(audio_path)
        
        return {"result":f"{file_name}.pdf"}

@app.post('/chatbot/chat',dependencies=[Depends(JWTBearer())])
async def chatBotChat(chat:PolicyChatModel):    
    pdf_path=f'./uploads/{chat.pdf}'
    policy_crew =  ChatCrew(pdf_path=pdf_path)
    context=' | '.join(chat.context)
    inputs={
        "query": chat.query,
        "context": context,
    }
    result=await asyncio.to_thread(policy_crew.crew().kickoff,inputs)
    result=result.dict()
    result['type']=2
    return {'result':result}

@app.post('/start/virtual-chat',dependencies=[Depends(JWTBearer())])
async def policyStart(file:List[UploadFile]): 
        fileArray=[]
        for i in file:
            file_name=generate(size=10)
            audio_path = f'./uploads/{file_name}.pdf'
            fileArray.append(f"{file_name}.pdf")
            with open(audio_path, "wb") as f:
                data=await asyncio.to_thread(i.file.read)
                await asyncio.to_thread(f.write,data)
        return {"result":fileArray}

def merge_pdfs(pdf_paths, output_path="merged.pdf"):
    """
    Merge multiple PDFs into one.
    
    Args:
        pdf_paths (list): List of paths to the PDF files.
        output_path (str): Path to save the merged PDF.
    
    Returns:
        str: Path to the merged PDF.
    """
    if len(pdf_paths) == 1:
        return pdf_paths[0]  # No merging needed if only one PDF is provided

    merger = PdfMerger()
    for pdf in pdf_paths:
        merger.append(pdf)
    merger.write(output_path)
    merger.close()
    return output_path

def initialize_virtual_assistant(pdf_paths):
    """
    Initialize the Virtual Assistant with the given PDF(s).
    If there are two PDFs, they are merged before initializing.
    """
    # Merge PDFs if more than one is provided
    merged_pdf_path = merge_pdfs(pdf_paths)
    print(f"Using merged PDF at: {merged_pdf_path}")
    return ChatCrew(pdf_paths=[merged_pdf_path])

@app.post('/virtual-chat/chat',dependencies=[Depends(JWTBearer())])
async def policyChat(chat:VirtualChatModel):    
    pdfPaths=[]
    for i in chat.pdf:
        pdfPaths.append(f'./uploads/{i}')
    assistant_crew = initialize_virtual_assistant(pdfPaths)
    context=' | '.join(chat.context)
    inputs={
        "query": chat.query,
        "context": context,
    }
    result=await asyncio.to_thread(assistant_crew.crew().kickoff,inputs)
    result=result.dict()
    result['type']=2
    return {'result':result}

@app.post('/start/onboarding-agent',dependencies=[Depends(JWTBearer())])
async def onboardingStart(file:UploadFile):
        file_name=generate(size=10)
        audio_path = f'./uploads/{file_name}.pdf'
        with open(audio_path, "wb") as f:
            data=await asyncio.to_thread(file.file.read)
            await asyncio.to_thread(f.write,data)
        # response = id_reader_crew.crew().kickoff(inputs=inputs)
        # os.remove(audio_path)
        
        return {"result":file_name}

@app.post('/onboarding-agent/chat',dependencies=[Depends(JWTBearer())])
async def onboardingChat(chat:OnboardingChatModel):    
    pdf_path=f'./uploads/{chat.pdf}.pdf'
    inputs = {
        "query": chat.query,
        "context":chat.context,
        "pdf_path": pdf_path
    }
    result=await asyncio.to_thread(OnboardingChatbot(inputs=inputs).crew().kickoff,inputs)
    result=result.dict()
    result['type']=2
    return {'result':result}


@app.get('/users')
def getUsers():
    return retreiveUsers()

app.include_router(agent_router)
app.include_router(auth_router)