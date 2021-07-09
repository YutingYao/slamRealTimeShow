# -*- coding: utf-8 -*-
import datetime
import json
import uuid
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.profile import region_provider

import random

from aliyunsdkdysmsapi.request.v20170525 import SendSmsRequest
from apscheduler.schedulers.background import BackgroundScheduler

from ShareCloudServer.settings import ACCESS_KEY_ID, ACCESS_KEY_SECRET

import logging

from users.models import PhoneVerifyRecord

logger = logging.getLogger(__name__)
logger = logging.getLogger('django')

"""
短信业务调用接口示例，版本号：v20170525

Created on 2017-06-12

"""
# try:
#     reload(sys)
#     sys.setdefaultencoding('utf8')
# except NameError:
#     pass
# except Exception as err:
#     raise err


# 注意：不要更改
REGION = "cn-hangzhou"
PRODUCT_NAME = "Dysmsapi"
DOMAIN = "dysmsapi.aliyuncs.com"

acs_client = AcsClient(ACCESS_KEY_ID, ACCESS_KEY_SECRET, REGION)
region_provider.add_endpoint(PRODUCT_NAME, REGION, DOMAIN)


# 生成随机字符串
def random_str(random_length=8):
    str = ''
    # 生成字符串的可选字符串
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    for i in range(random_length):
        str += chars[random.randint(0, length)]
    return str


def send_phone_code(phone, send_type="register"):
    """
    用来发送手机验证码
    :param phone:        手机号
    :param send_type:    #验证码类型
    :return:
    """
    # 发送后返回的信息所对应的所有状况
    dict_status = {'OK': '发送成功',
                   'isp.RAM_PERMISSION_DENY': 'RAM权限DENY',
                   'isv.OUT_OF_SERVICE': '业务停机',
                   'isv.PRODUCT_UN_SUBSCRIPT': '未开通云通信产品的阿里云客户',
                   'isv.PRODUCT_UNSUBSCRIBE': '产品未开通',
                   'isv.ACCOUNT_NOT_EXISTS': '账户不存在',
                   'isv.ACCOUNT_ABNORMAL': '账户异常',
                   'isv.SMS_TEMPLATE_ILLEGAL	': '短信模板不合法',
                   'isv.SMS_SIGNATURE_ILLEGAL': '短信签名不合法',
                   'isv.INVALID_PARAMETERS': '参数异常',
                   'isp.SYSTEM_ERROR': '系统错误',
                   'isv.MOBILE_NUMBER_ILLEGAL': '非法手机号',
                   'isv.MOBILE_COUNT_OVER_LIMIT': '手机号码数量超过限制',
                   'isv.TEMPLATE_MISSING_PARAMETERS': '模板缺少变量',
                   'isv.BUSINESS_LIMIT_CONTROL': '业务限流',
                   'isv.INVALID_JSON_PARAM': 'JSON参数不合法，只接受字符串值',
                   'isv.BLACK_KEY_CONTROL_LIMIT': '黑名单管控',
                   'isv.PARAM_LENGTH_LIMIT': '参数超出长度限制',
                   'isv.PARAM_NOT_SUPPORT_URL': '不支持URL',
                   'isv.AMOUNT_NOT_ENOUGH': '账户余额不足'
                   }

    __business_id = uuid.uuid1()  # __business_id 发送短信 必须 生成的一个参数

    code = random.randint(1000, 9999)  # 生成4位数验证码

    params = {"code": code}  # 创建一个字典
    json_params = json.dumps(params)  # 把字典转化为json

    if send_type == "register":
        # 开始发送短信 并返回短信相应
        send_msg = send_sms(__business_id, phone, "欧诺嘉三维数字化平台", "SMS_195335052", json_params)
        dict_send_msg = eval(send_msg)  # 把返回的信息转化为字典
        send_status = dict_send_msg.get('Code')  # 获取到发送状态
        # params = u'{"name":"wqb","code":"12345678","address":"bz","phone":"13000000000"}'
        # b'{"Message":"OK","RequestId":"EC69DF87-2D8F-4A95-BF32-6C96A88E1B78","BizId":"489514132684964407^0","Code":"OK"}'
        if send_status == "OK":
            print("手机验证码发送成功")
            logger.info("phone:" + str(phone) + " 手机号用户注册验证码发送成功！")

            # 接下来把验证法以及发送的 成功的 BizId 保存入数据库中
            BizId = dict_send_msg['BizId']

            # 让之前 发送的注册验证码全部失效,实例化验证码的
            phone_verify_records = PhoneVerifyRecord.objects.filter(phone=str(phone), send_type="register",
                                                                    record_validity="valid")

            for phone_verify_record in phone_verify_records:
                phone_verify_record.record_validity = "invalid"
                phone_verify_record.save()

                logger.info(
                    "phone:" + str(phone_verify_record.phone) + " code:" + str(
                        phone_verify_record.code) + " 让之前的注册验证码失效")
            # print("BizId:", BizId)

            phone_record = PhoneVerifyRecord()
            phone_record.phone = str(phone)
            phone_record.code = str(code)
            phone_record.send_type = send_type
            phone_record.BizId = BizId
            phone_record.save()
            scheduler = BackgroundScheduler()
            # datetime.timedelta(days=1))
            dead_time = datetime.datetime.now() + datetime.timedelta(minutes=5, seconds=0)
            print("dead_time:", dead_time)
            scheduler.add_job(dead_phone_verify_records, 'date', run_date=dead_time,
                              args=[[phone_record]])
            scheduler.start()
            logger.info("phone:" + str(phone) + " 发送成功的手机注册验证码存入数据库！")
            return dict_status[send_status]
        else:
            print("手机注册验证码发送失败")
            logger.error("phone:" + str(phone) + " 手机注册验证码发送失败:" + dict_status[send_status])
            # print(dict_status[send_status])  # 打印发送失败的原因  #这里新增log 日志
            # 返回发送
            return dict_status[send_status]

    elif send_type == "forget":
        # 找回密码
        send_msg = send_sms(__business_id, phone, "欧诺嘉三维数字化平台", "SMS_196880043", json_params)
        dict_send_msg = eval(send_msg)  # 把返回的信息转化为字典
        send_status = dict_send_msg.get('Code')  # 获取到发送状态
        # params = u'{"name":"wqb","code":"12345678","address":"bz","phone":"13000000000"}'
        # b'{"Message":"OK","RequestId":"EC69DF87-2D8F-4A95-BF32-6C96A88E1B78","BizId":"489514132684964407^0","Code":"OK"}'

        if send_status == "OK":
            # print("手机找回密码验证码发送成功")
            logger.info("phone:" + str(phone) + " 找回密码验证码发送成功")
            BizId = dict_send_msg['BizId']

            # 让之前 发送的找回密验证码全部失效
            phone_verify_records = PhoneVerifyRecord.objects.filter(phone=str(phone), send_type="forget",
                                                                    record_validity="valid")
            #
            for phone_verify_record in phone_verify_records:
                phone_verify_record.record_validity = "invalid"
                phone_verify_record.save()
                logger.info(
                    "phone:" + str(phone_verify_record.phone) + " code:" + str(
                        phone_verify_record.code) + " 让之前的找回密码验证码失效")

            phone_record = PhoneVerifyRecord()
            phone_record.phone = str(phone)
            phone_record.code = str(code)
            phone_record.send_type = send_type
            phone_record.BizId = BizId
            phone_record.save()

            logger.info("phone:" + str(phone) + " 发送成功的手机找回密码验证码存入数据库！")

            # TODO: 异步任务使得
            # return dict_status[send_status]

            scheduler = BackgroundScheduler()
            # datetime.timedelta(days=1))
            dead_time = datetime.datetime.now() + datetime.timedelta(minutes=5, seconds=0)
            # print("dead_time:", dead_time)
            scheduler.add_job(dead_phone_verify_records, 'date', run_date=dead_time,
                              args=[[phone_record]])
            scheduler.start()
            logger.info("phone:" + str(phone) + " 发送成功的手机注册验证码存入数据库！")
            return dict_status[send_status]



        else:
            print("手机验证码发送失败")
            logger.error("phone:" + str(phone) + " 手机找回密码验证码发送失败:" + dict_status[send_status])
            print(dict_status[send_status])  # 打印发送失败的原因  #这里新增log 日志
            return dict_status[send_status]
    elif send_type == "sms_login":
        # TODO: 短信验证码登录
        send_msg = send_sms(__business_id, phone, "欧诺嘉三维数字化平台", "SMS_197210215", json_params)
        dict_send_msg = eval(send_msg)  # 把返回的信息转化为字典
        send_status = dict_send_msg.get('Code')  # 获取到发送状态
        # params = u'{"name":"wqb","code":"12345678","address":"bz","phone":"13000000000"}'
        # b'{"Message":"OK","RequestId":"EC69DF87-2D8F-4A95-BF32-6C96A88E1B78","BizId":"489514132684964407^0","Code":"OK"}'

        if send_status == "OK":
            # print("手机找回密码验证码发送成功")
            logger.info("phone:" + str(phone) + " 找回密码验证码发送成功")
            BizId = dict_send_msg['BizId']

            # 让之前 发送的找回密验证码全部失效
            phone_verify_records = PhoneVerifyRecord.objects.filter(phone=str(phone), send_type="sms_login",
                                                                    record_validity="valid")
            #
            for phone_verify_record in phone_verify_records:
                phone_verify_record.record_validity = "invalid"
                phone_verify_record.save()
                logger.info(
                    "phone:" + str(phone_verify_record.phone) + " code:" + str(
                        phone_verify_record.code) + " 让之前的找回密码验证码失效")

            phone_record = PhoneVerifyRecord()
            phone_record.phone = str(phone)
            phone_record.code = str(code)
            phone_record.send_type = send_type
            phone_record.BizId = BizId
            phone_record.save()

            logger.info("phone:" + str(phone) + " 发送成功的手机找回密码验证码存入数据库！")

            # TODO: 异步任务使得
            # return dict_status[send_status]

            scheduler = BackgroundScheduler()
            # datetime.timedelta(days=1))
            dead_time = datetime.datetime.now() + datetime.timedelta(minutes=5, seconds=0)
            # print("dead_time:", dead_time)
            scheduler.add_job(dead_phone_verify_records, 'date', run_date=dead_time,
                              args=[[phone_record]])
            scheduler.start()
            logger.info("phone:" + str(phone) + " 发送成功的手机注册验证码存入数据库！")
            return dict_status[send_status]



        else:
            print("手机验证码发送失败")
            logger.error("phone:" + str(phone) + " 手机找回密码验证码发送失败:" + dict_status[send_status])
            print(dict_status[send_status])  # 打印发送失败的原因  #这里新增log 日志
            return dict_status[send_status]
        pass
    elif send_type == "sms_certification":
        # TODO: 短信验证码登录
        send_msg = send_sms(__business_id, phone, "欧诺嘉三维数字化平台", "SMS_198520055", json_params)
        dict_send_msg = eval(send_msg)  # 把返回的信息转化为字典
        send_status = dict_send_msg.get('Code')  # 获取到发送状态
        # params = u'{"name":"wqb","code":"12345678","address":"bz","phone":"13000000000"}'
        # b'{"Message":"OK","RequestId":"EC69DF87-2D8F-4A95-BF32-6C96A88E1B78","BizId":"489514132684964407^0","Code":"OK"}'

        if send_status == "OK":
            # print("手机找回密码验证码发送成功")
            logger.info("phone:" + str(phone) + " 身份认证 验证码发送成功")
            BizId = dict_send_msg['BizId']

            # 让之前 发送的找回密验证码全部失效
            phone_verify_records = PhoneVerifyRecord.objects.filter(phone=str(phone), send_type="sms_login",
                                                                    record_validity="valid")
            #
            for phone_verify_record in phone_verify_records:
                phone_verify_record.record_validity = "invalid"
                phone_verify_record.save()
                logger.info(
                    "phone:" + str(phone_verify_record.phone) + " code:" + str(
                        phone_verify_record.code) + " 让之前的身份认证验证码失效")

            phone_record = PhoneVerifyRecord()
            phone_record.phone = str(phone)
            phone_record.code = str(code)
            phone_record.send_type = send_type
            phone_record.BizId = BizId
            phone_record.save()

            logger.info("phone:" + str(phone) + " 发送成功的手机找回密码验证码存入数据库！")

            # TODO: 异步任务使得
            # return dict_status[send_status]

            scheduler = BackgroundScheduler()
            # datetime.timedelta(days=1))
            dead_time = datetime.datetime.now() + datetime.timedelta(minutes=5, seconds=0)
            # print("dead_time:", dead_time)
            scheduler.add_job(dead_phone_verify_records, 'date', run_date=dead_time,
                              args=[[phone_record]])
            scheduler.start()
            logger.info("phone:" + str(phone) + " 发送成功的手机注册验证码存入数据库！")
            return dict_status[send_status]



        else:
            print("手机验证码发送失败")
            logger.error("phone:" + str(phone) + " 手机找回密码验证码发送失败:" + dict_status[send_status])
            print(dict_status[send_status])  # 打印发送失败的原因  #这里新增log 日志
            return dict_status[send_status]
        pass
    else:
        logger.error("验证码类型未指定", send_type)
        return "验证码类型未指定"


def send_sms(business_id, phone_numbers, sign_name, template_code, template_param=None):
    """
    :param business_id:
    :param phone_numbers:
    :param sign_name:
    :param template_code:
    :param template_param:
    :return: smsResponse
    """
    smsRequest = SendSmsRequest.SendSmsRequest()
    # 申请的短信模板编码,必填
    smsRequest.set_TemplateCode(template_code)

    # 短信模板变量参数
    if template_param is not None:
        smsRequest.set_TemplateParam(template_param)

    # 设置业务请求流水号，必填。
    smsRequest.set_OutId(business_id)

    # 短信签名
    smsRequest.set_SignName(sign_name)

    # 数据提交方式
    # smsRequest.set_method(MT.POST)

    # 数据提交格式
    # smsRequest.set_accept_format(FT.JSON)

    # 短信发送的号码列表，必填。
    smsRequest.set_PhoneNumbers(phone_numbers)

    # 调用短信发送接口，返回json
    smsResponse = acs_client.do_action_with_exception(smsRequest)

    # TODO 业务处理

    return smsResponse


def dead_phone_verify_records(phone_verify_records):
    print("dead_phone_verify_records")
    for phone_verify_record in phone_verify_records:
        phone_verify_record.record_validity = "invalid"
        phone_verify_record.save()
        print("invalid")


WEBSOCKET = websockets.serve(echo, 'localhost', 8765)
print(WEBSOCKET)

if __name__ == '__main__':
    __business_id = uuid.uuid1()
    # print(__business_id)
    params = {"code": "123456", }
    json_params = json.dumps(params)  # 把字典转化为json
    print(json_params)
    # params = u'{"name":"wqb","code":"12345678","address":"bz","phone":"13000000000"}'
    print(eval(send_sms(__business_id, "18210540120", "欧诺嘉三维数字化平台", "SMS_197210215", json_params)))
