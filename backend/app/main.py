"""创建FastAPI实例、注册中间件和路由、定义启动生命周期"""
from contextlib import asynccontextmanager

from fastapi import FastAPI,Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware,RequestResponseEndpoint
from starlette.responses import Response

from app.api import health
from app.config import settings
from app.database import init_db
from app.api import (
    auth,
    projects,
    requirements,
    generations,
    skills,
    settings as settings_api,
    designs,
    knowledge,
    testcases,
    test_tasks,
    evaluations,
)
from app.services.llm import LLMCallError

@asynccontextmanager
async def lifespan(app:FastAPI):
    if not settings.debug:
        weak_passwords = {"","nini123456","admin","password","123456"}
        if settings.auth_password in weak_passwords or len(settings.auth_password)<16:
            raise RuntimeError("生产环境必须通过AUTH_PASSWORD配置至少16位的非默认密码")
    init_db()
    yield

app = FastAPI(
    title=settings.app_name,
    description="AI 测试用例管理平台",
    version="0.1.0",
    lifespan=lifespan,
    docs_url="/docs" if settings.debug else None,
    redoc_url="/redoc" if settings.debug else None,
    openapi_url="/openapi.json" if settings.debug else None
)

@app.exception_handler(LLMCallError)
async def llm_error_handler(request:Request,exc:LLMCallError):
    """LLM/Embedding 调用失败(Key过期，限流，网络等)同意返回中文提示，前端直接展示detail"""
    return JSONResponse(status_code=502,content={"detail":str(exc)})

class ApiAuthMiddleware(BaseHTTPMiddleware):
    """保护除登录与健康检查外的全部业务API"""
    public_paths={"/api/auth/login","/api/auth/register","/api/health"}

    async def dispatch(self,request:Request,call_next:RequestResponseEndpoint)->Response:
        path=request.url.path.rstrip("/") or "/"
        if request.method == "OPTIONS" or not path.startswith("/api/") or path in self.public_paths:
            return await call_next(request)
        authorization = request.headers.get("Authorization","")
        scheme,_,token  = authorization.partition(" ")
        session = auth.get_session(token) if scheme.lower() == "bearer" and token else None
        if session is None:
            return JSONResponse(
                status_code=401,
                content={"detail":"登录已失效，请重新登录"},
                headers={"WWW-Authenticate":"Bearer"},
            )
        request.state.auth_token=token
        request.state.auth_session=session
        return await call_next(request)


# 先注册鉴权，再注册 CORS，使跨域响应（包括 401）也带正确的 CORS 头。
app.add_middleware(ApiAuthMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cor_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(health.router,prefix="/api")
app.include_router(auth.router,prefix="/api")
app.include_router(projects.router,prefix="/api")
app.include_router(requirements.router,prefix="/api")
app.include_router(generations.router,prefix="/api")
app.include_router(skills.router,prefix="/api")
app.include_router(settings_api.router,prefix="/api")
app.include_router(designs.router,prefix="/api")
app.include_router(knowledge.router,prefix="/api")
app.include_router(testcases.router,prefix="/api")
app.include_router(testcases.project_router,prefix="/api")
app.include_router(test_tasks.router,prefix="/api")
app.include_router(evaluations.router,prefix="/api")