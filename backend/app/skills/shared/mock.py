# 测试用例的mock
def mock_cases(feature: str,count: int,case_types: list[str],skill_name:str,smoke:bool =False) -> list[dict]:
    cases = []
    for i in range(count):
        case_type = case_types[i % len(case_types)]
        prefix = {"functional":"功能","boundary":"边界","exception":"异常"}.get(case_type,"")
        cases.append({
            "title":f"{prefix}-{feature}-用例{i+1}",
            "priority":"P0" if i==0 else "P1",
            "case_type": case_type,
            "is_smoke":True if smoke else (i==0),
            "precondition":f"用户已进入{feature}相关页面",
            "steps":["执行相关操作","观察系统响应"],
            "expected_result":"系统按预期响应",
            "skill_name":skill_name
        })
    return cases

# 功能点mock
MOCK_REQUIREMENT_ITEMS = [
    {
        "module": "用户登录",
        "feature": "账号密码登录",
        "description": "用户使用账号和密码登录系统",
        "acceptance_criteria": "正确账号密码可登录\n错误密码提示失败\n空账号或密码不可提交",
        "constraints": "密码长度 6-20 位",
        "priority": "P0",
    },
    {
        "module": "用户登录",
        "feature": "手机号验证码登录",
        "description": "用户使用手机号和短信验证码登录",
        "acceptance_criteria": "正确验证码可登录\n验证码 60 秒有效\n错误 5 次锁定 30 分钟",
        "constraints": "验证码 6 位数字",
        "priority": "P1",
    },
]

# 设计稿提取功能点mock
MOCK_SOURCE = "mock"

MOCK_DESIGN_INSIGHTS = [
    {
        "page": "示例页面（Mock 数据，未调用视觉模型）",
        "module": "页面交互",
        "feature": "提交表单",
        "description": "用户填写必填信息后提交表单",
        "acceptance_criteria": "必填信息完整时提交按钮可用，提交后展示成功反馈",
        "constraints": "必填项为空时按钮保持禁用",
        "priority": "P1",
    },
]

# 功能点确定测试范围mock
MOCK_SCOPE = {
    "in_scope": [
        "核心登录流程（账号密码、手机号验证码）",
        "密码错误提示与连续错误锁定策略",
        "输入校验与边界（空值、格式、长度）",
    ],
    "out_scope": [
        "第三方 OAuth / 扫码登录",
        "性能与并发压测",
        "UI 视觉走查",
    ],
    "risks": [
        "短信验证码通道稳定性未知",
        "锁定阈值与风控策略耦合，需与产品确认",
        "多端并发登录行为未在需求中明确",
    ],
}

