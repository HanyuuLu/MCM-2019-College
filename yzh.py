def t1(S_sum, freeRate) -> int:
    return S_sum * freeRate
def t2(S_sum, serviceRate) -> int:
    return S_sum * serviceRate
def t3(pay_sum,ad_free) -> int:
    return pay_sum * ad_free / 1000
def t4(sedMoney, s1, r,customerBalance,S_sum) -> int:
    assert len(sedMoney) == 12
    copyCustomerBalance = customerBalance
    print(copyCustomerBalance)
    for i in range(len(sedMoney)):
        for x in range(1, 12 - i):
            sedMoney[i] = (1 + r) * sedMoney[i]
    for x in range(1,13):
        customerBalance = (1 + r) * customerBalance
    return (customerBalance)*(1-s1)-copyCustomerBalance- S_sum + (sum(sedMoney))*(1-s1)
def o1(v_machine, v_maintain, n_machine, s) -> int:
    return n_machine * (v_machine + v_maintain) + s

def o2(n_ad, v_ad) -> int:
    return n_ad * v_ad
def w(input):
    return \
        t1(input['sum'], input['freeRate']) +\
        t2(input['sum'], input['serviceRate']) + \
        t3(input['paySum'], input['adFree']) + \
        t4(input['sedMoney'], input['s1'], input['r'], input['customerBalance'], input['S_sum']) - \
        o1(input['v_machine'], input['v_maintain'], input['n_machine'], input['s']) - \
        o2(input['n_ad'],input['v_ad'])



if __name__ == '__main__':
    input = {
        "S_sum": None,  # 年度营业额
        'freeRate': None,  # 手续费费率
        'serviceRate': None,  # 服务费费率
        'pay_sum': None,  # 交易笔数
        'ad_free':None, # 广告费用/每一千次观看
        'customerBalance': None,  # 总用户余额
        'sedMoney': list(),  # 月营业额
        'n_machine': None,  # 机器数量
        'v_machine': None,  # 机器单价
        'v_maintain': None,  # 维护单价
        's': None,   # 劳动力成本
        'n_ad': None,  # 广告数量
        'v_ad': None,  # 广告单价
        'r': None,  # 沉淀资金增长率
        's1':None,  # 银行手续费
    }
    input['S_sum'] = 43800
    input['freeRate']= 0.001 
    input['serviceRate']=0.006
    input['pay_sum'] = 21900
    input['ad_free']=60
    input['customerBalance'] = 1300
    input['sedMoney'] = [3650, 3650, 3650, 3650, 3650, 3650, 3650, 3650, 3650, 3650, 3650, 3650]
    input['n_machine']= 0.1
    input['v_machine']= 500
    input['v_maintain']=20
    input['s']= 200
    input['n_ad']=10
    
    input['v_ad']=1
    input['r']=0.0375/12
    input['s1']=0.0078
    print(t1(input['S_sum'],input['freeRate'])+t2(input['S_sum'],input['serviceRate'])+t3(input['pay_sum'],input['ad_free'])\
    +t4(input['sedMoney'],input['s1'],input['r'],input['customerBalance'],input['S_sum'])-o1(input['v_machine'],input['v_maintain'],input['n_machine'],input['s'])-o2(input['n_ad'],input['v_ad']))

