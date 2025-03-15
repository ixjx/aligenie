from ninja import NinjaAPI, Schema

from .tools import Computer

api = NinjaAPI()

'''
{
    sessionId='cc95ccd7-a5d5-4059-8a1e-2dcf6f611a33' 
    utterance='打开电脑' 
    requestData={} 
    botId=157481 
    domainId=86762 
    skillId=109764 
    skillName='请帮我' 
    intentId=185874 
    intentName='skill' 
    slotEntities=[] 
    requestId='20250308105456017-2037045565' 
    device={} 
    skillSession={'skillSessionId': 'ce2880dc-2274-4e9f-aae3-d609b5401428', 'newSession': True} 
    context={'system': {'apiAccessToken': ''}}
}
'''
class AligenieReq(Schema):
    sessionId: str
    utterance: str  # 语料
    requestData: dict
    botId: int
    domainId: int
    skillId: int
    skillName: str  # 技能名
    intentId: int
    intentName: str # 意图名
    slotEntities: list
    requestId: str
    device: dict
    skillSession: dict
    context: dict

@api.get('ping/')
def ping(request):
    return 'pong!'

@api.post('skill/')
def skill(request, data: AligenieReq):
    # 固定响应格式，需在2s内回复
    RES_DATA = {
        'returnCode': '0',
        'returnErrorSolution': '',
        'returnMessage': '',
        'returnValue':
            {'reply': '',
             'resultType': 'RESULT',
             'actions':
                 [{'name': 'audioPlayGenieSource',
                   'properties': {'audioGenieId': '123'}}],
             'properties': {},
             'executeCode': 'SUCCESS',
             'msgInfo': ''
             }
    }
    if request.META.get('HTTP_X_TOKEN') == 'indeed':  # 自定义头部验证，需在天猫精灵开放平台设置
        pc = Computer(ip='要开机的ip', mac='要开机的mac')
        # 技能判断、响应技能
        # print(data)
        if data.skillName == '请帮我':
            ISWAKE = pc.check_status()
            if '打开电脑' in data.utterance or '开电脑' in data.utterance:
                if ISWAKE:
                    # 开机状态下不操作
                    RES_DATA['returnValue']['reply'] = '猪头，电脑是开机状态！猪头'
                else:
                    # 关机状态下才开机
                    pc.wake_up()
                    RES_DATA['returnValue']['reply'] = '哈哈哈，开电脑执行成功！'
            elif '关闭电脑' in data.utterance or '关电脑' in data.utterance:
                if ISWAKE:
                    pc.shutdown()
                    RES_DATA['returnValue']['reply'] = '哈哈哈，关电脑执行成功！'
                else:
                    RES_DATA['returnValue']['reply'] = '猪头，电脑是关机状态！猪头'
            else:
                RES_DATA['returnValue']['reply'] = '未识别到意图！'
        else:
            RES_DATA['returnValue']['reply'] = '自定义技能不存在！'

    return RES_DATA