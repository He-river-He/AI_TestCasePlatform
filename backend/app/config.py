from pathlib import Path
from pydantic_settings import BaseSettings,SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent

class Settings(BaseSettings):
    # 从哪里读取环境变量，以及遇到额外配置项时怎么处理
    model_config = SettingsConfigDict(env_file="../.env",env_file_encoding="utf-8",extra="ignore")

    llm_api_key:str=""
    llm_base_url:str="https://api.deepseek.com"
    llm_model:str="deepseek-v4-flash"
    llm_mock_mode:bool = True

    # 视觉模型（设计稿解析），必须支持 OpenAI-compatible 多模态消息
    vision_api_key : str = ""
    vision_base_url : str = ""
    vision_model : str = ""

    # Embedding 模型（知识库检索用），与 Chat 接口类型不同，需单独配置
    embedding_api_key: str =""
    embedding_base_url: str =""
    embedding_model: str =""

    # Rerank 模型（知识库检索精排），留空则只做混合检索 RRF 融合
    rerank_api_key: str =""
    rerank_base_url: str =""
    rerank_model: str =""

    # 评测专用 LLM（AI Judge / 召回率判定），留空则复用上面的生成模型配置
    eval_llm_api_key: str = ""
    eval_llm_base_url: str = ""
    eval_llm_model: str = ""

    # 生产环境额外允许的自建 OpenAI 兼容接口域名（逗号分隔，不包含协议或路径）
    model_api_extra_hosts: str =""

    app_name: str="AI测试用例管理平台"
    debug:bool = True
    # LangGraph 运行检查点与业务库分开保存，便于失败任务恢复。
    aitc_langgraph_checkpoint_path: str = ""
    database_url:str = f"sqlite:///{BASE_DIR/'data'/'app.db'}"
    cors_origins:str ="http://localhost:5173,http://127.0.0.1:5173"

    auth_username: str = "admin"
    auth_password: str = "nini123456"
    auth_token_ttl_hours: int =24
    allow_registration: bool = True
    auth_max_attempts: int = 5
    auth_lockout_minutes: int = 15
    registration_max_per_hour:int =5

    design_asset_dir: str =""


    @property
    def cor_origin_list(self) -> list[str]:
        return [item.strip() for item in self.cors_origins.split(",") if item.strip()]
    
    @property
    def use_mock_llm(self) -> bool:
        return self.llm_mock_mode or not self.llm_api_key

settings =Settings()